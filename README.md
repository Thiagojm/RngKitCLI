# 🎲 RngKit CLI - Command Line Interface

**A powerful command-line tool for True Random Number Generator data collection and statistical analysis**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CLI](https://img.shields.io/badge/Interface-CLI-black.svg)](https://en.wikipedia.org/wiki/Command-line_interface)

*by [Thiago Jung](https://github.com/Thiagojm) • [thiagojm1984@hotmail.com](mailto:thiagojm1984@hotmail.com)*

[GitHub Repository](https://github.com/Thiagojm/RngKitCLI) • [Streamlit Version](https://github.com/Thiagojm/RngKitST)

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [🔧 Supported Hardware](#-supported-hardware)
- [⚡ Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [🚀 Usage Guide](#-usage-guide)
- [📁 File Naming Convention](#-file-naming-convention)
- [🔧 Configuration](#-configuration)
- [⚠️ Troubleshooting](#️-troubleshooting)
- [📄 License](#-license)

---

## 🎯 Overview

**RngKit CLI** is a command-line interface version of the popular RngKit application, designed for collecting and analyzing data from True Random Number Generators (TRNGs) and Pseudo Random Number Generators (PRNGs). This tool provides the same powerful functionality as the Streamlit version but in a lightweight, scriptable CLI format.

### ✨ Key Features

- 🔌 **Multi-Device Support**: TrueRNG, BitBabbler, and Pseudo RNG
- 📊 **Statistical Analysis**: Automated Excel report generation with Z-score charts
- 🔄 **Data Concatenation**: Combine multiple CSV files for extended analysis
- 🖥️ **Cross-Platform**: Windows, Linux, and macOS support
- ⚡ **Lightweight**: No GUI dependencies, perfect for automation
- 🐍 **Scriptable**: Easy integration into Python scripts and workflows

### 🔄 What's New in CLI Version

- ✅ **Command-Line Interface**: Full CLI with comprehensive argument parsing
- ✅ **Automation Ready**: Perfect for batch processing and scripting
- ✅ **Minimal Dependencies**: Lightweight installation without GUI components
- ✅ **Progress Indicators**: Real-time progress bars and status updates
- ✅ **Error Handling**: Robust error handling with detailed error messages

---

## 🔧 Supported Hardware

| Device | Model | Status | Notes |
|--------|-------|--------|-------|
| **TrueRNG** | TrueRNG3, TrueRNGPro | ✅ Supported | [ubld.it](https://ubld.it/) |
| **BitBabbler** | Black, White | ✅ Supported | [bitbabbler.org](http://www.bitbabbler.org/what.html) |
| **Pseudo RNG** | Python `secrets` | ✅ Supported | Not truly random, for testing only |

---

## ⚡ Quick Start

1. **Install dependencies and setup hardware**:
   ```bash
   # Linux (automated)
   sudo ./tools/installers/setup_rng_devices_linux_python.sh
   pip3 install -r requirements.txt
   
   # Windows (manual)
   # Install drivers from tools/installers/ folder
   pip install -r requirements.txt
   
   # macOS
   brew install libusb
   pip install -r requirements.txt
   ```

2. **Check device status**:
   ```bash
   python main.py status
   ```

3. **Collect data**:
   ```bash
   python main.py collect --device bitbabbler --bits 2048 --interval 1 --duration 60
   ```

4. **Analyze data**:
   ```bash
   # Auto-detect parameters from filename (recommended)
   python main.py analyze --file data/raw/20250917T140811_trng_s2048_i1.csv
   
   # Or specify manually if needed
   python main.py analyze --file data/raw/sample.csv --bits 2048 --interval 1
   ```

---

## 📦 Installation

### 🪟 Windows Installation

#### Hardware Setup

1. **TrueRNG/TrueRNGPro**:
   - Navigate to `tools/installers/TrueRng/` folder
   - Right-click `TrueRNG.inf` or `TrueRNGpro.inf`
   - Select "Install" and follow the prompts
   - Device should appear as a COM port

2. **BitBabbler**:
   - Run `vcredist_x64.exe` from `tools/installers/BitBabbler/`
   - Insert BitBabbler device into USB port
   - Run `zadig-2.8.exe` and install driver for your device
   - Ensure device is recognized by the system

#### Python Setup

```bash
# Clone the repository
git clone https://github.com/Thiagojm/RngKitCLI.git
cd RngKitCLI

# Install dependencies
pip install -r requirements.txt

# Make executable (optional)
chmod +x main.py
```

### 🐧 Linux Installation

#### Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/Thiagojm/RngKitCLI.git
cd RngKitCLI

# Run the automated setup script
sudo ./tools/installers/setup_rng_devices_linux_python.sh

# Install Python dependencies
pip3 install -r requirements.txt

# Log out and back in for group changes to take effect
```

This script will:
- ✅ Set up udev rules for device access
- ✅ Create required user groups
- ✅ Configure device permissions
- ✅ Install system dependencies

#### Manual Setup

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install system dependencies
sudo apt-get install libusb-1.0-0-dev

# Set up udev rules for device access
sudo cp tools/installers/TrueRng/udev_rules/99-TrueRNG.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules

# Add user to bit-babbler group
sudo usermod -aG bit-babbler $USER

# Log out and back in for group changes to take effect
```

### 🍎 macOS Installation

```bash
# Clone the repository
git clone https://github.com/Thiagojm/RngKitCLI.git
cd RngKitCLI

# Install system dependencies
brew install libusb

# Install Python dependencies
pip install -r requirements.txt
```

---

## 📁 Installer Files

The `tools/installers/` directory contains platform-specific installation files:

### 🪟 Windows Installers
- **BitBabbler**:
  - `vcredist_x64.exe` - Visual C++ Redistributable
  - `zadig-2.8.exe` - Driver installation tool
- **TrueRNG**:
  - `TrueRNG3/TrueRNG.inf` - TrueRNG3 driver
  - `TrueRNGpro/TrueRNGpro.inf` - TrueRNGpro driver

### 🐧 Linux Installers
- `setup_rng_devices_linux_python.sh` - Automated setup script
- `TrueRng/udev_rules/99-TrueRNG.rules` - udev rules for TrueRNG

### 📋 Installation Process
1. **Windows**: Run the appropriate `.exe` files and `.inf` drivers
2. **Linux**: Execute the setup script with `sudo` privileges
3. **macOS**: Use Homebrew for system dependencies

---

## 🚀 Usage Guide

### 📊 Data Collection

#### Basic Collection

```bash
# Collect from BitBabbler for 60 seconds
python main.py collect --device bitbabbler --bits 2048 --interval 1 --duration 60

# Collect from TrueRNG with custom output
python main.py collect --device truerng --bits 1024 --interval 1 --output my_data

# Collect from Pseudo RNG (for testing)
python main.py collect --device pseudo --bits 4096 --interval 2 --duration 120
```

#### Advanced Collection

```bash
# BitBabbler with XOR folding
python main.py collect --device bitbabbler --bits 2048 --interval 1 --folds 2 --duration 300

# High-frequency collection
python main.py collect --device truerng --bits 512 --interval 1 --duration 30

# Verbose output for debugging
python main.py collect --device bitbabbler --bits 2048 --interval 1 --verbose
```

### 📈 Data Analysis

#### Analyze CSV Files

```bash
# Auto-detect parameters from filename (recommended)
python main.py analyze --file data/raw/20250917T140811_trng_s2048_i1.csv

# Auto-detect with custom output
python main.py analyze --file data/raw/20250917T140811_trng_s2048_i1.csv --output analysis_report

# Auto-detect with verbose output
python main.py analyze --file data/raw/20250917T140811_trng_s2048_i1.csv --verbose

# Manual override (when needed)
python main.py analyze --file data/raw/sample.csv --bits 2048 --interval 1

# Partial override (auto-detect interval, override bits)
python main.py analyze --file data/raw/20250917T140811_trng_s2048_i1.csv --bits 1024
```

#### Analyze Binary Files

```bash
# Auto-detect parameters from filename (recommended)
python main.py analyze --file data/raw/20250917T140811_trng_s2048_i1.bin

# Auto-detect with custom output
python main.py analyze --file data/raw/20250917T140811_trng_s2048_i1.bin --output binary_analysis

# Manual override (when needed)
python main.py analyze --file data/raw/sample.bin --bits 2048 --interval 1
```

#### Auto-Detection Feature

The analyze command can automatically detect the sample size (bits) and interval from RngKit-generated filenames:

- **Filename format**: `YYYYMMDDTHHMMSS_{device}_s{bits}_i{interval}[_f{folds}]`
- **Examples**:
  - `20250917T140811_trng_s2048_i1.csv` → auto-detects bits=2048, interval=1
  - `20250917T140834_pseudo_s1024_i2.bin` → auto-detects bits=1024, interval=2
  - `20250917T141124_concat_s2048_i1.csv` → auto-detects bits=2048, interval=1

**Benefits:**
- ✅ **Convenience**: No need to remember parameters
- ⚡ **Speed**: Faster command execution
- 🔒 **Reliability**: Reduces human error
- 📁 **Compatibility**: Works with all RngKit-generated files

### 🔗 Data Concatenation

```bash
# Auto-detect parameters and generate output filename (recommended)
python main.py concat --files file1_s2048_i1.csv file2_s2048_i1.csv file3_s2048_i1.csv

# Auto-detect with custom output filename
python main.py concat --files file1_s2048_i1.csv file2_s2048_i1.csv --output combined

# Auto-detect with verbose output
python main.py concat --files file1_s2048_i1.csv file2_s2048_i1.csv --verbose

# Manual override (when needed)
python main.py concat --files file1.csv file2.csv --output combined --bits 2048 --interval 1

# Partial override (auto-detect interval, override bits)
python main.py concat --files file1_s2048_i1.csv file2_s2048_i1.csv --bits 1024
```

#### Concat Auto-Detection Feature

The concat command can automatically detect parameters and generate output filenames:

- **Parameter detection**: Uses the first filename to detect bits and interval
- **Auto-generated output**: Creates timestamped filenames when `--output` is not specified
- **Filename format**: `YYYYMMDDTHHMMSS_concat_s{bits}_i{interval}.csv`

**Benefits:**
- ✅ **Convenience**: No need to specify parameters or output filename
- ⚡ **Speed**: Fastest possible command execution
- 🔒 **Reliability**: Reduces human error
- 📁 **Organization**: Timestamped files are easy to identify

### 🔍 Device Status

```bash
# Check all devices
python main.py status

# Check with verbose output
python main.py status --verbose
```

---

## 📁 File Naming Convention

Files follow a structured naming pattern that encodes important metadata:

```
YYYYMMDDTHHMMSS_{device}_s{bits}_i{interval}[_f{folds}]
```

### 📝 Format Breakdown

| Component | Description | Example |
|-----------|-------------|---------|
| `YYYYMMDDTHHMMSS` | Timestamp | `20201011T142208` |
| `{device}` | Device type | `trng`, `bitb`, `pseudo` |
| `s{bits}` | Sample size in bits | `s2048` |
| `i{interval}` | Interval in seconds | `i1` |
| `_f{folds}` | BitBabbler fold level | `f0` (RAW), `f1-f4` (XOR) |

### 💡 Example

```
20201011T142208_bitb_s2048_i1_f0
```

- **Date**: October 11, 2020
- **Time**: 14:22:08
- **Device**: BitBabbler
- **Sample Size**: 2048 bits
- **Interval**: 1 second
- **Mode**: RAW (f0)

---

## 🔧 Configuration

### Environment Variables

- `RNGKIT_DATA_DIR`: Override default data directory (default: `./data/raw`)

### Command Line Options

#### Global Options

- `--verbose, -v`: Enable verbose output
- `--help, -h`: Show help message

#### Collect Command

- `--device, -d`: RNG device to use (bitbabbler, truerng, pseudo)
- `--bits, -b`: Number of bits per sample (default: 2048)
- `--interval, -i`: Sample interval in seconds (whole numbers only) (default: 1, whole numbers only)
- `--duration, -t`: Collection duration in seconds (default: unlimited)
- `--folds, -f`: BitBabbler XOR folds (0=RAW, 1-4=folds, default: 0)
- `--output, -o`: Output filename (without extension)

#### Analyze Command

- `--file, -f`: Input file to analyze (.csv or .bin)
- `--bits, -b`: Number of bits per sample (auto-detected from filename if not specified)
- `--interval, -i`: Sample interval in seconds (auto-detected from filename if not specified)
- `--output, -o`: Output Excel filename (default: auto-generated)

#### Concat Command

- `--files, -f`: CSV files to concatenate
- `--output, -o`: Output CSV filename (default: auto-generated with timestamp)
- `--bits, -b`: Number of bits per sample (auto-detected from first filename if not specified)
- `--interval, -i`: Sample interval in seconds (auto-detected from first filename if not specified)

---

## ⚠️ Troubleshooting

### 🐧 Linux Compatibility

| Issue | Status | Workaround |
|-------|--------|------------|
| **TrueRNG + BitBabbler combination** | ❌ Not supported | Use individual devices instead |
| **Permission denied** | ⚠️ Common | Add user to appropriate groups |

### 🔧 Common Issues

#### BitBabbler Issues

- **Device not detected**: Ensure proper USB connection and driver installation
  - Windows: Reinstall using `tools/installers/BitBabbler/zadig-2.8.exe`
  - Linux: Run `sudo ./tools/installers/setup_rng_devices_linux_python.sh`
- **Permission denied**: Add user to `bit-babbler` group and restart session
- **Driver issues**: 
  - Windows: Install Visual C++ Redistributable from `tools/installers/BitBabbler/vcredist_x64.exe`
  - Linux: Check udev rules and group membership

#### TrueRNG Issues

- **Port not found**: Check USB connection and driver installation
  - Windows: Install driver from `tools/installers/TrueRng/TrueRNG3/TrueRNG.inf`
  - Linux: Run `sudo ./tools/installers/setup_rng_devices_linux_python.sh`
- **Permission denied**: Ensure user has access to serial ports
- **Timeout errors**: Check device connection and try different USB port

#### General Issues

- **Import errors**: Ensure all dependencies are installed
- **File not found**: Check file paths and permissions
- **Analysis errors**: Verify file format and parameters

### 🐛 Debug Mode

Use the `--verbose` flag to get detailed information about what the tool is doing:

```bash
python main.py collect --device bitbabbler --bits 2048 --interval 1 --verbose
```

---

## 📄 License

**MIT License**

Copyright (c) 2025 Thiago Jung Mendaçolli

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

**Made with ❤️ by [Thiago Jung](https://github.com/Thiagojm)**

[⭐ Star this repo](https://github.com/Thiagojm/RngKitCLI) • [🐛 Report Issues](https://github.com/Thiagojm/RngKitCLI/issues) • [💬 Discussions](https://github.com/Thiagojm/RngKitCLI/discussions)
