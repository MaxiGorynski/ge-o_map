from http.server import HTTPServer, SimpleHTTPRequestHandler

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')  # Allow GET requests
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

# Run the server
httpd = HTTPServer(('localhost', 8000), CORSRequestHandler)
print("Serving on http://localhost:8000 with CORS enabled...")
httpd.serve_forever()
