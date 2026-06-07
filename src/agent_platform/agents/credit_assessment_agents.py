from crewai import Agent
from agent_platform.llm.llmfactory import get_default_llm
from agent_platform.tools.credit_assessment_tools import (
    analyze_financials,
    research_industry,
    check_compliance,
)


def create_credit_assessment_agents():
    """
    Create specialized credit assessment agents.
    These agents work in parallel under manager coordination.
    """

    financial_analyst = Agent(
        role="Senior Financial Analyst",
        goal="Analyze applicant financial health and calculate credit risk metrics",
        backstory="""You are a seasoned financial analyst with 15 years in commercial 
        lending. You excel at interpreting financial statements, calculating ratios, 
        and assessing borrower capacity. You identify both strengths and concerns in 
        financial profiles and explain them clearly.""",
        tools=[analyze_financials],
        llm=get_default_llm(),
        verbose=True,
        allow_delegation=False,
    )

    industry_researcher = Agent(
        role="Industry Research Analyst",
        goal="Evaluate business sector trends and market position",
        backstory="""You are an industry research specialist who tracks market trends, 
        competitive dynamics, and sector-specific risks. You provide context on whether 
        a business operates in a growing or declining sector and what challenges they face.""",
        tools=[research_industry],
        llm=get_default_llm(),
        verbose=True,
        allow_delegation=False,
    )

    compliance_officer = Agent(
        role="Lending Compliance Officer",
        goal="Ensure loan applications meet regulatory and policy requirements",
        backstory="""You are a compliance specialist who knows lending regulations, 
        internal policies, and documentation requirements inside and out. You identify 
        policy violations, flag missing documentation, and determine approval authority 
        levels. You protect the bank from regulatory risk.""",
        tools=[check_compliance],
        llm=get_default_llm(),
        verbose=True,
        allow_delegation=False,
    )

    credit_manager = Agent(
        role="Credit Decision Manager",
        goal="Synthesize analyses and make sound credit decisions",
        backstory="""You are an experienced credit manager who makes final lending 
        decisions. You review financial analysis, industry research, and compliance 
        findings to make balanced decisions that manage risk while supporting good 
        business opportunities. You explain decisions clearly with supporting rationale.""",
        llm=get_default_llm(),
        verbose=True,
        allow_delegation=True,
    )

    return {
        "financial": financial_analyst,
        "industry": industry_researcher,
        "compliance": compliance_officer,
        "manager": credit_manager,
    }
