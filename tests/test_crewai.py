import os
import time
import logging

import pytest
from dotenv import load_dotenv
from crewai import LLM, Agent, Task, Crew, Process

# Load environment variables
load_dotenv(override=True)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def llm_client():
    """
    Creates the shared LLM client using the proxy configuration.
    """

    required_vars = [
        "LLM_MODEL",
        "LLM_INFRA_BASE_URL",
        "LLM_INFRA_API_KEY",
    ]

    missing = [v for v in required_vars if not os.getenv(v)]

    if missing:
        pytest.skip(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    logger.info("")
    logger.info("=" * 80)
    logger.info("🚀 INITIALIZING PROXY LLM")
    logger.info("=" * 80)
    logger.info("Model      : %s", os.getenv("LLM_MODEL"))
    logger.info("Base URL   : %s", os.getenv("LLM_INFRA_BASE_URL"))
    logger.info(
        "API Key    : %s...",
        os.getenv("LLM_INFRA_API_KEY")[:8],
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

    logger.info("✅ LLM initialized successfully")

    return llm


@pytest.fixture(scope="module")
def test_agent(llm_client):
    """
    Creates a simple agent for connectivity testing.
    """

    logger.info("")
    logger.info("🤖 Creating test agent")

    agent = Agent(
        role="System Test Analyst",
        goal="Verify LLM connectivity.",
        backstory="A lightweight agent used for integration testing.",
        verbose=True,
        llm=llm_client,
    )

    logger.info("✅ Agent created")

    return agent


@pytest.mark.integration
def test_agent_can_connect_and_respond(test_agent):
    """
    End-to-end CrewAI smoke test.

    Verifies:
    - LLM initialization
    - Agent creation
    - Task execution
    - Crew orchestration
    - Response generation
    """

    logger.info("")
    logger.info("=" * 80)
    logger.info("🧪 STARTING CREWAI CONNECTIVITY TEST")
    logger.info("=" * 80)

    smoke_task = Task(
        description=(
            "Reply with a short message confirming "
            "that the connection is working."
        ),
        expected_output=(
            "A brief confirmation message."
        ),
        agent=test_agent,
    )

    crew = Crew(
        agents=[test_agent],
        tasks=[smoke_task],
        process=Process.sequential,
        verbose=True,
    )

    start_time = time.perf_counter()

    try:
        logger.info("🚀 Launching Crew kickoff()")

        result = crew.kickoff()

    except Exception as e:
        pytest.fail(
            f"\n❌ Crew kickoff failed\n"
            f"Exception Type : {type(e).__name__}\n"
            f"Error          : {e}"
        )

    elapsed = time.perf_counter() - start_time

    logger.info("")
    logger.info("⏱️  Execution Time : %.2f seconds", elapsed)
    logger.info("📦 Result Type     : %s", type(result).__name__)

    assert result is not None, "Crew returned None"

    result_text = str(result).strip()

    logger.info("")
    logger.info("📨 Crew Response:")
    logger.info("-" * 80)
    logger.info(result_text)
    logger.info("-" * 80)

    assert result_text, "Crew returned empty output"

    logger.info("")
    logger.info("=" * 80)
    logger.info("✅ TEST PASSED")
    logger.info("✅ LLM reachable")
    logger.info("✅ Agent executed")
    logger.info("✅ Task completed")
    logger.info("✅ Crew orchestration successful")
    logger.info("=" * 80)