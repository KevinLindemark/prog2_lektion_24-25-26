import smbus
import time

bus = smbus.SMBus(1) # RPi revision 2 (0 for revision 1)
i2c_address = 0x49  # default address

dry = 685
wet = 291

def get_soilmoisture_percentage():
    # Reads word (2 bytes) as int - 0 is comm byte
    rd = bus.read_word_data(i2c_address, 0)
    # Exchanges high and low bytes
    data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
    # Ignores two least significiant bits
    adc_val = data >> 2
    moist_perc = (dry - adc_val) * 100.0 / (dry - wet)
    moist_perc = format(moist_perc, '.2f')
    print("Moisture percentage: ", moist_perc)
    return moist_perc