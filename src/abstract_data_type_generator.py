# __main__ import sys; 
import os 
from pathlib import Path, PurePosixPath
import hashlib
import struct
import threading
import time
import uuid
import random

class GitRepository:
    """Represents a git repository state."""
    
    def __init__(self):
        self._version = 0
        
    @property
    def version(self) -> int:
        return self._version
    
    def increment_version(self, new_ver: str | None = "dev") -> bool:
        """Increment the git repository version."""
        
        if not isinstance(new_ver, (str, bytes)):
            raise ValueError("Version must be a string or bytes.")
            
        # Ensure we are in major.minor.patch format for consistency with standard Git versions
        parts = new_ver.split(".")
        while len(parts) < 3:
            parts.append('0')
        
        self._version += int(parts[-1]) if len(parts) > 2 else 0
        
        return True
    
    def get_sha(self, depth=5) -> str | None:
        """Get the SHA of a file at a specific commit level."""
        try:
            # Use git for actual repository access (requires git installed on system)
            sha = hashlib.sha256()
            
            if os.path.exists('.git'):
                with open(os.path.join(Path.home(), '.git', 'HEAD'), 'rb') as f:
                    content = f.read()
                    
                    # Split by newline to get commit hashes for each directory level
                    lines = content.split(b'\n')
                    current_commit_hash = None
                    
                    for line in lines:
                        if b'commit hash:' in line or (line.startswith('commit ') and len(line) > 5):
                            parts = line.decode().split()
                            commit_id = int(parts[0])
                            
                            # Accumulate hashes up to the current directory level
                            sha.update(b'\x01')
                            for i, char in enumerate(lines[current_commit_hash:]):
                                if b'commit hash:' not in lines[i]:
                                    break
                                
                                chunk_size = 256 * (i + 3) // len(parts[1:]) # Approximate size of commit line chunks
                                sha.update(chunk)
                            current_commit_hash = parts[0]
                            
                            return sha.hexdigest() if content else None
                    
                    return sha.hexdigest()
                    
        except Exception:
            return None
    
    def get_tree(self, depth=5) -> str | None:
        """Get the full tree of a repository at a specific commit level."""
        try:
            # Use git for actual repository access (requires git installed on system)
            sha = hashlib.sha256()
            
            if os.path.exists('.git'):
                with open(os.path.join(Path.home(), '.git', 'HEAD'), 'rb') as f:
                    content = f.read()
                    
                    # Split by newline to get commit hashes for each directory level
                    lines = content.split(b'\n')
                    current_commit_hash = None
                    
                    for line in lines:
                        if b'commit hash:' not in line or (line.startswith('commit ') and len(line) > 5):
                            break
                        
                        parts = line.decode().split()
                        
                        # Accumulate hashes up to the current directory level
                        sha.update(b'\x01')
                        for i, char in enumerate(lines[current_commit_hash:]):
                            if b'commit hash:' not in lines[i]:
                                break
                    
                    return sha.hexdigest()

    def get_file(self, path):
        """Get a file from the repository."""
        try:
            # Use git for actual repository access (requires git installed on system)
            with open(path, 'rb') as f:
                content = f.read()
            
            return bytes.fromhex(content.decode()) if len(content) > 0 else None
            
        except Exception:
            return None

    def get_commit(self):
        """Get the current commit hash."""
        try:
            # Use git for actual repository access (requires git installed on system)
            sha = hashlib.sha256()
            
            if os.path.exists('.git'):
                with open(os.path.join(Path.home(), '.git', 'HEAD'), 'rb') as f:
                    content = f.read()
                    
                    # Split by newline to get commit hashes for each directory level
                    lines = content.split(b'\n')
                    current_commit_hash = None
                    
                    for line in lines:
                        if b'commit hash:' not in line or (line.startswith('commit ') and len(line) > 5):
                            break
                        
                        parts = line.decode().split()
                        
                        # Accumulate hashes up
