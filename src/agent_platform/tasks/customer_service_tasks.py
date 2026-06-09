from crewai import Task
from agent_platform.guardrails.customer_support_guardrails import (
    mask_card_numbers_guardrail,
)


def create_customer_service_tasks(agents, customer_query, customer_id):
    """
    Create tasks for hierarchical customer service workflow.
    Manager will coordinate these tasks dynamically.
    """

    # Task 1: Classify and Route Query
    intake_task = Task(
        description=f"""Analyze this customer query and determine routing:
        
        Customer Query: "{customer_query}"
        Customer ID: {customer_id}
        
        Use the classification tool to:
        1. Identify the query category
        2. Assess urgency level
        3. Recommend routing to appropriate specialist
        4. Extract key information for the handling agent""",
        expected_output="""Query classification containing:
        - Category (authentication, account_inquiry, fraud_concern, etc.)
        - Urgency level (low, medium, high, critical)
        - Recommended routing
        - Key information extracted from query""",
        agent=agents["intake"],
    )

    # Task 2: Retrieve Account Context
    account_task = Task(
        description=f"""Retrieve account information for customer {customer_id}.
        
        Provide:
        1. Current account status and balance
        2. Recent transaction history
        3. Any active alerts or issues
        4. Relevant account details for addressing the query""",
        expected_output="""Account summary containing:
        - Account information
        - Account status and balance
        - Recent activity
        - Any alerts or concerns
        - Customer profile information""",
        agent=agents["account"],
        context=[intake_task],  # Depends on intake classification
        guardrail=mask_card_numbers_guardrail,
    )

    # Task 3: Resolve or Escalate
    resolution_task = Task(
        description="""Based on the query classification and account context, 
        either resolve the customer issue or prepare for escalation.
        
        If resolvable:
        1. Execute appropriate account action
        2. Provide clear confirmation to customer
        3. Document resolution
        
        If escalation needed:
        1. Summarize the situation
        2. Identify escalation path
        3. Prepare handoff information""",
        expected_output="""Resolution report containing:
        - Action taken (if resolved)
        - Customer communication (what to tell the customer)
        - Escalation recommendation (if needed)
        - Reference numbers or case IDs""",
        agent=agents["resolution"],
        context=[intake_task, account_task],
    )

    # Task 4: Technical Support (conditional, used if query is technical)
    technical_task = Task(
        description="""Provide technical support for complex system or application issues.
        
        1. Review the query and account context
        2. Search knowledge base for solutions
        3. Provide step-by-step troubleshooting
        4. Escalate to engineering if system-wide issue""",
        expected_output="""Technical support response containing:
        - Problem diagnosis
        - Step-by-step solution
        - Knowledge base article references
        - Escalation flag if needed""",
        agent=agents["technical"],
        context=[intake_task, account_task],
    )

    return [intake_task, account_task, resolution_task, technical_task]
