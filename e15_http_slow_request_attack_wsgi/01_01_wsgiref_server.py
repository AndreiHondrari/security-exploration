
from wsgiref.simple_server import make_server

from wsgi_app import application


def main() -> None:
    print("** SERVER START **")
    HOST = '127.0.0.1'
    PORT = 7777
    httpd = make_server(HOST, PORT, application)
    print(f"Listen on {(HOST, PORT,)} ...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nCtrl+C detected!")

    print("** SERVER END **")


if __name__ == "__main__":
    main()
