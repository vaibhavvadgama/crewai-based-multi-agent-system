from crewai import Task


def create_credit_assessment_tasks(agents, application_data):
    """
    Create tasks for parallel credit analysis.
    Financial, industry, and compliance analyses run simultaneously.
    """

    applicant = application_data["applicant"]
    loan_request = application_data["loan_request"]

    # Task 1: Financial Analysis (parallel)
    financial_task = Task(
        description=f"""Conduct comprehensive financial analysis of loan application.
        
        Applicant Data:
        - Annual Income: ${applicant['annual_income']:,}
        - Existing Debt: ${applicant['existing_debt']:,}
        - Assets: ${applicant['assets']:,}
        - Credit Score: {applicant['credit_score']}
        
        Loan Request:
        - Amount: ${loan_request['amount']:,}
        - Purpose: {loan_request['purpose']}
        - Term: {loan_request['term_months']} months
        
        Analyze:
        1. Debt-to-income ratios
        2. Loan-to-value metrics
        3. Affordability assessment
        4. Credit profile evaluation
        5. Risk indicators""",
        expected_output="""Financial analysis report containing:
        - Key financial ratios calculated
        - Debt capacity assessment
        - Credit quality evaluation
        - Financial risk rating (low/medium/high)
        - Recommendation with supporting data""",
        agent=agents["financial"],
    )

    # Task 2: Industry Research (parallel)
    industry_task = Task(
        description=f"""Research industry trends and business viability.
        
        Business Information:
        - Industry: {applicant['industry']}
        - Business Age: {applicant['business_age_years']} years
        - Business Type: {applicant['business_type']}
        
        Analyze:
        1. Industry outlook and growth trends
        2. Sector-specific risks
        3. Business maturity assessment
        4. Competitive environment
        5. Market stability""",
        expected_output="""Industry analysis report containing:
        - Industry outlook (positive/stable/negative)
        - Growth rate and trends
        - Key risk factors
        - Business maturity assessment
        - Sector risk rating""",
        agent=agents["industry"],
    )

    # Task 3: Compliance Check (parallel)
    compliance_task = Task(
        description=f"""Verify compliance with lending policies and regulations.
        
        Review Requirements:
        - Loan amount: ${loan_request['amount']:,}
        - Credit score: {applicant['credit_score']}
        - Income verification: {applicant.get('income_verified', 'Not specified')}
        - Employment verification: {applicant.get('employment_verified', 'Not specified')}
        
        Check:
        1. Minimum credit score requirements
        2. Debt-to-income thresholds
        3. Loan amount approval authorities
        4. Documentation completeness
        5. Regulatory compliance""",
        expected_output="""Compliance review report containing:
        - Compliance status (compliant/conditional/non-compliant)
        - Policy violations identified
        - Warnings and conditions
        - Required approvals
        - Missing documentation""",
        agent=agents["compliance"],
    )

    # Task 4: Final Decision (depends on all parallel tasks)
    decision_task = Task(
        description="""Synthesize all analyses and make final credit decision.
        
        Review findings from:
        - Financial analysis
        - Industry research
        - Compliance check
        
        Make Decision:
        1. Weigh all factors and risks
        2. Consider compensating strengths
        3. Apply credit judgment
        4. Determine: APPROVE, APPROVE_WITH_CONDITIONS, or DECLINE
        5. Provide clear justification
        6. Specify any conditions or monitoring requirements""",
        expected_output="""Credit decision report containing:
        - Final Decision: APPROVE / APPROVE_WITH_CONDITIONS / DECLINE
        - Decision rationale with key factors
        - Risk rating (low/medium/high)
        - Conditions (if approved with conditions)
        - Pricing recommendations (rate, terms)
        - Monitoring requirements""",
        agent=agents["manager"],
        context=[financial_task, industry_task, compliance_task],
    )

    return [financial_task, industry_task, compliance_task, decision_task]
