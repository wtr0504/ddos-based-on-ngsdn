#!/usr/bin/python

import socket
# h3a wget http://[2001:1:2::1]:8080/
# h2 /mininet/host-service/httpSimpleServer.py &
class SimpleHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port, 0, 0))
            self.server_socket.listen(5)
            print("HTTP server running on %s, port %d" % (self.host, self.port))

            while True:
                client_socket, client_address = self.server_socket.accept()
                print("Received connection from %s" % str(client_address))
                self.handle_request(client_socket)

        except Exception as e:
            print(str(e))

        finally:
            if self.server_socket:
                self.server_socket.close()
                print("HTTP server closed")

    def handle_request(self, client_socket):
        request_data = client_socket.recv(1024).decode('utf-8')
        request_lines = request_data.split('\n')
        if request_lines:
            method, path, http_version = request_lines[0].strip().split()
            print("HTTP method %s, path: %s, HTTP version: %s" % (method, path, http_version))
            response_body = "<html><body><h1>Hello, World!</h1></body></html>"
            response_headers = [
                "HTTP/1.1 200 OK",
                "Content-Type: text/html",
                "Content-Length: %d" % len(response_body),
                "\n"
            ]
            response = '\n'.join(response_headers) + response_body
            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()
            print("Response sent")

if __name__ == "__main__":
    HOST = ''
    PORT = 8080
    http_server = SimpleHTTPServer(HOST, PORT)
    http_server.start()
