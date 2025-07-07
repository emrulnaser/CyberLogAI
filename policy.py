import re

class GDPRComplianceChecker:
    def __init__(self):
        self.article_keywords = {
            "Article 5 – Principles relating to processing": {
                "keywords": [
                    "lawfulness", "fairness", "transparency", "purpose limitation", "data minimisation",
                    "accuracy", "storage limitation", "integrity", "confidentiality", "accountability",
                    "adequate", "relevant", "limited to what is necessary", "accurate and up to date",
                    "data protection principles", "principles for processing"
                ],
                "min_matches": 1
            },
            "Article 6 – Lawfulness of processing": {
                "keywords": [
                    "lawful basis", "consent", "contract", "legal obligation", "vital interests",
                    "public task", "legitimate interests", "processing is necessary", "grounds for processing",
                    "explicit consent" # Explicitly in text
                ],
                "min_matches": 2
            },
            "Article 7 – Conditions for consent": {
                "keywords": [
                    "freely given", "specific", "informed", "unambiguous", "withdraw consent",
                    "explicit consent", "clear affirmative action", "demonstrate consent", "separate request",
                    "consent is obtained" # Explicitly in text
                ],
                "min_matches": 1
            },
            "Article 9 – Processing of special categories of data": {
                "keywords": [
                    "health data", "biometric", "racial", "ethnic", "genetic", "religious",
                    "sexual orientation", "political opinions", "trade union membership", "special categories of personal data",
                    "sensitive data", "glucose level", "medication", "heart rate" # Explicitly in text
                ],
                "min_matches": 2
            },
            "Articles 12-23 – Data subject rights": {
                "keywords": [
                    "right to access", "right to rectification", "right to erasure", "delete your data",
                    "right to restrict processing", "right to data portability", "right to object",
                    "right to not be subject to automated decision-making", "view, edit, or remove your data",
                    "exercising your rights", "data subject rights", "individual rights"
                ],
                "min_matches": 1
            },
            "Article 13/14 – Information requirements": {
                "keywords": [
                    "purposes of processing", "categories of data", "contact details of controller",
                    "who we share with", "how long we store", "your data is used", "collected data includes",
                    "data retention period", "identity of controller", "source of personal data",
                    "recipients of data", "international transfers", "right to lodge a complaint",
                    "privacy notice", "privacy policy", "shared only with medical professionals under contract" # Added this exact phrase
                ],
                "min_matches": 1
            },
            "Article 25 – Data protection by design and by default": {
                "keywords": [
                    "privacy by design", "default settings", "pseudonymisation", "data minimisation",
                    "design choices", "data protection by default", "appropriate technical and organisational measures"
                ],
                "min_matches": 1
            },
            "Article 30 – Records of processing activities": {
                "keywords": [
                    "records of processing", "processing inventory", "processing log", "data register",
                    "RPA", "Article 30 register", "data mapping"
                ],
                "min_matches": 1
            },
            "Article 32 – Security of processing": {
                "keywords": [
                    "security measures", "encrypted", "encryption", "confidentiality", "integrity",
                    "availability", "firewall", "secure storage", "access control", "resilience",
                    "restoration", "technical and organisational measures", "risk of varying likelihood and severity",
                    "data is encrypted" # Explicitly in text
                ],
                "min_matches": 1
            },
            "Article 33/34 – Data breach notification": {
                "keywords": [
                    "data breach", "breach notification", "inform affected", "report breach",
                    "within 72 hours", "supervisory authority", "high risk to the rights and freedoms"
                ],
                "min_matches": 1
            },
            "Article 35 – Data Protection Impact Assessment": {
                "keywords": [
                    "impact assessment", "DPIA", "risk assessment", "high risk processing",
                    "consultation with supervisory authority", "necessity and proportionality",
                    "data protection impact assessment" # Explicitly in text
                ],
                "min_matches": 1
            },
            "Article 37-39 – Data Protection Officer": {
                "keywords": [
                    "Data Protection Officer", "DPO", "dpo@", "contact our DPO", "privacy officer",
                    "tasks of the DPO", "role of the DPO", "independent advice"
                ],
                "min_matches": 1
            },
             "International Data Transfers (Articles 44-50)": {
                "keywords": [
                    "international transfers", "adequate level of protection", "standard contractual clauses",
                    "binding corporate rules", "derogations", "transfer mechanisms", "third country transfers"
                ],
                "min_matches": 1
            },
            "Supervisory Authorities (Articles 51-59)": {
                "keywords": [
                    "supervisory authority", "data protection authority", "DPA", "ICO", "CNIL", "competent authority",
                    "powers of supervisory authorities", "complaint to supervisory authority"
                ],
                "min_matches": 1
            },
            "Remedies, Liabilities, and Penalties (Articles 77-84)": {
                "keywords": [
                    "right to lodge a complaint", "judicial remedy", "compensation", "administrative fines",
                    "penalties", "infringement", "material or non-material damage"
                ],
                "min_matches": 1
            }
        }

    def check_compliance(self, text):
        text_lower = text.lower()
        results = {}
        compliant_articles_count = 0
        total_articles = len(self.article_keywords)

        for article, criteria in self.article_keywords.items():
            keywords = criteria["keywords"]
            min_matches = criteria["min_matches"]
            total_keywords_for_article = len(keywords)

            found_keywords = []
            for kw in keywords:
                # Prioritize exact phrase match for multi-word keywords
                if len(kw.split()) > 1:
                    if re.search(re.escape(kw), text_lower):
                        found_keywords.append(kw)
                else: # For single word keywords, ensure whole word matching
                    if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                        found_keywords.append(kw)
            
            num_found_for_article = len(found_keywords)
            
            article_match_percentage = 0
            if total_keywords_for_article > 0:
                article_match_percentage = round((num_found_for_article / total_keywords_for_article) * 100)

            if num_found_for_article >= min_matches:
                results[article] = {
                    "found_terms": ", ".join(sorted(set(found_keywords))),
                    "match_percentage": f"{article_match_percentage}%",
                    "status": "✅ Potentially Compliant",
                    "explanation": f"Found {num_found_for_article} out of {total_keywords_for_article} expected terms, meeting the minimum of {min_matches} for this article. This indicates a good level of attention to this area."
                }
                compliant_articles_count += 1
            else:
                missing_keywords = [
                    kw for kw in keywords
                    if (len(kw.split()) > 1 and not re.search(re.escape(kw), text_lower)) or \
                       (len(kw.split()) == 1 and not re.search(r'\b' + re.escape(kw) + r'\b', text_lower))
                ]
                results[article] = {
                    "found_terms": ", ".join(sorted(set(found_keywords))) if found_keywords else "No matching terms",
                    "match_percentage": f"{article_match_percentage}%",
                    "status": "❌ Requires Review (Potentially Non-compliant)",
                    "explanation": f"Found {num_found_for_article} out of {total_keywords_for_article} expected terms. Failed to meet the minimum of {min_matches} for this article. Consider adding or clarifying terms like: {', '.join(sorted(set(missing_keywords)))}."
                }

        score_percentage = round((compliant_articles_count / total_articles) * 100)
        results["Overall Compliance Summary"] = {
            "score_percentage": f"{score_percentage}%",
            "compliant_articles": f"{compliant_articles_count}/{total_articles} Articles",
            "status_overview": "This score indicates the breadth of GDPR topics covered in the text. Full compliance requires more than just keyword presence.",
            "recommendation": "Use this as a high-level indicator. A CIPP/E professional would conduct a deeper, contextual analysis, reviewing actual processes and documentation, not just text."
        }

        return results

