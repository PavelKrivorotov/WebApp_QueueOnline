import { ref, reactive } from 'vue'
import { defineStore } from 'pinia'

import { useAuthStore } from './auth-store';
import { LOCALSTORAGE } from '../settings';
import { getLocalStorage, removeLocalStorage } from '../localstorage'
import { queueQueues, queueRetrieve } from '../http/requests'

export const useQueueStore = defineStore('queue-store', () => {
    const wsConnect = ref(null);

    const queueObject = reactive({
        title: null,
        key: null,
        created: null,
        lifetime: null,
        state: null,
    });

    const userObject = reactive({
        position: null,
        userId: null,
        role: null,
    });

    const queueList = ref([]);

    function setWsConnect(token, queueKey) {
        wsConnect.value = new WebSocket(
            `ws://127.0.0.1:8000/queue/ws/${queueKey}?token=${token}`
        )

        wsConnect.value.onopen = (event) => {
            wsConnect.value.send(
                JSON.stringify({
                    action_key:'QA00003',
                })
            )

            console.log('onopen in queueStore')
        }
    }

    function setQueueData(cleanQueue) {
        queueObject.key = cleanQueue.key;
        queueObject.title = cleanQueue.title;
        queueObject.created = cleanQueue.created;
        queueObject.lifetime = cleanQueue.lifetime;
        queueObject.state = cleanQueue.state;
    }

    function makeQueueObject(rawQueue) {
        const element = {
            title: rawQueue['title'],
            key: rawQueue['key'],
            created: rawQueue['created'],
            lifetime: rawQueue['queue_lifetime_key'],
            state: rawQueue['is_active'],
        }
        return element;
    }

    function setUserData(cleanUser) {
        userObject.position = cleanUser.position;
        userObject.userId = cleanUser.userId;
        userObject.role = cleanUser.role;
    }

    function updateUserData(rawUsers) {
        let user = rawUsers.find(
            value => makeUserObject(value).userId == userObject.userId
        )
        userObject.position = makeUserObject(user).position
    }

    function makeUserObject(rawUser) {
        const element = {
            position: rawUser['position'],
            
            // userId: rawUser['user_id'],
            userId: rawUser['id'],

            role: rawUser['queue_role']
        }
        return element;
    }

    function setDefaultQueueToList() {
        queueList.value.splice(0, 0, queueObject)
    }

    function removeDefaultQueueFromList() {
        let index = queueList.value.findIndex(
            value => value.key == queueObject.key
        );
        queueList.value.splice(index, 1);
    }

    async function setQueueList() {
        try {
            const authStore = useAuthStore();

            const response = await queueQueues(
                authStore['authorizationToken']
            )

            // New
            queueList.value.splice(0, queueList.value.length);
            // 

            response.data['results'].forEach(element => {
                queueList.value.push(
                    makeQueueObject(element)
                );
            });
        }
        catch (error) {
            console.log('error in `queue-store` -> setQueueList')
            console.error(error)
        }
    }

    function setQueueConnect(cleanObject) {
        const authStore = useAuthStore();

        setWsConnect(
            authStore['authorizationToken'],
            cleanObject.key
        );
        setQueueData(cleanObject);
    }

    function createQueue(rawQueue) {
        const queue = makeQueueObject(rawQueue);
        // addQueueToHeadList(queue);
        queueList.value.splice(0, 0, queue);
        setQueueConnect(queue);
    }

    function searchQueue(rawQueue) {
        const queue = makeQueueObject(rawQueue);
        setQueueConnect(queue);
    }

    return {
        wsConnect,

        queueObject,
        userObject,

        queueList,

        setWsConnect,

        setQueueData,
        makeQueueObject,
        setUserData,
        updateUserData,
        makeUserObject,

        setDefaultQueueToList,
        removeDefaultQueueFromList,

        setQueueList,
        setQueueConnect,

        createQueue,
        searchQueue,
    }
});

export async function setQueueStore() {  
    const queueKey = getLocalStorage(LOCALSTORAGE['QUEUE_KEY']);
    if (queueKey) {
        const authStore = useAuthStore();
        const queueStore = useQueueStore();

        try {
            const response = await queueRetrieve(
                authStore['authorizationToken'],
                queueKey
            );
            const queue = queueStore.makeQueueObject(response.data)

            queueStore.setWsConnect(
                authStore['authorizationToken'],
                queueKey
            );
            queueStore.setQueueData(queue);
        }
        catch (error) {
            removeLocalStorage(LOCALSTORAGE['QUEUE_KEY'])

            console.log('error in `queue-store` -> setQueueStore')
            console.error(error)
        }
    }
}
