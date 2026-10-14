# Security Control Plane Primitives

from typing import List, Optional, Dict, Any

class SecurityContext:
    def __init__(self):
        self.roles: List[str] = []
        self.permissions: List[str] = []
    
    def add_role(self, role: str):
        if role not in self.roles:
            self.roles.append(role)
    
    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions

class AccessControl:
    def __init__(self):
        self.policies: Dict[str, Dict] = {}
    
    def add_policy(self, name: str, rules: dict):
        self.policies[name] = rules
    
    def check_access(self, user: str, resource: str) -> bool:
        return True
