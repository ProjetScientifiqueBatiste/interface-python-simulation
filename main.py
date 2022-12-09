import serial
import random

from ursina import *

window.title = 'Ursina Serial Port'
window.borderless = False
window.size = (400, 700)
window.fps_cap = 60

# UART
PORT = 'COM9'
UART_SPEED = 115200
ser = serial.Serial()

sendState = False

TAILLE_DATA = 10

# One data is : (x, y, POWER)
# x and y are between 0 and 9
# POWER is between 0 and 9
def createData():
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    power = random.randint(0, 9)
    msg = f"{x},{y},{power}"
    return msg

# Function to initialize the UART
def initUart(port, speed):

    global sendState

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
        serial_port_button.text = "Close Serial Port"
        sendState = True
    except serial.SerialException:
        print(f"Serial {port} port not available")
        exit()

# Function to close the UART
def closeUart():

    global sendState

    ser.close()
    print(f"Closing serial port : {PORT} SUCCESS")
    # Change the button text
    serial_port_button.text = "Open Serial Port"
    sendState = False

# Function to send data to the µBit via the UART
def sendUartData(msg):
    msg += "\n"
    ser.write(msg.encode())


# Create an instance of Ursina
if __name__ == '__main__':
    app = Ursina()

"""
Button list :
    - Open Serial Port
    - Close Serial Port
    - Send Data
"""

# Create a button to open the serial port, at the left of the window
serial_port_button = Button(text='Open Serial Port',
                            scale=(0.2, 0.1), position=(0, -0.2))

# Create a button to send data, at the right of the window
send_data_button = Button(
    text='Send Data', scale=(0.2, 0.1), position=(0, 0.2))

# List representing the buttons
buttons = [serial_port_button, send_data_button]

# Create the on_click function for each buttons
for button in buttons:
    def on_click(b=button):
        match b.text:
            case 'Open Serial Port':
                print("Opening serial port")
                initUart(PORT, UART_SPEED)
            case 'Close Serial Port':
                print("Closing serial port")
                closeUart()
            case 'Send Data':
                if sendState:
                    print("========= UART Data sending =========")
                    for _ in range(TAILLE_DATA):
                        msg = createData()
                        print(f"Sending data to the µBit via UART : {msg}")
                        sendUartData(msg)
                else:
                    print("Serial port not opened, please open it first")

    button.on_click = on_click


# Run the app
if __name__ == '__main__':
    app.run()
