from serpapi import GoogleSearch
import json

def get_list_of_attractions(query, lat=40.7455096, lon=74.0083012):

  ll = f"@{lat},{lon},14z"

  params = {
    "engine": "google_maps",
    "q": query,
    "ll": ll,
    "api_key": "95005b7ec1ba94377d7b3cd6f11e80f7b073b9771abe6f196f60392b5f77f65f"
  }

  # Pobranie wyników
  search = GoogleSearch(params)
  results = search.get_dict()

  # Sprawdzenie i zapis do JSON
  places = results.get("local_results", [])

  data = []
  for i, place in enumerate(places, 1):
      place_prop = f"{i}. {place.get('title'), place.get('rating'), place.get('address')}"
      data.append(place_prop)

  return data


