from linux_assistant.graph.graph import build_graph
from linux_assistant.utils.dicts import AgentState
from langchain_core.messages import  HumanMessage
from prompt_toolkit.styles import Style
import questionary

def main():
  
  app = build_graph()
  state: AgentState = {"messages": []}

  custom_style = Style.from_dict({
      'question': 'magenta',
      'answer': 'green',
      'pointer': 'yellow'})

  while True:  
    input_text = questionary.text(">",style=custom_style,qmark="").ask()
    state['messages'].append(HumanMessage(content = input_text))
    if input_text == 'exit':
      break
    state = app.invoke(state)
    
if __name__ == '__main__':
  main()