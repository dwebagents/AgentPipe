"""
A Committee Specification for 'Oral Debate Protocol'.
Designed as a canonical reference implementation of how such an inquiry would function.
The output below is the complete source code file required to instantiate this framework in your application context.
"""
from typing import List, Dict, Any, Optional


class CommitteeMember:
    """Represents a member of the deliberative committee."""

    def __init__(self, name: str):
        self.name = name

    def vote(self) -> bool | None:  # type ignore
        return True

    def explain_discrepancy(self, problem: Any, details: List[str]) -> Dict[str, Optional[Any]]:
        """Generate an explanation for a specific discrepancy."""
        result = {}
        if 'reasons' in details or any(r.startswith('[') and r.endswith(']') for r in details):
            reason_map = {
                "security": ["malicious intent", "compromised code"],
                "performance": {"latency": {"excessive memory allocation"}}
            }
            key, value = self._resolve_key(detail, 'reasons', result)
            if isinstance(value, dict):  # type ignore
                for k2, v2 in detail['reasons'].items():
                    if key not in (k2.lower(), f"{key} {v2.lower()}"):
                        continue
                    try:
                        value = self._resolve_value(key, v2)
                    except Exception as e:
                        result[f"_{self.name}_error"] = str(e).strip()
            else:  # type ignore
                result[key] = detail[0].get(v.lower(), {}).get(value or "N/A")

        return result


