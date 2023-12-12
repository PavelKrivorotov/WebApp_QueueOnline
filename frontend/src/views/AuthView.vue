<script setup>
</script>

<template>
    <VToolbar>
        <template v-slot:append>
            <VBtn to="/auth/login">Sign In</VBtn>
            <VBtn to="/auth/registration">Sign Up</VBtn>
        </template>
    </VToolbar>

    <RouterView></RouterView>
</template>

<style scope>
</style>
