import psycopg2

from MapDraw import GeoPlotter
from sql2json import sql2json


class PostgreSQL_use:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
        except Exception as error:
            print(f"Error connecting to PostgreSQL database: {error}")
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()

    def use(self, sql):
        if not self.connection:
            print("No connection established.")
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            tables = cursor.fetchall()
            sql_out = []
            for table in tables:
                sql_out.append({"geom": table[0], "name": table[1]})
            return sql_out, "查询成功"
        except Exception as error:
            print(f"Error fetching tables: {error}")
            return [], str(error)


# 示例如何使用这个类
if __name__ == "__main__":
    db = PostgreSQL_use(
        user="postgres",
        password="20020727",
        host="localhost",
        port="5432",  # PostgreSQL 的默认端口是 5432
        database="china"
    )

    db.connect()
    out= db.use("SELECT ST_AsGeoJSON(wkb_gometry),名称 FROM bou2_4p WHERE wkb_geometry && (SELECT wkb_geometry FROM bou2_4p WHERE adcode93 = 110000)")
    db.close()

    sql2json(out)

    font_path = "./src/手书体.ttf"
    file_path = "./src/"
    geojson_file1 = "sql_data.json"
    output_file = "out.png"

    plotter = GeoPlotter(font_path, file_path, geojson_file1, output_file)
    #plotter.draw()
# 查询时需要包括ST_AsGeoJSON(wkb_geometry)字段
