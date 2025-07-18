import json
import os
import string
import random
from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)

app.debug = True

def generate_random_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_started")
def get_started():
    id = generate_random_id(6)
    return redirect(f"/notes/{id}")

@app.route("/notes/<id>")
def notes(id):
    print(f"Notepad ID: {id}")
    return render_template("notes.html", id=id)

@app.route("/api", methods=["GET", "POST"])
def api():
    if request.method == "GET":
        id = request.args.get("id")
        
        if not id:
            return jsonify({"error": "Missing 'id' parameter"}, 400)
        
        print(f"API request. ID: {id}.")

        DATA_FILE = "/workspaces/sticky-notes/static/data/db.json"
        if not os.path.exists(DATA_FILE):
            return jsonify({
                "status": "ok",
                "id": id,
                "data": []
            })

        with open(DATA_FILE, "r") as f:
            try:
                all_notes = json.load(f)
            except json.JSONDecodeError:
                return jsonify({"error": "Malformed JSON file."}), 500
            
        user_notes = [note for note in all_notes if note.get("id") == id]
            
        return jsonify({
            "status": "ok",
            "id": 1,
            "data": user_notes
        })
    
    if request.method == "POST":
        id = request.args.get("id")

        if not id:
            return jsonify({"error": "Missing 'id' parameter"}, 400)
        
        print("Post request recived.")

        data = request.get_json()
        
        if not data or not isinstance(data, list):
            return jsonify({
                "error": "Invalid or missing JSON data."
            }, 400)

        try:
            DATA_FILE = "/workspaces/sticky-notes/static/data/db.json"
            if not DATA_FILE:
                return jsonify({
                    "error": "Failed to find data file."
                }, 400)
            
            with open(DATA_FILE, "r") as f:
                all_notes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_notes = []
        
        all_notes = [note for note in all_notes if note.get("id") != id]

        for idx, note in enumerate(data, start=1):
            all_notes.append({
                "id": id,
                "note-id": idx,
                "title": note.get("title", ""),
                "body": note.get("body", "")
            })

        with open(DATA_FILE, "w") as f:
            json.dump(all_notes, f, indent=1)

        return jsonify({
            "status": "success"
        }, 201)


if __name__ == '__main__':
    app.run('0.0.0.0', 8080)