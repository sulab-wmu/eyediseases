#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from sqlalchemy.dialects.postgresql import UUID

from ek_optical.extensions import db
from ek_optical.util import uuid4_string


class GeneticGWAS(db.Model):
    __tablename__ = 'genetic_gwas'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    gene_id = db.Column(db.String(16), nullable=True)
    chromosome = db.Column(db.String(2), nullable=True)
    scope = db.Column(db.String(16), nullable=True)
    gene = db.Column(db.String(32), nullable=True)
    variant = db.Column(db.String(255), nullable=True)
    major_allele = db.Column(db.String(32), nullable=True)
    minor_allele = db.Column(db.String(128), nullable=True)
    band = db.Column(db.String(32), nullable=True)
    ensembl = db.Column(db.String(255), nullable=True)
    p_value = db.Column(db.Float, nullable=True)
    beta = db.Column(db.Float, nullable=True)
    context = db.Column(db.String(128), nullable=True)
    cadd = db.Column(db.String(32), nullable=True)
    polyphen = db.Column(db.String(32), nullable=True)
    sift = db.Column(db.String(32), nullable=True)
    phylop = db.Column(db.String(32), nullable=True)
    study = db.Column(db.Text, nullable=True)
    initial_sample_size = db.Column(db.Text, nullable=True)
    peplication_sample_size = db.Column(db.Text, nullable=True)
    disease = db.Column(db.String(255), nullable=True, index=True)
    pubmed = db.Column(db.String(255), nullable=True)
    drug = db.Column(db.String(32), nullable=True)

    def to_variant(self):
        return {
            'id': self.variant,
            'name': self.variant,
            'type': 'variant'
        }

    def to_json(self):
        return {
            'id': self.id,
            'gene_id': self.gene_id,
            'chromosome': self.chromosome,
            'scope': self.scope,
            'variant_': self.variant,
            'gene': self.gene,
            'major_allele': self.major_allele,
            'minor_allele': self.minor_allele,
            'band': self.band,
            'ensembl': self.ensembl,
            'p_value': self.p_value,
            'beta': self.beta,
            'context': self.context,
            'cadd': self.cadd,
            'polyphen': self.polyphen,
            'sift': self.sift,
            'phylop': self.phylop,
            'study': self.study,
            'initial_sample_size': self.initial_sample_size,
            'peplication_sample_size': self.peplication_sample_size,
            'disease': self.disease,
            'pubmed': self.pubmed,
        }

    def to_json_disease(self):
        return {
            'gene_id': self.gene_id,
            'symbol': self.gene,
            'band': self.band,
            'variants': self.variant,
            'position_hg38': self.ensembl.lower(),
            'major_allele': self.major_allele,
            'minor_allele': self.minor_allele,
            'p_value': self.p_value,
            'beta': self.beta,
            'context': self.context,
            'cadd': self.cadd,
            'initial': self.initial_sample_size,
            'peplication': self.peplication_sample_size,
            'pubmed': self.pubmed,
            'disease': self.disease,
        }


class GeneticOMIM(db.Model):
    __tablename__ = 'genetic_omim'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    gene_id = db.Column(db.String(32), nullable=True)
    gene = db.Column(db.String(32), nullable=True)
    gene_name = db.Column(db.String(128), nullable=True)
    variant = db.Column(db.String(255), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    band = db.Column(db.String(32), nullable=True)
    omim = db.Column(db.String(16), nullable=True)
    ensembl = db.Column(db.String(128), nullable=True)
    synonyms = db.Column(db.String(128), nullable=True)
    location = db.Column(db.Text, nullable=True)
    clinvar = db.Column(db.Text, nullable=True)
    decipher = db.Column(db.Text, nullable=True)
    gnomad = db.Column(db.Text, nullable=True)
    pubmed = db.Column(db.Text, nullable=True)
    disease = db.Column(db.String(255), nullable=True, index=True)
    disease_omim = db.Column(db.String(16), nullable=True)
    confidence = db.Column(db.String(32), nullable=True)
    publications = db.Column(db.Text, nullable=True)
    phenotypes_in_omim = db.Column(db.Text, nullable=True)
    phenotypes_in_hpo = db.Column(db.String(128), nullable=True)
    drug = db.Column(db.String(32), nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'gene_id': self.gene_id,
            'gene': self.gene,
            'gene_name': self.gene_name,
            'variant': self.variant,
            'summary': self.summary,
            'band': self.band,
            'omim': self.omim,
            'ensembl': self.ensembl,
            'synonyms': self.synonyms,
            'location': self.location,
            'clinvar': self.clinvar,
            'decipher': self.decipher,
            'gnomad': self.gnomad,
            'disease': self.disease,
            'pubmed': self.pubmed,
            'disease_omim': self.disease_omim,
            'confidence': self.confidence,
            'publications': self.publications,
            'phenotypes_in_omim': self.phenotypes_in_omim,
            'phenotypes_in_hpo': self.phenotypes_in_hpo,
        }

    def to_json_disease(self):
        return {
            "gene_id": self.gene_id,
            "symbol": self.gene,
            "band": self.band,
            "name": self.gene_name,
            "variants": self.variant,
            "ensembl": self.ensembl,
            "omim": self.omim,
            'phenotype': self.phenotypes_in_omim,
            "confidence": self.confidence,
            'pubmed': self.pubmed,
            'disease': self.disease,
        }
