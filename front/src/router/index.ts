import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/jira-sync',
      name: 'jira-sync',
      component: () => import('../views/JiraSyncView.vue'),
    },
    {
      path: '/docs',
      name: 'documentation',
      component: () => import('../views/DocumentationView.vue'),
    },
  ],
})

export default router
