import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';
import vuetify  from './vuetify';

import { setAuthStore } from './pinia/auth-store';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(vuetify);

setAuthStore();

app.mount('#app');
