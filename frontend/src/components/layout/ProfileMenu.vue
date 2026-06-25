<script setup>
    import { defineProps, defineEmits, ref, computed, onMounted, onUnmounted } from 'vue';
    import { useAuthStore } from '@/stores/auth';
    import { useRouter } from 'vue-router';

    const authStore = useAuthStore();
    const router = useRouter();

    const props = defineProps(["profileMenuOpen"]);
    const emits = defineEmits(["update:profileMenuOpen"]);

    const menu = ref(null);
    const open = computed({
        get(){
            return props.profileMenuOpen;
        },
        set(value){
            emits("update:profileMenuOpen", value);
        }
    })

    const handleClickOutside = (event) => {
        // Se o menu estiver aberto E o elemento clicado NÃO estiver dentro da div
        if (open.value && menu.value && !menu.value.contains(event.target)) {
            open.value = false;
        }
    };

    onMounted(() =>{
        document.addEventListener('click', handleClickOutside);
    })
    onUnmounted(() =>{
        document.removeEventListener('click', handleClickOutside);
    })

    const sign_out_ = async () => {
        try{
            authStore.logout();
            router.push("/login");
        }catch(error){
            console.log(error.message);
        }
    }

 </script>


<template>
    <div v-if="open" ref="menu" class="bg-white border border-default-medium rounded-base shadow-lg w-44">
        <ul class="p-2 text-sm text-body font-medium" aria-labelledby="dropdownDelayButton">
            
            <li>
                <a href="#" class="inline-flex items-center w-full p-2 hover:bg-neutral-tertiary-medium hover:text-heading rounded">Settings</a>
            </li>
            <li>
                <a href="#" @click="sign_out_" class="inline-flex items-center w-full p-2 hover:bg-neutral-tertiary-medium hover:text-heading rounded">Sign out</a>
            </li>
        </ul>
    </div>
</template>