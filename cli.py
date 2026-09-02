import argparse
from db import init_db, save_finding, clear_findings
from report import save_report_to_file
from crawler import crawl
from checks.headers import check_security_headers
from checks.exposed_files import check_exposed_files
from checks.outdated_js import check_outdated_js
from checks.xss import check_xss
from checks.sqli import check_sqli
from checks.error_handling import check_error_handling
from checks.crypto_checks import check_crypto_failures
from checks.auth_checks import check_rate_limiting, check_csrf_tokens
from dvwa_auth import get_dvwa_session, set_security_low


def run_scan(target_url, db_path="vulnscan.db"):
    print(f"\n{'='*60}")
    print(f"VulnScan - Web Vulnerability Scanner")
    print(f"{'='*60}")
    print(f"Target: {target_url}\n")

    init_db(db_path)
    clear_findings(db_path)

    all_findings = []

    # --- Unauthenticated checks (public page) ---
    print("[*] Crawling target...")
    pages, forms = crawl(target_url)
    print(f"    Found {len(pages)} pages and {len(forms)} forms\n")

    print("[*] Checking security headers...")
    header_findings = check_security_headers(target_url)
    all_findings += header_findings
    print(f"    Found {len(header_findings)} issues\n")

    print("[*] Scanning for exposed files...")
    file_findings = check_exposed_files(target_url)
    all_findings += file_findings
    print(f"    Found {len(file_findings)} exposed files\n")

    print("[*] Checking for outdated JavaScript libraries...")
    js_findings = check_outdated_js(target_url)
    all_findings += js_findings
    print(f"    Found {len(js_findings)} outdated libraries\n")

    print("[*] Checking CSRF token presence...")
    csrf_findings = check_csrf_tokens(forms)
    all_findings += csrf_findings
    print(f"    Found {len(csrf_findings)} forms missing CSRF protection\n")

    print("[*] Testing login rate limiting...")
    rate_findings = check_rate_limiting(target_url)
    all_findings += rate_findings
    print(f"    Found {len(rate_findings)} rate-limiting issues\n")

    # --- Authenticated checks (behind DVWA login) ---
    print("[*] Authenticating for deep scan...")
    session = get_dvwa_session(base_url=target_url)
    set_security_low(session, base_url=target_url)
    print("    Session established\n")

    sqli_url = target_url.rstrip('/') + "/vulnerabilities/sqli/"
    xss_url = target_url.rstrip('/') + "/vulnerabilities/xss_r/"

    sqli_forms = [{
        "page": sqli_url, "action": "", "method": "get",
        "inputs": ["id", "Submit"]
    }]

    print("[*] Checking security headers (cookies/crypto) on authenticated session...")
    crypto_findings = check_crypto_failures(sqli_url, session=session)
    all_findings += crypto_findings
    print(f"    Found {len(crypto_findings)} issues\n")

    print("[*] Testing for verbose error disclosure (authenticated)...")
    error_findings = check_error_handling(sqli_url, sqli_forms, session=session)
    all_findings += error_findings
    print(f"    Found {len(error_findings)} issues\n")

    print("[*] Testing for SQL injection...")
    sqli_findings = check_sqli(sqli_url, sqli_forms, session)
    all_findings += sqli_findings
    print(f"    Found {len(sqli_findings)} SQLi issues\n")

    print("[*] Testing for XSS vulnerabilities (authenticated)...")
    xss_findings = check_xss(xss_url, session=session)
    all_findings += xss_findings
    print(f"    Found {len(xss_findings)} XSS vulnerabilities\n")

    # --- Save + report ---
    for finding in all_findings:
        save_finding(finding, target_url, db_path)

    print(f"{'='*60}")
    print(f"Scan Complete!")
    print(f"{'='*60}")
    print(f"Total Findings: {len(all_findings)}\n")

    print("[*] Generating report...")
    save_report_to_file("vulnscan_report.md", db_path)
    print(f"\n[OK] Scan finished. Report saved to vulnscan_report.md\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VulnScan - Lightweight Web Vulnerability Scanner")
    parser.add_argument("--target", required=True, help="Target URL to scan (e.g., http://localhost/DVWA/)")
    parser.add_argument("--db", default="vulnscan.db", help="Path to SQLite database (default: vulnscan.db)")
    args = parser.parse_args()
    run_scan(args.target, args.db)