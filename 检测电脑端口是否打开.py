import socket


for port in range(1, 65535):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.01)
    state = sock.connect_ex(("192.168.0.1", port))
    if 0 == state:
        print("port: {} is open".format(port))
    sock.close()