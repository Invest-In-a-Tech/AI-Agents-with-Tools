"""
Module for handling interactions between the user and the agent.

This script imports necessary modules and functions, defines the InteractionHandler class,
and provides methods for processing user inputs and managing the conversation history.

Classes:
    InteractionHandler: Class to handle interactions between the user and the agent.
"""

# Import necessary modules and functions from other files
from src.config.config import get_env_variable
from src.utils.tools_init import initialize_tools
from src.utils.agent_setup_openai import setup_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
import os


##############################################
# Define the InteractionHandler class
# ============================================
class InteractionHandler:
    """
    Class to handle interactions between the user and the agent.

    This class provides methods for initializing tools and agent executor, processing user inputs,
    determining the type of input (text or image), and maintaining the conversation history.

    Attributes:
        tools (dict): Dictionary of initialized tools required for the agent.
        agent_executor (AgentExecutor): Configured agent executor with the initialized tools.
        chat_history (list): List to keep track of the conversation history.
    """
    def __init__(self, chat_history=[]):
        """
        Initialize tools and agent executor, and create an empty list to store chat history.

        Args:
            chat_history (list, optional): Initial conversation history. Defaults to an empty list.
        """
        self.tools = initialize_tools()  # Load and initialize external tools required for the agent
        self.agent_executor = setup_agent(self.tools)  # Setup the agent with the initialized tools
        self.chat_history = chat_history  # Initialize an empty list to keep track of the conversation history


    ##############################################
    # Define the handle_input method
    # ============================================
    def handle_input(self, input_value, query=""):
        """
        Process the user's input, determine its type (image or text), 
        and call the appropriate processing function based on the input type.

        Args:
            input_value (str): The user's input.
            query (str, optional): Additional query for image input. Defaults to an empty string.

        Returns:
            dict: The result of processing the input.
        """
        # Check if the input is an image based on a special prefix
        if input_value.lower().startswith("image:"):
            input_type = "image"
            input_value = input_value[6:].strip()  # Remove the "image:" prefix to get the actual input
        else:
            input_type = "text"
        
        # Create a HumanMessage object for the input and append it to the chat history
        input_message = HumanMessage(content=input_value)
        self.chat_history.append(input_message)
        
        # Call the appropriate method based on the input type
        if input_type == "text":
            result = self.process_text_input(input_value)
        elif input_type == "image":
            result = self.process_image_input(input_value, query)
        else:
            # Return an error message for unknown input types
            return "Unknown input type."
        
        # Create an AIMessage object for the output and append it to the chat history
        output_message = AIMessage(content=result['output'])
        self.chat_history.append(output_message)
        return result


    ##############################################
    # Define the process_text_input method
    # ============================================
    def process_text_input(self, input_value):
        """
        Process text input by invoking the appropriate tool or action based on specific commands or general text input.

        Args:
            input_value (str): The user's text input.

        Returns:
            dict: The result of processing the text input.
        """
        # Check for specific text commands and invoke the corresponding tool or action
        if input_value.lower().startswith("search:"):
            # Extract the search query and invoke the Google search tool
            search_query = input_value[len("search:"):].strip()
            return self.agent_executor.invoke({
                "input": search_query,
                "tool": "google_search",
                "action": "run",
                "parameters": {},
                "chat_history": self.chat_history
            })
        else:
            # For general text input, invoke the agent executor without specifying a tool or action
            return self.agent_executor.invoke({
                "input": input_value,
                "parameters": {},
                "chat_history": self.chat_history
            })

    
    ##############################################
    # Defines the process_image_input method
    # ============================================
    def process_image_input(self, input_value, query):
        """
        Process image input by invoking an image processing tool with the given input and query.

        Args:
            input_value (str): The user's image input.
            query (str): Additional query for processing the image.

        Returns:
            dict: The result of processing the image input.
        """
        return self.agent_executor.invoke({
            "input": f"Process image: {input_value} with query: {query}",
            "tool": "image_processing_tool",
            "action": "process_image",
            "parameters": {"description": input_value, "query": query},
            "chat_history": self.chat_history
        })


    ##############################################
    # Define the run method
    # ============================================
    def run(self):
        """
        Start the interaction loop, accepting user input and processing it until the user decides to quit.
        """
        print("Welcome! I'm here to assist you. Type 'quit' to exit the conversation.")
        while True:
            # Accept user input
            input_value = input("\nEnter your input: ").strip()
            if input_value.lower() == "quit":
                # Exit the loop if the user types 'quit'
                print("Exiting the conversation.")
                break
            
            # Handle the user's input and optionally print the result
            results = self.handle_input(input_value)
            # print(results['output'])
