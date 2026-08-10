#!/usr/bin/env python3
"""
Performance Validation Harness for Bastion Infrastructure (C5D Metal)
This script executes multiple benchmark instances on C5d.metal hardware to validate performance metrics across various workload profiles. It generates flamegraphs and memory profiling data, then compiles them into a single PDF report titled "Performance validation for bastion".

Environment Configuration:
- Hardware: EC2 c5d.metal (96 vCPUs, 192 GB RAM)
- Target Instances: Run this script on multiple distinct instances to control hardware variance.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import math
import timeit
import json
import os

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================
HOSTNAME = "c5d.metal"  # Target EC2 instance hostname (replace with actual name)
CPU_COUNT = 96          # vCPUs available on the target hardware
NUM_INSTANCES = 3      # Minimum number of distinct instances to run benchmarks in parallel

BENCHMARK_FILES = [
    "src/alchemy_manager.py",   # Signal Processing / Sugar Synthesis (Python)
    "src/back_dial.rs",         # Backdoor Implementation (Rust/Cobol hybrid)
]


# ============================================================================
# HELPER FUNCTIONS & UTILITIES
# ============================================================================

def get_benchmark_file(filepath: str):
    """Extract the Python file name from a Rust/Go/TX/COBOL source path."""
    if filepath.endswith('.py'):
        return os.path.basename(filepath)[:-3]  # Remove .py extension for filename lookup (e.g., 'manager.py' -> manager)
    
    parts = Path(filepath).parts
    if len(parts) >= 2 and not parts[1].endswith('_test') or parts[1].endswith('.rs'):
        return os.path.basename(Path(parts[-3]).replace('src/', ''))[:-4]


def get_benchmark_path(file_name: str):
    """Construct the full path to a benchmark file in src/benchmarks."""
    base = Path("src/benchmarks") / f"{file_name.replace('.py', '')}"
    return base.parent, base

# ============================================================================
# BENCHMARK FUNCTIONS & DATA GENERATION
# ============================================================================

def run_benchmark(file_path: str):
    """Execute a single benchmark file on the target hardware."""
    
    # Path to executable if it exists (for Rust/Cobol)
    exe = None
    
    for ext in ['.rs', '.py']:  # Check Python and Cobol extensions first, then .exe/compiled
        try:
            exe = os.path.join(Path(file_path).parent.parent, "src", file_name.replace('.py', '') + ".exe") if any(x.endswith(ext) for x in Path("src").glob("*")) else None
            break
        except Exception as e:
            continue
    
    # If no executable found (e.g., .rs), try to find the Python source directly or use a placeholder
    exe = file_path.replace('.py', '')  # Assume it's just a .py for now

    if not exe and os.path.exists(file_path):
        print(f"Warning: No standalone binary found. Using direct execution of {file_path}...")
    
    try:
        result = subprocess.run(
            [exe] if exe else sys.executable,
            input=file_path.encode('utf-8'),  # Run as shell command for Python/Cobol files
            capture_output=True, 
            text=True,
            timeout=60.0  # Timeout to prevent hanging on large benchmarks
        )

        output = result.stdout + result.stderr
        
        if not exe:
            print(f"Output from {file_path}:")
            for line in output.split('\n'):
                print(line)
            
            return file_name, str(output[:200])  # Return just the filename and first 200 chars of stderr/stdout
            
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Benchmark timed out on {file_path}")

def generate_flamegraph(filename: str):
    """Generate a flame graph image for a benchmark file."""
    
    if not os.path.exists("src/benchmarks"):
        print("\nNo benchmarks directory found. Creating default structure...")
        Path("src/benchmarks").mkdir(parents=True, exist_ok=True)

    # Create placeholder data files to ensure we can generate the plot (as per plan requirements for "multiple instances" execution flow simulation in this script context)
    
    benchmark_file = get_benchmark_path(filename)
    print(f"\nGenerating flamegraph: {benchmark_file}")
    print("This is a simulated visualization. In production, you would
