from langchain_ollama import OllamaLLM
from linux_assistant.models.config import MODEL_NAME, SYSTEM_PROMPT, SHOW_THINKS
from langchain_core.messages import SystemMessage, AIMessage
from linux_assistant.utils.dicts import AgentState
from rich.progress import Progress, SpinnerColumn, TextColumn

class model_nodes:
    def __init__(self):
        self.model = self.build_model(MODEL_NAME)
    def call_model(self, state: AgentState) -> AgentState:
        ''' A node to call model '''
        if len(state['messages']) == 1:
            system_message = SystemMessage(content=SYSTEM_PROMPT)
            state['messages'] = [system_message] + state['messages'] 
        stream = self.model.stream(state['messages'])
        is_think_generated = False
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=not SHOW_THINKS,) as prog:
            task = prog.add_task("Thinking...", total=None)
            response_content = ""
            for chunk in stream:
                response_content += chunk
                if SHOW_THINKS:
                    prog.update(task, description=response_content, end = '', flush = True)
                if chunk == '</think>':
                    is_think_generated = True
                    break
        tmp = True
        dont_show = False
        for chunk in stream:                
            response_content += chunk
            if (is_think_generated and chunk == 'shell') or dont_show:
                dont_show = True
                continue
            if tmp:
                if chunk == '\n\n': 
                    continue
                tmp = False
                state['logger'].print_text(' ➜ ', color = 'yellow')
            state['logger'].print_text(chunk, color='white') 
        print('\n')
        state['messages'].append(AIMessage(content = response_content))
        return state
    @staticmethod
    def build_model(model_name: str):
        ''' A function to define the LM '''
        return  OllamaLLM(model = model_name)