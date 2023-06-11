import socket
import threading
from datetime import datetime
import pytz
import logging

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address, server):
        self.connection = connection
        self.address = address
        self.server = server 
        threading.Thread.__init__(self)

    def run(self):
        while True:
            data = self.connection.recv(1024)
            if data:
                request = data.decode().strip()
                if data.startswith(b'TIME') and data.endswith(b'\r\n'):
                    jakarta_timezone = pytz.timezone("Asia/Jakarta")
                    current_time = datetime.now(jakarta_timezone).strftime("%H:%M:%S")
                    response = f"JAM {current_time}\r\n"
                    self.connection.sendall(response.encode())
                    self.server.update_response_count() 
            else:
                break
        self.connection.close()

class TimeServer(threading.Thread):
    def __init__(self, host, port):
        self.the_clients = []
        self.client_count = 0
        self.response_count = 0 
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        logging.info(f"Time server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            logging.info(f"New connection from {client_address[0]}:{client_address[1]}")

            client_thread = ProcessTheClient(client_socket, client_address, self)  
            client_thread.start()
            self.the_clients.append(client_thread)
            self.client_count += 1
            logging.info(f"Total clients connected: {self.client_count}")
            
    def update_response_count(self):
        self.response_count += 1
        logging.info(f"Total responses sent: {self.response_count}")
        

def main():
    host = '0.0.0.0'  
    port = 45000
    server = TimeServer(host, port)
    server.start()

if __name__ == "__main__":
    main()