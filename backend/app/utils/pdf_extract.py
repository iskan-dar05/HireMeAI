import fitz
import json

def rect_to_list(rect):
        if rect is None:
                return None
        return [rect.x0, rect.y0, rect.x1, rect.y1]


def extract_layout_from_pdf(pdf_path):
        doc = fitz.open(pdf_path)
        layout_data = []

        for page_index, page in enumerate(doc):
                page_dict = {
                        "page_number": page_index + 1,
                        "width": page.rect.width,
                        "height": page.rect.height,
                        "blocks": [],
                        "images": [],
                        "drawings": [],
                }

                # Extract text blocks (with positions, fonts, etc.)
                text_dict = page.get_text("rawdict")
                for block in text_dict["blocks"]:
                        if "lines" in block:
                                for line in block["lines"]:
                                        for span in line["spans"]:
                                                page_dict["blocks"].append({
                                                        "text": span.get("text", ""),
                                                        "font": span.get("font", ""),
                                                        "size": span.get("size", 0),
                                                        "color": span.get("color", 0),
                                                        "bbox": span.get("bbox", []),
                                                        "ascender": span.get("ascender", 0),
                                                        "descender": span.get("descender", 0),
                                                        "origin": span.get("origin", [0, 0]),
                                                        "char_space": span.get("char_space", 0),
                                                        "word_space": span.get("word_space", 0),
                                                })
                for img_index, img in enumerate(page.get_images(full=True)):
                        xref = img[0]
                        image_name = img[7]
                        base_image = doc.extract_image(xref)
                        try:
                                bbox = page.get_image_bbox(image_name)
                                bbox_coords = [bbox.x0, bbox.y0, bbox.x1, bbox.y1]
                        except:
                                bbox_coords = None
                        page_dict["images"].append({
                                "index": img_index,
                                "xref": xref,
                                "width": base_image["width"],
                                "height": base_image["height"],
                                "colorspace": base_image["colorspace"],
                                "ext": base_image["ext"],
                                "bbox": bbox_coords,
                        })
                for d in page.get_drawings():
                        page_dict["drawings"].append({
                                "type": d["type"],  # line, rect, etc.
                                "rect": rect_to_list(d.get("rect")),
                                "color": d.get("color"),
                                "fill": d.get("fill"),
                                "width": d.get("width"),
                        })



                layout_data.append(page_dict)

        doc.close()
        return layout_data





if __name__ == "__main__":
        pdf_path = "resume.pdf"
        layout = extract_layout_from_pdf(pdf_path)


        with open("layout.json", "w", encoding="utf-8") as f:
                json.dump(layout, f, indent=2, ensure_ascii=False)
        print("layou extracted success")


