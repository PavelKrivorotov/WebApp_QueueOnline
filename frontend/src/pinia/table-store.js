import { reactive } from 'vue';
import { defineStore } from "pinia";

import { useQueueUserStore } from './queue-user-store';

export const useTableStore = defineStore('table-store', () => {
    const tableObject = reactive({
        headers: [
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
        ],
        items: [],
    });

    function swapState(userObject, item) {
        if (userObject['position']) {
            if (item.position == userObject['position'] + 1) {
                return true;
            }
        }
        return false;
    }

    function replaceState(userObject, item) {
        if (userObject['position']) {
            if (item.position != userObject['position']) {
                return true;
            }
        }
        return false;
    }

    function makeTableItem(userObject, clearElement) {
        return {
            position: clearElement['position'],
            userId: clearElement['userId'],
            queueRole: clearElement['role'],
            action: null,
            actionPermissions: {
                swap: swapState(userObject, clearElement),
                replace: replaceState(userObject, clearElement),
            }
        }
    }

    function clearTableItems() {
        tableObject.items.splice(0, tableObject.items.length)
    }

    function setTableItems(items) {
        const queueUserStore = useQueueUserStore();

        items.forEach(element => {
            const clearElement = queueUserStore.makeUserObject(element);
            tableObject.items.push(
                makeTableItem(queueUserStore['userObject'], clearElement)
            );
        });
    }

    // function updateActionPermissions() {
    function refreshTableItems() {
        const queueUserStore = useQueueUserStore();

        tableObject.items.forEach(element => {
            element.actionPermissions.swap = swapState(queueUserStore['userObject'], element);
            element.actionPermissions.replace = replaceState(queueUserStore['userObject'], element);
        });
    }

    return {
        tableObject,

        makeTableItem,
        clearTableItems,
        setTableItems,
        refreshTableItems,
    }
});
