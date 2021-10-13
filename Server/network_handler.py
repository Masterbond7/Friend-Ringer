# Importing libraries
import socket   # Networking
import time     # Timestamp

from load_data import load_data # Load data

def handle_connection(server):
    try:
        # Accept connection
        client, address = server.accept()

        # State that a device has connected
        print("Connected to: {ip}:{port}".format(ip=address[0], port=address[1]))

        # Receive the message from the arduino
        message = client.recv(1024).decode().replace("\r\n", "")

        # Load data
        data = load_data()

        # Dissect the message
        clientdata = {}
        command = message.split("|")[0] # Split the message and set the first string as command

        # Handle init command (format: init|<name>) (returns: <id>)
        if command == "init":
            # Give out an ID
            newID = str(len(data))
            clientdata["id"] = newID
            client.send(newID.encode("ASCII"))
            print("Given out id {id}".format(id=newID))

            # Clientdata
            command, clientdata["name"] = message.split("|")
            clientdata["last_conn"] = int(time.time())
            clientdata["active"] = True
            clientdata["ringing"] = False

            # Add their name to the database
            data.append(clientdata)

            # Display the newly acquired information as well as all the data stored
            print("Connection ID: {id}, Name: {name}".format(id=clientdata["id"], name=clientdata["name"]))
            print(data, end="\n\n")

        # Handle edit command (format: edit|<id>|<new name>) (returns: )
        elif command == "edit":
            # Clientdata
            command, clientdata["id"], clientdata["name"] = message.split("|")
            clientdata["last_conn"] = int(time.time())
            clientdata["active"] = True
            clientdata["ringing"] = False

            # Get the name and ID data, and store/update it in the data variable
            if not any(userdata["id"] == clientdata["id"] for userdata in data):
                data.append(clientdata)
            else:
                data[int(clientdata["id"])] = clientdata
        
            # Display the newly acquired information as well as all the data stored
            print("Connection ID: {id}, Name: {name}".format(id=clientdata["id"], name=clientdata["name"]))
            print(data, end="\n\n")

        # Handle view command (format: view|<id>) (retruns: <ringing>)
        elif command=="view":
            # Split the message
            command, clientdata["id"] = message.split("|")

            # Make the user active
            data[int(clientdata["id"])]["last_conn"] = int(time.time())
            data[int(clientdata["id"])]["active"] = True

            # Send the result (0/1)
            client.send(str(int(data[int(clientdata["id"])]["ringing"])).encode("ASCII"))

        # Close the connection
        client.close()

    # Stop errors from crashing the program (mostly to stop me being stupid while manually testing)
    except Exception as e:
        print("An error has occurred,"+str(e))
        try: client.send("ERROR".encode("ASCII")); client.close()
        except: print("Unable to inform client of error.")


    
    # Returning everything (just in case)
    return server, data
