<script setup>
import { ref, watch, onMounted } from 'vue';

import { useAuthStore } from '../pinia/auth-store';
import { useQueueStore , setQueueStore} from '../pinia/queue-store';
import { LOCALSTORAGE } from '../settings';
import { setLocalStorage } from '../localstorage'

import ConfirmDialog from './dialogs/ConfirmDialog.vue';
import ContentInfoDialog from './dialogs/ContentInfoDialog.vue';

const authStore = useAuthStore()
const queueStore = useQueueStore();

const isActiveLeaveConfirmDialog = ref(false);
const isActiveInfoDialog = ref(false);

const tableHeaders = ref([
    {
        title: 'position',
        key: 'position',
    },
    {
        title: 'user_id',
        key: 'userId',
    },
    {
        title: 'role',
        key: 'queueRole'
    },
    {
        title: 'action',
        key: 'action'
    }
]);
const tableItems = ref([])

watch(
    () => queueStore['wsConnect'],
    (newConnect, oldConnect) => {
        console.log('watch worked in ContentComponent')

        // 
        // 
        if (oldConnect) {
            console.log('newConnect: ', newConnect)
            console.log('oldConnect: ', oldConnect)

            oldConnect.close();
            tableItems.value.splice(0, tableItems.value.length);
        }
        // 


        queueStore['wsConnect'].onmessage = (event) => {
            const response = JSON.parse(event.data);
            console.log(response)
            // 
            switch (response['action']['action_key']) {
                // connect
                case 'QA00003':
                    // 
                    // setLocalQueueKey(response['action']['queue_key']);
                    setLocalStorage(
                        LOCALSTORAGE['QUEUE_KEY'],
                        response['action']['queue_key']
                    );

                    queueStore['queueObject']['key'] = response['action']['queue_key'];
                    queueStore.setUserData(
                        queueStore.makeUserObject(response['user'])
                    )

                    clearTableItems();
                    setTableItems(response['users']);
                    break;
                
                // disconnect
                case 'QA00004':
                    break;

                // join
                case 'QA00005':
                    queueStore.setUserData(
                        queueStore.makeUserObject(response['user'])
                    )
                    // queueStore.setDefaultQueueToList();
                    queueStore.setQueueList();

                    setTableItems(response['users']);
                    updateActionPermissions();
                    break;

                // leave
                case 'QA00006':
                    queueStore.setUserData(
                        queueStore.makeUserObject(response['user'])
                    )
                    // queueStore.removeDefaultQueueFromList();
                    queueStore.setQueueList();

                    clearTableItems();
                    setTableItems(response['users']);
                    break;

                // replace-offer
                case 'QA00007':
                    break;

                // replace-accept
                case 'QA00008':
                    break;

                // skip
                case 'QA00009':
                    queueStore.updateUserData(response['users']);
                    clearTableItems();
                    setTableItems(response['users']);
                    break;

                default:
                    break;
            }
        }

        queueStore['wsConnect'].onclose = (event) => {
            console.log('Close connect!', event);
        }
    }
)

function swapState(item) {
    if (queueStore['userObject']['position']) {
        if (item.position == queueStore['userObject']['position'] + 1) {
            return true;
        }
    }
    return false;
}

function replaceState(item) {
    if (queueStore['userObject']['position']) {
        if (item.position != queueStore['userObject']['position']) {
            return true;
        }
    }
    return false;
}

function joinButtonClick() {
    queueStore['wsConnect'].send(
        JSON.stringify({
            action_key: 'QA00005'
        })
    );
}

function leaveButtonClick() {
    isActiveLeaveConfirmDialog.value = false;
    queueStore['wsConnect'].send(
        JSON.stringify({
            action_key: 'QA00006'
        })
    );
}

function skipButtonClick(item) {
    queueStore['wsConnect'].send(
        JSON.stringify({
            action_key: 'QA00009',
            passive_queue_user_id: item.userId,
        })
    );
}

function clearTableItems() {
    tableItems.value.splice(0, tableItems.value.length)
}

function setTableItems(items) {
    items.forEach(element => {
        const clearElement = queueStore.makeUserObject(element);
        tableItems.value.push(
            makeTableItem(clearElement)
        );
    });
}

// 
function updateActionPermissions() {
    tableItems.value.forEach(element => {
        element.actionPermissions.swap = swapState(element);
        element.actionPermissions.replace = replaceState(element);
    });
}
// 

function makeTableItem(clearElement) {
    return {
        position: clearElement['position'],
        userId: clearElement['userId'],
        queueRole: clearElement['role'],
        action: null,
        actionPermissions: {
            swap: swapState(clearElement),
            replace: replaceState(clearElement),
        }
    }
}

onMounted(() => {
    setQueueStore();
})
</script>

