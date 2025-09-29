"""
Filename utilities for RngKit CLI.
"""

import re
from datetime import datetime, timedelta
import os
from pathlib import Path
from typing import Optional


def format_capture_name(device: str, bits: int, interval: int, folds: Optional[int] = None) -> str:
    """Return canonical filename stem for a capture.

    Example: 20201011T142208_bitb_s2048_i1_f0
    """
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    name = f"{ts}_{device}_s{bits}_i{interval}"
    if device == "bitb" and folds is not None:
        name += f"_f{folds}"
    return name


def parse_bits(name: str) -> int:
    """Parse bits from filename."""
    m = re.search(r"_s(\d+)_", name)
    if not m:
        raise ValueError("bits not found in name")
    return int(m.group(1))


def parse_interval(name: str) -> int:
    """Parse interval from filename."""
    m = re.search(r"_i(\d+)", name)
    if not m:
        raise ValueError("interval not found in name")
    return int(m.group(1))


def get_unique_capture_name(
    device: str,
    bits: int,
    interval: int,
    folds: Optional[int] = None,
    output_dir: str = "./data/raw/"
) -> str:
    """
    Generate a unique capture filename stem by incrementing the timestamp until no .bin file conflict.

    Args:
        device: Device suffix (e.g., 'bitb', 'trng', 'pseudo')
        bits: Number of bits per sample
        interval: Sample interval in seconds
        folds: Optional XOR folds for BitBabbler
        output_dir: Directory to save files and check conflicts

    Returns:
        str: Unique filename stem without extension
    """
    os.makedirs(output_dir, exist_ok=True)
    dt = datetime.now()
    while True:
        ts = dt.strftime("%Y%m%dT%H%M%S")
        name = f"{ts}_{device}_s{bits}_i{interval}"
        if device == "bitb" and folds is not None:
            name += f"_f{folds}"
        full_path = Path(output_dir) / f"{name}.bin"
        if not full_path.exists():
            return name
        dt += timedelta(seconds=1)