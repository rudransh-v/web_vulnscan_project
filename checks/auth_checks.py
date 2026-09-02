import requests
import time
from bs4 import BeautifulSoup

def check_rate_limiting(base_url, attempts=5):
    findings = []
    login_url = base_url.rstrip('/') + "/login.php"
    session = requests.Session()

    blocked = False
    for i in range(attempts):
        page = session.get(login_url)
        soup = BeautifulSoup(page.text, "html.parser")
        token_input = soup.find("input", {"name": "user_token"})
        token = token_input["value"] if token_input else ""

        resp = session.post(login_url, data={
            "username": "admin",
            "password": f"wrongpass{i}",
            "Login": "Login",
            "user_token": token
        })

        if "blocked" in resp.text.lower() or resp.status_code == 429:
            blocked = True
            break
        time.sleep(0.3)

    if not blocked:
        findings.append({
            "type": "Missing Rate Limiting",
            "severity": "High",
            "description": f"No lockout or delay detected after {attempts} failed login attempts.",
            "recommendation": "Implement account lockout or exponential backoff after repeated failed logins."
        })

    return findings


def check_csrf_tokens(forms):
    findings = []
    for form in forms:
        inputs = form.get("inputs", [])
        method = form.get("method", "get").lower()
        # Only state-changing forms (POST) need CSRF protection
        if method == "post" and not any("token" in (i or "").lower() for i in inputs):
            findings.append({
                "type": "Missing CSRF Protection",
                "severity": "Medium",
                "page": form.get("page"),
                "description": "POST form has no CSRF token field.",
                "recommendation": "Add a per-session CSRF token to all state-changing forms."
            })
    return findings