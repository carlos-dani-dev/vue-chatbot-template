<script setup>
    import { ref, onMounted } from 'vue'
    import { getUserSessions } from '@/services/chat_session'
    import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
    import { XMarkIcon } from '@heroicons/vue/24/outline'
    import TriondaIcon from '@/assets/icons/trionda_icon.svg?component'
    import WCTrophyIcon from '@/assets/icons/wc-trophy-icon.svg?component'
    import AddSession from '@/assets/icons/add-session.svg?component'
    import { useChatSessionsStore } from '@/stores/chat_session_store'

    const sessoes = ref();
    const sessionsStore = useChatSessionsStore();

    async function load_chat_session(){
        await sessionsStore.loadSessions();    
    }

    onMounted(load_chat_session);

    const open = ref(true)

</script>

<template>
    <div>
        <button class="open-menu-btn rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 hover:bg-sidebar-nav-hover" @click="open = true">
            <WCTrophyIcon class="wc-trophy-icon"></WCTrophyIcon>
            <span class="text-sm text-sidebar-nav-foreground">WorldCup Chatbot</span>
        </button>
        
        <TransitionRoot as="template" :show="open">
            <Dialog class="relative z-10" @close="open = false">
            <TransitionChild as="template" enter="ease-in-out duration-500" enter-from="opacity-0" enter-to="" leave="ease-in-out duration-500" leave-from="" leave-to="opacity-0">
                <div class="fixed inset-0 bg-gray-500/75 transition-opacity"></div>
            </TransitionChild>

            <div class="fixed inset-0 overflow-hidden">
                <div class="absolute inset-0 overflow-hidden">
                <div class="pointer-events-none fixed inset-y-0 left-0 flex max-w-full pr-10 sm:pr-16">
                    <TransitionChild as="template" enter="transform transition ease-in-out duration-500 sm:duration-700" enter-from="-translate-x-full" enter-to="translate-x-0" leave="transform transition ease-in-out duration-500 sm:duration-700" leave-from="translate-x-0" leave-to="-translate-x-full">
                    <DialogPanel class="pointer-events-auto relative w-screen max-w-md">
                        <TransitionChild as="template" enter="ease-in-out duration-500" enter-from="opacity-0" enter-to="" leave="ease-in-out duration-500" leave-from="" leave-to="opacity-0">
                        <div class="absolute top-0 right-0 -mr-8 flex pt-4 pl-2 sm:-mr-10 sm:pl-4">
                            <button type="button" class="relative rounded-md text-gray-300 hover:text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" @click="open = false">
                            <span class="absolute -inset-2.5"></span>
                            <span class="sr-only">Close panel</span>
                            <XMarkIcon class="size-6" aria-hidden="true" />
                            </button>
                        </div>
                        </TransitionChild>
                        <div class="relative flex h-full flex-col overflow-y-auto bg-white py-6 shadow-xl">
                            <div class="px-4 sm:px-6">
                                <DialogTitle class="text-base font-semibold text-gray-900">Sessões</DialogTitle>
                            </div>

                            <div class="group cursor-pointer">
                                
                                <router-link to="/chats" class="new-session-a w-full flex items-center justify-center gap-x-3.5 py-2 px-2.5 text-sm text-gray-500 group-hover:text-black transition-colors duration-200" href="#">
                                    <AddSession class="add-session-icon"></AddSession>
                                    <p class="text-sm font-semibold">Nova sessão</p>
                                </router-link>

                            </div>

                            <div class="relative mt-4 flex-1 px-4 sm:px-6">
                                <ul>
                                    <li v-for="sessao in sessionsStore.sessions" :key="sessao.id">
                                        <router-link :to="`/chats/${sessao.id}`" 
                                            class="sessions-a w-full flex items-center gap-x-3.5 py-2 px-2.5 text-sm text-sidebar-nav-foreground rounded-lg hover:bg-sidebar-nav-hover focus:outline-hidden focus:bg-sidebar-nav-focus" href="#">
                                            <TriondaIcon class="trionda-icon"></TriondaIcon>
                                            <p class="text-sm font-semibold text-gray-800">{{sessao.title}}</p>
                                        </router-link>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </DialogPanel>
                    </TransitionChild>
                </div>
                </div>
            </div>
            </Dialog>
        </TransitionRoot>
    </div> 
</template>

<style scoped>
  .open-menu-btn {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
    height: 40px;
    width: 200px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .wc-trophy-icon {
    width: 24px;
    height: 24px;
    flex-shrink: 0;
    color: rgba(107, 114, 128); 
    fill: currentColor;
    stroke: currentColor;
    
    transition: all 0.3s ease; 
  }

  .open-menu-btn:hover .wc-trophy-icon {
    color: black; 
    }

    .new-session-a {
        /* Removemos a cor e o hover daqui, o Tailwind assume isso */
        cursor: pointer;
    }

    .add-session-icon {
        width: 24px;
        height: 24px;
        flex-shrink: 0;
        /* Removemos a cor fixa daqui */
        fill: currentColor;
        stroke: currentColor;
        transition: all 0.3s ease; 
    }

    .new-session-a:hover .add-session-icon {
        color: black; 
    }
    .new-session-a:hover .hr {
        color: black; 
    }
    .new-session-a:hover {
        color: black; 
    }

  .trionda-icon {
    width: 25px;
    height: 25px;
    flex-shrink: 0;
    transition: all 0.3s ease;
  }

  .sessions-a:hover .trionda-icon {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    25% {
      transform: rotate(-8deg);
    }
    50% {
      transform: rotate(0deg);
    }
    75% {
      transform: rotate(8deg);
    }
    100% {
      transform: rotate(0deg);
    }
  }
</style>