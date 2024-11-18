"""
Main script for running the interaction handler.

This script modifies the system path to ensure that the 'src' directory is included,
imports the InteractionHandler class, and runs the interaction handler if this script
is executed as the main program.

Classes:
    InteractionHandler: Class to handle interactions between the user and the agent.
"""

# Import necessary modules from the standard library
import sys  # Module to manipulate the Python runtime environment
import os  # Module to interact with the operating system

# Add the parent directory of 'src' to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# This allows the script to import modules from the 'src' directory and its parent directory

# Import the InteractionHandler class from the appropriate module
from src.controllers.interaction_handler import InteractionHandler

##############################################
# Check if this script is the main program
# ============================================
if __name__ == "__main__":
    """
    If this script is executed as the main program, instantiate and run the InteractionHandler.
    """
    # Instantiate the InteractionHandler
    interaction_handler = InteractionHandler()
    
    # Run the interaction handler to start handling user interactions
    interaction_handler.run()
    
    # Print a message indicating that the InteractionHandler has been instantiated
    print("InteractionHandler instantiated")
