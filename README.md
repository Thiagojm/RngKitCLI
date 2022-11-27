# RngKitCLI 0.1
by Thiago Jung  
https://github.com/Thiagojm/RngKitCLI   
thiagojm1984@hotmail.com   
Written in Python 3.11
-----------------------

# ABSTRACT

This application a types of TRNG - True Random Number Generator (TrueRNG) for data collection and statistical analysis for several purposes, including mind-matter interaction research.  
It uses random number generation to collect and count the number of times the '1' bit appears in a series of user-defined size and interval.
Afterwards, the data can be analyzed and compared with the number expected by chance (50%) and create a chart with a cumulative Z-Score.


# Supported Hardware:

1- TrueRNG and TrueRNGPro (https://ubld.it/);  

# Installation

Windows INSTRUCTIONS
--------------------

1. Install Python 64-bit for Windows from:
https://www.python.org/

2. Put all files in the same directory

3. Open a command prompt (run the cmd command in Windows)

4. Change to the directory you created above and run: 

`install_python_libs.bat`

5. Choose from the Windows_Drivers folder the right driver for your hardware, right-click the TrueRNG.inf or TrueRNGpro.inf file and select Install. Follow the instructions for installation. 

6. Install the required Python libraries:

`python3 -m pip install -r requirements.txt`

7. Plug in a single TrueRNG V1, V2, V3, Pro, or ProV2

8. Run the application:

`python3 main.py`

Linux Instructions (Ubuntu / Debian-based)
------------------------------------------

1. Install Python3

`sudo apt install python3`

2. Install the required Python libraries:

`python3 -m pip install -r requirements.txt`

3. Plug in a single TrueRNG V1, V2, V3, Pro, or ProV2

4. Run the application:

`python3 main.py`

5. If needed, install the linux drivers as described in the README.md in the udev_rules folder.
