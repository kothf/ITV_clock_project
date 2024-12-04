from machine import Pin
import time

# Define GPIO pins for the 74HC595
data_pin = Pin(14, Pin.OUT)  # Data pin (DS)
clock_pin = Pin(13, Pin.OUT)  # Shift clock pin (SH_CP)
latch_pin = Pin(12, Pin.OUT)  # Latch pin (ST_CP)


def shift_out(data):
    """Shift out 8 bits of data to the 74HC595."""
    for i in range(8):
        bit = (data >> (7 - i)) & 1  # Extract the MSB first
        data_pin.value(bit)  # Set data pin
        clock_pin.value(1)  # Pulse clock to shift bit
        clock_pin.value(0)


def turn_on_all_segments():
    """
    Turn on all segments of all four 7-segment indicators.
    """
    latch_pin.value(0)  # Lower latch to prepare for new data

    # Send data for all 4 displays (4 bytes of all segments on)
    for _ in range(4):  # 4 indicators
        shift_out(0b11111111)  # All segments ON (for common cathode)

    latch_pin.value(1)  # Latch to display data


def main():
    while True:
        turn_on_all_segments()  # Turn on all segments
        #time.sleep(0.5)  # Keep it on for 1 second (adjust as needed)


# Run the main program
if __name__ == "__main__":
    main()
