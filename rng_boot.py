# sudo nano /etc/rc.local
# sudo lxterminal -e python3 /home/pi/Desktop/RngKitCLI/boot.py &

# Default imports
import time
from time import localtime, strftime
import os
import serial
from serial.tools import list_ports


# External imports

from bitstring import BitArray
from colorama import init

init(autoreset=True)

from colorama import Fore

# Internal imports

def find_rng():
    rng_com_port = None

    # Call list_ports to get com port info
    ports_avaiable = list_ports.comports()

    print("Searching for RNG device...\n")
    for temp in ports_avaiable:
    #   print(temp[1] + ' : ' + temp[2])
        if '04D8:F5FE' in temp[2]:
            print(f'{Fore.CYAN}Found TrueRNG on {temp[0]} \n')
            if rng_com_port == None:        # always chooses the 1st TrueRNG found
                rng_com_port=temp[0]
        if '16D0:0AA0' in temp[2]:
            print(f'{Fore.CYAN}Found TrueRNGPro on {temp[0]} \n')
            if rng_com_port == None:        # always chooses the 1st TrueRNG found
                rng_com_port=temp[0]
        if '04D8:EBB5' in temp[2]:
            print(f'{Fore.CYAN}Found TrueRNGoroV2 on {temp[0]} \n')
            if rng_com_port == None:        # always chooses the 1st TrueRNG found
                rng_com_port=temp[0]
    if rng_com_port == None:
        print(f'{Fore.RED}No TrueRNG found. Attach it and try again.\n')
    return rng_com_port


def start_serial(rng_com_port):
    print('==================================================\n')

    # Print which port we're using
    print(f'{Fore.CYAN}Using com port:  ' + str(rng_com_port), "\n")

    # Try to setup and open the comport
    ser = serial.Serial(port=rng_com_port, timeout=10)  # timeout set at 10 seconds in case the read fails
            
    # Open the serial port if it isn't open
    if(ser.isOpen() == False):
        ser.open()

    # Set Data Terminal Ready to start flow
    ser.setDTR(True)

    # This clears the receive buffer so we aren't using buffered data
    ser.flushInput()
    return ser


def trng3_cap(sample_value, interval_value, ser):
    blocksize = int(sample_value / 8)
    file_name = time.strftime(
        f"%Y%m%d-%H%M%S_trng_s{sample_value}_i{interval_value}")
    file_name = f"/home/pi/Desktop/RngKitCLI/1-SavedFiles/{file_name}"
    num_loop = 1
    total_bytes = 0
    print(f"{Fore.GREEN}Starting capture:\n")
    print(f"{Fore.YELLOW}Saving to file {file_name}\n")
    try:
        while True:
            total_bytes += blocksize
            print(f"{Fore.CYAN}Collecting data - Loop: {num_loop} - Total bytes collected: {total_bytes}")
            total_bytes += blocksize
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
        print(f"{Fore.YELLOW} Capture stopped by user, closing serial port and exiting")
        print(f"{Fore.GREEN}Total bytes collected: {total_bytes}, saved to {file_name}")
        

if __name__ == "__main__":
    print("\n", f"{Fore.MAGENTA}#" * 29, "\n")
    print(
        f"{Fore.CYAN}Hello, Welcome to the RngKitCLI Auto Start - {Fore.YELLOW}ver 0.1 - {Fore.GREEN}by Thiago Jung"
    )
    print("\n", f"{Fore.MAGENTA}#" * 29, "\n")
    time.sleep(30)
    rng_com_port = find_rng()
    if rng_com_port != None:
        sample_value, interval_value = 2048, 1
        ser = start_serial(rng_com_port)
        trng3_cap(sample_value, interval_value, ser)