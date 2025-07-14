from linux_assistant.graph.graph import build_graph
from linux_assistant.utils.dicts import AgentState
from langchain_core.messages import  HumanMessage

def main():
  app = build_graph()
  state: AgentState = {"messages": []}
  while True:  
    input_text = input('Chat with AI: ')
    state['messages'].append(HumanMessage(content = input_text))
    if input_text == 'exit':
      break
    state = app.invoke(state)
    
if __name__ == '__main__':
  main()