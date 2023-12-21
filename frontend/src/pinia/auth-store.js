import { ref } from 'vue';
import { defineStore } from 'pinia';

import * as settings from '../settings';
import { getLocalStorage, setLocalStorage, removeLocalStorage } from '../localstorage';
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
                isAuthenticated.value = true;
                authorizationToken.value = token;

                await tokenConfirm(token);
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

    function authorizationComplete(token) {
        isAuthenticated.value = true;
        authorizationToken.value = token;

        setLocalStorage(
            settings.LOCALSTORAGE['AUTHORIZATION_TOKEN'],
            token
        );
    }

    return {
        isAuthenticated,
        authorizationToken,

        setAuthStore,
        authorizationComplete,
    }
});
