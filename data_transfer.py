import requests
import pandas as pd

url = "https://www.numbeo.com/api/city_prices"
params = {
    "api_key": "YOUR_API_KEY",  # Numbeo wymaga klucza (rejestracja darmowa)
    "query": "Paris, France"
}

response = requests.get(url, params=params)
data = response.json()

df = pd.json_normalize(data)
df.head()
