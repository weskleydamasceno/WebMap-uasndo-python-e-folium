import folium
import os
import pandas as pd

data = pd.read_csv("data/Volcanoes.txt")
lat = (data["LAT"])
lon = (data["LON"])
elev = (data["ELEV"])
name = (data["NAME"])

# create a map object
m = folium.Map(location=[38.58, -99.09], tiles="OpenStreetMap", zoom_start=5, width='70%', height='70%', left='15%', top='15%')

tooltip = 'Click for more info'

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

# Create a function to change the marker colors
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

# Geojson Data
#overlay = os.path.join('data', 'geojson.json')

# Geojson overlay
#folium.GeoJson(overlay, name='Aracati').add_to(m)

# create a FeatureGroup layer to volcanoes
fgv = folium.FeatureGroup(name='Volcanoes map')

for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), tooltip=tooltip,  icon=folium.Icon(color=color_producer(el))))

# create a FeatureGroup layer to population
fgp = folium.FeatureGroup(name='Population map')

# adding a GeoJson layer
fgp.add_child(folium.GeoJson(data=open('data/world.json', 'r', encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
        else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
        else 'red'}))

m.add_child(fgv)
m.add_child(fgp)
m.add_child(folium.LayerControl())

# generate map
m.save('map.html')