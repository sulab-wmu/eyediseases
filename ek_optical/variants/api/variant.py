#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from flask import request, jsonify
from flask_classful import FlaskView, route

from ek_optical.extensions import db
from ek_optical.util import make_dict_response, InvalidUsage
from ek_optical.variants.models import Summary, Causality, Gnomad

area = {
    'ami': 'Latino',  # todo
    'afr': 'African /<br>African American',
    'amr': 'Latino',
    'asj': 'Ashkenazi<br>Jewish',
    'eas': 'East Asian',
    'fin': 'Finnish',
    'nfe': 'Non-Finnish<br>European',
    'sas': 'South Asian',
    'oth': 'Other'
}


class VariantAPI(FlaskView):
    def get(self):
        variant_id = request.args.get('name')
        if variant_id is None:
            raise InvalidUsage('incomplete', 400)
        summary = db.session.query(Summary).filter_by(snpid=variant_id).first()
        causality = db.session.query(Causality).filter_by(variant=variant_id).all()
        gnomad = db.session.query(Gnomad).filter_by(variant=variant_id).first()

        gnomad_data_value = []
        gnomad_data_text = []
        gnomad_data_key = []
        if gnomad:
            for k, v in gnomad.territory.items():
                gnomad_data_value.append(float(v) * 100)
                gnomad_data_text.append(f'{v}%')
                gnomad_data_key.append(area[k])

        response = {
            'summary': None if not summary else summary.to_json(),
            'causality': [ex.to_json() for ex in causality],
            'gnomad': {
                'y': gnomad_data_key,
                'x': gnomad_data_value,
                'text': gnomad_data_text,
            },
        }

        return make_dict_response(response)

    @route('list', methods=['GET'])
    def variant_list(self):
        variant_name = request.args.get('name')
        if variant_name:
            variants = db.session.query(Summary).filter(
                Summary.snpid.ilike("%" + variant_name + "%"),
            ).limit(20)
            return jsonify({'data': [g.to_list() for g in variants]}), 200
        return jsonify([]), 200

    @route('search/auto', methods=['GET'])
    def search_auto(self):
        search_name = request.args.get('search_name')
        if not search_name:
            return jsonify({'gene': []}), 200

        rs_variant = db.session.query(Summary).filter(
            Summary.variant.ilike("%" + search_name + "%"),
        ).limit(10)

        response = {
            'variant': [item.variants for item in rs_variant],
        }
        return jsonify(response), 200
