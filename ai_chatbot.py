import openai
import gradio

#Remove the line below if you are using officia OpenAI API key or
#reverse proxy from some other service except PawanOsman
openai.api_base="https://api.pawan.krd/unfiltered/v1" 

openai.api_key="Your API Key"

history = []

first_message = True
file_name = "Defalut"

def chat_bot(message):
    global first_message,file_name
    if first_message:
        file_name = message[:50]
        first_message = False
    history.append({"role": "user", "content": message})
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=history)
    response = chat_completion.choices[0].message.content
    history.append({"role": "assistant", "content": response})
    with open(f"{file_name}.txt",'a',encoding="utf-8") as f:
        f.write(f"Message : {message}\n")
        f.write(f"Response : {response}\n")
    conversation = [(history[i]["content"],history[i+1]["content"]) for i in range(0,len(history)-1,2)]
    print(conversation)
    return "",conversation
    
with gradio.Blocks() as chatbot_ui:
    gradio.Markdown("""<h1><center>My First AI ChatBot</center><h1>""")
    chatbot = gradio.Chatbot()
    txt = gradio.Textbox(show_label=False,placeholder="Chat with me about anything that you want!!")
    submit = gradio.Button("Send")
    submit.click(chat_bot,inputs=txt,outputs=[txt,chatbot])

chatbot_ui.launch()
