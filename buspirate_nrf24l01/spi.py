#!/usr/bin/python2

from buspirate import *
import time
import sys
import logging


class Spi:


    def __init__(self,port="/dev/ttyUSB0",baud=115200):
        self.bp = BusPirate(port,baud);

    def setup(self):
        if not self.bp.enterBitBangMode():
            logging.info("Error BB");
        logging.info("Entered BB Mode");
        if not self.bp.enterSpiMode():
            logging.info("Error Spi");
        logging.info("Entered SPI Mode");
        self.bp.cfgPeripherals(1,0,0,0);
        self.bp.setSpeed(SpiSpeed._30kHz);
        self.bp.spiConfig(SpiConfig.OUT_3_3 | SpiConfig.CLOCK_EDGE_ACTIVE_IDLE);

    def send(self,data):
        return self.bp.send(data);

    def csLow(self):
        self.bp.csLow();

    def csHigh(self):
        self.bp.csHigh();

    def cfgPeripherals(self,power,pull_up,AUX,CS):
        self.bp.cfgPeripherals(power,pull_up,AUX,CS);
    
