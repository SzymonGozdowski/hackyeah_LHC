import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from marker_functions import set_icon_with_color
from categories import categories, get_attractions
import numpy as np

number_of_cities = 49

# ---- Load data ----
@st.cache_data
def load_city_data():
    df = pd.read_csv("full_data.csv")
    # Ensure column names are clean (replace en-dash with hyphen)
    df = df.rename(columns=lambda x: x.replace("–", "-").strip())
    df["in_trip"] = False
    df["days"] = 1
    df = df.set_index("City")
    return df


if "cities_data" not in st.session_state:
    st.session_state.cities_data = load_city_data()

cities_data = st.session_state.cities_data


if "city_values" not in st.session_state:
    st.session_state.city_values = [255] * number_of_cities

if "city_counter" not in st.session_state:
    st.session_state.city_counter = 0


# ---- Subpage selection ----
page = st.sidebar.radio("Select page:", ["City Ranking", "Trip Planner"])

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

# -------------------------------
# PAGE 1: City Ranking
# -------------------------------
if page == "City Ranking":
    st.title("City Ranking")

    # Ranking weights
    st.sidebar.subheader("Ranking Weights")
    weight_cost = st.sidebar.slider("Weight: Cost (food + rent)", 0.0, 1.0, 0.5)
    weight_safety = st.sidebar.slider("Weight: Safety Index", 0.0, 1.0, 0.5)
    weight_air = st.sidebar.slider("Weight: Air Quality", 0.0, 1.0, 0.0)

    # Standard assumptions for monthly cost
    apartment_size = 50
    rental_yield = 0.04
    meals_per_day = 3
    days = 30

    # Compute estimated monthly cost
    cost_list = []
    for city, row in cities_data.iterrows():
        food_cost = meals_per_day * days * row["Meal (€)"]
        yearly_rent = row["Rent per m² (€)"] * apartment_size * rental_yield
        daily_rent = yearly_rent / 365
        rent_cost = daily_rent * days
        total_cost = food_cost + rent_cost
        cost_list.append(total_cost)
    cities_data["estimated_monthly_cost"] = cost_list

    # Normalize for ranking
    cost_norm = (cities_data["estimated_monthly_cost"] - cities_data["estimated_monthly_cost"].min()) / \
                (cities_data["estimated_monthly_cost"].max() - cities_data["estimated_monthly_cost"].min())
    safety_norm = (cities_data["Safety Index (0-1)"] - cities_data["Safety Index (0-1)"].min()) / \
                  (cities_data["Safety Index (0-1)"].max() - cities_data["Safety Index (0-1)"].min())
    air_norm = (cities_data["Air Quality (normalized)"] - cities_data["Air Quality (normalized)"].min()) / \
               (cities_data["Air Quality (normalized)"].max() - cities_data["Air Quality (normalized)"].min())

    # Combined ranking score
    cities_data["ranking_score"] = (
            weight_safety * safety_norm +
            weight_cost * (1 - cost_norm) +
            weight_air * air_norm
    )

    ranked = cities_data.sort_values("ranking_score", ascending=False)
    st.subheader("Top Cities")
    st.dataframe(ranked[["estimated_monthly_cost", "Safety Index (0-1)", "Air Quality (normalized)", "ranking_score"]])


# -------------------------------
# PAGE 2: Trip Planner
# -------------------------------
else:
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

    st.subheader("Select cities that you are interested in on the map 🌍")

    # ---- Map ----
    m = folium.Map(location=[52, 10], zoom_start=4)
    st.session_state.city_counter = 0
    for city, row in st.session_state.cities_data.iterrows():
        tooltip_text = f"Match percentage: {round(st.session_state.city_values[st.session_state.city_counter] * 100 / 255, 2)} %"
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

    # Handle city selection
    if output["last_object_clicked_popup"]:
        city_name = output["last_object_clicked_popup"].split("\n")[0].strip()
        st.write(f"Selected city: **{city_name}**")


        def toggle_city():
            cities_data.at[city_name, "in_trip"] = not cities_data.at[city_name, "in_trip"]


        checkbox = st.checkbox(
            f"Add {city_name} to your trip",
            value=cities_data.loc[city_name]["in_trip"],
            on_change=toggle_city
        )
        if checkbox:
            st.success(f"{city_name} has been added ✅")

    # Sidebar: Trip costs
    with st.sidebar:
        st.header("🧳 To-Visit List & Costs")
        meals_per_day = st.number_input("Meals per day", 1, 10, 3)
        apartment_size = st.number_input("Apartment size (m²)", 10, 200, 50)
        # rental_yield = st.number_input("Rental yield (% per year)", 1.0, 10.0, 4.0, 0.1) / 100
        rental_yield = 0.08  # 4% fixed rental yield

        trip_cities = cities_data[cities_data["in_trip"]]
        total_food_cost = 0
        total_rent_cost = 0
        if len(trip_cities) > 0:
            for city in trip_cities.index:
                city_data = cities_data.loc[city]
                st.write(f"**{city}**")

                # Remove city
                if st.button(f"Remove {city}", key=f"remove_{city}"):
                    cities_data.at[city, "in_trip"] = False

                # Number of days
                days = st.number_input(f"Days in {city}", 1, 30, int(city_data["days"]), key=f"days_{city}")
                cities_data.at[city, "days"] = days

                # Costs
                food_cost = days * meals_per_day * city_data["Meal (€)"]
                yearly_rent = city_data["Rent per m² (€)"] * apartment_size * rental_yield
                daily_rent = yearly_rent / 365
                rent_cost = daily_rent * days

                total_food_cost += food_cost
                total_rent_cost += rent_cost

                st.write(f"- Food cost: €{food_cost:.2f}")
                st.write(f"- Apartment rent estimate: €{rent_cost:.2f}")

            st.markdown("---")
            st.subheader(f"Total estimated food cost: €{total_food_cost:.2f}")
            st.subheader(f"Total estimated apartment rent: €{total_rent_cost:.2f}")
            st.subheader(f"Grand total for trip: €{total_food_cost + total_rent_cost:.2f}")
        else:
            st.write("No cities added yet.")
