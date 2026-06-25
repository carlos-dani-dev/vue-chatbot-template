import { useAuthStore } from '@/stores/auth'
import { errorMessages } from 'vue/compiler-sfc'
import { fetchComAuth } from './api';

const BASE_URL = 'http://localhost:8000'

export const getChatMessages = async (chatId) =>{
    try{
        const response = await fetchComAuth(`/chats/${chatId}/messages`);

        if(!response.ok){
            throw new Error(`Erro na requisição: ${response.status}`)
        }

        const sessoes = await response.json();
        return sessoes
    }catch(error){
        console.log(error.message)
    }
};


export const sendChatMessage = async (chatId, content, model, system_prompt) =>{
    try{
        const response = await fetchComAuth(`/chats/${chatId}/messages`,  {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: content,
                model: model,
                system_prompt: system_prompt
            })
        })

        if(!response.ok){
            throw new Error(`Erro na requisição: ${response.status}`)
        }

        return await response.json();

    }catch(error){
        console.log(error.message)
    }
};