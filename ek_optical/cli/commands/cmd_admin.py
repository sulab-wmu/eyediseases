#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import random

import click
import colorlover
from flask.cli import with_appcontext

from ek_optical.epigenomics.models import Epigenomics
from ek_optical.extensions import db
from ek_optical.genetics.models import GeneExpression
from ek_optical.variants.models import Causality


@click.group()
def cli():
    """ Image tagger admin functions """
    pass


def random_color():
    a_l = ['div', 'qual', 'seq']
    a = int(random.uniform(3, 10))
    b = colorlover.scales[str(a)][random.choice(a_l)]
    c = random.choice(list(b.keys()))
    d = random.choice(b[c])
    return d


@cli.command()
@with_appcontext
def add_color():
    cas = db.session.query(Causality).all()
    ca_disease_array = sorted(set(x.disease for x in cas))
    ca_color = {}
    for ca_disease in ca_disease_array:
        ca_color[ca_disease] = random_color()
    for ca in cas:
        ca.color = ca_color[ca.disease]
        db.session.add(ca)
    ges = db.session.query(GeneExpression).all()
    ge_disease_array = sorted(set(x.disease for x in ges))
    ge_color = {}
    for ge_disease in ge_disease_array:
        ge_color[ge_disease] = random_color()
    for ge in ges:
        ge.color = ge_color[ge.disease]
        db.session.add(ge)
    db.session.commit()
    print('修改color列成功')


@cli.command()
@with_appcontext
def add_epigenomics():
    ep_obj = {
        'AMD-RPE-ATAC.bw': 'ATAC&Age-related macular degeneration-RPE',
        'AMD-Retina-ATAC.bw': 'ATAC&Age-related macular degeneration-Retina',
        'Iris-pigment-epithelial-RRBS-methy.bw': 'RRBS-methy&Iris-pigment-epithelial',
        'Macula_ATAC.bw': 'ATAC&Macula',
        'RB-Bis-seq.bw': 'Bis-seq&Retinoblastoma',
        'RB-H3K27Ac.bw': 'H3K27Ac&Retinoblastoma',
        'RB-H3K27me3.bw': 'H3K27me3&Retinoblastoma',
        'RB-H3K4me1.bw': 'H3K4me1&Retinoblastoma',
        'RB-H3K4me3.bw': 'H3K4me3&Retinoblastoma',
        'RB-H3K9me3_2.bw': 'H3K9me3_2&Retinoblastoma',
        'RPE-H3K27ac.bw': 'H3K27Ac&Retianl-pigment-epithelial',
        'Retina-H3K27ac.bw': 'H3K27Ac&Retina',
        'Retina_ATAC.bw': 'ATAC&Retina',
        'Retinal-pigment-epithelial-cells - H3K27ac .bw': 'H3K27Ac&Retianl-pigment-epithelial-cells',
        'Retinal-pigment-epithelial-cells-H3K4me3.bw': 'H3K4me3&Retianl-pigment-epithelial-cells',
        'WERI-Rb-1-H3K4me3.bw': 'H3K4me3&WERI-Retinoblastoma-1',
        'iPSC-RPE-ATAC.bw': 'ATAC&IPSC-RPE',
        'iPSC-RPE-H3K27ac.bw': 'H3K27Ac&IPSC-RPE',
        'keratoconus-RRBS.bw': 'RRBS&Keratoconus',
        'retinal-pigment-epithelial-Bis-seq.bw': 'Bis-seq&Retianl-pigment-epithelial',
        'retinal-pigment-epithelial-RRBS-methy.bw': 'RRBS-methy&Retianl-pigment-epithelial',
    }
    eps = db.session.query(Epigenomics).all()
    for ep in eps:
        arr = ep_obj[ep.file_name].split('&')
        ep.disease = arr[1]
        ep.data_type = arr[0]
        db.session.add(ep)
    db.session.commit()
