#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from flask import request
from flask_classful import FlaskView

from ek_optical.disease.models import GeneticGWAS, GeneticOMIM
from ek_optical.extensions import db
from ek_optical.util import InvalidUsage, make_dict_response


class DiseasesAPI(FlaskView):
    def list(self):
        disease_name = request.args.get('name')
        if not disease_name:
            return make_dict_response({'gene': []})

        gwas_disease = db.session.query(GeneticGWAS.disease).distinct().filter(GeneticGWAS.disease.ilike("%" + disease_name + "%"))
        omim_disease = db.session.query(GeneticOMIM.disease).distinct().filter(GeneticOMIM.disease.ilike("%" + disease_name + "%"))
        disease_query = gwas_disease.union_all(omim_disease).distinct().limit(20)
        return make_dict_response(data=[{'id': x.disease, 'name': x.disease} for x in disease_query])

    def gwas(self):
        disease = request.args.get('dis')
        page = request.args.get('page', 1, type=int)
        number = request.args.get('number', 10, type=int)

        if not disease:
            raise InvalidUsage('传递的信息不全！')

        query = db.session.query(GeneticGWAS).filter_by(disease=disease)
        paginate = query.paginate(page, number, False)
        response = {
            "data": [r.to_json_disease() for r in query],
            "pagination": {
                'total': paginate.total,
                'page': page,
                'number': number,
                'total_pages': paginate.pages,
            },
        }
        return make_dict_response(response)

    def omim(self):
        disease = request.args.get('dis')
        page = request.args.get('page', 1, type=int)
        number = request.args.get('number', 10, type=int)

        if not disease:
            raise InvalidUsage('传递的信息不全！')

        query = db.session.query(GeneticOMIM).filter_by(disease=disease)
        paginate = query.paginate(page, number, False)
        response = {
            "data": [r.to_json_disease() for r in query],
            "pagination": {
                'total': paginate.total,
                'page': page,
                'number': number,
                'total_pages': paginate.pages,
            },
        }
        return make_dict_response(response)
