import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as cls
from matplotlib.font_manager import FontProperties
import matplotlib as mpl


class GeoPlotter:
    def __init__(self, font_path, file_path, geojson_file1, output_file, crs="EPSG:4326", plt_cmap="Spectral",
                 colorlist=None):
        self.font = FontProperties(fname=font_path)
        self.file_path = file_path
        self.geojson_file1 = geojson_file1
        self.output_file = output_file
        self.crs = crs
        self.plt_cmap = plt_cmap
        self.colorlist = colorlist if colorlist else ['#FF5733', '#3498db', '#27ae60', '#f39c12']
        mpl.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # Load data
        self.data = gpd.read_file(self.file_path + self.geojson_file1, encoding='utf-8')
        self.data.to_crs(self.crs, inplace=True)

    def polygons(self, layer, field=''):
        if '' == field:
            layer['color'] = layer.index % 4
            palette = cls.ListedColormap(self.colorlist)
            ax = layer.plot(column='color', cmap=palette)
        else:
            ax = layer.plot(column=field, cmap=self.plt_cmap, color='grey', legend=True)
        return ax

    def points(self, layer, field='', base=None):
        if '' == field:
            ax = layer.plot(ax=base, color='red', markersize=5)
        else:
            max_value = layer[field].max()
            min_value = layer[field].min()
            layer['size'] = 10 * (layer[field] - min_value) / (max_value - min_value)
            ax = layer.plot(ax=base, color='red', markersize=layer['size'])
        return ax

    def antt(self, data, view):
        data['coords'] = data['geometry'].apply(lambda x: x.representative_point().coords[:])
        data['coords'] = [coords[0] for coords in data['coords']]
        for coord, label in zip(data['coords'], data['name']):
            view.annotate(label, xy=coord, horizontalalignment='center', fontproperties=self.font)
        return view

    def draw(self):
        ax = self.polygons(self.data)
        ax = self.antt(self.data, ax)
        plt.savefig(self.file_path + self.output_file, dpi=300, bbox_inches='tight')
        print("画图ing")
        # plt.show()


# 示例调用
if __name__ == "__main__":
    font_path = "./src/手书体.ttf"
    file_path = "./src/"
    geojson_file1 = "sql_data.json"
    output_file = "out.png"

    plotter = GeoPlotter(font_path, file_path, geojson_file1, output_file)
    plotter.draw()
