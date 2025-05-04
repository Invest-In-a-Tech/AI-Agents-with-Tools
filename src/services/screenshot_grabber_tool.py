"""
Module for capturing screenshots from a specified monitor using the ScreenshotGrabberTool.

This script imports necessary modules, defines a Pydantic model for input validation,
and implements a tool class that captures and saves screenshots.

Classes:
    ScreenshotInput(BaseModel): Pydantic model for validating and documenting the expected input for the screenshot tool.
    ScreenshotGrabberTool(BaseTool): Class for the screenshot grabbing tool, extending LangChain's BaseTool.
"""

# Import necessary standard library modules and third-party packages
import os
import time
from typing import Type
from screeninfo import get_monitors  # Used to retrieve information about the monitors connected to the system
import mss  # Reliable multi-monitor screenshot tool
from PIL import Image  # Used to process raw image data
from pydantic import BaseModel, Field  # For data validation and settings management
from langchain.tools import BaseTool  # Base class for creating tools within a certain framework
from langchain_core.tools import ToolException  # Custom exception for error handling within tools


###################################################
# Define the input schema for the screenshot tool 
# =================================================
class ScreenshotInput(BaseModel):
    """
    Represents the input parameters for capturing a screenshot.

    Args:
        monitor_number (int, optional): Specifies which monitor to take a screenshot of. Defaults to 1.

    Attributes:
        monitor_number (int): The monitor number from which to capture the screenshot.
    """
    monitor_number: int = Field(default=1, description="The monitor number from which to capture the screenshot.")


###################################################
# Define the ScreenshotGrabberTool class
# =================================================
class ScreenshotGrabberTool(BaseTool):
    """
    Tool for taking a screenshot of the specified monitor and saving it to a predefined directory.
    """

    name: str = "screenshot_grabber"
    description: str = "Tool to grab screenshots of the current screen"
    args_schema: Type[BaseModel] = ScreenshotInput

    def _run(self, monitor_number: int = 1) -> str:
        """
        Takes a screenshot of the specified monitor and saves it to a predefined directory.

        Args:
            monitor_number (int): The monitor number from which to capture the screenshot. Defaults to 1.

        Returns:
            str: A message indicating where the screenshot was saved.
        
        Raises:
            ToolException: If an invalid monitor number is specified.
        """
        # Define the directory where screenshots will be saved
        save_directory = os.path.join("screenshot_grabber", "screenshots")

        # Create the directory if it doesn't already exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Generate a timestamp for the filename to ensure uniqueness
        timestamp = time.strftime('%Y%m%d_%H%M%S')

        # Construct the filename and path for the screenshot
        filename = f"screenshot_{timestamp}.png"
        file_path = os.path.join(save_directory, filename)

        # Use MSS to take the screenshot
        with mss.mss() as sct:
            if monitor_number > len(sct.monitors) - 1 or monitor_number < 1:
                raise ToolException(f"Monitor number {monitor_number} is out of range. Available monitors: 1 to {len(sct.monitors) - 1}")

            monitor = sct.monitors[monitor_number]  # mss uses 1-based index; index 0 is all monitors combined
            screenshot = sct.grab(monitor)

            # Convert raw bytes to image and save
            img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
            img.save(file_path)

        return f"Screenshot saved as {file_path}"

