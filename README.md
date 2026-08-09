\# VulnScan — Lightweight Web Vulnerability Scanner



Enterprise SIEM tools like Splunk and Nessus cost thousands per year. \*\*VulnScan\*\* is a lightweight, open-source web vulnerability scanner that detects security issues in real time, classifies severity, and generates professional reports—the core SOC workflow, built from scratch in Python.



\## Problem Statement



Web vulnerability scanning is critical but expensive. VulnScan addresses this gap by providing automated vulnerability detection targeting OWASP Top 10 categories, professional reporting with severity classification, and a web-based dashboard for visualization.



\## Features



\*\*Core Scanning Modules\*\*

\- Web Crawler — Discovers pages and forms via BFS

\- Security Headers Checker — Detects missing CSP, HSTS, X-Frame-Options

\- Exposed Files Scanner — Identifies publicly accessible sensitive paths

\- Outdated JS Library Detector — Flags known-vulnerable JavaScript versions

\- SQL Injection Prober — Tests form fields with SQLi payloads

\- XSS Vulnerability Detector — Submits test payloads, detects reflected XSS



\*\*Storage \& Reporting\*\*

\- SQLite Database — Persistent findings storage

\- CLI Report Generator — Generates professional Markdown reports

\- PDF Export — Download findings as formatted PDF



\*\*Web Dashboard\*\*

\- Risk Score Gauge — Visual 0-100 risk assessment

\- Real-time Charts — Severity distribution, findings by type

\- Interactive Findings Table — Sortable, filterable by severity

\- Detail Modals — Click findings for full description \& recommendations

\- Dark Mode UI — Professional, polished aesthetic



\## Setup \& Installation



Prerequisites: Python 3.10+, XAMPP (for DVWA target)



Clone and setup:

```bash

git clone https://github.com/rudransh-v/web\_vulnscan\_project.git

cd web\_vulnscan\_project/vulnscan

python -m venv venv

source venv/bin/activate

pip install requests beautifulsoup4 flask reportlab

```



\## Usage



Run full scanner pipeline:

```bash

python cli.py --target http://localhost/DVWA/

```



Launch web dashboard:

```bash

python dashboard/app.py

```



Then open browser to: http://localhost:5000



\## Dashboard Features



\- \*\*Summary Metrics\*\* — Risk score, quick stats, severity cards

\- \*\*Interactive Charts\*\* — Severity distribution, findings by type

\- \*\*Findings Table\*\* — Sortable, filterable by severity

\- \*\*Filter by Severity\*\* — Click severity cards to narrow results

\- \*\*Detail Modal\*\* — Click "Details →" to see full finding information

\- \*\*PDF Export\*\* — Download findings as formatted PDF report



\## Evidence Screenshots



!\[Dashboard Complete](06\_dashboard\_complete\_view.png)



Complete dashboard view showing risk score gauge, charts, and findings table.



!\[Dashboard Filtered](03\_dashboard\_filtered\_high.png)



Interactive filtering by severity level.



!\[Finding Details](04\_dashboard\_modal\_details.png)



Detail modal showing full finding information.



!\[PDF Report](05\_dashboard\_pdf\_export.png)



Professional PDF report generation.



\## What This Project Demonstrates



\*\*Security Knowledge:\*\* Web application vulnerability types (OWASP Top 10), attack signatures, risk assessment, incident response workflow



\*\*Software Engineering:\*\* Full-stack development, modular architecture, database design, RESTful API, web UI/UX



\*\*DevOps \& Deployment:\*\* Version control, Python virtual environments, dependency management



\## Technology Stack



\- Backend: Python 3.14

\- Web Server: Flask

\- Database: SQLite

\- Frontend: HTML/CSS/JavaScript

\- Charts: Chart.js

\- Reports: ReportLab

\- Libraries: requests, BeautifulSoup4



\## Project Timeline



\- Days 1-2: Core crawler + headers checker ✓

\- Days 3-4: Exposed files + outdated JS ✓

\- Days 5-6: SQLi + XSS probers ✓

\- Day 7: Database + CLI pipeline ✓

\- Day 8: Web dashboard + charts ✓

\- Day 9: End-to-end testing + evidence ✓

\- Day 10: Documentation + final push ✓



\## License



MIT License — Free for educational and personal use.



\## Author



\*\*Rudransh V\*\* — 3rd Year Computer Science Student, Cybersecurity Focus



GitHub: \[@rudransh-v](https://github.com/rudransh-v)

