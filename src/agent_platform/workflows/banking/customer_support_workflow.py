import pprint as pretty
from crewai import Crew, Process
from agent_platform.llm.llmfactory import get_default_llm
from agent_platform.agents.customer_service_agents import create_customer_service_agents
from agent_platform.tasks.customer_service_tasks import create_customer_service_tasks


def handle_customer_query(query: str, customer_id: str):
    """
    Process customer service query using hierarchical workflow.
    """
    print(f"\n{'='*80}")
    print(f"CUSTOMER SERVICE - Query Processing")
    print(f"Customer: {customer_id}")
    print(f"Query: {query}")
    print(f"{'='*80}\n")

    # Create the agent team
    agents = create_customer_service_agents()

    # Create tasks
    tasks = create_customer_service_tasks(agents, query, customer_id)

    # Create hierarchical crew
    # Manager agent coordinates specialists automatically
    crew = Crew(
        agents=[
            agents["intake"],
            agents["account"],
            agents["resolution"],
            agents["technical"],
        ],
        tasks=tasks,
        process=Process.hierarchical,
        manager_llm=agents["manager"].llm,  # Use manager's LLM for coordination
        verbose=True,
    )

    # Execute
    try:
        result = crew.kickoff()

        print(f"\n{'='*80}")
        print("FINAL RESPONSE TO CUSTOMER")
        print(f"{'='*80}\n")
        print(result)

        return result

    except Exception as e:
        print(f"\nError processing query: {str(e)}")
        return None


if __name__ == "__main__":
    # Example 1: Password reset request
    result1 = handle_customer_query(
        query="I can't log into my account. I think I forgot my password.",
        customer_id="CUST12345",
    )

    # Example 2: Account inquiry
    # result2 = handle_customer_query(
    #     query="What's my current balance and recent transactions?",
    #     customer_id="CUST12345"
    # )

    # Example 3: Technical issue
    # result3 = handle_customer_query(
    #     query="The mobile app keeps crashing when I try to view statements.",
    #     customer_id="CUST67890"
    # )
