import paho.mqtt.client as mqtt
import random
import time
import serial

import requests

def postApi(data):
    ip = "TEST"
    port = "5000"

    # Send data to the server
    r = requests.post(f"http://{ip}:{port}/api/postData", json=data)
    print(f"Résultat requete : {r.text}")

# UART
PORT = 'COM6'
UART_SPEED = 9600
ser = serial.Serial()

isSerialOpen = False

# Function to initialize the UART
def initUart(port, speed):

    global isSerialOpen

    ser.port = port
    ser.baudrate = speed
    ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
    ser.parity = serial.PARITY_NONE  # set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
    ser.timeout = None  # block read

    ser.xonxoff = False  # disable software flow control
    ser.rtscts = False  # disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False

    # Try opening the serial port
    try:
        ser.open()
        print(f"Opening serial port: {port} SUCCESS")
        # Change the button text
        isSerialOpen = True
    except serial.SerialException:
        print(f"Serial {port} port not available")

#point="capteur,numero=4 intensity=10"

MQTT_SERVER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "capteur"

client = mqtt.Client() #Création client MQTT

initUart(PORT, UART_SPEED)

while True:
    if isSerialOpen :
        if ser.in_waiting:
            print("Donnée reçue")
            string = ser.readline().decode("ascii")
            # Split the data every 2 characters
            data = [string[i:i+2] for i in range(0, len(string), 2)]
            data = data[:-1]
            data = [chr(int(x)) for x in data]

            joinedData = [
                data[0] + data[1],
                data[2] + data[3] + data[4] + data[5],
                data[6],
                data[7] + data[8],
                data[9] + data[10] + data[11] + data[12],
                data[13:-1],
                data[-1]
            ]

            data = [
                int(joinedData[0]),
                f"{chr(int(joinedData[1][0] + joinedData[1][1]))}{chr(int(joinedData[1][2] + joinedData[1][3]))}",
                int(joinedData[2]),
                f"{chr(int(joinedData[3][0] + joinedData[3][1]))}",
                f"{chr(int(joinedData[4][0] + joinedData[4][1]))}{chr(int(joinedData[4][2] + joinedData[4][3]))}",
                int("".join(joinedData[5])),
                int(joinedData[6])
            ]

            # Calcul de la taille et vérification
            taillePayload = len("".join(list(map(str, data[:-2]))))
            if taillePayload != data[-1]:
                print("Erreur de taille", taillePayload, data[-1])
                break
            else:
                print("Taille OK")
                print(data)



            point = f"capteur,numero={int(data[1])} intensity={int(data[4])},etat={int(data[3])}"
            try :
                client.connect(MQTT_SERVER,MQTT_PORT)
                print("Connection to MQTT server successful")
            except :
                print("Connection to MQTT server failed")
                exit()

            try:
                client.publish(MQTT_TOPIC,point)
                print("Sent")
            except:
                print("Publishing Error")
                exit()

            client.disconnect()
