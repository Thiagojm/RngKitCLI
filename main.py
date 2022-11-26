# Default imports
import time
from time import localtime, strftime


# External imports

from bitstring import BitArray
import serial
from serial.tools import list_ports

# Internal imports

def trng3_cap():
    # global thread_cap
    sample_value = 256
    interval_value = 1
    blocksize = int(sample_value / 8)
    ports_avaiable = list(list_ports.comports())
    rng_com_port = None
    for temp in ports_avaiable:
        if temp[1].startswith("TrueRNG"):
            if rng_com_port == None:  # always chooses the 1st TrueRNG found
                rng_com_port = str(temp[0])
    file_name = time.strftime(
        f"%Y%m%d-%H%M%S_trng_s{sample_value}_i{interval_value}")
    file_name = f"1-SavedFiles/{file_name}"
    print(ports_avaiable)
    print(rng_com_port)
    while True:
        start_cap = time.time()
        with open(file_name + '.bin', "ab") as bin_file:  # save binary file
            try:
                # timeout set at 10 seconds in case the read fails
                ser = serial.Serial(port=rng_com_port, timeout=10)
                if (ser.isOpen() == False):
                    ser.open()
                ser.setDTR(True)
                ser.flushInput()
            except Exception as e:
                print("Error opening serial port", e)
                break
            try:
                x = ser.read(blocksize)  # read bytes from serial port
            except Exception:
                print("Error reading from serial port")
                break
            bin_file.write(x)
            ser.close()
        bin_hex = BitArray(x)  # bin to hex
        bin_ascii = bin_hex.bin  # hex to ASCII
        # count numbers of ones in the string
        num_ones_array = bin_ascii.count('1')
        # open file and append time and number of ones
        with open(file_name + '.csv', "a+") as write_file:
            write_file.write(
                f'{strftime("%H:%M:%S", localtime())} {num_ones_array}\n')
        end_cap = time.time()
        # print(interval_value - (end_cap - start_cap))
        try:
            time.sleep(interval_value - (end_cap - start_cap))
        except Exception:
            pass
        

if __name__ == "__main__":
    print("Starting capture")
    trng3_cap()