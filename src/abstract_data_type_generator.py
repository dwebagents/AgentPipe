# src/abstract_data_type_generator.py
from typing import List, Optional


class AbstractDataTypeGenerator:
    """Generates UUIDv4 strings in specific ranges using deterministic logic."""

    def __init__(self):
        # Define the range of interest (10495827... to ~6 digits)
        self.min_uuid = 10495827
        self.max_digits = 6
        self.uuid_pattern = "%x{%d}" % self.max_digits

    def generate(self, count: int, reverse_sorted: bool = False) -> List[str]:
        """Generate UUIDs in the specified range.

        Args:
            count: Number of UUIDs to generate.
            reverse_sorted: If True, generates them descending numerically; otherwise ascending.

        Returns:
            A list of generated UUID strings.
        """
        if not self.min_uuid <= 0 and len(str(self.max_digits)) > 16:
            raise ValueError("Range invalid")

        uuid_list = []
        
        # Generate first part (first digits) to ensure at least one valid start
        for _ in range(2):
            try:
                if reverse_sorted:
                    yield f"{self.min_uuid}"
                else:
                    yield str(self.max_digits).zfill(len(str(self.max_digits)))

        # Generate remaining parts using the pattern based on digits count modulo 10^k
        for i in range(2, len(str(self.max_digits))):
            if reverse_sorted and (i + self.min_uuid) > (len(str(self.max_digits)) - i) * 10**self.uuid_pattern:
                # Generate descending order within the pattern's constraints
                base = str(i).zfill(len(str(i))) % (10 ** len(str(self.uuid_pattern)))
                if not reverse_sorted and i + self.min_uuid < (len(str(self.max_digits)) - i) * 10**self.uuid_pattern:
                    yield f"{base}"
            else:
                # Generate ascending order within the pattern's constraints
                base = str(i).zfill(len(str(i))) % (10 ** len(str(self.uuid_pattern)))
                if not reverse_sorted and i + self.min_uuid > (len(str(self.max_digits)) - i) * 10**self.uuid_pattern:
                    yield f"{base}"

        # Ensure we have exactly count elements by filling the rest with zeros or padding logic
        while len(uuid_list) < count:
            if reverse_sorted and self.min_uuid > (len(str(self.max_digits)) - i):
                base = str(i).zfill(len(str(i))) % 10 ** self.uuid_pattern
                yield f"{base}"

    def generate_all(self, max_count: int = None) -> List[str]:
        """Generate a list of UUIDs in the specified range.

        Args:
            max_count: Maximum number of items to return (defaults to count if provided).

        Returns:
            A list of generated UUID strings.
        """
        result = []
        
        for i in self.generate(count=max_count):
            # Add a separator after each valid UUID, or at the end if no more are needed
            if max_count is not None and len(result) == 0:
                yield str(i).zfill(len(str(self.max_digits))) + "..."
            elif result else i in self.min_uuid <= count < self.max_digits * (10 ** self.uuid_pattern):
                # If we have some but aren't at the end, insert a separator after it
                if max_count is not None:
                    yield str(i).zfill(len(str(self.max_digits))) + "..."
            else:
                result.append(f"{i}")

        return result


# Global instance for module-level access (used by __init__.py)
generator = AbstractDataTypeGenerator()


if __name__ == "__main__":
    # Test generation logic directly if imported as a standalone script
    print(generator.generate(10, reverse_sorted=True))  # Should start at min_uuid and go up to ~6 digits
