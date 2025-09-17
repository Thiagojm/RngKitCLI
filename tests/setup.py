#!/usr/bin/env python3
"""
Setup script for RngKit CLI.

This script handles the installation and distribution of the RngKit CLI package.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "RngKit CLI - Command Line Interface for Random Number Generator Data Collection and Analysis"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="rngkit-cli",
    version="1.0.0",
    author="Thiago Jung",
    author_email="thiagojm1984@hotmail.com",
    description="Command Line Interface for Random Number Generator Data Collection and Analysis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Thiagojm/RngKitCLI",
    project_urls={
        "Bug Reports": "https://github.com/Thiagojm/RngKitCLI/issues",
        "Source": "https://github.com/Thiagojm/RngKitCLI",
        "Documentation": "https://github.com/Thiagojm/RngKitCLI#readme",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "rngkit=main:main",
        ],
    },
    keywords="random number generator, trng, bitbabbler, truerng, cryptography, statistics, cli",
    include_package_data=True,
    zip_safe=False,
)

