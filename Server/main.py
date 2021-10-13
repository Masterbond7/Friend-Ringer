# Importing libraries
print("Importing Libraries")
import socket                            # Networking
import os, json                          # Saving and loading data
from threading import Thread             # Multithreading
from flask import Flask, render_template # Web server
import waitress                          # Web server
import time                              # Timestamp & delay

from network_handler import handle_connection


# Defining function to load data
def load_data():
    # Checking if data file exists, if it does, load and display data
    print("Checking if data file exists")
    if os.path.isfile("data.json"):
        print("Loading data")
        datafile = open("data.json", 'r')
        data = json.load(datafile)
        datafile.close()
        print("Loaded data: {data}".format(data=data), end="\n")
    
        # Return the data
        return data
    
    else:
        print("No data file")
        return []


# Defining network thread
def thread_networking():
    # Creating data variable
    data = load_data()

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

    # Main networking loop
    ##old_data = []
    while True:
        server, data = handle_connection(server, data)
        if True:#not data == old_data:
            # Save the data in a file
            datafile = open("data.json", 'w')
            json.dump(data, datafile)
            datafile.close()

            ##old_data = data

    # Close socket
    server.close() # NOTE: this code is unreachable

# Defining thread to determine if devices are "active"
def thread_is_active():
    # Creating old_data variable
    old_data = []

    while True:
        # Updating data variable
        data = load_data()

        if not data == []:
            UNIX_time = int(time.time())
            for entry in data:
                if entry["last_conn"] + 30 <= UNIX_time:
                    entry["active"] = False
                else:
                    entry["active"] = True
                
            # Save the data in a file
            if not old_data == data:
                datafile = open("data.json", 'w')
                json.dump(data, datafile)
                datafile.close()
                old_data = data
        time.sleep(5)


# Defining flask
website = Flask(__name__)

@website.route('/')
def index():
    return render_template("index.jinja", data=load_data())


if __name__ == "__main__":
    #flask_thread = Thread(target=lambda: waitress.serve(website, host="0.0.0.0", port=5000))
    networking_thread = Thread(target=thread_networking)
    is_active_thread = Thread(target=thread_is_active)

    #flask_thread.start(); print("Hosted website")
    networking_thread.start()
    is_active_thread.start()
    website.run(host="", port=5000, debug=True)