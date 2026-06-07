from crewai.tools import tool
import json
from datetime import datetime, timedelta


@tool("Classify Customer Query")
def classify_query(query_text: str) -> dict:
    """
    Classify customer query by category and urgency.
    Returns category, urgency level, and suggested routing.
    """
    query_lower = query_text.lower()

    # Category classification
    if any(word in query_lower for word in ["password", "login", "access", "locked"]):
        category = "authentication"
        urgency = "high"
    elif any(word in query_lower for word in ["statement", "balance", "transaction"]):
        category = "account_inquiry"
        urgency = "medium"
    elif any(word in query_lower for word in ["fraud", "unauthorized", "suspicious"]):
        category = "fraud_concern"
        urgency = "critical"
    elif any(word in query_lower for word in ["loan", "credit", "rate", "application"]):
        category = "credit_services"
        urgency = "medium"
    elif any(
        word in query_lower for word in ["technical", "error", "bug", "not working"]
    ):
        category = "technical_issue"
        urgency = "high"
    else:
        category = "general_inquiry"
        urgency = "low"

    # Routing suggestion
    routing = {
        "authentication": "resolution_agent",
        "account_inquiry": "account_agent",
        "fraud_concern": "escalate_to_fraud_team",
        "credit_services": "credit_specialist",
        "technical_issue": "technical_agent",
        "general_inquiry": "resolution_agent",
    }

    return {
        "category": category,
        "urgency": urgency,
        "suggested_routing": routing.get(category, "manager_review"),
        "keywords_detected": [
            word
            for word in ["password", "fraud", "error", "loan"]
            if word in query_lower
        ],
    }


@tool("Access Customer Account")
def access_customer_account(customer_id: str) -> dict:
    """
    Retrieve customer account information and recent activity.
    Returns account status, balance, recent transactions, and alerts.
    """
    # Simulated account data
    accounts = {
        "CUST12345": {
            "customer_id": "CUST12345",
            "name": "John Smith",
            "account_type": "Premium Checking",
            "status": "active",
            "balance": 15420.50,
            "last_login": "2024-03-24T10:15:00Z",
            "recent_transactions": [
                {
                    "date": "2024-03-25",
                    "description": "ATM Withdrawal",
                    "amount": -200.00,
                },
                {
                    "date": "2024-03-24",
                    "description": "Salary Deposit",
                    "amount": 5500.00,
                },
                {
                    "date": "2024-03-23",
                    "description": "Online Purchase",
                    "amount": -89.99,
                },
            ],
            "alerts": [],
            "customer_since": "2019-06-15",
            "contact_email": "john.smith@email.com",
            "contact_phone": "+1-555-0123",
        },
        "CUST67890": {
            "customer_id": "CUST67890",
            "name": "Sarah Johnson",
            "account_type": "Business Checking",
            "status": "active",
            "balance": 45230.75,
            "last_login": "2024-03-25T14:30:00Z",
            "recent_transactions": [
                {
                    "date": "2024-03-25",
                    "description": "Wire Transfer",
                    "amount": -15000.00,
                },
                {"date": "2024-03-24", "description": "Deposit", "amount": 22000.00},
            ],
            "alerts": ["High-value wire transfer pending verification"],
            "customer_since": "2021-03-10",
            "contact_email": "sarah.j@business.com",
            "contact_phone": "+1-555-0456",
        },
    }

    return accounts.get(customer_id, {"error": "Customer not found"})


@tool("Execute Account Action")
def execute_account_action(
    customer_id: str, action: str, parameters: dict = None
) -> dict:
    """
    Execute common account actions like password reset, statement generation, etc.
    Returns confirmation and next steps.
    """
    if parameters is None:
        parameters = {}

    valid_actions = {
        "reset_password": "Password reset initiated. Temporary password sent to registered email.",
        "request_statement": f"Statement for period {parameters.get('period', 'last 30 days')} generated and sent to email.",
        "update_contact": "Contact information update request submitted. Verification required.",
        "report_fraud": "Fraud report filed. Case number FR-2024-12345 created. Fraud team will contact within 2 hours.",
        "dispute_transaction": "Transaction dispute initiated. Reference number DT-2024-67890. Resolution within 10 business days.",
    }

    if action not in valid_actions:
        return {
            "success": False,
            "message": f"Unknown action: {action}",
            "available_actions": list(valid_actions.keys()),
        }

    return {
        "success": True,
        "action": action,
        "customer_id": customer_id,
        "message": valid_actions[action],
        "timestamp": datetime.now().isoformat(),
        "reference_number": f"REF-{hash(action + customer_id) % 1000000}",
    }


@tool("Check Knowledge Base")
def check_knowledge_base(query: str) -> dict:
    """
    Search internal knowledge base for solutions and documentation.
    Returns relevant articles and step-by-step solutions.
    """
    # Simulated knowledge base
    knowledge_base = {
        "password reset": {
            "article_id": "KB001",
            "title": "How to Reset Your Password",
            "solution": "1. Click 'Forgot Password' on login page\n2. Enter registered email\n3. Check email for reset link\n4. Create new password (min 12 characters)",
            "related_articles": [
                "KB002: Account Security",
                "KB015: Two-Factor Authentication",
            ],
        },
        "transaction dispute": {
            "article_id": "KB045",
            "title": "Disputing a Transaction",
            "solution": "1. Identify the disputed transaction\n2. Gather supporting documentation\n3. Submit dispute form within 60 days\n4. Wait for investigation (5-10 business days)",
            "related_articles": [
                "KB046: Fraud Protection",
                "KB047: Chargeback Process",
            ],
        },
        "mobile app error": {
            "article_id": "KB123",
            "title": "Troubleshooting Mobile App Issues",
            "solution": "1. Clear app cache\n2. Update to latest version\n3. Check internet connection\n4. Restart device\n5. Reinstall if problem persists",
            "related_articles": ["KB124: App Features", "KB125: Mobile Security"],
        },
    }

    query_lower = query.lower()
    for key, article in knowledge_base.items():
        if key in query_lower:
            return article

    return {
        "article_id": None,
        "title": "No exact match found",
        "solution": "Please contact customer support for personalized assistance.",
        "related_articles": [],
    }
