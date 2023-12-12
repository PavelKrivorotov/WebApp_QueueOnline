<script setup>
import { ref } from 'vue';

import { useAuthStore } from '../pinia/auth-store';
import { authLogout } from '../http/requests'
import { LOCALSTORAGE } from '../settings';
import { removeLocalStorage } from '../localstorage';

import QueueComponent from '../components/QueueComponent.vue'
import ContentComponent from '../components/ContentComponent.vue';
import HistoryComponent from '../components/HistoryComponent.vue'

const authStore = useAuthStore();

const isActiveQueues = ref(true);
const isActiveSettings = ref(false);

function activeQueuesContent() {
    isActiveQueues.value = true;
    isActiveSettings.value = false;
}

function activeSettingsContent() {
    isActiveQueues.value = false;
    isActiveSettings.value = true;
}

async function userLogout() {
    try {
        // const response = await authLogout;

        authStore.isAuthenticated = false;
        authStore.authorizationToken = null;

        // 
        removeLocalStorage(LOCALSTORAGE['AUTHORIZATION_TOKEN'])

    }
    catch (error) {
        console.log('Error in `HomeVieW -> userLogout!`')
        console.error(error)
    }
}

async function queueCreate(queue) {
    console.log('Create queue emits HomeView')
}

async function queueConnect(queue) {
    console.log('Connect queue emits HomeView', queue)
}

async function queueJoin(key) {
    console.log('Join queue emits HomeView')
}
</script>

<template>
    <div v-if="!authStore.isAuthenticated">
        <VToolbar>
            <template v-slot:append>
                <VBtn to="/auth/login">Sign In</VBtn>
                <VBtn to="/auth/registration">Sign Up</VBtn>
            </template>
        </VToolbar>
    </div>

    <div v-else>
        <VToolbar>
            <template v-slot:prepend>
                <VBtn>Profile</VBtn>
                <VBtn :active="isActiveQueues" @click="activeQueuesContent">Queues</VBtn>
            </template>

            <template v-slot:append>
                <VBtn :active="isActiveSettings" @click="activeSettingsContent">Settings</VBtn>
                <VBtn @click="userLogout">Log Out</VBtn>
            </template>
        </VToolbar>

        <div v-if="isActiveQueues">
            <VContainer fluid>
                <VRow>
                    <VCol
                    cols="2"
                    >
                        <QueueComponent
                        @queue:create="queueCreate"
                        @queue:connect="queueConnect"
                        @queue:join="queueJoin"
                        ></QueueComponent>
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
        </div>

        <div v-else-if="isActiveSettings">
            <VContainer fluid>
                <VRow>
                    <VCol>Settings</VCol>
                </VRow>
            </VContainer>
        </div>
    </div>
</template>

<style scope>
</style>
