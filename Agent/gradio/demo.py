import gradio as gr
def echo(message, history):
    return message
with gr.Blocks() as demo:
    with gr.Tab(label="tct2img"):
        with gr.Row():
            with gr.Column(scale=15):
                txt1 = gr.Textbox(lines=2,label="")
                txt2 = gr.Textbox(lines=2,label="")
            with gr.Column(scale=1,min_width=1):
                builtin1 = gr.Button(value="1")
                builtin2 = gr.Button(value="2")
                builtin3 = gr.Button(value="3")
                builtin4 = gr.Button(value="4")
            with gr.Column(scale=6):
                generate_button = gr.Button(value="Generate",variant="stop",scale=1)
                with gr.Row():
                    drop = gr.Dropdown(choices=[1,2,3],label="style1")
                    drop2 = gr.Dropdown(choices=[1, 2, 3], label="style1")
    with gr.Tab(label="chat"):
            chat = gr.ChatInterface(fn=echo, examples=["hello", "hola", "merhaba"], title="Echo Bot")






demo.launch()

