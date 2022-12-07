from tkinter import *

import serial
import time

# Graphic interface for the send program
master = Tk()
scales=list()
Nscales=60

for i in range(Nscales):
    w=Scale(master, from_=9, to=0) # creates widget
    w.grid(row=i//10,column=i-(i//10)*10)
    scales.append(w) # stores widget in scales list

# send serial message 
# Don't forget to establish the right serial port ******** ATTENTION
# SERIALPORT = "/dev/ttyUSB0"
SERIALPORT = "COM6"
BAUDRATE = 115200
ser = serial.Serial()

def initUART():     
        if serialButton['text'] == "Open Serial":
            # ser = serial.Serial(SERIALPORT, BAUDRATE)
            ser.port=SERIALPORT
            ser.baudrate=BAUDRATE
            ser.bytesize = serial.EIGHTBITS #number of bits per bytes
            ser.parity = serial.PARITY_NONE #set parity check: no parity
            ser.stopbits = serial.STOPBITS_ONE #number of stop bits
            ser.timeout = None          #block read

            # ser.timeout = 0             #non-block read
            # ser.timeout = 2              #timeout block read
            ser.xonxoff = False     #disable software flow control
            ser.rtscts = False     #disable hardware (RTS/CTS) flow control
            ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
            #ser.writeTimeout = 0     #timeout for write
            print ("Starting Up Serial Monitor")
            try:
                print(f"Opening serial port: {SERIALPORT}")
                ser.open()
            except serial.SerialException:
                print("Serial {} port not available".format(SERIALPORT))
                exit()
            serialButton['text'] = "Close Serial"
            b['state'] = 'normal'
        else:
            print(f"Closing serial port : {SERIALPORT}")
            ser.close()
            serialButton['text'] = "Open Serial"
            b['state'] = 'disabled'


def sendUARTMessage(msg):
    msg += "\n"
    ser.write(msg.encode())
    # print("Message <" + msg + "> sent to micro-controller." )

def read_scales():
    cptScale = 0
    b['state'] = 'disabled'
    print("Reading values : ")
    for i in range(Nscales):
        column = i-(i//10)*10
        row = i//10
        messageSent = f"({row},{column},{scales[i].get()})"
        if (scales[i].get()>0) :
            print(f"Active scale {i} : {messageSent}")
        # print(f"Message sent to the µBit: {messageSent}")
        sendUARTMessage(messageSent)
        cptScale += 1
        # time.sleep(0.5)
    print(f"Number of scales sent : {cptScale}")


    b['state'] = 'normal'

b=Button(master,text="Send Values",highlightcolor="blue",command=read_scales, state="disabled") # button to read values
serialButton=Button(master,text="Open Serial",highlightcolor="blue",command=initUART) # button to read values
b.grid(row=6,column=7,columnspan = 3)
serialButton.grid(row=6, column=0, columnspan = 3)

# initUART()

mainloop()