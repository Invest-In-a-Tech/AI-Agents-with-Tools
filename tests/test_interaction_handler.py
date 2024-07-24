import pytest
from src.controllers.interaction_handler import InteractionHandler
from langchain_core.messages import AIMessage, HumanMessage

def test_interaction_handler_initialization():
    handler = InteractionHandler()
    assert handler is not None
    assert handler.tools is not None
    assert handler.agent_executor is not None
    assert handler.chat_history == []
