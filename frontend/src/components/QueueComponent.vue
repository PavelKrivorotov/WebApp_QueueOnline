<script setup>
import { ref, onMounted } from 'vue';

import { useAuthStore } from '../pinia/auth-store';
import { useQueueStore } from '../pinia/queue-store';
import { useQueueUserStore } from '../pinia/queue-user-store';

import QueueCreateDialog from './dialogs/QueueCreateDialog.vue';
import QueueSearchDialog from './dialogs/QueueSearchDialog.vue';

const authStore = useAuthStore();
const queueStore = useQueueStore();
const queueUserStore = useQueueUserStore();

const isActiveQueueCreateDialog = ref(false);
const isActiveQueueSearchDialog = ref(false);

function queueCreateDialogClickOk() {
    isActiveQueueCreateDialog.value = false;
}

function queueCreateDialogClickClose() {
    isActiveQueueCreateDialog.value = false;
}

function queueCreateDialogComplete(response) {
    queueStore.createQueue(response.data)
}

function queueCreateDialogError() {}

function queueSearchDialogClickOk() {
    isActiveQueueSearchDialog.value = false;
}

function queueSearchDialogClickClose() {
    isActiveQueueSearchDialog.value = false;
}

function queueSearchDialogComplete(response) {
    queueStore.searchQueue(response.data)
}

function queueSearchDialogError() {}

onMounted(() => {
    queueStore.setQueueList();
});
</script>


<template>
    <VCard>
        <VCardTitle>Queues</VCardTitle>
        <VDivider></VDivider>

        <VVirtualScroll
        :items="queueStore['queueList']"
        >
            <template v-slot:default="{ item }">
                <VListItem
                >
                    <template v-slot:title>
                        {{ item.title }}
                    </template>

                    <template v-slot:subtitle>
                        {{ item.key }}
                    </template>

                    <template v-slot:append>
                        <VTooltip
                        text="Connect"
                        location="bottom"
                        >
                            <template v-slot:activator=" { props }">
                                <VBtn
                                icon
                                v-bind="props"
                                size="x-small"
                                @click="queueUserStore.setQueueConnect(item)"
                                >
                                    <VIcon>mdi-login</VIcon>
                                </VBtn>
                            </template>
                        </VTooltip>
                    </template>
                </VListItem>
            </template>
        </VVirtualScroll>
    </VCard>

    <VCard>
        <VCardTitle>Options</VCardTitle>
        <VDivider></VDivider>

        <VList>
            <VListItem
            prepend-icon="mdi-plus"
            @click="isActiveQueueCreateDialog = true"
            >
                Create
            </VListItem>

            <VListItem
            prepend-icon="mdi-magnify"
            @click="isActiveQueueSearchDialog = true"
            >
                Search
            </VListItem>
        </VList>
    </VCard>

    <QueueCreateDialog
    :is-active="isActiveQueueCreateDialog"
    @click:ok="queueCreateDialogClickOk"
    @click:close="queueCreateDialogClickClose"
    @complete="queueCreateDialogComplete"
    @error="queueCreateDialogError"
    ></QueueCreateDialog>

    <QueueSearchDialog
    :is-active="isActiveQueueSearchDialog"
    @click:ok="queueSearchDialogClickOk"
    @click:close="queueSearchDialogClickClose"
    @complete="queueSearchDialogComplete"
    @error="queueSearchDialogError"
    ></QueueSearchDialog>
</template>

<style scope>
</style>
