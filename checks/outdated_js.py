import requests
import re
from bs4 import BeautifulSoup

def check_outdated_js(url):
    """
    Scans a page for script tags and identifies outdated/vulnerable JavaScript libraries.
    Returns a list of findings for known vulnerable versions.
    """
    
    # Known vulnerable library versions (name: list of vulnerable versions)
    vulnerable_libraries = {
        "jquery": ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9", "1.10", "1.11", "2.0", "2.1"],
        "bootstrap": ["2.0", "2.1", "2.2", "2.3", "3.0", "3.1", "3.2", "3.3"],
        "angular": ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5"],
        "underscore": ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"],
        "moment": ["2.0", "2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9", "2.10"],
    }
    
    findings = []
    
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all script tags
        script_tags = soup.find_all("script")
        
        for script in script_tags:
            src = script.get("src")
            
            # Only check external scripts (with src attribute)
            if src:
                # Extract filename from src
                filename = src.split("/")[-1].lower()
                
                # Check each vulnerable library
                for library, versions in vulnerable_libraries.items():
                    if library in filename:
                        # Extract version using regex (e.g., "1.11.0" from "jquery-1.11.0.min.js")
                        version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', filename)
                        
                        if version_match:
                            version = version_match.group(1)
                            
                            # Check if this version is known to be vulnerable
                            # Simplified: check if major.minor matches any vulnerable version
                            major_minor = '.'.join(version.split('.')[:2])
                            
                            if major_minor in versions:
                                findings.append({
                                    "type": "Outdated JavaScript Library",
                                    "library": library.capitalize(),
                                    "version": version,
                                    "src": src,
                                    "severity": "Medium",
                                    "description": f"{library.capitalize()} {version} is outdated and may contain known vulnerabilities.",
                                    "recommendation": f"Update {library.capitalize()} to the latest stable version."
                                })
    
    except requests.RequestException as e:
        findings.append({
            "type": "Connection Error",
            "library": "",
            "version": "",
            "src": "",
            "severity": "Critical",
            "description": str(e),
            "recommendation": "Verify the target URL is reachable."
        })
    
    return findings


if __name__ == "__main__":
    target = "http://localhost/DVWA/"
    results = check_outdated_js(target)
    
    if results:
        print(f"\n===== Outdated JavaScript Libraries Found =====\n")
        for finding in results:
            print(f"[{finding['severity']}] {finding['library']} {finding['version']}")
            print(f"  Source: {finding['src']}")
            print(f"  Description: {finding['description']}")
            print(f"  Recommendation: {finding['recommendation']}\n")
    else:
        print("\nNo outdated JavaScript libraries found.\n")