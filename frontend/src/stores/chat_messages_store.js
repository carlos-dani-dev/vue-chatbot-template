import { defineStore } from 'pinia'
import { getChatMessages, sendChatMessage } from '@/services/message'

export const useChatMessagesStore = defineStore('chatMessages', {
    state: () => ({
        messagesByChat: {} // { [chatId]: [ { id, role, content }, ... ] }
    }),
    getters: {
        currentMessages: (state) => (chatId) => state.messagesByChat[chatId] ?? []
    },
    actions: {
        async loadMessages(chatId) {
            if (!chatId) return
            const response = await getChatMessages(chatId)
            this.messagesByChat[chatId] = response.list_messages
        },
        addMessage(chatId, message) {
            if (!this.messagesByChat[chatId]) {
                this.messagesByChat[chatId] = []
            }
            this.messagesByChat[chatId].push(message)
        }
    }
})