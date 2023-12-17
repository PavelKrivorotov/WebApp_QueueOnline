<script setup>
import { useRouter } from 'vue-router';

import * as settings from './settings'
import { removeLocalStorage } from './localstorage';
import { useAuthStore } from './pinia/auth-store';
import { authLogout } from './http/requests'

const router = useRouter();
const authStore = useAuthStore();

async function userLogout() {
    try {
        // const response = await authLogout;

        authStore['isAuthenticated'] = false;
        authStore['authorizationToken'] = null;

        // 
        removeLocalStorage(settings.LOCALSTORAGE['AUTHORIZATION_TOKEN'])
        
        // 
        router.push({
            path: '/auth/login',
        });
    }
    catch (error) {
        console.log('Error in `HomeVieW -> userLogout!`')
        console.error(error)
    }
}
</script>

<template>
    <VApp>
        <template v-if="authStore['isAuthenticated']">
            <VAppBar>
                <template v-slot:append>
                    <VBtn icon="mdi-account"></VBtn>
                    <VBtn icon="mdi-logout" @click="userLogout"></VBtn>
                </template>
            </VAppBar>
        </template>

        <template v-else>
            <VAppBar>
                <template v-slot:append>
                    <VBtn to="/auth/login">Sign In</VBtn>
                    <VBtn to="/auth/registration">Sign Up</VBtn>
                </template>
            </VAppBar>
        </template>

        <VMain>
            <RouterView />
        </VMain>
    </VApp>
</template>

<style scoped>
</style>
