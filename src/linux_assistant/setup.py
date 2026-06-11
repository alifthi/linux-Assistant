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
    if cuda:
        print("Installing CUDA version of llama-cpp-python...")
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "llama-cpp-python",
            "--extra-index-url",
            "https://abetlen.github.io/llama-cpp-python/whl/cu124"
        ])
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