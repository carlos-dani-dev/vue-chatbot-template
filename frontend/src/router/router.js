import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import Login from '@/components/login/Login.vue'
import Signup from '@/components/login/Signup.vue'
import Chat from '@/components/home/Chat.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: "/login", component: Login},
    {path: "/signup", component: Signup},
    {path: "/chats/:chatId?", component: Chat}
  ]
})

router.beforeEach(async (to, from) => {
  const authStore = useAuthStore()
  if (
    !authStore.isAuthenticated &&
    to.path !== '/login' &&
    to.path !== '/signup'
  ) {
    return { path: '/login' }
  }
})

export default router;