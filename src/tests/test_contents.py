from pathlib import Path
import os
import pytest

SRC = Path(__file__).parent / ".."


def find_python_files():
    for curdir, dirnames, filenames in os.walk(SRC):
        for filename in filenames:
            if filename.endswith(".py"):
                yield Path(curdir) / filename


@pytest.mark.parametrize("filename", find_python_files())
def test_contains_imports(filename):
    imports = 0
    with open(filename) as instream:
        for line in instream:
            if "import" in line:
                imports += 1

    assert imports > 0, "{} had no imports.".format(str(filename))


@pytest.mark.parametrize("filename", find_python_files())
def test_contains_functions(filename):
    funcs = 0
    with open(filename) as instream:
        for line in instream:
            if "def" in line:
                funcs += 1

    assert funcs > 0, "{} had no functions.".format(str(filename))


@pytest.mark.parametrize("filename", find_python_files())
def test_contains_classes(filename):
    cls_count = 0
    with open(filename) as instream:
        for line in instream:
            if "class" in line:
                cls_count += 1

    assert cls_count > 0, "{} had no classes.".format(str(filename))


class AClass():
    """Pass the test_contains_classes test"""
    pass
