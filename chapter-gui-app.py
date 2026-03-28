import os
import tkinter as tk
from tkinter import ttk, scrolledtext
import mysql.connector
import requests
from PIL import Image, ImageTk
from io import BytesIO
import threading

class Warhammer40kApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Warhammer 40K Chapter Browser")
        self.root.geometry("1000x700")

        # Variablen
        self.chapter_var = tk.StringVar()
        self.chapters = []
        self.chapter_images = {}  # Cache für Bilder

        # Hauptcontainer
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Linke Seite - Chapter Liste
        left_frame = ttk.Frame(main_frame, padding="5", relief="groove", borderwidth=1)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=(0, 10))

        # Suchfeld
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(search_frame, text="Suche:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_chapters)

        refresh_button = ttk.Button(search_frame, text="↻", width=3, command=self.load_chapters)
        refresh_button.pack(side=tk.RIGHT)

        # Chapter Liste
        ttk.Label(left_frame, text="Chapter:").pack(anchor=tk.W)
        self.chapter_listbox = tk.Listbox(left_frame, width=30, height=20)
        self.chapter_listbox.pack(fill=tk.BOTH, expand=True)
        self.chapter_listbox.bind('<<ListboxSelect>>', self.show_chapter_details)

        # Rechte Seite - Chapter Details
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Oberer Teil - Überschrift und Bild
        top_frame = ttk.Frame(right_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        self.title_label = ttk.Label(top_frame, text="", font=("Helvetica", 16, "bold"))
        self.title_label.pack(side=tk.LEFT)

        # Rahmen für Bild
        self.image_frame = ttk.Frame(right_frame, width=200, height=200)
        self.image_frame.pack(side=tk.TOP, anchor=tk.CENTER, pady=10)

        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(expand=True)

        # Mittlerer Teil - Details
        details_frame = ttk.Frame(right_frame)
        details_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Zwei Spalten für Details
        left_details = ttk.Frame(details_frame)
        left_details.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        right_details = ttk.Frame(details_frame)
        right_details.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Linke Spalte
        self.homeworld_label = self.create_detail_field(left_details, "Heimatwelt:")
        self.leader_label = self.create_detail_field(left_details, "Anführer:")
        self.champion_label = self.create_detail_field(left_details, "Champion:")
        self.primarch_label = self.create_detail_field(left_details, "Primarch:")
        self.legion_label = self.create_detail_field(left_details, "Legion:")

        # Rechte Spalte
        self.successor_label = self.create_detail_field(right_details, "Nachfolgekapitel:")
        self.founding_label = self.create_detail_field(right_details, "Gründung:")
        self.colors_label = self.create_detail_field(right_details, "Farben:")
        self.weapons_label = self.create_detail_field(right_details, "Waffen:")

        # Unterer Teil - Beschreibung
        desc_frame = ttk.LabelFrame(right_frame, text="Beschreibung")
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.description_text = scrolledtext.ScrolledText(desc_frame, wrap=tk.WORD, height=6)
        self.description_text.pack(fill=tk.BOTH, expand=True)

        # Statusleiste
        self.status_bar = ttk.Label(root, text="Bereit", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Laden der Daten
        self.load_chapters()

    def create_detail_field(self, parent, label_text):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)

        label = ttk.Label(frame, text=label_text, width=15)
        label.pack(side=tk.LEFT)

        value_label = ttk.Label(frame, text="")
        value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        return value_label

    def db_connection(self):
        """Datenbankverbindung herstellen"""
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.environ.get("DB_PASSWORD", ""),
            database="warhammer40k",
            port="3308"
        )

    def load_chapters(self):
        """Lade alle Kapitel aus der Datenbank"""
        self.update_status("Lade Kapitel...")

        try:
            db = self.db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT id, name FROM chapters ORDER BY name")
            self.chapters = cursor.fetchall()
            db.close()

            self.update_status(f"{len(self.chapters)} Kapitel geladen")
            self.update_chapter_list()
        except Exception as e:
            self.update_status(f"Fehler beim Laden der Kapitel: {e}")

    def update_chapter_list(self):
        """Aktualisiere die Chapter-Liste im UI"""
        self.chapter_listbox.delete(0, tk.END)

        for chapter in self.chapters:
            self.chapter_listbox.insert(tk.END, chapter['name'])

        if self.chapters:
            self.chapter_listbox.select_set(0)
            self.show_chapter_details(None)

    def filter_chapters(self, event=None):
        """Filtere die Kapitel basierend auf der Sucheingabe"""
        search_term = self.search_entry.get().lower()

        try:
            db = self.db_connection()
            cursor = db.cursor(dictionary=True)

            if search_term:
                cursor.execute("SELECT id, name FROM chapters WHERE name LIKE %s ORDER BY name", (f"%{search_term}%",))
            else:
                cursor.execute("SELECT id, name FROM chapters ORDER BY name")

            self.chapters = cursor.fetchall()
            db.close()

            self.update_chapter_list()
            self.update_status(f"{len(self.chapters)} Kapitel gefunden")
        except Exception as e:
            self.update_status(f"Fehler beim Filtern: {e}")

    def show_chapter_details(self, event=None):
        """Zeige Details zu einem ausgewählten Kapitel"""
        selection = self.chapter_listbox.curselection()

        if not selection:
            return

        selected_index = selection[0]
        if selected_index < 0 or selected_index >= len(self.chapters):
            return

        selected_chapter = self.chapters[selected_index]
        chapter_id = selected_chapter['id']

        self.update_status(f"Lade Details für {selected_chapter['name']}...")

        try:
            db = self.db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM chapters WHERE id = %s", (chapter_id,))
            chapter = cursor.fetchone()
            db.close()

            if not chapter:
                self.update_status("Kapitel nicht gefunden")
                return

            # UI aktualisieren
            self.title_label.config(text=chapter['name'])

            # Details aktualisieren
            self.homeworld_label.config(text=chapter.get('homeworld', 'Unbekannt'))
            self.leader_label.config(text=chapter.get('leader', 'Unbekannt'))
            self.champion_label.config(text=chapter.get('champion', 'Unbekannt'))
            self.primarch_label.config(text=chapter.get('primarch', 'Unbekannt'))
            self.legion_label.config(text=chapter.get('legion', 'Unbekannt'))

            self.successor_label.config(text=chapter.get('successor_chapter', 'Unbekannt'))
            self.founding_label.config(text=chapter.get('founding', 'Unbekannt'))
            self.colors_label.config(text=chapter.get('colors', 'Unbekannt'))
            self.weapons_label.config(text=chapter.get('weapons', 'Unbekannt'))

            # Beschreibung
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(tk.END, chapter.get('description', 'Keine Beschreibung verfügbar.'))

            # Bild laden (im Hintergrund)
            self.image_label.config(image=None)  # Bild entfernen während wir laden
            if chapter.get('image_url'):
                threading.Thread(target=self.load_image, args=(chapter['image_url'], chapter_id)).start()

            self.update_status(f"Kapitel {chapter['name']} geladen")
        except Exception as e:
            self.update_status(f"Fehler beim Laden der Details: {e}")

    def load_image(self, url, chapter_id):
        """Lade das Bild im Hintergrund und aktualisiere die UI"""
        if not url:
            return

        try:
            if chapter_id in self.chapter_images:
                self.display_image(self.chapter_images[chapter_id])
                return

            response = requests.get(url)
            image = Image.open(BytesIO(response.content))

            # Bild skalieren
            max_size = (200, 200)
            image.thumbnail(max_size, Image.LANCZOS)

            # In Tkinter-Format konvertieren
            tk_image = ImageTk.PhotoImage(image)

            # Bild cachen
            self.chapter_images[chapter_id] = tk_image

            # Im UI anzeigen
            self.display_image(tk_image)
        except Exception as e:
            print(f"Fehler beim Laden des Bildes: {e}")

    def display_image(self, tk_image):
        """Zeigt das Bild in der UI an"""
        # Muss im Hauptthread ausgeführt werden
        self.root.after(0, lambda: self.image_label.config(image=tk_image))

    def update_status(self, message):
        """Aktualisiere die Statusleiste"""
        self.status_bar.config(text=message)
        print(message)  # Auch in der Konsole ausgeben

if __name__ == "__main__":
    root = tk.Tk()
    app = Warhammer40kApp(root)
    root.mainloop()
