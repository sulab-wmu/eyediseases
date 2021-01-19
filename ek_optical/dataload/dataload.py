#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import os

import pandas as pd
from flask import json

from ek_optical.util import uuid4_string


def read_snp_summary(file):
    summary = pd.read_csv(file, delimiter='\t', header=None, names=['variants', 'gene', 'protein_change', 'consequence', 'prediction'])
    return summary


def joint_area_json(df):
    for row in df.index:
        rs_row_data = {}
        for col in range(4, df.columns.size):
            vl_col = str(df.iloc[row, col])
            if vl_col != 'nan':
                dict_area = vl_col.split("=")
                rs_row_data[dict_area[0]] = dict_area[1]

        df.iloc[row, 3] = json.dumps(rs_row_data)

    return df


def read_gnomad(file):
    df = pd.read_csv(file, delimiter='\t', header=None)
    new_columns_list = ['chromosome', 'scope', 'variant', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'a11']
    new_columns = pd.core.indexes.base.Index(new_columns_list)
    df.columns = new_columns
    col_name = df.columns.tolist()
    col_name.insert(3, 'territory')
    df = df.reindex(columns=col_name)
    df = joint_area_json(df)
    df = df.loc[:, ['chromosome', 'scope', 'variant', 'territory']]
    return df


def read_gene_expression(file):
    gene = pd.read_csv(file, delimiter='\t')
    gene = gene.drop(labels=0)
    col = gene.columns.tolist()
    gene = gene.melt(id_vars=['Gene_Symbol', '-'], value_vars=col[2:19108])
    gene.rename(columns={'-': 'disease', 'Gene_Symbol': 'gene_id', 'variable': 'gene'}, inplace=True)

    return gene


def insert_uuid4(df):
    col = df.columns.tolist()
    col.insert(0, 'id')
    df = df.reindex(columns=col)
    df['id'] = [uuid4_string() for i in range(len(df))]
    return df


def insert_file_marker(df, file):
    file_name = os.path.basename(file).split('.')[0]
    col = df.columns.tolist()

    if file_name == 'GSE134355':
        col.insert(3, 'labels')
        df = df.reindex(columns=col)
        df['cell_type'] = [None for i in range(len(df))]

    col.insert(9, 'cell_type')
    df = df.reindex(columns=col)
    df['cell_type'] = [file_name for i in range(len(df))]

    return df


def insert_file_out(df, file):
    file_name = os.path.basename(file).split('.')[0]
    print(file_name)
    col = df.columns.tolist()

    col.insert(6, 'cell_type')
    df = df.reindex(columns=col)
    df['cell_type'] = [file_name for i in range(len(df))]

    return df


def insert_dis_type(df, file):
    file_name = os.path.basename(file).split('.')
    dis_name, dis_type = file_name[0], file_name[1]
    col = df.columns.tolist()

    col.insert(0, 'disease')
    col.insert(1, 'dataset')
    df = df.reindex(columns=col)
    df['disease'] = [dis_name for i in range(len(df))]
    df['dataset'] = [dis_type for i in range(len(df))]

    return df
