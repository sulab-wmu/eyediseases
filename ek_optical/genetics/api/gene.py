#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from flask import request, jsonify
from flask_classful import FlaskView, route

from ek_optical.extensions import db
from ek_optical.genetics.models import Gene
from ek_optical.genetics.models import GeneExpression
from ek_optical.util import make_dict_response, InvalidUsage


class GeneAPI(FlaskView):
    def get(self):
        gene_name = request.args.get('name')
        if not gene_name:
            raise InvalidUsage('name not provided', 400)
        gene = db.session.query(Gene).filter_by(symbol=gene_name).first_or_404()
        return make_dict_response(data=gene.to_json())

    def list(self):
        gene_name = request.args.get('name')
        if gene_name:
            genes = db.session.query(Gene).filter(
                Gene.symbol.ilike("%" + gene_name + "%"),
            ).limit(20)
            return jsonify({'data': [g.to_list() for g in genes]}), 200
        return jsonify([]), 200

    @route('/search', methods=['GET'])
    def gene_and_expression(self):
        gene_id = request.args.get('gene_id')
        if not gene_id:
            raise InvalidUsage('gene_id not provided')

        gene = db.session.query(Gene).filter_by(gene=gene_id).first()
        return make_dict_response(gene=None if not gene else gene.to_json())

    @route('/expression-violin', methods=['GET'])
    def gene_expression_violin(self):
        gene_name = request.args.get('name')
        if not gene_name:
            raise InvalidUsage('name not provided')

        genes = db.session.query(GeneExpression).filter_by(gene=gene_name).all()
        response = {
            'gene': [gene.to_json() for gene in genes],
            'disease': sorted(set(x.disease for x in genes)),
        }
        return make_dict_response(response)
