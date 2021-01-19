<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <section class="section">
        <div class="container ">
            <div class="content has-text-centered">
                <h1 class="title">{{ diseaseName }}</h1>

                <div class="jump-options">
                    <img @click="dynamicClick('disease')"
                         alt="Genetics"
                         src="../assets/icon-browse-genetics.png"/>

                    <img :class="{'jump-option-disabled': !isActive('expression')}"
                         @click="dynamicClick('expression')"
                         alt="Expression"
                         src="../assets/icon-browse-expression.png"/>

                    <img :class="{'jump-option-disabled': !isActive('epigenomics')}"
                         @click="dynamicClick('epigenomics')"
                         alt="Epigenomics"
                         src="../assets/icon-browse-epigenomics.png"/>
                </div>
            </div>

            <div class="columns is-centered">
                <div class="column is-narrow">
                    <div class="content">
                        <h4 class="title is-4">Options:</h4>
                        <ol type="1">
                            <li>Genetics: Browse the candidate gene and variant by disease type.</li>
                            <li>Expression: Browse and search gene expression by tissue, disease and development stage.</li>
                            <li>Epigenomics: Browse and search ChIP-seq, ATAC-seq and DNA methylation data in Genome Browser.</li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    import {getDiseaseExist} from "../api/server";

    export default {
        data() {
            return {
                diseaseName: null,
                expression: false,
                epigenomics: false
            }
        },

        created() {
            const disease = this.$route.query.name;
            if (disease) {
                this.diseaseName = disease;
                getDiseaseExist(disease).then(result => {
                    this.expression = result.data.expression;
                    this.epigenomics = result.data.epigenomics;
                })
            }
        },

        methods: {
            isActive(page) {
                if (page === 'expression') {
                    return this.expression
                } else if (page === 'epigenomics') {
                    return this.epigenomics
                }
            },

            dynamicClick(page) {
                if (page === 'disease') {
                    this.$router.push({name: 'disease', query: {name: this.diseaseName}})
                } else if (page === 'expression') {
                    if (this.expression) {
                        this.$router.push({name: 'expression', query: {name: this.diseaseName}})
                    }
                } else if (page === 'epigenomics') {
                    if (this.epigenomics) {
                        this.$router.push({name: 'epigenomics', query: {name: this.diseaseName}})
                    }
                }
            },
        }
    }
</script>

<style lang="scss" scoped>
.jump-options {
    img {
        cursor: pointer;
        width: 260px;
        border-radius: 15px;
        margin: 2.5%
    }

    .jump-option-disabled {
        -webkit-filter: grayscale(100%); /* Webkit */
        filter: grayscale(100%); /* W3C */
        cursor: not-allowed;
    }
}
</style>
