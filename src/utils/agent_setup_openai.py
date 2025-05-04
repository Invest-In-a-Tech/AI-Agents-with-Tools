"""
Module for setting up an agent using the LangChain framework with OpenAI's GPT models.

This script imports necessary modules and classes, defines the setup_agent function,
and binds tools to a ChatOpenAI instance for advanced conversational capabilities.

Functions:
    setup_agent(tools): Configures and returns an AgentExecutor instance with the provided tools.
"""

# Import necessary modules and classes from various packages and files
from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler  
from src.prompts.advanced_assistant_prompt import advanced_assistant_prompt  # Custom prompt template for initializing conversation
from src.config.config import get_env_variable  # Function to retrieve environment variables


##############################################
# Define the setup_agent function
# ============================================
def setup_agent(tools):
    """
    Configures and returns an AgentExecutor instance using OpenAI's GPT models.

    This function:
    1. Retrieves the OpenAI API key from environment variables.
    2. Initializes a ChatOpenAI instance with the specified model, API key, and streaming callback.
    3. Binds the provided tools to the ChatOpenAI instance.
    4. Defines a structured prompt template for the language model.
    5. Creates an agent pipeline that processes input, uses the prompt template, queries the language model, and parses the output.
    6. Returns an AgentExecutor instance configured with the defined agent, tools, and verbosity settings.

    Args:
        tools (dict): A dictionary of tools to bind to the ChatOpenAI instance.

    Returns:
        AgentExecutor: An instance of AgentExecutor configured with the specified tools and settings.
    """
    
    # Retrieve the OpenAI API key from environment variables
    openai_api_key = get_env_variable("OPENAI_API_KEY")

    # Initialize a ChatOpenAI instance with specific model, API key, and callbacks for streaming output
    llm = ChatOpenAI(
        model="gpt-4o",  # Our most advanced, multimodal flagship model that’s cheaper and faster than GPT-4 Turbo. Currently points to gpt-4o-2024-05-13.
        # model="gpt-4.1",  # Specify the model to use (commented lines show other options)
        # model="gpt-3.5-turbo-0125",  # Specify the model to use (commented lines show other options)
        # model="gpt-4-0125-preview", 
        # model="gpt-4",       
        api_key=openai_api_key,  # Use the retrieved API key
        streaming=True,  # Enable streaming for real-time processing
        callbacks=[StreamingStdOutCallbackHandler()]  # Use a callback handler for streaming output to stdout
    )

    # Bind the ChatOpenAI instance with the provided tools for extended functionality
    llm_with_tools = llm.bind_tools(list(tools.values()))

    # Define a prompt template that structures the input for the language model
    prompt = ChatPromptTemplate.from_messages([
        ("system", advanced_assistant_prompt),  # System-level message to initialize conversation context
        MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for the conversation history
        ("user", "{input}"),  # Placeholder for the user's input
        MessagesPlaceholder(variable_name="agent_scratchpad"),  # Placeholder for any additional agent-specific messages
    ])

    # Define an agent pipeline that processes input, uses the prompt template, queries the language model, and parses the output
    agent = (
        {
            "input": lambda x: x["input"],  # Extract the user's input from the provided data
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),  # Process intermediate steps for the agent's scratchpad
            "chat_history": lambda x: x["chat_history"],  # Pass through the conversation history
        }
        | prompt  # Apply the prompt template to structure the input for the language model
        | llm_with_tools  # Query the language model with tools bound
        | OpenAIToolsAgentOutputParser()  # Parse the output from the language model
    )

    # Return an AgentExecutor instance configured with the defined agent, tools, and verbosity settings
    return AgentExecutor(
        agent=agent, 
        tools=list(tools.values()), 
        verbose=False  # Enable verbose output for debugging or informational purposes
    )
