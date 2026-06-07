import os
from dotenv import load_dotenv
from agent_platform.llm.lmstudio import get_lmstudio_llm
import agent_platform.config.env as env

load_dotenv()


# Default LLM for quick testing
def get_default_llm():
    model = env.LLM_MODEL
    temperature = env.LLM_TEMPERATURE
    base_url = env.LLM_INFRA_BASE_URL
    api_key = env.LLM_INFRA_API_KEY
    llm_type = env.LLM_INFRA_LLM_TYPE

    return get_lmstudio_llm(model, temperature, base_url, api_key, llm_type)
