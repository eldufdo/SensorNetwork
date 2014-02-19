from spi import Spi
import time

# Registers
CONFIG = 0x00
EN_AA = 0x01
EN_RXADDR = 0x02
SETUP_AW = 0x03
SETUP_RETR = 0x04
RF_CH = 0x05
RF_SETUP = 0x06
STATUS = 0x07
OBSERVE_TX = 0x08
CD = 0x09
RX_ADDR_P0 = 0x0A
RX_ADDR_P1 = 0x0B
RX_ADDR_P2 = 0x0C
RX_ADDR_P3 = 0x0D
RX_ADDR_P4 = 0x0E
RX_ADDR_P5 = 0x0F
TX_ADDR = 0x10
RX_PW_P0 = 0x11
RX_PW_P1 = 0x12
RX_PW_P2 = 0x13
RX_PW_P3 = 0x14
RX_PW_P4 = 0x15
RX_PW_P5 = 0x16
FIFO_STATUS = 0x17

# Bit Mnemonics
MASK_RX_DR = 6
MASK_TX_DS = 5
MASK_MAX_RT = 4
EN_CRC = 3
CRCO = 2
PWR_UP = 1
PRIM_RX = 0
ENAA_P5 = 5
ENAA_P4 = 4
ENAA_P3 = 3
ENAA_P2 = 2
ENAA_P1 = 1
ENAA_P0 = 0
ERX_P5 = 5
ERX_P4 = 4
ERX_P3 = 3
ERX_P2 = 2
ERX_P1 = 1
ERX_P0 = 0
AW = 0
ARD = 4
ARC = 0
PLL_LOCK = 4
RF_DR = 3
RF_PWR = 1
LNA_HCURR = 0
RX_DR = 6
TX_DS = 5
MAX_RT = 4
RX_P_NO = 1
TX_FULL = 0
PLOS_CNT = 4
ARC_CNT = 0
TX_REUSE = 6
FIFO_FULL = 5
TX_EMPTY = 4
RX_FULL = 1
RX_EMPTY = 0

# Instruction Mnemonics
R_REGISTER = 0x00
W_REGISTER = 0x20
REGISTER_MASK = 0x1F
R_RX_PAYLOAD = 0x61
W_TX_PAYLOAD = 0xA0
FLUSH_TX = 0xE1
FLUSH_RX = 0xE2
REUSE_TX_PL = 0xE3
NOP = 0xFF


class NRF24L01:

    def __init__(self):
        self.spi = Spi("/dev/ttyUSB1",115200);
        self.spi.setup();

    def writeReg(self,reg,data):
        self.spi.csLow();
        self.spi.send([W_REGISTER | reg]);
        self.spi.send(data);
        self.spi.csHigh();

    def readStatus(self):
        self.spi.csLow();
        data = self.spi.send([NOP]);
        self.spi.csHigh();
        return data[0];

    def readReg(self,reg,length=1):
        self.spi.csLow();
        data = [];
        for x in range(0,length):
            data.append(255); 
        self.spi.send([R_REGISTER | reg]);
        values = (self.spi.send(data));
        self.spi.csHigh();
        return values;

    def writePayload(self,data):
        self.spi.csLow();
        self.spi.send([W_TX_PAYLOAD]);
        x = 0;
        values = self.spi.send(data);
        self.spi.csHigh();
        return values;

    def readPayload(self):
        self.spi.csLow();
        self.spi.send([R_RX_PAYLOAD]);
        value = self.spi.send([0]);
        self.spi.csHigh();
        return value;

    def ceHigh(self):
        self.spi.cfgPeripherals(1,0,1,1);

    def ceLow(self):
        self.spi.cfgPeripherals(1,0,0,1);

    def flushTX(self):
        self.spi.send([FLUSH_TX]);
