from langchain.callbacks.stdout import StdOutCallbackHandler
from typing import Any, Dict, List, Optional
from langchain.schema import LLMResult

class Logger(StdOutCallbackHandler):

    mode = "Debug"

    def __init__(self, color: str | None = None, mode: str | None = None) -> None:
        super().__init__(color)
        self.mode = mode

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Print out the prompts."""
        print("PROMPTS", prompts)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Do nothing."""
        print("RESULTS", response)

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""
        print(f"Chain inputs: {inputs}")
