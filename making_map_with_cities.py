from marker_functions import set_icon_with_color
import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import numpy as np

number_of_cities = 49


# ---- Load data from CSV ----
@st.cache_data
def load_city_data():
    df = pd.read_csv("full_data.csv")
    df["In_Trip"] = False  # add column to track selection
    df = df.set_index("City")
    return df


if "cities_data" not in st.session_state:
    st.session_state.cities_data = load_city_data()


if "city_values" not in st.session_state:
    st.session_state.city_values = [255] * number_of_cities

if "city_counter" not in st.session_state:
    st.session_state.city_counter = 0


def change_selection_of_the_city():
    st.session_state.cities_data.at[city_name, "In_Trip"] = (
        not st.session_state.cities_data.at[city_name, "In_Trip"]
    )


def calculate_values(list_of_selected_categories):

    list_of_values = [0] * number_of_cities
    counter = 0

    if not list_of_selected_categories:
        return [255] * number_of_cities

    for row in st.session_state.cities_data.iterrows():
        if "Tourism" in list_of_selected_categories:
            list_of_values[counter] += row[1][0]
        if "Night Life" in list_of_selected_categories:
            list_of_values[counter] += row[1][1]
        if "Safety Index" in list_of_selected_categories:
            list_of_values[counter] += row[1][3]
        if "Low Meal Prices" in list_of_selected_categories:
            list_of_values[counter] += 1 - row[1][6]
        if "Low Rent Prices" in list_of_selected_categories:
            list_of_values[counter] += 1 - row[1][7]
        if "Air Quality" in list_of_selected_categories:
            list_of_values[counter] += row[1][8]
        counter += 1

    values = np.array(list_of_values)
    min_val = np.min(values)
    max_val = np.max(values)
    if max_val - min_val == 0:
        normalized = np.ones_like(values)  # unikamy dzielenia przez 0
    else:
        normalized = (values - min_val) / (max_val - min_val)

    scaled = np.round(normalized * 255).astype(int)

    return scaled.tolist()


# ---- UI ----
st.title("Travel Preferences")

selected_categories = st.multiselect(
    "Choose categories you are interested in:",
    options=[
        "Tourism",
        "Night Life",
        "Safety Index",
        "Low Meal Prices",
        "Low Rent Prices",
        "Air Quality",
    ],
)


if selected_categories:
    st.session_state.city_values = calculate_values(selected_categories)

st.title("Select cities that you are interested in on the map 🌍")

# ---- Map ----
m = folium.Map(location=[52, 10], zoom_start=4)
st.session_state.city_counter = 0
for city, row in st.session_state.cities_data.iterrows():

    tooltip_text = f"Match percentage: {round(st.session_state.city_values[st.session_state.city_counter]*100/255,2)} %"
    folium.Marker(
        [row["Latitude"], row["Longitude"]],
        popup=city,
        tooltip=tooltip_text,
        icon=set_icon_with_color(
            st.session_state.city_values[st.session_state.city_counter]
        ),
    ).add_to(m)
    st.session_state.city_counter += 1

output = st_folium(m, width=700, height=500)

# ---- Handle city selection ----

if output["last_object_clicked_popup"]:
    # Extract only the city name (before the first newline)
    city_name = output["last_object_clicked_popup"]

    st.write(f"Selected city: **{city_name}**")
    checkbox = st.checkbox(
        f"Add {city_name} to your trip",
        value=st.session_state.cities_data.loc[city_name]["In_Trip"],
        on_change=change_selection_of_the_city,
    )
    if checkbox:
        st.success(f"{city_name} has been added ✅")
# ---- Sidebar: To-Visit List ----
with st.sidebar:
    st.header("🧳 To-Visit List")
    trip_cities = st.session_state.cities_data[st.session_state.cities_data["In_Trip"]]
    if len(trip_cities) > 0:
        for city in trip_cities.index:
            st.write(f"- {city}")
    else:
        st.write("No cities added yet.")