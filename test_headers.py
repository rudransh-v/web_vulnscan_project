from checks.headers import check_security_headers

target = "http://localhost"

results = check_security_headers(target)

print("\n===== VulnScan Security Header Report =====\n")

if not results:
    print("No missing security headers found.")
else:
    for finding in results:
        print(f"[{finding['severity']}] {finding['header']}")
        print(f"Description   : {finding['description']}")
        print(f"Recommendation: {finding['recommendation']}")
        print()