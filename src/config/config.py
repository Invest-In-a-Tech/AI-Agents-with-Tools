"""
Module for loading environment variables and retrieving their values.

This script imports necessary modules, automatically loads environment variables
from a .env file, and defines a function to retrieve these variables.

Functions:
    get_env_variable(name, default=None): Retrieves the value of an environment variable.
"""

# Import the necessary modules from the standard library and dotenv package
import os  # Module to interact with the operating system, including environment variables
from dotenv import load_dotenv, find_dotenv  # Functions from the dotenv package to load and find .env files

# Automatically locate and load environment variables from a .env file
load_dotenv(find_dotenv())  
# find_dotenv() searches for the .env file in the current directory or recursively up the hierarchy
# load_dotenv() reads the .env file found by find_dotenv() and loads the variables into the program's environment


##############################################
# Define the get_env_variable function
# ============================================
def get_env_variable(name, default=None):
    """
    Retrieve the value of an environment variable.

    This function fetches the value of an environment variable specified by 'name'.
    If the variable is not found, it returns the 'default' value provided.

    Args:
        name (str): The name of the environment variable to retrieve.
        default (any, optional): The default value to return if the environment variable is not found. Defaults to None.

    Returns:
        any: The value of the environment variable, or the default value if the variable is not found.
    """
    # Retrieve the value of an environment variable
    return os.environ.get(name, default)  
    # os.environ is a dictionary containing environment variables
    # .get() method is used to retrieve the value for the key 'name'
    # If 'name' does not exist in os.environ, the 'default' value is returned instead
