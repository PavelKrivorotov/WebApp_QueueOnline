<script setup>
import { useRouter } from 'vue-router';

import { useAuthStore } from '../pinia/auth-store';
import { LOCALSTORAGE } from '../settings';
import { setLocalStorage } from '../localstorage';

import LoginForm from '../components/forms/LoginForm.vue';

const router = useRouter();
const authStore = useAuthStore();

function beforeRequest() {

}

function afterResponse(response) {
    console.log(response)

    const token = response.data['key'];
    authStore.isAuthenticated = true;
    authStore.authorizationToken = token;

    // 
    setLocalStorage(
        LOCALSTORAGE['AUTHORIZATION_TOKEN'],
        token
    )

    router.push({
        path: '/',
    });
}

function errorRequest(error) {
    console.log('Error in `LoginView`:')
    console.error(error)
}
</script>

<template>
    <VContainer>
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
