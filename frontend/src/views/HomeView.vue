<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { useAuthStore } from '../pinia/auth-store';
import { authLogout } from '../http/requests'
import { LOCALSTORAGE } from '../settings';
import { removeLocalStorage } from '../localstorage';

import QueueComponent from '../components/QueueComponent.vue'
import ContentComponent from '../components/ContentComponent.vue';
import HistoryComponent from '../components/HistoryComponent.vue'

const router = useRouter();
const authStore = useAuthStore();

async function userLogout() {
    try {
        // const response = await authLogout;

        authStore['isAuthenticated'] = false;
        authStore['authorizationToken'] = null;

        // 
        removeLocalStorage(LOCALSTORAGE['AUTHORIZATION_TOKEN'])
        
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
    <VToolbar>
        <template v-slot:prepend>
            <!-- <VBtn>Profile</VBtn> -->
            <!-- <VBtn :active="isActiveQueues" @click="activeQueuesContent">Queues</VBtn> -->
        </template>

        <template v-slot:append>
            <VBtn icon="mdi-account"></VBtn>
            <VBtn icon="mdi-logout" @click="userLogout"></VBtn>
        </template>
    </VToolbar>

    <VContainer fluid>
        <VRow>
            <VCol
            cols="2"
            >
                <QueueComponent></QueueComponent>
            </VCol>

            <VCol
            cols="7"
            >
                <ContentComponent></ContentComponent>
            </VCol>

            <VCol
            cols="3"
            >
                <HistoryComponent></HistoryComponent>
            </VCol>
        </VRow>
    </VContainer>
</template>

<style scope>
</style>
