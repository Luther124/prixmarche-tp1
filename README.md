# TP1 — De la page statique à la première API

Programmation Web en Python · ISSEA AS3 · 2026-2027

## Contenu

| Fichier        | Rôle                                                                 |
|----------------|----------------------------------------------------------------------|
| `releve.html`  | Formulaire de relevé des prix (étape 2)                              |
| `style.css`    | Mise en forme « mobile d'abord » + media query pour écran large (étape 3) |
| `prix.csv`     | Données de prix (fictives)                                           |
| `app.py`       | Application Django tenant dans un seul fichier (étapes 4 et 5)       |

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Lancement

```bash
python app.py runserver
```

| Route                               | Résultat                                             |
|-------------------------------------|------------------------------------------------------|
| `/`                                 | Page d'accueil avec les liens                        |
| `/bonjour/<ville>/`                 | « Bonjour <ville> ! »                                |
| `/api/prix`                         | Tous les relevés en JSON + médiane par produit       |
| `/api/prix?produit=plantain`        | Filtre par produit (et/ou `?ville=Douala`) ; 404 JSON si aucun résultat |
| `/population/CMR/` *(bonus)*        | Population du pays via l'API de la Banque mondiale   |

Pour la page statique : ouvrir `releve.html` dans le navigateur, puis F12 → mode « appareil » (Ctrl+Maj+M).

## Usage de l'IA

<!-- 5 lignes à rédiger vous-même : outil utilisé, pour quelles parties,
     ce que vous avez vérifié/modifié, ce que vous avez appris, limites constatées. -->
* Outil : Claude (Claude Code).
* Ce que l’IA a produit : tous les fichiers (releve.html, style.css, prix.csv, app.py). Elle a aussi corrigé l’erreur `git remote` et expliqué les étapes GitHub.
* Ce que j'ai verifié: j'ai testé chaque route, relu le fichier `app.py`, tester le mode mobile.
* Ce que j'ai appris ou constaté : l’ambiguïté entre Django et app.py dans l’énoncé, l’intérêt de `escape()`, ou le fait que les données de `prix.csv` sont fictives.
