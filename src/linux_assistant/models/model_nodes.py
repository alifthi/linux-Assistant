from langchain_ollama import OllamaLLM
from linux_assistant.models.config import MODEL_NAME, SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, AIMessage
from linux_assistant.utils.dicts import AgentState


class model_nodes:
    def __init__(self):
        self.model = self.build_model(MODEL_NAME)
    def call_model(self, state: AgentState) -> AgentState:
        ''' A node to call model '''
        if len(state['messages']) == 1:
            system_message = SystemMessage(content=SYSTEM_PROMPT)
            state['messages'] = [system_message] + state['messages'] 
        stream = self.model.stream(state['messages'])
        response_content = ""
        for chunk in stream:
            response_content += chunk
            print(chunk, end='', flush=True) 
        print('\n')
        state['messages'].append(AIMessage(content = response_content))
        return state
    @staticmethod
    def build_model(model_name: str):
        ''' A function to define the LM '''
        return  OllamaLLM(model = model_name)