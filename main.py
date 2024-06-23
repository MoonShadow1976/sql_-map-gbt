import gradio as gr
import re
import ollama
from PostgreSQL_use import PostgreSQL_use
from chat import OllamaChatBot
from sql2json import sql2json
import MapDraw

# 初始化聊天历史
chat_history = []


def chat_with_model(user_input, history):
    global chat_history  # 使用全局变量来存储聊天历史

    # 将用户输入添加到聊天历史
    history.append({"role": "user", "content": user_input})

    # 将整个历史记录发送到模型并获取响应
    response_stream = ollama.chat(model='sqlcoder', messages=history)

    # 收集模型的响应

    model_response = response_stream['message']['content']

    # 将模型响应添加到聊天历史
    history.append({"role": "model", "content": model_response})

    # 返回更新后的聊天历史
    chat_display = [(item['role'], item['content']) for item in history]
    return chat_display, chat_display


def clear_chat():
    global chat_history
    chat_history = []
    return chat_history, []


if __name__ == "__main__":
    db = PostgreSQL_use(
        user="postgres",
        password="20020727",
        host="localhost",
        port="5432",  # PostgreSQL 的默认端口是 5432
        database="china"
    )
    bot = OllamaChatBot(
        model='sqlcoder:latest',
        sql_type='PostgreSQL'
    )

    # 与大模型交互
    out, history = bot.chat(question="湖北周围有哪些省会")

    # 使用正则表达式匹配SQL语句
    pattern = re.compile(r'SELECT.*?;')
    sql_statement = pattern.search(out).group()
    # 输出提取的SQL语句
    print(sql_statement)
    # 去除SELECT
    sql_statement_without_select = sql_statement.strip()[len('SELECT '):]
    getJson = "SELECT ST_AsGeoJSON(wkb_geometry)," + sql_statement_without_select

    # 数据库查询
    db.connect()
    sql_outs = db.use(sql_statement)
    db.close()

    # 获取数据库查询数据
    sql2json(sql_outs)
    # 绘图
    MapDraw
