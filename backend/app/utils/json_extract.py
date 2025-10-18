import json

def simplify_layout(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        layout = json.load(f)

    simplified = {"pages": []}

    for page in layout:
        page_data = {
            "page_number": page["page_number"],
            "text_blocks": []
        }

        for i, block in enumerate(page.get("blocks", [])):
            page_data["text_blocks"].append({
                "index": i,                   # 🧩 needed for mapping later
                "text": block.get("text", ""),
                "font": block.get("font", ""),
                "size": block.get("size", 0),
                "color": block.get("color", 0),
                "bbox": block.get("bbox", [])
            })

        simplified["pages"].append(page_data)

    return simplified


def merge_layout(original_layout, ai_layout):
    """Replaces text in original layout with new text from AI layout."""
    for ai_page, orig_page in zip(ai_layout["pages"], original_layout):
        for block in ai_page["text_blocks"]:
            index = block["index"]
            if index < len(orig_page.get("blocks", [])):
                orig_page["blocks"][index]["text"] = block["text"]
    return original_layout


