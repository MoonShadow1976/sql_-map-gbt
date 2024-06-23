import re

import gradio as gr
import os
from PIL import Image
import matplotlib

import MapDraw
from PostgreSQL_use import PostgreSQL_use
from chat import OllamaChatBot
from sql2json import sql2json


# Global variable to store output stream
output_stream = ""


def custom_print(*args, **kwargs):
    global output_stream
    message = " ".join(map(str, args))
    print(message, **kwargs)  # Optionally still print to console
    output_stream += message + "\n"
    return output_stream


def text_to_image_from_folder(text):
    global output_stream
    output_stream = ""  # Clear previous output

    # 类调用初始化
    db = PostgreSQL_use(
        user="postgres",
        password="20020727",
        host="localhost",
        port="5432",
        database="china"
    )

    bot = OllamaChatBot(
        model='sqlcoder:latest',
        sql_type='PostgreSQL'
    )
    # 与大模型交互
    custom_print(f"等待模型反馈问题:'{text}'")
    out, history = bot.chat(question=text)

    # 使用正则表达式匹配SQL语句
    pattern = re.compile(r'SELECT.*?;')
    sql_statement = pattern.search(out).group()
    # 使用 split 方法分割字符串并取出 FROM 及其后面的内容
    sql_statement_without_select = 'FROM' + sql_statement.split('FROM', 1)[1]
    getJson = "SELECT ST_AsGeoJSON(wkb_geometry), 名称 " + sql_statement_without_select
    # 输出提取的SQL语句
    custom_print(f"模型输出SQl查询语句:\n'{getJson}'")
    # 数据库查询
    custom_print("数据库查询中...")
    db.connect()
    sql_outs, result = db.use(getJson)
    db.close()
    # 查询结果
    custom_print(f"查询结果：{result}")
    # 获取数据库查询数据
    sql2json(sql_outs)
    custom_print("输出数据库查询结果到：sql_data.json")
    return output_stream


def draw_with_json():
    global output_stream

    custom_print("---------------------")
    custom_print("查询内容可视化中...")
    # 绘制地图
    plotter = MapDraw.GeoPlotter(
        font_path="./src/手书体.ttf",
        file_path="./src/",
        geojson_file1="sql_data.json",
        output_file="out.png"
    )
    plotter.draw()

    image_path = "./src/out.png"
    custom_print(f"地图存储位置: {image_path}，如需保存，请手动进行存储。")
    custom_print("！本地大模型模型输出并不稳定")

    if os.path.exists(image_path):
        img = Image.open(image_path)
        return img, output_stream
    else:
        custom_print("Image not found.")
        return "图片不存在，请检查输入文本是否正确。", output_stream


# Custom CSS style
css = """
#output-area {
    width: 20%;
    float: left;
    display: block;
    height: 100vh;
    overflow: auto;
    background-color: #f0f0f0; /* Example background color */
    padding: 10px; /* Example padding */
}

#main-content {
    width: 80%;
    float: right;
    height: calc(100vh - 50px);
    position: relative;
}
#image-container {
    width: 100%;
    height: 100%;
}
#bottom-input {
    position: fixed;
    bottom: 0;
    width: 20%;
    left: 20%;
    background-color: white;
    padding: 10px;
    box-shadow: 0px -2px 10px rgba(0,0,0,0.1);
}
@media screen and (max-width: 768px) {
    #output-area {
        display: none;
    }
    #main-content {
        width: 100%;
        float: none;
    }
    #bottom-input {
        width: 100%;
        left: 0;
    }
}
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown("# Text to Image from Folder")

    with gr.Row():
        with gr.Column(elem_id="output-area"):
            gr.Markdown("### 程序输出")
            output_textbox = gr.Textbox(label="输出内容", type="text", elem_id="output-textbox", interactive=False,
                                        lines=10)

        with gr.Column(elem_id="main-content"):
            output_image = gr.Image(label="Generated Image", type="pil", elem_id="image-container")

    with gr.Row(elem_id="bottom-input"):
        input_text = gr.Textbox(label="输入文字", type="text")
        submit_button = gr.Button("Submit")
        submit_button.click(fn=text_to_image_from_folder, inputs=input_text, outputs=output_textbox)

        draw_button = gr.Button("Draw")
        draw_button.click(fn=draw_with_json, inputs=None, outputs=[output_image, output_textbox])

if __name__ == "__main__":
    matplotlib.use("agg")  # Use the "agg" backend for matplotlib
    print("Starting Gradio interface...")
    demo.launch()  # Disable share to avoid the error
