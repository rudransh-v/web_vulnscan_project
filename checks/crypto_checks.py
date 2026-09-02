import requests
from urllib.parse import urlparse

def check_crypto_failures(url, session=None):
    findings = []
    requester = session if session else requests

    parsed = urlparse(url)
    if parsed.scheme == "http":
        findings.append({
            "type": "Missing HTTPS",
            "severity": "Medium",
            "description": "Site is served over plain HTTP instead of HTTPS.",
            "recommendation": "Enable TLS and redirect all HTTP traffic to HTTPS."
        })

    try:
        resp = requester.get(url, timeout=5)
        # Check the persistent cookie jar, not just this response's Set-Cookie
        jar = session.cookies if session else resp.cookies
        for cookie in jar:
            issues = []
            if not cookie.secure:
                issues.append("missing Secure flag")
            if not cookie.has_nonstandard_attr("HttpOnly"):
                issues.append("missing HttpOnly flag")
            if not cookie.get_nonstandard_attr("SameSite"):
                issues.append("missing SameSite attribute")
            if issues:
                findings.append({
                    "type": "Insecure Cookie Configuration",
                    "severity": "Medium",
                    "cookie_name": cookie.name,
                    "description": f"Cookie '{cookie.name}' is {', '.join(issues)}.",
                    "recommendation": "Set Secure, HttpOnly, and SameSite attributes on all session cookies."
                })
    except requests.RequestException as e:
        findings.append({
            "type": "Connection Error", "severity": "Critical",
            "description": str(e), "recommendation": "Verify the target URL is reachable."
        })

    return findings