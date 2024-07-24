
# AI Agents with Tools

## Project Description
This project provides a template for building interactive applications using various AI tools and APIs. It shows the integration of **OpenAI API**, **Google Generative AI API**, **LangChain**, function calling, and agents with tools. This template is designed to handle requests, process data, and return responses, acting as an intermediary between user inputs and AI-powered outputs.

### Key Features
- **AI Integration**: Integrates OpenAI API, Google Generative AI API, LangChain, and other advanced AI tools.
- **Interactivity**: Handles user inputs and processes them to provide meaningful AI-powered responses.
- **Framework Flexibility**: Compatible with FastAPI, Flask, and Django, allowing developers to choose their preferred framework.
- **Extensibility**: Provides a solid foundation that can be extended to support additional functionalities like CRUD operations and user authentication.
- **Best Practices**: Demonstrates best practices in AI integration and interactive application development.



## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites
- Python 3.8 or higher
- A system with Windows, macOS, or Linux operating system

### Step-by-Step Instructions
Clone the repository:

```sh
git https://github.com/Invest-In-a-Tech/AI-Agents-with-Tools
cd ai-agents-with-tools
```

Create and activate a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate   # On Windows, use `.venv\Scripts\activate`
```

Install the required dependencies:

```sh
pip install -r requirements.txt
```

## Usage
To run the AI Agent with Tools, follow these steps:

1. **Configure environment variables:**
   Create a `.env` file in the root directory of the project with the necessary environment variables. Refer to the `.env` template provided in the repository.

2. **Run the main application:**
   ```sh
   python src/run_interaction_handler.py
   ```
*Note: The `run_interaction_handler.py` script is for demonstration purposes and may need to be modified to suit your specific use case.*

## Project Structure
The project structure is as follows:

```lua
ai-agents-with-tools/
├── __pycache__/
├── .env
├── .gitignore
├── .pytest_cache/
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   ├── README.md
│   └── v/
│       └── cache/
├── .vscode/
│   └── settings.json
├── docs/
│   ├── api_spec.md
│   └── setup_guide.md
├── logs/
│   └── openai_api.log
├── pytest.ini
├── README.md
├── requirements.txt
├── scripts/
├── src/
│   ├── config/
│   │   └── config.py
│   ├── controllers/
│   │   └── interaction_handler.py
│   ├── prompts/
│   │   └── advanced_assistant_prompt.py
│   ├── run_interaction_handler.py
│   ├── services/
│   │   └── image_describer_tool.py
│   │   └── google_online_search_tool.py
│   ├── utils/
│   │   └── agent_setup_openai.py
│   ├── tools/
│   └── tools_init.py
├── tests/
│   └── test_interaction_handler.py
```

- **src/config/config.py**: Configuration settings for the project.
- **src/controllers/interaction_handler.py**: Handles interactions and coordinates between different tools.
- **src/prompts/advanced_assistant_prompt.py**: Contains advanced prompt handling logic.
- **src/run_interaction_handler.py**: Entry point for running the interaction handler.
- **src/services/image_describer_tool.py**: Describes images using the specified tool.
- **src/services/google_online_search_tool.py**: Implements a tool for performing online searches using Google API.
- **src/utils/agent_setup_openai.py**: Sets up the OpenAI API.
- **src/tools_init.py**: Initializes various tools required for the project.

## Configuration
Ensure that you have the necessary API keys and configurations set in your `.env` file. An example `.env` file might look like this:

```makefile
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_google_cse_id
```

## Architecture
The AI Agent with Tools is designed to handle requests and process data, with the storage of information managed by the client applications. Below is a high-level overview of the architecture:

- **AI Agent with Tools**: Acts as an intermediary, processing POST requests and returning appropriate responses.
- **Web Apps (1 & 2)**: Client applications that interact with the API, sending POST requests and storing responses in their respective databases.
- **Databases**: Store the responses received from the API.

## Detailed Module Descriptions

### src/controllers/interaction_handler.py
This module handles interactions between the user and the agent. It initializes the necessary tools and agent executor, processes user inputs, and manages the conversation history.

#### Class InteractionHandler:
- **Attributes:**
  - `tools`: Dictionary of initialized tools required for the agent.
  - `agent_executor`: Configured agent executor with the initialized tools.
  - `chat_history`: List to keep track of the conversation history.
- **Methods:**
  - `__init__(self, chat_history=[])`: Initializes tools, agent executor, and chat history.
  - `handle_input(self, input_value, query="")`: Processes user input, determines its type (text or image), and calls the appropriate processing function.
  - `process_text_input(self, input_value)`: Processes text input by invoking the appropriate tool or action.
  - `process_image_input(self, input_value, query)`: Processes image input by invoking an image processing tool.
  - `run(self)`: Starts the interaction loop, accepting user input and processing it until the user decides to quit.

### src/services/image_describer_tool.py
This module processes and describes images using Google Generative AI.

#### Class ImageDescriberTool:
- **Attributes:**
  - `name`: Name of the tool.
  - `description`: Short description of what the tool does.
  - `args_schema`: The input validation model assigned to the tool.
- **Methods:**
  - `_run(self, file_path: str, query: str = "describe the image") -> str`: Executes a synchronous image processing and description task.
  - `process_uploaded_image(file_path)`: Processes the uploaded image file to prepare it for API interaction.
  - `image_data_to_data_url(image_parts)`: Converts image data to a data URL format.

### src/services/google_online_search_tool.py
This module enables performing online searches using Google's search capabilities.

#### Class GoogleOnlineSearchTool:
- **Attributes:**
   - `name`: Name of the tool.
   - `description`: Short description of the tool's functionality, focusing on its ability to perform online searches.
   - `args_schema`: The input validation model assigned to the tool, ensuring that search queries meet specific criteria before execution.
- **Methods:**
   - `search(self, query: str, num_results: int = 10) -> list`: Executes an online search for the given query and returns a list of results. The number of results can be specified.
   - `format_search_results(self, results) -> str`: Formats the raw search results into a more readable or structured format, depending on the implementation details.
   - `validate_query(self, query: str) -> bool`: Validates the search query against the `args_schema` to ensure it meets the necessary criteria for a successful search.

## Contributing
We welcome contributions to Custom REST API. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature-branch
   ```
3. Make your changes and commit them:
   ```sh
   git commit -m 'Add new feature'
   ```
4. Push to the branch:
   ```sh
   git push origin feature-branch
   ```
5. Create a pull request.

For detailed guidelines, please refer to our Contributing Guide.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
