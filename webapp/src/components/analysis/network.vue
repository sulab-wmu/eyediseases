<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <div class="columns">
        <div class="column">
            <div class="content">

                <h6 class="title is-6">Enter gene or disease names</h6>
                <p class="subtitle is-6"><u style="cursor: pointer" @click="showExample">A search example</u></p>
            </div>
            <b-field>
                <b-input type="textarea" v-model="geneList"></b-input>
            </b-field>
            <b-button type="is-info" @click="renderSankeyDiagram">Submit</b-button>
        </div>
        <div class="column" :span="14">
            <div ref="sankeyDiagram"></div>
        </div>
    </div>
</template>

<script>
    import {drawSankey} from "./sankeyDiagram";
    import {getGeneDiseaseNetwork} from "../../api/server";

    export default {
        data() {
            return {
                geneList: 'C9,CFB,GLS,ACTB,ADAM9,BICC1'
            }
        },
        methods: {
            renderSankeyDiagram() {
                const sankeyElement = this.$refs.sankeyDiagram;
                sankeyElement.innerHTML = '';
                getGeneDiseaseNetwork({keywords: this.geneList}).then(res => {
                    drawSankey(sankeyElement, res.data, {width: sankeyElement.clientWidth, height: 800});
                })
            },

            showExample() {
                this.geneList = 'C9,CFB,GLS,ACTB,ADAM9,BICC1';
                this.renderSankeyDiagram();
            }
        },
        mounted() {
            this.renderSankeyDiagram()
        }
    }
</script>

<style lang="scss" scoped>
::v-deep .node rect {
    cursor: move;
    fill-opacity: .9;
    shape-rendering: crispEdges;
}

::v-deep .node text {
    pointer-events: none;
    text-shadow: 0 1px 0 #fff;
}

::v-deep .link {
    fill: none;
    stroke: #000;
    stroke-opacity: .2;
}

::v-deep .link:hover {
    stroke-opacity: .5;
}
</style>
