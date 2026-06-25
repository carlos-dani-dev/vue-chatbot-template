import { useAuthStore } from '@/stores/auth'
import { errorMessages } from 'vue/compiler-sfc'
import { fetchComAuth } from './api';

const BASE_URL = 'http://localhost:8000'

export const getUserSessions = async () =>{
    try{
        const response = await fetchComAuth('/chats');

        if(!response.ok){
            throw new Error(`Erro na requisição: ${response.status}`)
        }

        const sessoes = await response.json();
        return sessoes
    }catch(error){
        console.log(error.message)
    }
};

export const createChat = async (title, channel) =>{
    try{
        const response = await fetchComAuth('/chats/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: title,
                channel: channel,
                session_metadata: {
                    "additionalProp1": {}
                }
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
