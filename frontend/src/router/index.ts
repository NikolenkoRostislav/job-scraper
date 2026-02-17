import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue';
import RegisterView from '@/views/RegisterView.vue';
import LoginView from '@/views/LoginView.vue';
import JobView from '@/views/JobView.vue';
import AboutView from '@/views/AboutView.vue';
import AdminView from '@/views/AdminView.vue';
import NotFoundView from '@/views/NotFoundView.vue';


const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/job/:id', name: 'job', component: JobView, props: true },
  { path: '/about', name: 'about', component: AboutView },
  { path : '/admin', name: 'admin', component: AdminView },
  { path: '/:catchAll(.*)', name: 'not found', component: NotFoundView}
]


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

export default router
