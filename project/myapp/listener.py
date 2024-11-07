import socket

class MyListener:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    def _receive_data(self, conn):
        data_size_bytes = conn.recv(8)
        data_size = int.from_bytes(data_size_bytes, byteorder='big')
        data = conn.recv(data_size)
        
        print(f"Received data of size: {data_size}")
        print(f"First 16 bytes (in hex): {data[:16].hex()}")

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.ip_address, self.port))
            server_socket.listen()
            print(f"Listening on {self.ip_address}:{self.port}")
            
            while True:
                conn, _ = server_socket.accept()
                with conn:
                    self._receive_data(conn)
