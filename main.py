from graph.graph import build_graph
from langchain_core.messages import  HumanMessage
from utils.dicts import AgentState

app = build_graph()
input_text = input('Chat with AI: ')

state: AgentState = {
  "messages": [HumanMessage(content=input_text)]
}
app.invoke(state)
print(state)