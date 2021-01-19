<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <section class="section">
        <div class="container">
            <h1 class="title">Expression</h1>

            <div class="columns">
                <div class="column is-one-fifth">
                    <p class="title is-6">1. Select platform</p>
                    <div>
                        <b-radio v-model="platform" :disabled="!platform" native-value="microarray">Microarray</b-radio>
                    </div>
                    <div>
                        <b-radio v-model="platform" :disabled="!platform" native-value="rnaseq">RNA-seq</b-radio>
                    </div>
                </div>

                <div class="column is-one-fifth">
                    <p class="title is-6">2. Select species</p>
                    <div>
                        <b-radio v-model="species" native-value="human">Human</b-radio>
                    </div>
                    <div>
                        <b-radio v-model="species" native-value="mouse">Mouse</b-radio>
                    </div>
                </div>
                <div class="column">
                    <p class="title is-6">3. Select datasets</p>

                    <div>
                        <div v-if="species === 'mouse'">
                            <div class="content">
                                <b-switch
                                    v-model="isSwitchedMouse"
                                >
                                </b-switch>
                            </div>
                            <b-checkbox v-model="selectedOptions.mouse" v-for="item in availableData['mouse'].options" :native-value="item">{{ item }}</b-checkbox>
                        </div>

                        <template v-else>
                            <div v-if="platform === 'microarray'">
                                <div class="content">
                                    <b-switch
                                        v-model="isSwitchedMicro"
                                    >
                                    </b-switch>
                                </div>
                                <div class="content">
                                    <p class="title is-6">Normal tissue</p>
                                    <b-checkbox v-model="selectedOptions.microarray_tissue" v-for="item in availableData['microarray_tissue'].options" :native-value="item">{{ item }}</b-checkbox>
                                </div>

                                <div class="content">
                                    <p class="title is-6">Disease</p>
                                    <b-checkbox v-model="selectedOptions.microarray_disease" v-for="item in availableData['microarray_disease'].options" :native-value="item">{{ item }}</b-checkbox>
                                </div>
                            </div>

                            <div v-else>
                                <div class="content">
                                    <b-switch
                                        v-model="isSwitchedRNA"
                                    >
                                    </b-switch>
                                </div>
                                <div class="content">
                                    <h1>Normal tissue</h1>
                                    <b-checkbox v-model="selectedOptions.rnaseq_tissue" v-for="item in availableData['rnaseq_tissue'].options" :native-value="item">{{ item }}</b-checkbox>
                                </div>

                                <div class="content">
                                    <h1>Disease</h1>
                                    <b-checkbox v-model="selectedOptions.rnaseq_disease" v-for="item in availableData['rnaseq_disease'].options" :native-value="item">{{ item }}</b-checkbox>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>

                <div class="column">
                    <p class="title is-6">4. Enter Gene Symbol or Ensembl ID</p>
                    <div class="content">
                        <p class="subtitle is-6">Limited to 50 entries</p>
                        <p class="subtitle is-6"><u style="cursor: pointer" @click="defaultExample">A search example</u></p>
                        <b-field>
                            <b-input type="textarea" v-model="geneList"></b-input>
                        </b-field>
                        <b-button @click="heatMap" type="is-info">Submit</b-button>
                    </div>
                </div>
            </div>

            <hr>
            <div>
                <div class="columns">
                    <div class="column is-5">
                        <div class="content">
                            <b-button v-on:click="exportCsv()" v-if="heatMapData !== null">Download CSV</b-button>
                        </div>
                        <ag-grid-vue
                            :groupSelectsChildren="true"
                            :groupUseEntireRow="true"
                            :columnDefs="heatMapDataColumnDefs"
                            :rowData="heatMapData"
                            :rowDragManaged="true"
                            class="ag-theme-balham"
                            rowSelection="multiple"
                            overlayNoRowsTemplate="<span>No available data</span>"
                            :gridOptions="gridOptions"
                            :style="{width: '100%', height: '500px', visibility: !!heatMapData ? 'visible' : 'hidden'}">
                        </ag-grid-vue>
                    </div>
                    <div class="column is-offset-1">
                        <figure class="image">
                            <img :src="heatmapImageDataUrl" style="max-width: 100%; max-height: 700px">
                        </figure>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    import {AgGridVue} from "ag-grid-vue";
    import {getExpressionDatasets, getHeatMapData} from "../api/server";

    export default {
        components: {
            AgGridVue,
        },

        data() {
            return {
                availableData: {
                    microarray_tissue: [],
                    microarray_disease: [],
                    rnaseq_tissue: [],
                    rnaseq_disease: [],
                    mouse: [],
                },
                platform: undefined,
                species: undefined,
                geneList: '',

                isSwitchedMouse: undefined,
                isSwitchedMicro: undefined,
                isSwitchedRNA: undefined,

                selectedOptions: {
                    microarray_tissue: [],
                    microarray_disease: [],
                    rnaseq_tissue: [],
                    rnaseq_disease: [],
                    mouse: [],
                },

                heatMapData: null,
                heatMapDataColumnDefs: [],
                heatmapImageDataUrl: undefined,
                gridOptions: {},
            }
        },

        watch: {
            species(val) {
                if (val === 'mouse') {
                    this.platform = undefined;
                } else {
                    if (!this.platform) {
                        this.platform = 'microarray';
                    }
                }
            },
            isSwitchedMouse(val) {
                console.log("#######", val)
                if (val) {
                    this.selectedOptions.mouse = this.availableData['mouse'].options
                } else {
                    this.selectedOptions.mouse = []
                }
            },
            isSwitchedMicro(val) {
                if (val) {
                    this.selectedOptions.microarray_tissue = this.availableData['microarray_tissue'].options
                    this.selectedOptions.microarray_disease = this.availableData['microarray_disease'].options
                } else {
                    this.selectedOptions.microarray_tissue = []
                    this.selectedOptions.microarray_disease = []
                }
            },
            isSwitchedRNA(val) {
                if (val) {
                    this.selectedOptions.rnaseq_tissue = this.availableData['rnaseq_tissue'].options
                    this.selectedOptions.rnaseq_disease = this.availableData['rnaseq_disease'].options
                } else {
                    this.selectedOptions.rnaseq_tissue = []
                    this.selectedOptions.rnaseq_disease = []
                }
            }
        },

        created() {
            getExpressionDatasets().then(res => {
                const result = {}
                for (let item of res.data) {
                    result[item.key] = item
                }
                this.availableData = result;
                this.setOptionsFromUrl();
            });
        },

        methods: {
            defaultExample() {
                if (this.species === 'mouse') {
                    this.geneList = this.availableData.mouse.example;
                } else if (this.platform === 'microarray') {
                    this.geneList = this.availableData.microarray_tissue.example;
                } else {
                    this.geneList = this.availableData.rnaseq_tissue.example;
                }
            },

            setOptionsFromUrl() {
                const disease = this.$route.query.name;
                const species = this.$route.query.species;

                if (species) {
                    if (species === 'mouse') {
                        this.species = 'mouse'
                        this.selectedOptions.mouse = this.availableData['mouse'].options;
                    } else {
                        this.species = 'human'
                        this.selectedOptions.microarray_tissue = this.availableData['microarray_tissue'].options;
                        this.selectedOptions.microarray_disease = this.availableData['microarray_disease'].options;
                    }
                } else if (disease) {
                    this.species = 'human';
                    if (this.availableData['microarray_disease'].options.includes(disease)) {
                        this.platform = 'microarray';
                        this.selectedOptions.microarray_disease = [disease];
                    } else if (this.availableData['rnaseq_disease'].options.includes(disease)) {
                        this.platform = 'rnaseq';
                        this.selectedOptions.rnaseq_disease = [disease];
                    }
                } else {
                    this.species = 'human';
                }
            },

            exportCsv() {
                this.gridOptions.api.exportDataAsCsv();
            },

            heatMap() {
                if (!this.geneList) {
                    this.$buefy.notification.open('No genes provided')
                } else {
                    const params = {
                        type: this.species,
                        platform: this.platform,
                        gene: this.geneList,
                    };

                    if (this.species === 'mouse') {
                        params.tissue = this.selectedOptions.mouse.toString();
                    } else if (this.platform === 'microarray') {
                        params.tissue = this.selectedOptions.microarray_tissue.toString();
                        params.disease = this.selectedOptions.microarray_disease.toString();
                    } else {
                        params.tissue = this.selectedOptions.rnaseq_tissue.toString();
                        params.disease = this.selectedOptions.rnaseq_disease.toString();
                    }

                    getHeatMapData(params).then((res) => {
                        this.heatMapDataColumnDefs = res.columns.map(x => {
                            return {headerName: x, field: x}
                        });
                        this.heatMapData = res.data;
                        this.heatmapImageDataUrl = res.fig;
                    });
                }
            },
        },
    }
</script>

<style scoped>

</style>
