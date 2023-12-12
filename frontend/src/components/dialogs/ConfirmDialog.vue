<script setup>
const props = defineProps({
    isActive: Boolean,
    title: {
        type: String,
        default: 'Confirm dialog title'
    },
    text: {
        type: String,
        default: 'Confirmation dialog text'
    }
});

const emits = defineEmits([
    'click:ok',
    'click:close'
]);
</script>

<template>
    <VDialog
    v-model="props.isActive"
    width="400"
    persistent
    >
        <VCard>
            <VToolbar>
                <template v-slot:title>
                    {{ props.title }}
                </template>

                <template v-slot:append>
                    <VBtn icon="mdi-close" @click="emits('click:close')"></VBtn>
                </template>
            </VToolbar>

            <VCardText>
                {{ props.text }}
            </VCardText>

            <VCardActions>
                <VSpacer></VSpacer>
                <VBtn @click="emits('click:ok')">Yes</VBtn>
                <VBtn @click="emits('click:close')">No</VBtn>
            </VCardActions>
        </VCard>
    </VDialog>
</template>

<style scoped>
</style>
