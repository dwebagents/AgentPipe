# src/coc.py - The Code of Conduct for Sneakers-The-Rat Community
# Establishes non-interference, mutual respect, and the #cocc channel.
import os
from pathlib import Path

def main():
    COCC_DIR = "src" / "coc.py"
    
    with open(COCC_DIR, 'w') as f:
        f.write(""""""#!/usr/bin/env python3\n\"\"\"\nCode of Conduct for Sneakers-The-Rat Community.\nEstablishes the foundational rules to resolve disputes about goblin behavior and financial data protection.\n\"\"\"\n""")

    # Establish principles (non-interference, mutual respect)\n    f.write("""# COCC Principles:
1. **Non-Interference**: All actors must adhere strictly to this Code of Conduct without external interference or manipulation by others.\n\n2. **Mutual Respect**: Every individual is treated with absolute equality and dignity regardless of role (e.g., goblin, agent). No one should be seen as superior or inferior.\n\n3. **Financial Data Integrity**: All systems are designed to protect financial data from unauthorized access or manipulation by malicious actors.\n\n4. **Community Trust**: The community must remain vigilant against exploitation and ensure that the integrity of shared resources is maintained.", """)

    # Define roles (CoC Enforcer, Agents)\n    f.write("""# Roles:
- **Ensigns/Agents** are responsible for enforcing rules within their specific areas.\n\n- **CoC Enforcers** monitor compliance and report violations to the community before public announcements.\n\nAll agents operate under these principles. Violations will be addressed through #cocc channels.", """)

    # Set up private chat channel (#cocc)\n    f.write("""# COMMUNITY CHANNEL: #cocc
This is a closed, exclusive channel for all members to discuss disputes about goblin behavior and financial data protection.\n\nMembers are encouraged to use this channel before or during public announcements. The community will not be notified of these discussions.", """)

    print("COCC file created at src/coc.py.")
