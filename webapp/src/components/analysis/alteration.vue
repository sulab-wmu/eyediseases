<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <div>
        <div class="columns">
            <div class="column is-6">
                <p class="title is-5">Mean ATAC-Seq signal over AMD-associated genes</p>
                <ag-grid-vue :columnDefs="columnDefs1"
                             :rowData="data1"
                             :defaultColDef="defaultColDef"
                             :style="tableStyle"
                             overlayNoRowsTemplate="<span>No available data</span>"
                             :gridOptions="gridOptions"
                             class="table ag-theme-balham">
                </ag-grid-vue>
                <div class="content" style="text-align: right">
                    <b-button v-on:click="exportCsv()" v-if="data1 !== null">Download CSV</b-button>
                </div>
            </div>
            <div class="column is-6 is-offset-1">
                <p class="title is-5">Denstiy plot of ATAC-seq signal on AMD associated gene</p>
                <img src="../../assets/alteration.jpg" style="height: 640px">
            </div>
        </div>
    </div>
</template>

<script>
    import {AgGridVue} from 'ag-grid-vue';
    import {getAlteration} from "../../api/server";

    export default {
        components: {AgGridVue},
        data() {
            return {
                columnDefs1: [
                    {headerName: 'Symbol', field: 'gene', sortable: true},
                    {headerName: 'Normal Retina', field: 'normal_retina', sortable: true},
                    {headerName: 'AMD Retina', field: 'amd_retina', sortable: true},
                    {headerName: 'Normal RPE', field: 'normal_rpe', sortable: true},
                    {headerName: 'AMD RPE', field: 'amd_rpe', sortable: true},
                ],
                data1: [],
                defaultColDef: {flex: 1, resizable: true,},
                tableStyle: {
                    width: '100%',
                    height: '640px'
                },
                gridOptions: {},
            }
        },
        created() {
            getAlteration().then((res) => {
                this.data1 = res.data;
            })
        },
        methods: {
            exportCsv() {
                this.gridOptions.api.exportDataAsCsv();
            },
        }
    }
</script>

<style scoped>

</style>
