# Changelog

All notable changes to RngKit CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-27

### Added
- Initial release of RngKit CLI
- Command-line interface for data collection and analysis
- Support for BitBabbler, TrueRNG, and Pseudo RNG devices
- Data collection with configurable parameters (bits, interval, duration)
- Statistical analysis with Z-score calculations
- Excel report generation with charts
- CSV file concatenation functionality
- Device status checking
- Comprehensive help system
- Cross-platform support (Windows, Linux, macOS)
- Installation script and demo
- Extensive documentation and examples

### Features
- **Data Collection**: Collect data from various RNG devices with customizable parameters
- **Analysis**: Generate statistical reports and Excel files with Z-score charts
- **Concatenation**: Combine multiple CSV files for extended analysis
- **Device Management**: Check status and availability of RNG devices
- **CLI Interface**: Full command-line interface with comprehensive argument parsing
- **Progress Indicators**: Real-time progress bars and status updates
- **Error Handling**: Robust error handling with detailed error messages
- **Documentation**: Complete README with usage examples and troubleshooting

### Technical Details
- Python 3.8+ support
- Minimal dependencies (no GUI components)
- Modular architecture with separate modules for collection, analysis, and utilities
- Fallback implementations for core functionality
- Compatible with original RngKitST modules
- MIT License

