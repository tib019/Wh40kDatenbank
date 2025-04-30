import requests
from bs4 import BeautifulSoup
import mysql.connector
import time

def scrape_chapters():
    urls = [
        "https://wh40k-de.lexicanum.com/wiki/Ultramarines",
        "https://wh40k-de.lexicanum.com/wiki/Blood_Angels",
        "https://wh40k-de.lexicanum.com/wiki/Dark_Angels",
        "https://wh40k-de.lexicanum.com/wiki/Space_Wolves",
        "https://wh40k-de.lexicanum.com/wiki/Imperial_Fists(Space_Marines)",
        "https://wh40k-de.lexicanum.com/wiki/White_Scars",
        "https://wh40k-de.lexicanum.com/wiki/Salamanders",
        "https://wh40k-de.lexicanum.com/wiki/Raven_Guard",
        "https://wh40k-de.lexicanum.com/wiki/Iron_Hands",
        "https://wh40k-de.lexicanum.com/wiki/Crimson_Fists",
        "https://wh40k-de.lexicanum.com/wiki/Black_Templars",
        "https://wh40k-de.lexicanum.com/wiki/Deathwatch",
        "https://wh40k-de.lexicanum.com/wiki/Blood_Ravens"
    ]

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tonne96",
        database="warhammer40k",
        port="3308"
    )
    cursor = db.cursor()

    for url in urls:
        print(f"Scraping: {url}")
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            page_title = soup.find('h1', {'id': 'firstHeading'}).text.strip()
            chapter_name = page_title

            infobox = soup.find('table', {'class': 'infobox'})
            data = {}
            description = ""

            content_div = soup.find('div', {'id': 'mw-content-text'})
            if content_div:
                paragraphs = content_div.find_all('p', limit=3)
                description = ' '.join([p.text.strip() for p in paragraphs])

            if infobox:
                for row in infobox.find_all('tr'):
                    cells = row.find_all(['th', 'td'])
                    if len(cells) == 2:
                        key = cells[0].text.strip()
                        value = cells[1].text.strip()
                        data[key] = value

            homeworld = data.get('Heimatwelt', '')
            leader = data.get('Meister', '') or data.get('Ordensmeister', '')
            primarch = data.get('Primarch', '')
            weapons = data.get('Hauptwaffe', '') or data.get('Waffen', '')
            founding = data.get('Gründung', '')
            colors = data.get('Farben', '')
            legion = data.get('Legion', '')

            image_element = infobox.find('img') if infobox else None
            image_url = None
            if image_element:
                image_src = image_element.get('src', '')
                image_url = 'https://wh40k-de.lexicanum.com' + image_src if image_src.startswith('/') else image_src

            cursor.execute('''
                UPDATE chapters
                SET
                    homeworld = CASE WHEN %s != '' THEN %s ELSE homeworld END,
                    leader = CASE WHEN %s != '' THEN %s ELSE leader END,
                    primarch = CASE WHEN %s != '' THEN %s ELSE primarch END,
                    weapons = CASE WHEN %s != '' THEN %s ELSE weapons END,
                    image_url = CASE WHEN %s IS NOT NULL THEN %s ELSE image_url END,
                    legion = CASE WHEN %s != '' THEN %s ELSE legion END,
                    founding = CASE WHEN %s != '' THEN %s ELSE founding END,
                    colors = CASE WHEN %s != '' THEN %s ELSE colors END,
                    description = CASE WHEN %s != '' THEN %s ELSE description END
                WHERE name = %s
            ''', (
                homeworld, homeworld,
                leader, leader,
                primarch, primarch,
                weapons, weapons,
                image_url, image_url,
                legion, legion,
                founding, founding,
                colors, colors,
                description, description,
                chapter_name
            ))

            if cursor.rowcount == 0:
                cursor.execute('''
                    INSERT IGNORE INTO chapters
                    (name, homeworld, leader, weapons, image_url, primarch, legion, founding, colors, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    chapter_name, homeworld, leader, weapons, image_url, primarch, legion, founding, colors, description
                ))

            print(f"Daten für {chapter_name} verarbeitet.")
            db.commit()

            time.sleep(1)

        except Exception as e:
            print(f"Fehler beim Scrapen von {url}: {e}")

    db.close()
    print("Web Scraping abgeschlossen.")

if __name__ == "__main__":
    scrape_chapters()
