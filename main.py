from machine import Pin
import time

# Define pins
data_pin = Pin(14, Pin.OUT)   # DS
clock_pin = Pin(13, Pin.OUT)  # SH_CP
latch_pin = Pin(12, Pin.OUT)  # ST_CP

# Segment byte patterns for 0–9 (Common Anode — LOW to turn ON segment)
# So bits are inverted from the usual common cathode version
digit_to_segment = [
    0b11000000,  # 0
    0b11111001,  # 1
    0b10100100,  # 2
    0b10110000,  # 3
    0b10011001,  # 4
    0b10010010,  # 5
    0b10000010,  # 6
    0b11111000,  # 7
    0b10000000,  # 8
    0b10010000   # 9
]

# Digit selector (active LOW for common anode display)
digit_select = [
    0b1110,  # Enable digit 0
    0b1101,  # Enable digit 1
    0b1011,  # Enable digit 2
    0b0111   # Enable digit 3
]

def shift_out(byte_list):
    """Shift out multiple bytes to the chain of shift registers."""
    latch_pin.value(0)
    for byte in byte_list:
        for i in range(8):
            bit = (byte >> (7 - i)) & 1
            data_pin.value(bit)
            clock_pin.value(1)
            clock_pin.value(0)
    latch_pin.value(1)

def display_number(value):
    """
    Break a number into 4 digits and display them one at a time rapidly
    using multiplexing. Assumes 4 shift registers: 1 for segments, 3 for digit control.
    """
    digits = [int(d) for d in f"{value:04d}"]
    
    for i in range(4):
        segment_data = digit_to_segment[digits[i]]
        
        # Prepare digit selector: Only digit i is LOW (active)
        # digit_select is 4-bit; expand to 8 bits and fill 3 shift registers
        digit_mask = digit_select[i]
        digit_bytes = [
            0xFF,  # Default high for all digits
            0xFF,
            0xFF
        ]
        digit_bytes[i // 2] = 0xFF ^ (1 << ((i % 2) * 4))  # Activate one digit (custom wiring may vary)
        
        shift_out([segment_data] + digit_bytes)
        time.sleep(0.003)  # ~3ms per digit

def main():
    count = 0
    while True:
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 500:
            display_number(count)
        count = (count + 1) % 10000  # Loop from 0000 to 9999

if __name__ == "__main__":
    main()
