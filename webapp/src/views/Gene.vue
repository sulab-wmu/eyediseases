<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <section class="section">
        <div class="container">
            <div class="columns">
                <div class="column is-6">
                    <div class="content more-padding">
                        <h4 class="title is-4">Summary</h4>
                        <table class="custom-table">
                            <tr>
                                <th>Symbol</th>
                                <td>{{ gene_data.symbol }}</td>
                            </tr>
                            <tr>
                                <th>Name</th>
                                <td>{{ gene_data.name }}</td>
                            </tr>
                            <tr>
                                <th>Synonyms</th>
                                <td>{{ gene_data.synonyms }}</td>
                            </tr>
                            <tr>
                                <th>Type</th>
                                <td>{{ gene_data.gene_type }}</td>
                            </tr>
                            <tr>
                                <th>Location</th>
                                <td>
                                    {{ gene_data.location[0] }}
                                    <br>
                                    {{ gene_data.location[1] }}
                                </td>
                            </tr>
                            <tr>
                                <th>Strand</th>
                                <td>{{ gene_data.strand }}</td>
                            </tr>
                            <tr>
                                <th>Description</th>
                                <td>{{ gene_data.description }}</td>
                            </tr>
                        </table>
                    </div>

                    <div class="content more-padding">
                        <h4 class="title is-4">Disease and Phenotype</h4>
                        <table class="custom-table">
                            <tr>
                                <th>Disease</th>
                                <td>
                                    <b-taglist>
                                        <b-tag :key="item"
                                               style="cursor: pointer; background-color: #12545f; color: #fff"
                                               v-for="item in filteredEyeDiseases(gene_data.eye_disease)">
                                            <span @click="dumpDisease(item)">{{ item }}</span>
                                        </b-tag>
                                    </b-taglist>
                                </td>
                            </tr>
                            <tr>
                                <th>Phenotypes</th>
                                <td>
                                    <div class="content">
                                        <b-taglist>
                                            <b-tag :key="item.id" :style="{background: changeColor(item.color), color: 'white'}" v-for="item in gene_data.phenotypes">
                                                {{ item.name }}
                                            </b-tag>
                                        </b-taglist>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </div>
                </div>

                <div class="column is-6">
                    <div class="content more-padding">
                        <h4 class="title is-4">External References</h4>
                        <table class="custom-table">
                            <tr>
                                <th>OMIM MIM</th>
                                <td>
                                    <a :href="'https://omim.org/entry/'+Math.trunc(gene_data.omim)+'?search='+Math.trunc(gene_data.omim)" target="_blank">{{ Math.trunc(gene_data.omim) }}</a>
                                </td>
                            </tr>
                            <tr>
                                <th>Ensembl</th>
                                <td>
                                    <a :href="'https://www.ensembl.org/Homo_sapiens/Gene/Summary?db=core;g='+gene_data.ensembl" target="_blank">{{ gene_data.ensembl }}</a>
                                </td>
                            </tr>
                            <tr>
                                <th>ClinVar</th>
                                <td>
                                    <a :href="gene_data.clinvar" target="_blank">Look up variants for {{ gene_data.symbol }} in ClinVar</a>
                                </td>
                            </tr>
                            <tr>
                                <th>Decipher</th>
                                <td>
                                    <a :href="gene_data.decipher" target="_blank">Look up variants for {{ gene_data.symbol }} in Decipher</a>
                                </td>
                            </tr>
                            <tr>
                                <th>gnomAD</th>
                                <td>
                                    <a :href="gene_data.gnomad" target="_blank">Look up variants for {{ gene_data.gene }} in gnomAD</a>
                                </td>
                            </tr>
                            <tr>
                                <th>PanelApp</th>
                                <td>
                                    <a :href="gene_data.panelapp" target="_blank">Look up {{ gene_data.gene }} in PanelApp</a>
                                </td>
                            </tr>
                        </table>
                    </div>

                    <div class="content more-padding">
                        <h4 class="title is-4">Drug Targets</h4>
                        <ag-grid-vue
                            :columnDefs="columnDefs"
                            :rowData="rowData"
                            class="ag-theme-balham"
                            rowSelection="multiple"
                            :defaultColDef="defaultColDef"
                            overlayNoRowsTemplate="<span>No available data</span>"
                            style="width: 100%; height: 475px; margin: 0 auto;">
                        </ag-grid-vue>
                    </div>
                    <div class="content more-padding">
                        <h4 class="title is-4">Expression</h4>
                        <div id="violin-1-root"></div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    import {getGeneDetails, getGeneExpressionViolin} from "../api/server";
    import {render} from "../components/gtex-d3/EqtlViolinPlot"
    import {AgGridVue} from "ag-grid-vue";

    export default {
        components: {AgGridVue},
        data() {
            return {
                spinning: true,
                gene_data: {},
                defaultColDef: {flex: 1, resizable: true,},
                columnDefs: [
                    {headerName: 'DrugBank ID', field: 'value', sortable: true, filter: true},
                    {headerName: 'Drug Name', field: 'name', sortable: true, filter: true},
                ],
                rowData: []
            }
        },
        watch: {
            '$route': {
                handler(val) {
                    let name = val.query.name;
                    if (name) {
                        this.getGene(name);
                        // getGeneExpressionViolin(name).then((res) => {
                        //     console.log(res)
                        // })
                    } else {
                        // this.$router.push('/')
                    }
                },
                immediate: true,
                deep: true
            },
            gene_data(val) {
                if (val) {
                    this.rowData = val.drug_target
                }
            },
        },
        // filters: {
        //     filterColor(val) {
        //         if (val.color === 'yellow') {
        //             return 'is-warning'
        //         } else if (val.color === 'green') {
        //             return 'is-success'
        //         } else if (val.color === 'grey') {
        //             return 'is-dark'
        //         } else {
        //             return 'is-danger'
        //         }
        //     }
        // },
        methods: {
            getGene(name) {
                getGeneDetails(name).then(res => {
                    this.spinning = false;
                    this.gene_data = res.data;
                    this.getViolin(name)
                }).catch(() => {
                    this.$router.push(('/'))
                })
            },
            filteredEyeDiseases(val) {
                if (val) {
                    const arr = val.split(';');
                    arr.pop()
                    return arr
                } else {
                    return []
                }
            },
            dumpDisease(val) {
                this.$router.push({
                    name: 'disease',
                    query: {name: val}
                })
            },
            getViolin(val) {
                getGeneExpressionViolin(val).then((res) => {
                    if (res.disease.length > 0) {
                        let arr = [];
                        for (let i = 0; i < res.disease.length; i++) {
                            let obj = {
                                group: res.disease[i],
                                label: res.disease[i],
                                // color:'#ff0',
                                values: []
                            };
                            arr.push(obj)
                        }
                        for (let i = 0; i < arr.length; i++) {
                            for (let j = 0; j < res.gene.length; j++) {
                                if (res.gene[j].disease === arr[i].label) {
                                    arr[i].values.push(res.gene[j].value)
                                }
                            }
                        }
                        for (let i = 0; i < arr.length; i++) {
                            arr[i].size = arr[i].values.length
                        }
                        const config = {
                            id: 'violin-1-root',
                            data: arr, // web service call would assign the plot's data
                            width: 800,
                            height: 400,
                            marginLeft: 80,
                            marginRight: 90,
                            marginTop: 0,
                            marginBottom: 55,
                            showDivider: true,
                            xPadding: 0.1,
                            yLabel: 'TPM',
                            showSubX: true,
                            showX: false,
                            xAngle: 0,
                            subXAngle: 12,
                            showWhisker: true,
                            showLegend: true,
                            showSampleSize: false
                        };
                        render(config);
                    }
                })
            },
            changeColor(val) {
                if (val === 'yellow') {
                    return '#12545f'
                } else {
                    return val
                }
            }
        },
    }
</script>

<style lang="scss" scoped>
.more-padding {
    padding: 10px;
}

.custom-table {
    border: 1px solid #ccc;

    th {
        font-weight: normal;
        background-color: #fafafa;
        border-right: 1px solid #ccc;
    }
}
</style>
