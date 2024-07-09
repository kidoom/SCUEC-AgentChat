import gradio as gr
from Agent.LocalAgent.LLM.ChatAgent import predict
from Agent.LocalAgent.LLM.tools.RateArticle import RateArticleTool
from Agent.LocalAgent.view.ClickFunc.OCR import OCRTool

user_avatar = "D:/SCUEC-AgentChat/gaoda.jpg"  # 替换为实际路径或URL
bot_avatar = "D:/SCUEC-AgentChat/rtvcxwhq.png"  # 替换为实际路径或URL


chatbot = gr.Chatbot(
    value=None,
    label="聊天机器人",
    height=400,  # 固定高度
    avatar_images=(user_avatar, bot_avatar),
    placeholder="请输入消息...",
    layout="bubble",  # 或 "panel"，根据需要选择布局
)

agent_button = gr.Button("发送")

with gr.Blocks() as agent:
    with gr.Tab(label="chat"):
        chat = gr.ChatInterface(predict, chatbot=chatbot)
    with gr.Tab(label="作文评分"):
        with gr.Row():
            with gr.Column():
                file = gr.File(type="filepath")
                OCR_text = gr.Textbox(label="识别结果", show_copy_button=True)
                OCR_button = gr.Button("开始识别")
                OCR_button.click(fn=OCRTool, inputs=file, outputs=OCR_text)
            with gr.Column():
                txt1 = gr.Textbox(label="命题标准", max_lines=10)
                txt2 = gr.Textbox(label="作文内容", max_lines=15)
        with gr.Row():
            with gr.Column():
                result = gr.Textbox(label="批改结果", lines=1, interactive=False, show_copy_button=True)
                b = gr.Button("开始批改")
                b.click(RateArticleTool, inputs=[txt1, txt2], outputs=result)

agent.launch()