"""
Device management utilities for RngKit CLI.

This module provides device detection and management functionality
for various RNG hardware devices.
"""

from typing import Dict, Any, Optional

try:
    from ..devices import bitbabbler as dev_bitb
    from ..devices import truerng as dev_trng
    from ..devices import pseudo as dev_pseudo
except ImportError:
    # Fallback if modules not found
    dev_bitb = None
    dev_trng = None
    dev_pseudo = None


class DeviceManager:
    """Manages RNG device detection and access."""
    
    def __init__(self):
        """Initialize the device manager."""
        self.devices = {
            'bitbabbler': self.check_bitbabbler,
            'truerng': self.check_truerng,
            'pseudo': self.check_pseudo
        }
    
    def check_bitbabbler(self) -> Dict[str, Any]:
        """Check BitBabbler device availability.
        
        Returns:
            Dictionary with device status information
        """
        if dev_bitb is None:
            return {
                'available': False,
                'error': 'BitBabbler module not available'
            }
        
        try:
            if dev_bitb.detect():
                return {
                    'available': True,
                    'info': 'BitBabbler device detected and accessible'
                }
            else:
                return {
                    'available': False,
                    'error': 'BitBabbler device not detected'
                }
        except Exception as e:
            return {
                'available': False,
                'error': f'BitBabbler detection failed: {str(e)}'
            }
    
    def check_truerng(self) -> Dict[str, Any]:
        """Check TrueRNG device availability.
        
        Returns:
            Dictionary with device status information
        """
        if dev_trng is None:
            return {
                'available': False,
                'error': 'TrueRNG module not available'
            }
        
        try:
            if dev_trng.detect():
                return {
                    'available': True,
                    'info': 'TrueRNG device detected and accessible'
                }
            else:
                return {
                    'available': False,
                    'error': 'TrueRNG device not detected'
                }
        except Exception as e:
            return {
                'available': False,
                'error': f'TrueRNG detection failed: {str(e)}'
            }
    
    def check_pseudo(self) -> Dict[str, Any]:
        """Check Pseudo RNG availability.
        
        Returns:
            Dictionary with device status information
        """
        if dev_pseudo is None:
            return {
                'available': False,
                'error': 'Pseudo RNG module not available'
            }
        
        try:
            if dev_pseudo.detect():
                return {
                    'available': True,
                    'info': 'Pseudo RNG (Python secrets) available'
                }
            else:
                return {
                    'available': False,
                    'error': 'Pseudo RNG not available'
                }
        except Exception as e:
            return {
                'available': False,
                'error': f'Pseudo RNG detection failed: {str(e)}'
            }
    
    def get_device(self, device_name: str):
        """Get device module by name.
        
        Args:
            device_name: Name of the device ('bitbabbler', 'truerng', 'pseudo')
            
        Returns:
            Device module or None if not found
        """
        device_map = {
            'bitbabbler': dev_bitb,
            'truerng': dev_trng,
            'pseudo': dev_pseudo
        }
        return device_map.get(device_name.lower())
    
    def is_device_available(self, device_name: str) -> bool:
        """Check if a specific device is available.
        
        Args:
            device_name: Name of the device to check
            
        Returns:
            True if device is available, False otherwise
        """
        if device_name.lower() not in self.devices:
            return False
        
        status = self.devices[device_name.lower()]()
        return status['available']

