<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <section class="section">
        <div class="container">
            <b-tabs v-model="activeTab">
                <b-tab-item label="Gene-Disease Network" value="Gene-Disease Network">
                    <VueNetwork v-if="activeTab === 'Gene-Disease Network'"></VueNetwork>
                </b-tab-item>

                <b-tab-item label="Enriched GO and pathway" value="Enriched GO and pathway">
                    <VueGo v-if="activeTab === 'Enriched GO and pathway'"></VueGo>
                </b-tab-item>

                <b-tab-item label="Gene significance" value="Gene significance">
                    <GeneSignificance v-if="activeTab === 'Gene significance'"></GeneSignificance>
                </b-tab-item>

                <b-tab-item label="Co-expression" value="Co-expression">
                    <VueCoExpression v-if="activeTab === 'Co-expression'"></VueCoExpression>
                </b-tab-item>

                <b-tab-item label="Epigenetic alteration" value="Epigenetic alteration">
                    <VueEpigenetic v-if="activeTab === 'Epigenetic alteration'"></VueEpigenetic>
                </b-tab-item>
            </b-tabs>
        </div>
    </section>
</template>

<script>
    import VueNetwork from "../components/analysis/network";
    import VueGo from "../components/analysis/go";
    import VueCoExpression from "../components/analysis/co-expression";
    import VueEpigenetic from "../components/analysis/alteration";
    import GeneSignificance from "../components/analysis/gene-significance";

    export default {
        components: {
            VueNetwork,
            VueGo,
            VueCoExpression,
            VueEpigenetic,
            GeneSignificance,
        },
        data() {
            return {
                activeTab: 'Gene-Disease Network',
            }
        },
    }
</script>

<style scoped>

</style>
