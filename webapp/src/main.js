/*
 * Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
 * All rights reserved.
 */

import Vue from 'vue'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'

import App from './App.vue'
import {library} from '@fortawesome/fontawesome-svg-core'
import {fas} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

import router from './router'
import store from './store'
import './language/index'


library.add(fas)
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.use(Buefy, {defaultIconComponent: 'font-awesome-icon', defaultIconPack: 'fas'})

Vue.config.productionTip = false

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
