/*
 * Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
 * All rights reserved.
 */

/** * 引入vue-i18n */
import Vue from 'vue'
import VueI18n from 'vue-i18n';

/** * 导入APP json语言包 */
import app_zh from './zh-CN.json'
import app_en from './en-US.json';

Vue.use(VueI18n);

/** * 多语言配置 * Object.assign(zh,app_zh) * zh : iview 语言包 * app_zh : App json语言包 */
Vue.locale('zh', app_zh)
Vue.locale('en', app_en)

// 自动设置语言
// 获取本机系统语言
const navLang = navigator.language;
console.log('sdssdsdsds', navLang)

const localLang = (navLang === 'zh' || navLang === 'en') ? navLang : false;
/** * localStorage.getItem(key):获取指定key本地存储的值 * localStorage.setItem(key,value)：将value存储到key字段 * localStorage.removeItem(key):删除指定key本地存储的值 */
const lang = window.localStorage.getItem('language') || localLang || 'zh';


// 配置默认语言
// Vue.config.lang = 'zh-CN'; 默认为中文
// Vue.config.lang = 'en-US'; 默认为英文
Vue.config.lang = lang;

export default {}
