import socket


def main() -> None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    HOST = '127.0.0.1'
    PORT = 7777
    client.connect((HOST, PORT))

    REQUEST = "GET / HTTP/1.1\n\n"
    print("SEND ", REQUEST)
    client.send(REQUEST.encode())

    reply = client.recv(1024)
    print("REPLY")
    print(reply.decode())

    client.close()


if __name__ == "__main__":
    main()
