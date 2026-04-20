from flask import Flask
import sqlite3

app = Flask(__name__)

DB_PATH = "/data/app.db"

@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS visits (count INTEGER)")
    cursor.execute("SELECT count FROM visits")

    row = cursor.fetchone()
    if row is None:
        cursor.execute("INSERT INTO visits VALUES (1)")
        count = 1
    else:
        count = row[0] + 1
        cursor.execute("UPDATE visits SET count = ?", (count,))

    conn.commit()
    conn.close()

    return f"Nombre de visites : {count}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
