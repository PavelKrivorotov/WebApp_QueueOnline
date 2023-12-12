<script setup>
import { ref } from 'vue';

const historyItems = ref([
    {
        id: 1,
        action: 'connect',
        describtion: 'User `1-???` connecting!'
    },
    {
        id: 2,
        action: 'connect',
        describtion: 'User `2-???` connecting!'
    },
    {
        id: 3,
        action: 'offered-replace',
        describtion: 'User `1-???`offered to change placees with User `2-???`'
    },
    {
        id: 4,
        action: 'replace',
        describtion: 'User `1-???` replace with User `2-???`'
    },
]);

</script>

<template>
    <VCard>
        <VCardTitle>History</VCardTitle>

        <VCardText>
            <VVirtualScroll
            :items="historyItems"
            >
                <template v-slot:default="{ item }">
                    <!-- <VAlert
                    :title="`${item.id}-${item.action}`"
                    :text="item.describtion"
                    class="mb-2"
                    ></VAlert> -->

                    <p>Title: {{ item.title }}. Describtion: {{ item.describtion }}</p>
                    <br>
                </template>
            </VVirtualScroll>
        </VCardText>
    </VCard>
</template>

<style scope>
</style>
