import sys, os
from langchain.tools import tool
from langchain.utilities import PythonREPL
# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

class CommandInput(BaseModel):
    python_code_snippet: str = Field(description="should be a string with a valid python code snippet")

@tool("python_repl", return_direct=False, args_schema=CommandInput)
def python_repl(python_code_snippet: str) -> str:
    """Runs a given python code snippet."""
    python = PythonREPL()
    result = python.run(python_code_snippet)
    return result
