from flask import Flask, request
import requests
import os

app = Flask(__name__)

OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")
TIMEZONEDB_API_KEY = os.getenv("TIMEZONEDB_API_KEY")
DEFAULT_CITY = "Paris"

def get_lat_lon(city):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={OPENCAGE_API_KEY}&language=fr"
    res = requests.get(url).json()
    if res['results']:
        lat = res['results'][0]['geometry']['lat']
        lon = res['results'][0]['geometry']['lng']
        return lat, lon
    return None, None

def get_timezone(lat, lon):
    url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={TIMEZONEDB_API_KEY}&format=json&by=position&lat={lat}&lng={lon}"
    res = requests.get(url).json()
    if res['status'] == 'OK':
        return res['zoneName']  # ex: "Europe/Paris"
    return None

@app.route("/")
def heure():
    ville = request.args.get("ville", DEFAULT_CITY)

    lat, lon = get_lat_lon(ville)
    if lat is None or lon is None:
        return f"❌ Ville inconnue : {ville}"

    timezone = get_timezone(lat, lon)
    if timezone is None:
        return f"❌ Fuseau horaire introuvable pour {ville}"

    url = f"https://timeapi.io/api/Time/current/zone?timeZone={timezone}"
    response = requests.get(url)
    if response.status_code != 200:
        return f"⛔ Impossible de récupérer l'heure pour {ville}."

    data = response.json()
    heure = data.get("time")
    if not heure:
        return "⛔ Données d'heure invalides reçues."

    heure_court = heure[:5]
    ville_affichee = ville.title()
    return f"🕒 Il est {heure_court} à {ville_affichee}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
