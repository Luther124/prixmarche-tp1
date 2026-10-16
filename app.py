"""TP1 - Une application Django minimale tenant dans un seul fichier.

Lancement :  python app.py runserver
Puis ouvrir : http://127.0.0.1:8000/

# aidé par IA (Claude), vérifié par : <votre nom>
"""
import csv
import json
import re
import statistics
import sys
import urllib.error
import urllib.request
from pathlib import Path

from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.utils.html import escape

BASE_DIR = Path(__file__).resolve().parent

# Configuration minimale : pas de projet, pas de settings.py, tout est ici.
settings.configure(
    DEBUG=True,
    SECRET_KEY="tp1-cle-de-developpement-uniquement",
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],  # pour tester depuis un téléphone sur le même Wi-Fi (jamais en production)
)

JSON_LISIBLE = {"ensure_ascii": False, "indent": 2}  # accents lisibles + indentation


def lire_prix():
    """Lit prix.csv et renvoie une liste de dictionnaires (prix converti en entier)."""
    with open(BASE_DIR / "prix.csv", encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))
    for ligne in lignes:
        ligne["prix"] = int(ligne["prix"])
    return lignes


# ---------- Vues ----------

def accueil(request):
    return HttpResponse(
        """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PrixMarché - TP1</title></head>
<body style="font-family: system-ui, sans-serif; margin: 1rem;">
<h1>PrixMarché - TP1</h1>
<ul>
  <li><a href="/bonjour/Yaounde/">/bonjour/Yaounde/</a></li>
  <li><a href="/api/prix">/api/prix</a></li>
  <li><a href="/api/prix?produit=plantain">/api/prix?produit=plantain</a></li>
  <li><a href="/api/prix?ville=Douala">/api/prix?ville=Douala</a></li>
  <li><a href="/population/CMR/">/population/CMR/</a> (bonus, Banque mondiale)</li>
</ul>
</body></html>"""
    )


def bonjour(request, ville):
    # escape() empêche l'injection de HTML via l'URL (ex. /bonjour/<script>...)
    return HttpResponse(f"<h1>Bonjour {escape(ville)} !</h1>")


def api_prix(request):
    """Renvoie les relevés en JSON, filtrables par ?produit=...&ville=...,
    avec la médiane des prix par produit."""
    donnees = lire_prix()

    produit = request.GET.get("produit")
    ville = request.GET.get("ville")
    if produit:
        donnees = [d for d in donnees if d["produit"].lower() == produit.lower()]
    if ville:
        donnees = [d for d in donnees if d["ville"].lower() == ville.lower()]

    if not donnees:
        return JsonResponse(
            {"erreur": "Aucun relevé pour ces critères.", "produit": produit, "ville": ville},
            status=404,
            json_dumps_params=JSON_LISIBLE,
        )

    prix_par_produit = {}
    for d in donnees:
        prix_par_produit.setdefault(d["produit"], []).append(d["prix"])
    medianes = {p: statistics.median(v) for p, v in prix_par_produit.items()}

    return JsonResponse(
        {
            "devise": "XAF",
            "nombre_releves": len(donnees),
            "mediane_par_produit": medianes,
            "releves": donnees,
        },
        json_dumps_params=JSON_LISIBLE,
    )


def population(request, code_pays):
    """Bonus : population la plus récente d'un pays via l'API de la Banque mondiale."""
    # Code ISO3 (CMR, GAB, TCD...) : on valide avant de l'insérer dans une URL.
    if not re.fullmatch(r"[A-Za-z]{3}", code_pays):
        return HttpResponse("Code pays invalide : 3 lettres attendues (ex. CMR).", status=400)

    url = (
        f"https://api.worldbank.org/v2/country/{code_pays}"
        "/indicator/SP.POP.TOTL?format=json&mrnev=1"
    )
    try:
        with urllib.request.urlopen(url, timeout=10) as reponse:
            resultat = json.load(reponse)
        obs = resultat[1][0]  # resultat[0] = métadonnées, resultat[1] = observations
    except (urllib.error.URLError, TimeoutError):
        return HttpResponse("API Banque mondiale injoignable (connexion ?).", status=503)
    except (IndexError, KeyError, TypeError):
        return HttpResponse(f"Aucune donnée pour le pays {escape(code_pays)}.", status=404)

    pays = escape(obs["country"]["value"])
    valeur = f"{obs['value']:,}".replace(",", " ")  # séparateur de milliers à la française
    return HttpResponse(
        f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Population - {pays}</title></head>
<body style="font-family: system-ui, sans-serif; margin: 1rem;">
<h1>Population : {pays}</h1>
<p style="font-size: 2rem; color: #003366;"><strong>{valeur}</strong> habitants</p>
<p>Année : {escape(obs['date'])} · Source : Banque mondiale, indicateur SP.POP.TOTL</p>
<p><a href="/">← Accueil</a></p>
</body></html>"""
    )


# ---------- Routes (l'équivalent de urls.py) ----------

urlpatterns = [
    path("", accueil),
    path("bonjour/<str:ville>/", bonjour),
    path("api/prix", api_prix),
    path("population/<str:code_pays>/", population),
]


if __name__ == "__main__":
    execute_from_command_line(sys.argv)
