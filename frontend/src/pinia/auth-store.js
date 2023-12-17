import { ref } from 'vue';
import { defineStore } from 'pinia';

import * as settings from '../settings';
import { getLocalStorage, removeLocalStorage } from '../localstorage';
import { tokenConfirm } from '../http/requests';

export const useAuthStore = defineStore('auth-store', () => {
    const isAuthenticated = ref(false);
    const authorizationToken = ref(null);

    async function setAuthStore() {
        const token = getLocalStorage(settings.LOCALSTORAGE['AUTHORIZATION_TOKEN'])
    
        if (!token) {
            isAuthenticated.value = false;
            authorizationToken.value = token;
        }

        else {
            try {
                const response = await tokenConfirm(token);
                isAuthenticated.value = true;
                authorizationToken.value = token;
            }
            catch (error) {
                console.log('Error in auth-store -> setAuthStore');
                console.error(error);

                isAuthenticated.value = false;
                authorizationToken.value = null;

                removeLocalStorage(settings.LOCALSTORAGE['AUTHORIZATION_TOKEN']);
            }
        }
    }

    return {
        isAuthenticated,
        authorizationToken,

        setAuthStore,
    }
});
