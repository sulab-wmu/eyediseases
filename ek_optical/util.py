#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import json
import logging
import logging.config
import os
import uuid

import numpy as np
import pandas as pd
import sqlalchemy
from flask import jsonify
from six import string_types

__all__ = [
    'configure_logging',
    'InvalidUsage',
    'make_dict_response',
    'is_str',
    'create_custom_json_encoder',
    'pandas_obj_to_json',
    'numpy_obj_to_python',
    'uuid4_string',
    'split_params',
    'dedupe_iterable',
    'save_dataframe_using_copy',
    'create_engine_from_env',
]

from sqlalchemy import text


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def _make_logging_config(log_level):
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(name)s [%(threadName)s] %(levelname)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'propagate': True,
                'level': log_level,
            },
        }
    }


def configure_logging(log_level=None):
    # use a variable in the function object to determine if it has run before
    if getattr(configure_logging, 'has_run', False):
        return

    log_level = log_level or 'INFO'

    logging.config.dictConfig(_make_logging_config(log_level))

    logging.captureWarnings(True)

    configure_logging.has_run = True


def make_dict_response(payload=None, status_code=None, **kwargs):
    rv = dict(payload or ())
    rv.update(kwargs)
    response = jsonify(rv)
    response.status_code = status_code or 200
    return response


def is_str(arg):
    return isinstance(arg, string_types)


def numpy_obj_to_python(obj):
    if isinstance(obj, np.ndarray) and obj.ndim == 0:
        return obj.item()
    else:
        return obj


def pandas_obj_to_json(obj):
    if isinstance(obj, pd.DataFrame):
        new_obj = obj.applymap(numpy_obj_to_python)
    elif isinstance(obj, pd.Series):
        new_obj = obj.apply(numpy_obj_to_python)
    else:
        raise ValueError('this cannot happen!')
    return json.loads(new_obj.to_json(orient='split', date_format='iso', default_handler=str))


def create_custom_json_encoder(base_cls):
    class CustomJsonEncoderImpl(base_cls):
        def default(self, obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            if isinstance(obj, pd.DataFrame) or isinstance(obj, pd.Series):
                return pandas_obj_to_json(obj)
            if isinstance(obj, np.ndarray) and obj.ndim <= 1:
                return obj.tolist() if obj.ndim == 1 else obj.item()
            if isinstance(obj, np.bool_):
                return obj.item()
            if isinstance(obj, np.signedinteger):
                return obj.item()
            return base_cls.default(self, obj)

    return CustomJsonEncoderImpl


def uuid4_string():
    return str(uuid.uuid4())


def dedupe_iterable(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


def split_params(texts, delim=',', dedupe=False):
    if texts is None:
        return []

    texts = texts.strip()
    if not texts:
        return []

    splits = (p.strip() for p in texts.split(delim))
    return list(dedupe_iterable(splits) if dedupe else splits)


def _raw_connection_from(engine_or_conn):
    """
    Extract a raw_connection and determine if it should be automatically closed.
    Only connections opened by this package will be closed automatically.
    """
    if hasattr(engine_or_conn, 'cursor'):
        return engine_or_conn, False
    if hasattr(engine_or_conn, 'connection'):
        return engine_or_conn.connection, False
    return engine_or_conn.raw_connection(), True


def fit_dataframe_columns(df, columns, inplace=False):
    """
    Copies or modifies a dataframe with specified columns only,
    missing columns will be added and filled with None.
    If not in place, the returned column order will follow columns parameter.
    """
    original_columns = df.columns
    wanted_column_set = set(columns)
    original_column_set = set(original_columns)

    if len(wanted_column_set) != len(columns):
        raise ValueError('columns is not unique {}'.format(columns))

    missing_columns = wanted_column_set - original_column_set
    columns_to_delete = original_column_set - wanted_column_set

    if not inplace:
        df = df.copy()

    df.drop(columns_to_delete, axis=1, inplace=True)

    for missing_column in (c for c in columns if c in missing_columns):
        df[missing_column] = None

    if not inplace:
        return df[columns]


def get_columns_info(conn, schema, table, raise_if_none=True):
    sql_template = """
        SELECT
          table_catalog,
          table_schema,
          table_name,
          column_name,
          data_type,
          ordinal_position
        FROM information_schema.columns
        WHERE table_schema = :schema AND table_name = :table
        ORDER BY ordinal_position;
    """

    column_info_df = pd.read_sql(text(sql_template), conn, params={'schema': schema, 'table': table})

    if raise_if_none and len(column_info_df.index) == 0:
        raise RuntimeError(f'Could not get column info for {schema}.{table}, does it exist?')

    return column_info_df


def get_columns(conn, schema, table):
    return get_columns_info(conn, schema, table)['column_name'].tolist()


def prepare_dataframe(conn, df, schema, table, column_mappings=None):
    """ Automatically re-adjust the dataframe to have the same columns as specified by the schema and table """
    table_columns = get_columns(conn, schema, table)
    df_copy = df.copy()
    if column_mappings is not None:
        df_copy = df_copy.rename(columns=column_mappings)
    fit_dataframe_columns(df_copy, table_columns, inplace=True)
    return df_copy


def save_dataframe_using_copy(engine_or_conn, df, schema, table, prepare=False):
    """ Persists the dataframe to the schema and table specified, using postgresql's COPY function.
        with engine.begin() as conn:
            save_dataframe_using_copy(conn, option_data_, 'aspect', 'ts_option_price_daily', prepare=True)
    """
    if prepare:
        df = prepare_dataframe(engine_or_conn, df, schema, table)

    from io import StringIO
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    conn, autoclose = _raw_connection_from(engine_or_conn)
    cursor = conn.cursor()
    columns = ', '.join([f'{col}' for col in df.columns])
    sql = f'COPY {schema}.{table} ({columns}) FROM STDIN WITH CSV HEADER'
    cursor.copy_expert(sql=sql, file=csv_buffer)
    cursor.close()
    if autoclose:
        conn.commit()
        conn.close()


# TODO: 删除，用 db.engine
def create_engine_from_env(url, echo=False):
    return sqlalchemy.create_engine(create_engine_url_from_env(url), echo=echo)


def create_engine_url_from_env(url='APP_BIOTOOLS_DB_URL'):
    db_url = os.environ.get(url)
    if not db_url:
        raise RuntimeError('Environment variable APP_BIOTOOLS_DB_URL needs to be set\n' +
                           '  In BASH: export APP_BIOTOOLS_DB_URL=postgresql://<user>:<password>@<host>[:[port]]/<db_name>\n' +
                           '  In FISH: set -x APP_BIOTOOLS_DB_URL postgresql://<user>:<password>@<host>[:[port]]/<db_name>\n' +
                           'To unset, BASH: unset APP_BIOTOOLS_DB_URL, FISH: set -e APP_BIOTOOLS_DB_URL')
    return db_url
