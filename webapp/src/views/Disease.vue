<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <section class="section">
        <div class="container">
            <div class="columns">
                <div class="column is-one-quarter side-bar">
                    <div class="content">
                        <h5 class="title is-5">Search by Disease</h5>
                        <b-field>
                            <b-autocomplete
                                v-model="searchString"
                                placeholder="By disease name"
                                :open-on-focus="true"
                                :data="dataSource"
                                field="name"
                                @typing="changeDisease"
                                @select="option => selectDisease(option.name)">
                            </b-autocomplete>
                        </b-field>
                    </div>

                    <h5 class="title is-5">Browse by Disease</h5>
                    <b-menu :accordion="true">
                        <b-menu-list>
                            <b-menu-item v-for="menu in treeData">
                                <template slot="label" slot-scope="props">
                                    {{ menu.title }}
                                    <b-icon class="is-pulled-right" :icon="props.expanded ? 'angle-down' : 'angle-up'"></b-icon>
                                </template>
                                <b-menu-item
                                    :label="submenu.title"
                                    @click="selectDisease(submenu.title)"
                                    v-for="submenu in menu.children">
                                </b-menu-item>
                            </b-menu-item>


                        </b-menu-list>
                    </b-menu>
                </div>

                <div class="column">
                    <div class="content">
                        <h5 class="title is-5">OMIM: {{ diseaseName }}</h5>
                        <ag-table-g :data="agGirdDateO" :type="OMIMType"></ag-table-g>
                    </div>

                    <div class="content">
                        <h5 class="title is-5">GWAS: {{ diseaseName }}</h5>
                        <ag-table-g :data="agGirdDateG" :type="GWASType"></ag-table-g>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    import AgTableG from "../components/search/agrid_disease_table.vue";
    import diseasename from "../data/diseasename.json"
    import {getDiseaseList, getGWAS, getOMIM} from "../api/server";
    import {debounce} from "../utils";

    const treeData = [
        {
            title: 'Conjunctival Diseases (2)',
            key: '0-0',
            children: [
                {title: 'Chlamydia trachomatis seropositivity', key: '0-0-1'},
                {title: 'Pterygium', key: '0-0-2'},],

        },
        {
            title: 'Corneal Diseases (3)',
            key: '0-1',
            children: [
                {title: "Fuchs' endothelial corneal dystrophy", key: '0-1-1'},
                {title: 'Keratitis', key: '0-1-2'},
                {title: 'Keratoconus', key: '0-1-3'},
            ],
        },
        {
            title: 'Eye Nwoplasms (1)',
            key: '0-2',
            children: [
                {title: 'Uveal melanoma', key: '0-2-1'},
            ],
        },
        {
            title: 'Lacrimal Apparatus Diseases (1)',
            key: '0-3',
            children: [
                {title: 'Aplasia of lacrimal and salivary glands', key: '0-3-1'},
            ],
        },
        {
            title: 'Lens Diseases (5)',
            key: '0-4',
            children: [
                {title: 'Cataracts in type 2 diabetes', key: '0-4-1'},
                {title: 'Age-related cataracts', key: '0-4-2'},
                {title: 'Cataract ', key: '0-4-3'},
                {title: 'Age-related nuclear cataracts', key: '0-4-4'},
                {title: 'Lens dislocation', key: '0-4-5'},
            ],
        },
        {
            title: 'Ocular Hypertension (8)',
            key: '0-5',
            children: [
                {title: 'Glaucoma (exfoliation)', key: '0-5-1'},
                {title: 'Glaucoma (high intraocular pressure)', key: '0-5-2'},
                {title: 'Glaucoma (low intraocular pressure)', key: '0-5-3'},
                {title: 'Glaucoma (primary angle closure)', key: '0-5-4'},
                {title: 'Glaucoma (primary open-angle)', key: '0-5-5'},
                {title: 'Open-angle glaucoma and optic cup area', key: '0-5-6'},
                {title: 'Open-angle glaucoma and vertical cup-disc ratio', key: '0-5-7'},
                {title: 'Glaucoma', key: '0-5-8'},
            ],
        },
        {
            title: 'Ocular Motility Disorders (4)',
            key: '0-6',
            children: [
                {title: "Non-Richardson's syndrome vs Richardson's syndrome in progressive supranuclear palsy", key: '0-6-1'},
                {title: 'Progressive supranuclear palsy', key: '0-6-2'},
                {title: 'Strabismus', key: '0-6-3'},
                {title: 'Non-accommodative esotropia', key: '0-6-4'},
            ],
        },
        {
            title: 'Orbital Diseases (2)',
            key: '0-7',
            children: [
                {title: "Autoimmune thyroid diseases (Graves disease or Hashimoto's thyroiditis)", key: '0-7-1'},
                {title: 'Thyrotoxic hypokalemic periodic paralysis and Graves disease', key: '0-7-2'},
            ],
        },
        {
            title: 'Refractive Errors (7)',
            key: '0-8',
            children: [
                {title: 'Refractive astigmatism', key: '0-8-1'},
                {title: 'Corneal astigmatism', key: '0-8-2'},
                {title: 'Myopia', key: '0-8-3'},
                {title: 'Myopia (pathological)', key: '0-8-4'},
                {title: 'Myopia (severe)', key: '0-8-5'},
                {title: 'Hyperopia', key: '0-8-6'},
                {title: 'Refractive error', key: '0-8-7'},
            ],
        },
        {
            title: 'Retinal Diseases (59)',
            key: '0-9',
            children: [
                {title: 'Proliferative diabetic retinopathy', key: '0-9-1'},
                {title: 'Proliferative diabetic retinopathy in type 2 diabetes', key: '0-9-2'},
                {title: 'Proliferative vitreoretinopathy', key: '0-9-3'},
                {title: 'Retinal degeneration', key: '0-9-4'},
                {title: 'Retinal detachment', key: '0-9-5'},
                {title: 'Retinitis', key: '0-9-6'},
                {title: 'Retinopathy of prematurity ', key: '0-9-7'},
                {title: 'Rhegmatogenous retinal detachment', key: '0-9-8'},
                {title: 'Severe diabetic retinopathy in type 2 diabetes', key: '0-9-9'},
                {title: 'Sight-threatening diabetic retinopathy in type 2 diabetes', key: '0-9-10'},
                {title: 'Diabetic retinopathy', key: '0-9-11'},
                {title: 'Diabetic retinopathy in type 2 diabetes', key: '0-9-12'},
                {title: 'Chorioretinopathy', key: '0-9-13'},
                {title: 'Advanced age-related macular degeneration', key: '0-9-14'},
                {title: 'Age-related macular degeneration', key: '0-9-15'},
                {title: 'Age-related macular degeneration (geographic atrophy)', key: '0-9-16'},
                {title: 'Age-related macular degeneration (wet)', key: '0-9-17'},
                {title: 'Disease progression in age-related macular degeneration', key: '0-9-18'},
                {title: 'Exudative age-related macular degeneration', key: '0-9-19'},
                {title: 'Laterality in neovascular age-related macular degeneration', key: '0-9-20'},
                {title: 'Neovascular age-related macular degeneration', key: '0-9-21'},
                {title: 'Diabetic macular edema in type 2 diabetes', key: '0-9-22'},
                {title: 'Myopic maculopathy', key: '0-9-23'},
                {title: 'Blue cone monochromacy', key: '0-9-24'},
                {title: 'Cerebroretinal microangiopathy', key: '0-9-25'},
                {title: 'Cone dystrophy', key: '0-9-26'},
                {title: 'Cone-rod dystrophy', key: '0-9-27'},
                {title: 'Cone-rod synaptic disorder', key: '0-9-28'},
                {title: 'Doyne honeycomb degeneration of retina', key: '0-9-29'},
                {title: 'Febrile seizures', key: '0-9-30'},
                {title: 'Foveal hypoplasia', key: '0-9-31'},
                {title: 'Foveal hypoplasia with or without optic nerve misrouting and/or anterior segment dysgenesis', key: '0-9-32'},
                {title: 'Fundus albipunctatus', key: '0-9-33'},
                {title: 'Gyrate atrophy of choroid and retina with or without ornithinemia', key: '0-9-34'},
                {title: 'Macular dystrophy', key: '0-9-35'},
                {title: 'Microphthalmia', key: '0-9-36'},
                {title: 'Night blindness', key: '0-9-37'},
                {title: 'Retinal dysplasia', key: '0-9-38'},
                {title: 'Retinal dystrophy', key: '0-9-39'},
                {title: 'Retinoblastoma', key: '0-9-40'},
                {title: 'Retinopathy of prematurity', key: '0-9-41'},
                {title: 'Retinoschisis', key: '0-9-42'},
                {title: 'Stargardt disease', key: '0-9-43'},
                {title: 'Vitreoretinal dystrophy', key: '0-9-44'},
                {title: 'Vitreoretinopathy', key: '0-9-45'},
                {title: 'Achromatopsia', key: '0-9-46'},
                {title: 'Alagille syndrome', key: '0-9-47'},
                {title: 'Alstrom syndrome', key: '0-9-48'},
                {title: 'Bardet-Biedl syndrome', key: '0-9-49'},
                {title: 'Benign retinoma', key: '0-9-50'},
                {title: 'Boucher-Neuhauser syndrome', key: '0-9-51'},
                {title: 'Colorblindness', key: '0-9-52'},
                {title: 'Leber hereditary optic neuropathy', key: '0-9-53'},
                {title: 'Muscular dystrophy', key: '0-9-54'},
                {title: 'Optic atrophy', key: '0-9-55'},
                {title: 'Optic atrophy syndrome', key: '0-9-56'},
                {title: 'Optic disc anomalies', key: '0-9-57'},
                {title: 'Pigmentary retinopathy', key: '0-9-58'},
                {title: 'Sorsby fundus dystrophy', key: '0-9-59'},
            ],
        },
        {
            title: 'Uveal Diseases (13)',
            key: '0-10',
            children: [
                {title: 'Age-related macular degeneration (choroidal neovascularisation)', key: '0-10-1'},
                {title: 'Choroidal neovascularization', key: '0-10-2'},
                {title: 'Disease progression to choroidal neovascularization form in age-related macular degeneration', key: '0-10-3'},
                {title: 'Exfoliation syndrome', key: '0-10-4'},
                {title: "Behcet's disease", key: '0-10-5'},
                {title: 'Acute anterior uveitis (with or without ankylosing spondylitis)', key: '0-10-6'},
                {title: 'Acute anterior uveitis in ankylosing spondylitis', key: '0-10-7'},
                {title: 'Vogt-Koyanagi-Harada syndrome', key: '0-10-8'},
                {title: 'Exfoliation glaucoma or exfoliation syndrome', key: '0-10-9'},
                {title: 'Pseudoexfoliation syndrome', key: '0-10-10'},
                {title: 'Chorioretinal atrophy', key: '0-10-11'},
                {title: 'Choroidal dystrophy', key: '0-10-12'},
                {title: 'Choroideremia', key: '0-10-13'},
            ]
        },
        {
            title: 'Other Disease (80)',
            key: '0-11',
            children: [
                {title: '3-methylglutaconic aciduria', key: '0-11-1'},
                {title: 'Abetalipoproteinemia', key: '0-11-2'},
                {title: 'Aicardi-Goutieres syndrome', key: '0-11-3'},
                {title: 'Arts syndrome', key: '0-11-4'},
                {title: 'Bone mineral density variability', key: '0-11-5'},
                {title: 'Cerebrooculofacioskeletal syndrome', key: '0-11-6'},
                {title: 'Ceroid lipofuscinosis, neuronal', key: '0-11-7'},
                {title: 'Charcot-Marie-Tooth disease', key: '0-11-8'},
                {title: 'Chilblain lupus', key: '0-11-9'},
                {title: 'COACH syndrome', key: '0-11-10'},
                {title: 'Cockayne syndrome', key: '0-11-11'},
                {title: 'Combined oxidative phosphorylation deficiency', key: '0-11-12'},
                {title: 'Complement factor H deficiency', key: '0-11-13'},
                {title: 'Congenital disorder of glycosylation', key: '0-11-14'},
                {title: 'Cranioectodermal dysplasia', key: '0-11-15'},
                {title: 'De Grouchy syndrome', key: '0-11-16'},
                {title: 'De Sanctis-Cacchione syndrome', key: '0-11-17'},
                {title: 'Deafness', key: '0-11-18'},
                {title: 'Delayed cone adaptation', key: '0-11-19'},
                {title: 'Dementia', key: '0-11-20'},
                {title: 'Enhanced S-cone syndrome', key: '0-11-21'},
                {title: 'Fleck retina', key: '0-11-22'},
                {title: 'Fundus flavimaculatus', key: '0-11-23'},
                {title: 'Gout', key: '0-11-24'},
                {title: 'HARP syndrome', key: '0-11-25'},
                {title: 'Hemolytic anemia due to hexokinase deficiency', key: '0-11-26'},
                {title: 'Hyper-IgD syndrome', key: '0-11-27'},
                {title: 'Immunodeficiency', key: '0-11-28'},
                {title: 'Infantile liver failure syndrome', key: '0-11-29'},
                {title: 'Jalili syndrome', key: '0-11-30'},
                {title: 'Jobert syndrome', key: '0-11-31'},
                {title: 'Joubert syndrome', key: '0-11-32'},
                {title: 'Kearns-Sayre syndrome including retinal pigmentary degeneration', key: '0-11-33'},
                {title: 'Knobloch syndrome', key: '0-11-34'},
                {title: 'Land Island eye disease', key: '0-11-35'},
                {title: 'Leber congenital amaurosis', key: '0-11-36'},
                {title: 'Leigh syndrome', key: '0-11-37'},
                {title: 'Marshall syndrome', key: '0-11-38'},
                {title: 'Maturity-onset diabetes', key: '0-11-39'},
                {title: 'McKusick-Kaufman syndrome', key: '0-11-40'},
                {title: 'Meckel syndrome', key: '0-11-41'},
                {title: 'Mevalonic aciduria', key: '0-11-42'},
                {title: 'Mohr-Tranebjaerg syndrome', key: '0-11-43'},
                {title: 'Morbid obesity and spermatogenic failure', key: '0-11-44'},
                {title: 'Mucolipidosis III gamma', key: '0-11-45'},
                {title: 'Mucopolysaccharidosi', key: '0-11-46'},
                {title: 'Nephronophthisis', key: '0-11-47'},
                {title: 'Neurodegeneration', key: '0-11-48'},
                {title: 'Neuropathy', key: '0-11-49'},
                {title: 'Non-syndromic deafness', key: '0-11-50'},
                {title: 'Norrie disease', key: '0-11-51'},
                {title: 'Oculoauricular syndrome', key: '0-11-52'},
                {title: 'Oguchi disease', key: '0-11-53'},
                {title: 'Oliver-McFarlane syndrome', key: '0-11-54'},
                {title: 'Oregon eye disease', key: '0-11-55'},
                {title: 'Orofaciodigital syndrome', key: '0-11-56'},
                {title: 'Osteoarthritis with mild chondrodysplasia', key: '0-11-57'},
                {title: 'Osteoporosis-pseudoglioma syndrome', key: '0-11-58'},
                {title: 'Peroxisome biogenesis disorder', key: '0-11-59'},
                {title: 'Persistent hyperplastic primary vitreous', key: '0-11-60'},
                {title: 'Phosphoglycerate kinase 1 deficiency', key: '0-11-61'},
                {title: 'Phosphoribosylpyrophosphate synthetase superactivity', key: '0-11-62'},
                {title: 'Pituitary hormone deficiency, combined, 6', key: '0-11-63'},
                {title: 'Poretti-Boltshauser syndrome', key: '0-11-64'},
                {title: 'Porokeratosis', key: '0-11-65'},
                {title: 'Pseudoxanthoma elasticum', key: '0-11-66'},
                {title: 'Refsum disease', key: '0-11-67'},
                {title: 'Rhizomelic chondrodysplasia punctata', key: '0-11-68'},
                {title: 'Senior-Loken syndrome', key: '0-11-69'},
                {title: 'Short-rib thoracic dysplasia', key: '0-11-70'},
                {title: 'Sideroblastic anemia with B-cell immunodeficiency', key: '0-11-71'},
                {title: 'Simpson-Golabi-Behmel syndrom', key: '0-11-72'},
                {title: 'Spastic ataxia', key: '0-11-73'},
                {title: 'Spastic paraplegia', key: '0-11-74'},
                {title: 'Spinocerebellar ataxia', key: '0-11-75'},
                {title: 'Stickler syndrome', key: '0-11-76'},
                {title: 'Usher syndrome', key: '0-11-77'},
                {title: 'Vasculopathy, retinal', key: '0-11-78'},
                {title: 'Visual impairment', key: '0-11-79'},
                {title: 'Wolfram syndrome', key: '0-11-80'},
            ],
        }];

    export default {
        components: {AgTableG},
        data() {
            return {
                OMIMType: 'OMIM',
                GWASType: 'GWAS',
                totalO: null,
                totalG: null,
                agGirdDateG: [],
                agGirdDateO: [],
                dataSource: [],
                diseaseName: '',
                treeData,
                searchString: '',
            }
        },
        watch: {
            '$route': {
                handler(val) {
                    const diseaseName = val.query.name || 'Age-related macular degeneration';
                    this.diseaseName = diseaseName;
                    this.getData(diseaseName)
                },
                immediate: true,
                deep: true
            }
        },
        methods: {
            selectDisease(disease) {
                this.diseaseName = disease;
                this.getData(disease);
            },

            onSelect(selectedKeys, info) {
                if (!info.node.dataRef.children) {
                    this.diseaseName = info.node.dataRef.title;
                    this.getData(info.node.dataRef.title)
                }
            },
            onChangeO(pageNumber, pageSize) {
                this.getChangePageDataO(this.diseaseName, pageNumber, pageSize)
            },
            showSizeChangeO(current, size) {
                this.getChangePageDataO(this.diseaseName, current, size)
            },
            onChangeG(pageNumber, pageSize) {
                this.getChangePageDataG(this.diseaseName, pageNumber, pageSize)
            },
            showSizeChangeG(current, size) {
                this.getChangePageDataG(this.diseaseName, current, size)
            },
            jsonToArray() {
                let arr = [];
                for (let i in diseasename) {
                    arr.push(diseasename[i])
                }
                return arr
            },
            getData(name) {
                let disease_name = '';
                if (!name) {
                    disease_name = this.$route.query.disease
                } else {
                    disease_name = name
                }
                const params = {dis: disease_name};
                getGWAS(params).then(result => {
                    this.agGirdDateG = result.data;
                    this.totalG = result.pagination.total
                });

                getOMIM(params).then(result => {
                    this.agGirdDateO = result.data;
                    this.totalO = result.pagination.total
                })
            },
            getChangePageDataO(name, page, number) {
                let obj = {
                    dis: name,
                    page: page,
                    number: number,
                };

                getOMIM(obj).then(result => {
                    this.agGirdDateO = result.data;
                    this.totalO = result.pagination.total
                })
            },
            getChangePageDataG(name, page, number) {
                const params = {
                    dis: name,
                    page: page,
                    number: number,
                };

                getGWAS(params).then(result => {
                    this.agGirdDateG = result.data;
                    this.totalG = result.pagination.total
                })
            },
            changeDisease: debounce(function (e) {
                if (e === '' || e === undefined || e === null) {
                    this.dataSource = []
                } else {
                    getDiseaseList(e).then(res => {
                        this.dataSource = res.data
                    })
                }

            }, 317),
            searchDisease(val) {
                this.$router.push({
                    path: '/disease',
                    query: {name: val}
                })
            },
        }
    }
</script>

<style lang="scss" scoped>
.side-bar {
    min-width: 335px;
}

.autocomplete ::v-deep .dropdown-content {
    width: fit-content;
}
</style>
