from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


def get_lmstudio_llm(
    model: str, temperature: float, base_url: str, api_key: str, llm_type: str
) -> Dict[str, Any]:
    """
    Configures the necessary parameters for making an API call to a local
    LLM running via LMStudio.

    Args:
        model: Model name as string (e.g., "llama-2").
        temperature: Randomness control (float, default is 0.7).
        base_url: The API endpoint URL.
        api_key: Authentication key.
        llm_type: Specifies the type of language model ('openai', 'ollama').

    Returns:
        LLMConfig: A structured object containing all configuration parameters.
    """
    return {
        "model": model,
        "temperature": temperature,
        "base_url": base_url,
        "api_key": api_key,
        "llm_type": llm_type,
    }
