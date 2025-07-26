# policy/short_report.py

def run_short_scan(scan_results):
    """
    Generate summary text, total compliance score, and list of key non-compliant issues
    from the full scan results.

    Args:
        scan_results (dict): The full result dictionary from GDPRComplianceChecker.check_compliance().

    Returns:
        dict: A dictionary containing:
            - 'summary_text': Short report summary.
            - 'total_score': Compliance percentage score.
            - 'key_issues': List of non-compliant article titles.
            - 'full_report': The original scan_results for detailed display.
    """
    # The scan_results is already the full report from checker.check_compliance()
    full_report_data = scan_results

    # Extract overall compliance summary
    overall_summary = full_report_data.get("Overall Compliance Summary", {})
    total_score_str = overall_summary.get("score_percentage", "0%")
    total_score = float(total_score_str.replace('%', ''))

    # Identify key non-compliant articles (excluding the overall summary entry)
    key_issues = []
    for article, details in full_report_data.items():
        if article != "Overall Compliance Summary" and not details.get("compliant", False):
            key_issues.append(details.get("title", f"Article {article}"))

    summary_text = (
        f"GDPR Compliance Score: {total_score}%\n"
        f"Non-Compliant Articles: {len(key_issues)}"
    )

    return {
        "summary_text": summary_text,
        "total_score": total_score,
        "key_issues": key_issues,
        "full_report": full_report_data # Pass the full report for template to iterate
    }
