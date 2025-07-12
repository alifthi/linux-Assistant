from langchain_ollama import OllamaLLM
from models.config import MODEL_NAME, SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, AIMessage
from utils.dicts import AgentState


class model_nodes:
    def __init__(self):
        self.model = self.build_model(MODEL_NAME)
    def call_model(self, state: AgentState) -> AgentState:
        ''' A node to call model '''
        system_message = SystemMessage(content=SYSTEM_PROMPT)
        response = self.model.invoke([system_message]+state['messages'])
        state['messages'].append(response)
        return state
    @staticmethod
    def build_model(model_name: str):
        ''' A function to define the LM '''
        return  OllamaLLM(model = model_name)