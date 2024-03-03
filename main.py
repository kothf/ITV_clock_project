import machine
import utime

# Define pin numbers for shift registers
data_pin = machine.Pin(0, machine.Pin.OUT)  # Connect to SER
clock_pin = machine.Pin(1, machine.Pin.OUT)  # Connect to SRCLK
latch_pin = machine.Pin(2, machine.Pin.OUT)  # Connect to RCLK

# Define pins for ZS-042 RTC module (I2C)
i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8))
rtc_address = 0x68

# Define the segments for the 7-segment display
segments = [
    0b00111111,  # 0
    0b00000110,  # 1
    0b01011011,  # 2
    0b01001111,  # 3
    0b01100110,  # 4
    0b01101101,  # 5
    0b01111101,  # 6
    0b00000111,  # 7
    0b01111111,  # 8
    0b01101111,  # 9
]


def shift_out(data_pin, clock_pin, latch_pin, data):
    for _ in range(8):
        data_pin.value((data >> 7) & 1)
        data <<= 1
        clock_pin.on()
        clock_pin.off()
    latch_pin.on()
    latch_pin.off()




def display_digit(digit):
    shift_out(data_pin, clock_pin, latch_pin, segments[digit])


while True:
    # Read time from ZS-042 RTC module
    try:
        i2c.writeto(rtc_address, bytes([0x00]))
        time_data = i2c.readfrom(rtc_address, 7)
        hour, minute, second = (
            int(time_data[2]),
            int(time_data[1]),
            int(time_data[0]),
        )
    except OSError:
        continue

    # Display time on 7-segment displays
    display_digit(hour // 10)
    utime.sleep(0.001)
    display_digit(hour % 10)
    utime.sleep(0.001)
    display_digit(minute // 10)
    utime.sleep(0.001)
    display_digit(minute % 10)
    utime.sleep(0.001)
