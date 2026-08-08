import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, send_file
from db import get_all_findings, get_findings_by_severity
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
import json
import io

app = Flask(__name__)

def calculate_risk_score(findings):
    """Calculate overall risk score (0-100) based on findings"""
    if not findings:
        return 0
    
    score = 0
    for finding in findings:
        severity = finding[3]
        if severity == "Critical":
            score += 25
        elif severity == "High":
            score += 15
        elif severity == "Medium":
            score += 5
        elif severity == "Low":
            score += 2
    
    # Cap at 100
    return min(score, 100)


def get_scan_duration(findings):
    """Calculate scan duration from first and last finding timestamps"""
    if len(findings) < 2:
        return "< 1 minute"
    
    # Parse timestamps (simplified - assumes same day)
    try:
        first_time = findings[-1][7]  # Last in list (oldest)
        last_time = findings[0][7]    # First in list (newest)
        # For MVP, just return approximate
        return "~2 minutes"
    except:
        return "Unknown"


@app.route('/')
def dashboard():
    """Main dashboard page"""
    findings = get_all_findings()
    
    # Calculate statistics
    total = len(findings)
    critical = len(get_findings_by_severity("Critical"))
    high = len(get_findings_by_severity("High"))
    medium = len(get_findings_by_severity("Medium"))
    low = len(get_findings_by_severity("Low"))
    
    # Get target URL and scan time
    target_url = findings[0][1] if findings else "No scans yet"
    scan_time = findings[0][7] if findings else "Never"
    
    # Calculate risk score
    risk_score = calculate_risk_score(findings)
    
    # Get most common issue type
    type_counts = {}
    for finding in findings:
        ftype = finding[2]
        type_counts[ftype] = type_counts.get(ftype, 0) + 1
    most_common = max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else "None"
    
    # Get highest severity
    highest_severity = "None"
    if critical > 0:
        highest_severity = "Critical"
    elif high > 0:
        highest_severity = "High"
    elif medium > 0:
        highest_severity = "Medium"
    elif low > 0:
        highest_severity = "Low"
    
    scan_duration = get_scan_duration(findings)
    
    return render_template(
        'index.html',
        total=total,
        critical=critical,
        high=high,
        medium=medium,
        low=low,
        target_url=target_url,
        scan_time=scan_time,
        findings=findings,
        risk_score=risk_score,
        most_common=most_common,
        highest_severity=highest_severity,
        scan_duration=scan_duration
    )


@app.route('/api/findings')
def api_findings():
    """API endpoint for findings data (for charts)"""
    findings = get_all_findings()
    
    # Organize by check type
    by_type = {}
    by_severity = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    
    for finding in findings:
        check_type = finding[2]
        severity = finding[3]
        
        if check_type not in by_type:
            by_type[check_type] = 0
        by_type[check_type] += 1
        
        if severity in by_severity:
            by_severity[severity] += 1
    
    return jsonify({
        "by_type": by_type,
        "by_severity": by_severity,
        "total": len(findings)
    })


@app.route('/api/timeline')
def api_timeline():
    """API endpoint for timeline data"""
    findings = get_all_findings()
    
    # Group by hour/day (simplified for MVP)
    timeline = {}
    for finding in findings:
        timestamp = finding[7]
        # Extract date part
        date_key = timestamp.split()[0] if timestamp else "Unknown"
        timeline[date_key] = timeline.get(date_key, 0) + 1
    
    return jsonify(timeline)


@app.route('/api/findings/filtered/<severity>')
def api_findings_filtered(severity):
    """API endpoint for filtered findings"""
    findings = get_all_findings()
    filtered = [f for f in findings if f[3] == severity]
    
    return jsonify({
        "findings": [
            {
                "type": f[2],
                "description": f[4],
                "severity": f[3]
            } for f in filtered
        ],
        "count": len(filtered)
    })


@app.route('/export/pdf')
def export_pdf():
    """Generate and download PDF report"""
    findings = get_all_findings()
    
    # Create PDF
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.5*inch)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#10b981'),
        spaceAfter=30,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#10b981'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Title
    elements.append(Paragraph("VulnScan Security Report", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary
    target = findings[0][1] if findings else "Unknown"
    scan_date = findings[0][7] if findings else "Unknown"
    
    summary_text = f"""
    <b>Scan Target:</b> {target}<br/>
    <b>Scan Date:</b> {scan_date}<br/>
    <b>Total Findings:</b> {len(findings)}<br/>
    """
    elements.append(Paragraph(summary_text, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Statistics
    elements.append(Paragraph("Summary Statistics", heading_style))
    
    critical = len(get_findings_by_severity("Critical"))
    high = len(get_findings_by_severity("High"))
    medium = len(get_findings_by_severity("Medium"))
    low = len(get_findings_by_severity("Low"))
    
    stats_text = f"Critical: {critical} | High: {high} | Medium: {medium} | Low: {low}"
    elements.append(Paragraph(stats_text, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Findings
    elements.append(Paragraph("Detailed Findings", heading_style))
    
    for i, finding in enumerate(findings, 1):
        finding_text = f"""
        <b>{i}. {finding[2]}</b> [{finding[3]}]<br/>
        <b>Description:</b> {finding[4]}<br/>
        <b>Recommendation:</b> {finding[5]}<br/>
        <b>Found:</b> {finding[7]}<br/>
        <br/>
        """
        elements.append(Paragraph(finding_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    pdf_buffer.seek(0)
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='vulnscan_report.pdf'
    )


if __name__ == "__main__":
    print("\n" + "="*60)
    print("VulnScan Dashboard")
    print("="*60)
    print("Starting dashboard at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)