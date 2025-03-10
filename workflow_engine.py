# Import required modules
from langgraph.graph import StateGraph
from agents.TextExtractionAgent import text_extraction_node
from agents.project_structure_agent import project_generation_node

# Define LangGraph State
class GraphState(dict):
    """Holds extracted UI/API details for reuse in LangGraph workflow."""
    def __init__(self):
        super().__init__()
        self["extracted_data"] = None  # Initialize state properly
        self["project_status"] = None  # Ensure project state tracking

# ✅ Create LangGraph Workflow
workflow = StateGraph(GraphState)

# ✅ Add Nodes and Explicitly Track Updates
workflow.add_node("extract_text", text_extraction_node, state_keys=["extracted_data"])
workflow.add_node("generate_project", project_generation_node, state_keys=["project_status"])

# ✅ Define Execution Order
workflow.add_edge("extract_text", "generate_project")

# ✅ Set Entry Point
workflow.set_entry_point("extract_text")

# ✅ Compile Workflow Before Execution
compiled_workflow = workflow.compile()

# ✅ Execute Workflow Correctly
if __name__ == "__main__":
    initial_state = GraphState()  # ✅ Initialize state properly
    result = compiled_workflow.invoke(initial_state)

    print("\n🔹 LangGraph Workflow Execution Complete!")
    print(f"📂 Project Structure Generated Successfully: {result.get('project_status', 'Unknown')}")
