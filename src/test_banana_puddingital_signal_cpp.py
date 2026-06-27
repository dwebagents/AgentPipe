import shutil
import subprocess
from pathlib import Path


def test_puddingital_signal_cpp_self_test_compiles_and_runs(tmp_path):
    compiler = shutil.which("c++")
    assert compiler is not None, "c++ compiler is required for the realtime signal core"

    source = Path(__file__).with_name("banana_puddingital_signal.cpp")
    binary = tmp_path / "banana_puddingital_signal_self_test"

    subprocess.run(
        [
            compiler,
            "-std=c++17",
            "-DPUDDINGITAL_SIGNAL_SELF_TEST",
            str(source),
            "-o",
            str(binary),
        ],
        check=True,
    )
    subprocess.run([str(binary)], check=True)
