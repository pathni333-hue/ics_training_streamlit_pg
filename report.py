from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import os, datetime

def generate_report_pdf(username, df):
    path = f"/tmp/{username}_training_report.pdf"
    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, 27*cm, f"OT/ICS Cyber Training Report")
    c.setFont("Helvetica", 12)
    c.drawString(2*cm, 26*cm, f"User: {username}")
    c.drawString(2*cm, 25.3*cm, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y = 24*cm
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2*cm, y, "Progress Summary:")
    y -= 0.7*cm
    c.setFont("Helvetica", 11)
    for _, row in df.iterrows():
        c.drawString(2*cm, y, f"{row['timestamp'][:19]} | {row['module']} | Score: {row['score']:.1f}%")
        y -= 0.6*cm
        if y < 2*cm:
            c.showPage()
            y = 27*cm
    c.showPage()
    c.save()
    return path
