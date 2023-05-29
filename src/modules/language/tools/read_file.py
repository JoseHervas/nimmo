import sys, os, uuid
from langchain.tools import tool
# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from modules.file_manager import TempFolder

temp_folder = TempFolder()

class SearchInput(BaseModel):
    name: str = Field(description="should be a string with the file name")

@tool("read_file", return_direct=False, args_schema=SearchInput)
def read_file(name: str) -> str:
    """Reads a file with the given name"""
    try:
        contents = temp_folder.read_file(name)
        return contents
    except IOError:
        return IOError
