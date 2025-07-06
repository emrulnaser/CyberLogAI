import re

# 🔍 GDPR Rule Patterns (add near the bottom)
gdpr_rules = {
    "Article 5 – Principles": [
        "lawfulness", "fairness", "transparency", "purpose limitation", "data minimization",
        "accuracy", "storage limitation", "integrity", "confidentiality"
    ],
    "Article 6 – Lawfulness of Processing": [
        "legal basis", "consent", "contract", "legal obligation", "vital interest", "public task", "legitimate interests"
    ],
    "Article 7 – Consent": [
        "freely given", "informed consent", "withdraw consent", "explicit consent"
    ],
    "Article 13 – Information to be Provided": [
        "identity of controller", "contact details", "purposes of processing", "data subject rights",
        "data retention", "right to lodge a complaint"
    ]
}

# 🔍 GDPR Compliance Check Function
def check_gdpr_compliance(text):
    results = {}
    for article, keywords in gdpr_rules.items():
        found = any(re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE) for kw in keywords)
        results[article] = "✅ Present" if found else "❌ Missing"
    return results

# ✅ Optional: Local Test Run Block
if __name__ == "__main__":
    # Local test with a sample policy text file
    with open("sample_policy.txt", "r", encoding="utf-8") as f:
        policy_text = f.read()
    
    report = check_gdpr_compliance(policy_text)
    for article, status in report.items():
        print(f"{article}: {status}")
