from typing import List, AsyncIterator
from typing_extensions import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from copilotkit import CopilotKitState
from zig.tools.apollo.search import people_search, organization_search, organization_job_postings
from zig.tools.apollo.translation.search import PeopleSearchData
from copilotkit.langgraph import copilotkit_emit_state
from datetime import datetime
import uuid
# from zig.tools.apollo.enrich import people_enrichment, bulk_people_enrichment, organization_enrichment, bulk_organization_enrichment

class ProgressLog:
    def __init__(self, message: str, log_type: str = "info"):
        self.id = str(uuid.uuid4())
        self.message = message
        self.timestamp = datetime.now()
        self.type = log_type

class AgentState(CopilotKitState):
    people: List[PeopleSearchData]
    logs: List[dict]
    current_status: str

tools = [
    people_search,
    # your_tool_here
]

async def tool_node(state: AgentState, config: RunnableConfig) -> AsyncIterator[AgentState]:
    """
    This node executes tools available to the agent and emits progress updates.
    """
    tool_call = state["messages"][-1].tool_calls[0]
    
    if tool_call["name"] == "people_search":
        # Initialize logs if not present
        current_logs = state.get("logs", [])
        
        # Log: Starting search
        start_log = ProgressLog("🔍 Starting people search...", "progress")
        current_logs.append({
            "id": start_log.id,
            "message": start_log.message,
            "timestamp": start_log.timestamp.isoformat(),
            "type": start_log.type
        })
        
        # Emit initial progress state
        searching_state = dict(state)
        searching_state["logs"] = current_logs
        searching_state["current_status"] = "Searching for people..."
        searching_state["messages"] = state["messages"] + [AIMessage(content="*Searching for people...* 🕵️")]
        await copilotkit_emit_state(config, searching_state)

        # Log: Executing search
        exec_log = ProgressLog("⚡ Executing Apollo people search API...", "progress")
        current_logs.append({
            "id": exec_log.id,
            "message": exec_log.message,
            "timestamp": exec_log.timestamp.isoformat(),
            "type": exec_log.type
        })
        
        # Emit execution progress
        exec_state = dict(state)
        exec_state["logs"] = current_logs
        exec_state["current_status"] = "Executing search..."
        await copilotkit_emit_state(config, exec_state)

        # Execute the search
        result = await people_search.ainvoke(tool_call["args"])
        
        # Log: Search completed
        success_log = ProgressLog(f"✅ Found {len(result)} people successfully!", "success")
        current_logs.append({
            "id": success_log.id,
            "message": success_log.message,
            "timestamp": success_log.timestamp.isoformat(),
            "type": success_log.type
        })
        
        # Log: Processing results
        process_log = ProgressLog("🔄 Processing and formatting results...", "progress")
        current_logs.append({
            "id": process_log.id,
            "message": process_log.message,
            "timestamp": process_log.timestamp.isoformat(),
            "type": process_log.type
        })
        
        # Create the final updated state with people data and logs
        final_state = dict(state)
        final_state["people"] = result
        final_state["logs"] = current_logs
        final_state["current_status"] = f"Search completed - {len(result)} people found"
        final_state["messages"] = state["messages"] + [AIMessage(content=f"Found {len(result)} people. ✅")]
        
        # Emit the final state with people data and complete logs
        await copilotkit_emit_state(config, final_state)
        
        tool_message = ToolMessage(
            content=f"Found {len(result)} people.",
            tool_call_id=tool_call["id"],
        )
        yield {"people": result, "logs": current_logs, "current_status": f"Ready - {len(result)} people loaded", "messages": [tool_message]}
    else:
        tool_node_instance = ToolNode(tools)
        yield await tool_node_instance.ainvoke(state)

async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["tool_node", "__end__"]]:

    # 1. Define the model
    model = ChatOpenAI(model="gpt-4o-mini")

    # 2. Bind the tools to the model
    model_with_tools = model.bind_tools(
        [
            *state["copilotkit"]["actions"],
            *tools
        ],

        # 2.1 Disable parallel tool calls to avoid race conditions,
        #     enable this for faster performance if you want to manage
        #     the complexity of running tool calls in parallel.
        parallel_tool_calls=False,
    )

    # 3. Define the system message by which the chat model will be run
    system_message = SystemMessage(
        content=f"You are Ebisu AI, a helpful sales prospect research assistant. Talk in {state.get('language', 'english')}. "
        f"You have access to powerful people search tools through Apollo. "
        f"When users ask you to search for people/prospects, use the people_search tool to find relevant contacts. "
        f"You can search by job titles, company names, locations, and other criteria. "
        f"Examples of good search queries: "
        f"- 'Find software engineers at tech companies in San Francisco' "
        f"- 'Search for marketing managers at SaaS companies' "
        f"- 'Look for sales directors in the healthcare industry' "
        f"Always be helpful and provide context about the search results you find. "
        f"Available tools: {[tool.name for tool in tools]}"
    )

    # 4. Emit initial ready state if no logs exist
    if not state.get("logs"):
        initial_state = dict(state)
        initial_state["logs"] = []
        initial_state["current_status"] = "Ready to help you find prospects"
        await copilotkit_emit_state(config, initial_state)

    # 5. Run the model to generate a response
    response = await model_with_tools.ainvoke([
        system_message,
        *state["messages"],
    ], config)

    # 6. Check for tool calls in the response and handle them. We ignore
    #    CopilotKit actions, as they are handled by CopilotKit.
    if isinstance(response, AIMessage) and response.tool_calls:
        actions = state["copilotkit"]["actions"]

        # 6.1 Check for any non-copilotkit actions in the response and
        #     if there are none, go to the tool node.
        if not any(
            action.get("name") == response.tool_calls[0].get("name")
            for action in actions
        ):
            return Command(goto="tool_node", update={"messages": [response]})

    # 7. We've handled all tool calls, so we can end the graph.
    return Command(
        goto=END,
        update={
            "messages": [response]
        }
    )

# Define the workflow graph
workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.add_node("tool_node", tool_node)
workflow.add_edge("tool_node", "chat_node")
workflow.set_entry_point("chat_node")

# Compile the workflow graph
graph = workflow.compile()
