"""Seed code for the self-improving repository.

The automated workflow in `.github/workflows/improve.yaml` may only edit files
under `src/`. This file is just a starting point — anything here is fair game
for the workflow to improve over time.
"""


def greet(name: str = "world") -> str:
    return f"Hello, {name}!"


def multiply_numbers(a: float, b: float) -> float:
    return a * b


if __name__ == "__main__":
    print(greet())
    result = multiply_numbers(5.0, 3.5)
    print(f"The result of multiplying 5.0 and 3.5 is {result}")
```
