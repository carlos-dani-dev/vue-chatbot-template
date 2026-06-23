<script setup>
    import SendMessageIcon from "@/assets/icons/send-message-icon.svg?component"
    import Message from "@/components/home/Message.vue"
</script>

<template>
    <div class="flex flex-col min-h-screen justify-center ">

        <div class="chat-messages flex w-full justify-center mb-5">
            <ul class="flex flex-col w-3/5 gap-2">
                <li class="w-full pr-10">
                    <Message class="text-base font-semibold text-gray-900"></Message>
                </li>
                <li class="w-full pr-10">
                    <Message class="text-base font-semibold text-gray-900"></Message>
                </li>
                <li class="w-full pl-10">
                    <Message class="text-base font-semibold text-gray-900"></Message>
                </li>
            </ul>
        </div>
        <div class="chat-text-input flex w-full">
            <form class="flex w-full justify-center items-center gap-2">
                <input
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

<style scoped></style>