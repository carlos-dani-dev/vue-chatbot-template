import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        accessToken: localStorage.getItem('access_token') || null,
        user: null
    }),
    getters: {
        isAuthenticated: (state) => !!state.accessToken
    },
    actions: {
        setAccessToken(token) {
            this.accessToken = token
            localStorage.setItem('access_token', token)
        },
        setUser(user) {
            this.user = user
        },
        logout() {
            this.accessToken = null
            this.user = null
            localStorage.removeItem('access_token')
        }
    }
})