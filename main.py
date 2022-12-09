import serial
import random

from ursina import *

window.title = 'Ursina Serial Port'
window.borderless = False
window.size = (400, 700)
window.fps_cap = 30

# UART
PORT = 'COM9'
UART_SPEED = 115200
ser = serial.Serial()

isSerialOpen = False

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
        serial_port_button.text = "Close Serial Port"
        isSerialOpen = True
        serialStateText.text = f'Serial port {ser.port} opened'
        serialStateText.color = color.green
    except serial.SerialException:
        print(f"Serial {port} port not available")
        serialStateText.text = f'Serial port {ser.port} not available'
        serialStateText.color = color.red

# Function to close the UART
def closeUart():

    global isSerialOpen

    ser.close()
    print(f"Closing serial port : {PORT} SUCCESS")
    # Change the button text
    serial_port_button.text = "Open Serial Port"
    isSerialOpen = False
    serialStateText.text = f'Serial port {PORT} not opened'
    serialStateText.color = color.red

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

# Text to display the current state of the serial port
serialStateText = Text(text=f'Serial port {PORT} not opened', position=(-0.1, 0.4), color=color.red)

# Create a button to open the serial port, at the left of the window
serial_port_button = Button(text='Open Serial Port',
                            scale=(0.2, 0.1), position=(0, -0.2))

# Create a button to send data, at the bottom of the window
send_data_button = Button(
    text='Send Data', scale=(0.2, 0.1), position=(0, 0.2))

# List representing the buttons
buttons = [serial_port_button, send_data_button]

# Create the on_click function for each buttons
for button in buttons:

    # Apply the on_click function to each button
    def on_click(b=button):

        # Check which button is clicked using the match statement
        match b.text:
            # Serial Port opening and closing
            case 'Open Serial Port':
                print("Opening serial port")
                initUart(PORT, UART_SPEED)
            case 'Close Serial Port':
                print("Closing serial port")
                closeUart()

            # Send data to the µBit
            case 'Send Data':
                if isSerialOpen:
                    print("========= UART Data sending START =========")
                    for _ in range(TAILLE_DATA):
                        msg = createData()
                        print(f"Sending data to the µBit via UART : {msg}")
                        sendUartData(msg)
                    print("========= UART Data sending END =========")
                else:
                    print("Serial port not opened, please open it first")

    button.on_click = on_click


def update():
    # This function is called every frame

    # Check if there is data to read
    if isSerialOpen :
        if ser.in_waiting:
            dataRead = ser.readline()
            print(f"Received data from the µBit via UART : {dataRead}")
    
    if isSerialOpen :
        send_data_button.enable()
    else :
        send_data_button.disable()

# Run the app
if __name__ == '__main__':
    app.run()
