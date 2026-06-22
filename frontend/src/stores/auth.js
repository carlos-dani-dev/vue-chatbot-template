import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        accessToken: null,
        user: null
    }),
    getters: {
        isAuthenticated: (state) => !!state.accessToken
    },
    actions: {
        setAccessToken(token) {
            this.accessToken = token
        },
        setUser(user) {
            this.user = user
        },
        logout() {
            this.accessToken = null
            this.user = null
        }
    }
})