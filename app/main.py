from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Hello World"})

@app.route("/search")
def search():
    username = request.args.get("username", "")

    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE users (username TEXT)")
    cursor.execute("INSERT INTO users VALUES ('demo-user')")

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchall()

    connection.close()

    return jsonify({"results": result})

if __name__ == "__main__":
    app.run(debug=False)
