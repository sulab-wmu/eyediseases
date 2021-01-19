/*
 * Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
 * All rights reserved.
 */

import Vue from 'vue';
import axios from 'axios';
import {ToastProgrammatic as Toast} from 'buefy'

const message = {
    error(text, seconds = 2) {
        Toast.open({
            duration: seconds * 1000,
            message: text,
            type: 'is-danger'
        })
    }
}

const isHandlerEnabled = (config = {}) => {
    return !Object.prototype.hasOwnProperty.call(config, "bar") || config.handlerEnabled
};


const requestHandler = (request) => {
    if (isHandlerEnabled(request)) {

        const contentType = request.contentType || 'application/json';
        if (contentType === 'application/json') {
            request.data = JSON.stringify(request.data)
        }

        const requestDecorator = request.requestDecorator;
        if (typeof requestDecorator === "function") {
            requestDecorator(request);
        }

        request.headers['Content-Type'] = contentType;
        request.headers['Accept-Language'] = Vue.config.lang;
    }
    return request
};


const errorHandler = (error) => {
    if (isHandlerEnabled(error.config)) {
        if (error && error.response) {
            const errorData = error.response.data;
            const errorMessage = error.response.data.message;
            switch (error.response.status) {
                case 400:
                    // router.push({
                    //     path: "/",
                    // });
                    message.error(errorMessage, 2.5);
                    break;
                case 401:
                    message.error(errorMessage, 2.5);
                    // router.push({
                    //     path: "/",
                    // });
                    break;
                case 403:
                    message.error(errorMessage, 2.5);
                    break;
                case 404:
                    message.error(errorMessage, 2.5);
                    break;
                case 405:
                    console.log('请求方法未允许');
                    break;
                case 408:
                    console.log('请求超时');
                    break;
                case 422:
                    if (errorData.errors) {
                        for (const [model, validationErrors] of Object.entries(errorData.errors)) {
                            if (validationErrors.constructor === Object) {
                                for (const [m, v] of Object.entries(validationErrors)) {
                                    const validationErrorString2 = v.join(', ');
                                    message.error(`${m}: ${validationErrorString2}!`, 2.5);
                                }
                            } else {
                                const validationErrorString = validationErrors.join(', ')
                                message.error(`${model}: ${validationErrorString}!`, 2.5);
                            }

                        }
                    } else {
                        message.error(errorMessage, 2.5);
                    }
                    break;
                case 500:
                    console.log('服务器端出错');
                    break;
                case 501:
                    console.log('网络未实现');
                    break;
                case 502:
                    console.log('网络错误');
                    break;
                case 503:
                    console.log('服务不可用');
                    break;
                case 504:
                    console.log('网络超时');
                    break;
                case 505:
                    console.log('http版本不支持该请求');
                    break;
                default:
                    console.log(`连接错误`)
            }
        } else {
            console.log('连接到服务器失败')
        }
    }
    return Promise.reject({...error})
};

const successHandler = (response) => {
    if (isHandlerEnabled(response.config)) {
        // Handle responses
    }
    return response
};

export function makeUrl(path) {
    return process.env.VUE_APP_ROOT + path
}

function createAxios() {
    const http = axios.create({
        baseURL: process.env.VUE_APP_ROOT,
        // baseURL: 'http://10.3.1.105:5000',
        timeout: 50000, // 网络超时
    });

    // http request 拦截器
    // https://dev.to/teroauralinna/global-http-request-and-response-handling-with-the-axios-interceptor-30ae
    http.interceptors.request.use(request => requestHandler(request));
    // 响应拦截器即异常处理vm.axios.baseURL
    http.interceptors.response.use(
        response => successHandler(response),
        error => errorHandler(error),
    );
    return http
}

const axiosInstance = createAxios();


/**
 * 封装get方法
 * @param url
 * @param params
 * @returns {Promise}
 */
export function get(url, params = {}) {
    return new Promise((resolve, reject) => {
        axiosInstance.get(url, {
            params: params
        }).then(response => {
            resolve(response.data);
        }).catch(err => {
            reject(err)
        })
    })
}


export default axiosInstance
