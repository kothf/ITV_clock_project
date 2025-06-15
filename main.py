from machine import Pin
import time

# GPIO setup
data_pin = Pin(14, Pin.OUT)   # DS
clock_pin = Pin(13, Pin.OUT)  # SH_CP
latch_pin = Pin(12, Pin.OUT)  # ST_CP

# Segment patterns for digits 0–9 (common cathode: HIGH = ON)
digit_to_segment = [
    0b00111111,  # 0
    0b00000110,  # 1
    0b01011011,  # 2
    0b01001111,  # 3
    0b01100110,  # 4
    0b01101101,  # 5
    0b01111101,  # 6
    0b00000111,  # 7
    0b01111111,  # 8
    0b01101111   # 9
]

def shift_out(bytes_out):
    """Shift out list of 4 bytes (one per 74HC595)."""
    latch_pin.value(0)
    for byte in bytes_out:
        for i in range(8):
            bit = (byte >> (7 - i)) & 1
            data_pin.value(bit)
            clock_pin.value(1)
            clock_pin.value(0)
    latch_pin.value(1)

def display_number(digits):
    """
    digits: list of 4 integers, each 0–9
    Displays them on 4 digits.
    """
    segments = [
        digit_to_segment[digits[0]],
        digit_to_segment[digits[1]],
        digit_to_segment[digits[2]],
        digit_to_segment[digits[3]]
    ]
    shift_out(segments)

def get_user_input():
    """Ask the user for 4 digits and return them as a list."""
    while True:
        user_input = input("Enter 4 digits (e.g., 1234): ")
        if len(user_input) == 4 and user_input.isdigit():
            digits = [int(c) for c in user_input]
            return digits
        else:
            print("Invalid input! Please enter exactly 4 digits.")

def main():
    while True:
        digits = get_user_input()
        while True:
            display_number(digits)
            time.sleep(0.05)  # Short delay to avoid CPU overuse

if __name__ == "__main__":
    main()
