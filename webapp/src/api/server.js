/*
 * Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
 * All rights reserved.
 */

import {get} from './index'

/** 获取指定gwas结果 */
export const getGWAS = (obj) => {
    return get('/api/disease/gwas', obj);
};

/** 获取指定omim结果 */
export const getOMIM = (obj) => {
    return get('/api/disease/omim', obj);
};

/** 获取指定gene详情结果 */
export const getGeneDetails = (val) => {
    return get('/api/gene', {name: val});
};

/** 获取指定gene详情结果 */
export const getVariantDetails = (val) => {
    return get('/api/variant', {name: val});
};

/** 获取指定gene list */
export const getDiseaseList = (val) => {
    return get('/api/disease/list', {name: val});
};

/** 获取指定single cell cluster list */
export const getSingleCellList = (val) => {
    return get('/api/singleCell/list', {name: val});
};

/** 获取指定single cell data */
export const getSingleCell = (obj) => {
    return get('/api/singleCell', obj);
};

/** 获取指定ExpressionDatasets详情结果 */
export const getExpressionDatasets = () => {
    return get('/api/expression/datasets', {});
};

export const getHeatMapData = (obj) => {
    return get('/api/expression/heatmap_data', obj);
};

/** 获取指定getGeneExpressionViolin */
export const getGeneExpressionViolin = (val) => {
    return get('/api/gene/expression-violin', {name: val});
};

export const getEpigenomicsList = () => {
    return get('/api/epigenomics/list');
};

export const getEpigenomics = () => {
    return get('/api/epigenomics/tracks');
};

export const getDiseaseExist = (val) => {
    return get('api/search/exist', {name: val})
};

export const getSingeleCellGridData = (obj) => {
    return get('api/singleCell/grid', obj)
};

export const getDiseaseGo = (val) => {
    return get('/api/analysis/disease-go', {
        disease: val
    });
};

export const getDiseaseCo = (obj) => {
    return get('/api/analysis/disease-co', obj);
};

export const getGeneDiseaseNetwork = (obj) => {
    return get('/api/analysis/gene-disease-network', obj);
};

export const getHomeAllList = () => {
    return get('/api/search/total', {});
};

export const getAlteration = () => {
    return get('/api/analysis/alteration');
};

export const getSignificance = (obj) => {
    return get('/api/analysis/significance', obj);
};
