import random
import time
import hashlib
import os

from prettytable import PrettyTable

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

table = PrettyTable()

table.field_names = ["César", "Protocole", "Source", "Destination", "Data type", "Data", "Hash", "Taille"]

CLE_CESAR = 1
PROTOCOLE = 14

LARGEUR = 10
HAUTEUR = 6
NOMBRE_CAPTEURS = LARGEUR * HAUTEUR

# Function to cipher a message with the Cesar cipher
def cipherCesar(trame, key):
    for i in range(len(trame)):
        trame[i] = (trame[i] + key) % 256
    
    return trame

# Function to decipher a message with the Cesar cipher
def decipherCesar(trame, key):
    if type(trame) == list:
        newTrame = trame.copy()
        for i in range(len(newTrame)):
            newTrame[i] = (newTrame[i] - key) % 256
        return newTrame
    else:
        return (trame - key) % 256

# Function to get the id of a sensor in the array of sensors
def getSensorId(x, y):
    idSensor = x + y * LARGEUR
    return idSensor

# Function to create a data request
def createDataRequest(idSensor):
    # req = {Protocole}{source}{destination}{data type}{intensity}
    """
        Protocole : 1 byte ==> 14
        source : 2 byte ==> idSensor
        destination : 2 byte ==> 1
        data type : 1 byte ==> 1
        intensity : 1 byte ==> between 0 and 9
    """
    req = [
        PROTOCOLE, # Protocole
        idSensor // 256, # Source ("// 256" to get the first byte)
        idSensor % 256, # Source ("% 256" to get the second byte)
        1, # Destination
        1, # Data type
        createRandomData(), # Intensity (between 0 and 9
    ]

    # Ajout de 9 cases vides à la suite pour l'évolution du projet
    for _ in range(9):
        req.append(0)
    
    # Chiffrement de la requete avec le chiffrement de Cesar
    req = cipherCesar(req, CLE_CESAR)
    
    # Ajout du hash MD5 sur 12 octets à la fin
    hash = hashlib.md5(bytes(req)).digest()
    for i in range(len(hash)):
        req.append(hash[i])
    
    # Calcul de la taille de la requete sans le hash
    taille = len(req) - len(hash)

    # Ajout de la taille de la requete sur 1 octet à la fin
    req.append(taille)

    # Ajout de la requete dans le tableau
    if table.get_string() != "":
        table.clear_rows()

    # Ajout des lignes du tableau sans et avec le chiffrement de Cesar
    table.add_row([
        "False",
        decipherCesar(req[0], CLE_CESAR),
        decipherCesar(req[1] + req[2], CLE_CESAR),
        decipherCesar(req[3], CLE_CESAR),
        decipherCesar(req[4], CLE_CESAR),
        decipherCesar(req[5:15], CLE_CESAR),
        " ".join(map(str, req[15:-1])),
        req[-1]
    ])

    table.add_row([
        "True",
        req[0],
        req[1] + req[2],
        req[3],
        req[4],
        req[5:15],
        " ".join(map(str, req[15:-1])),
        req[-1]
    ])

    return req
    
# One data is : (x, y, POWER)
# x and y are between 0 and 9
# POWER is between 0 and 9
def createRandomData():
    return random.randint(0, 9)

# Function to send data to the µBit via the UART
def sendCliData(msg):
    print(*msg, sep=' ')

def displayArray(array):
    for i in range(len(array)):
        print(array[i])

def createRandomSensorArray(largeur, hauteur):
    array = [[createRandomData() for _ in range(largeur)] for _ in range(hauteur)]
    return array

def checkHash(trame):
    # Vérification du hash MD5 par rapport aux données dans la trame
    """
    Data : 15 octets
    Hash : 16 octets
    Taille : 1 octet
    """
    hashTrame = " ".join(map(str, trame[15:-1]))
    print("Hash présent dans la trame : ", hashTrame)
    hash = hashlib.md5(bytes(trame[:-17])).digest()
    hash = " ".join(map(str, hash))
    print("Hash re-calculé : ", hash)

    print("Les deux hash sont identiques" if hashTrame == hash else "Les deux hash sont différents")   

def main():
    # Init the array of sensors
    capteurs = createRandomSensorArray(LARGEUR, HAUTEUR)
    displayArray(capteurs)

    # Periodic sending of a data from a random sensor in the array
    while True:
        clear()
        # Get a random sensor
        x = random.randint(0, LARGEUR - 1)
        y = random.randint(0, HAUTEUR - 1)
        idSensor = getSensorId(x, y)
        # Create the data 
        data = createDataRequest(idSensor)
        # print the data
        print(table)

        # Vérification du hash MD5 par rapport aux données dans la trame
        checkHash(data)

        # Wait a bit
        time.sleep(5)

# Run the app
if __name__ == '__main__':
    main()