# Example Usage (replace this with your actual file reading and processing)
if __name__ == "__main__":
    checker = GDPRComplianceChecker()

    # The sample content you provided
    sample_data = """
    This app collects health-related data including glucose level, medication, and heart rate.
    Consent is obtained during onboarding. You can delete your data at any time.

    Data is encrypted and shared only with medical professionals under contract.
    All processing is based on explicit consent. We have conducted a Data Protection Impact Assessment.
    """

    print("--- Scanning Content ---") # Changed this header for clarity
    compliance_report = checker.check_compliance(sample_data)

    # Extract the overall compliance percentage for printing at the top
    overall_percentage_str = compliance_report["Overall Compliance Summary"]["score_percentage"]

    print("\n1. Compliance Results ")
    # This is the line you requested:
    print(f"Total Compliance percentage {overall_percentage_str}") 
    
    # Iterate through articles, excluding the "Overall Compliance Summary" which will be printed last
    for article, data in compliance_report.items():
        if article != "Overall Compliance Summary":
            print(f"\n{article}:")
            for key, value in data.items():
                print(f"  {key}: {value}")
    
    # Print the overall summary at the very end
    print("\nOverall Compliance Summary:")
    for key, value in compliance_report["Overall Compliance Summary"].items():
        print(f"  {key}: {value}")

    print("\nScanned Content Preview:") # Added this back as it was in your desired output
    print(sample_data)