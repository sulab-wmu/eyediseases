#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID

from ek_optical.extensions import db
from ek_optical.util import uuid4_string


class GeneNetworkDisease(db.Model):
    __tablename__ = 'gene_network_disease'

    id = db.Column(UUID(as_uuid=True), default=uuid4_string, primary_key=True)
    gene = db.Column(db.String(32), nullable=True)
    disease = db.Column(db.String(255), nullable=True)
    weight = db.Column(db.Float, nullable=True)
    dataset = db.Column(db.String(8), nullable=True)


class DiseaseGo(db.Model):
    __tablename__ = 'disease_go'

    id = db.Column(UUID(as_uuid=True), default=uuid4_string, primary_key=True)
    disease = db.Column(db.String(255), nullable=True)
    dataset = db.Column(db.String(8), nullable=True)
    category = db.Column(db.String(128), nullable=True)
    term = db.Column(db.Text, nullable=True)
    count = db.Column(db.Integer, nullable=True)
    percent = db.Column(db.Float, nullable=True)
    p_value = db.Column(db.Float, nullable=True)
    genes = db.Column(db.Text, nullable=True)
    list_total = db.Column(db.Integer, nullable=True)
    pop_hits = db.Column(db.Integer, nullable=True)
    pop_total = db.Column(db.Integer, nullable=True)
    fold_enrichment = db.Column(db.Float, nullable=True)
    bonferroni = db.Column(db.Float, nullable=True)
    benjamini = db.Column(db.Float, nullable=True)
    fdr = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'disease': self.disease,
            'dataset': self.dataset,
            'category': self.category,
            'term': self.term,
            'count': self.count,
            'percent': self.percent,
            'p_value': self.p_value,
            'genes': self.genes,
            'list_total': self.list_total,
            'pop_hits': self.pop_hits,
            'pop_total': self.pop_total,
            'fold_enrichment': round(self.fold_enrichment, 2),
            'bonferroni': self.bonferroni,
            'benjamini': self.benjamini,
            'fdr': round(self.fdr, 2)
        }


class Keratoconus(db.Model):
    __tablename__ = 'keratoconus'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    gene = db.Column(db.String(32), nullable=True)
    contrast_gene = db.Column(db.String(32), nullable=True)
    weight = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'contrast_gene': self.contrast_gene,
            'weight': self.weight
        }

    def to_reverse_json(self):
        return {
            'gene': self.contrast_gene,
            'contrast_gene': self.gene,
            'weight': self.weight
        }


class Retinoblastoma(db.Model):
    __tablename__ = 'retinoblastoma'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    gene = db.Column(db.String(32), nullable=True)
    contrast_gene = db.Column(db.String(32), nullable=True)
    weight = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'contrast_gene': self.contrast_gene,
            'weight': self.weight
        }

    def to_reverse_json(self):
        return {
            'gene': self.contrast_gene,
            'contrast_gene': self.gene,
            'weight': self.weight
        }


class AgeRelatedMacularDegeneration(db.Model):
    __tablename__ = 'age_related_macular_degeneration'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    gene = db.Column(db.String(32), nullable=True)
    contrast_gene = db.Column(db.String(32), nullable=True)
    weight = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'contrast_gene': self.contrast_gene,
            'weight': self.weight
        }

    def to_reverse_json(self):
        return {
            'gene': self.contrast_gene,
            'contrast_gene': self.gene,
            'weight': self.weight
        }


class GeneDiseaseCorrect(db.Model):
    __tablename__ = 'gene_disease_correct'

    id = db.Column(UUID(as_uuid=True), default=uuid4_string, primary_key=True)
    gene = db.Column(db.String(32), nullable=True)
    module = db.Column(db.String(32), nullable=True)
    kme = db.Column(db.Float, nullable=True)
    disease = db.Column(db.String(64), nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'module': self.module,
            'kme': self.kme,
        }


class GeneDiseaseSignificance(db.Model):
    __tablename__ = 'gene_disease_significance'

    id = db.Column(UUID(as_uuid=True), default=uuid4_string, primary_key=True)
    gene = db.Column(db.String(32), nullable=True)
    amd = db.Column(db.Float, nullable=True)
    dr = db.Column(db.Float, nullable=True)
    kc = db.Column(db.Float, nullable=True)
    glc = db.Column(db.Float, nullable=True)
    rp = db.Column(db.Float, nullable=True)
    rb = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'gene': self.gene,
            'amd': self.amd,
            'dr': self.dr,
            'kc': self.kc,
            'glc': self.glc,
            'rp': self.rp,
            'rb': self.rb
        }


class CornealEndothelialCells(db.Model):
    __tablename__ = 'corneal_endothelial_cells'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    gene = db.Column(db.String(32), nullable=True)
    contrast_gene = db.Column(db.String(32), nullable=True)
    weight = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'contrast_gene': self.contrast_gene,
            'weight': self.weight
        }

    def to_reverse_json(self):
        return {
            'gene': self.contrast_gene,
            'contrast_gene': self.gene,
            'weight': self.weight
        }


