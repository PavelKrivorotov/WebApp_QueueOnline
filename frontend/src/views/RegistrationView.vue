<script setup>
import { useRouter } from 'vue-router'

import { useAuthStore } from '../pinia/auth-store';
import { authLogin } from '../http/requests';

import RegistrationForm from '../components/forms/RegistrationForm.vue'

const authStore = useAuthStore();

function beforeRequest() {}
function errorRequest() {}
function afterResponse(response) {
    alert("Create user!");
}
</script>

<template>
    <VContainer class="fill-height" fluid>
        <VRow>
            <VCol>
                <RegistrationForm
                @beforeRequest="beforeRequest"
                @afterResponse="afterResponse"
                @errorRequest="errorRequest"
                ></RegistrationForm>
            </VCol>
        </VRow>
    </VContainer>
</template>

<style>
</style>
