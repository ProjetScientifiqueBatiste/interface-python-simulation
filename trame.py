import random
import time
import hashlib
import os

from prettytable import PrettyTable

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

table = PrettyTable()

table.field_names = ["César", "protocol", "Source", "Destination", "Data type", "Data", "Hashed Caesar", "Taille"]

CAESAR_KEY = 1
PROTOCOL_ID = 14

WIDTH = 10
HEIGHT = 6
SENSORS_AMOUT = WIDTH * HEIGHT

def cipherCaesar(frame, key):
    """ Function to cipher a message with the Caesar cipher """

    for i in range(len(frame)):
        frame[i] = (frame[i] + key) % 256
    
    return frame

def decipherCaesar(frame, key):
    """ Function to decipher a message with the Caesar cipher """

    if type(frame) == list:
        newFrame = frame.copy()
        for i in range(len(newFrame)):
            newFrame[i] = (newFrame[i] - key) % 256
        return newFrame
    else:
        return (frame - key) % 256

def getSensorId(x, y):
    """ Function to get the id of a sensor in the array of sensors """

    idSensor = x + y * WIDTH
    return idSensor

def createDataRequest(idSensor):
    """
        Function to create a data request
    
        protocol : 1 byte ==> 14
        source : 2 byte ==> idSensor
        destination : 2 byte ==> 1
        data type : 1 byte ==> 1
        intensity : 1 byte ==> between 0 and 9
    """
    req = [
        PROTOCOL_ID,
        idSensor // 256, # Source ("// 256" to get the first byte)
        idSensor % 256, # Source ("% 256" to get the second byte)
        1, # Destination
        1, # Data type
        createRandomData(), # Intensity (between 0 and 9)
        # *[0]*9, # Other data slots
    ]
    
    # Apply the Caesar cipher on the request
    req = cipherCaesar(req, CAESAR_KEY)
    
    # sha1 hash 
    hash = hashlib.sha1(bytes(req)).digest()[:5]
    for i in range(len(hash)):
        req.append(hash[i])
        
    # Data size
    size = len(req) - len(hash)
    req.append(size)

    # Clear the table
    if table.get_string() != "":
        table.clear_rows()

    # Add the data to the table
    table.add_row([
        "False",
        decipherCaesar(req[0], CAESAR_KEY),
        decipherCaesar(req[1] + req[2], CAESAR_KEY),
        decipherCaesar(req[3], CAESAR_KEY),
        decipherCaesar(req[4], CAESAR_KEY),
        decipherCaesar(req[5], CAESAR_KEY),
        " ".join(map(str, req[6:-1])),
        req[-1]
    ])

    table.add_row([
        "True",
        req[0],
        req[1] + req[2],
        req[3],
        req[4],
        req[5],
        " ".join(map(str, req[6:-1])),
        req[-1]
    ])

    return req
    
def createRandomData():
    """
        One data is : (x, y, POWER)
        x and y are between 0 and 9
        POWER is between 0 and 9
    """
    return random.randint(0, 9)

def displayArray(array):
    """ Function to display the array of sensors """

    for i in range(len(array)):
        print(array[i])

def createRandomSensorArray(width, height):
    """ Function to create a random array of sensors """

    array = [[createRandomData() for _ in range(width)] for _ in range(height)]
    return array

def checkHash(frame):
    """
        Check the sha1 hash according to the data in the frame
        Data : 15 bytes
        Hash : 6 bytes
        Size : 1 byte
    """

    hashFrame = " ".join(map(str, frame[6:-1]))
    print("Hash présent dans la trame : ", hashFrame)
    # Calculate the hash
    print(frame)
    hash = hashlib.sha1(bytes(frame[:5])).digest()[:5]
    hash = " ".join(map(str, hash))
    print("Hash re-calculé : ", hash)

    print("Les deux hash sont identiques" if hashFrame == hash else "Les deux hash sont différents")   

def main():
    # Init the array of sensors
    sensors = createRandomSensorArray(WIDTH, HEIGHT)
    displayArray(sensors)

    # Periodic sending of a data from a random sensor in the array
    while True:
        clear()
        # Get a random sensor
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        idSensor = getSensorId(x, y)
        # Create the data 
        data = createDataRequest(idSensor)
        # print the data
        print(table)

        # Check the hash
        checkHash(data)

        # Wait 
        time.sleep(5)

# Run the app
if __name__ == '__main__':
    main()
