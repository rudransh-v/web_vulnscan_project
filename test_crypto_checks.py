from checks.crypto_checks import check_crypto_failures

target = "http://localhost/DVWA/"

# add temporarily to test_crypto_checks.py, before the findings check

import requests
resp = requests.get(target)
print("Raw Set-Cookie header(s):")
print(resp.headers.get("Set-Cookie"))
print("\nParsed cookie jar:")
for c in resp.cookies:
    print(c.name, "| secure:", c.secure, "| rest:", c._rest if hasattr(c, '_rest') else "n/a")

findings = check_crypto_failures(target)

if findings:
    print(f"\n===== VulnScan Crypto/Cookie Report =====\n")
    for f in findings:
        print(f"[{f['severity']}] {f['type']}")
        print(f"  Description: {f['description']}")
        print(f"  Recommendation: {f['recommendation']}\n")
else:
    print("\nNo cryptographic/cookie issues found.\n")