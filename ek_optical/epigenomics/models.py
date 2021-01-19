#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from sqlalchemy.dialects.postgresql import UUID, JSONB

from ek_optical.extensions import db
from ek_optical.util import uuid4_string


class Epigenomics(db.Model):
    __tablename__ = 'epigenomics'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    file_url = db.Column(db.String(256), nullable=False)
    disease = db.Column(db.String(128), nullable=False)
    data_type = db.Column(db.String(16), nullable=False)

    def to_json(self, **kwargs):
        result = {
            'id': self.id,
            'url': self.file_url,
            'disease': self.disease,
            'data_type': self.data_type,
            'data_key': self.disease + '/' + self.data_type,
        }
        result.update(kwargs)
        return result


class AppConfig(db.Model):
    __tablename__ = 'app_config'

    key = db.Column(db.Text(), primary_key=True)
    value = db.Column(JSONB(), nullable=True)

    @classmethod
    def get_config_value(cls, key):
        config = db.session.query(cls).get(key)
        return config.value if config else None
