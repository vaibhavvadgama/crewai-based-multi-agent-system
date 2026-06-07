from crewai import Crew, Process
from agent_platform.agents.credit_assessment_agents import create_credit_assessment_agents
from agent_platform.tasks.credit_assessment_tasks import create_credit_assessment_tasks


def assess_credit_application(application_data):
    """
    Process credit application using hierarchical workflow with parallel analysis.
    """
    print(f"\n{'='*80}")
    print(f"CREDIT ASSESSMENT - Loan Application Review")
    print(f"Applicant: {application_data['applicant']['name']}")
    print(f"Requested Amount: ${application_data['loan_request']['amount']:,}")
    print(f"{'='*80}\n")

    # Create agents
    agents = create_credit_assessment_agents()

    # Create tasks
    tasks = create_credit_assessment_tasks(agents, application_data)

    # Create hierarchical crew
    crew = Crew(
        agents=[agents["financial"], agents["industry"], agents["compliance"]],
        tasks=tasks,
        process=Process.hierarchical,
        manager_llm=agents["manager"].llm,
        verbose=True,
    )

    # Execute
    try:
        result = crew.kickoff()

        print(f"\n{'='*80}")
        print("CREDIT DECISION")
        print(f"{'='*80}\n")
        print(result)

        return result

    except Exception as e:
        print(f"\nError in credit assessment: {str(e)}")
        return None


if __name__ == "__main__":
    # Sample loan application
    application = {
        "applicant": {
            "name": "TechStart Solutions Inc",
            "industry": "technology",
            "business_type": "LLC",
            "business_age_years": 3,
            "annual_income": 850000,
            "existing_debt": 120000,
            "assets": 450000,
            "credit_score": 710,
            "income_verified": True,
            "employment_verified": True,
        },
        "loan_request": {
            "amount": 250000,
            "purpose": "equipment_purchase",
            "term_months": 60,
        },
    }

    result = assess_credit_application(application)
