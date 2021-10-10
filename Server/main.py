# Importing libraries
print("Importing Libraries")
import socket
import json

# Creating data variable
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
server.listen(5)

# Main loop
while True:
    try:
        # Accept connection
        clientdata = {}
        client, address = server.accept()

        # State that a device has connected
        print("Connected to: {ip}:{port}".format(ip=address[0], port=address[1]))
        
        # Get the name and ID data and store/update it in the data variable
        clientdata["id"], clientdata["name"] = client.recv(1024).decode().replace("\r\n", "").split("|")
        if not any(userdata["id"] == clientdata["id"] for userdata in data):
            data.append(clientdata)
        else:
            data[int(clientdata["id"])] = clientdata

        # Save the data in a file
        datafile = open("data.json", 'w')
        json.dump(data, datafile)
        datafile.close()

        # Display the newly acquired information as well as all the data stored
        print("Connection ID: {id}, Name: {name}".format(id=clientdata["id"], name=clientdata["name"]))
        print(data, end="\n\n")

        # Close the connection
        client.close()
    
    # Stop errors from crashing the program (mostly to stop me being stupid while manually testing)
    except Exception as e:
        print("An error has occurred,"+str(e))

# Close socket
server.close() # NOTE: this code is unreachable