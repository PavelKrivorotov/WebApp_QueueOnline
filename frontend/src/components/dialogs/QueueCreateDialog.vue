<script setup>
import { ref, onMounted } from 'vue';
import { useForm, useField } from 'vee-validate';

import { useAuthStore } from '../../pinia/auth-store';
import { queueLifetimes, queueCreate } from '../../http/requests'

const props = defineProps({
    isActive: Boolean
});

const emits = defineEmits([
    'click:ok',
    'click:close',
    'complete',
    'error',
]);

const authStore = useAuthStore();

const { handleSubmit } = useForm();
const submit = handleSubmit(async (values) => {
    emits('click:ok');

    try {
        const formData = new FormData()
        formData.append('title', values.title)
        formData.append('queue_lifetime_key', values.lifetime)

        const response = await queueCreate(
            authStore['authorizationToken'],
            formData
        );

        emits('complete', response);
    }
    catch (error) {
        console.log('Error in QueueCreateForm -> submit')
        console.error(error)

        emits('error');
    }
});

const lifetimeItems = ref([]);

const title = useField('title');
const lifetime = useField('lifetime');

function makeItemText(seconds) {
    return `${seconds / 60} minutes`;
}

async function setLifetimeItems() {
    try {
        const response = await queueLifetimes()
        response.data['results'].forEach(element => {
            lifetimeItems.value.push({
                value: element['key'],
                text: makeItemText(element['lifetime']),
            });
        });
    }
    catch (error) {
        console.log('Error in QueueCreateForm -> setLifetimes');
        console.error(error);
    }
}

onMounted(() => {
    setLifetimeItems();
});
</script>

<template>
    <VDialog
    v-model="props.isActive"
    width="400"
    persistent
    rounded
    >
        <VCard>
            <VToolbar
            rounded
            >
                <template v-slot:title>
                    Create Queue
                </template>
                
                <template v-slot:append>
                    <VBtn
                    icon="mdi-close"
                    @click="emits('click:close')"
                    >
                    </VBtn>
                </template>
            </VToolbar>

            <VCardText>
                <VForm
                @submit="submit"
                >
                    <VTextField
                    label="Title"
                    v-model="title.value.value"
                    :error-messages="title.errorMessage.value"
                    ></VTextField>

                    <VSelect
                    label="Lifetime"
                    v-model="lifetime.value.value"
                    :error-messages="lifetime.errorMessage.value"
                    :items="lifetimeItems"
                    item-title="text"
                    item-value="value"
                    ></VSelect>

                    <div class="d-flex justify-end">
                        <VBtn type="submit">Create</VBtn>
                    </div>
                </VForm>
            </VCardText>
        </VCard>
    </VDialog>
</template>

<style scope>
</style>
