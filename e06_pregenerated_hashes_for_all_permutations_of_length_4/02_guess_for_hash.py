#!python

import os
import json
import argparse
import pickle
import pathlib

HASHES_DICTIONARY_DIRECTORY = "hashes_dictionary"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('hash', type=str, help="Hash to guess")
    args = parser.parse_args()

    hashes_dict_dir = pathlib.Path(HASHES_DICTIONARY_DIRECTORY).absolute()

    parts_count = 0
    summary_path = os.path.join(hashes_dict_dir, "0_summary.txt")
    with open(summary_path, "r") as summary_file:
        summary_dict = json.load(summary_file)
        parts_count = summary_dict.get("parts_count", 0)

    print(f"Detected parts count: {parts_count}")

    results = []
    if parts_count > 0:
        for i in range(1, parts_count + 1):
            part_name = f"hash_dict.{i}.part.data"
            part_path = os.path.join(hashes_dict_dir, part_name)
            print(f"Inspecting {part_name} ...")
            with open(part_path, "rb") as part_file:
                part_hashes_dict = pickle.load(part_file)
                results += part_hashes_dict.get(args.hash, [])

    print("RESULTS\n-------\n")

    for x in results:
        print(f"{x: >4}")
