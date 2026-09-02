import requests
from bs4 import BeautifulSoup

def check_xss(url, session=None):
    requester = session if session else requests
    xss_payload = "<script>alert('test')</script>"
    findings = []
    try:
        response = requester.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")
        for form in forms:
            action = form.get("action", "")
            method = form.get("method", "get").lower()
            inputs = form.find_all("input")
            data = {}
            for inp in inputs:
                name = inp.get("name")
                if name:
                    if inp.get("type") in [None, "text"]:
                        data[name] = xss_payload
                    else:
                        data[name] = inp.get("value", "")
            form_url = url.rstrip('/') + "/" + action if action else url
            if method == "post":
                submit_response = requester.post(form_url, data=data, timeout=5)
            else:
                submit_response = requester.get(form_url, params=data, timeout=5)
            if xss_payload in submit_response.text:
                findings.append({
                    "type": "Reflected XSS",
                    "severity": "High",
                    "payload": xss_payload,
                    "url": form_url,
                    "description": "Input was reflected without sanitization.",
                    "recommendation": "Escape user input before displaying it."
                })
    except requests.RequestException as e:
        findings.append({
            "type": "Connection Error", "severity": "Critical", "payload": "",
            "url": url, "description": str(e),
            "recommendation": "Verify the target URL is reachable."
        })
    return findings