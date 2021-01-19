<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <div>
        <div class="columns">
            <div class="column is-4">
                <div class="content">
                    <p class="title is-6">Multi-Gene Query</p>
                    <b-field>
                        <b-input v-model="form.gene"></b-input>
                    </b-field>
                    <b-button @click="submit" type="is-info">Submit</b-button>
                </div>
            </div>

            <div class="column is-3">
                <div class="content">
                    <p class="title is-6">Select group</p>
                    <b-field>
                        <b-radio-button v-model="form.species" native-value="disease">
                            <span>Disease</span>
                        </b-radio-button>

                        <b-radio-button v-model="form.species" native-value="tissue">
                            <span>Tissue</span>
                        </b-radio-button>
                    </b-field>
                </div>
            </div>

            <div class="column">
                <div class="content">
                    <p class="title is-6">Limit by</p>
                    <b-field>
                        <b-checkbox v-model="two" native-value="A" class="is-expanded">Threshold (Correlation > 0.75 or -0.75)</b-checkbox>
                        <b-input v-model="form.ThresholdThreshold" type="number" min="-1" max="1" step=".01"></b-input>
                    </b-field>

                    <!--                    <b-field>-->
                    <!--                        <b-checkbox v-model="two" native-value="B" class="is-expanded">Correlated genes</b-checkbox>-->
                    <!--                        <b-input v-model="form.Threshold_numbwe" type="number" min="1" max="100"></b-input>-->
                    <!--                    </b-field>-->
                </div>
            </div>
        </div>

        <hr>
        <div class="content">The correlation between the gene and the trait</div>
        <ag-grid-vue :columnDefs="columnDefs2"
                     :rowData="data2"
                     :defaultColDef="defaultColDef"
                     :style="tableStyle"
                     overlayNoRowsTemplate="<span>No available data</span>"
                     :gridOptions="gridOptions"
                     class="table ag-theme-balham">
        </ag-grid-vue>
        <div class="columns">
            <div class="column is-offset-10" style="text-align: right">
                <b-button v-on:click="exportCsv()" v-if="data2 !== null">Download CSV</b-button>
            </div>
        </div>
    </div>
</template>

