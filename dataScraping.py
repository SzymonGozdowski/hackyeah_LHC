import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_city_prices(city_name):
    """
    Scrape Numbeo cost-of-living table for a given city in EURO (€).
    city_name: str, e.g., "Paris" or "New-York"
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

    # Extract rows
    rows = table.find_all("tr")
    data = []
    for row in rows[1:]:  # skip header
        cols = row.find_all("td")
        cols = [col.text.strip() for col in cols]
        if len(cols) >= 2:
            data.append([cols[0], cols[1]])

    df = pd.DataFrame(data, columns=["Item", "Average Price (€)"])
    return df


# --- Example usage ---
city = input("Enter the city name (e.g., Paris, New-York): ")
df_city = get_city_prices(city)
if df_city is not None:
    print(df_city.head())
