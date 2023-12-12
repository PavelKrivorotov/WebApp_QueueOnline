import { createRouter, createWebHistory } from 'vue-router';

import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegistrationView from '../views/RegistrationView.vue';

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/',
			name: 'home-view',
			component: HomeView,
		},
		{
			path: '/auth',
			name: 'auth-view',
			redirect: {
				name: 'registartion-view',
			},
			children: [
				{
					path: 'registration/',
					name: 'registartion-view',
					component: RegistrationView,
				},
				{
					path: 'login/',
					name: 'login-view',
					component: LoginView,
				},
			]
		},
	]
})

export default router
