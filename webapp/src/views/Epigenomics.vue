<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <section class="section">
        <div class="container">
            <h1 class="title">Epigenomics</h1>

            <div class="columns">
                <div class="column is-4">
                    <p class="title is-6">1. Select disease / tissue</p>
                    <div :key="option" v-for="option in allDiseases">
                        <b-radio v-model="selectedDisease" :native-value="option">
                            {{ option }}
                        </b-radio>
                    </div>
                </div>

                <div class="column is-3">
                    <p class="title is-6">2. Select data type</p>
                    <div :key="option.type" v-for="option in availableTypes">
                        <b-checkbox v-model="selectedTypes" :native-value="option">
                            {{ option.type }}
                        </b-checkbox>
                    </div>
                </div>

                <div class="column is-5">
                    <p class="title is-6">3. Selected data</p>
                    <b-field>
                        <b-taginput
                            v-model="selectedTypes"
                            autocomplete
                            :allow-new="false"
                            field="data_key"
                            placeholder="Please select">
                        </b-taginput>
                    </b-field>
                    <b-button @click="makeIgv" type="is-info">Load</b-button>
                </div>
            </div>
            <div ref="igvBrowser" class="igvBrowser"></div>
        </div>
    </section>
</template>

<script>
    import IGV from 'igv'
    import {getEpigenomics, getEpigenomicsList} from '../api/server'

    export default {
        data() {
            return {
                allDiseases: {},
                diseasesTypes: [],
                allTracks: [],
                selectedDisease: undefined,
                selectedTypes: [],
            }
        },
        watch: {
            '$route': {
                handler(val) {
                    const diseaseName = val.query.name;
                    if (!diseaseName) {
                        this.selectedDisease = "Age-related macular degeneration"
                    } else {
                        this.selectedDisease = diseaseName;
                    }
                },
                immediate: true,
                deep: true
            }
        },
        computed: {
            availableTypes() {
                if (this.selectedDisease && this.diseasesTypes) {
                    return this.diseasesTypes[this.selectedDisease]
                } else {
                    return [];
                }
            }
        },
        created() {
            getEpigenomics().then((res) => {
                this.allTracks = res.tracks;
                this.reference = res.reference;
            })

            getEpigenomicsList().then(res => {
                this.allDiseases = res.diseases;
                this.diseasesTypes = res.diseases_types;
            })
        },
        methods: {
            makeIgv() {
                this.$refs.igvBrowser.innerHTML = '';
                const tracks = this.getTracks();
                const options = {
                    // genome: "hg19",
                    // reference file list: https://s3.amazonaws.com/igv.org.genomes/genomes.json
                    reference: this.reference,
                    locus: "chr7:27122007-27285206",
                    // locus: '22:16052542',
                    tracks: tracks,
                };

                IGV.createBrowser(this.$refs.igvBrowser, options)
                    .then(function () {
                        console.log("Created IGV browser");
                    })
            },
            getTracks() {
                return this.allTracks
                    .filter(x => this.isInSelected(x.data_key))
                    .map(x => {
                        return {
                            type: "wig",
                            name: x.data_key + ': ' + x.url.split('/').pop(),
                            url: x.url,
                            color: x.color,
                        }
                    });
            },
            isInSelected(dataKey) {
                const filtered = this.selectedTypes.filter(x => x.data_key === dataKey);
                return filtered.length > 0;
            },
        },
        mounted() {
            this.makeIgv()
        }
    }
</script>

<style scoped>
.igvBrowser {
    padding-top: 20px;
}

.igvBrowser ::v-deep .igv-logo {
    visibility: hidden;
}
</style>
