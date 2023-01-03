import random
import time
import hashlib
import os

from prettytable import PrettyTable

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

table = PrettyTable()

table.field_names = ["César", "Protocole", "Source", "Destination", "Data type", "Data", "Hash", "Taille"]

CAESAR_KEY = 1
PROTOCOLE = 14

LARGEUR = 10
HAUTEUR = 6
NOMBRE_CAPTEURS = LARGEUR * HAUTEUR

def cipherCaesar(trame, key):
    """ Function to cipher a message with the Caesar cipher """

    for i in range(len(trame)):
        trame[i] = (trame[i] + key) % 256
    
    return trame

def decipherCaesar(trame, key):
    """ Function to decipher a message with the Caesar cipher """

    if type(trame) == list:
        newTrame = trame.copy()
        for i in range(len(newTrame)):
            newTrame[i] = (newTrame[i] - key) % 256
        return newTrame
    else:
        return (trame - key) % 256

def getSensorId(x, y):
    """ Function to get the id of a sensor in the array of sensors """

    idSensor = x + y * LARGEUR
    return idSensor

def createDataRequest(idSensor):
    """
        Function to create a data request
    
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
        *[0]*9,
    ]
    
    # Chiffrement de la requete avec le chiffrement de Caesar
    req = cipherCaesar(req, CAESAR_KEY)
    
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

    # Ajout des lignes du tableau sans et avec le chiffrement de Caesar
    table.add_row([
        "False",
        decipherCaesar(req[0], CAESAR_KEY),
        decipherCaesar(req[1] + req[2], CAESAR_KEY),
        decipherCaesar(req[3], CAESAR_KEY),
        decipherCaesar(req[4], CAESAR_KEY),
        decipherCaesar(req[5:15], CAESAR_KEY),
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

def createRandomSensorArray(largeur, hauteur):
    """ Function to create a random array of sensors """

    array = [[createRandomData() for _ in range(largeur)] for _ in range(hauteur)]
    return array

def checkHash(trame):
    """
        Vérification du hash MD5 par rapport aux données dans la trame
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
