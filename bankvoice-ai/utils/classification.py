"""
Banking Complaint and Interaction Classification Module
Keyword-based classification into designated banking categories with priority scoring.
"""

from typing import Dict, List, Tuple


CATEGORIES = {
    "Fraud Complaints": {
        "keywords": [
            "fraud", "unauthorized", "scam", "phishing", "cloned", "stolen",
            "hacked", "suspicious", "imposter", "identity theft", "compromised",
            "skimming", "without permission", "bogus", "cheat", "otp scam"
        ],
        "urgency": "Critical",
        "description": "Potential unauthorized access, account takeover, or fraudulent transactions."
    },
    "Card Issues": {
        "keywords": [
            "card", "debit card", "credit card", "cvv", "atm card", "pin",
            "declined", "blocked", "swallowed", "lost card", "replacement card",
            "chip", "contactless", "expiration", "unblock", "platinum card"
        ],
        "urgency": "High",
        "description": "Debit/credit card operations, chip failures, PIN resets, or blockages."
    },
    "Transaction Issues": {
        "keywords": [
            "transaction", "transfer", "wire", "deposit", "withdrawal", "atm",
            "dispensed", "deducted", "overcharged", "duplicate charge", "duplicate",
            "failed payment", "pending", "refund", "reversal", "swift", "ach",
            "neft", "rtgs", "cash", "debited", "billing cycle"
        ],
        "urgency": "High",
        "description": "Payment discrepancies, duplicate debits, pending transfers, and ATM issues."
    },
    "Loan Issues": {
        "keywords": [
            "loan", "mortgage", "emi", "interest rate", "repayment", "foreclosure",
            "principal", "borrow", "collateral", "refinance", "sanction",
            "disbursement", "debt", "amortization", "auto loan", "home loan"
        ],
        "urgency": "Medium",
        "description": "Inquiries or disputes regarding mortgages, EMI calculations, and loans."
    },
    "Account Issues": {
        "keywords": [
            "account", "locked out", "locked", "login", "portal", "password",
            "balance", "statement", "overdraft", "dormant", "freeze", "kyc",
            "address", "routing number", "joint account", "profile", "regain access"
        ],
        "urgency": "Medium",
        "description": "Account administration, login credentials, KYC updates, and account freezes."
    },
    "General Enquiries": {
        "keywords": [
            "hours", "branch", "customer service", "representative", "information",
            "appointment", "inquire", "enquire", "notary", "policy", "feedback",
            "help", "query", "guidance", "open account", "timing", "compliment",
            "appreciation", "service"
        ],
        "urgency": "Low",
        "description": "General customer service inquiries, branch timing, and account onboarding."
    }
}


def classify_banking_complaint(text: str) -> Dict[str, any]:
    """
    Classify transcript into one of 6 banking complaint categories using weighted keyword matching.
    
    Args:
        text (str): Speech transcript from customer.
        
    Returns:
        dict with:
            - category: str
            - confidence: float (0.0 to 1.0)
            - matched_keywords: List[str]
            - urgency: str ("Critical", "High", "Medium", "Low")
            - description: str
            - all_scores: Dict[str, int]
    """
    if not text or not text.strip():
        return {
            "category": "General Enquiries",
            "confidence": 0.50,
            "matched_keywords": [],
            "urgency": "Low",
            "description": CATEGORIES["General Enquiries"]["description"],
            "all_scores": {cat: 0 for cat in CATEGORIES}
        }

    lowered_text = text.lower()
    category_matches: Dict[str, List[str]] = {}
    category_scores: Dict[str, int] = {}

    for cat_name, cat_info in CATEGORIES.items():
        matched = []
        score = 0
        for kw in cat_info["keywords"]:
            if kw in lowered_text:
                matched.append(kw)
                # Multi-word keywords carry higher specificity weight
                weight = 2 if " " in kw else 1
                score += weight
        category_matches[cat_name] = matched
        category_scores[cat_name] = score

    # Check for Fraud priority: if fraud has matches, prioritize due to regulatory compliance
    if category_scores.get("Fraud Complaints", 0) > 0:
        fraud_matched = category_matches["Fraud Complaints"]
        # If any high-risk fraud keyword is detected
        high_risk_kw = ["fraud", "unauthorized", "scam", "cloned", "stolen", "compromised", "hacked"]
        if any(hk in fraud_matched for hk in high_risk_kw):
            best_cat = "Fraud Complaints"
        else:
            best_cat = max(category_scores, key=category_scores.get)
    else:
        best_cat = max(category_scores, key=category_scores.get)

    highest_score = category_scores[best_cat]

    # If no keywords matched at all, fallback to General Enquiries
    if highest_score == 0:
        best_cat = "General Enquiries"
        confidence = 0.55
        urgency = "Low"
    else:
        # Confidence scaled by matched count
        confidence = min(0.60 + (highest_score * 0.10), 0.99)
        urgency = CATEGORIES[best_cat]["urgency"]

    return {
        "category": best_cat,
        "confidence": round(confidence, 2),
        "matched_keywords": category_matches.get(best_cat, []),
        "urgency": urgency,
        "description": CATEGORIES[best_cat]["description"],
        "all_scores": category_scores
    }

