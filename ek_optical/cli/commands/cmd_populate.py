#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import json
import os
from pathlib import Path

import click
import pandas as pd
from flask.cli import with_appcontext

from ek_optical.dataload.dataload import read_gnomad, read_gene_expression, insert_uuid4, insert_file_marker, insert_file_out, insert_dis_type
from ek_optical.epigenomics.models import Epigenomics, AppConfig
from ek_optical.extensions import db
from ek_optical.util import save_dataframe_using_copy


@click.group(name='populate')
def cli():
    """ Populate data commands """
    pass


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x01_snp_gene_summary(file, truncate):
    name = ['snpid', 'position_hg38', 'major_allele', 'variant', 'protein', 'polyPhen', 'cadd', 'sift', 'gerp', 'gene', 'ensembl', 'dbsnp', 'gnomad']
    summary = pd.read_csv(file, delimiter='\t', header=None, names=name)
    summary = insert_uuid4(summary)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.summary''')
        save_dataframe_using_copy(conn, summary, 'public', 'summary')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x02_gene(file, truncate):
    name = ['symbol', 'name', 'synonyms', 'gene_type', 'location', 'strand', 'description', 'omim', 'ensembl', 'clinvar', 'decipher', 'gnomad', 'panelapp', 'eye_disease', 'phenotypes', 'drugbank_id',
            'drug_target']
    gene = pd.read_csv(file, delimiter='\t', header=None, names=name)
    gene = insert_uuid4(gene)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.gene''')
        save_dataframe_using_copy(conn, gene, 'public', 'gene')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-l', '--limit', required=False)
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x03_gene_expression(file, limit, truncate):
    gene = read_gene_expression(file)
    gene = insert_uuid4(gene)
    # gene = gene.loc[10000001:20175936] todo 数据太大，分批导入

    if limit:
        click.echo('Limit data to: ' + limit)
        gene = gene[gene['gene'] == limit]

    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.gene_expression''')
        save_dataframe_using_copy(conn, gene, 'public', 'gene_expression')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x04_causality(file, truncate):
    name = ['variant', 'p_value', 'beta', 'disease']
    causality = pd.read_csv(file, delimiter='\t', header=None, names=name)
    causality = insert_uuid4(causality)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.causality''')
        save_dataframe_using_copy(conn, causality, 'public', 'causality')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x05_gnomad(file, truncate):
    gnomad = read_gnomad(file)
    gnomad = insert_uuid4(gnomad)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.gnomad''')
        save_dataframe_using_copy(conn, gnomad, 'public', 'gnomad')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x06_gwas(file, truncate):
    name = ['gene_id', 'gene', 'band', 'variant', 'ensembl', 'major_allele', 'minor_allele', 'p_value', 'beta', 'context', 'cadd', 'initial_sample_size', 'peplication_sample_size', 'pubmed',
            'disease']
    gwas = pd.read_csv(file, delimiter='\t', header=None, names=name)
    gwas = insert_uuid4(gwas)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.genetic_gwas''')
        save_dataframe_using_copy(conn, gwas, 'public', 'genetic_gwas')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x07_omim(file, truncate):
    name = ['gene', 'gene_name', 'variant', 'band', 'omim', 'ensembl', 'disease', 'confidence', 'phenotypes_in_omim', 'pubmed']
    omim = pd.read_csv(file, delimiter='\t', header=None, names=name)
    omim = insert_uuid4(omim)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.genetic_omim''')
        save_dataframe_using_copy(conn, omim, 'public', 'genetic_omim')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x08_micro_array(file, truncate):
    name = ['gene', 'ensembl_id', 'retina', 'corneal', 'corneal_epithelium', 'corneal_endothelium', 'conjunctiva', 'optic_nerve_head', 'lymphoblast', 'eye_orbit', 'lacrimal_gland', 'thyroid',
            'normal_uveal_melanocytes', 'retinal_detachment', 'diabetic_retinopathy', 'retinoblastoma', 'retinitis_pigmentosa', 'keratoconus', 'keratitis', 'trachoma', 'glaucoma',
            'fuchs_endothelial_corneal_dystrophy', 'uveal_melanoma', 'uveal_melanoma_mum2b', 'uveal_melanoma_ocm1a', 'graves_ophthalmopathy', 'nonspecific_orbital_inflammation', 'sarcoidosis',
            'granulomatosis_with_polyangiitis', 'thyroid_eye_disease']
    micro_array = pd.read_csv(file, delimiter='\t', header=None, names=name)
    micro_array = micro_array[
        ['gene', 'ensembl_id', 'retina', 'corneal', 'corneal_epithelium', 'corneal_endothelium', 'conjunctiva', 'optic_nerve_head', 'lymphoblast', 'eye_orbit', 'lacrimal_gland', 'thyroid',
         'normal_uveal_melanocytes']]
    micro_array = insert_uuid4(micro_array)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.expression_microarray_tissue''')
        save_dataframe_using_copy(conn, micro_array, 'public', 'expression_microarray_tissue')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x09_rna_seq(file, truncate):
    name = ['gene', 'ensembl_id', 'corneas', 'corneal_endothelial_cells', 'retina', 'retina_macula', 'retina_non_macula', 'rpe_macula', 'rpe_non_macula', 'retinal_endothelial_cells',
            'ipsc_derived_retinal_organoids', 'trabecular_meshwork_cells', 'age_related_macular_degeneration', 'diabetic_retinopathy', 'keratoconus', 'primary_open_angle_glaucoma',
            'retinitis_pigmentosa', 'retinoblastoma']
    rna_seq = pd.read_csv(file, delimiter='\t', header=None, names=name)
    rna_seq = rna_seq[['gene', 'ensembl_id', 'corneas', 'corneal_endothelial_cells', 'retina', 'retina_macula', 'retina_non_macula', 'rpe_macula', 'rpe_non_macula', 'retinal_endothelial_cells',
                       'ipsc_derived_retinal_organoids', 'trabecular_meshwork_cells']]
    rna_seq = insert_uuid4(rna_seq)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.expression_rna_seq_tissue''')
        save_dataframe_using_copy(conn, rna_seq, 'public', 'expression_rna_seq_tissue')


@cli.command()
@click.option('-p', '--prefix', required=True, default='')
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x11_epigenomics(prefix, truncate):
    if truncate:
        db.session.execute('''truncate public.epigenomics''')
    files = [
        ('AMD_Retina_MacR.bw', 'Age-related macular degeneration', 'ATAC-seq_Retina'),
        ('AMD_RPE_MacR.bw', 'Age-related macular degeneration', 'ATAC-seq_RPE'),
        ('corneal-epithelial-cells-H3K4me1.bw', 'Corneal epithelial', 'H3K4me1'),
        ('corneal-epithelial-cells-H3K4me3.bw', 'Corneal epithelial', 'H3K4me3'),
        ('corneal-epithelial-cells-H3K27ac.bw', 'Corneal epithelial', 'H3K27ac'),
        ('iPSC-RPE-ATAC.bw', 'Induced pluripotent stem cell-derived Retinal-pigment-epithelial', 'ATAC-seq'),
        ('iPSC-RPE-H3K27ac.bw', 'Induced pluripotent stem cell-derived Retinal-pigment-epithelial', ' H3K27ac'),
        ('Iris-pigment-epithelial-RRBS-methy.bw', 'Iris pigment epithelial', 'RRBS'),
        ('keratoconus-corneas-RRBS.bw', 'Keratoconus', 'RRBS'),
        ('Macula_ATAC.bw', 'Macula', 'ATAC-seq'),
        ('Retina-ATAC_1.bw', 'Retina', 'ATAC-seq_Retina'),
        ('Retina-ATAC_2.bw', 'Retina', 'ATAC-seq'),
        ('Retina-H3K27ac.bw', 'Retina', 'H3K27ac'),
        ('RPE-ATAC.bw', 'Retinal-pigment-epithelial', 'ATAC-seq_RPE'),
        ('RPE-H3K27ac.bw', 'Retinal-pigment-epithelial', 'H3K27ac'),
        ('RPE-Bis-methy.bw', 'Retinal-pigment-epithelial', 'Bisulfite-Seq'),
        ('RPE-H3K4me3.bw', 'Retinal-pigment-epithelial', 'H3K4me3'),
        ('retinal-pigment-epithelial-RRBS-methy.bw', 'Retinal-pigment-epithelial', 'RRBS'),
        ('RB-Bis-seq.bw', 'Retinoblastoma', 'Bisulfite-Seq'),
        ('RB-H3K27ac.bw', 'Retinoblastoma', 'H3K27ac'),
        ('RB-H3K27me3.bw', 'Retinoblastoma', 'H3K27me3'),
        ('RB-H3K4me1.bw', 'Retinoblastoma', 'H3K4me1'),
        ('RB-H3K4me3.bw', 'Retinoblastoma', 'H3K4me3'),
        ('RB-H3K9me3.bw', 'Retinoblastoma', 'H3K9me3'),
        ('Uveal melanoma_methylation_1.bw', 'Uveal melanoma', 'methylation1 450'),
        ('Uveal melanoma_methylation_2.bw', 'Uveal melanoma', 'methylation2 450'),
        ('WERI-Rb-1-H3K4me3.bw', 'Wills Eye Research Institute-Retinoblastoma-1', 'H3K4me3'),
    ]
    for f, disease, data_type in files:
        name = '/'.join([prefix, f]) if prefix else f
        ep = Epigenomics(file_=name, disease=disease, data_type=data_type)
        db.session.add(ep)
    db.session.commit()


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x12_microarray_disease(file, truncate):
    name = ['gene', 'ensembl_id', 'retina', 'corneal', 'corneal_epithelium', 'corneal_endothelium', 'conjunctiva', 'optic_nerve_head', 'lymphoblast', 'eye_orbit', 'lacrimal_gland', 'thyroid',
            'normal_uveal_melanocytes', 'retinal_detachment', 'diabetic_retinopathy', 'retinoblastoma', 'retinitis_pigmentosa', 'keratoconus', 'keratitis', 'trachoma', 'glaucoma',
            'fuchs_endothelial_corneal_dystrophy', 'uveal_melanoma', 'uveal_melanoma_mum2b', 'uveal_melanoma_ocm1a', 'graves_ophthalmopathy', 'nonspecific_orbital_inflammation', 'sarcoidosis',
            'granulomatosis_with_polyangiitis', 'thyroid_eye_disease']
    micro_array = pd.read_csv(file, delimiter='\t', header=None, names=name)
    micro_array = micro_array[['gene', 'ensembl_id', 'retinal_detachment', 'diabetic_retinopathy', 'retinoblastoma', 'retinitis_pigmentosa', 'keratoconus', 'keratitis', 'trachoma',
                               'glaucoma', 'fuchs_endothelial_corneal_dystrophy', 'uveal_melanoma', 'uveal_melanoma_mum2b', 'uveal_melanoma_ocm1a', 'graves_ophthalmopathy',
                               'nonspecific_orbital_inflammation', 'sarcoidosis', 'granulomatosis_with_polyangiitis', 'thyroid_eye_disease']]
    micro_array = insert_uuid4(micro_array)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.expression_microarray_disease''')
        save_dataframe_using_copy(conn, micro_array, 'public', 'expression_microarray_disease')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x13_rna_disease(file, truncate):
    name = ['gene', 'ensembl_id', 'corneas', 'corneal_endothelial_cells', 'retina', 'retina_macula', 'retina_non_macula', 'rpe_macula', 'rpe_non_macula', 'retinal_endothelial_cells',
            'ipsc_derived_retinal_organoids', 'trabecular_meshwork_cells', 'age_related_macular_degeneration', 'diabetic_retinopathy', 'keratoconus', 'primary_open_angle_glaucoma',
            'retinitis_pigmentosa', 'retinoblastoma']
    rna_seq = pd.read_csv(file, delimiter='\t', header=None, names=name)
    rna_seq = rna_seq[['gene', 'ensembl_id', 'age_related_macular_degeneration', 'diabetic_retinopathy', 'keratoconus', 'primary_open_angle_glaucoma', 'retinitis_pigmentosa', 'retinoblastoma']]
    rna_seq = insert_uuid4(rna_seq)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.expression_rna_seq_disease''')
        save_dataframe_using_copy(conn, rna_seq, 'public', 'expression_rna_seq_disease')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x14_mouse_expression(file, truncate):
    name = ['gene', 'human', 'e10_5', 'e11_5', 'e12_5', 'e13_5', 'web1_e10_5__12_5', 'web2_e11_5__13_5', 'p8_a', 'p8_b', 'p12_a', 'p12_b', 'p20_a', 'p20_b', 'p42_a', 'p42_b', 'p52_a', 'p52_b',
            'web_p10_11_12_a', 'web_p10_11_12_b']
    mouse = pd.read_csv(file, delimiter='\t', header=None, names=name)
    mouse = insert_uuid4(mouse)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.expression_mouse''')
        save_dataframe_using_copy(conn, mouse, 'public', 'expression_mouse')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x15_single_markers(file, truncate):
    file_name = os.path.basename(file).split('.')[0]
    name = ['gene', 'cluster', 'labels', 'p_val', 'avg', 'pct1', 'pct2'] if file_name == 'GSE107618' else ['gene', 'cluster', 'labels', 'p_val', 'avg', 'p_val_adj', 'pct1', 'pct2']
    markers = pd.read_csv(file, delimiter='\t', header=None, names=name)
    markers = insert_uuid4(markers)
    markers = insert_file_marker(markers, file)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.markers_cell''')
        save_dataframe_using_copy(conn, markers, 'public', 'markers_cell')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x17_single_out(file, truncate):
    name = ['name', 'xaxis', 'yaxis', 'cluster', 'labels']
    out = pd.read_csv(file, delimiter='\t', header=None, names=name)
    out = insert_uuid4(out)
    out = insert_file_out(out, file)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.markers_cell''')
        save_dataframe_using_copy(conn, out, 'public', 'out_cell')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x18_network_disease(file, truncate):
    name = ['gene', 'weight', 'disease', 'dataset']
    net = pd.read_csv(file, delimiter='\t', header=None, names=name)
    net = insert_uuid4(net)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.gene_network_disease''')
        save_dataframe_using_copy(conn, net, 'public', 'gene_network_disease')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x19_go(file, truncate):
    name = ['category', 'term', 'count', 'percent', 'p_value', 'genes', 'list_total', 'pop_hits', 'pop_total', 'fold_enrichment', 'bonferroni', 'benjamini', 'fdr']
    dis_go = pd.read_csv(file, delimiter='\t', header=None, names=name)
    dis_go = insert_dis_type(dis_go, file)
    dis_go = insert_uuid4(dis_go)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.disease_go''')
        save_dataframe_using_copy(conn, dis_go, 'public', 'disease_go')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x20_tissue_significance(file, truncate):
    name = ['gene_symbol', 'corneas', 'corneal_endothelial_cells', 'retina', 'retina_macula', 'retina_non_macula', 'rpe_macula', 'rpe_non_macula', 'retinal_endothelial_cells',
            'ipsc_derived_retinal_organoids', 'trabecular_meshwork_cells']
    tis = pd.read_csv(file, delimiter='\t', header=None, names=name)
    tis = insert_uuid4(tis)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.tissue_gene_significance''')
        save_dataframe_using_copy(conn, tis, 'public', 'tissue_gene_significance')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x21_gene_significance(file, truncate):
    name = ['gene', 'amd', 'dr', 'kc', 'glc', 'rp', 'rb']
    gene = pd.read_csv(file, delimiter='\t', header=None, names=name)
    gene = insert_uuid4(gene)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.disease_go''')
        save_dataframe_using_copy(conn, gene, 'public', 'gene_disease_significance')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-d', '--database', required=True)
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x22_gene_interaction(file, database, truncate):
    dis = pd.read_csv(file, delimiter='\t', error_bad_lines=False, chunksize=5000000, header=None, names=['gene', 'contrast_gene', 'weight'])
    for chunk in dis:
        engine = db.engine
        with engine.begin() as conn:
            if truncate:
                conn.execute(f'''truncate public.{database}''')
            save_dataframe_using_copy(conn, chunk, 'public', database)


