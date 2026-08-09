\# VulnScan — Lightweight Web Vulnerability Scanner



> Enterprise SIEM tools like Splunk and Nessus cost thousands per year. \*\*VulnScan\*\* is a lightweight, open-source web vulnerability scanner that detects security issues in real time, classifies severity, and generates professional reports—the core SOC workflow, built from scratch in Python.



\---



\## 🎯 Problem Statement



Web vulnerability scanning is a critical part of cybersecurity, but professional tools (Burp Suite Pro, Nessus, Shodan) are expensive and overkill for small businesses and startups. VulnScan addresses this gap by providing:



\- \*\*Automated vulnerability detection\*\* targeting OWASP Top 10 categories

\- \*\*Professional reporting\*\* with severity classification and remediation guidance

\- \*\*Web-based dashboard\*\* for visualizing findings

\- \*\*Zero dependencies\*\* on commercial tools or infrastructure



This project demonstrates the full lifecycle of security tool development: recon (crawling) → detection (checks) → analysis (storage) → reporting (CLI + web UI).



\---



\## ✨ Features



\### Core Scanning Modules

\- \*\*Web Crawler\*\* — Discovers pages and forms via BFS, respects scope boundaries

\- \*\*Security Headers Checker\*\* — Detects missing CSP, HSTS, X-Frame-Options, X-Content-Type-Options

\- \*\*Exposed Files Scanner\*\* — Identifies publicly accessible sensitive paths (/.git, /.env, /admin, etc.)

\- \*\*Outdated JS Library Detector\*\* — Flags known-vulnerable JavaScript library versions

\- \*\*SQL Injection Prober\*\* — Tests form fields with SQLi payloads (error-based, boolean-based)

\- \*\*XSS Vulnerability Detector\*\* — Submits test payloads, detects reflected XSS



\### Storage \& Reporting

\- \*\*SQLite Database\*\* — Persistent findings storage, queryable by severity/type

\- \*\*CLI Report Generator\*\* — Generates professional Markdown reports

\- \*\*PDF Export\*\* — Download findings as formatted PDF



\### Web Dashboard

\- \*\*Risk Score Gauge\*\* — Visual 0-100 risk assessment

\- \*\*Real-time Charts\*\* — Severity distribution (donut), findings by type (bar)

\- \*\*Interactive Findings Table\*\* — Sortable, filterable by severity

\- \*\*Detail Modals\*\* — Click any finding to see full description \& recommendations

\- \*\*Dark Mode UI\*\* — Professional, polished aesthetic

\- \*\*Quick Stats\*\* — Most common issue, highest severity, scan duration



\---



\## 🏗️ Architecture



┌─────────────────────────────────────────────────────────┐

│ VulnScan Pipeline │

└─────────────────────────────────────────────────────────┘



INPUT

