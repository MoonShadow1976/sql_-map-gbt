import re

import gradio as gr
import os
from PIL import Image
import matplotlib

import MapDraw
from PostgreSQL_use import PostgreSQL_use
from chat import OllamaChatBot
from sql2json import sql2json

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
plotter = MapDraw.GeoPlotter(
    font_path="./src/手书体.ttf",
    file_path="./src/",
    geojson_file1="sql_data.json",
    output_file="out.png"
)

out = "SELECT ST_AsGeoJSON(wkb_geometry),名称 FROM bou2_4p WHERE wkb_geometry && (SELECT wkb_geometry FROM bou2_4p WHERE adcode93 = 110000)"
# 使用 split 方法分割字符串并取出 FROM 及其后面的内容
ouuu = 'FROM' + out.split('FROM', 1)[1]
print(ouuu)