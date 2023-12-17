<script setup>
import { ref } from 'vue';

import QueueComponent from '../components/QueueComponent.vue'
import ContentComponent from '../components/ContentComponent.vue';
import HistoryComponent from '../components/HistoryComponent.vue'
</script>

<template>
    <VContainer fluid>
        <VRow>
            <VCol cols="2">
                <QueueComponent />
            </VCol>

            <VCol cols="7">
                <ContentComponent />
            </VCol>

            <VCol cols="3">
                <HistoryComponent />
            </VCol>
        </VRow>
    </VContainer>
</template>

<style scope>
</style>
