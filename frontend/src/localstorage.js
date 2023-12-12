import { LOCALSTORAGE } from './settings';

export function getLocalStorage(key) {
    if (!LOCALSTORAGE[key]) {
        // return null;
        throw Error(
            `In set localstorage. Key ${key} is not declare in LOCALSTORAGE settings`
        );
    }
    return localStorage.getItem(key);
}

export function setLocalStorage(key, value) {
    if (!LOCALSTORAGE[key]) {
        throw Error(
            `In set localstorage. Key ${key} is not declare in LOCALSTORAGE settings`
        );
    }
    localStorage.setItem(LOCALSTORAGE[key], value);
    return value;
}

export function removeLocalStorage(key) {
    if (!LOCALSTORAGE[key]) {
        throw Error(
            `In set localstorage. Key ${key} is not declare in LOCALSTORAGE settings`
        );
    }
    const value = localStorage.getItem(key);
    localStorage.removeItem(key);
    return value;
}
