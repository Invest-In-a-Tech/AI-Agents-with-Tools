"""
Module for integrating Google Search functionality with LangChain tools.

This script imports necessary modules and classes, loads configuration values from the environment,
and defines a Pydantic model and a tool class for performing Google searches.

Classes:
    SearchInput(BaseModel): Pydantic model for validating and documenting the expected input for the search tool.
    GoogleSearchTool(BaseTool): Class for the Google Search tool, extending LangChain's BaseTool.
"""

# Import necessary modules and classes for typing, LangChain tool management, Pydantic models, and utility functions
from typing import Optional, Type  
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_google_community import GoogleSearchAPIWrapper
from src.config.config import get_env_variable  # Import function to load environment variables

# Load necessary configuration values from the environment
google_api_key = get_env_variable("GOOGLE_API_KEY")  # API key for authenticating requests to Google's API
google_cse_id = get_env_variable("GOOGLE_CSE_ID")  # Custom Search Engine ID to specify which CSE to query


##############################################
# Define the SearchInput class
# ============================================
class SearchInput(BaseModel):  
    """
    Pydantic model for validating and documenting the expected input for the search tool.

    Attributes:
        query (str): The search query string that should be provided as input.
    """
    query: str = Field(description="should be a search query")  # Define a single field 'query' expected as input


##############################################
# Define the GoogleSearchTool class
# ============================================
class GoogleSearchTool(BaseTool):  
    """
    Class for the Google Search tool, extending LangChain's BaseTool.

    This class provides methods for performing synchronous Google searches using the specified API key and CSE ID.

    Attributes:
        name (str): Name of the tool.
        description (str): Short description of what the tool does.
        args_schema (Type[BaseModel]): The input validation model assigned to the tool.
        search (GoogleSearchAPIWrapper): Wrapper around Google's Search API.
    """
    name = "google_search"  # Name of the tool, used for referencing in the LangChain framework
    description = "Search Google for recent results."  # Short description of what the tool does
    args_schema: Type[BaseModel] = SearchInput  # Assign the input validation model to the tool

    # Initialize a wrapper around Google's Search API using the loaded environment variables
    search = GoogleSearchAPIWrapper(
        google_api_key=google_api_key,
        google_cse_id=google_cse_id
    ) 


    ##############################################
    # Define the _run method
    # ============================================
    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:  
        """
        Execute a synchronous search query using the tool.

        This method uses the API wrapper to perform a search with the provided query string.

        Args:
            query (str): The search query string.
            run_manager (Optional[CallbackManagerForToolRun]): Optional callback manager for tool run.

        Returns:
            str: The search results.
        """
        return self.search.run(query)


    ##############################################
    # Define the _arun method
    # ============================================
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:  
        """
        Placeholder for an asynchronous execution of the tool, currently not implemented.

        This method explicitly raises a NotImplementedError to indicate the lack of async support for Google Search.

        Args:
            query (str): The search query string.
            run_manager (Optional[AsyncCallbackManagerForToolRun]): Optional callback manager for tool run.

        Raises:
            NotImplementedError: Indicates that asynchronous execution is not supported.
        """
        raise NotImplementedError("Google Search does not support async")  
