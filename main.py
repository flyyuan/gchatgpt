# coding=UTF-8
import gradio as gr
import openai

openai.api_key = "your api key"

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]


def respond(chat_history, message):
    gr.update(value='')
    try:
        print('message', message)
        messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        res_text = response['choices'][0]['message']['content']
        messages.append({"role": "system", "content": res_text})
        print('res_text', res_text)
        return chat_history + [[message, res_text]]
    except Exception as e:
        print(e)
        messages.clear()
        return chat_history + [[message, "Error: " + str(e)]]


def reset_textbox():
    return gr.update(value='')


with gr.Blocks(css="footer {visibility: hidden}"
                   "#component-3{background: #1aad19;color: #fff;}") as demo:
    chatbot = gr.Chatbot()
    user_input = gr.Textbox()
    submit_btn = gr.Button("发送")

    user_input.submit(respond, [chatbot, user_input], chatbot, scroll_to_output=True, show_progress=True, )
    submit_btn.click(respond, [chatbot, user_input], chatbot, queue=False, show_progress=True)
    submit_btn.click(reset_textbox, [], [user_input])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=6860, share=False)
