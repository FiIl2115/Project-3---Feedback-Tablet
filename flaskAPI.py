from flask import Flask, jsonify, request
import sqlite3
import datetime
from flask_cors import CORS

CORS(app)

app = Flask(name)

DATABASE_FILE = 'mqtt.db'


@app.route('/feedback')
def get_feedback():
    db_conn = sqlite3.connect(DATABASE_FILE)
    sql = "SELECT * FROM sensors_data"

    cursor = db_conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    payload = []

    for row in rows:
        payload.append(row[2])

    print(payload)
    count_1 = payload.count('1 ')
    count_2 = payload.count('2 ')
    count_3 = payload.count('3 ')
    response = {"good": count_1,
                "mid": count_2,
                "bad": count_3}

    return jsonify(response)


@app.route('/feedbacko')
def get_feedbacko():
    db_conn = sqlite3.connect(DATABASE_FILE)
    sql = "SELECT feedback, mac, created_at FROM sensors_data"

    cursor = db_conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    response = []

    for row in rows[::-1]:
        response.append({"feedback": row[0], "mac": row[1], "time": datetime.fromtimestamp(row[2]).strftime(
                         "%A, %B %d, %Y %I:%M:%S")})

    return jsonify(response)


if name == 'main':
    app.run(host="0.0.0.0", debug=True)