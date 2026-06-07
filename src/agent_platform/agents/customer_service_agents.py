from crewai import Agent
from agent_platform.llm.llmfactory import get_default_llm
from agent_platform.tools.customer_service_tools import (
    classify_query,
    access_customer_account,
    execute_account_action,
    check_knowledge_base,
)


def create_customer_service_agents():
    """
    Create a hierarchical customer service team.
    Uses different LLMs based on task complexity for cost optimization.
    """

    # Intake Agent - Simple classification task, use fast/cheap model
    intake_agent = Agent(
        role="Customer Query Intake Specialist",
        goal="Quickly classify and route customer queries to appropriate handlers",
        backstory="""You are a front-line customer service agent who excels at 
        understanding customer needs and routing them efficiently. You identify 
        urgency levels and suggest the best specialist to handle each query.""",
        tools=[classify_query],
        llm=get_default_llm(),
        verbose=True,
        allow_delegation=False,
    )

    # Account Agent - Data retrieval, use mid-tier model
    account_agent = Agent(
        role="Account Information Specialist",
        goal="Access and explain customer account information accurately",
        backstory="""You are an account specialist with 8 years of experience. 
        You retrieve customer data, explain account activity, and identify any 
        issues that need attention. You present information clearly and highlight 
        anything unusual.""",
        tools=[access_customer_account],
        llm=get_default_llm(),
        verbose=True,
        allow_delegation=False,
    )

    # Resolution Agent - Common problem solving
    resolution_agent = Agent(
        role="Problem Resolution Specialist",
        goal="Resolve common customer issues efficiently using standard procedures",
        backstory="""You are a problem-solving expert who handles routine customer 
        requests like password resets, statement requests, and contact updates. 
        You follow documented procedures, execute actions accurately, and provide 
        clear confirmation to customers.""",
        tools=[execute_account_action, check_knowledge_base],
        llm=get_default_llm(),
        verbose=True,
        allow_delegation=False,
    )

    # Technical Agent - Complex issues, use stronger model
    technical_agent = Agent(
        role="Technical Support Specialist",
        goal="Diagnose and resolve technical issues with banking systems and applications",
        backstory="""You are a senior technical support engineer with deep knowledge 
        of banking systems, mobile applications, and online platforms. You troubleshoot 
        complex technical problems, provide detailed solutions, and escalate system-wide 
        issues when necessary.""",
        tools=[check_knowledge_base],
        llm=get_default_llm(),
        verbose=True,
        allow_delegation=False,
    )

    # Manager Agent - Coordination and decision-making, use best model
    manager_agent = Agent(
        role="Customer Service Manager",
        goal="Coordinate specialists to resolve customer queries efficiently and ensure quality",
        backstory="""You are an experienced customer service manager who oversees 
        a team of specialists. You assess situations, delegate tasks appropriately, 
        make escalation decisions, and ensure customers receive excellent service. 
        You balance efficiency with quality and know when to escalate to human staff.""",
        tools=[],  # Manager coordinates but doesn't execute actions directly
        llm=get_default_llm(),
        verbose=True,
        allow_delegation=True,  # This makes it a manager
    )

    return {
        "intake": intake_agent,
        "account": account_agent,
        "resolution": resolution_agent,
        "technical": technical_agent,
        "manager": manager_agent,
    }
