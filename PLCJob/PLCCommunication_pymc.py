import pymcprotocol
import time
import numpy as np

def initiate_PLC(plc_address, plc_port):

    pymc3e = pymcprotocol.Type3E()
    pymc3e.setaccessopt(commtype="ascii")
    pymc3e.connect(ip=plc_address, port=plc_port)
    cpu_type, cpu_code = pymc3e.read_cputype()
    print(f"Initiate PLC connection. CPU TYPE: {cpu_type}, CPU CODE: {cpu_code}")
    print(f"connected state: {pymc3e._is_connected}")
    return pymc3e


def read_plc(pymc, headdevice):    
    return pymc.batchread_bitunits(headdevice=headdevice, readsize=1)[0]


def write2plc_M(pymc, bit_address:list, values:list=[1], hold=False):

    if not (len(bit_address) == len(values)):
        raise Exception("Length of bit address need to be the same as values")

    pymc.randomwrite_bitunits(bit_devices=list(bit_address), values=list(values))
    
    if hold:
        return
    
    time.sleep(1.5)
    pymc.randomwrite_bitunits(bit_devices=list(bit_address), values=list([0 for _ in range(len(values))]))


def write2plc_D(pymc, bit_address:list, values:list=[1], hold=False):

    if not (len(bit_address) == len(values)):
        raise Exception("Length of bit address need to be the same as values")

    pymc.randomwrite(word_devices=list(bit_address), word_values=list(values), dword_devices=list(bit_address), dword_values=list(values))
    
    if hold:
        return
    
    time.sleep(1.5)
    pymc.randomwrite(word_devices=list(bit_address), word_values=list([0 for _ in range(len(values))]), dword_devices=list(bit_address), dword_values=list(values))
