from crewai import Task


def create_credit_assessment_tasks(agents, application_data):
    """
    Create tasks for hierarchical credit assessment with HITL integration.
    """

    applicant = application_data["applicant"]
    loan_request = application_data["loan_request"]

    # -----------------------------
    # Task 1: Financial Analysis
    # -----------------------------
    financial_task = Task(
        description=f"""
        Conduct comprehensive financial analysis of loan application.

        Applicant Data:
        - Name: {applicant['name']}
        - Annual Income: ${applicant['annual_income']:,}
        - Existing Debt: ${applicant['existing_debt']:,}
        - Assets: ${applicant['assets']:,}
        - Credit Score: {applicant['credit_score']}

        Loan Request:
        - Amount: ${loan_request['amount']:,}
        - Purpose: {loan_request['purpose']}
        - Term: {loan_request['term_months']} months

        Analyze:
        1. Debt-to-income ratio
        2. Loan-to-value implications
        3. Cash flow affordability
        4. Credit strength assessment
        5. Key financial risks
                """,
        expected_output="""
        Financial analysis report including:
        - Debt-to-income ratio
        - Affordability score
        - Risk rating (LOW/MEDIUM/HIGH)
        - Key strengths and weaknesses
        """,
        agent=agents["financial"],
    )

    # -----------------------------
    # Task 2: Industry Analysis
    # -----------------------------
    industry_task = Task(
        description=f"""
        Evaluate industry risk and business environment.

        Business:
        - Industry: {applicant['industry']}
        - Business Type: {applicant['business_type']}
        - Business Age: {applicant['business_age_years']} years

        Analyze:
        1. Industry growth trends
        2. Competitive pressure
        3. Cyclicality / volatility
        4. Sector-specific risks
        5. Long-term outlook
                """,
        expected_output="""
        Industry report including:
        - Sector outlook (positive/stable/negative)
        - Risk level
        - Growth trend summary
        - Competitive intensity
        """,
        agent=agents["industry"],
    )

    # -----------------------------
    # Task 3: Compliance Check
    # -----------------------------
    compliance_task = Task(
        description=f"""
        Perform lending compliance verification.

        Loan:
        - Amount: ${loan_request['amount']:,}
        - Credit Score: {applicant['credit_score']}

        Checks:
        1. Minimum credit score compliance
        2. Debt-to-income thresholds
        3. Lending authority limits
        4. Documentation completeness
        5. Regulatory constraints
                """,
        expected_output="""
        Compliance report:
        - Status: COMPLIANT / NON-COMPLIANT / CONDITIONAL
        - Violations (if any)
        - Required approvals
        """,
        agent=agents["compliance"],
    )

    # -----------------------------
    # Task 4: HITL Review Package
    # -----------------------------
    hitl_task = Task(
        description="""
        You are preparing a HUMAN REVIEW PACKET for a credit officer.

        Synthesize:
        - Financial analysis
        - Industry analysis
        - Compliance report

        Output MUST be decision-ready for human approval.

        Include:

        1. Executive summary (concise)
        2. Consolidated risk profile
        3. Top risk drivers (max 5)
        4. Mitigating factors
        5. System recommendation (advisory only)
        6. Uncertainties / open questions

        IMPORTANT:
        - Do NOT finalize approval decision
        - Do NOT override human authority
        - This is for HUMAN REVIEW ONLY
                """,
        expected_output="""
        Human review packet:
        - Executive summary
        - Risk synthesis
        - Advisory recommendation
        - Open questions for reviewer
        """,
        agent=agents["manager"],
        context=[financial_task, industry_task, compliance_task],
    )

    # -----------------------------
    # Task 5: Final Decision (post-HITL)
    # -----------------------------
    decision_task = Task(
        description="""
        You are the final Credit Decision Manager.

        You MUST consider:

        1. Financial analysis
        2. Industry analysis
        3. Compliance report
        4. HUMAN DECISION (mandatory input provided externally)

        Human decision is authoritative.

        Rules:
        - Follow human decision unless it violates compliance
        - If override is required, explicitly justify
        - Produce structured credit decision output
                """,
        expected_output="""
        Final credit decision:
        - Final status (APPROVED / DECLINED / CONDITIONAL)
        - Alignment with human decision
        - Risk summary
        - Conditions (if any)
        - Pricing / monitoring recommendations
        """,
        agent=agents["manager"],
        context=[financial_task, industry_task, compliance_task, hitl_task],
    )

    return [financial_task, industry_task, compliance_task, hitl_task, decision_task]
