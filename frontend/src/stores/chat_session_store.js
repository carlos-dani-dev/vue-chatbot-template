import { defineStore } from 'pinia'
import { getUserSessions } from '@/services/chat_session'


export const useChatSessionsStore = defineStore('chatSessions', {
    state: () => ({
        sessions: []
    }),
    actions: {
        async loadSessions(){
            const response = await getUserSessions();
            this.sessions = response.items;
        },
        async addSessions(session){
            this.sessions.unshift(session);
        }
    }
})