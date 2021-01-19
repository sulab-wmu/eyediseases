#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from sqlalchemy.dialects.postgresql import UUID

from ek_optical.extensions import db
from ek_optical.util import uuid4_string


class MappingTableMixin(object):
    @classmethod
    def reverse_column_mappings(cls):
        return {v: k for k, v in cls.column_mappings().items()}

    @classmethod
    def data_columns(cls):
        return list(cls.column_mappings().values())

    @classmethod
    def map_to_names(cls, _dict):
        mappings = cls.column_mappings()
        return {mappings.get(k, k): v for k, v in _dict.items()}


class ExpressionMouse(db.Model, MappingTableMixin):
    __tablename__ = 'expression_mouse'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    gene = db.Column(db.String(128), nullable=True)
    human = db.Column(db.String(255), nullable=True)
    e10_5 = db.Column(db.Float, nullable=True)
    e11_5 = db.Column(db.Float, nullable=True)
    e12_5 = db.Column(db.Float, nullable=True)
    e13_5 = db.Column(db.Float, nullable=True)
    web1_e10_5__12_5 = db.Column(db.Float, nullable=True)
    web2_e11_5__13_5 = db.Column(db.Float, nullable=True)
    p8_a = db.Column(db.Float, nullable=True)
    p8_b = db.Column(db.Float, nullable=True)
    p12_a = db.Column(db.Float, nullable=True)
    p12_b = db.Column(db.Float, nullable=True)
    p20_a = db.Column(db.Float, nullable=True)
    p20_b = db.Column(db.Float, nullable=True)
    p42_a = db.Column(db.Float, nullable=True)
    p42_b = db.Column(db.Float, nullable=True)
    p52_a = db.Column(db.Float, nullable=True)
    p52_b = db.Column(db.Float, nullable=True)
    web_p10_11_12_a = db.Column(db.Float, nullable=True)
    web_p10_11_12_b = db.Column(db.Float, nullable=True)

    def to_json(self):
        result = {
            'id': self.id,
            'gene': self.gene,
            'human': self.human,
            'e10_5': self.e10_5,
            'e11_5': self.e11_5,
            'e12_5': self.e12_5,
            'e13_5': self.e13_5,
            'web1_e10_5__12_5': self.web1_e10_5__12_5,
            'web2_e11_5__13_5': self.web2_e11_5__13_5,
            'p8_a': self.p8_a,
            'p8_b': self.p8_b,
            'p12_a': self.p12_a,
            'p12_b': self.p12_b,
            'p20_a': self.p20_a,
            'p20_b': self.p20_b,
            'p42_a': self.p42_a,
            'p42_b': self.p42_b,
            'p52_a': self.p52_a,
            'p52_b': self.p52_b,
            'web_p10_11_12_a': self.web_p10_11_12_a,
            'web_p10_11_12_b': self.web_p10_11_12_b,
        }
        return self.map_to_names(result)

    @classmethod
    def column_mappings(cls):
        return {
            'e10_5': 'E10.5',
            'e11_5': 'E11.5',
            'e12_5': 'E12.5',
            'e13_5': 'E13.5',
            'web1_e10_5__12_5': 'WEB1(E10.5-12.5)',
            'web2_e11_5__13_5': 'WEB2(E11.5-13.5)',
            'p8_a': 'P8_A',
            'p8_b': 'P8_B',
            'p12_a': 'P12_A',
            'p12_b': 'P12_B',
            'p20_a': 'P20_A',
            'p20_b': 'P20_B',
            'p42_a': 'P42_A',
            'p42_b': 'P42_B',
            'p52_a': 'P52_A',
            'p52_b': 'P52_B',
            'web_p10_11_12_a': 'WEB(P10_11_12_A)',
            'web_p10_11_12_b': 'WEB(P10_11_12_B)',
        }


