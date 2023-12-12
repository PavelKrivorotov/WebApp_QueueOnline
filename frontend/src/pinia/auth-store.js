import { ref } from 'vue';
import { defineStore } from 'pinia';

import { LOCALSTORAGE } from '../settings';
import { getLocalStorage } from '../localstorage';

export const useAuthStore = defineStore('auth-store', () => {
    const isAuthenticated = ref(false);
    const authorizationToken = ref(null);

    return {
        isAuthenticated,
        authorizationToken,
    }
});

export function setAuthStore() {
    const authStore = useAuthStore();
    const token = getLocalStorage(LOCALSTORAGE['AUTHORIZATION_TOKEN'])

    if (!token) { authStore.isAuthenticated = false; }
    else { authStore.isAuthenticated = true; }

    authStore.authorizationToken = token;
}
