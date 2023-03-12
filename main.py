# coding=UTF-8
import gradio as gr
import openai

openai.api_key = "your api key"

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]


def respond(chat_history, message):
    messages.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    res_text = response['choices'][0]['message']['content']
    messages.append({"role": "system", "content": res_text})
    print(res_text)
    return chat_history + [[message, res_text]]


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(respond, [chatbot, msg], chatbot, scroll_to_output=True, show_progress=True)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=6860, share=False)
