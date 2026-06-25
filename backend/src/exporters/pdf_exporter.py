from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from models.resume_model import Resume


class PDFExporter:
    """Exports a resume to a PDF file in memory."""

    def export(self, resume: Resume) -> bytes:
        buffer = BytesIO()
        document = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        content = []

        content.append(Paragraph(resume.title, styles["Title"]))
        content.append(Spacer(1, 12))

        if resume.target_role:
            content.append(Paragraph("Cargo Alvo", styles["Heading2"]))
            content.append(Paragraph(resume.target_role, styles["BodyText"]))
            content.append(Spacer(1, 12))

        if resume.content:
            content.append(Paragraph("Conteúdo do Currículo", styles["Heading2"]))
            content.append(Paragraph(resume.content, styles["BodyText"]))
            content.append(Spacer(1, 12))

        content.append(Paragraph("Versão", styles["Heading2"]))
        content.append(Paragraph(str(resume.version), styles["BodyText"]))
        document.build(content)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes
