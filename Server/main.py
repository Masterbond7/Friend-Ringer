# Importing libraries
print("Importing Libraries")
import socket                # Networking
import os, json              # Saving and loading data
from threading import Thread # Multithreading
from flask import Flask      # Web server
import waitress              # Web server

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
    while True:
        server, data = handle_connection(server, data)

    # Close socket
    server.close() # NOTE: this code is unreachable

# Defining flask
website = Flask(__name__)

@website.route('/')
def index():
    return "Hello World!"


if __name__ == "__main__":
    flask_thread = Thread(target=lambda: waitress.serve(website, host="0.0.0.0", port=5000))
    networking_thread = Thread(target=thread_networking)

    flask_thread.start(); print("Hosted website")
    networking_thread.start()