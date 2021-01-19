<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <div id="app">
        <section class="section page-top">
            <div class="container">

                <b-navbar :shadow="true">
                    <template slot="brand">
                        <b-navbar-item tag="router-link" :to="{ path: '/' }">
                            <img src="./assets/logo.png" alt="EyeDiseases">
                        </b-navbar-item>
                    </template>

                    <template slot="end">
                        <b-navbar-item tag="router-link" :to="{name: 'home'}">{{ $t('Home') }}</b-navbar-item>

                        <b-navbar-dropdown :label=browse>
                            <b-navbar-item tag="router-link" :to="{name: 'disease'}">{{ $t('Disease') }}</b-navbar-item>
                            <b-navbar-item tag="router-link" :to="{name: 'expression'}">{{ $t('Expression') }}</b-navbar-item>
                            <b-navbar-item tag="router-link" :to="{name: 'single-cell'}">{{ $t('Single') }}</b-navbar-item>
                            <b-navbar-item tag="router-link" :to="{name: 'epigenomics'}">{{ $t('Epigenomics') }}</b-navbar-item>
                        </b-navbar-dropdown>

                        <b-navbar-item tag="router-link" :to="{name: 'analysis'}">{{ $t('Analysis') }}</b-navbar-item>
                        <b-navbar-item tag="router-link" :to="{name: 'statistics'}">{{ $t('Statistics') }}</b-navbar-item>
                        <b-navbar-item tag="router-link" :to="{name: 'download'}">{{ $t('Download') }}</b-navbar-item>
                        <b-navbar-item tag="router-link" :to="{name: 'document'}">{{ $t('Document') }}</b-navbar-item>
                        <b-navbar-item tag="router-link" :to="{name: 'contact'}">{{ $t('Contact') }}</b-navbar-item>
                        <b-navbar-dropdown :label=language>
                            <b-navbar-item @click="ChinaLanguage">简体中文</b-navbar-item>
                            <b-navbar-item @click="EnglishLanguage">English</b-navbar-item>
                        </b-navbar-dropdown>
                    </template>
                </b-navbar>
            </div>
        </section>

        <router-view/>

        <section class="section">
            <div class="container">
                <div class="has-text-centered">
                    <hr>
                    <p>
                        Copyright © {{ currentYear }}, Institute of Biomedical Big Data,
                        <a href="http://en.wmu.edu.cn/" target="_blank">Wenzhou Medical University</a> | All Rights Reserved
                    </p>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
    import Vue from "vue";

    export default {
        data() {
            return {
                currentYear: new Date().getFullYear(),
                browse: this.$t('Browse'),
                language: this.$t('Language'),
            }
        },
        watch: {
            '$route'(to, from) {
                document.title = to.meta.title ? to.meta.title + ' - ' + 'EyeDiseases' : 'EyeDiseases';
            }
        },
        methods: {
            ChinaLanguage() {
                Vue.config.lang = 'zh'
                this.browse = '浏览'
                this.language = '语言'
            },
            EnglishLanguage() {
                Vue.config.lang = 'en'
                this.browse = 'Browse'
                this.language = 'language'
            }
        }
    }
</script>

<style lang="scss">
@import "~ag-grid-community/src/styles/ag-grid.scss";
@import "~ag-grid-community/src/styles/ag-theme-alpine/sass/ag-theme-alpine-mixin.scss";
@import "~ag-grid-community/src/styles/ag-theme-balham/sass/ag-theme-balham-mixin.scss";

.ag-theme-balham {
    @include ag-theme-balham((
        odd-row-background-color: #f5f5f5,
        row-border-color: transparent,
        row-hover-color: null,
        checkbox-checked-color: #2661ad,
        range-selection-border-color: #ff00b1,
        range-selection-background-color: #03305633
    ));

    .ag-menu-option-active {
        background-color: #2661ad;
        color: white;
    }
}

.ag-theme-alpine {
    @include ag-theme-balham((
        odd-row-background-color: #f5f5f5,
        row-border-color: transparent,
        row-hover-color: null,
        checkbox-checked-color: #2661ad,
        range-selection-border-color: #ff00b1,
        range-selection-background-color: #03305633
    ));

    .ag-menu-option-active {
        background-color: #2661ad;
        color: white;
    }
}

.page-top {
    padding-top: 0;
    padding-bottom: 2px;
}
</style>