<template>
    <div v-if="queueStore['userObject']['role'] == 'QR00001'">
    <!-- <div v-if="true"> -->
        <VCard>
            <VToolbar>
                <template v-slot:title>
                    {{ queueStore['queueObject']['title'] }}
                </template>

                <template v-slot:append>
                    <VBtn @click="isActiveInfoDialog = true">Info</VBtn>
                    <VBtn @click="joinButtonClick">Join</VBtn>
                </template>
            </VToolbar>

            <VCardText>
                <VDataTableVirtual
                :headers="tableHeaders"
                :items="tableItems"
                height="300"
                ></VDataTableVirtual>

                <VBtn>Not Member</VBtn>
            </VCardText>

            <VToolbar
            density="compact"
            >
                <template v-slot:append>
                    <div class="px-4">
                        <span class="text-button">Role: </span>
                        <span class="text-button">Not Member ({{ queueStore['userObject']['role'] }})</span>
                    </div>
                </template>
            </VToolbar>
        </VCard>
    </div>

    <div v-else-if="queueStore['userObject']['role'] == 'QR00002'">
    <!-- <div v-else-if="true"> -->
        <VCard>
            <VToolbar>
                <template v-slot:title>
                    {{ queueStore['queueObject']['title'] }}
                </template>

                <template v-slot:append>
                    <!-- <VBtn @click="leaveButtonClick">Leave</VBtn> -->
                    <VBtn @click="isActiveLeaveConfirmDialog = true">Leave</VBtn>
                    <ConfirmDialog
                    :is-active="isActiveLeaveConfirmDialog"
                    title="Queue leave"
                    text="Do you want to leve the Queue?"
                    @click:ok="leaveButtonClick"
                    @click:close="isActiveLeaveConfirmDialog = false"
                    ></ConfirmDialog>

                    <VBtn @click="isActiveInfoDialog = true">Info</VBtn>
                    <VBtn>Actions</VBtn>
                </template>
            </VToolbar>

            <VCardText>
                <VDataTableVirtual
                :headers="tableHeaders"
                :items="tableItems"
                height="300"
                >
                    <template v-slot:item.action="{ item }">
                        <div v-if="item.userId != queueStore['userObject']['userId']">
                            <VTooltip
                            text="Swap"
                            location="bottom"
                            >
                                <template v-slot:activator="{ props }">
                                    <VBtn
                                    icon
                                    size="x-small"
                                    :disabled="!item.actionPermissions.swap"
                                    v-bind="props"
                                    @click="skipButtonClick(item)"
                                    class="mr-2"
                                    >
                                        <VIcon>mdi-swap-vertical</VIcon>
                                    </VBtn>
                                </template>
                            </VTooltip>

                            <VTooltip
                            text="Replace"
                            location="bottom"
                            >
                                <template v-slot:activator="{ props }">
                                    <VBtn
                                    icon
                                    size="x-small"
                                    :disabled="!item.actionPermissions.replace"
                                    v-bind="props"
                                    >
                                        <VIcon>mdi-autorenew</VIcon>
                                    </VBtn>
                                </template>
                            </VTooltip>
                        </div>
                    </template>
                </VDataTableVirtual>

                <VBtn>Member</VBtn>
            </VCardText>

            <VToolbar
            density="compact"
            >
                <template v-slot:append>
                    <div class="px-4">
                        <span class="text-button">Role: </span>
                        <span class="text-button">Member ({{ queueStore['userObject']['role'] }})</span>
                    </div>
                </template>
            </VToolbar>
        </VCard>
    </div>

    <div v-else-if="queueStore['userObject']['role'] == 'QR00003'">
        <VCard>
            <VToolbar>
                <template v-slot:title>
                    {{ queueStore['queueObject']['title'] }}
                </template>

                <template v-slot:append>
                    <VBtn @click="leaveButtonClick">Leave</VBtn>
                    <VBtn @click="isActiveInfoDialog = true">Info</VBtn>
                    <VBtn>Actions</VBtn>
                </template>
            </VToolbar>

            <VCardText>
                <VDataTableVirtual
                :headers="tableHeaders"
                :items="tableItems"
                height="300"
                >
                    <template v-slot:item.action="{ item }">
                        <div v-if="item.userId != queueStore['userObject']['userId']">
                            <VTooltip
                            text="Swap"
                            location="bottom"
                            >
                                <template v-slot:activator="{ props }">
                                    <VBtn
                                    icon
                                    size="x-small"
                                    :disabled="!item.actionPermissions.swap"
                                    v-bind="props"
                                    @click="skipButtonClick(item)"
                                    class="mr-2"
                                    >
                                        <VIcon>mdi-swap-vertical</VIcon>
                                    </VBtn>
                                </template>
                            </VTooltip>

                            <VTooltip
                            text="Replace"
                            location="bottom"
                            >
                                <template v-slot:activator="{ props }">
                                    <VBtn
                                    icon
                                    size="x-small"
                                    :disabled="!item.actionPermissions.replace"
                                    v-bind="props"
                                    >
                                        <VIcon>mdi-autorenew</VIcon>
                                    </VBtn>
                                </template>
                            </VTooltip>
                        </div>
                    </template>
                </VDataTableVirtual>

                <VBtn>Leader</VBtn>
            </VCardText>

            <VToolbar
            density="compact"
            >
                <template v-slot:append>
                    <div class="px-4">
                        <span class="text-button">Role: </span>
                        <span class="text-button">Leader ({{ queueStore['userObject']['role'] }})</span>
                    </div>
                </template>
            </VToolbar>
        </VCard>
    </div>

    <ContentInfoDialog
    :is-active="isActiveInfoDialog"
    @click:close="isActiveInfoDialog = false"
    ></ContentInfoDialog>

    <p>Queue key: {{ queueStore['queueObject']['key'] }}</p>
    <p>Queue role: {{ queueStore['userObject']['role'] }}</p>
</template>

<style scope>
.user-row {
    color: red;
    background-color: green;
}
</style>
