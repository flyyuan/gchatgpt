# coding=UTF-8
import gradio as gr
import openai

openai.api_key = "your api key"

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]


def respond(chat_history, message):
    try:
        print('message',message)
        messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        res_text = response['choices'][0]['message']['content']
        messages.append({"role": "system", "content": res_text})
        print('res_text',res_text)
        return chat_history + [[message, res_text]]
    except Exception as e:
        print(e)
        messages.clear()
        return chat_history + [[message, "Error: " + str(e)]]


with gr.Blocks(css="footer {visibility: hidden}"
                   "#component-3{background: #1aad19;color: #fff;}") as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    submit = gr.Button("发送")

    msg.submit(respond, [chatbot, msg], chatbot, scroll_to_output=True, show_progress=True)
    submit.click(respond, [chatbot, msg], chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=6860, share=False)
