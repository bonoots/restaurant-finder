import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("GOOGLE_API_KEY")

API_URL = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = "places.displayName,places.formattedAddress,places.rating,places.userRatingCount"

@app.route("/", methods=["GET", "POST"])
def index():
    restaurants = []
    if request.method == "POST":
        query = request.form.get("query", "restaurants in Marrakech")
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": FIELD_MASK
        }
        payload = {
            "textQuery": query
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            for place in data.get("places", []):
                restaurants.append({
                    "name": place.get("displayName", {}).get("text", "N/A"),
                    "address": place.get("formattedAddress", "N/A"),
                    "rating": place.get("rating", "N/A"),
                    "user_ratings_total": place.get("userRatingCount", 0)
                })
        else:
            print("Error:", response.status_code, response.text)

    return render_template("index.html", restaurants=restaurants)

if __name__ == "__main__":
    app.run(debug=True)
