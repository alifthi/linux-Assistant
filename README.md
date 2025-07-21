# linux‑Assistant

An AI-powered assistant that lets you interact with your Linux system using natural language. Ask it to list files, install packages, inspect processes, or perform any shell task—behind the scenes it translates your request into safe bash commands and runs them for you.

---

## Features

- **Natural‑language interface**: Describe what you want to do—no need to remember exact commands.  
- **Interactive shell execution**: The assistant decides when to run commands, executes them in a temporary script, and returns the output.  
- **Continuous conversation**: You can follow up on results, ask for clarifications, or chain multiple operations in one session.  
- **Customizable**: Swap in any Ollama‑compatible model and adjust prompts to suit your workflow.

---

## Prerequisites

- **Linux** with Bash installed  
- **Python 3.12+**  
- [Ollama CLI & daemon](https://ollama.com/) with at least one local model (e.g. `qwen3:8b`)  
- (Optional but recommended) A dedicated Python virtual environment

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/alifthi/linux-Assistant.git
   cd linux-Assistant
   ```

2. **Set up a virtual environment**  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Open **`models/config.py`** and adjust:

- `MODEL_NAME` – the Ollama model you wish to use (e.g. `"qwen3:8b"`).  
- `SYSTEM_PROMPT` – how the assistant should frame its replies and decide when to run shell commands.

---

## Usage

Run the assistant and start chatting:

```bash
cd src
python -m linux_assistant
```

- Ask anything you would normally do in the terminal.

- Continue the conversation naturally or type `exit` to quit.

---

## Contributing

Contributions and feedback are welcome! Feel free to:

- Open issues for bugs or feature requests  
- Submit pull requests to improve prompts, handling, or documentation  
- Suggest new use cases or integrations

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.  
