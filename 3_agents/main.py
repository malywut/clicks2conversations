import time

import gradio as gr
from fire import Fire

from langchain_utils import create_agent

agent = None

def run_gui():
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clearButton = gr.ClearButton([msg, chatbot])
        global agent
        agent = create_agent()

        def clear():
            global agent
            agent = create_agent()

        clearButton.click(fn= clear)

        def user(user_message, history):
            return gr.update(value="", interactive=False), history + [[user_message, None]]

        def bot(history):
            bot_message = f"```\n{agent.run(history[-1][0])}\n ```"

            history[-1][1] = ""
            for character in bot_message:
                history[-1][1] += character
                time.sleep(0.01)
                yield history

        response = msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
        response.then(lambda: gr.update(interactive=True), None, [msg], queue=False)

    demo.queue()
    demo.launch()


if __name__ == "__main__":
    Fire(run_gui)