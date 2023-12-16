import { ref } from 'vue'
import { defineStore } from 'pinia'

import { useAuthStore } from './auth-store';
import { useQueueUserStore } from './queue-user-store';
import { queueQueues } from '../http/requests'

export const useQueueStore = defineStore('queue-store', () => {
    const queueList = ref([]);

    async function setQueueList() {
        try {
            const authStore = useAuthStore();
            const queueUserStore = useQueueUserStore();

            const response = await queueQueues(
                authStore['authorizationToken']
            )

            // New
            queueList.value.splice(0, queueList.value.length);
            // 

            response.data['results'].forEach(element => {
                queueList.value.push(
                    queueUserStore.makeQueueObject(element)
                );
            });
        }
        catch (error) {
            console.log('error in `queue-store` -> setQueueList')
            console.error(error)
        }
    }

    function createQueue(rawQueue) {
        const queueUserStore = useQueueUserStore();

        const queue = queueUserStore.makeQueueObject(rawQueue);
        queueList.value.splice(0, 0, queue);
        queueUserStore.setQueueConnect(queue);
        setQueueList()
    }

    function searchQueue(rawQueue) {
        const queueUserStore = useQueueUserStore();

        const queue = queueUserStore.makeQueueObject(rawQueue);
        queueUserStore.setQueueConnect(queue);
    }

    return {
        queueList,
        
        setQueueList,
        createQueue,
        searchQueue,
    }
});
