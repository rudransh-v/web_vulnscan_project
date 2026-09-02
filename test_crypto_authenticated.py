from dvwa_auth import get_dvwa_session, set_security_low
from checks.crypto_checks import check_crypto_failures

session = get_dvwa_session()
set_security_low(session)

target = "http://localhost/DVWA/vulnerabilities/sqli/"
findings = check_crypto_failures(target, session=session)

if findings:
    print(f"\n===== Authenticated Crypto/Cookie Report =====\n")
    for f in findings:
        print(f"[{f['severity']}] {f['type']}")
        print(f"  Description: {f['description']}\n")
else:
    print("\nNo issues found (unexpected — DVWA should have a PHPSESSID by now).\n")