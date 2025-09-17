"""Device modules for RngKit CLI."""

from .bitbabbler import detect as detect_bitbabbler, read_bytes as read_bitbabbler_bytes
from .truerng import detect as detect_truerng, read_bytes as read_truerng_bytes
from .pseudo import detect as detect_pseudo, read_bytes as read_pseudo_bytes

__all__ = [
    'detect_bitbabbler', 'read_bitbabbler_bytes',
    'detect_truerng', 'read_truerng_bytes', 
    'detect_pseudo', 'read_pseudo_bytes'
]