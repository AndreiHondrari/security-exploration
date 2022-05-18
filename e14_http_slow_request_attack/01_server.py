
from http.server import HTTPServer, BaseHTTPRequestHandler, HTTPStatus


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "plain/text")
        self.end_headers()
        self.wfile.write(b"Czesc mundo!\n")

    def do_KEK(self) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "plain/text")
        self.end_headers()
        self.wfile.write(b"This is KEEEEKKKK!\n")


def main() -> None:
    print("** SERVER START **")

    server_address = ('', 7777)

    print(f"Listen on {server_address} ...")

    httpd = HTTPServer(server_address, RequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nCtrl+C detected!")

    print("** SERVER END **")


if __name__ == "__main__":
    main()
