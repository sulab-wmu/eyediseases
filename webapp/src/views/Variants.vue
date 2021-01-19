<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <section class="section">
        <div class="container">
            <div class="columns">
                <div class="column">
                    <div class="content more-padding">
                        <h4 class="title is-4">Summary</h4>
                        <table class="table custom-table">
                            <tbody>
                            <tr>
                                <th>SNP</th>
                                <td>{{ summaryData.snpid }}</td>
                            </tr>
                            <tr>
                                <th>Position</th>
                                <td>chr{{ summaryData.position_hg38 }}(GRCh38)</td>
                            </tr>
                            <tr>
                                <th>Alleles</th>
                                <td>{{ summaryData.major_allele }}</td>
                            </tr>
                            <tr>
                                <th>Consequence</th>
                                <td>{{ summaryData.variant }}</td>
                            </tr>
                            <tr>
                                <th>Protein change</th>
                                <td>{{ summaryData.protein }}</td>
                            </tr>
                            <tr>
                                <th>PolyPhen prediction</th>
                                <td>{{ summaryData.polyphen }}</td>
                            </tr>
                            <tr>
                                <th>CADD</th>
                                <td>{{ summaryData.cadd }}</td>
                            </tr>
                            <tr>
                                <th>Gene</th>
                                <td>{{ summaryData.gene }}</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="column">
                    <div class="content more-padding">
                        <h4 class="title is-4">Associations</h4>
                        <div style="border: 1px solid #ccc; overflow: hidden">
                            <vue-plotly :data="data1" :layout="layout1" :options="options1" :autoresize="true"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="columns">
                <div class="column">
                    <div class="content more-padding">
                        <h4 class="title is-4">External References</h4>
                        <table class="custom-table">
                            <tbody>
                            <tr>
                                <th>Ensembl</th>
                                <td><a :href="summaryData.ensembl" target="_blank">{{ summaryData.snpid }}</a></td>
                            </tr>
                            <tr>
                                <th>dbSNP</th>
                                <td><a :href="summaryData.dbsnp" target="_blank">{{ summaryData.snpid }}</a></td>
                            </tr>
                            <tr>
                                <th>gnomAD</th>
                                <td><a :href="summaryData.gnomad" target="_blank">{{ summaryData.snpid }}</a></td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="column">
                    <div class="content more-padding">
                        <h4 class="title is-4">Minor allele frequencies</h4>
                        <div style="border: 1px solid #ccc; overflow: hidden">
                            <vue-plotly :data="dataGnomad" :layout="layoutGnomad" :options="optionsGnomad" :autoresize="true"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    import {getVariantDetails} from "../api/server";
    import VuePlotly from '@statnett/vue-plotly'

    export default {
        components: {
            VuePlotly,
        },
        data() {
            return {
                tableData: [],
                summaryData: {},
                dataGnomad: [
                    {
                        y: [],
                        x: [],
                        type: 'bar',
                        orientation: 'h',
                        text: [],
                    }
                ],
                layoutGnomad: {
                    height: 500,
                    // width: '100%',
                    xaxis: {
                        title: "MAF(%)",
                    },
                    margin: {
                        l: 120,
                        t: 30
                    },
                },
                optionsGnomad: {responsive: true},
                data1: [
                    {
                        x: [],
                        y: [],
                        mode: 'markers',
                        type: 'scatter',
                        // text: [],
                        // hoverinfo: "x+y",
                        hovertemplate: [],
                        marker: {
                            // color: [],
                            size: 20
                        },
                        transforms: [{
                            type: 'groupby',
                            groups: [],
                            styles: false
                        }]
                    },
                ],
                layout1: {
                    height: 500,
                    // width: '100%',
                    font: {
                        size: 12
                    },
                    title: "",
                    legend: {
                        x: 0,
                        y: -0.8,
                    },
                    xaxis: {
                        title: "OR",
                    },
                    yaxis: {
                        title: "-log10(p-value)",
                    }
                },
                options1: {responsive: true},
            }
        },
        watch: {
            '$route': {
                handler(val) {
                    let variantName = val.query.name;
                    if (variantName) {
                        this.layout1.title = variantName;
                        this.getVariantData(variantName);
                    } else {
                        this.$router.push('/')
                    }
                },
                immediate: true,
                deep: true
            }
        },
        methods: {
            getVariantData(variant) {
                getVariantDetails(variant).then(res => {
                    this.tableData = res.causality.slice(0)
                    let causality = res.causality
                    for (let i = 0; i < causality.length; i++) {
                        let bata = causality[i].beta || 0
                        let p_value = causality[i].p_value || 0
                        this.data1[0].x.push(bata)
                        this.data1[0].y.push(p_value)
                        let str = 'beta:' + bata + '<br>p_value:' + p_value

                        this.data1[0].hovertemplate.push(str)
                        this.data1[0].transforms[0].groups.push(causality[i].disease)
                    }

                    this.summaryData = res.summary;
                    this.dataGnomad[0]['y'] = res.gnomad.y;
                    this.dataGnomad[0]['x'] = res.gnomad.x;
                    this.dataGnomad[0]['text'] = res.gnomad.text
                })
            },
        }
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
