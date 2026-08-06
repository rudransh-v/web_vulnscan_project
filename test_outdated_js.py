from checks.outdated_js import check_outdated_js

target = "http://localhost/DVWA/"
findings = check_outdated_js(target)

if findings:
    print(f"\n===== VulnScan Outdated JS Report =====\n")
    for finding in findings:
        print(f"[{finding['severity']}] {finding['library']} {finding['version']}")
        print(f"  Source: {finding['src']}")
        print(f"  Description: {finding['description']}")
        print(f"  Recommendation: {finding['recommendation']}\n")
else:
    print("\nNo outdated JavaScript libraries found.\n")