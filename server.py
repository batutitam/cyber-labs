
import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("\n--- Incoming HTTP Headers ---")

        for header, value in self.headers.items():
            print(header, ":", value)

        print("-----------------------------")

        message = "Cybersecurity Lab - GET request works!"

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        self.wfile.write(message.encode())

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        content_type = self.headers.get("Content-Type", "")

        print("\n--- POST Request Headers ---")

        for header, value in self.headers.items():
            print(header, ":", value)

        print("----------------------------")

        if "application/json" in content_type:
            try:
                parsed_data = json.loads(post_data.decode())

                print("Username:", parsed_data.get("username"))
                print("Role:", parsed_data.get("role"))

            except json.JSONDecodeError:
                print("Invalid JSON received")

                self.send_response(400)
                self.send_header("Content-type", "text/plain")
                self.end_headers()

                self.wfile.write(b"400 Bad Request: Invalid JSON")
                return

        else:
            print("Received data:", post_data.decode())

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        self.wfile.write(b"POST request received successfully!")


server = HTTPServer(("127.0.0.1", 8000), MyHandler)

print("Server is running on http://127.0.0.1:8000")

server.serve_forever()

