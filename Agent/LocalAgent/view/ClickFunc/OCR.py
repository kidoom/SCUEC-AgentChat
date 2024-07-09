
import base64
import requests
import json
API_KEY = "Oj4Hq6yhI0ul2nSc3qbg8Ee6"
SECRET_KEY = "1Ym0ta0RazB30OFvH1izQUSrYILoda03"

import gradio as gr
def OCRTool(path):
    f = open(path,'rb')

    img = base64.b64encode(f.read())
    params = {"image": img}

    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage_loc?access_token=" + get_access_token()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=params)
    # 解析 JSON 数据
    data = json.loads(response.text)

    # 提取 words 字段
    words_list = [item['words'] for item in data['words_result']]

    result_string = ''.join(words_list)
    return result_string


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))




# with gr.Blocks() as agent:
#     with gr.Tab(label="chat"):
#         text = gr.Textbox()
#         file = gr.File(type="filepath")
#         button = gr.Button()
#         button.click(fn=OCRTool, inputs=file, outputs=text)
#
# agent.launch()