from langchain_ollama import OllamaLLM
from models.config import MODEL_NAME, SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, AIMessage
from utils.dicts import AgentState

def build_model(model_name: str):
    ''' A function to define the LM '''
    return  OllamaLLM(model = model_name)

def call_model(state: AgentState) -> AgentState:
    ''' A node to call model '''
    system_message = SystemMessage(content=SYSTEM_PROMPT)
    response = model.invoke([system_message]+state['messages'])
    state['messages'].append(response)
    return state