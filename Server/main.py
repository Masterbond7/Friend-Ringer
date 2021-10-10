# Importing libraries
print("Importing Libraries")
import socket

# Creating data
data = []

# Starting socket
print("Starting socket")
server = socket.socket()
host = ""
port = 6000

# Binding socket
print("Binding socket")
server.bind((host, port))

# Start listening
print("Listening on port {port}".format(port=port))
server.listen(1)

# Main loop
while True:
    try:
        clientdata = {}
        client, address = server.accept()

        print("Connected to: {ip}:{port}".format(ip=address[0], port=address[1]))
        
        clientdata["id"], clientdata["name"] = client.recv(1024).decode().replace("\r\n", "").split("|")
        if not any(userdata["id"] == clientdata["id"] for userdata in data):
            data.append(clientdata)
        else:
            data[int(clientdata["id"])] = clientdata

        print("Connection ID: {id}, Name: {name}".format(id=clientdata["id"], name=clientdata["name"]))
        print(data, end="\n\n")
        client.close()
    except Exception as e:
        print("An error has occured,"+str(e))

# Close socket
server.close()