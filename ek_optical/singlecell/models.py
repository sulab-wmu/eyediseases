#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from sqlalchemy.dialects.postgresql import UUID

from ek_optical.extensions import db
from ek_optical.util import uuid4_string


class MarkersCell(db.Model):
    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    gene = db.Column(db.String(128), nullable=True)
    cluster = db.Column(db.Integer, nullable=True)
    labels = db.Column(db.String(128), nullable=True)
    p_val = db.Column(db.Float, nullable=True)
    avg = db.Column(db.Float, nullable=True)
    p_val_adj = db.Column(db.Float, nullable=True)
    pct1 = db.Column(db.Float, nullable=True)
    pct2 = db.Column(db.Float, nullable=True)
    cell_type = db.Column(db.String(32), nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'gene': self.gene,
            'cluster': self.cluster,
            'labels': self.labels,
            'p_val': self.p_val,
            'avg_logFC': self.avg,
            'p_val_adj': self.p_val_adj,
            'pct.1': self.pct1,
            'pct.2': self.pct2,
        }


class OutCell(db.Model):
    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    name = db.Column(db.String(128), nullable=True)
    xaxis = db.Column(db.Float, nullable=True)
    yaxis = db.Column(db.Float, nullable=True)
    cluster = db.Column(db.String(4), nullable=True)
    labels = db.Column(db.String(64), nullable=True)
    cell_type = db.Column(db.String(32), nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'xaxis': self.xaxis,
            'yaxis': self.yaxis,
            'cluster': self.cluster,
            'labels': self.labels,
        }
