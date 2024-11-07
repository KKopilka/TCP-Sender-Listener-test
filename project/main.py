import sys
from myapp.sender import MySender
from myapp.listener import MyListener

def main():
    role = sys.argv[1]
    
    if role == "sender":
        server_address = sys.argv[2]
        server_port = int(sys.argv[3])
        sender = MySender(server_address, server_port)
        sender.send_data()
    elif role == "listener":
        ip_address = sys.argv[2]
        port = int(sys.argv[3])
        listener = MyListener(ip_address, port)
        listener.start_server()
    else:
        print("Invalid role specified. Use 'sender' or 'listener'.")

if __name__ == "__main__":
    main()
