from ursina import *

window.title = 'Ursina Serial Port'
window.borderless = False
window.size = (400, 700)

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
open_serial_port_button = Button(text='Open Serial Port', scale=(0.2, 0.1), position=(0, -0.2))

# Create a button to close the serial port, at the right of the window
close_serial_port_button = Button(text='Close Serial Port', scale=(0.2, 0.1))

# Create a button to send data, at the right of the window
send_data_button = Button(text='Send Data', scale=(0.2, 0.1), position=(0, 0.2))

# List representing the buttons
buttons = [open_serial_port_button, close_serial_port_button, send_data_button]

# Create on_click function for the buttons
for button in buttons:
    
    def on_click(b=button):
        print(b.text)
    
    button.on_click = on_click

# Run the app
if __name__ == '__main__':
    app.run()