from langchain_core.messages import ToolMessage
from utils.dicts import ShellRunnerInput, ShellRunnerOutput, AgentState
import tempfile
import os
import subprocess

def shell_node(inp: ShellRunnerInput)-> ShellRunnerOutput:
    '''To run a shell code that generated with AI'''
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as tf:
        tf.write(inp['code'])
        path = tf.name
    
    proc = subprocess.run(
        ["bash", path],
        capture_output=True,
        text=True,
        timeout=30  
        )

    os.remove(path)
    return ShellRunnerOutput(
        stdout=proc.stdout,
        stderr=proc.stderr,
        exit_code=proc.returncode
        )

def wants_shell(state: AgentState) -> AgentState:
    ''' To decide if shell needed '''
    last = state["messages"][-1]
    return True if 'shell_node' in last else False

def prepare_shell_code(state:AgentState) -> ShellRunnerInput:
    ''' To extract generated code '''
    last = state["messages"][-1]
    last = last.split('shell_node')[-1]
    last = last.split('```bash')[-1].split('```')[0]
    shell_code = ShellRunnerInput(code=last)
    return shell_code

def prepare_tool_prompt(state: AgentState, output: ShellRunnerOutput) -> AgentState:
    content = (
        f"stdout:\n{output['stdout']}\n"
        f"stderr:\n{output['stderr']}\n"
        f"exit_code: {output['exit_code']}"
    )
    state['messages'].append(ToolMessage(content=content))
    return state