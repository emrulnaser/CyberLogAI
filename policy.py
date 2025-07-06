import re
from collections import OrderedDict

# GDPR Rule Patterns with priority
GDPR_RULES = OrderedDict([
    ("Article 5 – Principles", [
        "lawfulness", "fairness", "transparency", "purpose limitation", 
        "data minimization", "accuracy", "storage limitation", 
        "integrity", "confidentiality"
    ]),
    ("Article 6 – Lawfulness", [
        "legal basis", "consent", "contract", "legal obligation", 
        "vital interest", "public task", "legitimate interests"
    ]),
    ("Article 7 – Conditions for Consent", [
        "freely given", "informed consent", "withdraw consent", 
        "explicit consent", "unambiguous consent"
    ]),
    ("Article 13 – Information to be Provided", [
        "identity of controller", "contact details", "purposes of processing", 
        "data subject rights", "data retention", "right to lodge a complaint"
    ]),
    ("Article 30 – Records of Processing", [
        "records of processing activities", "data inventory", 
        "processing records"
    ])
])

def check_gdpr_compliance(text):
    results = {}
    for article, keywords in GDPR_RULES.items():
        found_keywords = []
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
                found_keywords.append(kw)
        
        if found_keywords:
            results[article] = {
                "status": "✅ Compliant",
                "found": ", ".join(found_keywords[:3]) + ("..." if len(found_keywords) > 3 else "")
            }
        else:
            results[article] = {
                "status": "❌ Non-compliant",
                "found": "No matching terms"
            }
    
    # Calculate compliance score
    compliant_count = sum(1 for r in results.values() if "✅" in r["status"])
    results["Compliance Score"] = {
        "status": f"{compliant_count}/{len(GDPR_RULES)}",
        "found": f"{int(compliant_count/len(GDPR_RULES)*100)}%"
    }
    
    return results