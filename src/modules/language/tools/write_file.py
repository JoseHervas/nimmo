import sys, os, uuid
from langchain.tools import tool
# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from modules.file_manager import TempFolder

working_directory = TempFolder()

class SearchInput(BaseModel):
    contents: str = Field(description="should be a string with the contents of the file")

def generate_write_tool(llm):
    """Generates the tool for the module"""
    @tool("write_file", return_direct=False, args_schema=SearchInput)
    def write_file(contents: str) -> str:
        """Writes a file with the given contents. Returns the file name"""
        file_name = str(uuid.uuid4())
        try:
            working_directory.create_file(file_name, contents)
            # Sometimes bot remembers this and sometimes it doesn't
            # llm.remember(f"File has the name {file_name}")
            return f"File created with the name {file_name}"
        except IOError:
            return IOError

    # Agent tools can only accept 1 argument
    # so we need to use closures to pass in the llm
    return write_file
