import io
from models import CONFIG_JSON
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def wrap_text(text, font_name, font_size, max_width):
    lines = []
    for paragraph in text.splitlines():
        line = ''
        for char in paragraph:
            if pdfmetrics.stringWidth(line + char, font_name, font_size) <= max_width:
                line += char
            else:
                lines.append(line)
                line = char
        if line:
            lines.append(line)
    return lines


def create_pdf(config: CONFIG_JSON):
    # バッファを作成
    buffer = io.BytesIO()

    font_path = "./fonts/ipaexg.ttf"
    font_name = "IPAexGothic"
    font_size = 10.5
    line_height = font_size + 4
    title_height = 40

    pdfmetrics.registerFont(TTFont(font_name, font_path))

    # Canvasをバッファ上に作成
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin_x = 40
    margin_y = 40
    max_width = width - 2 * margin_x

    # ロゴ画像
    logo_path = "./images/logo.jpg"
    logo_width_pt = 20 * 72 / 25.4
    logo_height_pt = 20 * 72 / 25.4
    c.drawImage(logo_path, width - margin_x - logo_width_pt,
                height - margin_y - 30,
                width=logo_width_pt, height=logo_height_pt)

    c.setFont(font_name, 16)
    c.drawString(margin_x, height - margin_y,
                 f"GoodJob! ES作成代行 {config.name}様")

    c.setFont(font_name, font_size)
    y = height - margin_y - title_height

    def write_section(label, text, insert_top_margin=True):
        nonlocal y
        label_font_size = 13
        body_font_size = font_size  # 10.5
        label_spacing_above = 10
        label_spacing_below = 6

        if insert_top_margin:
            y -= label_spacing_above

        # 改ページが必要なら先にページを進める（ラベル描画前）
        if y <= margin_y:
            c.showPage()
            y = height - margin_y - title_height
            c.setFont(font_name, body_font_size)

        # ラベル描画（1回だけ）
        c.setFont(font_name, label_font_size)
        c.drawString(margin_x, y, f"【{label}】")
        y -= label_font_size + label_spacing_below

        # 本文描画
        c.setFont(font_name, body_font_size)
        wrapped = wrap_text(text, font_name, body_font_size, max_width)
        for line in wrapped:
            if y <= margin_y:
                c.showPage()
                y = height - margin_y - title_height
                c.setFont(font_name, body_font_size)
            c.drawString(margin_x, y, line)
            y -= line_height

    write_section(config.question1, config.answer1)
    write_section(config.question2, config.answer2)

    c.save()

    buffer.seek(0)
    pdf = buffer.read()
    buffer.close()
    return pdf
