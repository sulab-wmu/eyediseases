<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <section class="section">
        <div class="container">
            <h1 class="title">Single-cell RNAseq</h1>
            <div class="columns">
                <div class="column is-one-quarter">
                    <div class="content">
                        <h5 class="title is-5">Select Datasets</h5>
                        <b-dropdown v-model="singleCellName" aria-role="list" style="width: 100%">
                            <button class="button" slot="trigger" slot-scope="{ active }">
                                <span>{{ singleCellName }}</span>
                                <b-icon :icon="active ? 'angle-up' : 'angle-down'"></b-icon>
                            </button>
                            <b-dropdown-item value="Fetal eye" aria-role="listitem">
                                Fetal eye
                            </b-dropdown-item>
                            <b-dropdown-item value="Fetal Retina and RPE" aria-role="listitem">
                                Fetal Retina and RPE
                            </b-dropdown-item>
                            <b-dropdown-item value="Adult Retina1" aria-role="listitem">
                                Adult Retina1
                            </b-dropdown-item>
                            <b-dropdown-item value="Adult Retina2" aria-role="listitem">
                                Adult Retina2
                            </b-dropdown-item>
                            <b-dropdown-item value="Uveal melanoma" aria-role="listitem">
                                Uveal melanoma
                            </b-dropdown-item>
                            <b-dropdown-item value="AMD RPE" aria-role="listitem">
                                AMD RPE
                            </b-dropdown-item>
                        </b-dropdown>
                    </div>

                    <div class="content">
                        <h5 class="title is-5">Select Clusters</h5>
                        <div class="content">
                            <b-switch
                                v-model="isSwitched"
                            >
                            </b-switch>
                        </div>
                        <div style="border:1px solid #ccc; overflow:auto; padding: 5px;">
                            <div v-for="item in plainOptions">
                                <b-checkbox v-model="checkedList" :native-value="item" class="cluster-list">{{ item }}</b-checkbox>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column is-8">
                    <div class="content">
                        <h4 class="title is-4 has-text-centered">t-SNE map for {{ singleCellName }}</h4>
                        <vue-plotly :data="data" :layout="layout" :options="options" :autoresize="true"/>
                    </div>

                    <h4 class="title is-4 has-text-centered">Top markers for each subpopulation</h4>
                    <div class="content">
                        <template>
                            <ag-grid-vue
                                :animateRows="true"
                                :columnDefs="columnDefs"
                                :groupSelectsChildren="true"
                                :groupUseEntireRow="true"
                                :defaultColDef={resizable:true}
                                :rowData="rowData"
                                :rowDragManaged="true"
                                class="ag-theme-alpine"
                                rowSelection="multiple"
                                :pagination="true"
                                :gridOptions="gridOptions"
                                style="width: 100%; height: 450px;"
                            >
                                <ag-grid-column :menuTabs="['filterMenuTab']" :width="300" cellRendererFramework="name" field="name" headerName="123"
                                                slot="name"
                                                suppressSorting>
                                </ag-grid-column>
                            </ag-grid-vue>
                        </template>
                    </div>
                    <div class="columns">
                        <div class="column is-offset-10">
                            <b-button v-on:click="exportCsv()" v-if="rowData !== null">Download CSV</b-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    import VuePlotly from '@statnett/vue-plotly'
    import {getSingeleCellGridData, getSingleCell, getSingleCellList} from "../api/server";
    import {AgGridVue} from "ag-grid-vue";

    export default {
        components: {
            AgGridVue,
            VuePlotly,
        },
        data() {
            return {
                columnDefs: [
                    {headerName: 'Cluster', field: 'cluster', sortable: true, filter: true, rowDrag: true},
                    {headerName: 'Annotation', field: 'annotation', sortable: true, filter: true},
                    {headerName: 'gene', field: 'gene', sortable: true, filter: true},
                    {headerName: 'p_val', field: 'p_val', sortable: true, filter: true},
                    {headerName: 'avg_logFC', field: 'avg_logFC', sortable: true, filter: true},
                    {headerName: 'pct.1', field: 'pct1', sortable: true, filter: true},
                    {headerName: 'pct.2', field: 'pct2', sortable: true, filter: true},

                ],
                rowData: [],
                singleCellName: "Fetal Retina and RPE",
                checkedList: [],
                indeterminate: true,
                checkAll: false,

                isSwitched: true,
                gridOptions: {},

                plainOptions: [],
                data: [
                    {
                        x: [],
                        y: [],
                        mode: 'markers',
                        type: 'scatter',
                        transforms: [
                            {
                                type: 'groupby',
                                groups: [],
                            }
                        ]
                    },

                ],
                layout: {
                    xaxis: {
                        autorange: false,
                        range: [-50, 50],
                        zeroline: false,
                        fixedrange: true,
                    },
                    yaxis: {
                        autorange: false,
                        range: [-50, 50],
                        // position: 0.5,
                        zeroline: false,
                        fixedrange: true
                    },
                    margin: {
                        t: 50
                    },
                },
                options: {responsive: true},
            }
        },
        watch: {
            singleCellName: {
                handler(val) {
                    this.getList(val);
                    this.getGridData(val)
                },
                deep: true,
                immediate: true,
            },

            checkedList(val) {
                let checkedData = val.toString();
                let obj = {
                    name: this.singleCellName,
                    cluster: checkedData
                }
                if (this.checkedList.length === 0) {
                    this.$message.error('datasets list is None')
                } else {
                    getSingleCell(obj).then(res => {
                        this.data[0]['x'] = res.x;
                        this.data[0]['y'] = res.y;
                        this.data[0]['transforms'][0]['groups'] = res.group
                        this.layout.xaxis.range = res.x_range
                        this.layout.yaxis.range = res.y_range
                    })
                }
            },
            isSwitched(val) {
                if (val) {
                    this.checkedList = this.plainOptions
                } else {
                    this.checkedList = []
                }
            },
        },
        methods: {
            onChange(checkedList) {
                this.indeterminate = !!checkedList.length && checkedList.length < this.plainOptions.length;
                this.checkAll = checkedList.length === this.plainOptions.length;
            },
            onCheckAllChange(e) {
                Object.assign(this, {
                    checkedList: e.target.checked ? this.plainOptions : [],
                    indeterminate: false,
                    checkAll: e.target.checked,
                });
            },
            getList(val) {
                getSingleCellList(val).then(res => {
                    this.plainOptions = res.data
                    this.checkedList = res.data
                })
            },
            getGridData(val) {
                let obj = {
                    name: val
                };
                getSingeleCellGridData(obj).then(res => {
                    this.rowData = res.data;
                    this.total = res.pagination.total
                })
            },
            exportCsv() {
                this.gridOptions.api.exportDataAsCsv();
            }
        }
    }
</script>

<style scoped>
.cluster-list {
    font-size: 0.9rem;
}
</style>
