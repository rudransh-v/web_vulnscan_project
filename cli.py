import argparse
from db import init_db, save_finding, clear_findings
from report import save_report_to_file
from crawler import crawl
from checks.headers import check_security_headers
from checks.exposed_files import check_exposed_files
from checks.outdated_js import check_outdated_js
from checks.sqli import check_sqli
from checks.xss import check_xss


def run_scan(target_url, db_path="vulnscan.db"):
    """
    Run the complete VulnScan pipeline against a target.
    """
    print(f"\n{'='*60}")
    print(f"VulnScan - Web Vulnerability Scanner")
    print(f"{'='*60}")
    print(f"Target: {target_url}\n")
    
    # Initialize database
    init_db(db_path)
    clear_findings(db_path)
    
    # Step 1: Crawl the target
    print("[*] Crawling target...")
    pages, forms = crawl(target_url)
    print(f"    Found {len(pages)} pages and {len(forms)} forms\n")
    
    # Step 2: Security headers check
    print("[*] Checking security headers...")
    header_findings = check_security_headers(target_url)
    for finding in header_findings:
        save_finding(finding, target_url, db_path)
    print(f"    Found {len(header_findings)} issues\n")
    
    # Step 3: Exposed files check
    print("[*] Scanning for exposed files...")
    file_findings = check_exposed_files(target_url)
    for finding in file_findings:
        save_finding(finding, target_url, db_path)
    print(f"    Found {len(file_findings)} exposed files\n")
    
    # Step 4: Outdated JS check
    print("[*] Checking for outdated JavaScript libraries...")
    js_findings = check_outdated_js(target_url)
    for finding in js_findings:
        save_finding(finding, target_url, db_path)
    print(f"    Found {len(js_findings)} outdated libraries\n")
    
    # Step 5: SQLi check
    # print("[*] Testing for SQL injection...")
    # sqli_findings = check_sqli(target_url, forms, None)
    # for finding in sqli_findings:
    #     save_finding(finding, target_url, db_path)
    # print(f"    Found {len(sqli_findings)} potential SQLi vulnerabilities\n")

    sqli_findings = []  # Placeholder for now
    
    # Step 6: XSS check
    print("[*] Testing for XSS vulnerabilities...")
    xss_findings = check_xss(target_url)
    for finding in xss_findings:
        save_finding(finding, target_url, db_path)
    print(f"    Found {len(xss_findings)} XSS vulnerabilities\n")
    
    # Summary
    total_findings = len(header_findings) + len(file_findings) + len(js_findings) + len(sqli_findings) + len(xss_findings)
    
    print(f"{'='*60}")
    print(f"Scan Complete!")
    print(f"{'='*60}")
    print(f"Total Findings: {total_findings}\n")
    
    # Generate report
    print("[*] Generating report...")
    save_report_to_file("vulnscan_report.md", db_path)
    
    print(f"\n[✓] Scan finished. Report saved to vulnscan_report.md\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="VulnScan - Lightweight Web Vulnerability Scanner"
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target URL to scan (e.g., http://localhost/DVWA/)"
    )
    parser.add_argument(
        "--db",
        default="vulnscan.db",
        help="Path to SQLite database (default: vulnscan.db)"
    )
    
    args = parser.parse_args()
    
    run_scan(args.target, args.db)