<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <div>
        <b-field label="Select disease:">
            <b-select v-model="filterValue">
                <option
                    v-for="item in filterData"
                    :value="item.key"
                    :key="item.key">
                    {{ item.value }}
                </option>
            </b-select>
        </b-field>

        <b-collapse
            :open="true"
            class="card"
            animation="slide">
            <div
                slot="trigger"
                slot-scope="props"
                class="card-header"
                role="button">
                <p class="card-header-title">
                    Biological Process
                </p>
                <a class="card-header-icon">
                    <b-icon
                        :icon="props.open ? 'angle-down' : 'angle-up'">
                    </b-icon>
                </a>
            </div>
            <div class="card-content">
                <div class="content">
                    <ag-grid-vue :columnDefs="columnDefs_a"
                                 :defaultColDef="defaultColDef"
                                 :masterDetail="true"
                                 :rowData="rowData_a"
                                 :style="tableStyle"
                                 overlayNoRowsTemplate="<span>No available data</span>"
                                 :gridOptions="gridOptionsBiological"
                                 class="table ag-theme-balham">
                    </ag-grid-vue>
                </div>
                <div class="columns">
                    <div class="column is-offset-10" style="text-align: right">
                        <b-button v-on:click="exportCsvBiological()" v-if="rowData_a !== null">Download CSV</b-button>
                    </div>
                </div>
            </div>
        </b-collapse>

        <b-collapse
            :open="false"
            class="card"
            animation="slide">
            <div
                slot="trigger"
                slot-scope="props"
                class="card-header"
                role="button">
                <p class="card-header-title">
                    Cellular Component
                </p>
                <a class="card-header-icon">
                    <b-icon
                        :icon="props.open ? 'angle-down' : 'angle-up'">
                    </b-icon>
                </a>
            </div>
            <div class="card-content">
                <div class="content">
                    <ag-grid-vue :columnDefs="columnDefs_a"
                                 :defaultColDef="defaultColDef"
                                 :masterDetail="true"
                                 :rowData="rowData_b"
                                 :style="tableStyle"
                                 overlayNoRowsTemplate="<span>No available data</span>"
                                 :gridOptions="gridOptionsCellular"
                                 class="table ag-theme-balham">
                    </ag-grid-vue>
                </div>
                <div class="columns">
                    <div class="column is-offset-10" style="text-align: right">
                        <b-button v-on:click="exportCsvCellular()" v-if="rowData_b !== null">Download CSV</b-button>
                    </div>
                </div>
            </div>
        </b-collapse>

        <b-collapse
            :open="false"
            class="card"
            animation="slide">
            <div
                slot="trigger"
                slot-scope="props"
                class="card-header"
                role="button">
                <p class="card-header-title">
                    Molecular Function
                </p>
                <a class="card-header-icon">
                    <b-icon
                        :icon="props.open ? 'angle-down' : 'angle-up'">
                    </b-icon>
                </a>
            </div>
            <div class="card-content">
                <div class="content">
                    <ag-grid-vue :columnDefs="columnDefs_a"
                                 :defaultColDef="defaultColDef"
                                 :masterDetail="true"
                                 :rowData="rowData_c"
                                 :style="tableStyle"
                                 overlayNoRowsTemplate="<span>No available data</span>"
                                 :gridOptions="gridOptionsMolecular"
                                 class="table ag-theme-balham">
                    </ag-grid-vue>
                </div>
                <div class="columns">
                    <div class="column is-offset-10" style="text-align: right">
                        <b-button v-on:click="exportCsvMolecular()" v-if="rowData_c !== null">Download CSV</b-button>
                    </div>
                </div>
            </div>
        </b-collapse>

        <b-collapse
            :open="false"
            class="card"
            animation="slide">
            <div
                slot="trigger"
                slot-scope="props"
                class="card-header"
                role="button">
                <p class="card-header-title">
                    KEGG Pathway
                </p>
                <a class="card-header-icon">
                    <b-icon
                        :icon="props.open ? 'angle-down' : 'angle-up'">
                    </b-icon>
                </a>
            </div>
            <div class="card-content">
                <div class="content">
                    <ag-grid-vue
                        :columnDefs="columnDefs_a"
                        :defaultColDef="defaultColDef"
                        :masterDetail="true"
                        :rowData="rowData_d"
                        :style="tableStyle"
                        overlayNoRowsTemplate="<span>No available data</span>"
                        :gridOptions="gridOptionsKEGG"
                        class="table ag-theme-balham">
                    </ag-grid-vue>
                </div>
                <div class="columns">
                    <div class="column is-offset-10" style="text-align: right">
                        <b-button v-on:click="exportCsvKEGG()" v-if="rowData_d !== null">Download CSV</b-button>
                    </div>
                </div>
            </div>
        </b-collapse>

    </div>

</template>

<script>
    import {AgGridVue} from 'ag-grid-vue';
    import {getDiseaseGo} from "../../api/server";

    const filterData = [
        {key: 'AMD', value: 'Age-related macular degeneration'},
        {key: 'Corneal_astigmatism', value: 'Corneal Astigmatism'},
        {key: 'GLC', value: 'Glaucoma'},
        {key: 'Myopia', value: 'Myopia'},
        {key: 'Refractive_astigmatism', value: 'Refractive Astigmatism'},
        {key: 'Refractive_error', value: 'Refractive error'},
        {key: 'Cataract', value: 'Cataract'},
        {key: 'Diabetic_retinopathy', value: 'Diabetic retinopathy'},
        {key: 'Retinitis', value: 'Retinitis'},
    ]
    export default {
        components: {AgGridVue},
        data() {
            return {
                current: ['Gene-Disease Network'],
                filterValue: 'AMD',
                tableStyle: {
                    width: '100%',
                    height: '400px'
                },
                filterData: filterData,
                detailCellRendererParams: null,
                defaultColDef: {editable: false, resizable: true,},
                columnDefs_a: [{headerName: 'Term', field: 'term', sortable: true},
                    {headerName: 'Count', field: 'count', sortable: true, width: 200},
                    {headerName: '%', field: 'percent', sortable: true, width: 200},
                    {headerName: 'P Value', field: 'p_value', sortable: true, width: 200},
                    {headerName: 'Fold Enrichment', field: 'fold_enrichment', sortable: true, width: 200},
                    {headerName: 'FDR', field: 'fdr', sortable: true, width: 200},
                    {headerName: 'Genes', field: 'genes', cellRenderer: 'agGroupCellRenderer', width: 200},
                ],
                rowData_a: [],
                rowData_b: [],
                rowData_c: [],
                rowData_d: [],

                gridOptionsKEGG: {},
                gridOptionsMolecular: {},
                gridOptionsCellular: {},
                gridOptionsBiological: {},
            }
        },
        watch: {
            filterValue(val) {
                this.getGO(val)
            }
        },
        methods: {
            getGO(val) {
                getDiseaseGo(val).then((res) => {
                    this.rowData_a = res.go.bp
                    this.rowData_b = res.go.cc;
                    this.rowData_c = res.go.mf;
                    this.rowData_d = res.go.kegg;
                })
            },
            exportCsvKEGG() {
                this.gridOptionsKEGG.api.exportDataAsCsv();
            },
            exportCsvMolecular() {
                this.gridOptionsMolecular.api.exportDataAsCsv();
            },
            exportCsvCellular() {
                this.gridOptionsCellular.api.exportDataAsCsv();
            },
            exportCsvBiological() {
                this.gridOptionsBiological.api.exportDataAsCsv();
            }
        },
        created() {
            this.getGO(this.filterValue)
        },

    }
</script>

<style scoped>

</style>
