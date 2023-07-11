import tempfile
import argparse
import readcsv
import uuid

from anki.collection import Collection as aopen
from anki.exporting import *
from sound import sound
from translate import translate
import os


def create_anki_collection(front_back_pair_list, output_file):
    (fd, path) = tempfile.mkstemp(suffix=".anki2")
    col = aopen(path)
    col.upgrade_to_v2_scheduler()
    for idx, item in enumerate(front_back_pair_list):
        print(f'Processing item {idx} {item}')
        card = col.newNote()
        # To add sound, use [sound:] format e.g. "Test front [sound:test.mp3]"
        sound_uuid = str(uuid.uuid4())
        card["Front"] = f"{item.front} [sound:{sound_uuid}.wav]"
        sound_bytes = sound(item.front, 'glow-speak:fr_siwis')
        with open(os.path.join(col.media.dir(), f"{sound_uuid}.wav"), "wb") as note:
            note.write(sound_bytes)
        card["Back"] = item.back or translate(item.front, 'fr', 'en')
        col.addNote(card)

    with open(output_file, 'w') as _:
        pass
    e = AnkiPackageExporter(col)
    e.exportInto(output_file)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=str)
    parser.add_argument("input_cvs_file", type=str)
    parser.add_argument("--output_file_name", type=str, required=False, default="result")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    front_back_pairs = readcsv.read_and_process_csv_file(args.input_cvs_file)
    create_anki_collection(front_back_pairs, os.path.join(args.output_dir, f"{args.output_file_name}.apkg"))
    print('Bye!')
