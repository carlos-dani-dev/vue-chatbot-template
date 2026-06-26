<script setup>
    
    import { onMounted, defineEmits, defineProps, computed } from 'vue'
    import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
    import { useChatSessionsStore } from '@/stores/chat_session_store'

    import { XMarkIcon } from '@heroicons/vue/24/outline'
    import PlusIcon from '@/assets/icons/plus-icon.svg?component'
    

    const sessionsStore = useChatSessionsStore();

    async function load_chat_session(){
        await sessionsStore.loadSessions();    
    }

    onMounted(load_chat_session);

    const props = defineProps(['sideBarMenuOpen']);
    const emit = defineEmits(['update:sideBarMenuOpen']);

    const open = computed({
        get(){
            return props.sideBarMenuOpen
        },
        set(value){
            emit('update:sideBarMenuOpen', value);
        }
    })

</script>

<template>
    <div>
        <TransitionRoot as="template" :show="open">
            <Dialog class="relative z-20" @close="open = false">
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
                                <DialogTitle class="text-base font-semibold text-gray-900">Sessions</DialogTitle>
                            </div>

                            <div class="group cursor-pointer">
                                
                                <router-link to="/chats" @click="open = false" class="new-session-a w-full flex items-center justify-center gap-x-3.5 py-2 px-2.5 text-sm text-gray-500 group-hover:text-black transition-colors duration-200" href="#">
                                    <PlusIcon class="plus-icon"></PlusIcon>
                                    <p class="text-sm font-semibold">New session</p>
                                </router-link>

                            </div>

                            <div class="relaive mt-4 flex-1 px-4 sm:px-6">
                                <ul>
                                    <li v-for="session in sessionsStore.sessions" :key="session.id">
                                        <router-link :to="`/chats/${session.id}`" @click="open = false" 
                                            class="sessions-a w-full flex items-center gap-x-3.5 py-2 px-2.5 text-sm text-sidebar-nav-foreground rounded-lg hover:bg-sidebar-nav-hover focus:outline-hidden focus:bg-sidebar-nav-focus" href="#">
                                            <p class="text-sm font-semibold text-gray-800">{{session.title}}</p>
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
    .new-session-a {
        cursor: pointer;
    }

    .plus-icon {
        width: 24px;
        height: 24px;
        flex-shrink: 0;
        color: rgba(107, 114, 128);
        fill: currentColor;
        stroke: currentColor;
        transition: color 0.3s ease; 
    }

    .new-session-a:hover .plus-icon,
    .new-session-a:focus .plus-icon {
        color: black; 
    }
    .new-session-a:hover,
    .new-session-a:focus {
        color: black; 
    }
</style>