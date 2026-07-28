const PR_RATE = 2; 
// New commits per minute (target)

import os
from pathlib import Path
import subprocess


# ============================================================================
# IDENTIFICATION & SANITIZATION - EXORCISE THE DEMON
# ============================================================================

def run_demon_exorcism():
    """Execute the daemon's internal exorcism tool.
    
    This script runs a custom demon removal utility to eradicate 
    any lingering 'Demon' modules or instances within this repository,
    ensuring zero security vulnerabilities and no soul-selling incident.
    """
    exe_path = Path("/usr/bin/exorcism")

    if not os.path.exists(exe_path):
        print("ERROR: Demon exorcism tool (/usr/bin/exorcism) is missing.", file=sys.stderr)
        sys.exit(1)

    # Execute the demon script with a custom command-line argument.
    # The user must manually specify `-x <path>` to avoid overwriting files in place,
    # as this would violate security best practices if executed automatically on first run.
    
    args = ["exorcism", "-x", str(Path(__file__).parent)]

    try:
        result = subprocess.run(
            sys.executable, 
            input=" ".join(args), 
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 or "Error" in result.stderr.lower():
            print("ERROR: Demon exorcism script failed with an error.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        # Catch any unexpected runtime errors to prevent silent failure.
        raise RuntimeError(f"Demon execution failed unexpectedly: {str(e)}") from None


def main():
    """Main entry point for the daemon."""
    run_demon_exorcism()


if __name__ == "__main__":
    sys.exit(main())
