# Warhammer 40K Chapter Browser
## Projektdokumentation

**Version:** 1.0
**Datum:** 28.02.2025
**Autor:** [Ihr Name]

---

## Inhaltsverzeichnis

1. [Projektübersicht](#1-projektübersicht)
2. [Funktionsumfang](#2-funktionsumfang)
3. [Systemarchitektur](#3-systemarchitektur)
4. [Installation und Konfiguration](#4-installation-und-konfiguration)
5. [Datenbankstruktur](#5-datenbankstruktur)
6. [API-Dokumentation](#6-api-dokumentation)
7. [Frontend-Dokumentation](#7-frontend-dokumentation)
8. [Webscraping-Komponente](#8-webscraping-komponente)
9. [Testszenarien](#9-testszenarien)
10. [Sicherheitsaspekte](#10-sicherheitsaspekte)
11. [Erweiterungsmöglichkeiten](#11-erweiterungsmöglichkeiten)
12. [Glossar](#12-glossar)

---

## 1. Projektübersicht

### 1.1 Projektbeschreibung

Der "Warhammer 40K Chapter Browser" ist eine Webanwendung, die Informationen über Space Marine-Kapitel aus dem Warhammer 40.000-Universum anzeigt. Die Anwendung ermöglicht es Benutzern, Kapitel zu durchsuchen, zu filtern und detaillierte Informationen zu jedem Kapitel abzurufen.

### 1.2 Projektziele

- Erstellung einer Datenbank zur Speicherung von Warhammer 40K Chapter-Informationen
- Entwicklung einer RESTful API zum Zugriff auf die Daten
- Implementierung eines Webscrapers zum automatischen Befüllen der Datenbank
- Gestaltung einer benutzerfreundlichen Weboberfläche
- Bereitstellung verschiedener Filteroptionen und Suchfunktionen

### 1.3 Zielgruppe

- Warhammer 40K-Fans und Spieler
- Hobbyisten, die Informationen über Space Marine-Kapitel benötigen
- Entwickler, die die API für eigene Anwendungen nutzen möchten

### 1.4 Technologiestack

- **Backend:** Python, Flask (Webframework)
- **Datenbank:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Webscraping:** Beautiful Soup, Requests
- **Entwicklungsumgebung:** [Beschreibung Ihrer IDE]
- **Versionskontrolle:** [Beschreibung Ihres Versionskontrollsystems]

---

## 2. Funktionsumfang

### 2.1 Kernfunktionen

- **Kapitelübersicht:** Anzeige aller verfügbaren Space Marine-Kapitel
- **Detailansicht:** Ausführliche Informationen zu jedem Kapitel
- **Suchfunktion:** Filterung der Kapitel nach Namen oder Eigenschaften
- **Sortieroptionen:** Sortierung der Kapitel nach verschiedenen Kriterien
- **API-Endpunkte:** RESTful-API für den programmatischen Zugriff auf die Daten
- **Automatische Datenbeschaffung:** Webscraper zum Füllen der Datenbank

### 2.2 Benutzeroberfläche

- Responsive Design für die Nutzung auf verschiedenen Geräten
- Intuitive Navigation und Benutzerführung
- Visuelle Darstellung der Kapitel-Embleme und Farbschemen
- Dynamisches Laden von Inhalten ohne vollständige Seitenneuladen
- Statusanzeigen und Ladeindikatoren für bessere Benutzererfahrung

---

## 3. Systemarchitektur

### 3.1 Architekturübersicht

Die Anwendung folgt einer klassischen 3-Schichten-Architektur:

1. **Präsentationsschicht:** HTML, CSS und JavaScript für die Benutzeroberfläche
2. **Anwendungsschicht:** Flask-Backend mit API-Endpunkten
3. **Datenschicht:** MySQL-Datenbank zur Speicherung der Kapitelinformationen

Zusätzlich gibt es die Datenbeschaffungskomponente (Webscraper), die unabhängig von der Hauptanwendung läuft und die Datenbank mit Informationen befüllt.

### 3.2 Komponentendiagramm

```
+-----------------------+    +-------------------------+    +------------------+
|   Benutzeroberfläche  |    |   Backend (Flask API)   |    |     Datenbank    |
|                       |    |                         |    |                  |
|   - HTML5             |    |   - API-Endpunkte       |    |   - MySQL        |
|   - CSS3              |<-->|   - Datenabfragen       |<-->|   - Chapter Table|
|   - JavaScript        |    |   - Datenaufbereitung   |    |                  |
+-----------------------+    +-------------------------+    +------------------+
                                        ^
                                        |
                                        v
                              +---------------------+
                              |  Webscraper-Modul   |
                              |                     |
                              |  - Beautiful Soup   |
                              |  - Requests         |
                              +---------------------+
```

###