import requests

def check_error_handling(url, forms, session=None):
    requester = session if session else requests
    error_signatures = [
        "Warning:", "Fatal error:", "Notice:", "Deprecated:",
        "mysql_fetch", "SQLSTATE", "ODBC Driver",
        "Traceback (most recent call last)",
        "Microsoft OLE DB Provider",
        "on line", "in C:\\", "in /var/www", "stack trace",
    ]
    malicious_inputs = [
        "'", "\"", "<script>", "../../../etc/passwd",
        "999999999999999999999", "%00", "{{7*7}}",
    ]
    findings = []

    for form in forms:
        action = form.get("action") or ""
        method = form.get("method", "get").lower()
        form_url = url.rstrip('/') + "/" + action if action else url

        for payload in malicious_inputs:
            data = {name: payload for name in form.get("inputs", []) if name}
            if not data:
                continue
            try:
                if method == "post":
                    resp = requester.post(form_url, data=data, timeout=5)
                else:
                    resp = requester.get(form_url, params=data, timeout=5)
            except requests.RequestException:
                continue

            for sig in error_signatures:
                if sig.lower() in resp.text.lower():
                    findings.append({
                        "type": "Verbose Error Disclosure",
                        "severity": "Medium",
                        "payload": payload,
                        "signature": sig,
                        "url": form_url,
                        "description": f"Malformed input triggered a verbose error containing '{sig}'.",
                        "recommendation": "Disable verbose error/debug output in production; use generic error pages."
                    })
                    break

    return findings

