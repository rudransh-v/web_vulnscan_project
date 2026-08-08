import sqlite3
from datetime import datetime

def init_db(db_path="vulnscan.db"):
    """
    Initialize the SQLite database and create the findings table.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create findings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_url TEXT NOT NULL,
            check_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            details TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


def save_finding(finding, target_url, db_path="vulnscan.db"):
    """
    Save a single finding to the database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO findings (target_url, check_type, severity, description, recommendation, details)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        target_url,
        finding.get("type", "Unknown"),
        finding.get("severity", "Low"),
        finding.get("description", ""),
        finding.get("recommendation", ""),
        str(finding)  # Store full finding dict as JSON string
    ))
    
    conn.commit()
    conn.close()


def get_all_findings(db_path="vulnscan.db"):
    """
    Retrieve all findings from the database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM findings ORDER BY timestamp DESC")
    findings = cursor.fetchall()
    
    conn.close()
    
    return findings


def get_findings_by_severity(severity, db_path="vulnscan.db"):
    """
    Retrieve findings filtered by severity.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM findings WHERE severity = ? ORDER BY timestamp DESC",
        (severity,)
    )
    findings = cursor.fetchall()
    
    conn.close()
    
    return findings


def clear_findings(db_path="vulnscan.db"):
    """
    Clear all findings from the database (for fresh scans).
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM findings")
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Test database initialization
    init_db()
    print("Database initialized successfully.")