from greppo import app
import geopandas as gpd

# Passing a markdown text to the app.
md_text = """
<img src="https://i.imgur.com/OvzeCgx.png" width="200" height="200" />

## Gallery

<table>
  <tr>
    <td><img src="https://i.imgur.com/XT7QFtY.jpeg" width=270></td>
    <td><img src="https://i.imgur.com/GwhvXVZ.jpg" width=270></td>
  </tr>
 </table>

# Trip Statistics
"""

app.display(name="text", value=md_text)

app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

#charts

data1 = [46, 40, 42, 44, 45, 46, 48, 46, 42, 40]

app.line_chart(
    name="Cloud Coverage",
    description="Cloud coverage during trip",
    x=[i for i in range(10)],
    y=data1,
    color="rgb(3, 119, 252)",
)

data2 = [23, 24, 24, 24, 22, 23, 22, 22, 23, 22]

app.line_chart(
    name="Mean Temperature",
    description="Mean Temperature during trip",
    x=[i for i in range(10)],
    y=data2,
    color="rgb(3, 119, 252)",
)

data3 = [16, 14, 15, 15, 14, 16, 13, 12, 13, 14, 15]

app.line_chart(
    name="Air Quality Index",
    description="Air Quality Index during trip",
    x=[i for i in range(10)],
    y=data3,
    color="rgb(3, 119, 252)",
)

points_gdf = gpd.read_file("./data/points.geojson")

app.overlay_layer(
    points_gdf,
    name="Points",
    description="Trip data",
    style={"fillColor": "#0377fc", "marker-size":"medium"},
    visible=True,
)