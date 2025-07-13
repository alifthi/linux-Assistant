from graph.nodes import shell_node, prepare_shell_code,\
                        wants_shell, prepare_tool_prompt
from utils.dicts import AgentState
from models.model_nodes import model_nodes
from langgraph.graph import StateGraph, START,END

def build_graph() -> StateGraph:
    ''' This function builds graph '''
    call_model = model_nodes()
    graph = StateGraph(AgentState)
    graph.set_entry_point('call_model')
    graph.add_node('call_model', call_model.call_model)
    graph.add_node('prepare_tool_prompt', prepare_tool_prompt)
    graph.add_node('prepare_shell_code',prepare_shell_code)
    graph.add_node('shell_node', shell_node)
    graph.add_conditional_edges(
        "call_model",
        wants_shell,
        {True: 'prepare_shell_code', False: END}
    )
    graph.add_edge('prepare_shell_code', 'shell_node')
    graph.add_edge('shell_node', 'prepare_tool_prompt')
    graph.add_edge('prepare_tool_prompt','call_model')
    app = graph.compile()
    return app