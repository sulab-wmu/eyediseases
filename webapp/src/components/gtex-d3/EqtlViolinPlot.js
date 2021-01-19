/*
 * Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
 * All rights reserved.
 */

"use strict";
import {getGtexUrls} from "./modules/gtexDataParser";
import {groupedViolinPlot} from "./GTExViz";

export function render(par, gencodeId, variantId, tissueId, groupName = undefined, urls = getGtexUrls()) {
    par.numPoints = 10;
    groupedViolinPlot(par);

    // json(urls['dyneqtl'] + `?variantId=${variantId}&gencodeId=${gencodeId}&tissueSiteDetailId=${tissueId}`, {credentials:'include'})
    //     .then(function(json){
    //         let data = parseDynEqtl(json);
    //         // construct the dynEqtl data for the three genotypes: ref, het, alt
    //         par.data = [
    //             {
    //                 group: groupName||data.tissueSiteDetailId,
    //                 label: data.ref.length>2?"ref":data.ref,
    //                 size: data.homoRefExp.length,
    //                 values: data.homoRefExp
    //             },
    //             {
    //                 group: groupName||data.tissueSiteDetailId,
    //                 label: data.het.length>2?"het":data.het,
    //                 size: data.heteroExp.length,
    //                 values: data.heteroExp
    //             },
    //             {
    //                 group: groupName||data.tissueSiteDetailId,
    //                 label: data.alt.length>2?"alt":data.alt,
    //                 size: data.homoAltExp.length,
    //                 values: data.homoAltExp
    //             }
    //         ];
    //
    //
    //     })


}
