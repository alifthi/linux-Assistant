from langchain_core.messages import ToolMessage
from utils.dicts import AgentState
import tempfile
import os
import subprocess

def shell_node( state: AgentState)->  AgentState:
    '''To run a shell code that generated with AI'''
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as tf:
        tf.write(state['code'])
        path = tf.name
    
    proc = subprocess.run(
        ["bash", path],
        capture_output=True,
        text=True,
        timeout=30  
        )

    os.remove(path)
    state['stdout'], state['stderr'], state['exit_code'] = proc.stdout, proc.stderr, proc.returncode
    state['code']
    return state

def wants_shell(state: AgentState) -> AgentState:
    ''' To decide if shell needed '''
    last = state["messages"][-1].content.split('</think>')[-1]
    return True if 'shell_node' in last else False

def prepare_shell_code(state:AgentState) -> AgentState:
    ''' To extract generated code '''
    last = state["messages"][-1].content
    last = last.split('shell_node')[-1]
    last = last.split('```bash')[-1].split('```')[0]
    state['code'] = last
    return state

def prepare_tool_prompt( state: AgentState) -> AgentState:
    '''Prepare the output of executed command for LM'''
    content = (
        f"stdout:\n{state['stdout']}\n"
        f"stderr:\n{state['stderr']}\n"
        f"exit_code: {state['exit_code']}"
    )
    state['messages'].append(ToolMessage(content=content, tool_call_id="shell-1"))
    return state