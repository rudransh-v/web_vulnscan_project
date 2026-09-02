from crawler import crawl
from checks.auth_checks import check_rate_limiting, check_csrf_tokens

target = "http://localhost/DVWA/"

print("Testing rate limiting...")
rl_findings = check_rate_limiting(target)
for f in rl_findings:
    print(f"[{f['severity']}] {f['type']}: {f['description']}")

print("\nTesting CSRF tokens...")
pages, forms = crawl(target)
csrf_findings = check_csrf_tokens(forms)
if csrf_findings:
    for f in csrf_findings:
        print(f"[{f['severity']}] {f['type']}: {f['description']}")
else:
    print("No missing CSRF tokens found (or all forms already have token fields).")