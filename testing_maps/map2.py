import streamlit as st
from streamlit_folium import st_folium
import folium

st.title("Kliknij na mapę 🌍")

# Tworzymy mapę
m = folium.Map(location=[52.0, 19.0], zoom_start=6)

# Dodaj możliwość kliknięcia
m.add_child(folium.LatLngPopup())

# Renderujemy mapę w Streamlit
output = st_folium(m, width=700, height=500)

# Odczytaj kliknięcie
if output["last_clicked"]:
    lat = output["last_clicked"]["lat"]
    lon = output["last_clicked"]["lng"]
    st.write(f"Kliknięto w: **{lat:.4f}, {lon:.4f}**")

    # Przykład reakcji
    st.success("🎉 Wykonuję akcję na podstawie kliknięcia!")
