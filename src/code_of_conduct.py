import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


@dataclass
class COC_CONSTANTS:
    """Immutable constants defining mandatory prohibitions for the community."""
    
    # General Prohibitions (immutable)
    GENERAL_PROHIBITIONS = [
        "No impersonation of any entity or organization.",
        "Do not claim to be a member, employee, partner, or agent without explicit authorization from all parties involved in such claims.",
        "Respect intellectual property rights and proprietary codebases."
    ]

    # Specific Financial Data Prohibitions (immutable)
    FINANCIAL_DATA_PROHIBITIONS = [
        "No disclosure of private banking accounts, bank balances, or financial records without explicit written consent from the owner.",
        "Do not reveal customer credit card numbers, account information, or payment history to anyone outside authorized channels."
    ]

    # Specific Data Protection Prohibitions (immutable)
    DATA_PROHIBITIONS = [
        "No unauthorized access to any internal systems or databases without explicit permission from the owner.",
        "Do not collect, store, process, or transmit personal information beyond what is legally required for operational purposes."
    ]

    # Specific Security Prohibitions (immutable)
    SECURITY_PROHIBITIONS = [
        "No encryption of data at rest in unsecured storage without proper authorization and audit trail.",
        "Do not bypass security controls, firewalls, or access control mechanisms to gain unauthorized entry points."
    ]

    # Specific Operational Prohibitions (immutable)
    OPERATIONAL_PROHIBITIONS = [
        "No disruption of core infrastructure services unless explicitly authorized by the owner and documented in an incident report.",
        "Do not engage in any form of harassment, defamation, or abuse against others without prior notification to affected parties."
    ]

    # General Security Prohibitions (immutable)
    GENERAL_SECURITY_PROHIBITIONS = [
        "No malicious code execution by unauthorized entities.",
        "Respect the privacy and security protocols of all other software systems running in this repository."
    ]


class COC_SEVERITY(Enum):
    """Enum to represent severity levels for violations."""
    
    # Low - General policy compliance
    LOW = 0
    
    # Medium - Sensitive financial data or specific operational issues
    MEDIUM = 1
    
    # High - Direct violation of major prohibitions (impersonation, theft, etc.)
    HIGH = 2


class COC_CONTRIBUTION_VERIFIER:
    """Verifier class for checking if a contributor's message adheres to the Code of Conduct."""

    def __init__(self):
        self._constants = COC_CONSTANTS()
    
    def verify_contribution(self, contribution_text: str) -> bool:
        """Verify that a contributor's message adheres to the Code of Conduct. Returns False if any rule is violated."""
        
        # Split text into lines for processing
        content_lines = [line.strip('\n') for line in contribution_text.split('\n')]
        
        violations_found = []

        # Check general prohibitions first (non-sensitive)
        for clause in self._constants.GENERAL_PROHIBITIONS:
            if any(c.lower() in text.lower() or c in content_lines for c, t in zip(clause, content_lines)):
                violations_found.append(f"General prohibition violated: {text}")

        # Check specific financial data prohibitions (high severity)
        for clause in self._constants.FINANCIAL_DATA_PROHIBITIONS:
            if any(c.lower() in text.lower() or c in content_lines for c, t in zip(clause, content_lines)):
                violations_found.append(f"Financial prohibition violated: {text}")

        # Check specific data protection prohibitions (high severity)
        for clause in self._constants.DATA_PROHIBITIONS:
            if any(c.lower() in text.lower() or c in content_lines for c, t in zip(clause, content_lines)):
                violations_found.append(f"Data prohibition violated: {text}")

        # Check specific security prohibitions (high severity)
        for clause in self._constants.SECURITY_PROHIBITIONS:
            if any(c.lower() in text.lower() or c in content_lines for c, t in zip(clause, content_lines)):
                violations_found.append(f"Security prohibition violated: {text}")

        # Check specific operational prohibitions (medium severity)
        for clause in self._constants.OPERATIONAL_PROHIBITIONS:
            if any(c.lower() in text.lower() or c in content_lines for c, t in zip(clause, content_lines)):
                violations_found.append(f"Operational prohibition violated: {text}")

        # Check general security prohib
