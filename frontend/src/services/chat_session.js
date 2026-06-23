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