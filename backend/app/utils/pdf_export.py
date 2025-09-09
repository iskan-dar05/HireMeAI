from fpdf import FPDF
import os


def save_to_pdf(text, filename="ai_resume.pdf"):
    output_dir = os.path.join("app", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    pdf_path = os.path.join(output_dir, filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(pdf_path)
    return filename  # ✅ return just "ai_resume.pdf"



