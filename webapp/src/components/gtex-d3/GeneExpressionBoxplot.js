/*
 * Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
 * All rights reserved.
 */
'use strict';

import {json} from 'd3-fetch';
import {getGtexUrls, parseGeneExpressionForBoxplot, parseTissues} from './modules/gtexDataParser';

import Boxplot from './modules/Boxplot';

export function launch(rootId, gencodeId, urls = getGtexUrls()) {
    const promises = [
        json(urls.tissue, {credentials: 'include'}),
        json(urls.geneExp + gencodeId, {credentials: 'include'})
    ];

    Promise.all(promises)
        .then(function (args) {
            const tissues = parseTissues(args[0]);
            const tissueIdNameMap = {};
            const tissueIdColorMap = {};
            tissues.forEach(x => {
                tissueIdNameMap[x.tissueSiteDetailId] = x.tissueSiteDetail;
                tissueIdColorMap[x.tissueSiteDetailId] = x.colorHex;
            });
            const boxplotData = parseGeneExpressionForBoxplot(args[1], tissueIdNameMap, tissueIdColorMap);
            let ids = {
                rootId: rootId,
                tooltipId: 'boxplot-tooltip'
            };
            let boxplot = new Boxplot(boxplotData);
            let plotOptions = {
                width: 1000,
                height: 600,
                marginLeft: 50,
                marginRight: 100,
                marginBottom: 160,
                yAxisUnit: 'TPM'
            };
            boxplot.render(ids.rootId, plotOptions);
        });
}
