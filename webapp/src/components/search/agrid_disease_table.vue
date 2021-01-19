<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <ag-grid-vue
        :columnDefs="columnDefs"
        :defaultColDef="defaultColDef"
        :groupSelectsChildren="true"
        :groupUseEntireRow="true"
        :rowData="rowData"
        :rowDragManaged="true"
        overlayNoRowsTemplate="<span>No available data</span>"
        class="ag-theme-alpine"
        rowSelection="multiple"
        :pagination="true"
        style="width:100%; height: 375px;"
    >
        <ag-grid-column :menuTabs="['filterMenuTab']" :width="300" cellRendererFramework="name" field="name" headerName="123"
                        slot="name"
                        suppressSorting>
        </ag-grid-column>
    </ag-grid-vue>
</template>

<script>
    import {AgGridVue} from "ag-grid-vue";

    let SquareComponent = {
        template: '<a :href="getVariantList()">{{ this.params.data.variants }}</a>',
        methods: {
            getVariantList() {
                // console.log(this.params.data)
                return '/variants?name=' + this.params.data.variants
            }
        }
    };

    let GeneComponent = {
        template: '<a :href="getGeneView()">{{ this.params.data.symbol }}</a>',
        methods: {
            getGeneView() {
                // console.log(this.params.data)
                return '/gene?name=' + this.params.data.symbol
            }
        }
    };

    let MiMComponent = {
        template: '<span>{{getNewPhenotype()}}</span>',
        methods: {
            getNewPhenotype() {
                // console.log(this.params.data)
                if (this.params.data.phenotype) {
                    const arr = this.params.data.phenotype.split(';')
                    return arr[1] + ';' + arr[0]
                } else {
                    return this.params.data.phenotype
                }
            }
        }
    };

    let PubComponent = {
        template: '<a :href="params.data.pubmed" target="_blank">{{ getPubmedList() }}</a>',
        methods: {
            getPubmedList() {
                // console.log(this.params.data)
                let rs = this.params.data.pubmed.split('/')
                // console.log(rs)
                return rs[rs.length - 1]
            }
        }
    };

    export default {
        props: ['type', 'data'],
        data() {
            return {
                pages: null,
                columnDefs: [],
                rowData: [],
                defaultColDef: {
                    resizable: true,
                }
            }
        },
        watch: {
            type: {
                handler(val) {
                    this.columnDefs = this.getColumn(val)
                },
                immediate: true,
                deep: true,
            },
            data: {
                handler(val) {
                    this.rowData = val
                },
                immediate: true,
                deep: true,
            }
        },
        components: {
            AgGridVue, SquareComponent, PubComponent, GeneComponent, MiMComponent
        },
        methods: {
            getColumn(st) {
                let str = st.toLowerCase()
                if (str === 'gwas') {

                    return [
                        // {headerName: 'Gene.ID', field: 'gene_id', sortable: true, filter: true, rowDrag: true},
                        {headerName: 'Gene Symbol', field: 'symbol', sortable: true, filter: true, cellRendererFramework: 'GeneComponent'},
                        {headerName: 'Band', field: 'band', sortable: true, filter: true},
                        {headerName: 'Variants', field: 'variants', sortable: true, filter: true, cellRendererFramework: 'SquareComponent'},
                        {headerName: 'Position(hg38)', field: 'position_hg38', sortable: true, filter: true},
                        {headerName: 'Major allele', field: 'major_allele', sortable: true, filter: true},
                        {headerName: 'Minor allele', field: 'minor_allele', sortable: true, filter: true},
                        {headerName: 'p-Value', field: 'p_value', sortable: true, filter: true},
                        {headerName: 'BETA', field: 'beta', sortable: true, filter: true},
                        {headerName: 'Context', field: 'context', sortable: true, filter: true},
                        {headerName: 'CADD', field: 'cadd', sortable: true, filter: true},
                        {headerName: 'INITIAL.SAMPLE.SIZE', field: 'initial', sortable: true, filter: true},
                        {headerName: 'REPLICATION.SAMPLE.SIZE', field: 'peplication', sortable: true, filter: true},
                        {headerName: 'Pubmed', field: 'pubmed', sortable: true, filter: true, cellRendererFramework: 'PubComponent'},
                        // {headerName: 'Disease', field: 'disease', sortable: true, filter: true},

                    ]
                } else if (str === 'omim') {
                    return [
                        // {headerName: 'Gene ID', field: 'gene_id', sortable: true, filter: true, rowDrag: true},
                        {headerName: 'Gene Symbol', field: 'symbol', sortable: true, filter: true, cellRendererFramework: 'GeneComponent'},
                        {headerName: 'Band', field: 'band', sortable: true, filter: true},
                        {headerName: 'Gene Name', field: 'name', sortable: true, filter: true},
                        {headerName: 'Variants', field: 'variants', sortable: true, filter: true, cellRendererFramework: 'SquareComponent'},
                        {headerName: 'EnsemblID', field: 'ensembl', sortable: true, filter: true},
                        {headerName: 'Gene MIM number', field: 'omim', sortable: true, filter: true,},
                        {headerName: 'Phenotype MIM number', field: 'phenotype', sortable: true, filter: true, cellRendererFramework: 'MiMComponent'},
                        {headerName: 'confidence', field: 'confidence', sortable: true, filter: true},
                        {headerName: 'pubmed', field: 'pubmed', sortable: true, filter: true, cellRendererFramework: 'PubComponent'},
                        // {headerName: 'Disease', field: 'disease', sortable: true, filter: true},
                    ]
                }
            }
        },
    }
</script>

<style scoped>

</style>