class ExpressionRNASeqTissue(db.Model, MappingTableMixin):
    __tablename__ = 'expression_rna_seq_tissue'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    gene = db.Column(db.String(128), nullable=True, index=True)
    ensembl_id = db.Column(db.String(128), nullable=True)

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
        result = {
            'id': self.id,
            'gene': self.gene,
            'ensembl_id': self.ensembl_id,
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
        return self.map_to_names(result)

    def to_json_analysis(self):
        result = {
            'id': self.id,
            'gene': self.gene,
            'ensembl_id': self.ensembl_id,
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
        return result

    @classmethod
    def column_mappings(cls):
        return {
            'corneas': 'Corneas',
            'corneal_endothelial_cells': 'Corneal endothelial cells',
            'retina': 'Retina',
            'retina_macula': 'Retina macula',
            'retina_non_macula': 'Retina non-macula',
            'rpe_macula': 'RPE macula',
            'rpe_non_macula': 'RPE non-macula',
            'retinal_endothelial_cells': 'Retinal endothelial cells',
            'ipsc_derived_retinal_organoids': 'iPSC-derived retinal organoids',
            'trabecular_meshwork_cells': 'Trabecular meshwork cells',
        }


class ExpressionRNASeqDisease(db.Model, MappingTableMixin):
    __tablename__ = 'expression_rna_seq_disease'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    gene = db.Column(db.String(128), nullable=True, index=True)
    ensembl_id = db.Column(db.String(128), nullable=True)

    age_related_macular_degeneration = db.Column(db.Float, nullable=True)
    diabetic_retinopathy = db.Column(db.Float, nullable=True)
    keratoconus = db.Column(db.Float, nullable=True)
    primary_open_angle_glaucoma = db.Column(db.Float, nullable=True)
    retinitis_pigmentosa = db.Column(db.Float, nullable=True)
    retinoblastoma = db.Column(db.Float, nullable=True)

    def to_json(self):
        result = {
            'id': self.id,
            'gene': self.gene,
            'ensembl_id': self.ensembl_id,
            'age_related_macular_degeneration': self.age_related_macular_degeneration,
            'diabetic_retinopathy': self.diabetic_retinopathy,
            'keratoconus': self.keratoconus,
            'primary_open_angle_glaucoma': self.primary_open_angle_glaucoma,
            'retinitis_pigmentosa': self.retinitis_pigmentosa,
            'retinoblastoma': self.retinoblastoma,
        }
        return self.map_to_names(result)

    def to_json_analysis(self):
        result = {
            'id': self.id,
            'gene': self.gene,
            'ensembl_id': self.ensembl_id,
            'age_related_macular_degeneration': self.age_related_macular_degeneration,
            'diabetic_retinopathy': self.diabetic_retinopathy,
            'keratoconus': self.keratoconus,
            'primary_open_angle_glaucoma': self.primary_open_angle_glaucoma,
            'retinitis_pigmentosa': self.retinitis_pigmentosa,
            'retinoblastoma': self.retinoblastoma,
        }
        return result

    @classmethod
    def column_mappings(cls):
        return {
            'age_related_macular_degeneration': 'Age-related macular degeneration',
            'diabetic_retinopathy': 'Diabetic retinopathy',
            'keratoconus': 'Keratoconus',
            'primary_open_angle_glaucoma': 'Primary open-angle glaucoma',
            'retinitis_pigmentosa': 'Retinitis pigmentosa',
            'retinoblastoma': 'Retinoblastoma',
        }


class ExpressionMicroarrayTissue(db.Model, MappingTableMixin):
    __tablename__ = 'expression_microarray_tissue'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    gene = db.Column(db.String(128), nullable=True, index=True)
    ensembl_id = db.Column(db.String(128), nullable=True)

    retina = db.Column(db.Float, nullable=True)
    corneal = db.Column(db.Float, nullable=True)
    corneal_epithelium = db.Column(db.Float, nullable=True)
    corneal_endothelium = db.Column(db.Float, nullable=True)
    conjunctiva = db.Column(db.Float, nullable=True)
    optic_nerve_head = db.Column(db.Float, nullable=True)
    lymphoblast = db.Column(db.Float, nullable=True)
    eye_orbit = db.Column(db.Float, nullable=True)
    lacrimal_gland = db.Column(db.Float, nullable=True)
    thyroid = db.Column(db.Float, nullable=True)
    normal_uveal_melanocytes = db.Column(db.Float, nullable=True)

    def to_json(self):
        result = {
            'id': self.id,
            'gene': self.gene,
            'ensembl_id': self.ensembl_id,
            'retina': self.retina,
            'corneal': self.corneal,
            'corneal_epithelium': self.corneal_epithelium,
            'corneal_endothelium': self.corneal_endothelium,
            'conjunctiva': self.conjunctiva,
            'optic_nerve_head': self.optic_nerve_head,
            'lymphoblast': self.lymphoblast,
            'eye_orbit': self.eye_orbit,
            'lacrimal_gland': self.lacrimal_gland,
            'thyroid': self.thyroid,
            'normal_uveal_melanocytes': self.normal_uveal_melanocytes,
        }
        return self.map_to_names(result)

    @classmethod
    def column_mappings(cls):
        return {
            'retina': 'Retina',
            'corneal': 'Corneal',
            'corneal_epithelium': 'Corneal epithelium',
            'corneal_endothelium': 'Corneal endothelium',
            'conjunctiva': 'Conjunctiva',
            'optic_nerve_head': 'Optic nerve head',
            'lymphoblast': 'Lymphoblast',
            'eye_orbit': 'Eye Orbit',
            'lacrimal_gland': 'Lacrimal gland',
            'thyroid': 'Thyroid',
            'normal_uveal_melanocytes': 'Normal uveal melanocytes',
        }


class ExpressionMicroarrayDisease(db.Model, MappingTableMixin):
    __tablename__ = 'expression_microarray_disease'

    id = db.Column(UUID(as_uuid=False), default=uuid4_string, primary_key=True)
    gene = db.Column(db.String(128), nullable=True, index=True)
    ensembl_id = db.Column(db.String(128), nullable=True)

    retinal_detachment = db.Column(db.Float, nullable=True)
    diabetic_retinopathy = db.Column(db.Float, nullable=True)
    retinoblastoma = db.Column(db.Float, nullable=True)
    retinitis_pigmentosa = db.Column(db.Float, nullable=True)
    keratoconus = db.Column(db.Float, nullable=True)
    keratitis = db.Column(db.Float, nullable=True)
    trachoma = db.Column(db.Float, nullable=True)
    glaucoma = db.Column(db.Float, nullable=True)
    fuchs_endothelial_corneal_dystrophy = db.Column(db.Float, nullable=True)
    uveal_melanoma = db.Column(db.Float, nullable=True)
    uveal_melanoma_mum2b = db.Column(db.Float, nullable=True)
    uveal_melanoma_ocm1a = db.Column(db.Float, nullable=True)
    graves_ophthalmopathy = db.Column(db.Float, nullable=True)
    nonspecific_orbital_inflammation = db.Column(db.Float, nullable=True)
    sarcoidosis = db.Column(db.Float, nullable=True)
    granulomatosis_with_polyangiitis = db.Column(db.Float, nullable=True)
    thyroid_eye_disease = db.Column(db.Float, nullable=True)

    def to_json(self):
        result = {
            'id': self.id,
            'gene': self.gene,
            'ensembl_id': self.ensembl_id,
            'retinal_detachment': self.retinal_detachment,
            'diabetic_retinopathy': self.diabetic_retinopathy,
            'retinoblastoma': self.retinoblastoma,
            'retinitis_pigmentosa': self.retinitis_pigmentosa,
            'keratoconus': self.keratoconus,
            'keratitis': self.keratitis,
            'trachoma': self.trachoma,
            'glaucoma': self.glaucoma,
            'fuchs_endothelial_corneal_dystrophy': self.fuchs_endothelial_corneal_dystrophy,
            'uveal_melanoma': self.uveal_melanoma,
            'uveal_melanoma_mum2b': self.uveal_melanoma_mum2b,
            'uveal_melanoma_ocm1a': self.uveal_melanoma_ocm1a,
            'graves_ophthalmopathy': self.graves_ophthalmopathy,
            'nonspecific_orbital_inflammation': self.nonspecific_orbital_inflammation,
            'sarcoidosis': self.sarcoidosis,
            'granulomatosis_with_polyangiitis': self.granulomatosis_with_polyangiitis,
            'thyroid_eye_disease': self.thyroid_eye_disease,
        }
        return self.map_to_names(result)

    @classmethod
    def column_mappings(cls):
        return {
            'retinal_detachment': "Retinal detachment",
            'diabetic_retinopathy': "Diabetic retinopathy",
            'retinoblastoma': "Retinoblastoma",
            'retinitis_pigmentosa': "Retinitis pigmentosa",
            'keratoconus': "Keratoconus",
            'keratitis': "Keratitis",
            'trachoma': "Trachoma",
            'glaucoma': "Glaucoma",
            'fuchs_endothelial_corneal_dystrophy': "Fuchs' endothelial corneal dystrophy",
            'uveal_melanoma': "Uveal melanoma",
            'uveal_melanoma_mum2b': "Uveal melanoma MUM2B",
            'uveal_melanoma_ocm1a': "Uveal melanoma OCM1A",
            'graves_ophthalmopathy': "Graves' ophthalmopathy",
            'nonspecific_orbital_inflammation': "Nonspecific orbital inflammation",
            'sarcoidosis': "Sarcoidosis",
            'granulomatosis_with_polyangiitis': "Granulomatosis with polyangiitis",
            'thyroid_eye_disease': "Thyroid eye disease",
        }
