import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from translate import translate as trans_word
import tempfile
from anki.collection import Collection as aopen
from anki.exporting import *
from sound import sound
import uuid
import os
from readcsv import process_csv
import io
import subprocess

app = Flask(__name__)
CORS(app)


def _anki_card(front_back_pair_list, output_file):
    (fd, path) = tempfile.mkstemp(suffix=".anki2")
    col = aopen(path)
    col.upgrade_to_v2_scheduler()
    for idx, item in enumerate(front_back_pair_list):
        print(f'Processing item {idx} {item}')
        card = col.newNote()
        # To add sound,use[sound:] format e.g."Test front[sound:test.mp3]"
        sound_uuid = str(uuid.uuid4())
        card["Front"] = f"{item.front}[sound:{sound_uuid}.wav]"
        sound_bytes = sound(item.front, 'glow-speak:fr_siwis')
        with open(os.path.join(col.media.dir(), f"{sound_uuid}.wav"), "wb") as note:
            note.write(sound_bytes)
        card["Back"] = item.back or trans_word(item.front, 'fr', 'en')
        col.addNote(card)

    with open(output_file, 'w') as _:
        pass

    e = AnkiPackageExporter(col)
    e.exportInto(output_file)


@app.route('/csv_to_anki', methods=['POST'])
def csv_to_anki():
    file = request.files['file']
    cvs_fo = io.StringIO(file.read().decode())
    front_back_list = process_csv(cvs_fo)
    output_file_name = os.path.join(os.getcwd(), "tmpdir", f"{uuid.uuid4()}.apkg")
    try:
        _anki_card(front_back_list, output_file_name)
        return send_file(output_file_name, as_attachment=True)
    finally:
        os.unlink(output_file_name)


@app.route('/translate', methods=['POST'])
def translate():
    word = request.json['word']
    sound_bytes = sound(word, 'glow-speak:fr_siwis')
    sound_b64_str = base64.b64encode(sound_bytes).decode('utf-8')
    translation = trans_word(word, 'fr', 'en')

    return jsonify({
        "audio": sound_b64_str,
        "translation": translation
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123)
