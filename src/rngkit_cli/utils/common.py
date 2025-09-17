"""
Common utility functions for RngKit CLI.

This module provides utility functions for data directory management,
parameter validation, and user interface elements.
"""

import os
import sys
from typing import Dict, Any


def ensure_data_dir() -> str:
    """Ensure data directory exists and return its path.
    
    Returns:
        Path to the data directory (created if it doesn't exist)
        
    Raises:
        OSError: If directory cannot be created
    """
    default_dir = os.path.join(os.getcwd(), "data", "raw")
    base = os.environ.get("RNGKIT_DATA_DIR", default_dir)
    os.makedirs(base, exist_ok=True)
    return base


def validate_params(bit_count: int, time_count: int) -> bool:
    """Validate RNG collection parameters.
    
    Args:
        bit_count: Number of bits per sample (must be positive and divisible by 8)
        time_count: Sample interval in seconds (must be >= 1)
        
    Returns:
        True if parameters are valid, False otherwise
    """
    if bit_count <= 0 or (bit_count % 8) != 0:
        return False
    if time_count < 1:
        return False
    return True


def print_banner() -> None:
    """Print the RngKit CLI banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗██╗████████╗    ██████╗██╗     ██╗        ║
║  ██╔══██╗████╗  ██║██╔════╝ ██║ ██╔╝██║╚══██╔══╝   ██╔════╝██║     ██║        ║
║  ██████╔╝██╔██╗ ██║██║  ███╗█████╔╝ ██║   ██║      ██║     ██║     ██║        ║
║  ██╔══██╗██║╚██╗██║██║   ██║██╔═██╗ ██║   ██║      ██║     ██║     ██║        ║
║  ██║  ██║██║ ╚████║╚██████╔╝██║  ██╗██║   ██║      ╚██████╗███████╗██║        ║
║  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝       ╚═════╝╚══════╝╚═╝        ║
║                                                                              ║
║  Command Line Interface for Random Number Generator Data Collection          ║
║  Version 1.0.0 - by Thiago Jung (thiagojm1984@hotmail.com)                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_device_status(verbose: bool = False) -> None:
    """Print status of all available RNG devices.
    
    Args:
        verbose: If True, show detailed device information
    """
    from .devices import DeviceManager
    
    print("🔍 Checking RNG Device Status...")
    print("=" * 50)
    
    device_manager = DeviceManager()
    devices = {
        'BitBabbler': device_manager.check_bitbabbler(),
        'TrueRNG': device_manager.check_truerng(),
        'Pseudo RNG': device_manager.check_pseudo()
    }
    
    for device_name, status in devices.items():
        if status['available']:
            print(f"✅ {device_name}: Available")
            if verbose and 'info' in status:
                print(f"   {status['info']}")
        else:
            print(f"❌ {device_name}: Not Available")
            if verbose and 'error' in status:
                print(f"   Error: {status['error']}")
    
    print("=" * 50)
    
    available_count = sum(1 for status in devices.values() if status['available'])
    if available_count == 0:
        print("⚠️  No RNG devices available. Pseudo RNG will be used for testing.")
    else:
        print(f"✅ {available_count} device(s) available for data collection.")


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "1h 23m 45s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}h {minutes}m {secs:.1f}s"


def print_progress(current: int, total: int, prefix: str = "Progress") -> None:
    """Print a progress bar.
    
    Args:
        current: Current progress value
        total: Total progress value
        prefix: Prefix text for the progress bar
    """
    if total == 0:
        return
    
    percent = (current / total) * 100
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    print(f'\r{prefix}: |{bar}| {percent:.1f}% ({current}/{total})', end='', flush=True)
    
    if current == total:
        print()  # New line when complete
