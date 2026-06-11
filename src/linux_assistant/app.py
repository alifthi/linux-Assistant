from linux_assistant.graph.graph import build_graph
from linux_assistant.utils.dicts import AgentState
from linux_assistant.utils.console_utils import console_utils


def run_app():
    app = build_graph()
    console = console_utils()

    state: AgentState = {"messages": [], "logger": console}

    console.release_banner()

    while True:
        input_text = console.get_user_input()

        if input_text == "exit":
            break

        state["messages"].append({
            "role": "user",
            "content": input_text
        })

        state = app.invoke(state)