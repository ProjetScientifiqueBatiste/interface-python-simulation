import serial
import random
import time
import json
import requests

# API
ip = "172.20.10.3"
port = "5000"

def getData(ip, port):
    address = f"http://{ip}:{port}/api/getData"
    data = requests.get(address)
    data = json.loads(data.text)
    return data

# UART
PORT = 'COM9'
UART_SPEED = 9600
ser = serial.Serial()

isSerialOpen = False

CAESAR_KEY = 1
PROTOCOL_ID = 14

WIDTH = 11
HEIGHT = 6
SENSORS_AMOUNT = WIDTH * HEIGHT

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

# Function to close the UART
def closeUart():

    global isSerialOpen

    ser.close()
    print(f"Closing serial port : {PORT} SUCCESS")
    # Change the button text
    isSerialOpen = False

# Function to send data to the µBit via the UART
def sendUartData(data):
    data += "\n"
    ser.write(data.encode("ascii"))

# Run the app
if __name__ == '__main__':

    initUart(PORT, UART_SPEED)

    while True:

        print("========= UART Data sending START =========")

        try :
            datas = getData(ip, port)
        except :
            print("Error while getting data from the API")
            datas = []

        for capteur in datas:
            idCapteur = str(capteur["idSensor"]).zfill(2)
            if len(idCapteur) <= 2:
                state = int(1 and random.randint(0, 19) != 0)
                intensity = str(capteur["intensite"] if state else 10).zfill(2)

                data = f"{idCapteur}{state}{intensity}"

                print(f"Sending data : {data}")
                sendUartData(data)
                time.sleep(0.1)

        print("========= UART Data sending END =========")

        time.sleep(10)

