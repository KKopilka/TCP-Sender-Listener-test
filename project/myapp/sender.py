import socket
import os
import random
import time

class MySender:
    MAX_SIZE = 8 * 1024 * 1024 * 1024  # 8 ГБ
    
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port

    def _generate_random_bytes(self):
        size = random.randint(1, MySender.MAX_SIZE)
        return os.urandom(size)

    def send_data(self):
        data = self._generate_random_bytes()
        data_size = len(data)
        
        for attempt in range(3):
            try:
                with socket.create_connection((self.server_address, self.server_port)) as sock:
                    size_bytes = data_size.to_bytes((data_size.bit_length() + 7) // 8, byteorder='big')
                    sock.sendall(size_bytes + data)
                    print("Data sent successfully.")
                    return
            except (ConnectionRefusedError, OSError):
                if attempt < 2:
                    print("Retrying connection...")
                    time.sleep(10)
                else:
                    print("Failed to connect to the server.")
