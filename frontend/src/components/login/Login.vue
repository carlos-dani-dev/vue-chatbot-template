<script setup>
    import WCTrophyIcon from '@/assets/icons/wc-trophy-icon.svg?component'
    import { ref } from 'vue';
    import { useAuthStore } from '@/stores/auth'
    import { signin } from '@/services/api'
    import router from '@/router/router';

    const authStore = useAuthStore() 

    const signinForm = ref({
        email: '',
        password: ''
    });

    const signin_ = async () => {
        try{
            const data = await signin(signinForm.value.email, signinForm.value.password)
            authStore.setAccessToken(data.access_token)
            router.push("/")
        } catch(error){
            console.log(error.message);
        }
    }

</script>

<template>
    <main class="flex items-center min-h-screen justify-center w-full px-4">
        <form @submit.prevent="signin_" id="signin-form" class="flex w-full flex-col max-w-96">

            <div class="flex items-center justify-center gap-20">
                <h2 class="text-3xl font-medium font-semibold text-gray-900">Sign in</h2>
                <a class="logo-a flex items-center">
                    <WCTrophyIcon class="wc-trophy-icon mb-5"></WCTrophyIcon>
                    <span class="font-semibold">WorldCup Chatbot</span>
                </a>
                
            </div>
            <p class="mt-4 text-base text-gray-500/90">
                Por favor, insira um email e uma senha para acessar.
            </p>

            <div class="mt-10">
                <label class="font-medium">Email</label>
                <input
                    v-model="signinForm.email"
                    placeholder="Insira seu email"
                    class="mt-2 rounded-md ring ring-gray-200 focus:ring-2 focus:ring-indigo-600 outline-none px-3 py-3 w-full"
                    required
                    type="email"
                    name="email"
                />
            </div>

            <div class="mt-6">
                <label class="font-medium">Senha</label>
                <input
                    v-model="signinForm.password"
                    placeholder="Insira sua senha"
                    class="mt-2 rounded-md ring ring-gray-200 focus:ring-2 focus:ring-indigo-600 outline-none px-3 py-3 w-full"
                    required
                    type="password"
                    name="password"
                />
            </div>

            <button
                type="submit"
                class="login-btn mt-8 py-3 w-full cursor-pointer rounded-md text-white"
            >
                Login
            </button>
            <p class='text-center py-8'>
                Ainda não possui uma conta? <router-link to="/signup" class="text-indigo-600 hover:underline">Registre-se</router-link>
            </p>
        </form>
    </main>
</template>

<style scoped>

.login-btn{
    background-color: rgb(62, 64, 69); 
    flex-shrink: 0;
    transition: all 0.3s ease; 
}
.login-btn:hover{
    background-color: black;
    color: white;
}

.wc-trophy-icon {
    flex-shrink: 0;
    fill: currentColor;
    stroke: currentColor;

    transition: all 0.3s ease; 
}

.logo-a:hover{
    color: rgb(102, 106, 117);
}

</style>