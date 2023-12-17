import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';
import vuetify  from './vuetify';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(vuetify);

import { useAuthStore } from './pinia/auth-store';
const authStore = useAuthStore();
authStore.setAuthStore();

app.mount('#app');
