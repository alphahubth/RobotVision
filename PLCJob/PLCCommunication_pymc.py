import pymcprotocol

import time
import numpy as np
import logging



def initiate_PLC(plc_address, plc_port):

    pymc3e = pymcprotocol.Type3E(plctype="iQ-R")
    pymc3e.setaccessopt(commtype="binary")
    pymc3e.connect(ip=plc_address, port=plc_port)
    print(f"connected state: {pymc3e._is_connected}")
    return pymc3e


def read_plc_M(pymc, headdevice):    
    return pymc.batchread_bitunits(headdevice=headdevice, readsize=1)[0]

def write2plc_M(pymc, bit_address:list, values:list=[1], hold=False):

    if not (len(bit_address) == len(values)):
        raise Exception("Length of bit address need to be the same as values")

    pymc.randomwrite_bitunits(bit_devices=list(bit_address), values=list(values))
    
    if hold:
        return
    
    time.sleep(1.5)
    pymc.randomwrite_bitunits(bit_devices=list(bit_address), values=list([0 for _ in range(len(values))]))


def write2plc_D(pymc, word_address: list, values: list = [1], hold=False):
    if not (len(word_address) == len(values)):
        raise Exception("Length of word address needs to be the same as values")

    pymc.randomwrite(word_devices=word_address, word_values=values, dword_devices=word_address, dword_values=values)
    
    if hold:
        return
    
    time.sleep(1.5)
    pymc.randomwrite(word_devices=word_address, word_values=[0 for _ in values], dword_devices=word_address, dword_values=[0 for _ in values])

