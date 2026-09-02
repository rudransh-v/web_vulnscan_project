# VulnScan Report

**Generated:** 2026-09-02 10:13:26

## Summary

- **Total Findings:** 16
- **Critical:** 3
- **High:** 3
- **Medium:** 8
- **Low:** 2

## Findings by Severity

### Critical (3)

**SQL Injection (Bypass)**

- **Target:** http://localhost/DVWA/
- **Description:** Payload in 'id' returned significantly more data than baseline — likely a logic bypass (e.g. OR '1'='1').
- **Recommendation:** Use parameterized queries / prepared statements instead of string concatenation.
- **Found:** 2026-09-02 04:35:07

**SQL Injection**

- **Target:** http://localhost/DVWA/
- **Description:** SQL error triggered by payload in field 'id'
- **Recommendation:** Use parameterized queries / prepared statements instead of string concatenation.
- **Found:** 2026-09-02 04:35:07

**SQL Injection (Bypass)**

- **Target:** http://localhost/DVWA/
- **Description:** Payload in 'id' returned significantly more data than baseline — likely a logic bypass (e.g. OR '1'='1').
- **Recommendation:** Use parameterized queries / prepared statements instead of string concatenation.
- **Found:** 2026-09-02 04:35:07

### High (3)

**Exposed Sensitive File/Directory**

- **Target:** http://localhost/DVWA/
- **Description:** Sensitive file/directory found at /.git/config
- **Recommendation:** Remove or restrict access to /.git/config
- **Found:** 2026-09-02 04:35:07

**Missing Rate Limiting**

- **Target:** http://localhost/DVWA/
- **Description:** No lockout or delay detected after 5 failed login attempts.
- **Recommendation:** Implement account lockout or exponential backoff after repeated failed logins.
- **Found:** 2026-09-02 04:35:07

**Reflected XSS**

- **Target:** http://localhost/DVWA/
- **Description:** Input was reflected without sanitization.
- **Recommendation:** Escape user input before displaying it.
- **Found:** 2026-09-02 04:35:07

### Medium (8)

**Missing Security Header**

- **Target:** http://localhost/DVWA/
- **Description:** Protects against Cross-Site Scripting (XSS).
- **Recommendation:** Configure a Content-Security-Policy header.
- **Found:** 2026-09-02 04:35:07

**Missing Security Header**

- **Target:** http://localhost/DVWA/
- **Description:** Forces browsers to use HTTPS.
- **Recommendation:** Enable HTTPS and add the HSTS header.
- **Found:** 2026-09-02 04:35:07

**Exposed Sensitive File/Directory**

- **Target:** http://localhost/DVWA/
- **Description:** Sensitive file/directory found at /robots.txt
- **Recommendation:** Remove or restrict access to /robots.txt
- **Found:** 2026-09-02 04:35:07

**Exposed Sensitive File/Directory**

- **Target:** http://localhost/DVWA/
- **Description:** Sensitive file/directory found at /.git/
- **Recommendation:** Remove or restrict access to /.git/
- **Found:** 2026-09-02 04:35:07

**Missing HTTPS**

- **Target:** http://localhost/DVWA/
- **Description:** Site is served over plain HTTP instead of HTTPS.
- **Recommendation:** Enable TLS and redirect all HTTP traffic to HTTPS.
- **Found:** 2026-09-02 04:35:07

**Insecure Cookie Configuration**

- **Target:** http://localhost/DVWA/
- **Description:** Cookie 'security' is missing Secure flag, missing HttpOnly flag, missing SameSite attribute.
- **Recommendation:** Set Secure, HttpOnly, and SameSite attributes on all session cookies.
- **Found:** 2026-09-02 04:35:07

**Insecure Cookie Configuration**

- **Target:** http://localhost/DVWA/
- **Description:** Cookie 'PHPSESSID' is missing Secure flag, missing HttpOnly flag, missing SameSite attribute.
- **Recommendation:** Set Secure, HttpOnly, and SameSite attributes on all session cookies.
- **Found:** 2026-09-02 04:35:07

**Verbose Error Disclosure**

- **Target:** http://localhost/DVWA/
- **Description:** Malformed input triggered a verbose error containing 'on line'.
- **Recommendation:** Disable verbose error/debug output in production; use generic error pages.
- **Found:** 2026-09-02 04:35:07

### Low (2)

**Missing Security Header**

- **Target:** http://localhost/DVWA/
- **Description:** Protects against Clickjacking.
- **Recommendation:** Set X-Frame-Options to DENY or SAMEORIGIN.
- **Found:** 2026-09-02 04:35:07

**Missing Security Header**

- **Target:** http://localhost/DVWA/
- **Description:** Prevents MIME-type sniffing.
- **Recommendation:** Add X-Content-Type-Options: nosniff.
- **Found:** 2026-09-02 04:35:07

