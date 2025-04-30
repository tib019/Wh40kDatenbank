import mysql.connector
import csv

def import_csv_data():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tonne96",
        database="warhammer40k",
        port="3308"
    )

    cursor = db.cursor()


    cursor.execute("TRUNCATE TABLE chapters")

    with open('chapters.csv', encoding='utf-8') as file:
        csv_data = csv.reader(file)
        next(csv_data)
        for row in csv_data:

            cleaned_data = [field.strip('"') if field.startswith('"') and field.endswith('"') else field for field in row]


            cursor.execute('''
                REPLACE INTO chapters
                (name, homeworld, leader, champion, weapons, image_url, legion, primarch, successor_chapter, founding, colors)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                cleaned_data[0],  # name
                cleaned_data[1],  # homeworld
                cleaned_data[2],  # leader
                cleaned_data[3],  # champion
                cleaned_data[4],  # weapons
                cleaned_data[5],  # image_url
                cleaned_data[6],  # legion
                cleaned_data[7],  # primarch
                cleaned_data[8],  # successor_chapter
                cleaned_data[9],  # founding
                cleaned_data[10]  # colors
            ))

    db.commit()
    db.close()
    print(f"CSV-Daten erfolgreich importiert.")

if __name__ == "__main__":
    import_csv_data()
