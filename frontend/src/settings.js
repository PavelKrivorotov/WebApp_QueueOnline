// Server API section
export const SERVER_PROTOCOL = import.meta.env.VITE_SERVER_PROTOCOL
export const SERVER_HOST = import.meta.env.VITE_SERVER_HOST
export const SERVER_PORT = import.meta.env.VITE_SERVER_PORT


// Axios section
export const AXIOS_TIMEOUT = 1000;
export const AXIOS_HEADERS = {
    'Content-Type': 'application/json',
};


// Local storage section
export const LOCALSTORAGE = {
    EMAIL: 'EMAIL',
    AUTHORIZATION_TOKEN: 'AUTHORIZATION_TOKEN',
    QUEUE_KEY: 'QUEUE_KEY',
};
