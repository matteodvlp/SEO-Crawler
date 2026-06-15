from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def add_paragraph(story, text, style, space_after=8):
    story.append(Paragraph(text, style))
    story.append(Spacer(1, space_after))


def build_table_data(site_results, table_text_style):
    table_data = [["URL", "Score", "Problems"]]

    for result in site_results:
        issues = result["score_data"]["issues"]

        issues_text = "<br/>".join(issues) if issues else "No relevant issues found"

        table_data.append([
            Paragraph(result["url"], table_text_style),
            Paragraph(f"{result['score_data']['score']}/100", table_text_style),
            Paragraph(issues_text, table_text_style),
        ])

    return table_data


def build_results_table(site_results, table_text_style):
    table = Table(
        build_table_data(site_results, table_text_style),
        colWidths=[220, 60, 250],
        repeatRows=1,
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    return table


def generate_site_pdf_report(
    start_url,
    site_results,
    average_score,
    llm_report,
    output_path="reports/seo_site_report.pdf",
):
    doc = SimpleDocTemplate(output_path, pagesize=A4)

    styles = getSampleStyleSheet()

    table_text_style = ParagraphStyle(
        "TableText",
        parent=styles["BodyText"],
        fontSize=8,
        leading=10,
    )

    story = []

    add_paragraph(story, "SEO Site Audit Report", styles["Title"], 16)

    add_paragraph(story, f"<b>Initial URL:</b> {start_url}", styles["BodyText"], 4)
    add_paragraph(story, f"<b>Average score:</b> {average_score}/100", styles["BodyText"], 4)
    add_paragraph(story, f"<b>Pages analyzed:</b> {len(site_results)}", styles["BodyText"], 20)

    add_paragraph(story, "General comment", styles["Heading2"], 8)
    add_paragraph(story, llm_report["summary"], styles["BodyText"], 16)

    add_paragraph(story, "Strengths", styles["Heading2"], 8)
    for strength in llm_report.get("strengths", []):
        add_paragraph(story, f"• {strength}", styles["BodyText"], 4)

    add_paragraph(story, "Priorities", styles["Heading2"], 8)
    for index, priority in enumerate(llm_report["priorities"], start=1):
        add_paragraph(story, f"<b>{index}.</b> {priority}", styles["BodyText"], 4)

    story.append(Spacer(1, 16))
    add_paragraph(story, "Page results", styles["Heading2"], 8)

    story.append(build_results_table(site_results, table_text_style))

    doc.build(story)