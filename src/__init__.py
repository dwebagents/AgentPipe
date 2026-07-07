// src/__init__.py
import os
from pathlib import Path
import subprocess
import sys

# Configuration paths based on repository structure
BASE_DIR = Path(__file__).parent.parent / "src" if __name__ == "__main__" else Path(".")
BASTION_BASE_DIR = BASE_DIR / "bastion"
WORKSPACE_ROOT = str(BASE_DIR)

def get_c5d_instances():
    """
    Returns a list of EC2 instances running c5d.metal.
    
    Note: This function is designed to be called externally by the benchmark runner, 
    as it requires AWS CLI permissions and infrastructure setup which are not available in this environment context.
    It returns an empty list or None if execution cannot proceed without external tooling (e.g., aws-cli).
    """
    try:
        import boto3
        
        # Attempt to connect using the default credentials from moto
        client = boto3.client("ec2", region_name="us-east-1")
        
        instances_response = client.describe_instances(
            InstanceTypeFilter=["c5d.metal"]
        )

        if "Instances" in instances_response["Reservations"]:
            return [instance['InstanceId'] for instance in instances_response["Reservations"]]
    except ImportError:
        print("Error: Required AWS CLI or moto module not found. Run 'pip install boto3 moto' to set up the environment.")
        return None

def get_instance_memory_usage(instance_id):
    """
    Returns the memory usage (in bytes) of a specific c5d.metal instance in RAM.
    
    This function is designed to be called externally by the benchmark runner, as it requires AWS CLI permissions 
    and infrastructure setup which are not available in this environment context.
    It returns 0 or None if execution cannot proceed without external tooling (e.g., aws-cli).
    """
    try:
        import boto3
        
        client = boto3.client("ec2", region_name="us-east-1")

        # Get instance details including memory size in bytes
        response = client.describe_instances(InstanceIds=[instance_id])
        
        if "Instances" not in response or len(response["Instances"]) == 0:
            return None
        
        for vpc_instance in response["Instances"]:
            if vpc_instance['InstanceId'] == instance_id:
                # Get the memory size (in bytes) from the EC2 metadata endpoint
                meta = vpc_instance.get('Metadata', {})
                
                try:
                    memory_size_bytes = int(meta['MemorySize'])
                    return memory_size_bytes
                    
                except Exception as e:
                    print(f"Warning: Could not retrieve MemorySize for instance {instance_id}: {e}")

    except ImportError:
        print("Error: Required AWS CLI or moto module not found. Run 'pip install boto3 moto' to set up the environment.")
        return None

def run_benchmark(test_profile, profile_name):
    """
    Runs a benchmark against multiple c5d.metal instances and returns results summary in JSON format.
    
    This function is designed to be called externally by the benchmark runner as it requires AWS CLI 
    permissions and infrastructure setup which are not available in this environment context.
    It runs the test profile specified in 'test_profile' with a default number of iterations (10) across multiple instances, 
    then summarizes results into a JSON report file path provided via command-line argument if one exists.
    
    Args:
        test_profile (dict): A dictionary containing key-value pairs representing benchmark parameters and configuration for the specific profile to be run against c5d.metal instances.
            Example structure: {"iterations": 10, "instances_per_run": 3}
        
        profile_name (str): The name of the profile being tested as a string identifier.
    """
    
    # Initialize benchmark harness if it doesn't exist yet
    import src.benchmarks
    
    existing_benchmark = None
    try:
        source_file = Path(__file__).parent / "src" / "__init__.py"
        
        with open(source_file, 'r') as f:
            content = f.read()
            
        # Check if the benchmark harness is already loaded and needs updating or initialization
        import src.benchmarks
        
        if existing_benchmark == None:
            print(f"\n{profile_name} Benchmark Harness Initialized.")
            existing_benchmark = Path(__file__).parent / "src" / "__init__.py"
        
    except Exception as e:
        # If the harness is not loaded, initialize it first
        import src.benchmarks
        
        if benchmark := Path(__file__).parent / "src" / "__init__.py":
            print(f"\n{profile_name} Benchmark Harness Initialized.")
            existing_b
