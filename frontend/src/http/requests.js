import axios from 'axios';

import * as settings from '../settings'
import * as urls from './urls'

const ax = axios.create({
    baseURL: `${settings.SERVER_PROTOCOL}://${settings.SERVER_HOST}:${settings.SERVER_PORT}`,
    timeout: settings.AXIOS_TIMEOUT,
    headers: settings.AXIOS_HEADERS,
});

export async function tokenConfirm(token) {
    try {
        const response = await ax.get(
            urls.URL_GET_TOKEN_CONFIRM, {
                headers: {
                    'Token': token,
                }
            }
        );

        return response;
    }
    catch (error) {
        throw error;
    }
}

export async function authRegistartion(formData) {
    try {
        const response = await ax.post(
            urls.URL_POST_AUTH_REGISTARTION,
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
            urls.URL_POST_AUTH_LOGIN,
            formData,
        );

        return response;
    }
    catch (error) {
        throw error;
    }
}

export async function authLogout(token) {
    try {
        const response = await ax.delete(
            urls.URL_DELETE_AUTH_LOGOUT, {
                headers: {
                    'Token': token,
                }
            }
        );

        return response;
    }
    catch (error) {
        throw error
    }
}


export async function queueCreate(token, formData) {
    try {
        const response = await ax.post(
            urls.URL_POST_QUEUE_CREATE,
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
            `${urls.URL_GET_QUEUE_RETRIEVE}/${queueKey}`, {
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
            urls.URL_GET_QUEUE_QUEUES, {
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
            urls.URL_GET_QUEUE_LIFETIMES,
        );

        return response;
    }
    catch (error) {
        throw error;
    }
}
