from flask import Flask, jsonify, request, render_template, send_from_directory
import mysql.connector
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get("DB_PASSWORD", ""),
        database="warhammer40k",
        port="3308"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chapters', methods=['GET'])
def get_all_chapters():
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chapters")
    result = cursor.fetchall()
    db.close()
    return jsonify(result)

@app.route('/chapters/<int:chapter_id>', methods=['GET'])
def get_chapter(chapter_id):
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chapters WHERE id = %s", (chapter_id,))
    result = cursor.fetchone()
    db.close()
    return jsonify(result) if result else ('Not found', 404)

@app.route('/chapters/name/<string:chapter_name>', methods=['GET'])
def get_chapter_by_name(chapter_name):
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chapters WHERE name LIKE %s", (f"%{chapter_name}%",))
    result = cursor.fetchall()
    db.close()
    return jsonify(result) if result else ('Not found', 404)

@app.route('/api/image-proxy')
def image_proxy():
    """Proxy für externe Bilder, falls nötig"""
    url = request.args.get('url')
    if not url:
        return "URL Parameter fehlt", 400

    import requests
    try:
        response = requests.get(url)
        return response.content, 200, {'Content-Type': response.headers.get('Content-Type')}
    except Exception as e:
        return str(e), 500


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

if __name__ == '__main__':

    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)


    if not os.path.exists('templates/index.html'):
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Warhammer 40K Chapter API</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>Warhammer 40K Chapter API</h1>
    <p>Verwenden Sie die folgenden Endpunkte:</p>
    <ul>
        <li><a href="/chapters">/chapters</a> - Alle Kapitel anzeigen</li>
        <li>/chapters/1 - Kapitel nach ID anzeigen</li>
        <li>/chapters/name/Ultramarines - Kapitel nach Namen suchen</li>
    </ul>
    <p>Besuchen Sie die <a href="/gui">GUI-Version</a> für eine grafische Anzeige der Daten.</p>
</body>
</html>''')


    if not os.path.exists('static/style.css'):
        with open('static/style.css', 'w', encoding='utf-8') as f:
            f.write('''body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
h1 {
    color: #333;
}
a {
    color: #0066cc;
}''')

    app.run(debug=True)
