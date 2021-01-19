#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from flask import jsonify, request
from flask_classful import FlaskView

from ek_optical.disease.models import GeneticGWAS, GeneticOMIM
from ek_optical.epigenomics.models import Epigenomics
from ek_optical.expression.models import ExpressionMicroarrayDisease, ExpressionRNASeqDisease
from ek_optical.extensions import db
from ek_optical.genetics.models import Gene
from ek_optical.util import make_dict_response
from ek_optical.variants.models import Summary


class SearchAPI(FlaskView):
    def statistic(self):
        gene_count = db.session.query(Gene.symbol).count()

        gwas_disease = db.session.query(GeneticGWAS.disease).distinct()
        omim_disease = db.session.query(GeneticOMIM.disease).distinct()
        disease_count = gwas_disease.union_all(omim_disease).distinct().count()

        gwas_variants = db.session.query(GeneticGWAS.variant).distinct()
        omim_variants = db.session.query(GeneticOMIM.variant).distinct()
        variants_count = gwas_variants.union_all(omim_variants).distinct().count()

        gwas_study = db.session.query(GeneticGWAS.study).distinct()
        omim_study = db.session.query(GeneticOMIM.publications).distinct()
        study_count = gwas_study.union_all(omim_study).distinct().count()

        return make_dict_response(data={'gene': gene_count, 'disease': disease_count, 'snp': variants_count, 'studies': study_count})

    def exist(self):
        disease_name = request.args.get('name')

        epigenomic = db.session.query(Epigenomics.disease).all()
        epigenomics = [ep[0] for ep in epigenomic]

        epigenomics_exist = disease_name in epigenomics
        micro_exist = disease_name in ExpressionMicroarrayDisease.data_columns()
        seq_exist = disease_name in ExpressionRNASeqDisease.data_columns()

        return jsonify({'data': {'epigenomics': epigenomics_exist, 'expression': micro_exist or seq_exist}}), 200

    def total(self):
        gene = db.session.query(Gene.symbol).distinct()
        variant = db.session.query(Summary.snpid).distinct()
        gwas_disease = db.session.query(GeneticGWAS.disease).distinct()
        omim_disease = db.session.query(GeneticOMIM.disease).distinct()
        disease_count = gwas_disease.union_all(omim_disease).distinct()

        response = {
            'gene': [i[0] for i in gene],
            'variant': [i[0] for i in variant],
            'disease': [i[0] for i in disease_count]
        }

        return make_dict_response(data=response)
