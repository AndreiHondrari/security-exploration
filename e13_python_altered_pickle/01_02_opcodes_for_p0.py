import pickletools
import string

from pickletools import OpcodeInfo

from functools import partial
from typing import List

hprint = partial(print, "\n#")


def opcodes_for_protocol(protocol: int) -> List[OpcodeInfo]:
    return list(
        filter(
            lambda opc: opc.proto == protocol,
            pickletools.opcodes
        )
    )


def main() -> None:
    print("Obtain opcodes info per protocol")
    p0_opcodes = opcodes_for_protocol(0)

    for opc in p0_opcodes:
        if opc.code in string.printable:
            printable_code = opc.code
        else:
            printable_code = str(hex(ord(opc.code)))

        hprint(f"{opc.name} | {printable_code}")
        print(opc.doc)


if __name__ == "__main__":
    main()
