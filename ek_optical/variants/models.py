#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from sqlalchemy.dialects.postgresql import UUID, JSONB

from ek_optical.extensions import db
from ek_optical.util import uuid4_string


class Causality(db.Model):
    __tablename__ = 'causality'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    variant = db.Column(db.String(16), nullable=True, index=True)
    p_value = db.Column(db.Float, nullable=True)
    beta = db.Column(db.Float, nullable=True)
    disease = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(50), nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'variant': self.variant,
            'p_value': self.p_value,
            'beta': self.beta or 0,
            'disease': self.disease,
            'color': self.color
        }


class Gnomad(db.Model):
    __tablename__ = 'gnomad'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    chromosome = db.Column(db.String(2), nullable=True)
    scope = db.Column(db.String(16), nullable=True)
    variant = db.Column(db.String(16), nullable=True, index=True)
    territory = db.deferred(db.Column(JSONB, default={}, nullable=True))

    def to_json(self):
        return {
            'id': self.id,
            'chromosome': self.chromosome,
            'scope': self.scope,
            'variant': self.variant,
            'territory': self.territory,
        }


class Summary(db.Model):
    __tablename__ = 'summary'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    snpid = db.Column(db.String(32), nullable=True)
    position_hg38 = db.Column(db.String(32), nullable=True)
    major_allele = db.Column(db.String(1024), nullable=True)
    variant = db.Column(db.String(128), nullable=True)
    protein = db.Column(db.String(64), nullable=True)
    polyphen = db.Column(db.String(32), nullable=True)
    cadd = db.Column(db.String(32), nullable=True)
    sift = db.Column(db.String(32), nullable=True)
    gerp = db.Column(db.String(32), nullable=True)
    gene = db.Column(db.String(128), nullable=True)
    ensembl = db.Column(db.Text, nullable=True)
    dbsnp = db.Column(db.Text, nullable=True)
    gnomad = db.Column(db.Text, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'snpid': self.snpid,
            'position_hg38': self.position_hg38,
            'major_allele': self.major_allele,
            'variant': self.variant,
            'protein': self.protein,
            'polyphen': self.polyphen,
            'cadd': self.cadd,
            'sift': self.sift,
            'gerp': self.gerp,
            'gene': self.gene,
            'ensembl': self.ensembl,
            'dbsnp': self.dbsnp,
            'gnomad': self.gnomad,
        }

    def to_list(self):
        return {
            'id': self.id,
            'name': self.snpid,
        }
