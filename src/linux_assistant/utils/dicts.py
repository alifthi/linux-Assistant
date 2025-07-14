from typing import TypedDict,  Sequence
from langchain_core.messages import BaseMessage    
    
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    code: str 
    stdout: str
    stderr: str
    exit_code: int