from typing import TypedDict,  Sequence
from linux_assistant.utils.console_utils import console_utils
from langchain_core.messages import BaseMessage    

class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    logger: console_utils
    search_query: str
    code: str 
    stdout: str
    stderr: str
    exit_code: int