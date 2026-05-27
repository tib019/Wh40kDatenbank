# ADR-003: Tkinter für Desktop-GUI

**Status:** Accepted  
**Datum:** 2025

## Kontext
Neben der Web-Oberfläche soll eine native Desktop-GUI für lokale Nutzung ohne Browser angeboten werden.

## Entscheidung
Tkinter (Python Standard Library) für die Desktop-GUI (`chapter-gui-app.py`).

## Abgewogene Alternativen
- **PyQt/PySide:** Professionellere GUIs, aber zusätzliche Abhängigkeit und Lizenzfragen
- **wxPython:** Native Look-and-Feel, aber komplexere API
- **Electron:** Web-Technologien, aber sehr schwer für ein kleines Python-Projekt

## Konsequenzen
**Positiv:**
- In Python Standard Library enthalten, keine zusätzliche Installation
- Ausreichend für einfache Datenbankansichten und CRUD-Operationen

**Negativ:**
- Veraltetes Look-and-Feel
- Eingeschränkte UI-Möglichkeiten
