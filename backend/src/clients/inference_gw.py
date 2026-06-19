#copiado

from typing import Any

from .inference_client import InferenceHttpClient
from ..schemas.openaiLike_schema import ChatCompletionRequest


class InferenceGateway:
    """Encaminha completions para inference-api (payload sem metadados de chat)."""

    def __init__(self, provider: InferenceHttpClient | None = None) -> None:
        self._provider = provider or InferenceHttpClient()

    def chat_completion(self, request: ChatCompletionRequest) -> dict[str, Any]:
        if request.stream:
            msg = "stream=true não é suportado; envie stream=false."
            raise ValueError(msg)
        data = request.model_dump(exclude_none=True)
        data.pop("session_id", None)
        data.pop("channel", None)
        print("[inference payload]", data)
        return self._provider.chat_completions(data)