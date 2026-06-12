# linux‑Assistant

An AI-powered assistant that lets you interact with your Linux system using natural language. Ask it to list files, install packages, inspect processes, or perform any shell task—behind the scenes it translates your request into safe bash commands and runs them for you.

---

## Features

- **Natural‑language interface**: Describe what you want to do—no need to remember exact commands.  
- **Interactive shell execution**: The assistant decides when to run commands, executes them in a temporary script, and returns the output.  
- **Continuous conversation**: You can follow up on results, ask for clarifications, or chain multiple operations in one session.  
- **Customizable**: Swap in any llama.cpp model and adjust prompts to suit your workflow.

---

## Prerequisites

- **Linux**
- **Python 3.12+**   
- (Optional but recommended) A dedicated Python virtual environment

---

## Configuration

Open **`models/config.py`** and adjust:

- `GENERATION_MODEL` – the GGUF model you wish to use.
- `REPO_ID` – The hf repository you want to model beeing download from.
- `SYSTEM_PROMPT` – how the assistant should frame its replies and decide when to run shell commands.

---
## Installation

* Install via pip

```bash
$ pip install linux-assistant
```

* Build from source

```bash
$ git clone https://github.com/alifthi/linux-Assistant.git
$ cd linux-Assistant
$ pip install -e .
```
---
## Usage

Run the assistant and start chatting:

```bash
$ linux-assistant
```

- If inference enginee is not installed, you need to run `linux-assistant setup` to install inference enginee.

- Ask anything you would normally do in the terminal.

- Continue the conversation naturally or type `exit` to quit.
---
Run the assistant using Docker

```bash
docker run --name <Container's name> \
   -v linux_assistant_volume:/app/data \
   -v "$(pwd)":/app/workspace alifthi/linux-assistant 

```

---

## Contributing

Contributions and feedback are welcome! Feel free to:

- Open issues for bugs or feature requests  
- Submit pull requests to improve prompts, handling, or documentation  
- Suggest new use cases or integrations

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.  
