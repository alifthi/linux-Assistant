from graph.graph import build_graph
from langchain_core.messages import  HumanMessage
from utils.dicts import AgentState

app = build_graph()
state: AgentState = {"messages": []}
while True:  
  input_text = input('Chat with AI: ')
  state['messages'].append(HumanMessage(content = input_text))
  if input_text == 'exit':
    break
  state = app.invoke(state)