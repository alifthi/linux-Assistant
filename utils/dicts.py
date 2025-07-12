from typing import TypedDict,  Sequence
from langchain_core.messages import BaseMessage

class ShellRunnerInput(TypedDict):
    code: str     
    
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    
class ShellRunnerOutput(TypedDict):
    stdout: str
    stderr: str
    exit_code: int