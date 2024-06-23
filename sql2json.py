import json


def sql2json(sql_outs):
    # 创建基本的GeoJSON结构
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    for out in sql_outs:
        # 添加Feature
        feature = {
            "type": "Feature",
            "properties": {
                "name": out["name"]
            },
            "geometry": json.loads(out["geom"])
        }
        # 将Feature添加到features列表中
        geojson_data["features"].append(feature)

    if sql_outs == []:
        feature = {
            "type": "Feature",
            "properties": {
                "name": "空"
            },
            "geometry": {"type": "MultiPolygon", "coordinates": [[[
                [114, 30], [115, 30], [115, 31], [114, 31]
            ]]]}
        }
        geojson_data["features"].append(feature)
        print("空表")

    # 将GeoJSON数据保存到文件中
    with open('./src/sql_data.json', 'w', encoding='utf-8') as file:
        json.dump(geojson_data, file, ensure_ascii=False, indent=4)

    print("GeoJSON文件已创建并保存为 data_new.json")


if __name__ == "__main__":
    sql2json([])
