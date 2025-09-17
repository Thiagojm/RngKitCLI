"""
Data collection module for RngKit CLI.

This module provides functionality for collecting data from various RNG devices
and saving it to files in the appropriate format.
"""

import os
import sys
import time
import signal
from datetime import datetime
from typing import Optional, Dict, Any
from bitstring import BitArray

try:
    from .devices import bitbabbler as dev_bitb
    from .devices import truerng as dev_trng
    from .devices import pseudo as dev_pseudo
    from .services import filenames as fn_service
    from .services import storage as storage_service
except ImportError:
    # Fallback if modules not found
    dev_bitb = None
    dev_trng = None
    dev_pseudo = None
    fn_service = None
    storage_service = None

from .utils import ensure_data_dir, validate_params, format_duration


class DataCollector:
    """Handles data collection from RNG devices."""
    
    def __init__(self, verbose: bool = False):
        """Initialize the data collector.
        
        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose
        self.data_dir = ensure_data_dir()
        self.collecting = False
        self.samples_collected = 0
        self.start_time = None
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals for graceful shutdown."""
        if self.collecting:
            print(f"\n\nReceived signal {signum}. Stopping collection...")
            self.collecting = False
    
    def collect(self, device: str, bits: int, interval: int, duration: Optional[int] = None,
                folds: int = 0, output_file: Optional[str] = None) -> None:
        """Collect data from the specified RNG device.
        
        Args:
            device: Device type ('bitbabbler', 'truerng', 'pseudo')
            bits: Number of bits per sample
            interval: Sample interval in seconds (must be >= 1)
            duration: Collection duration in seconds (None for unlimited)
            folds: BitBabbler XOR folds (0=RAW, 1-4=folds)
            output_file: Output filename (without extension)
            
        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If device is not available or collection fails
        """
        # Validate parameters
        if not validate_params(bits, interval):
            raise ValueError("Invalid parameters. Bits must be divisible by 8 and interval >= 1")
        
        # Check device availability
        device_module = self._get_device_module(device)
        if device_module is None:
            raise RuntimeError(f"Device module for {device} not available")
        
        if not device_module.detect():
            raise RuntimeError(f"{device} device not detected or not accessible")
        
        # Generate output filename
        if output_file is None:
            device_suffix = "bitb" if device == "bitbabbler" else "trng" if device == "truerng" else "pseudo"
            if fn_service:
                output_file = fn_service.format_capture_name(
                    device_suffix, bits, int(interval), folds if device == "bitbabbler" else None
                )
            else:
                timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
                output_file = f"{timestamp}_{device_suffix}_s{bits}_i{int(interval)}"
                if device == "bitbabbler":
                    output_file += f"_f{folds}"
        
        # Set up file paths
        bin_path = os.path.join(self.data_dir, f"{output_file}.bin")
        csv_path = os.path.join(self.data_dir, f"{output_file}.csv")
        
        if self.verbose:
            print(f"Device: {device}")
            print(f"Sample size: {bits} bits")
            print(f"Sample interval: {interval} seconds")
            print(f"Duration: {format_duration(duration) if duration else 'unlimited'}")
            print(f"Output files: {bin_path}, {csv_path}")
            if device == "bitbabbler":
                print(f"XOR folds: {folds}")
            print()
        
        # Start collection
        self.collecting = True
        self.samples_collected = 0
        self.start_time = time.time()
        
        try:
            self._collect_loop(device_module, device, bits, interval, duration, folds, bin_path, csv_path)
        except KeyboardInterrupt:
            print("\nCollection interrupted by user.")
        except Exception as e:
            print(f"\nCollection failed: {e}")
            raise
        finally:
            self.collecting = False
            if self.samples_collected > 0:
                elapsed = time.time() - self.start_time
                print(f"\nCollection completed!")
                print(f"Samples collected: {self.samples_collected}")
                print(f"Total time: {format_duration(elapsed)}")
                print(f"Average rate: {self.samples_collected / elapsed:.2f} samples/second")
                print(f"Files saved: {bin_path}, {csv_path}")
    
    def _collect_loop(self, device_module, device: str, bits: int, interval: int,
                     duration: Optional[int], folds: int, bin_path: str, csv_path: str) -> None:
        """Main collection loop.
        
        Args:
            device_module: Device module to use for collection
            device: Device type name
            bits: Number of bits per sample
            interval: Sample interval in seconds (must be >= 1)
            duration: Collection duration in seconds
            folds: BitBabbler XOR folds
            bin_path: Path to binary output file
            csv_path: Path to CSV output file
        """
        bytes_per_sample = bits // 8
        last_sample_time = 0
        
        with open(bin_path, 'wb') as bin_file, open(csv_path, 'w', newline='') as csv_file:
            import csv
            csv_writer = csv.writer(csv_file)
            # No header row to match expected format
            
            while self.collecting:
                current_time = time.time()
                
                # Check if enough time has passed for next sample
                if current_time - last_sample_time >= interval:
                    try:
                        # Collect sample
                        sample_data = self._collect_sample(device_module, device, bytes_per_sample, folds)
                        if sample_data:
                            # Write to binary file
                            bin_file.write(sample_data)
                            bin_file.flush()
                            
                            # Count ones and write to CSV
                            bit_array = BitArray(sample_data)
                            ones_count = bit_array.count(1)
                            timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
                            csv_writer.writerow([timestamp, ones_count])
                            csv_file.flush()
                            
                            self.samples_collected += 1
                            
                            # Print detailed sample information
                            readable_time = datetime.now().strftime("%H:%M:%S")
                            print(f"Row {self.samples_collected:4d} | Time: {readable_time} | Ones: {ones_count:4d}")
                        
                        last_sample_time = current_time
                        
                        # Check duration limit
                        if duration and (current_time - self.start_time) >= duration:
                            break
                            
                    except Exception as e:
                        if self.verbose:
                            print(f"Sample collection error: {e}")
                        continue
    
    def _collect_sample(self, device_module, device: str, bytes_per_sample: int, folds: int) -> bytes:
        """Collect a single sample from the device.
        
        Args:
            device_module: Device module to use
            device: Device type name
            bytes_per_sample: Number of bytes to collect
            folds: BitBabbler XOR folds
            
        Returns:
            Sample data as bytes
        """
        if device == "bitbabbler":
            return device_module.read_bytes(bytes_per_sample, folds)
        elif device == "truerng":
            return device_module.read_bytes(bytes_per_sample)
        elif device == "pseudo":
            return device_module.read_bytes(bytes_per_sample)
        else:
            raise ValueError(f"Unknown device: {device}")
    
    def _get_device_module(self, device: str):
        """Get the appropriate device module.
        
        Args:
            device: Device type name
            
        Returns:
            Device module or None if not available
        """
        device_map = {
            'bitbabbler': dev_bitb,
            'truerng': dev_trng,
            'pseudo': dev_pseudo
        }
        return device_map.get(device.lower())
