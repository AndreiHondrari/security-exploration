import socket
import time


def main() -> None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    HOST = '127.0.0.1'
    PORT = 7777
    client.connect((HOST, PORT))

    REQUEST = "GET / HTTP/1.1\n\n"
    print("SLOW SEND ", REQUEST)

    REQUEST_BYTES = REQUEST.encode()

    for x in REQUEST_BYTES:
        x_byte = x.to_bytes(1, 'big')
        print("B ", x_byte)
        client.send(x_byte)
        time.sleep(0.5)

    reply = client.recv(1024)
    print("REPLY")
    print(reply.decode())

    print("Final wait before socket close (2s) ...")
    time.sleep(2)

    print("Sending KEK at the end ...")
    client.send(b"KEK /\n\n")
    print("REPLY")
    print(reply.decode())

    client.close()


if __name__ == "__main__":
    main()
