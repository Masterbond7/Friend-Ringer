# Importing libraries
import os, json # Load data

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