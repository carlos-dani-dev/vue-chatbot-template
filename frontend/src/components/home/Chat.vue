<script setup>
    import { ref, computed, onMounted, watch } from "vue";
    import { useRoute, useRouter } from "vue-router";

    import SideBarMenu from '@/components/layout/SideBarMenu.vue';
    import SendMessageIcon from "@/assets/icons/send-message-icon.svg?component"
    import ProfileIcon from "@/assets/icons/profile_icon.svg?component"
    import Message from "@/components/home/Message.vue"
    import { createChat } from "@/services/chat_session";
    import { useChatSessionsStore } from "@/stores/chat_session_store";
    import { useChatMessagesStore } from "@/stores/chat_messages_store";

    const route = useRoute();
    const router = useRouter();
    const chatId = computed(() => route.params.chatId);
    
    const sessionsStore = useChatSessionsStore();
    const messagesStore = useChatMessagesStore();

    const isLoading = ref(false)
    const messages = computed(() => messagesStore.currentMessages(chatId.value));

    async function load_chat_messages(){
        await messagesStore.loadMessages(chatId.value);    
    }
    
    onMounted(load_chat_messages);
    watch(chatId, load_chat_messages);
    
    const messageContent = ref("")
    async function send_message_(){
        
        if(!messageContent.value.trim()) return
        
        const content = messageContent.value;
        messageContent.value = "";

        try{
            let currentChatId = chatId.value;

            const channel = "web";
            const title = "";

            if (!currentChatId){
                const newChat = await createChat(title, channel);
                currentChatId = newChat.id;
                sessionsStore.addSessions(newChat);
                router.replace(`/chats/${currentChatId}`)
            }
            
            const system_prompt = "Você é um especialista e por isso deve ser breve, porém assertivo, em sua resposta.";
            const model = "llama3.2:3b";

            messagesStore.addMessage(currentChatId, {"role": "user", "content": content})            
            isLoading.value=true;
            const response = await sendChatMessage(currentChatId, content, model, system_prompt);
            messagesStore.addMessage(currentChatId, response.assistant_message);
            isLoading.value=false;
            messageContent.value = "";
        }catch(error){
            console.log(error.messages);
            messageContent.value = content;
        }
    }

</script>

<template>
    <SideBarMenu class="fixed"></SideBarMenu>
    <div class="flex flex-col h-screen justify-center ">

        <div class="chat-messages overflow-y-auto flex w-full justify-center mt-2">
            <ul class="flex flex-col w-3/5 gap-2">
                
                <li v-for="message in messages" :key="message.id" :class="message.role == 'user' ? 'pl-40' : 'pr-40'" class="w-full">
                    <Message :messageRole="message.role" :messageContent="message.content" :class="message.role == 'user' ? 'bg-blue-900': 'bg-gray-900'"
                     class="text-base font-semibold text-gray-900"></Message>
                </li>
                
                <li v-if="isLoading" class="w-full pr-10 py-2 flex justify-start">
                    <div class="loader"></div>
                </li>

            </ul>
        </div>
        
        <div class="chat-text-input mb-5 flex w-full">
            <ProfileIcon class=" absolute ml-5"></ProfileIcon>
            <form @submit.prevent="send_message_" class="flex w-full justify-center items-center gap-2">
                <input
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
</template>

<style scoped>

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