<script setup>
import { ref } from 'vue';
// import { useQueueStore } from '../../pinia/queue-store';
import { useQueueUserStore } from '../../pinia/queue-user-store';

const props = defineProps({
    isActive: Boolean,
});

const emits = defineEmits([
    'click:close'
]);

const queueUserStore = useQueueUserStore();
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
                    v-model="queueUserStore['queueObject']['title']"
                    readonly
                    ></VTextField>

                    <VTextField
                    label="Key"
                    v-model="queueUserStore['queueObject']['key']"
                    readonly
                    ></VTextField>

                    <VTextField
                    label="Date of created"
                    v-model="queueUserStore['queueObject']['created']"
                    readonly
                    ></VTextField>

                    <VTextField
                    label="Lifetime"
                    v-model="queueUserStore['queueObject']['lifetime']"
                    readonly
                    ></VTextField>

                    <VTextField
                    label="Is active"
                    v-model="queueUserStore['queueObject']['state']"
                    readonly
                    ></VTextField>
                </VForm>
            </VCardText>
        </VCard>
    </VDialog>
</template>

<style style>
</style>
