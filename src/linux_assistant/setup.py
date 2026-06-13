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


def detect_cuda_version():
    try:
        result = subprocess.run(
            ["nvcc", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "release" in line:
                    import re
                    match = re.search(r"release (\d+)\.(\d+)", line)
                    if match:
                        major, minor = match.group(1), match.group(2)
                        return f"cu{major}{minor}"
    except FileNotFoundError:
        print("nvcc not found, trying nvidia-smi for CUDA version...")

    try:
        result = subprocess.run(
            ["nvidia-smi"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            import re
            match = re.search(r"CUDA Version: (\d+)\.(\d+)", result.stdout)
            if match:
                major, minor = match.group(1), match.group(2)
                return f"cu{major}{minor}"
    except FileNotFoundError:
        print("nvidia-smi not found, unable to detect CUDA version.")

    return None


def install_llama_cpp(cuda=False):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    if cuda:
        print("Installing CUDA version of llama-cpp-python...")
        import os
        env = os.environ.copy()
        cuda_version = detect_cuda_version()
        if cuda_version is None:
            raise RuntimeError("Could not detect CUDA version. Ensure nvcc or nvidia-smi is available.")
        print(f"Detected CUDA version: {cuda_version}")
        subprocess.check_call(
            [sys.executable, 
             "-m",
             "pip",
             "install",
             "--only-binary=:all:",
             "llama-cpp-python",
             "--extra-index-url",f"https://abetlen.github.io/llama-cpp-python/whl/{cuda_version}"],
            env=env
        )
    else:
        print("Installing CPU version of llama-cpp-python...")
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "--only-binary=:all:",
            "llama-cpp-python",
            "--extra-index-url",
            "https://abetlen.github.io/llama-cpp-python/whl/cpu"
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