<script setup>
    import { ref, computed } from 'vue';
    import { signup } from '@/services/api'
    import router from '@/router/router';

    const pwdConfirmation = ref('');
    const signupForm = ref({
        email: '',
        username: '',
        password: '',
        role: 'user'
    });

    const pwdMatch = computed(() => {
        return signupForm.value.password === pwdConfirmation.value// && signupForm.value.password !== ''
    })

    const signUp = async () => {
        try{
            const data = await signup(signupForm.value.email, signupForm.value.username, signupForm.value.password, signupForm.value.role)
            router.push("/login")
        }catch(error){
            console.log(error.message)
        }
    }


</script>

<template>
    <main class="flex items-center min-h-screen justify-center w-full px-4">
        <form @submit.prevent="signUp" id="signup-form" class="flex w-full flex-col max-w-96">
            
            <div class="flex items-center justify-center gap-20">
                <h2 class="text-3xl font-medium font-semibold text-gray-900">Sign up</h2>               
            </div>
            <p class="mt-1 text-base text-gray-500/90">
                Por favor, finalize o cadastro para acessar.
            </p>

            <div class="mt-5">
                <div class="">
                    <label class="font-medium">Email</label>
                    <input
                        v-model="signupForm.email"
                        placeholder="Insira seu email"
                        class="mt-2 rounded-md ring ring-gray-200 focus:ring-2 focus:ring-indigo-600 outline-none px-3 py-3 w-full"
                        required
                        type="email"
                        name="email"
                    />
                </div>

                <div class="mt-5">
                    <label class="font-medium">Nome de usuário</label>
                    <input
                        v-model="signupForm.username"
                        placeholder="Insira seu nome de usuário"
                        class="mt-2 rounded-md ring ring-gray-200 focus:ring-2 focus:ring-indigo-600 outline-none px-3 py-3 w-full"
                        required
                        type="text"
                        name="username"
                    />
                </div>

                <div class="mt-5">
                    <label class="font-medium">Senha</label>
                    <input
                        v-model="signupForm.password"
                        placeholder="Insira sua senha"
                        class="mt-2 rounded-md ring ring-gray-200 focus:ring-2 focus:ring-indigo-600 outline-none px-3 py-3 w-full"
                        required
                        type="password"
                        name="password"
                    />
                </div>

                <div class="mt-2">
                    <label class="txt-sm font-medium font-semibold text-gray-600">Confirme sua senha</label>
                    <input
                        v-model ="pwdConfirmation"
                        placeholder="Confirme sua senha"
                        class="rounded-md ring ring-gray-200 focus:ring-2 focus:ring-indigo-600 outline-none px-3 py-3 w-full"
                        required
                        type="password"
                        name="confirm-password"
                    />
                </div>
            </div>
            <p v-if="!pwdMatch" style="color: red">As senhas não coincidem</p>

            <button
                type="submit"
                :disabled="!pwdMatch"
                class="login-btn mt-8 py-3 w-full cursor-pointer rounded-md text-white"
            >
                Registrar-se
            </button>
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
</style>