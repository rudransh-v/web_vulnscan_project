# VulnScan — Lightweight Web Vulnerability Scanner

A Python-based web vulnerability scanner that detects security issues, classifies severity, and generates reports. Built from scratch as an educational/portfolio project targeting OWASP Top 10 categories.

## Table of Contents
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Architecture](#architecture)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Dashboard Features](#dashboard-features)
- [Example Scan Results](#example-scan-results)
- [Screenshots](#screenshots)
- [What This Demonstrates](#what-this-demonstrates)
- [Tech Stack](#tech-stack)
- [Project Timeline](#project-timeline)
- [Key Learnings](#key-learnings)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)
- [Author](#author)

---

## Problem Statement

- Professional vulnerability scanners (Nessus, Burp Suite Pro) are expensive and overkill for learning/small-scale use
- VulnScan is a lightweight, open-source alternative built to understand OWASP Top 10 detection mechanics
- Provides automated detection, severity classification, and remediation guidance in a single pipeline

---

## Features

**Core Scanning Modules**
- Web crawler — BFS-based, discovers pages and forms within scope
- Security headers checker — flags missing CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- Exposed files scanner — checks for publicly accessible sensitive paths (`.git`, `.env`, `/admin`)
- Outdated JS library detector — flags known-vulnerable JS library versions
- XSS detector — submits test payloads, checks for reflected XSS (runs in CLI pipeline)
- SQL injection prober — error-based and boolean-based SQLi testing (standalone module, not yet wired into the automated CLI pipeline — see [Limitations](#limitations))

**Storage & Reporting**
- SQLite database — persistent findings, queryable by severity/type
- Markdown report generator
- PDF export

**Web Dashboard**
- Risk score gauge (0–100, weighted by severity)
- Severity distribution chart (donut) + findings-by-type chart (bar)
- Filterable, sortable findings table
- Click-through detail modals
- Dark mode UI

---

## Architecture

```
Crawler (discovers pages/forms)
   → Check modules (headers, files, JS, XSS)
   → SQLite database
   → CLI report + Flask dashboard
```

---

## Setup & Installation

**Prerequisites:** Python 3.10+, 8GB RAM minimum

```bash
# 1. Clone
git clone https://github.com/rudransh-v/web_vulnscan_project.git
cd web_vulnscan_project/vulnscan

# 2. Virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install requests beautifulsoup4 flask reportlab

# 4. Set up target (DVWA via XAMPP)
# - Install XAMPP, start Apache + MySQL
# - Clone DVWA into C:\xampp\htdocs\DVWA
# - Set security level to Low at http://localhost/DVWA/security.php
```

---

## Usage

```bash
# Run full scan
python cli.py --target http://localhost/DVWA/

# View report
cat vulnscan_report.md

# Launch dashboard
python dashboard/app.py
# → open http://localhost:5000
```

---

## Dashboard Features

- Risk score gauge + quick stats (most common issue, highest severity, total findings)
- Interactive severity/type charts
- Click severity cards or filter buttons to narrow the findings table
- "Details" button opens a modal with full finding info
- PDF export button

---

## Example Scan Results

Against DVWA (Low security):

| Check | Typical Findings |
|---|---|
| Missing security headers | 4 |
| Exposed files | 3 (`.git/config`, `robots.txt`, `.git/`) |
| Outdated JS libraries | 0–2 |
| Reflected XSS | 0–1 |

**Total (CLI pipeline):** ~7 findings

---

## Screenshots

<img src="06_dashboard_complete_view.png" width="600" alt="Dashboard Overview">
<img src="03_dashboard_filtered_high.png" width="600" alt="Filtered Results">
<img src="04_dashboard_modal_details.png" width="600" alt="Finding Details Modal">
<img src="05_dashboard_pdf_export.png" width="600" alt="PDF Export">

---

## What This Demonstrates

- **Security knowledge** — OWASP Top 10 vulnerability types, severity classification, remediation guidance
- **Software engineering** — full-stack build (Python backend + Flask/JS frontend), modular scanner architecture, SQLite schema design
- **DevOps** — Git/GitHub workflow, virtual environments, dependency management
- **Practical skills** — debugging real environment issues, working with third-party libraries, rate-limiting/timeout handling

---

## Tech Stack

| Layer | Tools |
|---|---|
| Backend | Python 3.14 |
| Web server | Flask |
| Database | SQLite |
| Frontend | HTML / CSS / JS |
| Charts | Chart.js |
| Reports | ReportLab |
| Libraries | requests, BeautifulSoup4 |

---

## Project Timeline

| Days | Work | Status |
|---|---|---|
| 1–2 | Crawler + headers checker | ✅ |
| 3–4 | Exposed files + outdated JS | ✅ |
| 5–6 | SQLi + XSS probers | ✅ |
| 7 | Database + CLI pipeline | ✅ |
| 8 | Web dashboard | ✅ |
| 9 | End-to-end testing + evidence | ✅ |
| 10 | Documentation | ✅ |

---

## Key Learnings

- HTTP response analysis for vulnerability detection
- Web crawling scope control (BFS, depth limits, timeouts)
- CSRF token handling, input validation, output encoding concepts
- SQLite schema design + querying
- Flask routing, Jinja2 templating, Chart.js integration

---

## Limitations

- SQLi module exists but requires an authenticated session (`dvwa_auth.py`) not yet wired into the automated CLI pipeline — runs standalone only
- XSS check only tests unauthenticated/public pages
- No support for JavaScript-rendered SPAs (requests + BeautifulSoup only see static HTML)
- Outdated JS library list is small and manually maintained (5 libraries, no live CVE feed)
- Risk score is a simple weighted sum, not CVSS-based
- No authentication on the dashboard itself — local/demo use only

---

## Future Enhancements

**Phase 2:** Authenticated scanning, stored XSS detection, TLS/SSL checks, CVE database integration, scheduling, notifications

**Phase 3:** PostgreSQL backend, multi-target scanning, dashboard auth, compliance reporting (OWASP/PCI-DSS), API-driven architecture

---

## Author

**Rudransh Vyas** — 3rd Year ECE Student, Cybersecurity Focus
GitHub: [github.com/rudransh-v](https://github.com/rudransh-v)
