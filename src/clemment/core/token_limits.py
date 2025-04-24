from ..config import MODEL_TOKEN_LIMITS

class TokenLimits:
    """
    A class to manage and retrieve token limits for OpenAI models.
    """
    def __init__(self):
        self._model_token_limits = MODEL_TOKEN_LIMITS

    def get_token_limit(self, model: str) -> int:
        """
        Get token limit for the specified model.
        Return the smallest token limit of the models available if the model
        is not found.
        """
        if model in self._model_token_limits:
            return self._model_token_limits.get(model)
        return min(self._model_token_limits.values())
