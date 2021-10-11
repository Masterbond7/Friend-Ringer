# Importing libraries
import socket   # Networking
import os, json # Saving and loading data

def handle_connection(server, data):
    try:
        # Accept connection
        client, address = server.accept()

        # State that a device has connected
        print("Connected to: {ip}:{port}".format(ip=address[0], port=address[1]))

        # Receive the message from the arduino
        message = client.recv(1024).decode().replace("\r\n", "")

        # Dissect the message
        clientdata = {}
        clientdata["id"], clientdata["name"] = message.split("|")

        # Handle init command
        if clientdata["id"] == "init":
            # Give out an ID
            newID = str(len(data))
            clientdata["id"] = newID
            client.send(newID.encode("ASCII"))
            print("Given out id {id}".format(id=newID))

            # Add their name to the database
            data.append(clientdata)

        # Get the name and ID data and store/update it in the data variable
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
    
    # Returning everything (just in case)
    return server, data
