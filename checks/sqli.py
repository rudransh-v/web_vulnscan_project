import requests
import time
from urllib.parse import urljoin

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "'",
    "' OR '1'='1' -- ",
]

SQL_ERROR_SIGNATURES = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
]

def resolve_action_url(page, action):
    if not action or action == "#":
        return page
    return urljoin(page, action)

def check_sqli(base_url, forms, session):
    findings = []
    for form in forms:
        page = form["page"]
        action_url = resolve_action_url(page, form.get("action"))
        method = form.get("method", "get").lower()
        fields = [f for f in form["inputs"] if f and f.lower() != "submit"]

        if not fields:
            continue

        # Baseline request with a harmless value, used to detect bypasses later
        baseline_params = {f: ("1" if f == fields[0] else "Submit") for f in form["inputs"] if f}
        try:
            if method == "get":
                baseline_resp = session.get(action_url, params=baseline_params, timeout=5)
            else:
                baseline_resp = session.post(action_url, data=baseline_params, timeout=5)
            baseline_len = len(baseline_resp.text)
        except requests.RequestException:
            baseline_len = 0

        for field in fields:
            for payload in SQLI_PAYLOADS:
                params = {f: (payload if f == field else "Submit") for f in form["inputs"] if f}
                try:
                    if method == "get":
                        response = session.get(action_url, params=params, timeout=5)
                    else:
                        response = session.post(action_url, data=params, timeout=5)
                except requests.RequestException as e:
                    print(f"Could not reach {action_url}: {e}")
                    continue

                time.sleep(0.2)
                body_lower = response.text.lower()
                error_hit = any(sig in body_lower for sig in SQL_ERROR_SIGNATURES)

                if error_hit:
                    findings.append({
                        "type": "SQL Injection",
                        "field": field,
                        "url": action_url,
                        "method": method,
                        "payload": payload,
                        "severity": "Critical",
                        "description": f"SQL error triggered by payload in field '{field}'",
                        "recommendation": "Use parameterized queries / prepared statements instead of string concatenation."
                    })
                    print(f"[FINDING] SQLi in '{field}' with payload: {payload}")
                elif len(response.text) > baseline_len + 200:
                    findings.append({
                        "type": "SQL Injection (Bypass)",
                        "field": field,
                        "url": action_url,
                        "method": method,
                        "payload": payload,
                        "severity": "Critical",
                        "description": f"Payload in '{field}' returned significantly more data than baseline — likely a logic bypass (e.g. OR '1'='1').",
                        "recommendation": "Use parameterized queries / prepared statements instead of string concatenation."
                    })
                    print(f"[FINDING] Possible SQLi bypass in '{field}' with payload: {payload}")
                else:
                    print(f"Tested '{field}' with: {payload} -> no error detected")

    return findings

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from dvwa_auth import get_dvwa_session, set_security_low

    session = get_dvwa_session()
    set_security_low(session)

    fake_forms = [
        {"page": "http://localhost/DVWA/vulnerabilities/sqli/", "action": "#", "method": "get", "inputs": ["id", "Submit"]}
    ]
    check_sqli("http://localhost/DVWA/", fake_forms, session)