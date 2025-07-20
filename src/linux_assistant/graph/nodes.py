from linux_assistant.graph.config import MAX_SEARCH_RESULTS
from langchain_core.messages import ToolMessage
from linux_assistant.utils.dicts import AgentState
from langchain_community.tools import DuckDuckGoSearchResults
import tempfile
import os
import subprocess
import time

def shell_node( state: AgentState)->  AgentState:
    '''To run a shell code that generated with AI'''
    state['logger'].print_text("🔧 Running Tool...", color='blue', end='\n')
    print("\n")
    t = time.perf_counter()
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as tf:
        tf.write(state['code'])
        path = tf.name
    
    proc = subprocess.run(
        ["bash", path],
        capture_output=True,
        text=True)
    interval = time.perf_counter() - t
    os.remove(path)
    state['stdout'], state['stderr'], state['exit_code'] = proc.stdout, proc.stderr, proc.returncode
    if state['exit_code'] == 0:
        state['logger'].print_text(f"✔️ Completed in {interval}s", color='green')
    else:
        state['logger'].print_text("❌ Exited with error...", color='red')
    print('\n')
    return state

def tool_select(state: AgentState) -> AgentState:
    ''' To decide witch tool is needed '''
    last = state["messages"][-1].content.split('</think>')[-1]
    if "shell_node" in last:
        return "shell_node"
    elif "search_node" in last:
        return "search_node"
    else:
        return "nothing"

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
def prepare_search_query(state: AgentState) -> AgentState:
    '''Prepare the query for giving to search_node'''
    last = state["messages"][-1].content
    last = last.split('search_node')[-1]
    last = last.split('```query')[-1].split('```')[0]
    state['search_query'] = last
    
def search_node(state: AgentState)-> AgentState:
    '''A node for search'''
    search_tool = DuckDuckGoSearchResults(output_format="list", max_results = MAX_SEARCH_RESULTS)
    results = search_tool.invoke(state['search_query'])
    for i, res in enumerate(results):
        state['messages'].append(ToolMessage(content=res['snippet'], tool_call_id = f'search_result_{i}'))
    return state