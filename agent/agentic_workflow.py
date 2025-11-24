
from utils.model_loader  import ModelLoader
from prompt_library.prompt import SYSTERM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition

from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import Calculatortool
from tools.currency_conversion_tool import CurrencyConverterTool 

class GraphBuilder():
    def __init__(self,model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider= model_provider)
        self.llm = self.model_loader.load_llm()
        self.tools=[]
        
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.expense_calculator_tools = Calculatortool()
        self.currency_converter_tools = CurrencyConverterTool() 
        
        self.tools.extend([* self.weather_tools.weather_tool_list,
                       * self.place_search_tools.place_search_tool_list,
                       * self.calculator_tools.calculator_tool_list,
                       * self.currancy_converter_tools.currency_converter_tool.list])    
        
        self.llm_with_tools = self.llm.bind_tools(tools= self.tools)   
        self.graph = None
        self.system_prompt = SYSTERM_PROMPT
    
    def agent_funtion(self,state: MessagesState):  
        # takes the decision for which tool to be called
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}
 
 
    def build_graph(self):
       graph_builder = StateGraph(MessagesState())
       graph_builder.add_edge(START, "agent")
       graph_builder.add_node("agent", self.agent_funtion)
       graph_builder.add_node("tools", ToolNode(tools=self.tools))
       graph_builder.add_conditional_edges("agent", tools_condition)
       graph_builder.add_edge("tools", "agent")
       graph_builder.add_edge("agent", END) 
       self.graph = graph_builder.compile()
       return self.graph     
    
    def __call__(self):
        return self.build_graph()
        