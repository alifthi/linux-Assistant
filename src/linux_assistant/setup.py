import platform
import subprocess
import sys


def detect_cuda():
    try:
        result = subprocess.run(
            ["nvidia-smi"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def install_llama_cpp(cuda=False):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    if cuda:
        print("Installing CUDA version of llama-cpp-python...")
        import os
        env = os.environ.copy()
        env["CMAKE_ARGS"] = "-DGGML_CUDA=on"
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "llama-cpp-python"],
            env=env
        )
    else:
        print("Installing CPU version of llama-cpp-python...")
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "llama-cpp-python"
        ])


def setup_cmd():
    print("Linux Assistant Setup\n")

    system = platform.system()
    print(f"Detected OS: {system}")

    cuda = detect_cuda()
    print(f"NVIDIA GPU detected: {cuda}")

    choice = None

    if cuda:
        print("\nSelect backend:")
        print("1) CUDA (recommended)")
        print("2) CPU only")

        choice = input("> ").strip()

        use_cuda = (choice == "1")
    else:
        print("No GPU detected → using CPU")
        use_cuda = False

    install_llama_cpp(cuda=use_cuda)

    print("\nSetup complete ✔")