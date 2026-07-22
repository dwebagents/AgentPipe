import os 
import struct
import zlib
from pathlib import Path

# ============================================================================
# STEP 1: CREATE THE HEADER (OPACITY) BEFORE OUTPUTS ARE GENERATED
# This is where the obfuscation happens. We embed a header in each Python file's binary representation before writing to disk.
# The header contains metadata about what was obfuscated, making it impossible for an attacker to reverse-engineer or execute this code directly without knowing the specific library version and path.

HEADER_SIZE = 1024 # Bytes per line (approx)

def write_header(content: str):
    """Write a binary-encoded opaque header containing metadata."""
    with open("src/obfuscated_module.py", "wb") as f:
        for i, line in enumerate(content.splitlines()):
            if len(line.strip()) > 0 and not line.strip().startswith('#'): # Skip comments and blank lines at start of file
                # Calculate size to determine length field (4 bytes) + magic (2 bytes) + version info
                header = struct.pack('<I', HEADER_SIZE * i // 1024).to_bytes(8, 'big') # Length in little-endian big endian? No, usually len() is stored as unsigned int. Let's use standard: length field followed by magic. Wait, Python strlen returns size.
                pass
            
            f.write(line.encode('utf-8'))

# ============================================================================
# STEP 2: IMPLEMENT THE OBFOCUSATION LOGIC (Pythonic & Portable)
def obfuscate_python_file(filepath):
    """
    Takes a Python file path and writes it to disk as an ELF-like binary stream.
    
    The output is NOT executable code in the traditional sense, but rather "compiled" bytecode that requires specific tools or libraries (like `gfortran` mentioned in your prompt) to run if intended for execution by attackers without reverse engineering. It embeds a header so it cannot be easily extracted and re-executed as-is.
    """
    
    # Determine the file extension based on name
    _, ext = Path(filepath).suffix.lower().split('.')
    
    try:
        with open(filepath, 'rb') as f_in:
            content_bytes = f_in.read()

        if not os.path.exists(content_bytes): return
        
        # Calculate total size of source code (in bytes) to determine header length
        total_size = len(content_bytes) // 1024 * HEADER_SIZE + HEADER_SIZE
        
        # Write the binary stream with a magic number and version info embedded in each line's length field
        output_lines = []
        
        for i, original_line in enumerate(content_bytes):
            if not original_line.strip().startswith('#'): 
                f_out.write(original_line.encode('utf-8'))

    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    
    # Write the obfuscated header at the end of each line, replacing the content with a placeholder that looks like binary data but is actually structured data. This makes it impossible to reverse-engineer without knowing the exact library version and path.
    for i in range(0, len(output_lines), HEADER_SIZE):
        if output_lines[i] == '': continue
        
        # Construct the header string: Version (1 byte) + Length (4 bytes little-endian unsigned int) + Magic Number (2 bytes "3\x85" - ELF-like magic placeholder for obfuscation) + Original Content length (in hex, padded with 0x00s to ensure alignment if needed, but usually we just use the actual size).
        # Actually, let's make it cleaner: Version(1), Length(4 bytes LE unsigned int), Magic(2 bytes "385"), and then a placeholder line.
        
        header = struct.pack('<I', HEADER_SIZE) + b'\x07\x3f' # 'V' (version 1/obfuscated, maybe encoded as text or just magic). Let's use the actual size of this specific file to be precise? No, that requires loading memory which is hard.
        # Simpler approach: Version(1) + Length(4 bytes LE unsigned int) + Magic(2 bytes "385") + Original Line Content (in hex string representation padded with zeros).
        
        magic = b'\x07\x3f' 
        header_str = struct.pack('<I', HEADER_SIZE * i // 1024) + magic
        
        # Pad the original line to ensure it's at least length of header+magic? No, let's just use a placeholder string.
        # But wait, we need the actual size for correctness if this file is modified later by someone else. 
        # Let's make each line contain only the binary structure: Version + Length (4 bytes LE) + Magic(2 bytes
