#!/usr/bin/env python3
"""
CPU Profiler for Milestone 04
Monitors CPU usage and saves data to csv file for graphing
"""
import psutil
import time
import csv
import sys
from datetime import datetime

def monitor_cpu(duration=60, interval=1, output_file='cpu_usage.csv'):
    """
    Monitor CPU usage for specified duration
    
    Args:
        duration: total monitoring time in seconds
        interval: sampling interval in seconds
        output_file: CSV file to save results
    """
    print(f"Starting CPU monitoring for {duration} seconds...")
    print(f"Sampling every {interval} seconds")
    print(f"Data will be saved to: {output_file}")
    print("Press Ctrl+C to stop early\n")
    
    # Write header
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'cpu_percent', 'cpu_count'])
    
    start_time = time.time()
    sample_count = 0
    
    try:
        while (time.time() - start_time) < duration:
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=interval)
            timestamp = datetime.now().isoformat()
            
            # Write to CSV
            with open(output_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, cpu_percent, psutil.cpu_count()])
            
            sample_count += 1
            elapsed = time.time() - start_time
            
            # Print progress
            print(f"[{elapsed:5.1f}s] CPU: {cpu_percent:5.1f}% (Sample {sample_count})", end='\r')
            
    except KeyboardInterrupt:
        print(f"\n\nMonitoring stopped by user after {sample_count} samples")
    
    print(f"\nMonitoring complete. {sample_count} samples saved to {output_file}")
    
    # Calculate statistics
    try:
        import pandas as pd
        df = pd.read_csv(output_file)
        print(f"\nStatistics:")
        print(f"  Average CPU: {df['cpu_percent'].mean():.2f}%")
        print(f"  Max CPU: {df['cpu_percent'].max():.2f}%")
        print(f"  Min CPU: {df['cpu_percent'].min():.2f}%")
    except ImportError:
        # Fallback if pandas not available
        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            cpu_values = [float(row[1]) for row in reader]
        if cpu_values:
            print(f"\nStatistics:")
            print(f"  Average CPU: {sum(cpu_values)/len(cpu_values):.2f}%")
            print(f"  Max CPU: {max(cpu_values):.2f}%")
            print(f"  Min CPU: {min(cpu_values):.2f}%")

if __name__ == "__main__":
    # Default: monitor for 60 seconds, 1-second intervals
    duration = 60
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
        except ValueError:
            print("Usage: python cpu_profiler.py [duration_seconds]")
            sys.exit(1)
    
    monitor_cpu(duration=duration)