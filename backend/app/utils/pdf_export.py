import fitz
import os

OUTPUT_DIR = os.path.join("app", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_to_pdf(new_layout, template_path: str):
    doc = fitz.open(template_path)

    # For now, overwrite text in the first page only
    page = doc[0]

    # ⚠️ Remove old text: optional, if you don’t want overlapping
    # page.clean_contents()

    for block in new_layout:
        x0, y0, x1, y1 = block["bbox"]

        # Remove old text
        rect = fitz.Rect(x0, y0, x1, y1)
        page.add_redact_annot(rect, fill=(1, 1, 1))  # white background
    page.apply_redactions()

    for block in new_layout:
        (x0, y0, x1, y1) = block["bbox"]
        text = block["text"]

        # Insert text at same position
        page.insert_text(
            (x0, y0),
            text,
            fontname="helv",  # fallback font
            fontsize=block.get("size", 11),
            color=(0, 0, 0)  # always black, you can map block["color"]
        )

    # Save file to outputs folder
    output_path = os.path.join(OUTPUT_DIR, "resume_filled.pdf")
    doc.save(output_path)
    doc.close()

    return os.path.basename(output_path)
