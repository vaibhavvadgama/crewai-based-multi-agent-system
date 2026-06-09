from crewai import Crew, Process
from agent_platform.agents.credit_assessment_agents import (
    create_credit_assessment_agents,
)
from agent_platform.tasks.credit_assessment_tasks import create_credit_assessment_tasks


def assess_credit_application(application_data):
    """
    End-to-end credit assessment with Human-in-the-Loop approval gate.
    """

    print("\n" + "=" * 80)
    print("CREDIT ASSESSMENT PIPELINE STARTED")
    print(f"Applicant: {application_data['applicant']['name']}")
    print(f"Loan Amount: ${application_data['loan_request']['amount']:,}")
    print("=" * 80 + "\n")

    # -----------------------------
    # Step 1: Initialize agents
    # -----------------------------
    agents = create_credit_assessment_agents()

    # -----------------------------
    # Step 2: Build tasks
    # -----------------------------
    tasks = create_credit_assessment_tasks(agents, application_data)

    # -----------------------------
    # Step 3: Run analysis crew
    # -----------------------------
    crew = Crew(
        agents=[
            agents["financial"],
            agents["industry"],
            agents["compliance"],
        ],
        tasks=tasks,
        process=Process.hierarchical,
        manager_llm=agents["manager"].llm,
        verbose=True,
    )

    # Execute analysis + HITL packet
    analysis_result = crew.kickoff()

    # -----------------------------
    # Step 4: HUMAN GATE
    # -----------------------------
    print("\n" + "=" * 80)
    print("HUMAN REVIEW REQUIRED")
    print("=" * 80)
    print(analysis_result)

    decision = (
        input("\nEnter decision (APPROVE / DECLINE / CONDITIONAL): ").strip().upper()
    )
    notes = input("Enter rationale: ").strip()

    human_input = {
        "decision": decision,
        "notes": notes,
    }

    print("\nHuman decision captured:", human_input)

    # -----------------------------
    # Step 5: Final decision crew
    # -----------------------------
    final_prompt = f"""
You are the Credit Decision Manager.

Here is the full analysis:
{analysis_result}

Human decision:
- Decision: {human_input['decision']}
- Notes: {human_input['notes']}

Now produce final structured credit decision report.

Rules:
- Human decision is primary authority
- Only override if compliance violation exists
"""

    final_crew = Crew(
        agents=[agents["manager"]],
        tasks=[tasks[-1]],  # decision_task
        process=Process.sequential,
        verbose=True,
    )

    # Inject human context into task dynamically
    tasks[-1].description += f"\n\nHUMAN INPUT:\n{human_input}"

    final_result = final_crew.kickoff()

    print("\n" + "=" * 80)
    print("FINAL CREDIT DECISION")
    print("=" * 80)
    print(final_result)

    return final_result


if __name__ == "__main__":

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

    assess_credit_application(application)
