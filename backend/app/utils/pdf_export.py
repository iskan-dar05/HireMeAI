from fpdf import FPDF
import os
import textwrap

def clean_text(s: str) -> str:
    return ''.join(ch if ord(ch) < 65535 else '?' for ch in s)


def force_break(line: str, max_len: int = 80) -> str:
    """Force-break any overlong word into chunks that fit."""
    words = []
    for word in line.split():
        if len(word) > max_len:
            # break it into safe chunks
            for i in range(0, len(word), max_len):
                words.append(word[i:i+max_len])
        else:
            words.append(word)
    return " ".join(words)


def save_to_pdf(text, filename="ai_resume.pdf"):
    output_dir = os.path.join("app", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    pdf_path = os.path.join(output_dir, filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(left=10, top=10, right=10)

    # ✅ Use a Unicode font
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    
    for line in text.split("\n"):
        line = clean_text(line)
        line = force_break(line, max_len=80)  # <-- new step
        wrapped = textwrap.fill(line, width=80, break_long_words=True, break_on_hyphens=False)
        pdf.multi_cell(0, 10, wrapped)

    pdf.output(pdf_path)
    return filename
