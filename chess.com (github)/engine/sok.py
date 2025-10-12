
import http.server
import ssl
import socketserver


CERT = "/home/love/Codes/Web/chess.com/engine/_cert.pem"
KEY  = "/home/love/Codes/Web/chess.com/engine/_key"
PASS = "password"

HOST = "localhost"
PORT = 8443

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Hello from a self-signed TLS server!</h1>")

# Create an SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(CERT, KEY, PASS)

# Create the server
httpd = socketserver.TCPServer((HOST, PORT), MyHandler)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
print(f"Serving HTTPS on {HOST}:{PORT}")
httpd.serve_forever()
