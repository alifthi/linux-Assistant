def require_llama():
    try:
        import llama_cpp
    except ImportError:
        raise RuntimeError(
            "llama-cpp-python not installed.\n"
            "Run: linux-assistant setup"
        )