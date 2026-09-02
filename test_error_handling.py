from crawler import crawl
from checks.error_handling import check_error_handling

target = "http://localhost/DVWA/"
pages, forms = crawl(target)
findings = check_error_handling(target, forms)

if findings:
    print(f"\n===== VulnScan Error Handling Report =====\n")
    for f in findings:
        print(f"[{f['severity']}] {f['type']}")
        print(f"  Payload: {f['payload']}")
        print(f"  Signature matched: {f['signature']}")
        print(f"  URL: {f['url']}\n")
else:
   print(f"\nForms tested: {len(forms)}")
   for f in forms:
       print(f" - {f}")