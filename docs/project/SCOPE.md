# Projektscope — WH40K Datenbank

## Problem
Warhammer 40k Spieler möchten schnell auf Informationen zu Space Marine Kapiteln, Einheiten und Fraktionen zugreifen. Die Daten sind verstreut auf verschiedenen Fan-Wikis.

## Lösung
Eine lokale Datenbank mit Web-Interface und Desktop-GUI, die Warhammer 40k Kapitel- und Fraktionsdaten aus Fan-Wikis scraped und übersichtlich aufbereitet.

## In Scope
- Web-Scraping von WH40K Fan-Wikis (Python)
- SQLite-Datenbank für strukturierte Datenhaltung
- Flask-API als Backend
- Web-Interface (HTML-Templates)
- Desktop-GUI mit Tkinter
- CSV-Import/Export für Datenmigration
- pytest-basierte Tests

## Out of Scope
- Offizielle Games Workshop API-Integration
- Multi-User-/Cloud-Betrieb
- Mobile App
- Spielregeln / Punktwerte (nur Lore-Daten)

## Technologie-Stack
| Schicht | Technologie |
|---------|-------------|
| Web-Backend | Python, Flask |
| Datenbank | SQLite |
| Scraping | Python (BeautifulSoup/requests) |
| Desktop-GUI | Python, Tkinter |
| Templates | Jinja2 |
| Tests | pytest |
