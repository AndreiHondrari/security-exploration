#!python

import pickle
import string
import itertools
import os
import hashlib
import pathlib
import json

from collections import defaultdict


SIZE = 4
ALPHANUM_CHARS = string.digits + string.ascii_letters
HASHES_DICTIONARY_DIRECTORY = "hashes_dictionary"

if __name__ == "__main__":
    hashes_dict_dir = pathlib.Path(HASHES_DICTIONARY_DIRECTORY).absolute()

    # clear dir and generate new
    if hashes_dict_dir.exists():
        for hash_part_file in hashes_dict_dir.iterdir():
            hash_part_file.unlink()

        hashes_dict_dir.rmdir()

    os.mkdir(hashes_dict_dir)

    # permutations iterator
    chars_permutations = itertools.permutations(ALPHANUM_CHARS, SIZE)

    candidate_count = 0
    hash_dict_part_count = 0
    candidates_hash_dictionary = defaultdict(list)

    try:
        while True:
            candidate = "".join(next(chars_permutations))
            candidate_hash = hashlib.sha256(
                candidate.encode('utf-8')
            ).hexdigest()
            candidates_hash_dictionary[candidate_hash].append(candidate)

            candidate_count += 1

            if candidate_count >= 1_000_000:
                hash_dict_part_count += 1

                part_name = f"hash_dict.{hash_dict_part_count}.part.data"
                part_path = os.path.join(hashes_dict_dir, part_name)

                print(f"Dumping {part_name} at {candidate}")
                with open(part_path, "wb") as part_file:
                    pickle.dump(candidates_hash_dictionary, part_file)

                candidates_hash_dictionary = defaultdict(list)
                candidate_count = 0

    except StopIteration:
        print("\n----------\nWE'RE DONE\n")

    print(f"Finalizing ...")

    summary_path = os.path.join(hashes_dict_dir, "0_summary.txt")
    with open(summary_path, "w") as summary_file:
        json.dump({"parts_count": hash_dict_part_count}, summary_file)
