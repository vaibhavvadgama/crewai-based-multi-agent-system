import os
import time
import logging

import pytest
from dotenv import load_dotenv
from crewai import LLM

# Load environment variables
load_dotenv(override=True)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def llm_client():
    """
    Initialize LLM client once for the entire test module.
    """

    required_vars = [
        "LLM_MODEL",
        "LLM_INFRA_BASE_URL",
        "LLM_INFRA_API_KEY",
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        pytest.skip(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    logger.info("=" * 80)
    logger.info("🚀 INITIALIZING LLM CLIENT")
    logger.info("=" * 80)

    logger.info("Model      : %s", os.getenv("LLM_MODEL"))
    logger.info("Base URL   : %s", os.getenv("LLM_INFRA_BASE_URL"))
    logger.info(
        "API Key    : %s...",
        os.getenv("LLM_INFRA_API_KEY")[:8]
    )

    llm = LLM(
        model=os.getenv("LLM_MODEL"),
        base_url=os.getenv("LLM_INFRA_BASE_URL"),
        api_key=os.getenv("LLM_INFRA_API_KEY"),
        provider="openai",
        extra_headers={
            "User-Agent": "CrewAI-Integration-Test/1.0"
        },
    )

    logger.info("✅ LLM client initialized successfully")

    return llm


@pytest.mark.integration
def test_llm_connectivity(llm_client):
    """
    Smoke test to verify:
    - LLM proxy is reachable
    - Authentication works
    - Model returns a valid response
    """

    prompt = """
    Reply with exactly:
    OK
    """.strip()

    logger.info("")
    logger.info("=" * 80)
    logger.info("🧪 STARTING LLM CONNECTIVITY TEST")
    logger.info("=" * 80)

    logger.info("Prompt:")
    logger.info(prompt)

    start_time = time.perf_counter()

    try:
        response = llm_client.call(prompt)

    except Exception as e:
        pytest.fail(
            f"\n❌ LLM invocation failed\n"
            f"Exception Type : {type(e).__name__}\n"
            f"Error          : {e}"
        )

    elapsed = time.perf_counter() - start_time

    logger.info("")
    logger.info("⏱️  Response Time: %.2f seconds", elapsed)
    logger.info("📦 Response Type: %s", type(response).__name__)

    # Normalize response
    if response is None:
        pytest.fail("❌ Response is None")

    if isinstance(response, str):
        content = response.strip()

    elif isinstance(response, dict):
        content = (
            response.get("text")
            or response.get("content")
            or str(response)
        ).strip()

    else:
        content = str(response).strip()

    logger.info("")
    logger.info("📨 Response Content:")
    logger.info(content)

    # Assertions
    assert content, "Response content is empty"

    logger.info("")
    logger.info("=" * 80)
    logger.info("✅ TEST PASSED")
    logger.info("✅ Proxy reachable")
    logger.info("✅ Authentication valid")
    logger.info("✅ Model returned content")
    logger.info("=" * 80)