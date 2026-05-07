"""
AI Agent com Function Calling - MVP
Pacote principal da aplicação
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "MVP de AI Agent com Function Calling e Logging"

from agent import AIAgent
from functions import registry, FunctionRegistry
from logger import logger

__all__ = ["AIAgent", "registry", "FunctionRegistry", "logger"]
