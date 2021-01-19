<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <div>
        <div class="columns">
            <div class="column is-4">
                <div class="content">
                    <p class="title is-6">Gene Query</p>
                    <b-field>
                        <b-input v-model="form.gene"></b-input>
                    </b-field>
                    <b-button @click="submit" type="is-info">Submit</b-button>
                </div>
            </div>

            <div class="column is-3">
                <div class="content">
                    <p class="title is-6">Select group</p>
                    <div class="content">
                        <p class="title is-6">Normal tissue</p>
                        <b-checkbox v-model="selectedOptions.microarray_tissue" v-for="item in availableData['microarray_tissue']" :native-value="item" @change.native="PlayTissue">{{
                                item
                            }}
                        </b-checkbox>
                    </div>

                    <div class="content">
                        <p class="title is-6">Disease</p>
                        <b-checkbox v-model="selectedOptions.microarray_disease" v-for="item in availableData['microarray_disease']" :native-value="item" @change.native="PlayDisease">{{
                                item
                            }}
                        </b-checkbox>
                    </div>
                </div>
            </div>

            <div class="column">
                <div class="content">
                    <p class="title is-6">Limit by</p>
                    <b-field>
                        <b-checkbox v-model="two" native-value="A" class="is-expanded">Threshold (Correlation > 0.75 or -0.75)</b-checkbox>
                        <b-input v-model="form.ThresholdThreshold" type="number" min="-1" max="1" step=".01"></b-input>
                    </b-field>

                    <b-field>
                        <b-checkbox v-model="two" native-value="B" class="is-expanded">Number of the most correlated genes</b-checkbox>
                        <b-input v-model="form.Threshold_numbwe" type="number" min="1" max="500"></b-input>
                    </b-field>
                </div>
            </div>
        </div>

        <hr>
        <div class="content">Gene correlation</div>
        <ag-grid-vue :columnDefs="columnDefs1"
                     :rowData="data1"
                     :defaultColDef="defaultColDef"
                     :style="tableStyle"
                     overlayNoRowsTemplate="<span>No available data</span>"
                     :gridOptions="gridOptions"
                     class="table ag-theme-balham">
        </ag-grid-vue>
        <div class="columns">
            <div class="column is-offset-10" style="text-align: right">
                <b-button v-on:click="exportCsv()" v-if="data1 !== null">Download CSV</b-button>
            </div>
        </div>

        <hr>
        <div class="content">Gene modules</div>
        <ag-grid-vue :columnDefs="columnDefs2"
                     :rowData="data2"
                     :defaultColDef="defaultColDef"
                     :style="tableStyle"
                     overlayNoRowsTemplate="<span>No available data</span>"
                     :gridOptions="gridOptions1"
                     class="table ag-theme-balham">
        </ag-grid-vue>
        <div class="columns">
            <div class="column is-offset-10" style="text-align: right">
                <b-button v-on:click="exportCsv1()" v-if="data2 !== null">Download CSV</b-button>
            </div>
        </div>
    </div>
</template>

<script>
    import {AgGridVue} from 'ag-grid-vue';
    import {getDiseaseCo} from "../../api/server";

    export default {
        components: {AgGridVue},
        data() {
            return {
                availableData: {
                    microarray_tissue: ['Retina', 'Corneal', 'RPE_macula', 'Retina_macula', 'RPE_non_macula', 'Retina_non_macula', 'Corneal_endothelial_cells'],
                    microarray_disease: ['Keratoconus', 'Retinoblastoma', 'Age-Related-Macular-Degeneration'],
                },
                selectedOptions: {
                    microarray_tissue: ['Retina'],
                    microarray_disease: [],
                },
                tableStyle: {
                    width: '100%',
                    height: '400px'
                },
                defaultColDef: {flex: 1, resizable: true,},

                columnDefs1: [{headerName: 'Query', field: 'gene', sortable: true},
                    {headerName: 'Target', field: 'contrast_gene', sortable: true},
                    {headerName: 'Correlation score', field: 'weight', sortable: true},],

                columnDefs2: [{headerName: 'Symbol', field: 'gene', sortable: true},
                    {headerName: 'Module', field: 'module', sortable: true},
                    {headerName: 'KME', field: 'kme', sortable: true},],

                rowData: [],
                n: 10,
                radioStyle: {
                    display: 'block',
                    height: '30px',
                    lineHeight: '30px',
                },
                form: {
                    gene: 'ACE2,SLC6A20,FYCO1,SEMA3F,CARD11,LOXL2',
                    ThresholdThreshold: '0.1',
                    Threshold_numbwe: '50'
                },
                two: ['B'],
                data1: [],
                data2: [],

                gridOptions: {},
                gridOptions1: {},
            }
        },
        created() {
            let obj = {
                gene: this.form.gene,
                species: this.selectedOptions
            };
            if (this.two.indexOf('A') > -1) {
                obj.ThresholdThreshold = this.form.ThresholdThreshold
            }
            if (this.two.indexOf('B') > -1) {
                obj.Threshold_numbwe = this.form.Threshold_numbwe
            }

            if (obj.gene && obj.species) {
                getDiseaseCo(obj).then((res) => {
                    this.data1 = res.data.data1;
                    this.data2 = res.data.data2;
                })

            } else {
                this.$message.error('Incorrect parameters')
            }
        },
        methods: {
            submit() {
                let obj = {
                    gene: this.form.gene,
                    species: this.selectedOptions
                };
                if (this.two.indexOf('A') > -1) {
                    obj.ThresholdThreshold = this.form.ThresholdThreshold
                }
                if (this.two.indexOf('B') > -1) {
                    obj.Threshold_numbwe = this.form.Threshold_numbwe
                }

                if (obj.gene && obj.species) {
                    getDiseaseCo(obj).then((res) => {
                        this.data1 = res.data.data1;
                        this.data2 = res.data.data2;
                    })

                } else {
                    this.$message.error('Incorrect parameters')
                }
            },
            exportCsv() {
                this.gridOptions.api.exportDataAsCsv();
            },
            exportCsv1() {
                this.gridOptions1.api.exportDataAsCsv();
            },
            PlayTissue(e) {
                if (e.target.checked) {
                    this.selectedOptions.microarray_tissue = [e.target.value];
                    this.selectedOptions.microarray_disease = []
                } else {
                    this.selectedOptions.microarray_tissue = [];
                    this.selectedOptions.microarray_disease = []
                }
            },
            PlayDisease(e) {
                if (e.target.checked) {
                    this.selectedOptions.microarray_tissue = [];
                    this.selectedOptions.microarray_disease = [e.target.value]
                } else {
                    this.selectedOptions.microarray_tissue = [];
                    this.selectedOptions.microarray_disease = []
                }
            }

        }
    }
</script>

<style scoped>

</style>
