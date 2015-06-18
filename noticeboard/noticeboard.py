#!/usr/bin/env python3

import os
import json
import sqlite3
import datetime
from contextlib import closing
from flask import Flask, g, jsonify, redirect

"""API overview:

/api/notes -> {notes: <list of all notes>}
/api/notes/<id> -> {note: <the note with the given id>}
/api/notes/create/<text> -> OK (Adds a new note to notes with text)
/api/notes/<id>/delete -> OK (Deletes and removes the note from notes)
/api/notes/<id>/update/<text> -> OK (Replace text of note with new text)
"""

app = Flask(__name__)

DATABASE = 'noticeboard.db'
DEBUG = True

app.config.from_object(__name__)


def get_rows(table):
    rows = g.db.execute("select * from {table}".format(table=table))
    rows = [{key: row[key] for key in row.keys()} for row in rows]
    return rows


def get_row(table, row_id):
    cursor = g.db.execute(
        "select * from {table} where id = ?".format(table=table), (row_id,))
    rows = list(cursor)
    if len(rows) != 1:
        raise NotImplementedError
    row = rows[0]
    row = {key: row[key] for key in row.keys()}
    return row


def create_row(table, fields, values):
    fields = tuple(fields)
    values = tuple(values)
    fields_str = ", ".join(fields)
    placeholders = ", ".join(["?" for field in fields])
    query = "insert into {table} ({fields}) values ({values})".format(
        table=table, fields=fields_str, values=placeholders)

    c = g.db.cursor()
    c.execute(query, values)
    g.db.commit()
    return get_row(table, c.lastrowid)


def delete_row(table, row_id):
    g.db.execute("delete from {} where id={}".format(table, row_id))
    g.db.commit()
    return row_id


def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    if not os.path.isfile(app.config["DATABASE"]):
        init_db()
    g.db = connect_db()


@app.route("/")
def hello_world():
    return redirect("static/index.html")


@app.route("/api")
@app.route("/api/v1")
def api_help():
    return jsonify({
        "version": "v1",
        "links": {
            "/api/v1/notes": "List all notes",
            "/api/v1/notes/create/<text>": "Creates new note with <text>",
            "/api/v1/notes/<id>": "Retrieves note matching <id>"}})


@app.route("/api/v1/notes", methods=["GET"])
def notes():
    return jsonify({"notes": get_rows("Notes")})


@app.route("/api/v1/notes/create/<text>", methods=["GET", "POST"])
def ceate_note(text):
    now = datetime.datetime.now()
    new_note = create_row("Notes", ("text", "created"), (text, now))
    return jsonify({"note": new_note})


@app.route("/api/v1/notes/<note_id>", methods=["GET", "POST"])
def return_note(note_id):
    note = get_row("Notes", note_id)
    return jsonify({"note": note})


@app.route("/api/v1/notes/delete/<note_id>", methods=["GET", "POST"])
def delete_note(note_id):
    delete_row("Notes", note_id)
    return jsonify({"deleted_note_id": note_id})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