class RetinaNonMacula(db.Model):
    __tablename__ = 'retina_non_macula'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    gene = db.Column(db.String(32), nullable=True)
    contrast_gene = db.Column(db.String(32), nullable=True)
    weight = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'contrast_gene': self.contrast_gene,
            'weight': self.weight
        }

    def to_reverse_json(self):
        return {
            'gene': self.contrast_gene,
            'contrast_gene': self.gene,
            'weight': self.weight
        }


class NonMacula(db.Model):
    __tablename__ = 'non_macula'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    gene = db.Column(db.String(32), nullable=True)
    contrast_gene = db.Column(db.String(32), nullable=True)
    weight = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'contrast_gene': self.contrast_gene,
            'weight': self.weight
        }

    def to_reverse_json(self):
        return {
            'gene': self.contrast_gene,
            'contrast_gene': self.gene,
            'weight': self.weight
        }


class RetinaMacula(db.Model):
    __tablename__ = 'retina_macula'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    gene = db.Column(db.String(32), nullable=True)
    contrast_gene = db.Column(db.String(32), nullable=True)
    weight = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'contrast_gene': self.contrast_gene,
            'weight': self.weight
        }

    def to_reverse_json(self):
        return {
            'gene': self.contrast_gene,
            'contrast_gene': self.gene,
            'weight': self.weight
        }


class Macula(db.Model):
    __tablename__ = 'macula'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    gene = db.Column(db.String(32), nullable=True)
    contrast_gene = db.Column(db.String(32), nullable=True)
    weight = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'contrast_gene': self.contrast_gene,
            'weight': self.weight
        }

    def to_reverse_json(self):
        return {
            'gene': self.contrast_gene,
            'contrast_gene': self.gene,
            'weight': self.weight
        }


class Retina(db.Model):
    __tablename__ = 'retina'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    gene = db.Column(db.String(32), nullable=True)
    contrast_gene = db.Column(db.String(32), nullable=True)
    weight = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'contrast_gene': self.contrast_gene,
            'weight': self.weight
        }

    def to_reverse_json(self):
        return {
            'gene': self.contrast_gene,
            'contrast_gene': self.gene,
            'weight': self.weight
        }


class Corneal(db.Model):
    __tablename__ = 'corneal'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    gene = db.Column(db.String(32), nullable=True)
    contrast_gene = db.Column(db.String(32), nullable=True)
    weight = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'contrast_gene': self.contrast_gene,
            'weight': self.weight
        }

    def to_reverse_json(self):
        return {
            'gene': self.contrast_gene,
            'contrast_gene': self.gene,
            'weight': self.weight
        }


class GeneTissueCorrect(db.Model):
    __tablename__ = 'gene_tissue_correct'

    id = db.Column(UUID(as_uuid=True), default=uuid4_string, primary_key=True)
    gene = db.Column(db.String(32), nullable=True)
    module = db.Column(db.String(32), nullable=True)
    kme = db.Column(db.String(32), nullable=True)
    tissue = db.Column(db.String(32), nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'module': self.module,
            'kme': self.kme,
        }


class TissueGeneSignificance(db.Model):
    __tablename__ = 'tissue_gene_significance'

    id = db.Column(UUID(as_uuid=True), default=uuid4_string, primary_key=True)
    gene_symbol = db.Column(db.String(128), nullable=True)
    corneas = db.Column(db.Float, nullable=True)
    corneal_endothelial_cells = db.Column(db.Float, nullable=True)
    retina = db.Column(db.Float, nullable=True)
    retina_macula = db.Column(db.Float, nullable=True)
    retina_non_macula = db.Column(db.Float, nullable=True)
    rpe_macula = db.Column(db.Float, nullable=True)
    rpe_non_macula = db.Column(db.Float, nullable=True)
    retinal_endothelial_cells = db.Column(db.Float, nullable=True)
    ipsc_derived_retinal_organoids = db.Column(db.Float, nullable=True)
    trabecular_meshwork_cells = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'gene_symbol': self.gene_symbol,
            'corneas': self.corneas,
            'corneal_endothelial_cells': self.corneal_endothelial_cells,
            'retina': self.retina,
            'retina_macula': self.retina_macula,
            'retina_non_macula': self.retina_non_macula,
            'rpe_macula': self.rpe_macula,
            'rpe_non_macula': self.rpe_non_macula,
            'retinal_endothelial_cells': self.retinal_endothelial_cells,
            'ipsc_derived_retinal_organoids': self.ipsc_derived_retinal_organoids,
            'trabecular_meshwork_cells': self.trabecular_meshwork_cells,
        }


class EpigeneticAlteration(db.Model):
    __tablename__ = 'epigenetic_alteration'

    id = db.Column(UUID(as_uuid=True), default=uuid4_string, primary_key=True)
    gene = db.Column(db.String(128), nullable=True, index=True)
    normal_retina = db.Column(db.Float, nullable=True)
    amd_retina = db.Column(db.Float, nullable=True)
    normal_rpe = db.Column(db.Float, nullable=True)
    amd_rpe = db.Column(db.Float, nullable=True)

    def to_json(self):
        return {
            'gene': self.gene,
            'normal_retina': self.normal_retina,
            'amd_retina': self.amd_retina,
            'normal_rpe': self.normal_retina,
            'amd_rpe': self.amd_rpe
        }
