import http.server
import socketserver
import os
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(BASE, 'tasks.json')
AGENDA_FILE = os.path.join(BASE, 'agenda.json')

FILE_MAP = {
    '/api/tasks': TASKS_FILE,
    '/api/agenda': AGENDA_FILE,
}

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        target = FILE_MAP.get(self.path)
        if target:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                with open(target, 'w') as f:
                    json.dump(data, f, indent=2)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

port = int(os.environ.get("PORT", 8000))
with socketserver.TCPServer(("", port), DashboardHandler) as httpd:
    print(f"Dashboard serving on http://localhost:{port}")
    httpd.serve_forever()
