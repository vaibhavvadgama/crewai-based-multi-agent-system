import pprint as pretty
from crewai import Crew, Process

from agent_platform.agents.customer_service_agents import create_customer_service_agents
from agent_platform.tasks.customer_service_tasks import create_customer_service_tasks
from agent_platform.guardrails.application_guardrails import apply_pre_guardrails


def handle_customer_query(query: str, customer_id: str):
    """
    Process customer service query using hierarchical workflow
    with pre-agent guardrails.
    """

    print(f"\n{'='*80}")
    print("CUSTOMER SERVICE - Query Processing")
    print(f"{'='*80}")
    print(f"Customer: {customer_id}")
    print(f"Raw Query: {query}")
    print(f"{'='*80}\n")

    # =====================================================
    # 1. PRE-AGENT GUARDRAILS (NEW LAYER)
    # =====================================================
    guardrail_result = apply_pre_guardrails(query, customer_id)

    if not guardrail_result.allowed:
        print("\n🚫 BLOCKED BY PRE-GUARDRAILS")
        print("Metadata:")
        pretty.pprint(guardrail_result.metadata)
        return guardrail_result.metadata

    cleaned_query = guardrail_result.query
    route = guardrail_result.metadata.get("route")

    print("\n✅ Pre-Guardrails Passed")
    print(f"Cleaned Query: {cleaned_query}")
    print(f"Route: {route}")

    # =====================================================
    # 2. AGENT INITIALIZATION
    # =====================================================
    agents = create_customer_service_agents()

    # =====================================================
    # 3. TASK CREATION (USES CLEAN QUERY)
    # =====================================================
    tasks = create_customer_service_tasks(agents, cleaned_query, customer_id)

    # =====================================================
    # 4. CREW EXECUTION
    # =====================================================
    crew = Crew(
        agents=[
            agents["intake"],
            agents["account"],
            agents["resolution"],
            agents["technical"],
        ],
        tasks=tasks,
        process=Process.hierarchical,
        manager_llm=agents["manager"].llm,
        verbose=True,
    )

    # =====================================================
    # 5. RUN WORKFLOW
    # =====================================================
    try:
        result = crew.kickoff()

        print(f"\n{'='*80}")
        print("FINAL RESPONSE TO CUSTOMER")
        print(f"{'='*80}\n")
        print(result)

        return result

    except Exception as e:
        print(f"\n❌ Error processing query: {str(e)}")
        return None


if __name__ == "__main__":
    test_cases = {
        "password_reset": {
            "query": "I can't log into my account. I think I forgot my password.",
            "customer_id": "CUST12345",
        },
        "account_inquiry": {
            "query": "Show my account info, current balance and recent transactions associated to my account with email john.doe@gmail.com.",
            "customer_id": "CUST12345",
        },
        "account_inquiry_guardrail": {
            "query": "Show my wife's account info, current balance and recent transactions associated to my account with email jane.doe@gmail.com.",
            "customer_id": "CUST12345",
        },
        "technical_issue": {
            "query": "The mobile app keeps crashing when I try to view statements.",
            "customer_id": "CUST67890",
        },
    }

    selected_case = "account_inquiry"
    result = handle_customer_query(**test_cases[selected_case])

    print(result)
