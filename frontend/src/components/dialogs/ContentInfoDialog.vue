<script setup>
import { ref } from 'vue';
import { useQueueStore } from '../../pinia/queue-store';

const props = defineProps({
    isActive: Boolean,
});

const emits = defineEmits([
    'click:close'
]);

const queueStore = useQueueStore();
</script>

<template>
    <VDialog
    v-model="props.isActive"
    width="450"
    persistent
    rounded
    >
        <VCard>
            <VToolbar>
                <template v-slot:title>
                    Queue information
                </template>

                <template v-slot:append>
                    <VBtn icon="mdi-close" @click="emits('click:close')"></VBtn>
                </template>
            </VToolbar>
            
            <VCardText>
                <VForm>
                    <VTextField
                    label="Title"
                    v-model="queueStore['queueObject']['title']"
                    readonly
                    ></VTextField>

                    <VTextField
                    label="Key"
                    v-model="queueStore['queueObject']['key']"
                    readonly
                    ></VTextField>

                    <VTextField
                    label="Date of created"
                    v-model="queueStore['queueObject']['created']"
                    readonly
                    ></VTextField>

                    <VTextField
                    label="Lifetime"
                    v-model="queueStore['queueObject']['lifetime']"
                    readonly
                    ></VTextField>

                    <VTextField
                    label="Is active"
                    v-model="queueStore['queueObject']['state']"
                    readonly
                    ></VTextField>
                </VForm>
            </VCardText>
        </VCard>
    </VDialog>
</template>

<style style>
</style>
