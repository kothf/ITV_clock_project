# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import machine
led = machine.Pin("LED", machine.Pin.OUT)
led.off()
led.on()
