# Default imports
import time
from time import localtime, strftime
import os


# External imports

from bitstring import BitArray
import serial
from serial.tools import list_ports

# Internal imports


rng_com_port = None

# Call list_ports to get com port info
ports_avaiable = list_ports.comports()

# Loop on all available ports to find TrueRNG
print('Com Port List')
for temp in ports_avaiable:
 #   print(temp[1] + ' : ' + temp[2])
    if '04D8:F5FE' in temp[2]:
        print('Found TrueRNG on ' + temp[0])
        if rng_com_port == None:        # always chooses the 1st TrueRNG found
            rng_com_port=temp[0]
    if '16D0:0AA0' in temp[2]:
        print('Found TrueRNGpro on ' + temp[0])
        if rng_com_port == None:        # always chooses the 1st TrueRNG found
            rng_com_port=temp[0]
    if '04D8:EBB5' in temp[2]:
        print('Found TrueRNGproV2 on ' + temp[0])
        if rng_com_port == None:        # always chooses the 1st TrueRNG found
            rng_com_port=temp[0]

print('==================================================')

# Print which port we're using
print('Using com port:  ' + str(rng_com_port))

# Try to setup and open the comport
try:
    ser = serial.Serial(port=rng_com_port,timeout=10)  # timeout set at 10 seconds in case the read fails
except:
    print('Port Not Usable!')
    print('Do you have permissions set to read ' + rng_com_port + ' ?')
    
    
# Open the serial port if it isn't open
if(ser.isOpen() == False):
    ser.open()

# Set Data Terminal Ready to start flow
ser.setDTR(True)

# This clears the receive buffer so we aren't using buffered data
ser.flushInput()

# Set bytes to read
sample_value = 256

# Set interval size in seconds
interval_value = 1

def trng3_cap(sample_value, interval_value, ser):
    # global thread_cap
    blocksize = int(sample_value / 8)
    file_name = time.strftime(
        f"%Y%m%d-%H%M%S_trng_s{sample_value}_i{interval_value}")
    file_name = f"1-SavedFiles/{file_name}"
    num_loop = 1
    try:
        while True:
            print("Collecting data - Loop: ", num_loop)
            start_cap = time.time()
            with open(file_name + '.bin', "ab") as bin_file:  # save binary file
                try:
                    x = ser.read(blocksize)  # read bytes from serial port
                except Exception:
                    print("Error reading from serial port")
                    break
                bin_file.write(x)  # write bytes to binary file
            bin_hex = BitArray(x)  # bin to hex
            bin_ascii = bin_hex.bin  # hex to ASCII
            # count numbers of ones in the string
            num_ones_array = bin_ascii.count('1')
            # open file and append time and number of ones
            with open(file_name + '.csv', "a+") as write_file:
                write_file.write(
                    f'{strftime("%H:%M:%S", localtime())} {num_ones_array}\n')
            end_cap = time.time()
            num_loop += 1
            try:
                time.sleep(interval_value - (end_cap - start_cap))
            except Exception:
                pass
    except KeyboardInterrupt:
        ser.close()
        if os.name == 'posix':
            os.system('stty -F '+rng_com_port+' min 1')
        print("Keyboard Interrupt")

if __name__ == "__main__":
    print("Starting capture")
    trng3_cap(sample_value, interval_value, ser)