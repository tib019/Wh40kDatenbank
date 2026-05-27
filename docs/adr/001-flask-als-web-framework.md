# ADR-001: Flask als Web-Framework

**Status:** Accepted  
**Datum:** 2025

## Kontext
Die WH40K-Datenbank benötigt ein leichtgewichtiges Web-Backend, das Web-Scraping-Ergebnisse als REST-API bereitstellt und eine einfache Web-Oberfläche rendert.

## Entscheidung
Flask als minimalistisches Python-Web-Framework.

## Abgewogene Alternativen
- **FastAPI:** Moderner, aber für dieses Projekt überdimensioniert (keine Async-Anforderungen)
- **Django:** Zu viel Overhead (ORM, Admin, etc.) für ein kleines Hobby-Projekt
- **Bottle:** Noch minimalistischer, aber kleineres Ökosystem

## Konsequenzen
**Positiv:**
- Minimale Konfiguration, schneller Einstieg
- Gut geeignet für Prototypen und kleinere Datenbank-Apps
- Ausreichend für REST-API + Template-Rendering

**Negativ:**
- Kein eingebautes ORM (manuelles SQL oder SQLAlchemy nötig)
- Nicht für große Traffic-Mengen geeignet
