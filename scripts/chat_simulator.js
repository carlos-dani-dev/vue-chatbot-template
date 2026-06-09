import ollama from 'ollama'

async function send_message(message_content, stream_bool) {

    const response = await ollama.chat({
        model: 'llama3.2:3b',
        messages: [{role:'user', content: message_content}],
        stream: stream_bool
    });
    
    if(stream_bool){
        for await (const part of response) {
            process.stdout.write(part.message.content);
        }

        console.log()

    }else{
        console.log(response)
    }

}

send_message('Quem é o maior jogador da seleção portuguesa?', false)