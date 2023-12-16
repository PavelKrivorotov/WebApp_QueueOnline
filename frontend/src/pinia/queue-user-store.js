import { ref, reactive } from 'vue';
import { defineStore } from 'pinia';

import * as settings from '../settings'
import { getLocalStorage, removeLocalStorage } from '../localstorage'
import { useAuthStore } from './auth-store';
import { queueRetrieve } from '../http/requests'

export const useQueueUserStore = defineStore('queue-user-store', () => {
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

    function setQueueData(cleanQueue) {
        queueObject.key = cleanQueue.key;
        queueObject.title = cleanQueue.title;
        queueObject.created = cleanQueue.created;
        queueObject.lifetime = cleanQueue.lifetime;
        queueObject.state = cleanQueue.state;
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

    function setQueueConnect(cleanObject) {
        const authStore = useAuthStore();

        setWsConnect(
            authStore['authorizationToken'],
            cleanObject.key
        );
        setQueueData(cleanObject);
    }

    // async function setQueueStore() { 
    // setDefault()
    async function setQueueUserStore() {   
        const queueKey = getLocalStorage(settings.LOCALSTORAGE['QUEUE_KEY']);
        if (queueKey) {
            const authStore = useAuthStore();
            const queueUserStore = useQueueUserStore();
    
            try {
                const response = await queueRetrieve(
                    authStore['authorizationToken'],
                    queueKey
                );
                const queue = queueUserStore.makeQueueObject(response.data)
    
                queueUserStore.setWsConnect(
                    authStore['authorizationToken'],
                    queueKey
                );
                queueUserStore.setQueueData(queue);
            }
            catch (error) {
                removeLocalStorage(settings.LOCALSTORAGE['QUEUE_KEY'])
    
                console.log('error in `queue-store` -> setQueueStore')
                console.error(error)
            }
        }
    }

    return {
        wsConnect,
        queueObject,
        userObject,

        setWsConnect,
        makeQueueObject,
        setQueueData,
        makeUserObject,
        setUserData,
        updateUserData,
        setQueueConnect,

        setQueueUserStore,
    }
});
