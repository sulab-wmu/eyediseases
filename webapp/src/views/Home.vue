<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <div class="home">
        <section class="has-bg-img">
            <figure>
                <img src="../assets/home-banner.jpg">
            </figure>
            <div class="disease-position">
                <b-field>
                    <b-autocomplete
                        rounded
                        v-model="diseaseName"
                        :data="filterDiseaseList"
                        :placeholder="this.$t('Basadbd')"
                        clearable
                        class="disease-search"
                        @select="option => diseaseSelect = option">
                        <template slot="empty">No results found</template>
                    </b-autocomplete>
                </b-field>

                <router-link class="disease-hint"
                             :to="{name: 'browse-disease', query: {name: 'Age-related macular degeneration'}}">
                    {{ $t('example') }} {{ $t('armd') }}
                </router-link>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="columns reverse-row-order">
                    <div class="column is-three-quarters">
                        <h1 class="title">{{ $t('Explore') }}</h1>

                        <div class="tile is-ancestor">
                            <div class="tile is-parent is-vertical">
                                <article class="tile is-child">
                                    <div class="columns">
                                        <div class="column side-title valign-middle"><h5 class="title is-5">{{ $t('Genetics') }}</h5></div>
                                        <div class="column middle-column valign-middle">
                                            <figure class="image is-48x48"><img src="../assets/icon-gene.jpg"></figure>
                                            <b-autocomplete
                                                style="width: 130px"
                                                v-model="geneName"
                                                :data="filterGeneList"
                                                placeholder="By gene"
                                                clearable
                                                @select="option => geneSelect = option">
                                                <template slot="empty">No results found</template>
                                            </b-autocomplete>
                                            <router-link :to="{name: 'gene', query: {name: 'CFH'}}" style="margin-left: 5px; font-size: 0.85em">{{ $t('example') }} CFH</router-link>
                                        </div>
                                        <div class="column end-column valign-middle">{{ $t('Bassdbg') }}</div>
                                    </div>

                                    <div class="columns">
                                        <div class="column side-title"></div>
                                        <div class="column middle-column valign-middle">
                                            <figure class="image is-48x48"><img src="../assets/icon-human.jpg"></figure>
                                            <b-autocomplete
                                                style="width: 130px"
                                                v-model="variantName"
                                                :data="filterVariantList"
                                                placeholder="By Variant"
                                                clearable
                                                @select="option = variantSelect = option">
                                                <template slot="empty">No results found</template>
                                            </b-autocomplete>
                                            <router-link :to="{name: 'variants', query: {name: 'rs10490924'}}" style="margin-left: 5px; font-size: 0.85em">{{ $t('example') }} rs10490924</router-link>
                                        </div>
                                        <div class="column valign-middle">{{ $t('Basadbv') }}</div>
                                    </div>
                                    <hr>
                                </article>

                                <article class="tile is-child">
                                    <div class="columns">
                                        <div class="column side-title valign-middle"><h5 class="title is-5">{{ $t('Transcriptomics') }}</h5></div>
                                        <div class="column middle-column valign-middle">
                                            <figure class="image is-48x48"><img src="../assets/icon-expression.jpg"></figure>
                                            <router-link :to="{name: 'expression', query: {species: 'human'}}">{{ $t('multi_gene_query') }}</router-link>
                                        </div>
                                        <div class="column valign-middle">{{ $t('Basebgad') }}</div>
                                    </div>

                                    <div class="columns">
                                        <div class="column side-title"></div>
                                        <div class="column middle-column valign-middle">
                                            <figure class="image is-48x48"><img src="../assets/icon-mouse.jpg"></figure>
                                            <router-link :to="{name: 'expression', query: {species: 'mouse'}}">{{ $t('eye_development') }}</router-link>
                                        </div>
                                        <div class="column valign-middle">{{ $t('Basebgas') }}</div>
                                    </div>

                                    <div class="columns">
                                        <div class="column side-title"></div>
                                        <div class="column middle-column valign-middle">
                                            <figure class="image is-48x48"><img src="../assets/icon-singlecell.jpg"></figure>
                                            <router-link :to="{name: 'single-cell'}">{{ $t('single_rna') }}</router-link>
                                        </div>
                                        <div class="column valign-middle">{{ $t('Vctamgbtad') }}</div>
                                    </div>
                                    <hr>
                                </article>

                                <article class="tile is-child">
                                    <div class="columns">
                                        <div class="column side-title valign-middle"><h5 class="title is-5">{{ $t('Epigenomics') }}</h5></div>
                                        <div class="column middle-column valign-middle">
                                            <figure class="image is-48x48"><img src="../assets/icon-epigenomic.jpg"></figure>
                                            <router-link :to="{name: 'epigenomics'}">{{ $t('Genome') }}</router-link>
                                        </div>
                                        <div class="column valign-middle">{{ $t('Bgsdbdt') }}</div>
                                    </div>
                                    <hr>
                                </article>
                            </div>
                        </div>

                        <h1 class="title">{{ $t('EyeDS') }}</h1>
                        <nav class="level">
                            <div v-for="item in stats" class="level-item has-text-centered">
                                <div>
                                    <p class="heading">{{ $t(item.name) }}</p>
                                    <p class="title" :style="{color: item.color}">{{ item.count }}</p>
                                </div>
                            </div>
                        </nav>
                    </div>

                    <div class="column">
                        <div class="content">
                            <h1 class="title">{{ $t('Introduction') }}</h1>
                            <p style="text-align: justify">{{ $t('introduction') }}</p>
                            <div class="visit-tracker" ref="visitTracker"></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>

