"""
Data analysis module for RngKit CLI.

This module provides functionality for analyzing collected RNG data
and generating statistical reports and visualizations.
"""

import os
import sys
from typing import List, Optional
from datetime import datetime

try:
    from .services import storage as storage_service
    from .services import filenames as fn_service
except ImportError:
    # Fallback if modules not found
    storage_service = None
    fn_service = None

from .utils import ensure_data_dir


class DataAnalyzer:
    """Handles data analysis and report generation."""
    
    def __init__(self, verbose: bool = False):
        """Initialize the data analyzer.
        
        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose
        self.data_dir = ensure_data_dir()
    
    def analyze(self, file_path: str, bits: int, interval: int, 
                output_file: Optional[str] = None) -> str:
        """Analyze a data file and generate Excel report.
        
        Args:
            file_path: Path to input file (.csv or .bin)
            bits: Number of bits per sample
            interval: Sample interval in seconds
            output_file: Output Excel filename (optional)
            
        Returns:
            Path to generated Excel file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If parameters are invalid
            RuntimeError: If analysis fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        if bits <= 0 or (bits % 8) != 0:
            raise ValueError("Bits must be positive and divisible by 8")
        
        if interval <= 0:
            raise ValueError("Interval must be positive")
        
        if self.verbose:
            print(f"Analyzing file: {file_path}")
            print(f"Sample size: {bits} bits")
            print(f"Sample interval: {interval} seconds")
        
        try:
            # Read data based on file extension
            if file_path.endswith('.bin'):
                if storage_service:
                    df = storage_service.read_bin_counts(file_path, bits)
                else:
                    df = self._read_bin_counts_fallback(file_path, bits)
            elif file_path.endswith('.csv'):
                if storage_service:
                    df = storage_service.read_csv_counts(file_path)
                else:
                    df = self._read_csv_counts_fallback(file_path)
            else:
                raise ValueError("Unsupported file format. Use .csv or .bin files")
            
            if self.verbose:
                print(f"Loaded {len(df)} samples")
            
            # Add Z-score calculations
            if storage_service:
                df = storage_service.add_zscore(df, bits)
            else:
                df = self._add_zscore_fallback(df, bits)
            
            # Generate output filename
            if output_file is None:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                output_file = f"{base_name}_analysis.xlsx"
            
            # Ensure output is in data directory
            if not os.path.isabs(output_file):
                output_file = os.path.join(self.data_dir, output_file)
            
            # Write Excel report
            if storage_service:
                excel_path = storage_service.write_excel_with_chart(df, file_path, bits, interval)
            else:
                excel_path = self._write_excel_fallback(df, output_file, bits, interval)
            
            # Always show success status
            print(f"✅ Analysis completed successfully!")
            print(f"📊 Generated Excel report: {excel_path}")
            print(f"📈 Analyzed {len(df)} samples with {bits}-bit blocks")
            
            if self.verbose:
                print(f"📁 Full path: {os.path.abspath(excel_path)}")
            
            return excel_path
            
        except Exception as e:
            raise RuntimeError(f"Analysis failed: {str(e)}")
    
    def concatenate(self, files: List[str], output_file: str, bits: int, interval: int) -> str:
        """Concatenate multiple CSV files.
        
        Args:
            files: List of CSV file paths to concatenate
            output_file: Output CSV filename
            bits: Number of bits per sample
            interval: Sample interval in seconds
            
        Returns:
            Path to concatenated CSV file
            
        Raises:
            FileNotFoundError: If any input file doesn't exist
            ValueError: If parameters are invalid
            RuntimeError: If concatenation fails
        """
        if not files:
            raise ValueError("No files provided for concatenation")
        
        if len(files) < 2:
            raise ValueError("At least 2 files required for concatenation")
        
        # Check all files exist
        for file_path in files:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Input file not found: {file_path}")
        
        if self.verbose:
            print(f"Concatenating {len(files)} files:")
            for file_path in files:
                print(f"  - {file_path}")
        
        try:
            # Generate output filename with timestamp
            if not os.path.isabs(output_file):
                output_file = os.path.join(self.data_dir, output_file)
            
            # Ensure output file has .csv extension
            if not output_file.endswith('.csv'):
                output_file += '.csv'
            
            if storage_service:
                # Create output stem with timestamp and parameters
                timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
                out_stem = f"{timestamp}_concat_s{bits}_i{interval}"
                out_stem = os.path.join(os.path.dirname(output_file), out_stem)
                concat_path = storage_service.concat_csv_files(files, out_stem)
            else:
                concat_path = self._concat_csv_fallback(files, output_file)
            
            # Always show success status
            print(f"✅ Concatenation completed successfully!")
            print(f"📄 Generated combined CSV: {concat_path}")
            print(f"🔗 Combined {len(files)} files with {bits}-bit samples")
            
            if self.verbose:
                print(f"📁 Full path: {os.path.abspath(concat_path)}")
                print(f"📊 Input files processed:")
                for i, file_path in enumerate(files, 1):
                    print(f"   {i}. {os.path.basename(file_path)}")
            
            return concat_path
            
        except Exception as e:
            raise RuntimeError(f"Concatenation failed: {str(e)}")
    
    def _read_bin_counts_fallback(self, file_path: str, block_bits: int):
        """Fallback method to read binary file and count bits."""
        import pandas as pd
        from bitstring import BitArray
        
        data_list = []
        with open(file_path, 'rb') as binary_file:
            block = 1
            while True:
                data = binary_file.read(block_bits // 8)
                if not data:
                    break
                ones = BitArray(data).count(1)
                data_list.append([block, ones])
                block += 1
        
        return pd.DataFrame(data_list, columns=['samples', 'ones'])
    
    def _read_csv_counts_fallback(self, file_path: str):
        """Fallback method to read CSV file."""
        import pandas as pd
        
        df = pd.read_csv(file_path, header=None, names=['time', 'ones'])
        df['time'] = pd.to_datetime(df['time'], format='%Y%m%dT%H%M%S').apply(lambda x: x.strftime('%H:%M:%S'))
        return df
    
    def _add_zscore_fallback(self, df, block_bits: int):
        """Fallback method to add Z-score calculations."""
        import numpy as np
        
        expected_mean = 0.5 * block_bits
        expected_std_dev = np.sqrt(block_bits * 0.5 * 0.5)
        df['cumulative_mean'] = df['ones'].expanding().mean()
        df['z_test'] = (df['cumulative_mean'] - expected_mean) / (expected_std_dev / np.sqrt(df.index + 1))
        return df
    
    def _write_excel_fallback(self, df, output_file: str, block_bits: int, interval: int):
        """Fallback method to write Excel file with chart."""
        import pandas as pd
        import xlsxwriter
        
        try:
            writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Zscore', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Zscore']
            chart = workbook.add_chart({'type': 'line'})
            chart.add_series({
                'categories': ['Zscore', 1, 0, len(df), 0], 
                'values': ['Zscore', 1, 3, len(df), 3]
            })
            chart.set_title({'name': os.path.basename(output_file)})
            chart.set_x_axis({'name': f'Number of Samples - one sample every {interval} second(s)', 'date_axis': True})
            chart.set_y_axis({'name': f'Z-Score - Sample Size = {block_bits} bits'})
            chart.set_legend({'none': True})
            worksheet.insert_chart('F2', chart)
            writer.close()
            return output_file
        except Exception as e:
            # If xlsxwriter fails, just save as CSV
            csv_file = output_file.replace('.xlsx', '.csv')
            df.to_csv(csv_file, index=False)
            return csv_file
    
    def _concat_csv_fallback(self, files: List[str], output_file: str):
        """Fallback method to concatenate CSV files."""
        with open(output_file, 'w', newline='') as out:
            for i, file_path in enumerate(files):
                with open(file_path, 'r') as f:
                    if i > 0:  # Skip header for all but first file
                        next(f)
                    for line in f:
                        out.write(line)
        return output_file

