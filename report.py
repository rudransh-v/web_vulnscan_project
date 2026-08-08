from db import get_all_findings, get_findings_by_severity
from datetime import datetime

def generate_markdown_report(db_path="vulnscan.db"):
    """
    Generate a Markdown report from database findings.
    Returns the report as a string.
    """
    
    findings = get_all_findings(db_path)
    
    if not findings:
        return "# VulnScan Report\n\nNo findings.\n"
    
    # Group findings by severity
    severity_order = ["Critical", "High", "Medium", "Low"]
    findings_by_severity = {severity: [] for severity in severity_order}
    
    for finding in findings:
        severity = finding[4]  # severity column
        if severity in findings_by_severity:
            findings_by_severity[severity].append(finding)
    
    # Build report
    report = f"# VulnScan Report\n\n"
    report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Summary
    total = len(findings)
    critical = len(findings_by_severity["Critical"])
    high = len(findings_by_severity["High"])
    medium = len(findings_by_severity["Medium"])
    low = len(findings_by_severity["Low"])
    
    report += f"## Summary\n\n"
    report += f"- **Total Findings:** {total}\n"
    report += f"- **Critical:** {critical}\n"
    report += f"- **High:** {high}\n"
    report += f"- **Medium:** {medium}\n"
    report += f"- **Low:** {low}\n\n"
    
    # Detailed findings
    report += f"## Findings by Severity\n\n"
    
    for severity in severity_order:
        if findings_by_severity[severity]:
            report += f"### {severity} ({len(findings_by_severity[severity])})\n\n"
            
            for finding in findings_by_severity[severity]:
                id_val, target, check_type, sev, desc, rec, details, timestamp = finding
                report += f"**{check_type}**\n\n"
                report += f"- **Target:** {target}\n"
                report += f"- **Description:** {desc}\n"
                report += f"- **Recommendation:** {rec}\n"
                report += f"- **Found:** {timestamp}\n\n"
    
    return report


def save_report_to_file(filename="vulnscan_report.md", db_path="vulnscan.db"):
    """
    Generate report and save to file.
    """
    report = generate_markdown_report(db_path)
    
    with open(filename, 'w') as f:
        f.write(report)
    
    print(f"Report saved to {filename}")


if __name__ == "__main__":
    # Test report generation
    save_report_to_file()