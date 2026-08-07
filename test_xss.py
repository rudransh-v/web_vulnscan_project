from checks.xss import check_xss

results = check_xss()

print("\n===== VulnScan XSS Report =====\n")

if results:
    for finding in results:
        print(f"[{finding['severity']}] {finding['type']}")
        print(f"Payload: {finding['payload']}")
        print(f"Description: {finding['description']}")
        print(f"Recommendation: {finding['recommendation']}\n")
else:
    print("No reflected XSS found.")