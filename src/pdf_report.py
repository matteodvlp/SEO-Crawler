from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_site_pdf_report(
    start_url,
    site_results,
    average_score,
    llm_report,
    output_path="reports/seo_site_report.pdf"
):
    doc = SimpleDocTemplate(output_path, pagesize=A4)

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("SEO Site Audit Report", styles["Title"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph(f"<b>URL iniziale:</b> {start_url}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Score medio:</b> {average_score}/100", styles["BodyText"]))
    story.append(Paragraph(f"<b>Pagine analizzate:</b> {len(site_results)}", styles["BodyText"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Commento generale", styles["Heading2"]))
    story.append(Paragraph(llm_report["summary"], styles["BodyText"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Punti di forza", styles["Heading2"]))
    for strength in llm_report.get("strengths", []):
        story.append(Paragraph(f"• {strength}", styles["BodyText"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Priorità di intervento", styles["Heading2"]))
    for index, priority in enumerate(llm_report["priorities"], start=1):
        story.append(Paragraph(f"<b>{index}.</b> {priority}", styles["BodyText"]))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 20))
    story.append(Paragraph("Risultati per pagina", styles["Heading2"]))

    table_data = [
        ["URL", "Score", "Problemi"]
    ]

    for result in site_results:
        issues = ", ".join(result["score_data"]["issues"])

        table_data.append([
               Paragraph(result["url"], styles["BodyText"]),
               Paragraph(f"{result['score_data']['score']}/100", styles["BodyText"]),
               Paragraph(
                   issues or "Nessun problema rilevante",
                   styles["BodyText"]
               ),
        ])

    table = Table(table_data, colWidths=[240, 70, 190])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    story.append(table)

    doc.build(story)