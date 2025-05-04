"""
Module for initializing tool instances.

This script imports the necessary tool classes and defines a function to initialize
and return instances of these tools for use in other parts of the application.

Functions:
    initialize_tools(): Initializes and returns instances of various tools.
"""

# Import the tool classes from their respective modules
# from utils.screenshot_grabber_tool import ScreenshotGrabberTool
from services.screenshot_grabber_tool import ScreenshotGrabberTool
from src.services.image_describer_tool import ImageDescriberTool
from src.services.google_online_search_tool import GoogleSearchTool

##############################################
# Define the initialize_tools function
# ============================================
def initialize_tools():
    """
    Initialize and return instances of various tools.

    This function creates a dictionary named 'tools' to store instances of different tools.
    The keys of the dictionary are string identifiers for the tools, and the values are
    the instantiated objects of the respective tool classes.

    Returns:
        dict: A dictionary containing the initialized tool instances.
    """
    # Create a dictionary named 'tools' to store the instances of each tool
    tools = {
        "screenshot_grabber": ScreenshotGrabberTool(),  # Instance of ScreenshotGrabberTool
        "image_describer": ImageDescriberTool(),        # Instance of ImageDescriberTool
        "google_search": GoogleSearchTool()             # Instance of GoogleSearchTool
    }
    # Return the dictionary containing the tool instances
    return tools