@cli.command()
@click.option('-k', '--key', required=True)
@click.option('-v', '--value', required=True)
@with_appcontext
def x24_generic_config(key, value):
    db.session.execute('''truncate public.app_config''')
    config = AppConfig(key=key, value=json.loads(value))
    db.session.add(config)
    db.session.commit()


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x25_epigenetic_alteration(file, truncate):
    name = ['gene', 'normal_retina', 'amd_retina', 'normal_rpe', 'amd_rpe']
    gene = pd.read_csv(file, delimiter='\t', header=None, names=name)
    gene = insert_uuid4(gene)
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.epigenetic_alteration''')
        save_dataframe_using_copy(conn, gene, 'public', 'epigenetic_alteration')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-d', '--disease', required=True)
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x26_disease_correct(file, disease, truncate):
    dis = pd.read_csv(file, sep='\t', delimiter=' ')
    dis = insert_uuid4(dis)
    dis.rename(columns={'Symbol': 'gene', 'Module': 'module', 'KME': 'kme'}, inplace=True)
    dis['disease'] = disease
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.disease_go''')
        save_dataframe_using_copy(conn, dis, 'public', 'gene_disease_correct')


@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, resolve_path=True))
@click.option('-t', '--tissue', required=True)
@click.option('-t', '--truncate', default=False, required=True, help='是否清空数据表')
@with_appcontext
def x27_tissue_correct(file, tissue, truncate):
    tis = pd.read_csv(file, sep='\t', delimiter=' ')
    tis = insert_uuid4(tis)
    tis.rename(columns={'Symbol': 'gene', 'Module': 'module', 'KME': 'kme'}, inplace=True)
    tis['tissue'] = tissue
    engine = db.engine
    with engine.begin() as conn:
        if truncate:
            conn.execute('''truncate public.disease_go''')
        save_dataframe_using_copy(conn, tis, 'public', 'gene_tissue_correct')


