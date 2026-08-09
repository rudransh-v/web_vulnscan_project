\# VulnScan - Lightweight Web Vulnerability Scanner



Enterprise vulnerability scanning tools cost thousands per year. VulnScan is a lightweight, open-source web vulnerability scanner built in Python.



\## What It Does



\- Crawls websites to find pages and forms

\- Checks for security headers

\- Scans for exposed sensitive files

\- Detects outdated JavaScript libraries

\- Tests for SQL injection vulnerabilities

\- Detects XSS vulnerabilities

\- Stores findings in SQLite database

\- Generates reports and PDF exports

\- Professional web dashboard with charts and filtering



\## Setup



Install Python 3.10+, then:



1\. Clone: git clone https://github.com/rudransh-v/web\_vulnscan\_project.git

2\. Create venv: python -m venv venv

3\. Activate: venv\\Scripts\\Activate.ps1

4\. Install: pip install requests beautifulsoup4 flask reportlab



\## Usage



Run scanner: python cli.py --target http://localhost/DVWA/



View dashboard: python dashboard/app.py



Then open http://localhost:5000



\## Screenshots



Complete Dashboard



!\[Dashboard](06\_dashboard\_complete\_view.png)



Filtered Results



!\[Filtered](03\_dashboard\_filtered\_high.png)



Finding Details



!\[Details](04\_dashboard\_modal\_details.png)



PDF Report



!\[Report](05\_dashboard\_pdf\_export.png)



\## Author



Rudransh V - 3rd Year CS Student



GitHub: rudransh-v

