import requests
import streamlit as st

api_key = st.secrets["TMDB_API_KEY"]

url = "https://api.themoviedb.org/3/search/movie"

params = {
    "api_key": api_key,
    "query": "3 Idiots"
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)

if response.status_code == 200:
    data = response.json()

    if data["results"]:
        print("TMDB connection successful!")
        print("Movie found:", data["results"][0]["title"])
    else:
        print("Connection works, but movie was not found.")

else:
    print("TMDB API error:")
    print(response.text)