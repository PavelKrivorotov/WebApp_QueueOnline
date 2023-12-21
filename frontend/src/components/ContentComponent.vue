<script setup>
import { ref, watch, onMounted } from 'vue';

import * as settings from '../settings'
import { setLocalStorage } from '../localstorage'
import { useAuthStore } from '../pinia/auth-store';
import { useQueueStore } from '../pinia/queue-store';
import { useQueueUserStore } from '../pinia/queue-user-store';
import { useTableStore } from '../pinia/table-store';

import RoleComponent from './content-components/RoleComponent.vue';
import ConfirmDialog from './dialogs/ConfirmDialog.vue';
import ContentInfoDialog from './dialogs/ContentInfoDialog.vue';

const authStore = useAuthStore()
const queueStore = useQueueStore();
const queueUserStore = useQueueUserStore();
const tableStore = useTableStore();

const isActiveLeaveConfirmDialog = ref(false);
const isActiveInfoDialog = ref(false);

watch(
    () => queueUserStore['wsConnect'],
    (newConnect, oldConnect) => {
        console.log('watch worked in ContentComponent')

        // 
        // 
        if (oldConnect) {
            console.log('newConnect: ', newConnect)
            console.log('oldConnect: ', oldConnect)

            oldConnect.close();
            tableStore.clearTableItems();
        }
        // 


        queueUserStore['wsConnect'].onmessage = (event) => {
            const response = JSON.parse(event.data);
            console.log(response)
            // 
            switch (response['action']['action_key']) {
                // connect
                case 'QA00003':
                    setLocalStorage(
                        settings.LOCALSTORAGE['QUEUE_KEY'],
                        response['action']['queue_key']
                    );

                    queueUserStore['queueObject']['key'] = response['action']['queue_key'];
                    queueUserStore.setUserData(
                        queueUserStore.makeUserObject(response['user'])
                    )

                    tableStore.clearTableItems();
                    tableStore.setTableItems(response['users']);
                    break;
                
                // disconnect
                case 'QA00004':
                    break;

                // join
                case 'QA00005':
                    queueUserStore.setUserData(
                        queueUserStore.makeUserObject(response['user'])
                    )

                    queueStore.setQueueList();

                    tableStore.setTableItems(response['users']);
                    tableStore.refreshTableItems();
                    break;

                // leave
                case 'QA00006':
                    queueUserStore.setUserData(
                        queueUserStore.makeUserObject(response['user'])
                    );

                    queueStore.setQueueList();

                    tableStore.clearTableItems();
                    tableStore.setTableItems(response['users']);
                    break;

                // replace-offer
                case 'QA00007':
                    break;

                // replace-accept
                case 'QA00008':
                    break;

                // skip
                case 'QA00009':
                    queueUserStore.updateUserData(response['users']);

                    tableStore.clearTableItems();
                    tableStore.setTableItems(response['users']);
                    break;

                default:
                    break;
            }
        }

        queueUserStore['wsConnect'].onclose = (event) => {
            console.log('Close connect!', event);
        }
    }
)

function joinButtonClick() {
    queueUserStore['wsConnect'].send(
        JSON.stringify({
            action_key: 'QA00005'
        })
    );
}

function leaveButtonClick() {
    isActiveLeaveConfirmDialog.value = false;
    queueUserStore['wsConnect'].send(
        JSON.stringify({
            action_key: 'QA00006'
        })
    );
}

function swapButtonClick(item) {
    queueUserStore['wsConnect'].send(
        JSON.stringify({
            action_key: 'QA00009',
            passive_queue_user_id: item.userId,
        })
    );
}

onMounted(() => {
    queueUserStore.setQueueUserStore();
})
</script>

<template>
    <div v-if="queueUserStore['userObject']['role'] == 'QR00001'">
        <RoleComponent
        @click:swap="item => swapButtonClick(item)"
        @click:replace="item => console.log('replace (not member): ', item)"
        >
            <template v-slot:not-member>
                <VBtn @click="isActiveInfoDialog = true">Info</VBtn>
                <VBtn @click="joinButtonClick">Join</VBtn>
            </template>
        </RoleComponent>
    </div>

    <div v-else-if="queueUserStore['userObject']['role'] == 'QR00002'">
        <RoleComponent
        @click:swap="item => swapButtonClick(item)"
        @click:replace="item => console.log('replace (member): ', item)"
        >
            <template v-slot:member>
                <VBtn @click="isActiveLeaveConfirmDialog = true">Leave</VBtn>
                <VBtn @click="isActiveInfoDialog = true">Info</VBtn>
                <VBtn>Actions</VBtn>
            </template>
        </RoleComponent>
    </div>

    <div v-else-if="queueUserStore['userObject']['role'] == 'QR00003'">
        <RoleComponent
        @click:swap="item => swapButtonClick(item)"
        @click:replace="console.log('replace (leader): ', item)"
        >
            <template v-slot:member>
                <VBtn @click="isActiveInfoDialog = true">Info</VBtn>
                <VBtn>Actions</VBtn>
            </template>
        </RoleComponent>
    </div>

    <ContentInfoDialog
    :is-active="isActiveInfoDialog"
    @click:close="isActiveInfoDialog = false"
    ></ContentInfoDialog>


    <ConfirmDialog
    :is-active="isActiveLeaveConfirmDialog"
    title="Queue leave"
    text="Do you want to leve the Queue?"
    @click:ok="leaveButtonClick"
    @click:close="isActiveLeaveConfirmDialog = false"
    ></ConfirmDialog>


    <p>Queue key: {{ queueUserStore['queueObject']['key'] }}</p>
    <p>Queue role: {{ queueUserStore['userObject']['role'] }}</p>
</template>

<style scope>
</style>
