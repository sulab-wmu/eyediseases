#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import itertools
from collections import defaultdict

import colorlover as cl
from flask_classful import FlaskView

from ek_optical.epigenomics.models import Epigenomics, AppConfig
from ek_optical.extensions import db
from ek_optical.util import make_dict_response


class EpigenomicsAPI(FlaskView):

    def tracks(self):
        colors = itertools.cycle(cl.scales['4']['div']['RdYlBu'])
        results = db.session.query(Epigenomics).order_by(Epigenomics.disease.asc(), Epigenomics.data_type.asc()).all()
        ref_track = AppConfig.get_config_value('igv.ref.hg38')
        epigenomics = [x.to_json(color=next(colors)) for x in results]
        return make_dict_response(tracks=epigenomics, reference=ref_track)
        # dict_keys(['BrBG', 'PRGn', 'PiYG', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral'])

    def list(self):
        epigenomics = db.session.query(Epigenomics.disease, Epigenomics.data_type).distinct().order_by(
            Epigenomics.disease.asc(), Epigenomics.data_type.asc()).all()

        results = defaultdict(set)
        for disease, data_type in epigenomics:
            results[disease].add(data_type)

        return make_dict_response(
            diseases=sorted(results.keys()),
            diseases_types={d: [dict(type=x, disease=d, data_key=d + '/' + x) for x in sorted(v)] for d, v in results.items()}
        )
