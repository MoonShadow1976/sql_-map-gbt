import ollama


# 流输出
# stream = ollama.chat(model='sqlcoder', messages=[{'role': 'user', 'content': '查询武汉所有大学的面积?'}], stream=True)
# for chunk in stream:
#     print(chunk['message']['content'], end='', flush=True)
#

class OllamaChatBot:
    def __init__(self, model, sql_type):
        self.model = model
        self.question = ''
        self.sql_type = sql_type
        self.schema_prompt = ""

    def chat(self, question):
        self.question = question
        self.schema_prompt = f"""
                    ### 任务
                    生成一个SQL查询以回答以下问题:
                    '{self.question}'

                    ### 数据库式
                    此查询将在一个{self.sql_type}数据库上运行，该数据库的模式在以下字符串中表
                    示:
                    CREATE TABLE public.bou2_4p (
                        wkb_geometry geometry,        -- 几何位置信息，存储地理空间数据
                        area NUMERIC(12,3),           -- 面积，精度为小数点后三位
                        bou2_4m_ NUMERIC(11,0),       -- 未知字段，需进一步确认其意义
                        bou2_4m_id NUMERIC(11,0),     -- 未知字段，可能是唯一标识符或外键，需进一步确认其意义
                        adcode93 NUMERIC(6,0),        -- 行政区划代码（1993年）
                        adcode99 NUMERIC(6,0),        -- 行政区划代码（1999年）
                        名称 VARCHAR(50)              -- 省会名称，最大长度50字符
                    );


                    ### SQL输出
                    根据数据库模式，输出回答'{self.question}'的SQL查询如下:
                    ```sql
                    """
        # 直接输出
        response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': self.schema_prompt}])
        model_response = response['message']['content']
        return model_response, self.schema_prompt


if __name__ == "__main__":
    bot = OllamaChatBot(
        model='sqlcoder:latest',
        sql_type='PostgreSQL'
    )
    out, his = bot.chat(question="湖北周围有哪些省会")
    print(out)