└─> Target URL (http://localhost/DVWA/)

DETECTION ENGINE (checks/ folder)

├─> crawler.py ─> discovers pages/forms

├─> headers.py ─> checks security headers

├─> exposed\_files.py ─> scans for sensitive files

├─> outdated\_js.py ─> detects old libraries

├─> sqli.py ─> tests for SQL injection

└─> xss.py ─> probes for XSS

STORAGE LAYER

└─> db.py ─> SQLite (vulnscan.db)

findings table: id, target\_url, check\_type, severity,

description, recommendation, timestamp

REPORTING LAYER

├─> report.py ─> generates Markdown reports

├─> cli.py ─> orchestrates full pipeline

└─> dashboard/app.py ─> Flask web server

OUTPUT

├─> vulnscan\_report.md ─> CLI report (downloadable)

├─> vulnscan.db ─> persistent findings

└─> http://localhost:5000 ─> web dashboard (real-time)



\---



\## 📋 Setup \& Installation



\### Prerequisites

\- \*\*OS:\*\* Windows 10+, macOS, or Linux

\- \*\*Python:\*\* 3.10+ (with pip)

\- \*\*Node.js:\*\* 18+ (for Juice Shop target, optional)

\- \*\*RAM:\*\* 8GB minimum (4GB for basic usage)



\### Step 1: Clone the Repository



```bash

git clone https://github.com/rudransh-v/web\_vulnscan\_project.git

cd web\_vulnscan\_project/vulnscan

```



\### Step 2: Create Virtual Environment



```bash

python -m venv venv

source venv/bin/activate  # On Windows: venv\\Scripts\\Activate.ps1

```



\### Step 3: Install Dependencies



```bash

pip install requests beautifulsoup4 flask reportlab

```



\### Step 4: Set Up Target (DVWA)



Install XAMPP and DVWA:

1\. Download XAMPP from apachefriends.org

2\. Start Apache and MySQL

3\. Clone DVWA into `C:\\xampp\\htdocs\\DVWA`

4\. Set security level to "Low" at `http://localhost/DVWA/security.php`



\*(For testing with your own site, modify target URLs in `cli.py`)\*



\---



\## 🚀 Usage



\### Run Full Scanner Pipeline



```bash

python cli.py --target http://localhost/DVWA/

```



This will:

1\. Crawl the target

2\. Run all 6 security checks

3\. Store findings in SQLite

4\. Generate `vulnscan\_report.md`

5\. Print summary to console



\*\*Expected output:\*\*

============================================================

VulnScan - Web Vulnerability Scanner



Target: http://localhost/DVWA/



\[\*] Crawling target...

Found 1 pages and 1 forms



\[\*] Checking security headers...

Found 4 issues



\[\*] Scanning for exposed files...

Found 3 exposed files



\[\*] Checking for outdated JavaScript libraries...

Found 0 outdated libraries



\[\*] Testing for XSS vulnerabilities...

Found 0 XSS vulnerabilities



============================================================

Scan Complete!



Total Findings: 7



\[\*] Generating report...

Report saved to vulnscan\_report.md



\### View CLI Report



```bash

cat vulnscan\_report.md

```



\### Launch Web Dashboard



```bash

python dashboard/app.py

```



Then open browser to: \*\*http://localhost:5000\*\*



\---



\## 📊 Dashboard Features



\### Summary Metrics

\- \*\*Risk Score Gauge\*\* — Calculates 0-100 risk based on finding severity

\- \*\*Quick Stats\*\* — Most common issue, highest severity found, scan duration

\- \*\*Severity Cards\*\* — Total findings, breakdown by Critical/High/Medium/Low



\### Interactive Charts

\- \*\*Severity Distribution\*\* (Donut chart) — Visual breakdown of findings by severity

\- \*\*Findings by Type\*\* (Bar chart) — Count of each vulnerability type discovered



\### Findings Table

\- \*\*Sortable Columns\*\* — Click headers to sort

\- \*\*Filter by Severity\*\* — Click severity cards or filter buttons to narrow results

\- \*\*Detail Modal\*\* — Click "Details →" to see full finding information

\- \*\*PDF Export\*\* — Download findings as formatted PDF report



\---



\## 🔍 Example Scan Results



When run against DVWA (Low security level), VulnScan typically detects:



| Type | Count | Severity | Example |

|------|-------|----------|---------|

| Missing Security Headers | 4 | Medium/Low | CSP, HSTS, X-Frame-Options, X-Content-Type-Options |

| Exposed Files | 3 | High/Medium | /.git/config, /robots.txt, /.git/ |

| Outdated JS Libraries | 0-2 | Medium | Old jQuery/Bootstrap versions |

| SQL Injection | 0-1 | Critical | Login form vulnerable to SQLi |

| XSS Vulnerabilities | 0-1 | High | Form fields reflect unescaped input |



\*\*Total findings:\*\* 7-11 depending on DVWA configuration



\---



\## 📈 What This Project Demonstrates



\### Security Knowledge

\- Web application vulnerability types (OWASP Top 10)

\- Attack signatures and payloads

\- Risk assessment and severity classification

\- Incident response workflow (detect → classify → report → remediate)



\### Software Engineering

\- Full-stack application development (backend + frontend)

\- Modular architecture (reusable scanner modules)

\- Database design and querying (SQLite)

\- RESTful API design (Flask endpoints)

\- Web UI/UX (professional dark-mode dashboard)



\### DevOps \& Deployment

\- Version control (Git/GitHub)

\- Python virtual environments

\- Dependency management (pip)

\- Documentation and README best practices



\### Real-World Skills

\- Working with third-party libraries (requests, BeautifulSoup, Flask)

\- Debugging and troubleshooting

\- Testing and validation

\- Performance optimization (rate-limiting, timeouts)



\---



\## 🧠 What I Learned



\### Technical Insights

1\. \*\*HTTP Response Analysis\*\* — Understanding status codes, headers, and content to detect vulnerabilities

2\. \*\*Web Crawling Complexity\*\* — Breadth-first search, scope control, timeout handling

3\. \*\*Security Best Practices\*\* — Input validation, output encoding, CSRF token handling

4\. \*\*Database Design\*\* — Schema normalization, querying, persistence across sessions

5\. \*\*Web UI Frameworks\*\* — Flask routing, Jinja2 templating, Chart.js integration



\### Soft Skills

1\. \*\*Project Planning\*\* — 10-day sprint structure with incremental deliverables

2\. \*\*Documentation\*\* — Writing clear README, commit messages, code comments

3\. \*\*User-Centered Design\*\* — Building a dashboard teachers/recruiters would understand

4\. \*\*Problem-Solving\*\* — Debugging environment issues (PATH, file locks, imports)



\### Security Lessons

1\. \*\*Defense-in-Depth\*\* — Multiple layers (headers + file exposure + injection testing)

2\. \*\*Severity Matters\*\* — Not all findings are equal; risk scoring guides priorities

3\. \*\*Automation at Scale\*\* — Manual pentesting doesn't scale; tools like this enable it



\---



\## 🚀 Future Enhancements



\### Phase 2 (Stretch Goals)

\- \[ ] Authenticated scanning (login to DVWA, test protected endpoints)

\- \[ ] Stored XSS detection (longer test, state management)

\- \[ ] TLS/SSL certificate validation (expired certs, weak ciphers)

\- \[ ] CVE database integration (live NVD lookups for outdated libraries)

\- \[ ] Scan scheduling (recurring scans at intervals)

\- \[ ] Email/Slack notifications on critical findings



\### Phase 3 (Production)

\- \[ ] PostgreSQL backend (scales beyond SQLite)

\- \[ ] Kubernetes deployment (containerized scanner)

\- \[ ] Multi-target scanning (parallel execution)

\- \[ ] User authentication (role-based access)

\- \[ ] Compliance reporting (OWASP, PCI-DSS templates)

\- \[ ] API-driven architecture (separate backend/frontend)



\---

\## 📸 Evidence Screenshots



\### 1. Web Dashboard — Complete View

!\[Dashboard Complete](06\_dashboard\_complete\_view.png)

Risk score gauge (39/100)...



\### 2. Dashboard — Filtered Results

!\[Dashboard Filtered](03\_dashboard\_filtered\_high.png)

Interactive filtering...



\### 3. Finding Details Modal

!\[Finding Details](04\_dashboard\_modal\_details.png)

Click any finding...



\### 4. PDF Export

!\[PDF Report](05\_dashboard\_pdf\_export.png)

Generate professional PDF...



\## 🛠️ Technology Stack



| Component | Technology | Purpose |

|-----------|-----------|---------|

| \*\*Backend\*\* | Python 3.14 | Core scanning logic |

| \*\*CLI\*\* | Python argparse | Command-line interface |

| \*\*Web Server\*\* | Flask | REST API \& web server |

| \*\*Database\*\* | SQLite | Findings storage |

| \*\*Frontend\*\* | HTML/CSS/JS | Dashboard UI |

| \*\*Charts\*\* | Chart.js | Data visualization |

| \*\*Reports\*\* | ReportLab | PDF generation |

| \*\*Libraries\*\* | requests, BeautifulSoup4 | HTTP \& HTML parsing |

| \*\*Version Control\*\* | Git/GitHub | Code repository |



\---



\## 📝 Project Timeline



| Day | Milestone | Status |

|-----|-----------|--------|

| 1-2 | Core crawler + headers checker | ✅ Done |

| 3-4 | Exposed files + outdated JS | ✅ Done |

| 5-6 | SQLi + XSS probers | ✅ Done |

| 7 | Database + CLI pipeline | ✅ Done |

| 8 | Web dashboard + charts | ✅ Done |

| 9 | End-to-end testing + evidence | ✅ Done |

| 10 | Documentation + final push | ✅ Done |



\---



\## 🎓 How to Use This for Your Viva



\### 2-3 Minute Walkthrough



\*\*Part 1: Problem (30 seconds)\*\*

> "Professional vulnerability scanners cost thousands per year. I built VulnScan to demonstrate the core workflow: automated detection, severity classification, and professional reporting. This project covers the full security lifecycle I learned in my internship."



\*\*Part 2: Technical Demo (90 seconds)\*\*

1\. Show CLI running: `python cli.py --target http://localhost/DVWA/`

2\. Point out: crawler → checks → database → report

3\. Open dashboard: `python dashboard/app.py`

4\. Show risk score gauge, charts, findings table

5\. Click a finding to show modal

6\. Click "Export PDF" to show report generation

7\. Test filtering by severity



\*\*Part 3: Learning (30 seconds)\*\*

> "This project taught me: (1) how real security tools work, (2) full-stack development with Python/Flask, and (3) how to scope and execute a complex project in a fixed timeline. The dashboard is what makes it professional-grade — it's not just a script, it's a tool someone would actually use."



\---



\## 📚 References \& Resources



\- OWASP Top 10: https://owasp.org/www-project-top-ten/

\- DVWA: https://github.com/digininja/DVWA

\- Flask Documentation: https://flask.palletsprojects.com/

\- Chart.js: https://www.chartjs.org/

\- ReportLab: https://www.reportlab.com/



\---



\## 📄 License



MIT License — Free for educational and personal use.



\---



\## 👤 Author



\*\*Rudransh V\*\*  

3rd Year Computer Science Student  

Cybersecurity Focus



GitHub: \[@rudransh-v](https://github.com/rudransh-v)



\---



\## 🙏 Acknowledgments



\- InternPe Cybersecurity Internship (Weeks 1-4 learning foundation)

\- OWASP for vulnerability frameworks

\- Open-source community (requests, Flask, Chart.js, ReportLab)



\---



\*\*Last Updated:\*\* August 9, 2026  

\*\*Version:\*\* 1.0 (MVP Complete)



