import requests
from bs4 import BeautifulSoup

def check_xss(url):
    """
    Scans for reflected XSS vulnerabilities by submitting test payloads.
    Returns findings if payload is reflected unescaped in response.
    """
    
    xss_payload = "<script>alert('test')</script>"
    findings = []
    
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all forms on the page
        forms = soup.find_all("form")
        
        for form in forms:
            # Get form action and method
            action = form.get("action", "")
            method = form.get("method", "get").lower()
            
            # Find all input fields
            inputs = form.find_all("input")
            
            # Prepare payload data
            data = {}
            for inp in inputs:
                name = inp.get("name")
                if name:
                    # Inject payload into first text input
                    if inp.get("type") in [None, "text"]:
                        data[name] = xss_payload
                    else:
                        data[name] = inp.get("value", "")
            
            # Construct full URL
            form_url = url.rstrip('/') + "/" + action if action else url
            
            # Submit the form
            if method == "post":
                submit_response = requests.post(form_url, data=data, timeout=5)
            else:
                submit_response = requests.get(form_url, params=data, timeout=5)
            
            # Check if payload is reflected unescaped
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
            "type": "Connection Error",
            "severity": "Critical",
            "payload": "",
            "url": url,
            "description": str(e),
            "recommendation": "Verify the target URL is reachable."
        })
    
    return findings


if __name__ == "__main__":
    target = "http://localhost/DVWA/"
    results = check_xss(target)
    
    if results:
        print("\n===== VulnScan XSS Report =====\n")
        for finding in results:
            print(f"[{finding['severity']}] {finding['type']}")
            print(f"Payload: {finding['payload']}")
            print(f"URL: {finding['url']}")
            print(f"Description: {finding['description']}")
            print(f"Recommendation: {finding['recommendation']}\n")
    else:
        print("\nNo reflected XSS found.\n")