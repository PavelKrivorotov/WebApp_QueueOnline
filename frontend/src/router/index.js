import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../pinia/auth-store'

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

			beforeEnter: (to, from) => {
				const authStore = useAuthStore()
				if (!authStore['isAuthenticated']) {
					return { name: 'login-view' }
				}
			}
		},
		{
			path: '/auth',
			name: 'auth-view',
			redirect: {
				name: 'login-view',
			},
			children: [
				{
					path: 'login/',
					name: 'login-view',
					component: LoginView,
				},
				{
					path: 'registration/',
					name: 'registartion-view',
					component: RegistrationView,
				},
			]
		},
	]
})

export default router
