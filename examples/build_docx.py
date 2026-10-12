"""Create an RTL fixture. Requires python-docx; render separately before acceptance."""
import argparse
from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.opc.constants import RELATIONSHIP_TYPE as RT


def property_node(props, tag, value="1"):
    node = props.find(qn(tag))
    if node is None:
        node = OxmlElement(tag)
        props.append(node)
    node.set(qn("w:val"), value)
    return node


def direction(paragraph, rtl=True):
    property_node(paragraph._p.get_or_add_pPr(), "w:bidi", "1" if rtl else "0")
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT if rtl else WD_ALIGN_PARAGRAPH.LEFT


def run_text(paragraph, text, rtl=True):
    run = paragraph.add_run(text)
    run.font.name = "Tahoma" if rtl else "Consolas"
    run.font.size = Pt(12 if rtl else 10)
    props = run._r.get_or_add_rPr()
    property_node(props, "w:rtl", "1" if rtl else "0")
    fonts = props.find(qn("w:rFonts"))
    fonts.set(qn("w:cs"), "Tahoma")
    property_node(props, "w:szCs", "24")
    lang = property_node(props, "w:lang", "fa-IR" if rtl else "en-US")
    lang.set(qn("w:bidi"), "fa-IR")
    return run


def paragraph(doc, segments, style=None, rtl=True):
    p = doc.add_paragraph(style=style)
    direction(p, rtl)
    for text, is_rtl in segments:
        run_text(p, text, is_rtl)
    return p


def build(output):
    doc = Document()
    doc.core_properties.author = "Persian Output Skill"
    doc.core_properties.title = "نمونهٔ خروجی فارسی"
    for section in doc.sections:
        section.top_margin = section.bottom_margin = Inches(0.8)
        section.left_margin = section.right_margin = Inches(0.8)
    paragraph(doc, [("نمونهٔ خروجی فارسی", True)], "Title")
    paragraph(doc, [("این نمونه برای بررسی جهت بندها، جدول و متن ترکیبی است. تأیید نمایش به رندر و مشاهدهٔ صفحه نیاز دارد.", True)])
    paragraph(doc, [("این فایل‌ها به‌روز می‌شوند؛ آیا نیم‌فاصله‌ها درست هستند؟", True)])
    paragraph(doc, [("نسخهٔ ", True), ("v2.1.0", False), (" (نسخهٔ آزمایشی) روی پورت ", True), ("8080", False), (" اجرا می‌شود.", True)])
    paragraph(doc, [("تاریخ آزمون: ", True), ("2026-10-12", False), ("؛ مقدار فنی: ", True), ("3.14", False), ("؛ تعداد نمونه‌ها: ۱۲.", True)])
    paragraph(doc, [("مسیر فایل: ", True), (r"C:\Projects\demo\config.json", False)])
    for text in ["معنای متن حفظ شود.", "کد و لینک‌ها دقیق باقی بمانند."]:
        paragraph(doc, [(text, True)], "List Bullet")
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    property_node(table._tbl.tblPr, "w:bidiVisual")
    for cell, value in zip(table.rows[0].cells, ["مورد", "مقدار"]):
        direction(cell.paragraphs[0])
        run_text(cell.paragraphs[0], value)
    for label, value, is_rtl in [("نسخه", "v2.1.0", False), ("وضعیت", "آمادهٔ بررسی", True)]:
        cells = table.add_row().cells
        for cell in cells:
            direction(cell.paragraphs[0])
        run_text(cells[0].paragraphs[0], label)
        run_text(cells[1].paragraphs[0], value, is_rtl)
    p = paragraph(doc, [("پیوند: ", True)])
    target = "https://example.com/docs?q=rtl&v=2"
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), p.part.relate_to(target, RT.HYPERLINK, is_external=True))
    r = run_text(p, target, False)
    p._p.remove(r._r)
    link.append(r._r)
    p._p.append(link)
    paragraph(doc, [('payload = {"version": "v2.1.0", "amount": 3.14}', False)], rtl=False)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    print(f"Created {output}; visual review still required.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    build(parser.parse_args().output)
