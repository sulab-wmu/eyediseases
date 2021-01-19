#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from flask import request
from flask_classful import FlaskView, route
from sqlalchemy import and_, func

from ek_optical.extensions import db
from ek_optical.singlecell.models import OutCell, MarkersCell
from ek_optical.util import make_dict_response, InvalidUsage


def cell_colnum_mapping():
    return {
        'Fetal eye': "GSE134355",
        'Fetal Retina and RPE': "GSE107618",
        'Adult Retina1': "GSE133707",
        'Adult Retina2': "E-MTAB-7316",
        'Uveal melanoma': "GSE139829",
        'AMD RPE': "GSE135922"
    }


class SingleCellAPI(FlaskView):

    def get(self):
        cluster = request.args.get('cluster')
        cell_file_name = request.args.get('name')
        cell_file_name = cell_colnum_mapping()[cell_file_name]

        cell_tsne1 = []
        cell_tsne2 = []
        cell_group = []

        if cluster:
            cluster_columns = [cl.split(':')[1] for cl in cluster.split(',')]
            label_columns = [cl.split(':')[2] for cl in cluster.split(',')]
            if label_columns.count('None') > 0:
                rs_data = db.session.query(OutCell).filter_by(cell_type=cell_file_name).filter(OutCell.cluster.in_(cluster_columns)).all()
            else:
                rs_data = db.session.query(OutCell).filter_by(cell_type=cell_file_name).filter(and_(OutCell.cluster.in_(cluster_columns), OutCell.labels.in_(
                    label_columns))).all()

            rs_x = list(db.session.query(func.min(OutCell.xaxis), func.max(OutCell.xaxis)).filter_by(cell_type=cell_file_name).one())
            rs_y = list(db.session.query(func.min(OutCell.yaxis), func.max(OutCell.yaxis)).filter_by(cell_type=cell_file_name).one())

            rs_data.sort(key=lambda x: int(x.cluster))

            for item in rs_data:
                cell_tsne1.append(item.xaxis)
                cell_tsne2.append(item.yaxis)
                cell_group.append(f'cluster:{item.cluster}:{item.labels}')

        response = {
            'x': cell_tsne1,
            'y': cell_tsne2,
            'group': cell_group,
            'x_range': [rs_x[0]-3, rs_x[1]+3],
            'y_range': [rs_y[0]-3, rs_y[1]+3],
        }

        return make_dict_response(response)

    @route('list', methods=['GET'])
    def single_cell_list(self):
        cell_file_name = request.args.get('name')
        cell_file_name = cell_colnum_mapping()[cell_file_name]
        if cell_file_name:
            cluster_list = db.session.query(OutCell.cluster, OutCell.labels).filter_by(cell_type=cell_file_name).distinct().all()
            cluster_list = sorted(cluster_list, key=lambda x: int(x[0]))
            rs_cluster = [f'cluster:{cluster}:{labels}' for cluster, labels in cluster_list]
            return make_dict_response(data=rs_cluster)
        else:
            return make_dict_response(data=[])

    @route('/grid', methods=['GET'])
    def get_single_cell_data(self):
        name = request.args.get('name')
        page = request.args.get('page')
        number = request.args.get('number')
        name = cell_colnum_mapping()[name]

        page = 1 if not page else int(page)
        number = 10 if not number else int(number)

        if not name:
            raise InvalidUsage('传递的信息不全！', 400)

        cell_name = db.session.query(MarkersCell).filter_by(cell_type=name)
        paginate = cell_name.paginate(page, number, False)

        data = []
        if cell_name:
            for cn in cell_name:
                cell_data = {
                    "gene": cn.gene,
                    "cluster": cn.cluster,
                    "annotation": cn.labels,
                    "p_val": cn.p_val,
                    "avg_logFC": cn.avg,
                    "pct1": cn.pct1,
                    "pct2": cn.pct2,
                }
                data.append(cell_data)

        response = {
            "data": data,
            "pagination": {
                'total': paginate.total,
                'page': page,
                'number': number,
                'total_pages': paginate.pages,
            },
        }
        return make_dict_response(response)
