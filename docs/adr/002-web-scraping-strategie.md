# ADR-002: Web-Scraping für Warhammer 40k Daten

**Status:** Accepted  
**Datum:** 2025

## Kontext
Warhammer 40k Kapitel- und Einheitendaten sind auf Fan-Wikis (z.B. Warhammer 40k Wiki, Lexicanum) verfügbar, aber nicht als API. Die Daten werden für die lokale Datenbank benötigt.

## Entscheidung
Python-Scraper (`improved-web-scraper.py`) mit BeautifulSoup/requests für strukturierte Datenextraktion.

## Abgewogene Alternativen
- **Playwright/Selenium:** Für JavaScript-gerenderte Seiten nötig, aber Wiki-Seiten sind meist Server-Side-Rendered
- **Manuelle CSV-Pflege:** `chapters.csv` existiert als Fallback, aber nicht skalierbar
- **Externe API:** Keine offizielle GW-API verfügbar

## Konsequenzen
**Positiv:**
- Automatisierte Datenbeschaffung
- CSV-Export für Backup und Migration
- Keine Abhängigkeit von externen Diensten

**Negativ:**
- Scraper anfällig für Website-Änderungen
- Rechtliche Grauzone bei Scraping urheberrechtlicher Inhalte
- Rate-Limiting muss manuell beachtet werden
