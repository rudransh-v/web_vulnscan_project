import requests
import time

def check_exposed_files(base_url):
    """
    Scans for commonly exposed sensitive files and directories.
    Returns a list of findings for files that return HTTP 200 (exist).
    """
    
    sensitive_paths = [
        "/admin",
        "/admin.php",
        "/.env",
        "/.git/config",
        "/config.php",
        "/config.php.bak",
        "/backup.zip",
        "/database.sql",
        "/.htaccess",
        "/web.config",
        "/robots.txt",
        "/sitemap.xml",
        "/wp-admin/",
        "/phpmyadmin/",
        "/cpanel/",
        "/.git/",
        "/.svn/",
    ]
    
    findings = []
    
    for path in sensitive_paths:
        # Construct full URL
        test_url = base_url.rstrip('/') + path
        
        try:
            response = requests.get(test_url, timeout=5)
            
            # Flag if file/directory exists (200 OK)
            if response.status_code == 200:
                findings.append({
                    "type": "Exposed Sensitive File/Directory",
                    "path": path,
                    "url": test_url,
                    "status_code": response.status_code,
                    "severity": "High" if ".env" in path or "config" in path.lower() or "backup" in path.lower() else "Medium",
                    "description": f"Sensitive file/directory found at {path}",
                    "recommendation": f"Remove or restrict access to {path}"
                })
        
        except requests.RequestException as e:
            # Skip on connection error, continue with next path
            pass
        
        # Small delay between requests to avoid overwhelming the server
        time.sleep(0.2)
    
    return findings


if __name__ == "__main__":
    # This allows testing the module directly
    target = "http://localhost/DVWA/"
    results = check_exposed_files(target)
    
    if results:
        print(f"\n===== Exposed Files Found =====\n")
        for finding in results:
            print(f"[{finding['severity']}] {finding['path']}")
            print(f"  URL: {finding['url']}")
            print(f"  Status: {finding['status_code']}")
            print(f"  Description: {finding['description']}")
            print(f"  Recommendation: {finding['recommendation']}\n")
    else:
        print("\nNo exposed sensitive files found.\n")