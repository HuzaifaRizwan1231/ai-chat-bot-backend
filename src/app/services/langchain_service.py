from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage
from utils.response_builder import ResponseBuilder
from utils.pycrypto import encrypt

workflow = None
app = None
currentModelName = None

# Config
config = {"configurable": {"thread_id": "abc123"}}

def getLangchainResponse(langchainModel, text, modelName):
    global workflow, app, currentModelName
    try:
        
        if modelName != currentModelName:
            workflow = None
            app = None
            
        def callModel(state: MessagesState):
            response = langchainModel.invoke(state["messages"])
            return {"messages": response}
    
        # Define the workflow
        if workflow is None:
            currentModelName = modelName
            workflow = StateGraph(state_schema=MessagesState)
            workflow.add_edge(START, "model")
            workflow.add_node("model", callModel)

            # Add memory
            memory = MemorySaver()
            
            if app is None:
                app = workflow.compile(checkpointer=memory)
        
        # Generating persistent response
        input_messages = [HumanMessage(text)]
        response = app.invoke({"messages": input_messages}, config)
        
        # returning the response
        return ResponseBuilder().setSuccess(True).setMessage("Response Generated Successfully").setData(encrypt(response["messages"][-1].content)).setStatusCode(200).build()
        
    except Exception as e:
        response = ResponseBuilder().setSuccess(False).setMessage("An Error Occured").setError(str(e)).setStatusCode(500).build()
        # Logging the error
        print(response)
        return response
    
  
