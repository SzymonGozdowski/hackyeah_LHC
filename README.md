# hackyeah_LHC_team
GoodMap – Your AI-Powered Travel Planner

Built at HackYeah 2025

🌍 Overview

GoodMap is an interactive web app that helps travelers plan personalized trips across Europe.
It combines data visualization, city statistics, and live attraction search to help users make smarter travel decisions based on their preferences, budget, and interests.

With GoodMap, you can explore cities, compare travel costs, and find the best spots — all in one place.

✨ Features:
🗺️ Interactive Map Planner

Explore 49 European cities visualized on a map.

Filter destinations by your interests such as:

Tourism

Night Life

Safety Index

Air Quality

Meal and Rent Prices

Cities are color-coded based on how well they match your preferences.

💰 Trip Cost Estimator

Add cities to your personal trip list.

Define how many days you plan to stay in each.

Automatically calculate:

Total food expenses

Estimated apartment rent

Overall trip budget

🔎 Attraction Search (Google Maps + SerpApi)

Instantly find local attractions in any selected city.

Search for cafés, museums, clubs, or any custom query.

View names, ratings, addresses, and preview images.

🧠 How It Works

Choose your travel preferences – select categories that matter to you.

Explore the map – cities are scored and visualized by match percentage.

Add cities to your trip – track costs and number of days.

Search for attractions – use integrated Google Maps results to discover places to visit.

⚙️ Tech Stack

Frontend & UI: Streamlit

Maps: Folium
 + streamlit-folium

Data Analysis: pandas, NumPy

Attraction Search API: SerpApi
 (Google Maps integration)

Data: Pre-collected dataset of 49 European cities (full_data.csv)

🚀 How to Run Locally
# Clone the repository
git clone https://github.com/yourusername/tripmate.git
cd tripmate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py


Make sure you have a valid SerpApi API key, and update it in the code (or set it as an environment variable).

💡 Inspiration

We wanted to build a simple but powerful tool that helps travelers make data-driven decisions — choosing destinations not just by reputation, but by what truly fits their lifestyle, preferences, and budget.

👥 Team

Built with ❤️ by [Your Team Name] during HackYeah 2025.
Turning travel dreams into data-powered plans.

# Data taken from these websites:
https://www.numbeo.com
https://serpapi.com