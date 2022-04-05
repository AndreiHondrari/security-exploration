import pickle
import pickletools
from functools import partial

hprint = partial(print, "\n#")


class X:
    pass


def main() -> None:

    x1 = X()
    data = pickle.dumps(x1, protocol=0)

    hprint("Pickle data raw")
    print(data)

    hprint("Pickle data decoded")
    print(data.decode())
    print()

    print("Preoptimised")
    pickletools.dis(data)

    hprint("Optimised")
    data = pickletools.optimize(data)
    pickletools.dis(data)

    hprint("LOAD")
    pickle.loads(data)


if __name__ == "__main__":
    main()
