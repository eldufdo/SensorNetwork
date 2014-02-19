import serial
import time
import logging 

class SpiSpeed:
    _30kHz = 0;
    _125kHz = 1;
    _250kHz = 2;
    _1MHz = 3;
    _2MHz = 4;
    _2_6_MHz = 5;
    _4MHz = 6;
    _8MHz = 7;

class SpiConfig:
    OUT_3_3=8
    HIZ = 0
    CLOCK_IDLE_LOW=0
    CLOCK_IDLE_HIGH=4
    CLOCK_EDGE_ACTIVE_IDLE=2
    CLOCK_EDGE_IDLE_ACTIVE=0
    SAMPLE_MIDDLE=0
    SAMPLE_END=1

class BusPirate:

    def __init__(self,port='/dev/ttyUSB0',baud=115200):
        self.ser = serial.Serial(port,baud);
        logging.basicConfig(level=logging.INFO)
        self.timeout = 0.02;

    
    def setSerialTimeout(self,timeout):
        self.timeout = timeout;

    def enterBitBangMode(self):
        rounds = 40;
        while rounds > 0:
            self.ser.write([0]);
            time.sleep(self.timeout);
            if self.ser.inWaiting() > 4:
                data = str(self.ser.read(5));
                if data == "BBIO1":
                    return 1;
            rounds = rounds - 1;
        return 0;

    def enterSpiMode(self):
        self.ser.write([1]);
        time.sleep(self.timeout);
        if self.ser.inWaiting() > 3:
            recv = self.ser.read(4);
            if recv == "SPI1":
                return 1;
        return 0;
    
    def setSpeed(self,speed):
        self.ser.write([96 | speed]);
        self.ser.read();

    def csLow(self):
        self.ser.write([2]);
        self.ser.read();

    def csHigh(self):
        self.ser.write([3]);
        self.ser.read();
    
    def send(self,data):
        self.ser.write([16 | (len(data) - 1)]);
        time.sleep(self.timeout);
        self.ser.read();
        self.ser.write(data);
        time.sleep(self.timeout);
        ret = [];
        length = len(data);
        while length > 0:
            ret.append(self.ser.read());
            length = length - 1;
        return ret;
    
    def spiConfig(self,value):
        self.ser.write([(128 | value)]);
        self.ser.read();


    def cfgPeripherals(self,power,pull_up,AUX,CS):
        value = 64 | (power<<3) | (pull_up<<2) | (AUX<<1) | (CS<<0);
        self.ser.write([value]);
        self.ser.read();



