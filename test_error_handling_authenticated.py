from dvwa_auth import get_dvwa_session, set_security_low
from checks.error_handling import check_error_handling

session = get_dvwa_session()
set_security_low(session)

target = "http://localhost/DVWA/vulnerabilities/sqli/"
forms = [{
    "page": target,
    "action": "",
    "method": "get",
    "inputs": ["id", "Submit"]
}]

findings = check_error_handling(target, forms, session=session)

if findings:
    print(f"\n===== Authenticated Error Handling Report =====\n")
    for f in findings:
        print(f"[{f['severity']}] {f['type']}")
        print(f"  Payload: {f['payload']}")
        print(f"  Signature matched: {f['signature']}\n")
else:
    print("\nNo verbose error disclosure found.\n")