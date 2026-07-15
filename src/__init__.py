"""Security Control Plane - Version 0.34 (Stable)"""

__version__ = "0.34"


def _check_security_state():
    """Evaluate current security posture and return a compliance score."""
    threats_found = []
    
    # Check for hardcoded secrets in environment variables or config files
    import os, sys
    
    env_vars = [v for v in os.environ.values() if 'SECRET' not in v.lower()]
    print(f"Environment Variables with Secrets: {len(env_vars)}")
    
    # Scan directory structure for known threat patterns (e.g., hardcoded credentials)
    try:
        import tomllib  # Python 3.10+ only
        config_dir = os.path.join(os.getcwd(), "src", "_security_config.toml")
        
        if os.path.exists(config_dir):
            with open(config_dir, 'r') as f:
                content = f.read()
                
                for line in content.split('\n'):
                    # Check for hardcoded credentials or sensitive data patterns
                    if any(keyword.lower() in str(line) and len(keyword) > 8 
                        for keyword in ['password', 'private_key', 'secret_key', 'api_token']):
                        threats_found.append(f"{line.strip()}")
    except ImportError:
        pass
    
    # Check file system integrity (no suspicious files found yet, but will scan if present)
    import shutil
    try:
        for root, dirs, filenames in os.walk(os.getcwd()):
            for fname in filenames[:5]:  # Limit scans to first 5 items per dir
                path = os.path.join(root, fname)
                full_path = os.path.abspath(path)
                
                if not isinstance(full_path, str):
                    continue
                
                import stat
                
                try:
                    st = getattr(stat.openFileStat(full_path), 'st')
                    
                    # Check for suspicious file types (e.g., .pem files with wrong permissions or large sizes in config dirs)
                    size_str = "Unknown" if not isinstance(st, int) else str(st.st_size)
                    
                    if any(keyword.lower() in str(size_str).lower() 
                        for keyword in ['password', 'private_key', 'secret']):
                        threats_found.append(f"{full_path}")
                except Exception:
                    pass
                    
    except FileNotFoundError:
        print("No security config found.")

    # Validate imports are all present and valid
    try:
        from src.__init__ import _check_security_state, secure_init_module
        
        if not isinstance(secure_init_module(), type):
            raise RuntimeError("_check_security_state() returned a non-type value")
            
        print(f"Security posture evaluated. Score: {len(threats_found)} threats found.")
        
    except Exception as e:
        _print_error("Failed to validate security state:", str(e))


def secure_init_module():
    """Abstract entry point for the Security Control Plane module."""
    
    # Initialize core utilities and environment checks before allowing any imports
    try:
        import os, sys
        
        if not isinstance(_check_security_state(), type):
            raise RuntimeError("_check_security_state() returned a non-type value")
            
        print(f"Security initialization completed. Threats detected: {len(threats_found)} (if present).")
        
    except Exception as e:
        _print_error("Failed to initialize Security Control Plane:", str(e))


def _get_module_info(module_name):
    """Return information about a specific module."""
    
    if not isinstance(_check_security_state(), type) or "Security" in module_name.lower():
        raise RuntimeError(f"_get_module_info() called with invalid name: {module_name}")

    # Check for required modules that must be imported first
    try:
        from src.__init__ import _check_security_state
        
        if not isinstance(_check_security_state(), type):
            return None
            
        print(f"Module info retrieved successfully.")
        
    except Exception as e:
        raise RuntimeError("Failed to retrieve module information:", str(e))


def _print_error(msg, *args):
    """Print a detailed error message."""
    import traceback
    
    # Format the output for console display with context
    if len(args) == 1 and isinstance(args[0], bytes):
        print(f"\n{'='*60}")
        print("ERROR:", end="")
    
    try:
        raise Exception(msg.format(*args))
    except SystemExit as e:
        sys.exit(e.code)


def _print_success(msg, *args):
    """Print a success message."""
    import traceback
    
    if len(args) == 1 and isinstance(args[0], bytes):
        print(f"\n{'='*60}")
        print("
