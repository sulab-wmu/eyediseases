<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <div>
        <template>
            <ag-grid-vue
                :animateRows="true"
                :columnDefs="columnDefs"
                :groupSelectsChildren="true"
                :groupUseEntireRow="true"
                :rowData="rowData"
                :rowDragManaged="true"
                :autoHeight="true"
                @selection-changed="onSelectionChanged"
                class="ag-theme-alpine"
                rowSelection="single"
                overlayNoRowsTemplate="<span>No available data</span>"
                style="width:100%;height: 350px;">
            </ag-grid-vue>
        </template>
        <br/><br/>
    </div>
</template>

<script>
    import {AgGridVue} from "ag-grid-vue";

    export default {
        props: ['data'],
        data() {
            return {
                pages: null,
                columnDefs: [
                    {headerName: 'P', field: 'p_value', sortable: true},
                    {headerName: 'FINEMAP', field: 'beta', sortable: true},
                    {headerName: 'Trait', field: 'disease', sortable: true},
                ],
                rowData: []
            }
        },
        watch: {
            'data': {
                handler(val) {
                    this.rowData = val
                },
                deep: true,
                immediate: true
            },

        },
        components: {
            AgGridVue
        },
        methods: {
            onSelectionChanged(params) {
                console.log(params.api.getSelectedRows())
            }
        },
    }
</script>

<style scoped>

</style>
