import os
from dotenv import load_dotenv
from agent_platform.misc.utils import mask_password

load_dotenv()

LLM_MODEL = os.environ["LLM_MODEL"]
LLM_TEMPERATURE = os.environ.get("LLM_TEMPERATURE")
LLM_INFRA_BASE_URL = os.environ.get("LLM_INFRA_BASE_URL")
LLM_INFRA_API_KEY = os.environ.get("LLM_INFRA_API_KEY")
LLM_INFRA_LLM_TYPE = os.environ.get("LLM_INFRA_LLM_TYPE")


print("")
print("--------------------------------------------------")
print("Project ENV Variables")
print("--------------------------------------------------")
print("LLM_MODEL: " + LLM_MODEL)
print("LLM_TEMPERATURE: " + LLM_TEMPERATURE)
print("LLM_INFRA_BASE_URL: " + LLM_INFRA_BASE_URL)
print("LLM_INFRA_API_KEY: " + mask_password(LLM_INFRA_API_KEY))
print("LLM_INFRA_LLM_TYPE: " + LLM_INFRA_LLM_TYPE)
print("--------------------------------------------------")
print("")