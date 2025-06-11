from flask import Flask, request
import requests

app = Flask(__name__)

DEFAULT_CITY = "Paris"
TIMEZONE_LOOKUP = {
    "paris": "Europe/Paris",
    "new york": "America/New_York",
    "tokyo": "Asia/Tokyo",
    "londres": "Europe/London",
    "fort-de-france": "America/Martinique",
    "abidjan": "Africa/Abidjan",
    "sydney": "Australia/Sydney"
}

@app.route("/")
def heure():
    ville = request.args.get("ville", DEFAULT_CITY).lower()
    timezone = TIMEZONE_LOOKUP.get(ville)
    
    if not timezone:
        return f"❌ Ville inconnue : {ville}"
    
    url = f"https://timeapi.io/api/Time/current/zone?timeZone={timezone}"
    response = requests.get(url)

    if response.status_code != 200:
        return f"⛔ Impossible de récupérer l'heure pour {ville}."

    data = response.json()
    heure = data.get("time")  # format "HH:mm:ss"

    if not heure:
        return "⛔ Données d'heure invalides reçues."

    heure_court = heure[:5]  # Garde HH:mm

    ville_affichée = ville.title()
    return f"🕒 Il est {heure_court} à {ville_affichée}"

if __name__ == "__main__":
    app.run()
