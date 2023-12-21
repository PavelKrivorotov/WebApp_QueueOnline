<script setup>
import { useRouter } from 'vue-router';

import { useAuthStore } from '../pinia/auth-store';
import { LOCALSTORAGE } from '../settings';
import { setLocalStorage } from '../localstorage';

import LoginForm from '../components/forms/LoginForm.vue';

const router = useRouter();
const authStore = useAuthStore();

function beforeRequest() {}
function errorRequest(error) {
    console.log('Error in `LoginView`:')
    console.error(error)
}

function afterResponse(response) {
    authStore.authorizationComplete(response.data['key']);

    router.push({
        path: '/',
    });
}
</script>

<template>
    <VContainer class="fill-height" fluid>
        <VRow>
            <VCol>
                <LoginForm
                @beforeRequest="beforeRequest"
                @afterResponse="afterResponse"
                @errorRequest="errorRequest"
                ></LoginForm>
            </VCol>
        </VRow>
    </VContainer>
</template>

<style scope>
</style>
