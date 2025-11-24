
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

def create_dummy_pdf(file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    styles = getSampleStyleSheet()
    style = styles['Normal']
    
    # Title
    c.setFont('Helvetica-Bold', 16)
    c.drawString(100, height - 100, "Innovate Corp. - 2024 Annual Report")

    # Executive Summary
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, height - 150, "Executive Summary")
    p = Paragraph("Innovate Corp. demonstrated strong performance in 2024, driven by robust sales in our AI division and expansion into emerging markets. We achieved a record revenue of $1.2 billion, a 15% increase from the previous year. Our strategic initiatives are focused on sustainable growth, technological innovation, and maximizing shareholder value.", style)
    p.wrapOn(c, width - 200, height)
    p.drawOn(c, 100, height - 200)

    # Key KPIs
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, height - 250, "Key KPIs")
    kpis = [
        "Revenue: $1.2 Billion (+15% YoY)",
        "Net Profit Margin: 22%",
        "Customer Acquisition Cost (CAC): $150",
        "Customer Lifetime Value (LTV): $600",
        "Market Share: 25% (+2% YoY)",
    ]
    y = height - 270
    for kpi in kpis:
        c.setFont('Helvetica', 10)
        c.drawString(120, y, f"• {kpi}")
        y -= 20

    # Growth Drivers
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, y - 30, "Growth Drivers")
    y -= 50
    p = Paragraph("Our growth was primarily fueled by the successful launch of 'Synapse 2.0', our next-gen AI platform. Furthermore, our strategic partnerships in the Asia-Pacific region have opened up new revenue streams and customer segments. We continue to invest heavily in R&D to maintain our competitive edge.", style)
    p.wrapOn(c, width - 200, height)
    p.drawOn(c, 100, y)
    y -= p.height + 20

    # Risk Factors
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, y - 30, "Risk Factors")
    y -= 50
    p = Paragraph("We face several risks, including increased competition from agile startups, potential regulatory changes in data privacy, and dependency on key suppliers for our hardware components. The global economic climate also presents uncertainty that could impact enterprise spending.", style)
    p.wrapOn(c, width - 200, height)
    p.drawOn(c, 100, y)
    y -= p.height + 20
    
    # SWOT Analysis
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, y - 30, "SWOT Summary")
    y -= 50
    swot = [
        "Strengths: Strong brand recognition, patent-protected technology, high-margin products.",
        "Weaknesses: High operational costs, slow adoption in legacy industries.",
        "Opportunities: Expansion into healthcare AI, growing demand for automation.",
        "Threats: Intense price competition, cybersecurity threats, talent retention challenges."
    ]
    for item in swot:
        p = Paragraph(item, style)
        p.wrapOn(c, width - 200, height)
        p.drawOn(c, 120, y)
        y -= p.height + 5

    c.save()

if __name__ == "__main__":
    create_dummy_pdf("insightcopilot/data/sample_annual_report.pdf")
