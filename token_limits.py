class TokenLimits:
    """
    A class to manage and retrieve token limits for OpenAI models.
    """
    def __init__(self):
        self._model_token_limits = {
            "gpt-4": 8192,
            "gpt-4-turbo": 128000,
            "gpt-4o": 128000,
            "gpt-4o-mini": 128000,
            "o1": 200000,
            "o1-mini": 128000,
        }

    def get_token_limit(self, model: str) -> int:
        """
        Get token limit for the specified model.
        Return the smallest token limit of the models available if the model
        is not found.
        """
        smallest = min(self._model_token_limits.values())
        return self._model_token_limits.get(model, smallest)