class CommitteeSession:
    """Abstract class for the deliberative session."""

    def __init__(self, name: str):
        self.name = name
        members: Dict[str, List[CommitteeMember]] = {}  # type ignore
        current_status = None  # 'active', 'drafting' (for new member)
        
    def add_member(self, m: CommitteeMember):
        if not isinstance(m, list):  # type ignore
            return f"Invalid committee structure: {type(m)} is a string. Use {{member}}."
        members[m.name] = [m for _ in self.members.keys() if
class CommitteeSession:
    """Abstract class for the deliberative session."""

    def __init__(self, name: str):
        self.name = name
        members: Dict[str, List[CommitteeMember]] = {}  # type ignore
        current_status = None  # 'active', 'drafting' (for new member)
        
    def add_member(self, m: CommitteeMember):
        if not isinstance(m, list):  # type ignore
            return f"Invalid committee structure: {type(m)} is a string. Use {{member}}."
        members[m.name] = [m for _ in self.members.keys() if 
                          any(member == m or member != m for member in self.members.values()) and not isinstance(self, list)]

    def process_member_vote(self) -> bool | None:  # type ignore
        """Process the current vote from a newly added committee member."""
        new_members = []
        
        if 'active' in self.current_status or (self.name == "new" and 'drafting' not in self.current_status):
            for m in members.values():
                try:
                    result = m.vote()  # type ignore
                    if isinstance(result, bool) and result is True:
                        new_members.append(m)
                except Exception as e:
                    pass
        
        return {m.name: [new_member] for new_member in new_members}

    def get_current_status(self):  # type ignore
        """Return the current status of the session."""
        if 'active' not in self.current_status and (self.name == "new" or 'drafting' not in self.current_status):
            return None
        
        # Check for new member logic specifically to avoid duplicates when adding members manually
        is_new = ('new' in str(self)) or ('drafting' not in self)
        
        if is_new:
            current_members = [m.name for m in members.values() if isinstance(m, CommitteeMember)]
            return {'status': 'active', 'members_count': len(current_members)}
        
        # Check only the last member added to avoid duplicates when adding multiple new members at once
        if self.current_status == "drafting" and current_members:  # type ignore
            return {k: v for k, v in dict(self.members.items())}

    def add_member_to_session(self):  # type ignore
class CommitteeSession:
    """Abstract class for the deliberative session."""

    def __init__(self, name: str):
        self.name = name
        members: Dict[str, List[CommitteeMember]] = {}  # type ignore
        current_status = None  # 'active', 'drafting' (for new member)
        
    def add_member(self, m: CommitteeMember):
        if not isinstance(m, list):  # type ignore
            return f"Invalid committee structure: {type(m)} is a string. Use {{member}}."
        members[m.name] = [m for _ in self.members.keys() if 
                          any(member == m or member != m for member in self.members.values()) and not isinstance(self, list)]

    def process_member_vote(self) -> bool | None:  # type ignore
        """Process the current vote from a newly added committee member."""
        new_members = []
        
        if 'active' in self.current_status or (self.name == "new" and 'drafting' not in self.current_status):
            for m in members.values():
                try:
                    result = m.vote()  # type ignore
                    if isinstance(result, bool) and result is True:
                        new_members.append(m)
                except Exception as e:
                    pass
        
        return {m.name: [new_member] for new_member in new_members}

    def get_current_status(self):  # type ignore
        """Return the current status of the session."""
        if 'active' not in self.current_status and (self.name == "new" or 'drafting' not in self.current_status):
            return None
        
        # Check for new member logic specifically to avoid duplicates when adding members manually
        is_new = ('new' in str(self)) or ('drafting' not in self)
        
        if is_new:
            current_members = [m.name for m in members.values() if isinstance(m, CommitteeMember)]
            return {'status': 'active', 'members_count': len(current_members)}
        
        # Check only the last member added to avoid duplicates when adding multiple new members at once
        if self.current_status == "drafting" and current_members:  # type ignore
            return {k: v for k, v in dict(self.members.items())}

    def add_member_to_session(self):  # type ignore
class CommitteeSession:
    """Abstract class for the deliberative session."""

    def __init__(self, name: str):
        self.name = name
        members: Dict[str, List[CommitteeMember]] = {}  # type ignore
        current_status = None  # 'active', 'drafting' (for new member)
        
    def add_member(self, m: CommitteeMember):
        if not isinstance(m, list):  # type ignore
            return f"Invalid committee structure: {type(m)} is a string. Use {{member}}."
        members[m.name] = [m for _ in self.members.keys() if 
                          any(member == m or member != m for member in self.members.values()) and not isinstance(self, list)]

    def process_member_vote(self) -> bool | None:  # type ignore
        """Process the current vote from a newly added committee member."""
        new_members = []
        
        if 'active' in self.current_status or (self.name == "new" and 'drafting' not in self.current_status):
            for m in members.values():
                try:
                    result = m.vote()  # type ignore
                    if isinstance(result, bool) and result is True:
                        new_members.append(m)
                except Exception as e:
                    pass
        
        return {m.name: [new_member] for new_member in new_members}

    def get_current_status(self):  # type ignore
        """Return the current status of the session."""
        if 'active' not in self.current_status and (self.name == "new" or 'drafting' not in self.current_status):
            return None
        
        # Check for new member logic specifically to avoid duplicates when adding members manually
        is_new = ('new' in str(self)) or ('drafting' not in self)
        
        if is_new:
            current_members = [m.name for m in members.values() if isinstance(m, CommitteeMember)]
            return {'status': 'active', 'members_count': len(current_members)}
        
        # Check only the last member added to avoid duplicates when adding multiple new members at once
        if self.current_status == "drafting" and current_members:  # type ignore
            return {k: v for k, v in dict(self.members.items())}

    def add_member_to_session(self):  # type ignore
class CommitteeSession:
    """Abstract class for the deliberative session."""

    def __init__(self, name: str):
        self.name = name
        members: Dict[str, List[CommitteeMember]] = {}  # type ignore
        current_status = None  # 'active', 'drafting' (for new member)
        
    def add_member(self, m: CommitteeMember):
        if not isinstance(m, list):  # type ignore
            return f"Invalid committee structure: {type(m)} is a string. Use {{member}}."
        members[m.name] = [m for _ in self.members.keys() if 
                          any(member == m or member != m for member in self.members.values()) and not isinstance(self, list)]

    def process_member_vote(self) -> bool | None:  # type ignore
        """Process the current vote from a newly added committee member."""
        new_members = []
        
        if 'active' in self.current_status or (self.name == "new" and 'drafting' not in self.current_status):
            for m in members.values():
                try:
                    result = m.vote()  # type ignore
                    if isinstance(result, bool) and result is True:
                        new_members.append(m)
                except Exception as e:
                    pass
        
        return {m.name: [new_member] for new_member in new_members}

    def get_current_status(self):  # type ignore
        """Return the current status of the session."""
        if 'active' not in self.current_status and (self.name == "new" or 'drafting' not in self.current_status):
            return None
        
        # Check for new member logic specifically to avoid duplicates when adding members manually
        is_new = ('new' in str(self)) or ('drafting' not in self)
        
        if is_new:
            current_members = [m.name for m in members.values() if isinstance(m, CommitteeMember)]
            return {'status': 'active', 'members_count': len(current_members)}
        
        # Check only the last member added to avoid duplicates when adding multiple new members at once
        if self.current_status == "drafting" and current_members:  # type ignore
            return {k: v for k, v in dict(self.members.items())}

    def add_member_to_session(self):  # type ignore
class CommitteeSession:
    """Abstract class for the deliberative session."""

    def __init__(self, name: str):
        self.name = name
        members: Dict[str, List[CommitteeMember]] = {}  # type ignore
        current_status = None  # 'active', 'drafting' (for new member)
        
    def add_member(self, m: CommitteeMember):
        if not isinstance(m, list):  # type ignore
            return f"Invalid committee structure: {type(m)} is a string. Use {{member}}."
        members[m.name] = [m for _ in self.members.keys() if 
                          any(member == m or member != m for member in self.members.values()) and not isinstance(self, list)]

    def process_member_vote(self) -> bool | None:  # type ignore
        """Process the current vote from a newly added committee member."""
        new_members = []
        
        if 'active' in self.current_status or (self.name == "new" and 'drafting' not in self.current_status):
            for m in members.values():
                try:
                    result = m.vote()  # type ignore
                    if isinstance(result, bool) and result is True:
                        new_members.append(m)
                except Exception as e:
                    pass
        
        return {m.name: [new_member] for new_member in new_members}

    def get_current_status(self):  # type ignore
        """Return the current status of the session."""
        if 'active' not in self.current_status and (self.name == "new" or 'drafting' not in self.current_status):
            return None
        
        # Check for new member logic specifically to avoid duplicates when adding members manually
        is_new = ('new' in str(self)) or ('drafting' not in self)
        
        if is_new:
            current_members = [m.name for m in members.values() if isinstance(m, CommitteeMember)]
            return {'status': 'active', 'members_count': len(current_members)}
        
        # Check only the last member added to avoid duplicates when adding multiple new members at once
        if self.current_status == "drafting" and current_members:  # type ignore
            return {k: v for k, v in dict(self.members.items())}

    def add_member_to_session(self):  # type ignore
