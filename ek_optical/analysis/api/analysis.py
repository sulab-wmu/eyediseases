#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import json

import pandas as pd
from flask import jsonify, request
from flask_classful import FlaskView, route
from sqlalchemy import or_, text, and_

from ek_optical.analysis.models import (
    DiseaseGo,
    GeneDiseaseSignificance,
    Keratoconus,
    Corneal,
    TissueGeneSignificance,
    EpigeneticAlteration,
    GeneDiseaseCorrect,
    GeneTissueCorrect,
    Retina,
    Macula,
    RetinaMacula,
    NonMacula,
    RetinaNonMacula,
    CornealEndothelialCells,
    Retinoblastoma,
    AgeRelatedMacularDegeneration,
)
from ek_optical.extensions import db
from ek_optical.util import make_dict_response, InvalidUsage
from ek_optical.util import split_params


def mapping_disease_tissue():
    return {
        'Retina': Retina,
        'Corneal': Corneal,
        'RPE_macula': Macula,
        'Retina_macula': RetinaMacula,
        'RPE_non_macula': NonMacula,
        'Retina_non_macula': RetinaNonMacula,
        'Corneal_endothelial_cells': CornealEndothelialCells,
        'Keratoconus': Keratoconus,
        'Retinoblastoma': Retinoblastoma,
        'Age-Related-Macular-Degeneration': AgeRelatedMacularDegeneration,
    }


