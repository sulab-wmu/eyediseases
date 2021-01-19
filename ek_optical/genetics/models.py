#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import re

from sqlalchemy.dialects.postgresql import UUID

from ek_optical.extensions import db
from ek_optical.util import uuid4_string

OMIM_GROUP_PATTERN = re.compile(r'(.*)\s+([a-zA-Z:\d]+)\s(.*)')


class GeneExpression(db.Model):
    __tablename__ = 'gene_expression'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    gene_id = db.Column(db.String(32), nullable=True)
    disease = db.Column(db.String(255), nullable=True)
    gene = db.Column(db.String(32), nullable=True, index=True)
    value = db.Column(db.Float, nullable=True)
    color = db.Column(db.String(50), nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'gene_id': self.gene_id,
            'disease': self.disease,
            'gene': self.gene,
            'value': self.value or 0
        }


class Gene(db.Model):
    __tablename__ = 'gene'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    symbol = db.Column(db.String(32), nullable=True)
    name = db.Column(db.String(128), nullable=True)
    synonyms = db.Column(db.String(255), nullable=True)
    gene_type = db.Column(db.String(128), nullable=True)
    location = db.Column(db.Text, nullable=True)
    strand = db.Column(db.String(32), nullable=True)
    description = db.Column(db.Text, nullable=True)
    omim = db.Column(db.String(16), nullable=True)
    ensembl = db.Column(db.String(32), nullable=True)
    clinvar = db.Column(db.String(128), nullable=True)
    decipher = db.Column(db.String(128), nullable=True)
    gnomad = db.Column(db.String(128), nullable=True)
    panelapp = db.Column(db.String(128), nullable=True)
    eye_disease = db.Column(db.Text, nullable=True)
    phenotypes = db.Column(db.Text, nullable=True)
    drugbank_id = db.Column(db.Text, nullable=True)
    drug_target = db.Column(db.Text, nullable=True)

    def to_list(self):
        return {
            'id': self.id,
            'name': self.symbol,
        }

    def to_json(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'ensembl': self.ensembl,
            'synonyms': self.synonyms,
            'location': self.location_split(),
            'clinvar': self.clinvar,
            'decipher': self.decipher,
            'gnomad': self.gnomad,
            'panelapp': self.panelapp,
            'description': self.description,
            'drug_target': self.drug_target_obj(),
            'drugbank_id': self.drugbank_id,
            'eye_disease': self.eye_disease,
            'gene_type': self.gene_type,
            'name': self.name,
            'omim': self.omim,
            'phenotypes': self.hpo_phenotypes_obj(),
            'strand': self.strand,
        }

    def location_split(self):
        rs = self.location.split("(GRCh38/hg38)")
        rs[0] = rs[0] + "(GRCh38/hg38)"
        return rs

    def drug_target_obj(self):
        if not self.drug_target:
            return []

        def to_to_group(a):
            g_value, g_name = a.split(':')
            return {
                'value': g_value,
                'name': g_name
            }

        result = [to_to_group(c) for c in (self.drug_target.split(';')[0:-1])]
        return result

    def hpo_phenotypes_obj(self):
        if not self.phenotypes:
            return []

        def to_group(a):
            disease, ref_id, color = OMIM_GROUP_PATTERN.match(a).groups()
            return {
                'name': disease,
                'omim': ref_id,
                'color': color
            }

        result = [to_group(c) for c in (self.phenotypes.split(';')[0:-1])]
        return sorted(result, key=lambda t: t['color'] if t['color'] != 'grey' else 'z')
