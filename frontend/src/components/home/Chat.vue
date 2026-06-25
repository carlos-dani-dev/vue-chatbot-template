<script setup>
    import { ref, computed, onMounted, watch, nextTick, defineEmits } from "vue";
    import { useRoute, useRouter } from "vue-router";

    import SideBarMenu from '@/components/layout/SideBarMenu.vue';
    import ProfileMenu from "@/components/layout/ProfileMenu.vue";

    import SendMessageIcon from "@/assets/icons/send-message-icon.svg?component"
    import WCTrophyIcon from '@/assets/icons/wc-trophy-icon.svg?component'
    import ProfileIcon from "@/assets/icons/profile_icon.svg?component"
    import Message from "@/components/home/Message.vue"
    import { createChat } from "@/services/chat_session";
    import { sendChatMessage } from "@/services/chat_messages";
    import { useChatSessionsStore } from "@/stores/chat_session_store";
    import { useChatMessagesStore } from "@/stores/chat_messages_store";

    const route = useRoute();
    const router = useRouter();
    const chatId = computed(() => route.params.chatId);
    const sideBarMenuOpen = ref(false);
    const profileMenuOpen = ref(false);
    
    const sessionsStore = useChatSessionsStore();
    const messagesStore = useChatMessagesStore();

    const isLoading = ref(false)
    const messages = computed(() => messagesStore.currentMessages(chatId.value));

    async function load_chat_messages(){
        await messagesStore.loadMessages(chatId.value);    
    }
    
    onMounted(load_chat_messages);
    watch(chatId, load_chat_messages);
    
    const chatMessagesRef = ref(null);

    function scrollToBottom(){
        if (chatMessagesRef.value){
            chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight;
        }
    }

    const messageContent = ref("")
    async function send_message_(){
        
        if(!messageContent.value.trim()) return
        
        const content = messageContent.value;
        messageContent.value = "";

        try{
            let currentChatId = chatId.value;

            const channel = "web";
            const title = content.slice(0,30);

            if (!currentChatId){
                const newChat = await createChat(title, channel);
                currentChatId = newChat.id;
                console.log(newChat.title);
                sessionsStore.addSessions(newChat);
                router.replace(`/chats/${currentChatId}`)
            }
            
            const system_prompt = "Você é um especialista e por isso deve ser breve, porém assertivo, em sua resposta.";
            const model = "llama3.2:3b";

            messagesStore.addMessage(currentChatId, {"role": "user", "content": content})            
            isLoading.value = true;

            await nextTick();
            scrollToBottom();

            const response = await sendChatMessage(currentChatId, content, model, system_prompt);
            messagesStore.addMessage(currentChatId, response.assistant_message);
            isLoading.value = false;
            messageContent.value = "";

            await nextTick();
            scrollToBottom();
        }catch(error){
            console.log(error.messages);
            messageContent.value = content;
            isLoading.value = false;

            await nextTick();
            scrollToBottom();
        }
    }

</script>

<template>
    <SideBarMenu v-model:sideBarMenuOpen="sideBarMenuOpen"></SideBarMenu>
    
    <div class="flex flex-col h-screen relative">
        
        <button class="open-menu-btn fixed left-5" @click="sideBarMenuOpen = true">
            <WCTrophyIcon class="wc-trophy-icon"></WCTrophyIcon>
        </button>

        <div ref="chatMessagesRef" class="chat-messages overflow-y-auto flex-1 flex flex-col w-full items-center mt-2">
            
            <ul v-if="messages.length" class="flex flex-col w-3/5 gap-2 flex-1">
                
                <li v-for="message in messages" :key="message.id" :class="message.role == 'user' ? 'pl-40' : 'pr-40'" class="w-full">
                    <Message :messageRole="message.role" :messageContent="message.content" :class="message.role == 'user' ? 'bg-blue-900': 'bg-gray-900'"
                     class="text-base font-semibold text-gray-900"></Message>
                </li>
                
                <li v-if="isLoading" class="w-full pr-10 py-2 flex justify-start">
                    <div class="loader"></div>
                </li>
            </ul>

            <div v-else class="flex-1"></div>

            <div class="chat-text-input sticky bottom-0 mb-5 pt-2 flex w-full bg-white">
                <form @submit.prevent="send_message_" class="flex w-full justify-center items-center gap-2">
                    <input
                        :disabled="isLoading"
                        v-model="messageContent"
                        class="peer text-sm custom-input w-4/5 px-4 py-2 border border-gray-300 rounded-lg shadow-sm transition duration-300 ease-in-out transform focus:-translate-y-1 focus:outline-gray-300 hover:shadow-lg hover:border-gray-500 bg-gray-100"
                        placeholder="Pergunte qualquer coisa"
                        type="text"
                        id="unique-input"
                    />
                    
                    <button 
                        type="submit"
                        class="transition duration-300 ease-in-out transform peer-focus:-translate-y-1 text-gray-500 hover:text-gray-800 focus:outline-none"
                    >
                        <SendMessageIcon class="w-6 h-6"></SendMessageIcon>
                    </button>
                </form>
            </div>

        </div>

        <ProfileMenu v-model:profileMenuOpen="profileMenuOpen" class="fixed bottom-5 left-5 z-30"></ProfileMenu>
        <button class="open-profile-btn fixed bottom-5 left-5 z-10" @click.stop="profileMenuOpen = !profileMenuOpen">
            <ProfileIcon class="profile-icon"></ProfileIcon>
        </button>
    </div>
</template>

<style scoped>
.open-menu-btn, .open-profile-btn {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50px;
    width: 50px;
    cursor: pointer;
}

.wc-trophy-icon {
    width: 35px;
    height: 35px;
    flex-shrink: 0;
    color: rgba(107, 114, 128); 
    fill: currentColor;
    stroke: currentColor;
    transition: color 0.3s ease; 
}

.open-menu-btn:hover .wc-trophy-icon {
    color: black; 
}

.profile-icon {
    width: 40px;
    height: 40px;
    flex-shrink: 0;
    color: rgba(107, 114, 128); 
    fill: currentColor;
    stroke: currentColor;
    transition: color 0.3s ease; 
}

.open-profile-btn:hover .profile-icon {
    color: black;
}

.chat-text-input{
    background-color: transparent;
}

.loader {
  width: 30px;
  aspect-ratio: 4;
  background: radial-gradient(circle closest-side,#000 90%,#0000) 0/calc(100%/3) 100% space;
  clip-path: inset(0 100% 0 0);
  animation: l1 1s steps(4) infinite;
}
@keyframes l1 {to{clip-path: inset(0 -34% 0 0)}}

</style>