import sys
import socket
import logging
import time
from multiprocessing import Process

def kirim_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("membuka socket")

    server_address = ('172.18.0.4', 45000)
    logging.warning(f"opening socket {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        message = 'TIME\r\n'
        logging.warning(f"[CLIENT] sending {message}")
        sock.sendall(message.encode())
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            logging.warning(f"[DITERIMA DARI SERVER] {data}")
    finally:
        logging.warning("closing")
        sock.close()

def run_process():
    total_requests = 0  
    start_time = time.time()  
    while time.time() - start_time < 10:  
        process = Process(target=kirim_data)
        process.start()
        process.join()
        total_requests += 1  
    logging.warning(f"Total requests sent: {total_requests}")

if __name__ == '__main__':
    run_process()