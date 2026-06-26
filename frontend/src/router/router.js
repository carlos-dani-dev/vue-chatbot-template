import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import Login from '@/views/Login.vue'
import Signup from '@/views/Signup.vue'
import Chat from '@/views/Chat.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/login", component: Login },
    { path: "/signup", component: Signup },
    { path: "/chats/:chatId?", component: Chat },
    { path: "/", redirect: "/chats" },
    { path: "/:pathMatch(.*)*", component: Chat }
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