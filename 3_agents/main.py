import time

import gradio as gr
from fire import Fire
from langchain.callbacks import get_openai_callback
from langchain_utils import create_agent
import os

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

        clearButton.click(fn=clear)

        def user(user_message, history):
            return gr.update(
                value="", interactive=False), history + [
                [user_message, None]]

        def bot(history):
            with get_openai_callback() as cb:
                bot_message = f"```\n{agent.run(history[-1][0])}\n ```"

                # Write model usage in csv format to file

                with open("../monitoring.csv", "a") as f:
                    # get from environment variables
                    f.write(
                        f'"{int(time.time())}",{os.environ.get("MODEL")},"solution_3","{cb.prompt_tokens}","{cb.completion_tokens}"\n')

            history[-1][1] = ""
            for character in bot_message:
                history[-1][1] += character
                time.sleep(0.01)
                yield history

        response = msg.submit(
            user, [msg, chatbot],
            [msg, chatbot],
            queue=False).then(
            bot, chatbot, chatbot)
        response.then(
            lambda: gr.update(interactive=True),
            None, [msg],
            queue=False)

    demo.queue()
    demo.launch()


if __name__ == "__main__":
    Fire(run_gui)