<script>
    import {AgGridVue} from 'ag-grid-vue';
    import {getSignificance} from "../../api/server";

    export default {
        components: {AgGridVue},
        data() {
            return {
                tableStyle: {
                    width: '100%',
                    height: '400px'
                },
                defaultColDef: {flex: 1, resizable: true,},
                columnDefs1: [{headerName: 'Query', field: 'gene', sortable: true},
                    {headerName: 'Target', field: 'contrast_gene', sortable: true},
                    {headerName: 'Correlation score', field: 'weight', sortable: true},],

                columnDefs2: [],
                columnDefs3: [],
                rowData: [],
                n: 10,
                radioStyle: {
                    display: 'block',
                    height: '30px',
                    lineHeight: '30px',
                },
                form: {
                    gene: 'ACE2,SLC6A20,LZTFL1,CCR9,FYCO1,CXCR6,XCR1',
                    species: 'disease',
                    ThresholdThreshold: '0.1',
                    // Threshold_numbwe: '10'
                },
                two: [],
                data1: [],
                data2: [],
                data3: [],

                gridOptions: {},
            }
        },
        created() {
            let obj = {
                gene: this.form.gene,
                species: this.form.species
            };
            if (this.two.indexOf('A') > -1) {
                obj.ThresholdThreshold = this.form.ThresholdThreshold
            }
            // if (this.two.indexOf('B') > -1) {
            //     obj.Threshold_numbwe = this.form.Threshold_numbwe
            // }

            if (obj.gene && obj.species) {
                getSignificance(obj).then((res) => {
                    if (this.form.species === 'disease') {
                        this.columnDefs2 = [
                            {headerName: 'Gene', field: 'gene', sortable: true},
                            {headerName: 'Age-related macular degeneration', field: 'amd', sortable: true},
                            {headerName: 'Diabetic retinopathy', field: 'dr', sortable: true},
                            {headerName: 'Keratoconus', field: 'kc', sortable: true},
                            {headerName: 'Primary open-angle glaucoma', field: 'glc', sortable: true},
                            {headerName: 'Retinitis pigmentosa', field: 'rp', sortable: true},
                            {headerName: 'Retinoblastoma', field: 'rb', sortable: true},
                        ]
                    } else {
                        this.columnDefs2 = [
                            {headerName: 'Gene', field: 'gene_symbol', sortable: true},
                            {headerName: 'corneas', field: 'corneas', sortable: true},
                            {headerName: 'corneal_endothelial_cells', field: 'corneal_endothelial_cells', sortable: true},
                            {headerName: 'retina', field: 'retina', sortable: true},
                            {headerName: 'retina_macula', field: 'retina_macula', sortable: true},
                            {headerName: 'retina_non_macula', field: 'retina_non_macula', sortable: true},
                            {headerName: 'rpe_macula', field: 'rpe_macula', sortable: true},
                            {headerName: 'rpe_non_macula', field: 'rpe_non_macula', sortable: true},
                            {headerName: 'retinal_endothelial_cells', field: 'retinal_endothelial_cells', sortable: true},
                            {headerName: 'ipsc_derived_retinal_organoids', field: 'ipsc_derived_retinal_organoids', sortable: true},
                            {headerName: 'trabecular_meshwork_cells', field: 'trabecular_meshwork_cells', sortable: true},
                        ]
                    }
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
                    species: this.form.species
                };
                if (this.two.indexOf('A') > -1) {
                    obj.ThresholdThreshold = this.form.ThresholdThreshold
                }
                // if (this.two.indexOf('B') > -1) {
                //     obj.Threshold_numbwe = this.form.Threshold_numbwe
                // }

                if (obj.gene && obj.species) {
                    getSignificance(obj).then((res) => {
                        this.data1 = res.data.data1;
                        if (this.form.species === 'disease') {
                            this.columnDefs2 = [
                                {headerName: 'Gene', field: 'gene', sortable: true},
                                {headerName: 'Age-related macular degeneration', field: 'amd', sortable: true},
                                {headerName: 'Diabetic retinopathy', field: 'dr', sortable: true},
                                {headerName: 'Keratoconus', field: 'kc', sortable: true},
                                {headerName: 'Primary open-angle glaucoma', field: 'glc', sortable: true},
                                {headerName: 'Retinitis pigmentosa', field: 'rp', sortable: true},
                                {headerName: 'Retinoblastoma', field: 'rb', sortable: true},
                            ];
                            this.columnDefs3 = [
                                {headerName: 'Gene', field: 'gene'},
                                {headerName: 'Ensembl ID', field: 'ensembl_id'},
                                {headerName: 'Age-related macular degeneration', field: 'age_related_macular_degeneration'},
                                {headerName: 'Diabetic retinopathy', field: 'diabetic_retinopathy'},
                                {headerName: 'Keratoconus', field: 'keratoconus'},
                                {headerName: 'Primary open-angle glaucoma', field: 'primary_open_angle_glaucoma'},
                                {headerName: 'Retinitis pigmentosa', field: 'retinitis_pigmentosa'},
                                {headerName: 'Retinoblastoma', field: 'retinoblastoma'},
                            ]
                        } else {
                            this.columnDefs2 = [
                                {headerName: 'Gene', field: 'gene_symbol', sortable: true},
                                {headerName: 'corneas', field: 'corneas', sortable: true},
                                {headerName: 'corneal_endothelial_cells', field: 'corneal_endothelial_cells', sortable: true},
                                {headerName: 'retina', field: 'retina', sortable: true},
                                {headerName: 'retina_macula', field: 'retina_macula', sortable: true},
                                {headerName: 'retina_non_macula', field: 'retina_non_macula', sortable: true},
                                {headerName: 'rpe_macula', field: 'rpe_macula', sortable: true},
                                {headerName: 'rpe_non_macula', field: 'rpe_non_macula', sortable: true},
                                {headerName: 'retinal_endothelial_cells', field: 'retinal_endothelial_cells', sortable: true},
                                {headerName: 'ipsc_derived_retinal_organoids', field: 'ipsc_derived_retinal_organoids', sortable: true},
                                {headerName: 'trabecular_meshwork_cells', field: 'trabecular_meshwork_cells', sortable: true},
                            ];
                            this.columnDefs3 = [
                                {headerName: 'Gene', field: 'gene'},
                                {headerName: 'Ensembl ID', field: 'ensembl_id'},
                                {headerName: 'Corneas', field: 'corneas'},
                                {headerName: 'Corneal endothelial cells', field: 'corneal_endothelial_cells'},
                                {headerName: 'Retina', field: 'retina'},
                                {headerName: 'Retina macula', field: 'retina_macula'},
                                {headerName: 'Retina non-macula', field: 'retina_non_macula'},
                                {headerName: 'RPE macula', field: 'rpe_macula'},
                                {headerName: 'RPE non-macula', field: 'rpe_non_macula'},
                                {headerName: 'Retinal endothelial cells', field: 'retinal_endothelial_cells'},
                                {headerName: 'iPSC-derived retinal organoids', field: 'ipsc_derived_retinal_organoids'},
                                {headerName: 'Trabecular meshwork cells', field: 'trabecular_meshwork_cells'},
                            ]
                        }
                        this.data2 = res.data.data2;
                        this.data3 = res.data.data3;
                    })

                } else {
                    this.$message.error('Incorrect parameters')
                }
            },
            exportCsv() {
                this.gridOptions.api.exportDataAsCsv();
            }
        }
    }
</script>

<style scoped>

</style>