@cli.command()
@click.option('-d', '--dir', '_dir', required=True, type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.pass_context
@with_appcontext
def all(ctx, _dir):
    d = Path(_dir)
    click.echo('x01_snp_gene_summary')
    ctx.invoke(x01_snp_gene_summary, file=str(d / 'variant/snp_gene_context_summary.txt'))

    click.echo('x02_gene')
    ctx.invoke(x02_gene, file=str(d / 'gene/index_gene.txt'))

    click.echo('x03_gene_expression')
    ctx.invoke(x03_gene_expression, file=str(d / 'gene/RNA-Seq.combine.TPM.addID.boxplot.txt'), limit='CFH')

    click.echo('x04_causality')
    ctx.invoke(x04_causality, file=str(d / 'variant/Association.txt'))

    click.echo('x05_gnomad')
    ctx.invoke(x05_gnomad, file=str(d / 'variant/gnomad.txt'))

    click.echo('x06_gwas')
    ctx.invoke(x06_gwas, file=str(d / 'disease/GWAS.txt'))

    click.echo('x07_omim')
    ctx.invoke(x07_omim, file=str(d / 'disease/OMIM.txt'))

    click.echo('x08_micro_array')
    ctx.invoke(x08_micro_array, file=str(d / 'expression/Microarray.combine.mean_log2exp.addID.heatmap.txt'))
    #
    click.echo('x09_rna_seq')
    ctx.invoke(x09_rna_seq, file=str(d / 'expression/RNA-Seq.combine.mean_TPM.addID.heatmap.txt'))

    click.echo('x11_epigenomics')
    ctx.invoke(x11_epigenomics, prefix='http://localhost:8999/epigenomics')

    click.echo('x12_microarray_disease')
    ctx.invoke(x12_microarray_disease, file=str(d / 'expression/Microarray.combine.mean_log2exp.addID.heatmap.txt'))

    click.echo('x13_rna_disease')
    ctx.invoke(x13_rna_disease, file=str(d / 'expression/RNA-Seq.combine.mean_TPM.addID.heatmap.txt'))

    click.echo('x14_mouse_expression')
    ctx.invoke(x14_mouse_expression, file=str(d / 'expression/Mouse.development.combine.mean_exp.addID.txt'))

    click.echo('x15_single_markers')
    ctx.invoke(x15_single_markers, file=str(d / 'singlecell/markers/E-MTAB-7316.markers.txt'))

    click.echo('x15_single_markers')
    ctx.invoke(x15_single_markers, file=str(d / 'singlecell/markers/GSE107618.markers.txt'))

    click.echo('x15_single_markers')
    ctx.invoke(x15_single_markers, file=str(d / 'singlecell/markers/GSE133707.markers.txt'))

    click.echo('x15_single_markers')
    ctx.invoke(x15_single_markers, file=str(d / 'singlecell/markers/GSE135922.markers.txt'))

    click.echo('x15_single_markers')
    ctx.invoke(x15_single_markers, file=str(d / 'singlecell/markers/GSE139829.markers.txt'))

    click.echo('x15_single_markers')
    ctx.invoke(x15_single_markers, file=str(d / 'singlecell/markers/GSE134355.markers.txt'))

    click.echo('x17_single_out')
    ctx.invoke(x17_single_out, file=str(d / 'singlecell/outs/E-MTAB-7316.tSNE_out.txt'))

    click.echo('x17_single_out')
    ctx.invoke(x17_single_out, file=str(d / 'singlecell/outs/GSE107618.tSNE_out.txt'))

    click.echo('x17_single_out')
    ctx.invoke(x17_single_out, file=str(d / 'singlecell/outs/GSE133707.UMAP_out.txt'))

    click.echo('x17_single_out')
    ctx.invoke(x17_single_out, file=str(d / 'singlecell/outs/GSE134355.tSNE_out.txt'))

    click.echo('x17_single_out')
    ctx.invoke(x17_single_out, file=str(d / 'singlecell/outs/GSE135922.UMAP_out.txt'))

    click.echo('x17_single_out')
    ctx.invoke(x17_single_out, file=str(d / 'singlecell/outs/GSE139829.tSNE_out.txt'))

    click.echo('x18_network_disease')
    ctx.invoke(x18_network_disease, file=str(d / 'analysis/Gene_disease_network_final.txt'))

    file_list = ['AMD.GO.BP.txt', 'AMD.GO.CC.txt', 'AMD.GO.KEGG.txt', 'AMD.GO.MF.txt', 'Corneal_astigmatism.GO.BP.txt', 'Corneal_astigmatism.GO.CC.txt', 'Corneal_astigmatism.GO.KEGG.txt',
                 'Corneal_astigmatism.GO.MF.txt', 'GLC.GO.BP.txt', 'GLC.GO.CC.txt', 'GLC.GO.KEGG.txt', 'GLC.GO.MF.txt', 'Myopia.GO.BP.txt', 'Myopia.GO.CC.txt', 'Myopia.GO.KEGG.txt',
                 'Myopia.GO.MF.txt', 'Refractive_astigmatism.GO.BP.txt', 'Refractive_astigmatism.GO.CC.txt', 'Refractive_astigmatism.GO.MF.txt', 'Refractive_error.GO.BP.txt',
                 'Refractive_error.GO.CC.txt', 'Refractive_error.GO.KEGG.txt', 'Refractive_error.GO.MF.txt']
    for file in file_list:
        click.echo('x19_go: ' + file)
        ctx.invoke(x19_go, file=str(d / f'analysis/GO/{file}'))

    click.echo('x20_tissue_significance')
    ctx.invoke(x20_tissue_significance, file=str(d / 'analysis/Network/Tissue.Network.gene_disease_significance.txt'))

    click.echo('x21_gene_significance')
    ctx.invoke(x21_gene_significance, file=str(d / 'analysis/Network/Disease.Network.gene_disease_significance.txt'))

    click.echo('x22_gene_interaction')
    ctx.invoke(x22_gene_interaction, file=str(d / 'analysis/Network/Disease.Network.gene_gene_interaction.txt'))

    click.echo('x25_epigenetic_alteration')
    ctx.invoke(x25_epigenetic_alteration, file=str(d / 'analysis/Epigenetic_alteration.AMD_gene.signal.txt'))


@cli.command()
@click.pass_context
@with_appcontext
def igv_config(ctx):
    click.echo('writing default igv config')
    ctx.invoke(x24_generic_config, key='igv.ref.hg38', value=json.dumps(_reference_track()))


def _reference_track():
    prefix = "https://t-optical.lab.ekitech.ai:11443"
    return {
        "id": "hg38",
        "name": "Human (GRCh38/hg38)",
        "fasta": ("%s/data/genome/ref/hg38/hg38.fa" % prefix),
        "index": ("%s/data/genome/ref/hg38/hg38.fa.fai" % prefix),
        "cytoband": ("%s/data/genome/ref/hg38/cytoBandIdeo.txt.gz" % prefix),
        "tracks": [
            {
                "name": "Refseq Genes",
                "format": "refgene",
                "": ("%s/data/genome/ref/hg38/refGene.sorted.txt.gz" % prefix),
                "index": ("%s/data/genome/ref/hg38/refGene.sorted.txt.gz.tbi" % prefix),
                "visibilityWindow": -1,
                "removable": False,
                "order": 1000000
            }
        ]
    }
