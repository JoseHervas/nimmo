import sys, os, uuid
from tempfile import TemporaryDirectory
from langchain.tools import tool
# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

working_directory = TemporaryDirectory()

class SearchInput(BaseModel):
    contents: str = Field(description="should be a string with the contents of the file")

@tool("write_file", return_direct=False, args_schema=SearchInput)
def write_file(contents: str) -> str:
    """Writes a file with the given contents"""
    file_path = os.path.join(working_directory.name, str(uuid.uuid4()))
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(contents)
        return f"File created at {file_path}"
    except IOError:
        return IOError
