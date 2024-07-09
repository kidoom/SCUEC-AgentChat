import gradio as gr
from Agent.LocalAgent.LLM.ChatAgent import predict
from Agent.LocalAgent.LLM.tools.RateArticle import RateArticleTool
def echo(message, history):
    return message
# with gr.Blocks() as demo:
#     with gr.Tab(label="tct2img"):
#         with gr.Row():
#             with gr.Column(scale=15):
#                 txt1 = gr.Textbox(lines=2,label="")
#                 txt2 = gr.Textbox(lines=2,label="")
#             with gr.Column(scale=1,min_width=1):
#                 builtin1 = gr.Button(value="1")
#                 builtin2 = gr.Button(value="2")
#                 builtin3 = gr.Button(value="3")
#                 builtin4 = gr.Button(value="4")
#             with gr.Column(scale=6):
#                 generate_button = gr.Button(value="Generate",variant="stop",scale=1)
#                 with gr.Row():
#                     drop = gr.Dropdown(choices=[1,2,3],label="style1")
#                     drop2 = gr.Dropdown(choices=[1, 2, 3], label="style1")
#     with gr.Tab(label="chat"):
#             chat = gr.ChatInterface(fn=echo, examples=["hello", "hola", "merhaba"], title="Echo Bot")


with gr.Blocks() as agent:
    with gr.Tab(label="chat"):
            chat = gr.Interface(predict,title="Echo Bot",fill_height=True)
    with gr.Tab(label="作文评分"):
        with gr.Column(scale=15):
            txt1 = gr.Textbox(label="命题标准")
            txt2 = gr.Textbox(label="请输入作文")
            result = gr.Textbox(label="批改结果")
            b = gr.Button("开始批改")
            b.click(RateArticleTool,inputs=[txt1,txt2],outputs=result)




agent.launch()

