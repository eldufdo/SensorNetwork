#!/usr/bin/python2

from nrf24l01 import *

rf = NRF24L01();

rf.writeReg(RX_PW_P0,[1]);
rf.writeReg(RF_CH,[128]);
rf.writeReg(RF_SETUP,[38]);
rf.writeReg(CONFIG,[(1<<PWR_UP) | (1<<PRIM_RX) | (1<<EN_CRC)]);
time.sleep(0.002);
rf.ceHigh();

while (1) :
    while (ord(rf.readStatus()) & (1<<6)) == 0:
        i = 0

    rf.ceLow();
    rf.writeReg(STATUS,[1<<RX_DR]);
    print "Got value: " + str(ord(rf.readPayload()[0]));
    print "Status is " + str(bin(ord(rf.readStatus())));
    rf.ceHigh();
