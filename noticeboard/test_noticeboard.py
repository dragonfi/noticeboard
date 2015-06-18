import os
import json
import tempfile
import unittest

from noticeboard import noticeboard


class TestNoticeboard(unittest.TestCase):
    def setUp(self):
        self.fd, noticeboard.app.config["DATABASE"] = tempfile.mkstemp()
        noticeboard.app.config["TESTING"] = True
        self.app = noticeboard.app.test_client()
        noticeboard.init_db()

    def tearDown(self):
        os.close(self.fd)
        os.unlink(noticeboard.app.config["DATABASE"])

    def decode_json(self, resp):
        return json.loads(resp.data.decode('utf-8'))

    def test_no_note_by_default(self):
        resp = self.app.get("/api/v1/notes")
        data = self.decode_json(resp)
        self.assertEqual(data["notes"], [])

    def test_creating_note_with_text(self):
        text = "Foo Bar Baz"
        resp = self.app.get("/api/v1/notes/create/{}".format(text))
        data = self.decode_json(resp)
        self.assertEqual(data["note"]["text"], text)

    def test_created_note_can_be_retrieved(self):
        text = "Hello World!"
        resp = self.app.get("/api/v1/notes/create/{}".format(text))
        created_note = self.decode_json(resp)["note"]

        resp = self.app.get("/api/v1/notes/{}".format(created_note["id"]))
        retrieved_note = self.decode_json(resp)["note"]
        self.assertEqual(retrieved_note, created_note)

    def test_created_note_shows_up_in_notes(self):
        text = "Hello, 世界!"
        resp = self.app.get("/api/v1/notes/create/{}".format(text))
        note1 = self.decode_json(resp)["note"]

        text = "This is fun!"
        resp = self.app.get("/api/v1/notes/create/{}".format(text))
        note2 = self.decode_json(resp)["note"]

        resp = self.app.get("/api/v1/notes")
        notes = self.decode_json(resp)["notes"]
        self.assertIn(note1, notes)
        self.assertIn(note2, notes)

    def test_deleted_node_is_not_listed_in_notes(self):
        text = "Hello, 世界!"
        resp = self.app.get("/api/v1/notes/create/{}".format(text))
        note = self.decode_json(resp)["note"]

        self.app.get("/api/v1/notes/delete/{}".format(note["id"]))

        resp = self.app.get("/api/v1/notes")
        notes = self.decode_json(resp)["notes"]
        self.assertNotIn(note, notes)
