<script setup>
import { useQueueUserStore } from '../../pinia/queue-user-store';
import { useTableStore } from '../../pinia/table-store';

const emits = defineEmits([
    'click:swap',
    'click:replace',
]);

const queueUserStore = useQueueUserStore();
const tableStore = useTableStore();
</script>

<template>
    <VCard>
        <VToolbar>
            <template v-slot:title>
                {{ queueUserStore['queueObject']['title'] }}
            </template>

            <template v-slot:append>
                <slot name="not-member"></slot>
                <slot name="member"></slot>
                <slot name="leader"></slot>
            </template>
        </VToolbar>
        
        <VCardText>
            <VDataTableVirtual
            :headers="tableStore['tableObject']['headers']"
            :items="tableStore['tableObject']['items']"
            height="300"
            >
                <template v-slot:item.action="{ item }">
                    <div v-if="item.userId != queueUserStore['userObject']['userId']">
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
                                @click="emits('click:swap', item)"
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
                                @click="emits('click:replace', item)"
                                >
                                    <VIcon>mdi-autorenew</VIcon>
                                </VBtn>
                            </template>
                        </VTooltip>

                        <slot name="action-append" v-bind="{ item }"></slot>
                    </div>
                </template>
            </VDataTableVirtual>
        </VCardText>
        
        <VToolbar
        density="compact"
        >
            <template v-slot:append>
                <div class="px-4">
                    <span class="text-button">Role: </span>
                    <span class="text-button">{{ queueUserStore['userObject']['role'] }}</span>
                </div>
                </template>
        </VToolbar>
    </VCard>
</template>

<style scope>
</style>
