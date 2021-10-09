# Importing libraries
print("Importing Libraries")
import socket

# Starting socket
print("Starting socket")
server = socket.socket()
host = "0.0.0.0"
port = 6000

# Binding socket
print("Binding socket")
server.bind((host, port))

# Start listening
print("Listening on port {port}".format(port=port))
server.listen(1)

# Main loop
while True:
    client, address = server.accept()

    print("Connected to: {ip}:{port}".format(ip=address[0], port=address[1]))
    client.send("Hello World!\n".encode("ASCII"))
    client.close()

# Close socket
server.close()