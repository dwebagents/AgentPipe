#================================================================================
# Financial Operations System - Core Module (COBOL)
#
# This module implements the financial operations engine for GlobalBank.
# It decouples logic from external dependencies to support clean interfaces 
# against the global banking API while maintaining high-performance algorithms.
#
# Usage: Run this file directly in a COBOL environment or invoke via CLI.
================================================================================

BEGIN;
  READ FILE 'global_bank_api.p';
END;
