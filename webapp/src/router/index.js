/*
 * Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
 * All rights reserved.
 */

import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'home',
        component: Home,
        meta: {title: 'Home'}
    },
    {
        path: '/disease',
        name: 'disease',
        component: () => import(/* webpackChunkName: "disease" */ '../views/Disease.vue'),
        meta: {title: 'Disease', key: 2.1}
    },
    {
        path: '/browse-disease',
        name: 'browse-disease',
        component: () => import(/* webpackChunkName: "browse-disease" */ '../views/Browse.vue'),
        meta: {title: 'Browse', key: 2}
    },
    {
        path: '/expression',
        name: 'expression',
        component: () => import(/* webpackChunkName: "expression" */ '../views/Expression.vue'),
        meta: {title: 'Expression', key: 2.1}
    },

    {
        path: '/single-cell',
        name: 'single-cell',
        component: () => import(/* webpackChunkName: "single-cell" */ '../views/SingleCellRNASeq.vue'),
        meta: {title: 'Single-Cell RNASeq'}
    },
    {
        path: '/epigenomics',
        name: 'epigenomics',
        component: () => import(/* webpackChunkName: "epigenomics" */ '../views/Epigenomics.vue'),
        meta: {title: 'Epigenomics'}
    },

    // #################### Direct search jump pages ####################
    {
        path: '/gene',
        name: 'gene',
        component: () => import(/* webpackChunkName: "gene" */ '../views/Gene.vue'),
        meta: {title: 'Gene'}
    },
    {
        path: '/variants',
        name: 'variants',
        component: () => import(/* webpackChunkName: "variants" */ '../views/Variants.vue'),
        meta: {title: 'Variants'}
    },
    {
        path: '/analysis',
        name: 'analysis',
        component: () => import(/* webpackChunkName: "analysis" */ '../views/Analysis.vue'),
        meta: {title: 'Analysis', key: 3}
    },
    {
        path: '/statistics',
        name: 'statistics',
        component: () => import(/* webpackChunkName: "statistics" */ '../views/Statistics.vue'),
        meta: {title: 'Statistics', key: 5}
    },
    {
        path: '/download',
        name: 'download',
        component: () => import(/* webpackChunkName: "download" */ '../views/Download.vue'),
        meta: {title: 'Download', key: 5}
    },
    {
        path: '/document',
        name: 'document',
        component: () => import(/* webpackChunkName: "document" */ '../views/Document.vue'),
        meta: {title: 'Document', key: 5}
    },
    {
        path: '/contact',
        name: 'contact',
        component: () => import(/* webpackChunkName: "contact" */ '../views/Contact.vue'),
        meta: {title: 'Contact', key: 5}
    },
    {
        path: '/404',
        name: '404',
        component: () => import(/* webpackChunkName: "404" */ '../views/404.vue'),
        meta: {title: 'Not Found', key: 5}
    },
    {
        path: '*',
        redirect: {name: '404'},
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
