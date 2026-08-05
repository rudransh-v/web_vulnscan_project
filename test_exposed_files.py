from checks.exposed_files import check_exposed_files

target = "http://localhost/DVWA/"
findings = check_exposed_files(target)

if findings:
    print(f"\n===== VulnScan Exposed Files Report =====\n")
    for finding in findings:
        print(f"[{finding['severity']}] {finding['path']}")
        print(f"  URL: {finding['url']}")
        print(f"  Status Code: {finding['status_code']}")
        print(f"  Description: {finding['description']}")
        print(f"  Recommendation: {finding['recommendation']}\n")
else:
    print("\nNo exposed sensitive files found.\n")