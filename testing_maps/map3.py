import folium
from streamlit_folium import st_folium

# Tworzymy mapę
m = folium.Map(location=[52.0, 19.0], zoom_start=6)

# Tworzymy ikonę
city_icon = folium.CustomIcon(
    "testing_maps\city_icon.png", icon_size=(30, 30), icon_anchor=(15, 15)
)

# Tworzymy znacznik

marker = folium.Marker(
    location=[52.23, 21.01], tooltip="Warszawa", popup="Warszawa", icon=city_icon
)

# Dodajemy znacznik do mapy
m.add_child(marker)

# Można też dodać więcej

m.add_child(
    folium.Marker(
        location=[50.06, 19.94], tooltip="Kraków", popup="Kraków", icon=city_icon
    )
)


# Zapisz lub wyświetl
# m.save("mapa.html")

output = st_folium(m, width=700, height=500)
