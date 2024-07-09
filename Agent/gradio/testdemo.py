import gradio as gr
from Agent.LocalAgent.LLM.ChatAgent import predict
from Agent.LocalAgent.LLM.tools.RateArticle import RateArticleTool
import time


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


user_avatar = "D:/SCUEC-AgentChat/gaoda.jpg"  # 替换为实际路径或URL
bot_avatar = "D:/SCUEC-AgentChat/rtvcxwhq.png"  # 替换为实际路径或URL


def slow_echo(message, history):
    for i in range(len(message)):
        time.sleep(0.05)
        yield "You typed: " + message[: i + 1]


textbox = gr.Textbox()

chatbot = gr.Chatbot(
    value=None,
    label="聊天机器人",
    height=400,  # 固定高度
    avatar_images=(user_avatar, bot_avatar),
    placeholder="请输入消息...",
    layout="bubble",  # 或 "panel"，根据需要选择布局
)

with gr.Blocks() as agent:
    with gr.Tab(label="chat"):
        chat = gr.ChatInterface(slow_echo, chatbot=chatbot)
    with gr.Tab(label="作文评分"):
        with gr.Column(scale=15):
            txt1 = gr.Textbox(label="命题标准", max_lines=10)
            txt2 = gr.Textbox(label="作文内容", max_lines=15)
            result = gr.Textbox(label="批改结果",lines=1, interactive=False,show_copy_button=True)
            b = gr.Button("开始批改")
            b.click(RateArticleTool, inputs=[txt1, txt2], outputs=result)


agent.launch()
