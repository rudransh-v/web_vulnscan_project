import requests


def check_security_headers(url):
    required_headers = {
        "Content-Security-Policy": {
            "severity": "Medium",
            "description": "Protects against Cross-Site Scripting (XSS).",
            "recommendation": "Configure a Content-Security-Policy header."
        },
        "X-Frame-Options": {
            "severity": "Low",
            "description": "Protects against Clickjacking.",
            "recommendation": "Set X-Frame-Options to DENY or SAMEORIGIN."
        },
        "Strict-Transport-Security": {
            "severity": "Medium",
            "description": "Forces browsers to use HTTPS.",
            "recommendation": "Enable HTTPS and add the HSTS header."
        },
        "X-Content-Type-Options": {
            "severity": "Low",
            "description": "Prevents MIME-type sniffing.",
            "recommendation": "Add X-Content-Type-Options: nosniff."
        }
    }

    findings = []

    try:
        response = requests.get(url, timeout=5)

        for header, info in required_headers.items():
            if header not in response.headers:
                findings.append({
                    "type": "Missing Security Header",
                    "header": header,
                    "severity": info["severity"],
                    "description": info["description"],
                    "recommendation": info["recommendation"]
                })

    except requests.RequestException as e:
        findings.append({
            "type": "Connection Error",
            "header": "",
            "severity": "Critical",
            "description": str(e),
            "recommendation": "Verify the target URL is reachable."
        })

    return findings