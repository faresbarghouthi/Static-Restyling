#!/usr/bin/env python3
"""Generate a professional painting estimate PDF for Imagine Paint and Remodel.
   Updated: graphical paint-roller logo, revised line items, grand total $10,363.78
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable, Flowable

# ── Color palette ──────────────────────────────────────────────────────────────
TEAL        = colors.HexColor('#1A6B72')
TEAL_LIGHT  = colors.HexColor('#E8F4F5')
TEAL_MID    = colors.HexColor('#B8DCE0')
TEAL_DARK2  = colors.HexColor('#155960')   # deeper shade for icon outlines
DARK_GRAY   = colors.HexColor('#2D2D2D')
MID_GRAY    = colors.HexColor('#6B6B6B')
LIGHT_GRAY  = colors.HexColor('#F5F5F5')
WHITE       = colors.white
ALT_ROW     = colors.HexColor('#F0F9FA')
GOLD        = colors.HexColor('#F0A500')   # warm gold accent

OUTPUT_PATH = os.path.expanduser(
    '~/Desktop/Imagine_Paint_Remodel_Estimate_IPR-2026-0406.pdf'
)


# ═══════════════════════════════════════════════════════════════════════════════
# Graphical paint-roller logo flowable
# ═══════════════════════════════════════════════════════════════════════════════
class PaintRollerLogoFlowable(Flowable):
    """
    Draws a paint-roller icon using ReportLab canvas drawing primitives
    (rectangles, circles, rounded rects, lines) in teal + gold, then renders
    the company name and tagline text to the right of the icon.
    """
    WIDTH  = 4.0 * inch
    HEIGHT = 0.80 * inch

    def __init__(self):
        super().__init__()
        self.width  = self.WIDTH
        self.height = self.HEIGHT

    # ── low-level canvas drawing ─────────────────────────────────────────────
    def draw(self):
        c = self.canv

        # ── icon coordinate system: origin at bottom-left of the flowable ──
        # Icon occupies a ~52×48pt box starting at (0, 0)
        ix = 2    # small left margin
        iy = 4    # small bottom margin

        # --- Vertical handle (grip) -----------------------------------------
        # Rounded rectangle: 7 wide, 28 tall, positioned left side
        c.setFillColor(TEAL)
        c.setStrokeColor(TEAL_DARK2)
        c.setLineWidth(0.8)
        c.roundRect(ix + 6, iy, 7, 26, 3, fill=1, stroke=1)

        # Grip texture lines (small horizontal notches in a lighter shade)
        c.setStrokeColor(TEAL_LIGHT)
        c.setLineWidth(0.8)
        for gy in [iy + 6, iy + 11, iy + 16]:
            c.line(ix + 7, gy, ix + 12, gy)

        # --- Horizontal arm (connecting handle top to roller frame) ----------
        c.setFillColor(TEAL)
        c.setStrokeColor(TEAL_DARK2)
        c.setLineWidth(0.8)
        # arm: from top of handle across to the roller frame
        c.roundRect(ix + 6, iy + 24, 30, 5, 2, fill=1, stroke=1)

        # --- Roller cylinder (the main rolling pad) -------------------------
        roller_x = ix + 22
        roller_y = iy + 6
        roller_w = 28
        roller_h = 20

        # Cylinder body
        c.setFillColor(TEAL_MID)
        c.setStrokeColor(TEAL)
        c.setLineWidth(1.2)
        c.roundRect(roller_x, roller_y, roller_w, roller_h, 5, fill=1, stroke=1)

        # Gold accent band across the middle of the roller
        c.setFillColor(GOLD)
        c.setStrokeColor(colors.transparent)
        # Clip the band inside the rounded body visually by drawing a slim rect
        c.rect(roller_x + 1, roller_y + 7, roller_w - 2, 6, fill=1, stroke=0)

        # Left end-cap circle
        c.setFillColor(TEAL_DARK2)
        c.setStrokeColor(TEAL_DARK2)
        c.circle(roller_x, roller_y + roller_h / 2, 4, fill=1, stroke=0)

        # Right end-cap circle
        c.circle(roller_x + roller_w, roller_y + roller_h / 2, 4, fill=1, stroke=0)

        # Highlight sheen (small white-ish arc suggestion at top of roller)
        c.setFillColor(colors.HexColor('#C8E8EC'))
        c.setStrokeColor(colors.transparent)
        c.roundRect(roller_x + 5, roller_y + 13, 16, 4, 2, fill=1, stroke=0)

        # --- Paint drips below the roller -----------------------------------
        c.setFillColor(TEAL)
        c.setStrokeColor(colors.transparent)
        drip_tops = [roller_x + 5, roller_x + 13, roller_x + 21]
        for dx in drip_tops:
            # Ellipse body of drip
            c.ellipse(dx - 2.5, iy - 1, dx + 2.5, roller_y + 1, fill=1, stroke=0)
            # Pointed tip
            p = c.beginPath()
            p.moveTo(dx - 2, iy + 1)
            p.lineTo(dx + 2, iy + 1)
            p.lineTo(dx,     iy - 4)
            p.close()
            c.drawPath(p, fill=1, stroke=0)

        # ── Company name text (right of icon) ─────────────────────────────
        tx = ix + 58    # text start x

        # "Imagine Paint and Remodel" — bold, large
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(TEAL)
        c.drawString(tx, iy + 28, "Imagine Paint and Remodel")

        # Gold underline accent beneath the company name
        name_w = c.stringWidth("Imagine Paint and Remodel", "Helvetica-Bold", 16)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.5)
        c.line(tx, iy + 26, tx + name_w, iy + 26)

        # Tagline in italic teal
        c.setFont("Helvetica-Oblique", 8.5)
        c.setFillColor(MID_GRAY)
        c.drawString(tx + 2, iy + 12, "Where Quality Meets Craftsmanship")


def make_styles():
    base = getSampleStyleSheet()

    styles = {
        'company': ParagraphStyle(
            'company',
            fontName='Helvetica-Bold',
            fontSize=26,
            textColor=TEAL,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        'tagline': ParagraphStyle(
            'tagline',
            fontName='Helvetica-Oblique',
            fontSize=11,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        'estimate_label': ParagraphStyle(
            'estimate_label',
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=WHITE,
            alignment=TA_CENTER,
        ),
        'section_header': ParagraphStyle(
            'section_header',
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=WHITE,
        ),
        'body': ParagraphStyle(
            'body',
            fontName='Helvetica',
            fontSize=9,
            textColor=DARK_GRAY,
            leading=13,
        ),
        'body_bold': ParagraphStyle(
            'body_bold',
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=DARK_GRAY,
        ),
        'body_center': ParagraphStyle(
            'body_center',
            fontName='Helvetica',
            fontSize=9,
            textColor=DARK_GRAY,
            alignment=TA_CENTER,
        ),
        'body_right': ParagraphStyle(
            'body_right',
            fontName='Helvetica',
            fontSize=9,
            textColor=DARK_GRAY,
            alignment=TA_RIGHT,
        ),
        'total_label': ParagraphStyle(
            'total_label',
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=TEAL,
            alignment=TA_RIGHT,
        ),
        'total_value': ParagraphStyle(
            'total_value',
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=TEAL,
            alignment=TA_RIGHT,
        ),
        'grand_total_label': ParagraphStyle(
            'grand_total_label',
            fontName='Helvetica-Bold',
            fontSize=13,
            textColor=WHITE,
        ),
        'grand_total_value': ParagraphStyle(
            'grand_total_value',
            fontName='Helvetica-Bold',
            fontSize=13,
            textColor=WHITE,
            alignment=TA_RIGHT,
        ),
        'terms_header': ParagraphStyle(
            'terms_header',
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=TEAL,
            spaceAfter=2,
        ),
        'terms_body': ParagraphStyle(
            'terms_body',
            fontName='Helvetica',
            fontSize=8.5,
            textColor=DARK_GRAY,
            leading=13,
        ),
        'footer': ParagraphStyle(
            'footer',
            fontName='Helvetica-Oblique',
            fontSize=9,
            textColor=WHITE,
            alignment=TA_CENTER,
        ),
        'sig_label': ParagraphStyle(
            'sig_label',
            fontName='Helvetica',
            fontSize=8,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
        ),
        'sig_header': ParagraphStyle(
            'sig_header',
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=TEAL,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
    }
    return styles


def header_table(styles):
    """Top header: graphical paint-roller logo (left) + estimate meta (right)."""
    logo = PaintRollerLogoFlowable()

    meta_style = ParagraphStyle('meta', fontName='Helvetica', fontSize=9,
                                textColor=DARK_GRAY, alignment=TA_RIGHT, leading=14)

    meta_block = [
        Paragraph("<b>ESTIMATE</b>", ParagraphStyle(
            'est_title', fontName='Helvetica-Bold', fontSize=14,
            textColor=TEAL, alignment=TA_RIGHT, spaceAfter=4)),
        Paragraph("Estimate #:  <b>IPR-2026-0406</b>", meta_style),
        Paragraph("Date:  <b>April 6, 2026</b>", meta_style),
        Paragraph("Valid For:  <b>30 Days</b>", meta_style),
    ]

    tbl = Table(
        [[logo, meta_block]],
        colWidths=[4.0 * inch, 2.8 * inch],
    )
    tbl.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('RIGHTPADDING', (-1, 0), (-1, 0), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return tbl


def section_header_row(title, col_widths):
    """A full-width colored header row spanning all columns."""
    tbl = Table(
        [[Paragraph(title, ParagraphStyle(
            'sh', fontName='Helvetica-Bold', fontSize=10.5,
            textColor=WHITE, leading=14))]],
        colWidths=[sum(col_widths)],
    )
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), TEAL),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return tbl


def line_items_table(items, col_widths, styles):
    """Build an itemized table with alternating row shading."""
    col_header_style = ParagraphStyle(
        'ch', fontName='Helvetica-Bold', fontSize=8.5,
        textColor=WHITE, alignment=TA_CENTER)
    col_header_left = ParagraphStyle(
        'chl', fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE)

    header_row = [
        Paragraph("#", col_header_style),
        Paragraph("Description", col_header_left),
        Paragraph("Qty", col_header_style),
        Paragraph("Unit Price", col_header_style),
        Paragraph("Total", col_header_style),
    ]

    data = [header_row]
    for i, item in enumerate(items):
        num, desc, qty, unit, total = item
        row = [
            Paragraph(str(num), ParagraphStyle('c', fontName='Helvetica',
                      fontSize=8.5, textColor=DARK_GRAY, alignment=TA_CENTER)),
            Paragraph(desc, ParagraphStyle('dl', fontName='Helvetica',
                      fontSize=8.5, textColor=DARK_GRAY, leading=12)),
            Paragraph(str(qty), ParagraphStyle('c', fontName='Helvetica',
                      fontSize=8.5, textColor=DARK_GRAY, alignment=TA_CENTER)),
            Paragraph(unit, ParagraphStyle('r', fontName='Helvetica',
                      fontSize=8.5, textColor=DARK_GRAY, alignment=TA_RIGHT)),
            Paragraph(total, ParagraphStyle('r', fontName='Helvetica-Bold',
                      fontSize=8.5, textColor=DARK_GRAY, alignment=TA_RIGHT)),
        ]
        data.append(row)

    style = TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), TEAL_MID),
        ('TEXTCOLOR', (0, 0), (-1, 0), TEAL),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        # Alternating rows
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, ALT_ROW]),
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#C8DCE0')),
        ('LINEBELOW', (0, 0), (-1, 0), 1.0, TEAL),
        # Padding
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(style)
    return tbl


def subtotal_row(label, amount, col_widths):
    """Right-aligned subtotal bar."""
    total_width = col_widths[3] + col_widths[4]
    prefix_width = sum(col_widths) - total_width

    label_style  = ParagraphStyle('sl', fontName='Helvetica-Bold', fontSize=9.5,
                                  textColor=TEAL, alignment=TA_RIGHT)
    amount_style = ParagraphStyle('sa', fontName='Helvetica-Bold', fontSize=9.5,
                                  textColor=TEAL, alignment=TA_RIGHT)

    tbl = Table(
        [[Paragraph(label, label_style), Paragraph(amount, amount_style)]],
        colWidths=[prefix_width, total_width],
    )
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), TEAL_LIGHT),
        ('LINEABOVE', (0, 0), (-1, 0), 1.0, TEAL),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, TEAL),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (-1, 0), (-1, 0), 6),
    ]))
    return tbl


def summary_table(styles):
    """Estimate summary box with grand total."""
    label_style  = ParagraphStyle('suml', fontName='Helvetica', fontSize=10,
                                  textColor=DARK_GRAY, alignment=TA_LEFT)
    value_style  = ParagraphStyle('sumv', fontName='Helvetica', fontSize=10,
                                  textColor=DARK_GRAY, alignment=TA_RIGHT)
    bold_label   = ParagraphStyle('sumbl', fontName='Helvetica-Bold', fontSize=10,
                                  textColor=DARK_GRAY, alignment=TA_LEFT)

    rows = [
        [Paragraph("ESTIMATE SUMMARY", ParagraphStyle(
            'sumhdr', fontName='Helvetica-Bold', fontSize=11,
            textColor=WHITE)), Paragraph("", label_style)],
        [Paragraph("Downstairs — Full Interior", label_style),
         Paragraph("$5,750.00", value_style)],
        [Paragraph("Upstairs — Full Interior", label_style),
         Paragraph("$4,613.78", value_style)],
        [Paragraph("GRAND TOTAL", ParagraphStyle(
            'gtl', fontName='Helvetica-Bold', fontSize=12,
            textColor=WHITE, alignment=TA_LEFT)),
         Paragraph("$10,363.78", ParagraphStyle(
             'gtv', fontName='Helvetica-Bold', fontSize=12,
             textColor=WHITE, alignment=TA_RIGHT))],
    ]

    col_w = [3.5 * inch, 1.8 * inch]
    tbl = Table(rows, colWidths=col_w)
    tbl.setStyle(TableStyle([
        # Summary header
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('SPAN', (0, 0), (-1, 0)),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, 0), 10),
        # Line item rows
        ('BACKGROUND', (0, 1), (-1, 2), WHITE),
        ('LINEBELOW', (0, 1), (-1, 1), 0.4, TEAL_MID),
        ('LINEBELOW', (0, 2), (-1, 2), 0.4, TEAL_MID),
        # Grand total row
        ('BACKGROUND', (0, 3), (-1, 3), TEAL),
        ('TOPPADDING', (0, 3), (-1, 3), 9),
        ('BOTTOMPADDING', (0, 3), (-1, 3), 9),
        # General
        ('TOPPADDING', (0, 1), (-1, 2), 7),
        ('BOTTOMPADDING', (0, 1), (-1, 2), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1.5, TEAL),
    ]))
    return tbl


def terms_table(styles):
    """Terms and conditions in a bordered box."""
    header = ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=10,
                            textColor=TEAL, spaceAfter=4)
    item   = ParagraphStyle('ti', fontName='Helvetica', fontSize=8.5,
                            textColor=DARK_GRAY, leading=13)
    bold_prefix = ParagraphStyle('tp', fontName='Helvetica-Bold', fontSize=8.5,
                                 textColor=DARK_GRAY, leading=13)

    terms = [
        Paragraph("TERMS &amp; CONDITIONS", header),
        Paragraph("• <b>Deposit Required:</b> 50% ($5,181.89) due upon signing to schedule work", item),
        Paragraph("• <b>Balance Due:</b> Upon completion and final walk-through", item),
        Paragraph("• <b>Payment Methods:</b> Cash, Check, Zelle, or Card", item),
        Paragraph("• <b>Warranty:</b> All workmanship guaranteed for 1 year from completion date", item),
        Paragraph("• <b>Scope:</b> Price includes all labor and materials as outlined above", item),
        Paragraph("• <b>Client Responsibility:</b> Furniture moved prior to start date; "
                  "Imagine Paint &amp; Remodel is not responsible for pre-existing wall damage "
                  "beyond normal patching", item),
    ]

    tbl = Table([[terms]], colWidths=[6.8 * inch])
    tbl.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1.0, TEAL),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, -1), TEAL_LIGHT),
    ]))
    return tbl


def signature_table(styles):
    """Three-column signature section."""
    hdr = ParagraphStyle('sigh', fontName='Helvetica-Bold', fontSize=9.5,
                         textColor=TEAL, alignment=TA_CENTER, spaceAfter=4)
    lbl = ParagraphStyle('sigl', fontName='Helvetica', fontSize=8,
                         textColor=MID_GRAY, alignment=TA_CENTER)
    line_char = "_" * 32

    def sig_block(title, line1_label, line2_label):
        return [
            Paragraph(title, hdr),
            Paragraph(line_char, ParagraphStyle(
                'sline', fontName='Helvetica', fontSize=9,
                textColor=DARK_GRAY, alignment=TA_CENTER)),
            Paragraph(line1_label, lbl),
            Spacer(1, 10),
            Paragraph(line_char, ParagraphStyle(
                'sline2', fontName='Helvetica', fontSize=9,
                textColor=DARK_GRAY, alignment=TA_CENTER)),
            Paragraph(line2_label, lbl),
        ]

    header_row = [[
        Paragraph("ACCEPTANCE &amp; AUTHORIZATION", ParagraphStyle(
            'acchdr', fontName='Helvetica-Bold', fontSize=10.5,
            textColor=WHITE, alignment=TA_CENTER)),
    ]]

    sig_data = [[
        sig_block("Client Name", "Print Name", ""),
        sig_block("Client Signature &amp; Date", "Signature", "Date"),
        sig_block("Authorized By (Imagine Paint &amp; Remodel)", "Signature", "Date"),
    ]]

    header_tbl = Table(header_row, colWidths=[6.8 * inch])
    header_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), TEAL),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    sig_tbl = Table(sig_data, colWidths=[2.2 * inch, 2.3 * inch, 2.3 * inch])
    sig_tbl.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, -1), WHITE),
        ('LINEAFTER', (0, 0), (1, 0), 0.5, TEAL_MID),
        ('BOX', (0, 0), (-1, -1), 1.0, TEAL),
    ]))

    return [header_tbl, sig_tbl]


def footer_table(styles):
    """Dark teal footer bar."""
    contact = ParagraphStyle('contact', fontName='Helvetica', fontSize=8,
                             textColor=TEAL_LIGHT, alignment=TA_CENTER)
    tagline = ParagraphStyle('ftag', fontName='Helvetica-BoldOblique', fontSize=9.5,
                             textColor=WHITE, alignment=TA_CENTER)

    content = [
        Paragraph(
            "Thank you for choosing Imagine Paint and Remodel — "
            "<i>Where Quality Meets Craftsmanship!</i>", tagline),
        Spacer(1, 4),
        Paragraph("Phone: (000) 000-0000  |  Email: info@imaginepaintremodel.com  |  "
                  "Website: www.imaginepaintremodel.com", contact),
    ]

    tbl = Table([[content]], colWidths=[6.8 * inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), TEAL),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
    ]))
    return tbl


def build_pdf():
    styles = make_styles()

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.65 * inch,
        title="Painting Estimate IPR-2026-0406",
        author="Imagine Paint and Remodel",
    )

    # Column widths for line-item tables
    col_widths = [0.3 * inch, 3.3 * inch, 0.45 * inch, 1.1 * inch, 1.0 * inch]
    # total usable width ≈ 6.8"

    # ── Downstairs items — Total: $5,750.00 ───────────────────────────────────
    ds_items = [
        (1, "Wall & Ceiling Surface Prep\n(sanding, patching, taping, priming)", 1, "$725.00", "$725.00"),
        (2, "Wall & Ceiling Paint Application (2 coats)", 1, "$387.50", "$387.50"),
        (3, "Door Painting — Interior\n(both sides, frame & casing)", 18, "$75.00", "$1,350.00"),
        (4, "Trim, Baseboard & Crown Molding Painting", 1, "$437.50", "$437.50"),
        (5, "Touch-Up Labor & Quality Final Walk-Through", 1, "$350.00", "$350.00"),
        (6, "Materials & Supplies\n(paint, primer, tape, drop cloths, brushes, rollers)", 1, "$2,500.00", "$2,500.00"),
    ]

    # ── Upstairs items — Total: $4,613.78 ─────────────────────────────────────
    us_items = [
        (1, "Wall & Ceiling Surface Prep\n(sanding, patching, taping, priming)", 1, "$213.78", "$213.78"),
        (2, "Wall & Ceiling Paint Application (2 coats)", 1, "$162.00", "$162.00"),
        (3, "Door Painting — Interior\n(both sides, frame & casing)", 26, "$75.00", "$1,950.00"),
        (4, "Trim, Baseboard & Crown Molding Painting", 1, "$138.00", "$138.00"),
        (5, "Touch-Up Labor & Quality Final Walk-Through", 1, "$150.00", "$150.00"),
        (6, "Materials & Supplies\n(paint, primer, tape, drop cloths, brushes, rollers)", 1, "$2,000.00", "$2,000.00"),
    ]

    story = []

    # ── Header ─────────────────────────────────────────────────────────────────
    story.append(header_table(styles))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL,
                            spaceAfter=12, spaceBefore=8))

    # ── Downstairs section ─────────────────────────────────────────────────────
    story.append(section_header_row("DOWNSTAIRS — Full Interior Painting", col_widths))
    story.append(Spacer(1, 1))
    story.append(line_items_table(ds_items, col_widths, styles))
    story.append(subtotal_row("Downstairs Total:", "$5,750.00", col_widths))
    story.append(Spacer(1, 14))

    # ── Upstairs section ───────────────────────────────────────────────────────
    story.append(section_header_row("UPSTAIRS — Full Interior Painting", col_widths))
    story.append(Spacer(1, 1))
    story.append(line_items_table(us_items, col_widths, styles))
    story.append(subtotal_row("Upstairs Total:", "$4,613.78", col_widths))
    story.append(Spacer(1, 16))

    # ── Summary ────────────────────────────────────────────────────────────────
    # Right-align the summary table
    summary_wrapper = Table(
        [[Paragraph("", styles['body']), summary_table(styles)]],
        colWidths=[1.5 * inch, 5.3 * inch],
    )
    summary_wrapper.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(summary_wrapper)
    story.append(Spacer(1, 16))

    # ── Terms ──────────────────────────────────────────────────────────────────
    story.append(KeepTogether([terms_table(styles)]))
    story.append(Spacer(1, 16))

    # ── Signature ─────────────────────────────────────────────────────────────
    sig_parts = signature_table(styles)
    story.append(KeepTogether(sig_parts))
    story.append(Spacer(1, 16))

    # ── Footer ─────────────────────────────────────────────────────────────────
    story.append(footer_table(styles))

    doc.build(story)
    print(f"PDF saved to: {OUTPUT_PATH}")


if __name__ == '__main__':
    build_pdf()
