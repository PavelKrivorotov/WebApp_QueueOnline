import axios from 'axios';

import {
    AXIOS_BASE_URL,
    AXIOS_TIMEOUT,
    AXIOS_HEADERS } from '../settings';
import { 
    URL_POST_AUTH_REGISTARTION,
    URL_POST_AUTH_LOGIN,
    URL_DELETE_AUTH_LOGOUT,

    URL_POST_QUEUE_CREATE,
    URL_GET_QUEUE_RETRIEVE,
    URL_GET_QUEUE_QUEUES,

    URL_GET_QUEUE_LIFETIMES } from './urls';


const ax = axios.create({
    baseURL: AXIOS_BASE_URL,
    timeout: AXIOS_TIMEOUT,
    headers: AXIOS_HEADERS,
});

export async function authRegistartion(formData) {
    try {
        const response = await ax.post(
            URL_POST_AUTH_REGISTARTION,
            formData,
        );

        return response;
    }
    catch (error) {
        throw error;
    }
}

export async function authLogin(formData) {
    try {
        const response = await ax.post(
            URL_POST_AUTH_LOGIN,
            formData,
        );

        return response;
    }
    catch (error) {
        throw error;
    }
}

export async function authLogout(token) {}


export async function queueCreate(token, formData) {
    try {
        const response = await ax.post(
            URL_POST_QUEUE_CREATE,
            formData, {
                headers: {
                    'Token': token,
                    'Content-Type': 'application/json',
                }
            }
        );

        return response;
    }
    catch (error) {
        console.log(error)
    }
}

export async function queueRetrieve(token, queueKey) {
    try {
        const response = await ax.get(
            `${URL_GET_QUEUE_RETRIEVE}/${queueKey}`, {
                headers: {
                    'Token': token,
                    'Content-Type': 'application/json',
                }
            }
        );

        return response;
    }
    catch (error) {
        throw error;
    }
}

export async function queueQueues(token) {
    try {
        const response = await ax.get(
            URL_GET_QUEUE_QUEUES, {
                headers: {
                    'Token': token,
                    'Content-Type': 'application/json',
                }
            }
            
        );

        return response;
    }
    catch (error){
        throw error;
    }
}

export async function queueLifetimes() {
    try {
        const response = await ax.get(
            URL_GET_QUEUE_LIFETIMES,
        );

        return response;
    }
    catch (error) {
        throw error;
    }
}
