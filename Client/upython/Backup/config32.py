import time
from machine import Pin, SPI

class config:
    # Pin setting for ESP32 Hardware SPI
    MISO_PIN = 12
    MOSI_PIN = 13
    CLK_PIN  = 14
    CS_PIN = 15   # Write Pin
    DRDY_PIN = 16 # Read Pin
    RST_PIN = 5  # Write Pin

    def __init__(self):
        # SPI device, bus = 1
        self.hSPI  = None
        self.pCS   = None
        self.pRST  = None
        self.pDRDY = None

    def set_RST(self, setValue):
        self.pRST.value(setValue)

    def set_CS(self, setValue):
        self.pCS.value(setValue)

    def get_DRDY(self):
        return self.pDRDY.value()

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.hSPI.write(bytearray(data))


    def spi_readbytes(self, num_bytes):
        return self.hSPI.read(num_bytes) dsf


    def module_init(self):
        self.hSPI  = SPI(1, baudrate=1920000, polarity=0, phase=1, bits=8, sck=Pin(self.CLK_PIN), mosi=Pin(self.MOSI_PIN), miso=Pin(self.MISO_PIN))
        self.pCS   = Pin(self.CS_PIN, Pin.OUT)
        self.pRST  = Pin(self.RST_PIN, Pin.OUT)
        self.pDRDY = Pin(self.DRDY_PIN, Pin.IN, Pin.PULL_UP)
        return 0

    def module_exit(self):
        self.hSPI.deinit()
        self.pRST.value(0)
        self.pCS.value(0)