class AnalysisAPI(FlaskView):
    def get(self):
        return jsonify({'data': []}), 200

    @route('/disease-go', methods=['GET'])
    def analysis_go(self):
        disease = request.args.get('disease')
        gos_query = db.session.query(DiseaseGo).filter_by(disease=disease)
        bps = gos_query.filter_by(dataset='BP').all()
        ccs = gos_query.filter_by(dataset='CC').all()
        mfs = gos_query.filter_by(dataset='MF').all()
        keggs = gos_query.filter_by(dataset='KEGG').all()
        result = {
            'bp': [bp.to_json() for bp in bps],
            'cc': [cc.to_json() for cc in ccs],
            'mf': [mf.to_json() for mf in mfs],
            'kegg': [kegg.to_json() for kegg in keggs],
        }
        return make_dict_response(go=result)

    @route('/disease-co', methods=['GET'])
    def analysis_co(self):
        gene = request.args.get('gene')
        species = json.loads(request.args.get('species'))
        tt = request.args.get('ThresholdThreshold')
        tn = request.args.get('Threshold_numbwe')

        try:
            genes = gene.split(',')
        except:
            raise InvalidUsage('not found gene', 400)

        result = {
            'data1': [],
            'data2': [],
        }
        if not genes or not species['microarray_disease'] and not species['microarray_tissue']:
            return make_dict_response(data=result)

        if species['microarray_disease']:
            db_name = mapping_disease_tissue()[species['microarray_disease'][0]]
            gene_disease_query = db.session.query(db_name).filter(or_(db_name.gene.in_(genes), db_name.contrast_gene.in_(genes)))
            gds = db.session.query(GeneDiseaseCorrect).filter(and_(GeneDiseaseCorrect.gene.in_(genes), GeneDiseaseCorrect.disease.in_(species['microarray_disease'])))
            if tt:  # 0.1
                gene_disease_query = gene_disease_query.filter(or_(db_name.weight > float(tt), db_name.weight < -float(tt)))
                gds = gds.filter(or_(GeneDiseaseCorrect.weight > float(tt), GeneDiseaseCorrect.weight < -float(tt)))
            if tn:
                gene_disease_query = gene_disease_query.limit(float(tn))
                gds = gds.limit(float(tn))
            result['data1'] = [g.to_json() if g.contrast_gene not in genes else g.to_reverse_json() for g in gene_disease_query.all()]
            result['data2'] = [g.to_json() for g in gds.all()]

        if species['microarray_tissue']:
            db_name = mapping_disease_tissue()[species['microarray_tissue'][0]]
            gene_disease_query = db.session.query(db_name).filter(or_(db_name.gene.in_(genes), db_name.contrast_gene.in_(genes)))
            tgs = db.session.query(GeneTissueCorrect).filter(and_(GeneTissueCorrect.gene.in_(genes), GeneTissueCorrect.tissue.in_(species['microarray_tissue'])))
            if tt:
                gene_disease_query = gene_disease_query.filter(or_(db_name.weight > float(tt), db_name.weight < -float(tt)))
                tgs = tgs.filter(or_(GeneTissueCorrect.weight > float(tt), GeneTissueCorrect.weight < -float(tt)))
            if tn:
                gene_disease_query = gene_disease_query.limit(float(tn))
                tgs = tgs.limit(float(tn))
            result['data1'] = [g.to_json() if g.contrast_gene not in genes else g.to_reverse_json() for g in gene_disease_query.all()]
            result['data2'] = [g.to_json() for g in tgs.all()]

        return make_dict_response(data=result)

    @route('/gene-disease-network', methods=['GET'])
    def gene_disease_network(self):
        keywords = split_params(request.args.get('keywords', ''))
        if not keywords:
            raise InvalidUsage('No keywords provided')

        sql = text("""
            SELECT gene, disease, weight
            FROM gene_network_disease 
            WHERE gene IN :keywords or disease in :keywords;
        """)

        df = pd.read_sql(sql, db.engine, params={'keywords': tuple(keywords)})
        if len(df) == 0:
            raise InvalidUsage('No data points found')

        df = df.groupby(['gene', 'disease']).agg({'weight': 'max'}).reset_index().copy()
        weight_max = df['weight'].max()
        if weight_max > 0:
            df['weight'] = df['weight'] / weight_max
            df.loc[df['weight'] == 0, 'weight'] = df['weight'][df['weight'] > 0].min() * 0.1
        else:
            df['weight'] = 1

        unique_genes = df['gene'].drop_duplicates()
        unique_diseases = df['disease'].drop_duplicates()

        gene_mappings = {}
        disease_mappings = {}
        nodes = []
        node_counter = 0

        for g in unique_genes:
            nodes.append({'node': node_counter, 'name': g})
            gene_mappings[g] = node_counter
            node_counter = node_counter + 1

        for d in unique_diseases:
            nodes.append({'node': node_counter, 'name': d})
            disease_mappings[d] = node_counter
            node_counter = node_counter + 1

        links = []
        for _, row in df.iterrows():
            links.append({
                'source': gene_mappings[row['gene']],
                'target': disease_mappings[row['disease']],
                'value': row['weight']
            })

        node_links = {'nodes': nodes, 'links': links}
        return make_dict_response(data=node_links)

    @route('/alteration', methods=['GET'])
    def alteration(self):
        ep_alt = db.session.query(EpigeneticAlteration).all()
        data = [i.to_json() for i in ep_alt]
        return make_dict_response(data=data)

    @route('/significance', methods=['GET'])
    def significance(self):
        gene = request.args.get('gene')
        species = request.args.get('species')
        # tt = request.args.get('ThresholdThreshold')

        try:
            genes = gene.split(',')
        except:
            raise InvalidUsage('not found gene', 400)

        result = {
            'data1': [],
            'data2': [],
            'data3': []
        }
        if not gene or not species:
            return make_dict_response(data=result)

        if species == 'disease':
            gds = db.session.query(GeneDiseaseSignificance).filter(GeneDiseaseSignificance.gene.in_(genes)).all()
            result['data2'] = [g.to_json() for g in gds]

        if species == 'tissue':
            tgs = db.session.query(TissueGeneSignificance).filter(TissueGeneSignificance.gene_symbol.in_(genes)).all()
            result['data2'] = [g.to_json() for g in tgs]

        return make_dict_response(data=result)
