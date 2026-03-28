import os
import mysql.connector

def create_database():

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get("DB_PASSWORD", ""),
        port="3308"
    )
    cursor = db.cursor()


    cursor.execute("CREATE DATABASE IF NOT EXISTS warhammer40k")


    cursor.execute("USE warhammer40k")


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chapters (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        homeworld VARCHAR(255),
        leader VARCHAR(255),
        champion VARCHAR(255),
        weapons VARCHAR(255),
        image_url TEXT,
        legion VARCHAR(255),
        primarch VARCHAR(255),
        successor_chapter VARCHAR(255),
        founding VARCHAR(255),
        colors VARCHAR(255),
        description TEXT,
        UNIQUE KEY unique_name (name)
    )
    """)

    db.commit()
    db.close()

if __name__ == "__main__":
    create_database()
    print("Datenbank und Tabelle wurden erfolgreich erstellt.")