import {getHomeAllList} from "../api/server";

export default {
  name: 'Home',
  data() {
    return {
      disease: '',
      gene: '',
      variant: '',

      stats: [
        {name: 'DISEASES', count: '185', color: '#D67A48'},
        {name: 'GENES', count: '1,253', color: '#45969A'},
        {name: 'VARIANTS', count: '2,447', color: '#45969A'},
        {name: 'RNA', count: '1,056', color: '#988E41'},
        {name: 'MICROARRAY', count: '710', color: '#988E41'},
        {name: 'EPIGENOMIC', count: '105', color: '#FF0000'},
        {name: 'SINGLE', count: '6', color: '#988E41'},
        {name: 'STUDIES', count: '1,132', color: '#429B44'},
      ],

                name: '',
                selected: null,

                diseasesList: [],
                geneList: [],
                variantsList: [],

                diseaseName: '',
                geneName: '',
                variantName: '',

                diseaseSelect: null,
                geneSelect: null,
                variantSelect: null
            }
        },
        watch: {
            diseaseName(val) {
                if (val && this.diseasesList.includes(val)) {
                    this.$router.push({
                        name: 'browse-disease',
                        query: {name: val}
                    })
                }
            },
            geneName(val) {
                if (val && this.geneList.includes(val)) {
                    this.$router.push({
                        name: 'gene',
                        query: {name: val}
                    })
                }
            },
            variantName(val) {
                if (val && this.variantsList.includes(val)) {
                    this.$router.push({
                        name: 'variants',
                        query: {name: val}
                    })
                }
            },

        },
        computed: {
            filterDiseaseList() {
                return this.diseasesList.filter((option) => {
                    return option
                        .toString()
                        .toLowerCase()
                        .indexOf(this.diseaseName.toLowerCase()) >= 0
                })
            },
            filterGeneList() {
                return this.geneList.filter((option) => {
                    return option
                        .toString()
                        .toLowerCase()
                        .indexOf(this.geneName.toLowerCase()) >= 0
                })
            },
            filterVariantList() {
                return this.variantsList.filter((option) => {
                    return option
                        .toString()
                        .toLowerCase()
                        .indexOf(this.variantName.toLowerCase()) >= 0
                })
            }
        },

        mounted() {
            this.createRevolverMapsTracker();
        },

        methods: {
            defaultDisease() {
                this.$router.push({
                    name: 'browse-disease',
                    query: {name: 'Age-related macular degeneration'}
                })
            },
            createRevolverMapsTracker() {
                const script = document.createElement('script');
                script.type = 'text/javascript';
                script.src = '//rf.revolvermaps.com/0/0/6.js?i=5p4notlylpp&amp;m=7&amp;c=e63100&amp;cr1=ffffff&amp;f=arial&amp;l=0&amp;bv=90&amp;lx=-420&amp;ly=420&amp;hi=20&amp;he=7&amp;hc=a8ddff&amp;rs=80';
                script.async = true;
                this.$refs.visitTracker.appendChild(script);
            },
        },
        created() {
            getHomeAllList().then((res) => {
                this.diseasesList = res.data.disease;
                this.geneList = res.data.gene;
                this.variantsList = res.data.variant
            })
        }
    }
</script>

<style lang="scss" scoped>
.visit-tracker ::v-deep iframe {
    width: 318px;
    height: 318px;
}

.valign-middle {
    display: flex;
    align-items: center;
}

.column .is-48x48 {
    margin-right: 15px;
}

.has-bg-img {
    /*overflow: hidden;*/
    position: relative;
}

.disease-position {
    position: absolute;
    padding-left: 6%;
    bottom: 7%;

    .field {
        margin-bottom: 0;
    }

    .disease-search {
        width: 325px;
    }
}

.disease-hint {
    color: white;
    font-size: 0.85em;
    margin-left: 10px;
}

.side-title {
    flex: none;
    min-width: 175px;
}

.middle-column {
    flex: none;
    min-width: 0;
    width: 330px;
}

.end-column {
    min-width: 150px;
}

.autocomplete ::v-deep .dropdown-content {
    width: fit-content;
}

@media(max-width: 873px) {
    .visit-tracker {
        display: none;
    }

    .reverse-row-order {
        flex-direction: column-reverse;
        display: flex;
    }
}
</style>
