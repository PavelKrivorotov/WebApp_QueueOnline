<script setup>
import { useForm, useField } from 'vee-validate';

import { useAuthStore } from '../../pinia/auth-store'
import { queueRetrieve } from '../../http/requests';

const props = defineProps({
    'isActive': Boolean
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
    emits('click:ok')

    try {
        const response = await queueRetrieve(
            authStore['authorizationToken'],
            values.key
        )

        emits('complete', response)
    }
    catch (error) {
        console.log('Error in `QueueSearchDialog` -> submit')
        console.error(error)

        emits('error');
    }
});

const key = useField('key')
</script>

<template>
    <VDialog
    v-model="props.isActive"
    width="400"
    persistent
    >
        <VCard>
            <VToolbar
            rounded
            >
                <template v-slot:title>
                    Search Queue
                </template>

                <template v-slot:append>
                    <VBtn
                    icon="mdi-close"
                    @click="emits('click:close')"
                    ></VBtn>
                </template>
            </VToolbar>

            <VCardText>
                <VForm
                @submit="submit"
                >
                    <VTextField
                    label="Queue key"
                    v-model="key.value.value"
                    :error-messages="key.errorMessage.value"
                    ></VTextField>

                    <!-- <div class="d-flex justify-end">
                        <VBtn type="submit">Connect</VBtn>
                    </div> -->
                </VForm>
            </VCardText>

            <VCardActions>
                <VSpacer></VSpacer>
                <VBtn @click="submit">Connect</VBtn>
            </VCardActions>
        </VCard>
    </VDialog>
</template>

<style scope>
</style>
