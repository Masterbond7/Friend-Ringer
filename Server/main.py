# Importing libraries
print("Importing Libraries")
import socket
import os, json

# Creating data variable
data = []

# Checking if data file exists, if it does, load and display data
print("Checking if data file exists")
if os.path.isfile("data.json"):
    print("Loading data")
    datafile = open("data.json", 'r')
    data = json.load(datafile)
    datafile.close()
    print("Loaded data: {data}".format(data=data), end="\n")

# Starting socket
print("Starting socket")
server = socket.socket()
host = ""
port = 6000

# Binding socket
print("Binding socket")
server.bind((host, port))

# Start listening
server.listen(5)
print("Listening on port {port}".format(port=port))

# Main loop
while True:
    try:
        # Accept connection
        clientdata = {}
        client, address = server.accept()

        # State that a device has connected
        print("Connected to: {ip}:{port}".format(ip=address[0], port=address[1]))

        # Receive the message from the arduino
        message = client.recv(1024).decode().replace("\r\n", "")
        if message == "init":
            # Give out an ID
            newID = str(len(data))
            client.send(newID.encode("ASCII"))
            print("Given out id {id}".format(id=newID))
        else:
            # Get the name and ID data and store/update it in the data variable
            clientdata["id"], clientdata["name"] = message.split("|")
            if not any(userdata["id"] == clientdata["id"] for userdata in data):
                data.append(clientdata)
            else:
                data[int(clientdata["id"])] = clientdata
            
            # Display the newly acquired information as well as all the data stored
            print("Connection ID: {id}, Name: {name}".format(id=clientdata["id"], name=clientdata["name"]))
            print(data, end="\n\n")

        # Save the data in a file
        datafile = open("data.json", 'w')
        json.dump(data, datafile)
        datafile.close()

        # Close the connection
        client.close()

    # Stop errors from crashing the program (mostly to stop me being stupid while manually testing)
    except Exception as e:
        print("An error has occurred,"+str(e))

# Close socket
server.close() # NOTE: this code is unreachable
