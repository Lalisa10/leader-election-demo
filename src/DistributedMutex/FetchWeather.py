import requests

API_KEY = ""
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
        }
    else:
        print(f"Failed to fetch weather data: {response.status_code} - {response.text}")
        return None
