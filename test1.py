import streamlit as st
from serpapi import GoogleSearch

def get_list_of_attractions(query, lat, lon, api_key):
    ll = f"@{lat},{lon},14z"

    params = {
        "engine": "google_maps",
        "q": query,
        "ll": ll,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("local_results", [])


st.set_page_config(page_title="Google Maps Finder", page_icon="🗺️", layout="centered")
st.title("🗺️ Wyszukiwarka miejsc z Google Maps (SerpApi)")

api_key = st.text_input("🔑 Twój SerpApi API key", type="password")
query = st.text_input("🔍 Czego szukasz? (np. Coffee, Museum, Club)")
col1, col2 = st.columns(2)
lat = col1.number_input("📍 Latitude", value=40.7455096)
lon = col2.number_input("📍 Longitude", value=-74.0083012)

if st.button("Szukaj"):
    if not api_key:
        st.error("❌ Podaj swój API key do SerpApi!")
    elif not query:
        st.warning("⚠️ Wpisz, czego chcesz szukać.")
    else:
        with st.spinner("🔎 Szukam..."):
            results = get_list_of_attractions(query, lat, lon, api_key)

        if not results:
            st.warning("😢 Brak wyników — spróbuj zmienić zapytanie lub współrzędne.")
        else:
            st.success(f"✅ Znaleziono {len(results)} miejsc!")
            for r in results:
                st.subheader(r.get("title", "Nieznana nazwa"))
                st.write(f"⭐ Ocena: {r.get('rating', 'brak danych')}")
                st.write(f"📍 Adres: {r.get('address', 'brak danych')}")

                # Spróbuj uzyskać lepszy obrazek
                img_url = None
                if r.get("images"):
                    # Jeśli są większe zdjęcia
                    img_url = r["images"][0].get("thumbnail") or r["images"][0].get("image")
                elif r.get("thumbnail"):
                    img_url = r["thumbnail"]
                elif r.get("serpapi_thumbnail"):
                    img_url = r["serpapi_thumbnail"]

                if img_url:
                    st.image(img_url, width=400, caption=r.get("title"))

                st.markdown("---")
