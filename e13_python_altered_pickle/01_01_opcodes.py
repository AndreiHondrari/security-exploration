import pickletools
import string

from pickletools import OpcodeInfo

from functools import partial
from typing import List, Dict

hprint = partial(print, "\n#")


def opcodes_for_protocol(protocol: int) -> List[OpcodeInfo]:
    return list(
        filter(
            lambda opc: opc.proto == protocol,
            pickletools.opcodes
        )
    )


def display_protocol_opcodes(
    opcodes: List[OpcodeInfo]
) -> None:
    for opc in opcodes:
        short_doc = opc.doc[:50].replace('\n', '')

        if opc.code in string.printable:
            printable_code = opc.code
        else:
            printable_code = str(hex(ord(opc.code)))

        print(f"{printable_code: <5} | {opc.name: >20} | \t{short_doc} ...")


def main() -> None:
    print("Obtain opcodes info per protocol")
    protocols_opcodes: Dict[int, List[OpcodeInfo]] = {}
    for i in range(5):
        protocols_opcodes[i] = opcodes_for_protocol(i)

    for i in range(5):
        hprint(f"Opcodes for protocol #{i}")
        display_protocol_opcodes(protocols_opcodes[i])


if __name__ == "__main__":
    main()
