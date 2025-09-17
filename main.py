#!/usr/bin/env python3
"""
RngKit CLI - Command Line Interface for Random Number Generator Data Collection and Analysis

A powerful CLI tool for collecting and analyzing data from True Random Number Generators (TRNGs)
and Pseudo Random Number Generators (PRNGs).

Author: Thiago Jung
Email: thiagojm1984@hotmail.com
"""

import argparse
import sys
import os
from typing import Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rngkit_cli.collector import DataCollector
from rngkit_cli.analyzer import DataAnalyzer
from rngkit_cli.utils import ensure_data_dir, print_banner, print_device_status


def main() -> None:
    """Main entry point for RngKit CLI."""
    parser = argparse.ArgumentParser(
        description="RngKit CLI - Random Number Generator Data Collection and Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Collect data from BitBabbler
  python main.py collect --device bitbabbler --bits 2048 --interval 1 --duration 60

  # Analyze a CSV file
  python main.py analyze --file data/raw/sample.csv --bits 2048 --interval 1

  # Analyze a binary file
  python main.py analyze --file data/raw/sample.bin --bits 2048 --interval 1

  # Concatenate multiple CSV files
  python main.py concat --files file1.csv file2.csv --output combined.csv --bits 2048 --interval 1

  # Check device status
  python main.py status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Collect command
    collect_parser = subparsers.add_parser('collect', help='Collect data from RNG device')
    collect_parser.add_argument('--device', '-d', 
                               choices=['bitbabbler', 'truerng', 'pseudo'], 
                               required=True,
                               help='RNG device to use')
    collect_parser.add_argument('--bits', '-b', 
                               type=int, 
                               default=2048,
                               help='Number of bits per sample (default: 2048)')
    collect_parser.add_argument('--interval', '-i', 
                               type=int, 
                               default=1,
                               help='Sample interval in seconds (default: 1)')
    collect_parser.add_argument('--duration', '-t', 
                               type=int, 
                               help='Collection duration in seconds (default: unlimited)')
    collect_parser.add_argument('--folds', '-f', 
                               type=int, 
                               choices=[0, 1, 2, 3, 4],
                               default=0,
                               help='BitBabbler XOR folds (0=RAW, 1-4=folds, default: 0)')
    collect_parser.add_argument('--output', '-o', 
                               help='Output filename (without extension)')
    collect_parser.add_argument('--verbose', '-v', 
                               action='store_true',
                               help='Enable verbose output')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze collected data')
    analyze_parser.add_argument('--file', '-f', 
                               required=True,
                               help='Input file to analyze (.csv or .bin)')
    analyze_parser.add_argument('--bits', '-b', 
                               type=int, 
                               required=True,
                               help='Number of bits per sample')
    analyze_parser.add_argument('--interval', '-i', 
                               type=int, 
                               required=True,
                               help='Sample interval in seconds')
    analyze_parser.add_argument('--output', '-o', 
                               help='Output Excel filename (default: auto-generated)')
    analyze_parser.add_argument('--verbose', '-v', 
                               action='store_true',
                               help='Enable verbose output')
    
    # Concatenate command
    concat_parser = subparsers.add_parser('concat', help='Concatenate multiple CSV files')
    concat_parser.add_argument('--files', '-f', 
                              nargs='+', 
                              required=True,
                              help='CSV files to concatenate')
    concat_parser.add_argument('--output', '-o', 
                              required=True,
                              help='Output CSV filename')
    concat_parser.add_argument('--bits', '-b', 
                              type=int, 
                              required=True,
                              help='Number of bits per sample')
    concat_parser.add_argument('--interval', '-i', 
                              type=int, 
                              required=True,
                              help='Sample interval in seconds')
    concat_parser.add_argument('--verbose', '-v', 
                              action='store_true',
                              help='Enable verbose output')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Check device status')
    status_parser.add_argument('--verbose', '-v', 
                              action='store_true',
                              help='Enable verbose output')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Ensure data directory exists
    data_dir = ensure_data_dir()
    if args.verbose:
        print(f"Data directory: {data_dir}")
    
    # Execute command
    try:
        if args.command == 'collect':
            collector = DataCollector(verbose=args.verbose)
            collector.collect(
                device=args.device,
                bits=args.bits,
                interval=args.interval,
                duration=args.duration,
                folds=args.folds,
                output_file=args.output
            )
        elif args.command == 'analyze':
            analyzer = DataAnalyzer(verbose=args.verbose)
            analyzer.analyze(
                file_path=args.file,
                bits=args.bits,
                interval=args.interval,
                output_file=args.output
            )
        elif args.command == 'concat':
            analyzer = DataAnalyzer(verbose=args.verbose)
            analyzer.concatenate(
                files=args.files,
                output_file=args.output,
                bits=args.bits,
                interval=args.interval
            )
        elif args.command == 'status':
            print_device_status(verbose=args.verbose)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
