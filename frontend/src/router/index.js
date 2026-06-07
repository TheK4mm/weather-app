import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'

// Una sola vista por ahora; el router queda listo para escalar a más páginas.
const routes = [{ path: '/', name: 'home', component: HomeView }]

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})
