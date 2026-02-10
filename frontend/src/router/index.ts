import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue';
import RegisterView from '../views/RegisterView.vue';
import LoginView from '../views/LoginView.vue';
import SettingsView from '../views/SettingsView.vue';
import SkillsView from '../views/SkillsView.vue';
import JobView from '../views/JobView.vue';
import SourcesView from '../views/SourcesView.vue';
import AboutView from '../views/AboutView.vue';


const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/settings', name: 'settings', component: SettingsView },
  { path: '/skills', name: 'skills', component: SkillsView },
  { path: '/job/:id', name: 'job', component: JobView, props: true },
  { path: '/sources', name: 'sources', component: SourcesView },
  { path: '/about', name: 'about', component: AboutView },
]


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

export default router
