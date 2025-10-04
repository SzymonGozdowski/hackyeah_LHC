import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def get_cities_crime_and_safety_rate():
    url = "https://www.numbeo.com/crime/rankings.jsp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching data. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Znalezienie tabeli po id="t2"
    table = soup.find("table", {"id": "t2"})
    if not table:
        print("No table with id='t2' found.")
        return None

    #print(table)

    tbody = table.find("tbody")
    if not tbody:
        print("No tbody found in table.")
        return None

    rows = tbody.find_all("tr")
    data = []


    for row in rows:
        cols = row.find_all("td")
        cols = [col.get_text(strip=True) for col in cols]
        words = cols[1].split(", ")
        
        cols[0] = words[0]
        cols[1] = words[1]

        if len(cols) >= 4:
            data.append([cols[0], cols[1], cols[2], cols[3]])  # City, Crime Index, Safety Index, QoL Index

    df = pd.DataFrame(data, columns=["City", "Crime Index", "Safety Index", "Quality of Life Index"])
    return df

def get_city_prices(city_name):
    """
    Scrape Numbeo cost-of-living table for a given city in EURO (€) and return cleaned data.
    """
    city_url_name = city_name.replace(" ", "-")
    url = f"https://www.numbeo.com/cost-of-living/in/{city_url_name}?displayCurrency=EUR"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching data for {city_name}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "data_wide_table"})
    if not table:
        print(f"No data table found for {city_name}.")
        return None

    rows = table.find_all("tr")
    data = []
    for row in rows[1:]:
        cols = row.find_all("td")
        cols = [col.text.strip() for col in cols]
        if len(cols) >= 2:
            # Remove Euro sign and commas
            price = re.sub(r'[€,\s]', '', cols[1])
            try:
                price = float(price)
            except ValueError:
                price = None
            data.append([cols[0], price])

    df = pd.DataFrame(data, columns=["Item", f"{city_name}"])
    return df

def save_crime_and_safety_to_csv():
    crime_and_safety = get_cities_crime_and_safety_rate()
    crime_and_safety.to_csv("data_base/crime_rates_and_safety.csv", index=False, encoding="utf-8")
    print(crime_and_safety.head())

# List of 10 European cities
cities = [
    "London", "Paris", "Berlin", "Madrid", "Rome", "Barcelona", "Amsterdam",
    "Vienna", "Prague", "Lisbon", "Budapest", "Milan", "Munich", "Warsaw",
    "Athens", "Dublin", "Copenhagen", "Stockholm", "Oslo", "Helsinki", "Brussels",
    "Zurich", "Geneva", "Frankfurt", "Hamburg", "Edinburgh", "Glasgow", "Birmingham",
    "Manchester", "Valencia", "Naples", "Florence", "Venice", "Krakow (Cracow)",
    "Gdansk", "Lyon", "Marseille", "Nice", "Turin", "Bologna", "Bilbao", "Porto",
    "Braga", "Zagreb", "Ljubljana", "Tallinn", "Riga", "Vilnius", "Luxembourg"
]

all_data = []

for city in cities:
    print(f"Fetching prices for {city}...")
    df_city = get_city_prices(city)
    if df_city is not None:
        # Filter for Meal and Rent items
        df_filtered = df_city[df_city['Item'].str.contains(
            "Meal, Inexpensive Restaurant|Price per Square Meter to Buy Apartment in City Centre",
            case=False, regex=True
        )]
        all_data.append(df_filtered)


# Combine all cities into one DataFrame
master_df = all_data[0][["Item", f"{cities[0]}"]].copy()
for i in range(1, len(all_data)):
    master_df = master_df.merge(all_data[i], on="Item", how="outer")


# Optional: rename items for clarity
master_df['Item'] = master_df['Item'].replace({
    'Meal, Inexpensive Restaurant': 'Meal (€)',
    'Price per Square Meter to Buy Apartment in City Centre': 'Rent per m² (€)'
})

# Save CSV
master_csv_filename = "europe_meal_rent_prices_clean.csv"
master_df.to_csv(master_csv_filename, index=False)
print(f"Cleaned data saved to {master_csv_filename}")
print(master_df)




