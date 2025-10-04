import folium
from streamlit_folium import st_folium

# Tworzymy mapę
m = folium.Map(location=[52.0, 19.0], zoom_start=6)

# Tworzymy znacznik
marker = folium.Marker(location=[52.23, 21.01], popup="Warszawa")

# Dodajemy znacznik do mapy
m.add_child(marker)

# Można też dodać więcej
m.add_child(folium.Marker(location=[50.06, 19.94], popup="Kraków"))

# Zapisz lub wyświetl
# m.save("mapa.html")

output = st_folium(m, width=700, height=500)
