from flask import Flask, jsonify
import sqlite3
import os
import time

app = Flask(__name__)

DB_PATH = "/data/app.db"
BACKUP_PATH = "/backup"


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


@app.route("/count")
def count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS visits (count INTEGER)")
    cursor.execute("SELECT count FROM visits")

    row = cursor.fetchone()
    count = row[0] if row else 0

    conn.close()

    return f"Nombre de visites : {count}"


@app.route("/status")
def status():
    # 🔹 Nombre d'événements
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS visits (count INTEGER)")
    cursor.execute("SELECT count FROM visits")

    row = cursor.fetchone()
    count = row[0] if row else 0

    conn.close()

    # 🔹 Infos backup
    last_backup_file = None
    backup_age_seconds = None

    if os.path.exists(BACKUP_PATH):
        files = [f for f in os.listdir(BACKUP_PATH) if f.endswith(".db")]

        if files:
            files.sort(
                key=lambda f: os.path.getmtime(os.path.join(BACKUP_PATH, f)),
                reverse=True
            )

            last_backup_file = files[0]

            file_path = os.path.join(BACKUP_PATH, last_backup_file)
            backup_age_seconds = int(time.time() - os.path.getmtime(file_path))

    return jsonify({
        "count": count,
        "last_backup_file": last_backup_file,
        "backup_age_seconds": backup_age_seconds
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
