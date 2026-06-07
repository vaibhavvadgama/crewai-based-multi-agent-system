from crewai.tools import tool
import json


@tool("Analyze Financial Statements")
def analyze_financials(applicant_data: dict) -> dict:
    """
    Analyze applicant financial data and calculate key metrics.
    Returns financial ratios, cash flow analysis, and risk indicators.
    """
    income = applicant_data.get("annual_income", 0)
    existing_debt = applicant_data.get("existing_debt", 0)
    requested_amount = applicant_data.get("requested_amount", 0)
    assets = applicant_data.get("assets", 0)
    credit_score = applicant_data.get("credit_score", 0)

    # Calculate key ratios
    total_debt = existing_debt + requested_amount
    debt_to_income = (total_debt / income * 100) if income > 0 else 999
    loan_to_value = (requested_amount / assets * 100) if assets > 0 else 999

    # Assess financial health
    if debt_to_income < 36:
        debt_assessment = "Strong - Low debt burden"
    elif debt_to_income < 43:
        debt_assessment = "Acceptable - Moderate debt burden"
    else:
        debt_assessment = "Concerning - High debt burden"

    # Credit score evaluation
    if credit_score >= 750:
        credit_assessment = "Excellent"
    elif credit_score >= 700:
        credit_assessment = "Good"
    elif credit_score >= 650:
        credit_assessment = "Fair"
    else:
        credit_assessment = "Poor"

    return {
        "debt_to_income_ratio": round(debt_to_income, 2),
        "loan_to_value_ratio": round(loan_to_value, 2),
        "debt_assessment": debt_assessment,
        "credit_score": credit_score,
        "credit_assessment": credit_assessment,
        "monthly_debt_service": round(total_debt * 0.05 / 12, 2),  # Assuming 5% rate
        "affordability_score": 100 - min(debt_to_income, 100),
        "recommendation": (
            "approve" if debt_to_income < 43 and credit_score >= 650 else "review"
        ),
    }


@tool("Research Industry Trends")
def research_industry(industry: str, business_age_years: int) -> dict:
    """
    Analyze industry trends and business sector risk.
    Returns industry outlook, risk factors, and market position.
    """
    # Simulated industry research
    industry_data = {
        "technology": {
            "outlook": "positive",
            "growth_rate": 8.5,
            "risk_level": "medium",
            "key_risks": ["rapid change", "competition", "talent acquisition"],
            "stability_score": 70,
        },
        "healthcare": {
            "outlook": "positive",
            "growth_rate": 6.2,
            "risk_level": "low",
            "key_risks": ["regulatory changes", "reimbursement rates"],
            "stability_score": 85,
        },
        "retail": {
            "outlook": "mixed",
            "growth_rate": 2.1,
            "risk_level": "high",
            "key_risks": ["e-commerce competition", "consumer spending", "margins"],
            "stability_score": 55,
        },
        "manufacturing": {
            "outlook": "stable",
            "growth_rate": 3.5,
            "risk_level": "medium",
            "key_risks": ["supply chain", "automation", "global competition"],
            "stability_score": 70,
        },
        "default": {
            "outlook": "neutral",
            "growth_rate": 3.0,
            "risk_level": "medium",
            "key_risks": ["economic conditions", "competition"],
            "stability_score": 65,
        },
    }

    data = industry_data.get(industry.lower(), industry_data["default"])

    # Business age factor
    if business_age_years < 2:
        maturity = "startup"
        maturity_risk = "high"
    elif business_age_years < 5:
        maturity = "early_stage"
        maturity_risk = "medium"
    else:
        maturity = "established"
        maturity_risk = "low"

    data["business_maturity"] = maturity
    data["maturity_risk"] = maturity_risk

    return data


@tool("Check Lending Compliance")
def check_compliance(applicant_data: dict, loan_terms: dict) -> dict:
    """
    Validate loan application against lending policies and regulations.
    Returns compliance status, policy violations, and approval requirements.
    """
    violations = []
    warnings = []
    approvals_needed = []

    # Check loan amount limits
    requested = loan_terms.get("amount", 0)
    if requested > 500000:
        approvals_needed.append("Executive approval required for loans over $500K")

    # Check credit score requirements
    credit_score = applicant_data.get("credit_score", 0)
    if credit_score < 620:
        violations.append("Credit score below minimum threshold (620)")
    elif credit_score < 680:
        warnings.append(
            "Credit score in review range - additional documentation required"
        )

    # Check debt-to-income
    income = applicant_data.get("annual_income", 0)
    existing_debt = applicant_data.get("existing_debt", 0)
    dti = (existing_debt + requested) / income * 100 if income > 0 else 999
    if dti > 50:
        violations.append(f"Debt-to-income ratio ({dti:.1f}%) exceeds maximum (50%)")
    elif dti > 43:
        warnings.append(
            f"Debt-to-income ratio ({dti:.1f}%) requires compensating factors"
        )

    # Check documentation requirements
    if applicant_data.get("income_verified", False) == False:
        violations.append("Income verification required")

    if applicant_data.get("employment_verified", False) == False:
        warnings.append("Employment verification recommended")

    # Determine compliance status
    if len(violations) > 0:
        status = "non_compliant"
        can_approve = False
    elif len(warnings) > 0:
        status = "conditional"
        can_approve = True
    else:
        status = "compliant"
        can_approve = True

    return {
        "compliance_status": status,
        "can_approve": can_approve,
        "violations": violations,
        "warnings": warnings,
        "approvals_needed": approvals_needed,
        "additional_documentation": warnings + violations,
    }
