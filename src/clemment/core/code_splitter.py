import tiktoken
from langchain_text_splitters.python import PythonCodeTextSplitter

from ..config import MODEL_TOKEN_LIMITS


class CodeSplitter:
    """
    Splits python code into chunks based on token limits for OpenAI models
    while preserving the code structure.
    """
    def __init__(self, model: str, chunk_size: int):
        self.model = model
        token_limit = MODEL_TOKEN_LIMITS.get(model)
        if token_limit < chunk_size:
            raise ValueError(
                f'Chunk size {chunk_size} exceeds model token limit',
                f'{token_limit}.'
            )
        self.encoding = tiktoken.encoding_for_model(model)
        self.splitter = PythonCodeTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=0,
            length_function=self._count_tokens
        )

    def _count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a given text for the class model.
        """
        tokens = self.encoding.encode(text)
        return len(tokens)

    def split_code(self, code: str) -> list:
        """
        Split the code into chunks that fit within the token limit of the
        model.
        """
        return self.splitter.split_text(code)
