# import sqlite3
# import numpy
import folium
from folium.features import CustomIcon
from folium import features, plugins
from pandas import DataFrame

# 操作sqlite3数据库
# conn = sqlite3.connect('DB\\GPS.db')
# conn.execute("insert into GPS_points (lat,lon) values (34,56)")
# conn.commit()
# conn.close()
# print(4)

print(folium.__version__)
# python+folium地图
map_osm = folium.Map(location=[36.9848416666667, 111.8207],
                     # tiles='Stamen Toner',
                     zoom_start=18)

map_osm.add_child(folium.LatLngPopup())  # 点击地图任意一个位置将显示对应的经纬度
map_osm.add_child(folium.ClickForMarker(
    popup='ClickForMarker'))  # 点击地图任意一个位置会显示一个默认标记

# 标记方式一
folium.Marker([36.9848416666667, 111.8207],
              popup='center').add_to(
    map_osm)  # popup为点击标记点时出现的注释文字

# 标记方式二
folium.Marker([36.9846633333333, 111.820741666667],
              popup='point_1',
              icon=folium.Icon(color='cloud')).add_to(
    map_osm)
# 标记方式三
folium.Marker([36.9846866666667, 111.820841666667],
              popup='point_2',
              icon=folium.Icon(color='green')).add_to(map_osm)
# 标记方式四
folium.Marker([36.9846483333333, 111.820878333333],
              popup='point_3',
              icon=folium.Icon(color='red', icon='info-sign')).add_to(map_osm)
# 标记方式五（可用来做停留点的画）
folium.CircleMarker([36.9846766666667, 111.820881666667],
                    radius=30,
                    popup='Stay points example',
                    color='#3186cc',
                    fill_color='#3186cc').add_to(map_osm)
# 标记方式六（可以以任意多边形来标记）
folium.RegularPolygonMarker([36.9842, 111.8207],
                            popup='point_4',
                            fill_color='#132b5e',
                            number_of_sides=4,  # 表示正几边形，如3表示正三角形
                            radius=10
                            ).add_to(map_osm)

# 可以在完整的一段轨迹中添加“自行车”、“TAXI”、“步行”、“公交车”图标
icon = CustomIcon(
    'pic/bike.jpg',
    icon_size=(38, 40),
    icon_anchor=(22, 94),
    popup_anchor=(-3, -76)
)
marker = folium.Marker(location=[36.9841, 111.8215], icon=icon, popup='bike')
map_osm.add_child(marker)


# draw line（在两个经纬诚度之间连线）
kw = dict(opacity=1.0, weight=2)
line1 = folium.PolyLine(
    locations=[(36.9841, 111.8194), (36.9841, 111.8205)], color='red', **kw)
map_osm.add_child(line1)

# draw trajectory1（轨迹画出）
point_lon = [36.9860, 36.9861, 36.9860, 36.9858, 36.9857, 36.9856, 36.9855]
point_lat = [111.8217, 111.8213, 111.8211,
             111.8212, 111.8213, 111.8212, 111.8212]
color_line = features.PolyLine(
    list(zip(point_lon, point_lat)),
    color='red',
    weight=2,
    popup='轨迹1')
color_line.add_to(map_osm)

# draw trajectory2（轨迹画出）
Traj_data = [[36.9857, 111.8194, 2.4], [36.9856, 111.8193, 2.2],
             [36.9853, 111.8192, 2.1], [36.9851, 111.8195, 2.33]]
columns = ['Longitude', 'Latitude', 'Speed']
df = DataFrame(Traj_data, columns=columns)

"""
print(df.head())
output:
   Longitude  Latitude  Speed
0    36.9857  111.8194   2.40
1    36.9856  111.8193   2.20
2    36.9853  111.8192   2.10
3    36.9851  111.8195   2.33
"""

# draw trajectory3（轨迹画出）
Traj_data2 = [[36.9857, 111.8201], [36.9855, 111.8200],
              [36.9853, 111.8200], [36.9851, 111.8199]]
line2 = folium.PolyLine(locations=Traj_data2,
                        color='orange',
                        weight=2,
                        opacity=1,
                        popup='轨迹2')
map_osm.add_child(line2)

# draw trajectory4（轨迹画出，并标注文字，版本0.3.0，如无特殊要求，可忽略）
# Traj_data3 = [[36.9856, 111.8221], [36.9856, 111.8227],
#               [36.9856, 111.8235], [36.9857, 111.8244]]
# line3 = folium.PolyLine(Traj_data3,
#                         weight=10,
#                         color='black',
#                         popup='轨迹3')
# line3.add_to(map_osm)
# plugins.PolyLineTextPath(
#     line3,
#     "To 北京",
#     offset=-5
# ).add_to(map_osm)

# 可在起始点和终点处标明方向
kw = dict(prefix='fa', color='green', icon='arrow-up')
icon = folium.Icon(angle=180, **kw)  # angle是角度
folium.Marker([36.9858, 111.8226], icon=icon).add_to(map_osm)

# 若需要小窗口地图，可参考：http://nbviewer.jupyter.org/github/python-visualization/folium/tree/master/examples/中WidthHeight.ipynb
map_osm.save('osm.html')
