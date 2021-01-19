#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import base64
import io

import pandas as pd
import seaborn as sns
from flask import request
from flask_classful import FlaskView
from pandas.core.reshape.concat import concat
from sqlalchemy import asc

from ek_optical.expression.models import (
    ExpressionMouse,
    ExpressionMicroarrayTissue,
    ExpressionMicroarrayDisease,
    ExpressionRNASeqDisease,
    ExpressionRNASeqTissue,
)
from ek_optical.extensions import db
from ek_optical.util import make_dict_response, InvalidUsage
from ek_optical.util import split_params


class ExpressionAPI(FlaskView):
    def datasets(self):
        result = [
            {
                'key': 'microarray_tissue',
                'name': 'Human (Microarray) - Tissue',
                'options': list(ExpressionMicroarrayTissue.column_mappings().values()),
                'example': 'AADAC,AAK1,AANAT,AASDHPPT,AASS,AATF,ABCA1,ABCA8,ABCB1,ABCB11',
            },
            {
                'key': 'microarray_disease',
                'name': 'Human (Microarray) - Disease',
                'options': list(ExpressionMicroarrayDisease.column_mappings().values()),
                'example': 'AADAC,AAK1,AANAT,AASDHPPT,AASS,AATF,ABCA1,ABCA8,ABCB1,ABCB11',
            },
            {
                'key': 'rnaseq_tissue',
                'name': 'Human (RNASeq) - Tissue',
                'options': list(ExpressionRNASeqTissue.column_mappings().values()),
                'example': 'OR4F5,SAMD11,NOC2L,KLHL17,PLEKHN1,C1orf170,HES4,ISG15,AGRN,RNF223',
            },
            {
                'key': 'rnaseq_disease',
                'name': 'Human (RNASeq) - Disease',
                'options': list(ExpressionRNASeqDisease.column_mappings().values()),
                'example': 'OR4F5,SAMD11,NOC2L,KLHL17,PLEKHN1,C1orf170,HES4,ISG15,AGRN,RNF223',
            },
            {
                'key': 'mouse',
                'name': 'Mouse',
                'options': list(ExpressionMouse.column_mappings().values()),
                'example': 'Zfp92,Zfp91-cntf,Zfp91,Zfp90,Zfp9,Zfp87,Zfp85-rs1,Zfp84',
            },
        ]
        # return make_dict_response(data=[])
        return make_dict_response(data=result)

    def _get_table_name(self, _type):
        types = {
            'mouse': ExpressionMouse,
            'microarray_tissue': ExpressionMicroarrayTissue,
            'microarray_disease': ExpressionMicroarrayDisease,
            'rnaseq_tissue': ExpressionRNASeqTissue,
            'rnaseq_disease': ExpressionRNASeqDisease,
        }

        if _type not in types:
            raise InvalidUsage('Invalid type')

        return types[_type]

    def heatmap_data(self):
        import matplotlib.pyplot as plt

        _type = request.args.get('type')
        platform = request.args.get('platform')
        genes = split_params(request.args.get('gene'))
        if _type == 'mouse':
            datasets = split_params(request.args.get('tissue'))
            # if len(datasets) < 2:
            #     raise InvalidUsage('Too few data sets', 400)
            table_model = self._get_table_name(_type)
            query = db.session.query(table_model).filter(table_model.gene.in_(genes))
            df = pd.read_sql(query.statement, db.engine, index_col='gene')
            df = df.rename(columns=table_model.column_mappings())
            df = df[datasets]
        else:
            types = platform + '_' + 'tissue'
            datasets1 = split_params(request.args.get('tissue'))
            table_model = self._get_table_name(types)
            query = db.session.query(table_model).filter(table_model.gene.in_(genes)).order_by(asc(table_model.gene))
            df1 = pd.read_sql(query.statement, db.engine, index_col='gene')
            df1 = df1.rename(columns=table_model.column_mappings())
            df1 = df1[datasets1]

            types = platform + '_' + 'disease'
            datasets2 = split_params(request.args.get('disease'))
            table_model = self._get_table_name(types)
            query = db.session.query(table_model).filter(table_model.gene.in_(genes)).order_by(asc(table_model.gene))
            df2 = pd.read_sql(query.statement, db.engine, index_col='gene')
            df2 = df2.rename(columns=table_model.column_mappings())
            df2 = df2[datasets2]

            # if len(datasets1 + datasets2) < 2:
            #     raise InvalidUsage('Too few data sets', 400)

            df = concat([df1, df2], join="inner", axis=1)
            # print(df)

        df.index.name = None
        if len(df) == 0:
            empty_df = df.reset_index()
            return make_dict_response(
                fig=None,
                data=empty_df.to_dict('records'),
                columns=empty_df.columns.tolist(),
            )

        # cellSizePixels = 75
        # dpi = matplotlib.rcParams['figure.dpi']
        # marginWidth = matplotlib.rcParams['figure.subplot.right']-matplotlib.rcParams['figure.subplot.left']
        # marginHeight = matplotlib.rcParams['figure.subplot.top']-matplotlib.rcParams['figure.subplot.bottom']
        # Ny,Nx = df.shape
        # figWidth = (Nx*cellSizePixels/dpi)/0.8/marginWidth
        # figHeigh = (Ny*cellSizePixels/dpi)/0.8/marginHeight

        row_cluster = df.shape[0] > 1
        col_cluster = df.shape[1] > 1

        df = df.fillna(0)
        sns.set(font_scale=1.2)
        cluster = sns.clustermap(df, linewidths=1, cmap="mako", vmin=0, vmax=10, row_cluster=row_cluster, col_cluster=col_cluster)

        # axWidth = (Nx*cellSizePixels)/(figWidth*dpi)
        # axHeight = (Ny*cellSizePixels)/(figHeigh*dpi)
        #
        # # resize heatmap
        # ax_heatmap_orig_pos = cluster.ax_heatmap.get_position()
        # cluster.ax_heatmap.set_position([ax_heatmap_orig_pos.x0, ax_heatmap_orig_pos.y0,
        #                               axWidth, axHeight])
        #
        # # resize dendrograms to match
        # ax_row_orig_pos = cluster.ax_row_dendrogram.get_position()
        # cluster.ax_row_dendrogram.set_position([ax_row_orig_pos.x0, ax_row_orig_pos.y0,
        #                                      ax_row_orig_pos.width, axHeight])
        # ax_col_orig_pos = cluster.ax_col_dendrogram.get_position()
        # cluster.ax_col_dendrogram.set_position([ax_col_orig_pos.x0, ax_heatmap_orig_pos.y0+axHeight,
        #                                      axWidth, ax_col_orig_pos.height])

        plt.setp(cluster.ax_heatmap.xaxis.get_majorticklabels(), rotation=45, horizontalalignment='right')
        img = io.BytesIO()
        cluster.savefig(img, format='png')

        img.seek(0)
        fig = base64.b64encode(img.getvalue()).decode('utf-8')
        # Safari fix: https://stackoverflow.com/questions/27396376/base64-image-tag-in-safari-did-not-showed-up
        # pad_num = 4 - (len(fig) % 4)
        # if pad_num < 4:
        #     fig = fig + ('=' * pad_num)
        cluster_data = cluster.data2d.round(4).reset_index()
        return make_dict_response(
            fig='data:image/png;base64,' + fig,
            data=cluster_data.to_dict('records'),
            columns=cluster_data.columns.tolist(),
        )
