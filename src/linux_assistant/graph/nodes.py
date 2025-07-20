from linux_assistant.graph.config import MAX_SEARCH_RESULTS, WIKIPEDIA_RESULTS
from langchain_core.messages import ToolMessage
from linux_assistant.utils.dicts import AgentState
from rich.progress import Progress, SpinnerColumn, TextColumn
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from ddgs import DDGS
import tempfile
import os
import subprocess
import time
import gc
import warnings
warnings.filterwarnings("ignore", message="This package .* has been renamed to `ddgs`!", category=RuntimeWarning)


def shell_node( state: AgentState)->  AgentState:
    '''To run a shell code that generated with AI'''
    state['logger'].print_text("🔧 Running shell command ...", color='blue', end='\n')
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
    return state
class search_tools:
    def __init__(self):
        wiki_api = WikipediaAPIWrapper(
                        top_k_results=WIKIPEDIA_RESULTS,   
                        lang="en",         
                        doc_content_chars_max=2000
                    )
        self.wiki_tool = WikipediaQueryRun(
                api_wrapper=wiki_api,
                description="Search Wikipedia for general knowledge",
                verbose=False
            )
    def search_in_wiki(self, query):
        answer = self.wiki_tool.run(query)
        return answer
    @staticmethod
    def search_duckduckgo(query):
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results = MAX_SEARCH_RESULTS)
        return results
    def search_node(self, state: AgentState)-> AgentState:
        '''A node for search'''
        state['logger'].print_text("🔍 Searching ...", color='blue', end='\n')
        print("\n")
        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,) as prog:
            task = prog.add_task("Searching...", total=None)
            t = time.perf_counter()
            wiki_search_res = self.search_in_wiki(state['search_query'])
            ddg_res = self.search_duckduckgo(state['search_query'])
            interval = time.perf_counter() - t
        state['messages'].append(ToolMessage(content=wiki_search_res, tool_call_id = f'search_result_{0}'))
        for i, res in enumerate(ddg_res):
            state['messages'].append(ToolMessage(content=res['body'], tool_call_id = f'search_result_{i+1}'))
        if len(ddg_res) == 0:
            state['logger'].print_text("❌ No result found ", color='red')
        else:
            state['logger'].print_text(f"🔍 Search is completed in {interval}s, {len(ddg_res)} results found", color='green')
        print('\n')
        gc.collect()
        return state