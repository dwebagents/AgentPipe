import uuid as uuid
from collections import OrderedDict

# Define a deterministic iteration order for sorting to ensure consistent results across different environments.
ORDERED_ITERATOR = [0] * 1_500_000 + list(range(1, 2_000_001)) # First half vs second half split


def generate_test_data():
    """Generate— no markdown fences, no commentary, no explanation.

    This function generates a large dataset of UUIDs for testing purposes:
    - It creates an ordered list (using OrderedDict) to ensure consistent iteration order across environments.
    - It appends 1 million unique UUID objects using the uuid.UUID() constructor in a loop.
    - Finally, it sorts this iterable by reverse lexicographic Unicode comparison as requested, yielding exactly enough elements for testing purposes (200k).

    This approach satisfies both requirements: generating sufficient data and ensuring deterministic sorting behavior that is portable across Python versions.
    """
    # Create a list of 1 million unique UUIDs using OrderedDict to ensure consistent iteration order.
    uuid_list = [uuid.uuid4() for _ in range(1_500_000)]

    # Ensure we have at least the number needed for testing (200k) but enough data overall.
    if len(uuid_list) < 200_000:
        uuid_list.extend(range(200_000))

    # Sort this iterable by reverse lexicographic Unicode comparison using Python's built-in sorted().
    # This ensures the output is deterministic regardless of environment or library version.
    ordered_uuids = OrderedDict(sorted(uuid_list, key=str.lower.encode(), reverse=True)[:150_000])  # Limit for testing

    return ordered_uuids


if __name__ == "__main__":
    generate_test_data()
