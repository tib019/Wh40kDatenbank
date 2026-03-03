# ⚔️ Warhammer 40K Chapter Browser

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)

Eine vollständige Webanwendung zur Verwaltung und Anzeige von **Space Marine-Kapiteln** aus dem Warhammer 40.000-Universum. Das Projekt umfasst einen Web-Scraper, eine RESTful API, eine SQLite-Datenbank und ein interaktives Web-Frontend.

---

## 📋 Projektübersicht

| Eigenschaft | Details |
|---|---|
| **Backend** | Python, Flask |
| **Datenbank** | SQLite |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Datenbeschaffung** | Web-Scraper (BeautifulSoup) |
| **API** | RESTful JSON API |

---

## 🚀 Features

- **Datenbank** – Vollständige SQLite-Datenbank mit Space Marine-Kapitel-Informationen
- **Web-Scraper** – Automatisches Befüllen der Datenbank aus Online-Quellen
- **RESTful API** – JSON-Endpunkte für alle Datenbankoperationen
- **Suchfunktion** – Kapitel nach Name, Gründungsjahrhundert und Stammvater filtern
- **Web-GUI** – Interaktives Frontend mit Detailansichten
- **CSV-Import** – Bulk-Import von Kapitel-Daten via CSV

---

## 📁 Projektstruktur

```
Wh40kDatenbank/
├── improved-flask-api.py      # Haupt-Flask-Anwendung mit REST API
├── improved-db-setup.py       # Datenbankinitialisierung und Schema
├── improved-web-scraper.py    # Web-Scraper für Kapitel-Daten
├── improved-csv-import.py     # CSV-Import-Skript
├── web-gui-app.py             # Alternative GUI-Anwendung
├── chapter-gui-app.py         # Desktop-GUI (tkinter)
├── chapters.csv               # Beispiel-Datensatz
├── project-documentation.md  # Vollständige Projektdokumentation
├── templates/                 # Jinja2 HTML-Templates
└── static/                    # CSS, JavaScript, Bilder
```

---

## 🛠️ Installation & Setup

### Voraussetzungen

- Python 3.8+
- pip

### Schnellstart

```bash
# Repository klonen
git clone https://github.com/tib019/Wh40kDatenbank.git
cd Wh40kDatenbank

# Abhängigkeiten installieren
pip install flask beautifulsoup4 requests

# Datenbank initialisieren
python improved-db-setup.py

# (Optional) Daten via Web-Scraper befüllen
python improved-web-scraper.py

# (Optional) CSV-Import
python improved-csv-import.py

# Anwendung starten
python improved-flask-api.py
```

Die Anwendung ist dann unter `http://localhost:5000` erreichbar.

---

## 🔌 API-Endpunkte

| Methode | Endpunkt | Beschreibung |
|---|---|---|
| `GET` | `/api/chapters` | Alle Kapitel abrufen |
| `GET` | `/api/chapters/<id>` | Einzelnes Kapitel |
| `GET` | `/api/chapters/search?q=<query>` | Kapitel suchen |
| `POST` | `/api/chapters` | Neues Kapitel anlegen |
| `PUT` | `/api/chapters/<id>` | Kapitel aktualisieren |
| `DELETE` | `/api/chapters/<id>` | Kapitel löschen |

---

## 📖 Dokumentation

Die vollständige Projektdokumentation befindet sich in [`project-documentation.md`](project-documentation.md) und umfasst Systemarchitektur, Datenbankschema, API-Dokumentation, Frontend-Beschreibung sowie Testszenarien und Sicherheitsaspekte.

---

## 👨‍💻 Autor

**Tobias** – [@tib019](https://github.com/tib019)

---

## 📄 Hinweis

Warhammer 40.000 ist ein eingetragenes Warenzeichen von Games Workshop. Dieses Projekt ist ein inoffizielles Fan-Projekt zu Lern- und Demonstrationszwecken.
