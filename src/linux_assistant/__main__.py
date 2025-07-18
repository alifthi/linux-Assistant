from linux_assistant.graph.graph import build_graph
from linux_assistant.utils.dicts import AgentState
from langchain_core.messages import  HumanMessage
from linux_assistant.utils.console_utils import console_utils

def main():
  
  app = build_graph()
  state: AgentState = {"messages": []}
  console = console_utils()
  console.release_banner()
  while True:  
    input_text = console.get_user_input()
    state['messages'].append(HumanMessage(content = input_text))
    if input_text == 'exit':
      break
    state = app.invoke(state)
    
if __name__ == '__main__':
  main()