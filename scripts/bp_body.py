# -*- coding: utf-8 -*-
"""MboaAssur — Business Plan 2027-2029 (corps du document, ReportLab)."""
import os, sys, hashlib

PDF_SKILL_DIR = '/home/z/my-project/skills/pdf'
sys.path.insert(0, os.path.join(PDF_SKILL_DIR, 'scripts'))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, Image, KeepTogether,
                                CondPageBreak, HRFlowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from PIL import Image as PILImage

# ------------------------------------------------------------------ polices
FONT_DIR = '/usr/share/fonts'
pdfmetrics.registerFont(TTFont('NotoSerifSC', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSerifSC-Bold', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif', f'{FONT_DIR}/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Bold', f'{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Italic', f'{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-BoldItalic', f'{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', f'{FONT_DIR}/truetype/dejavu/DejaVuSansMono.ttf'))
registerFontFamily('NotoSerifSC', normal='NotoSerifSC', bold='NotoSerifSC-Bold')
registerFontFamily('FreeSerif', normal='FreeSerif', bold='FreeSerif-Bold',
                   italic='FreeSerif-Italic', boldItalic='FreeSerif-BoldItalic')
registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans')

from pdf import install_font_fallback
install_font_fallback()

# ------------------------------------------------- palette Template 07 (fixe)
PAGE_BG      = colors.HexColor('#f5f8fc')   # XL
SECTION_BG   = colors.HexColor('#edf2f9')   # XL
CARD_BG      = colors.HexColor('#e4ecf5')   # L
TABLE_STRIPE = colors.HexColor('#eef3fa')   # L
HEADER_FILL  = colors.HexColor('#1a4a7a')   # M
BORDER       = colors.HexColor('#c0d0e2')   # S
ACCENT       = colors.HexColor('#2d7ab3')   # XS
TEXT_PRIMARY = colors.HexColor('#142840')
TEXT_MUTED   = colors.HexColor('#5a7a96')

TABLE_HEADER_COLOR = HEADER_FILL
TABLE_ROW_EVEN     = colors.white
TABLE_ROW_ODD      = TABLE_STRIPE

# ------------------------------------------------------------------ page
PAGE_W, PAGE_H = A4
MARGIN = 0.9 * inch
AVAIL_W = PAGE_W - 2 * MARGIN
AVAIL_H = PAGE_H - 2 * MARGIN
H1_ORPHAN = AVAIL_H * 0.25

OUT_BODY = '/home/z/my-project/scripts/assets/bp_body.pdf'
ASSETS = '/home/z/my-project/scripts/assets'
DOC_TITLE = 'MboaAssur — Business Plan 2027-2029'
DOC_AUTHOR = 'Mballa Andela Rose'

# ------------------------------------------------------------------ styles
S = {}
S['body'] = ParagraphStyle('Body', fontName='FreeSerif', fontSize=10.5, leading=16.5,
                           alignment=TA_JUSTIFY, textColor=TEXT_PRIMARY,
                           spaceBefore=0, spaceAfter=9)
S['lead'] = ParagraphStyle('Lead', parent=S['body'], fontSize=11, leading=17.5,
                           textColor=TEXT_PRIMARY)
S['h1'] = ParagraphStyle('H1', fontName='FreeSerif-Bold', fontSize=19, leading=24,
                         textColor=HEADER_FILL, spaceBefore=16, spaceAfter=4)
S['h2'] = ParagraphStyle('H2', fontName='FreeSerif-Bold', fontSize=14, leading=19,
                         textColor=TEXT_PRIMARY, spaceBefore=14, spaceAfter=7)
S['h3'] = ParagraphStyle('H3', fontName='FreeSerif-Bold', fontSize=11.5, leading=16,
                         textColor=ACCENT, spaceBefore=10, spaceAfter=6)
S['bullet'] = ParagraphStyle('Bullet', parent=S['body'], alignment=TA_LEFT,
                             leftIndent=16, bulletIndent=4, spaceAfter=5)
S['caption'] = ParagraphStyle('Caption', fontName='FreeSerif-Italic', fontSize=8.5,
                              leading=12, alignment=TA_CENTER, textColor=TEXT_MUTED,
                              spaceBefore=3, spaceAfter=6)
S['th'] = ParagraphStyle('TH', fontName='FreeSerif-Bold', fontSize=9.5, leading=12.5,
                         alignment=TA_CENTER, textColor=colors.white)
S['td'] = ParagraphStyle('TD', fontName='FreeSerif', fontSize=9.5, leading=12.5,
                         alignment=TA_LEFT, textColor=TEXT_PRIMARY)
S['tdc'] = ParagraphStyle('TDC', parent=S['td'], alignment=TA_CENTER)
S['tdr'] = ParagraphStyle('TDR', parent=S['td'], alignment=TA_RIGHT)
S['tdb'] = ParagraphStyle('TDB', parent=S['td'], fontName='FreeSerif-Bold')
S['tdbc'] = ParagraphStyle('TDBC', parent=S['tdc'], fontName='FreeSerif-Bold')
S['tdbr'] = ParagraphStyle('TDBR', parent=S['tdr'], fontName='FreeSerif-Bold')
S['stat'] = ParagraphStyle('Stat', fontName='FreeSerif-Bold', fontSize=17, leading=21,
                           textColor=ACCENT, alignment=TA_CENTER)
S['statlab'] = ParagraphStyle('StatLab', fontName='FreeSerif', fontSize=8.5, leading=11.5,
                              textColor=TEXT_MUTED, alignment=TA_CENTER)
S['quote'] = ParagraphStyle('Quote', fontName='FreeSerif-Italic', fontSize=10.5,
                            leading=16.5, leftIndent=24, textColor=TEXT_MUTED,
                            spaceBefore=6, spaceAfter=10)
S['biblio'] = ParagraphStyle('Biblio', fontName='FreeSerif', fontSize=9.5, leading=14,
                             alignment=TA_LEFT, leftIndent=24, firstLineIndent=-24,
                             spaceAfter=6, textColor=TEXT_PRIMARY)
S['toc0'] = ParagraphStyle('TOC0', fontName='FreeSerif-Bold', fontSize=11.5, leading=20,
                           leftIndent=6, textColor=TEXT_PRIMARY)
S['toc1'] = ParagraphStyle('TOC1', fontName='FreeSerif', fontSize=10, leading=16,
                           leftIndent=26, textColor=TEXT_MUTED)
S['toctitle'] = ParagraphStyle('TOCTitle', fontName='FreeSerif-Bold', fontSize=19,
                               leading=24, textColor=HEADER_FILL, spaceAfter=14)

# ------------------------------------------------------------------ doc template
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if getattr(flowable, 'body_marker', False):
            if self.page < getattr(self, '_body_start', 10**6):
                self._body_start = self.page
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            display_page = self.page - getattr(self, '_body_start', 2) + 1
            self.notify('TOCEntry', (level, text, display_page, key))
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=False)

ROMAN = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v', 6: 'vi'}

def _page_decor(canvas, doc):
    canvas.saveState()
    # en-tête : titre + filet accent
    canvas.setFont('FreeSerif', 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, PAGE_H - 0.55 * inch, DOC_TITLE)
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(MARGIN, PAGE_H - 0.62 * inch, PAGE_W - MARGIN, PAGE_H - 0.62 * inch)
    # pied : auteur + numéro de page
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 0.62 * inch, PAGE_W - MARGIN, 0.62 * inch)
    canvas.setFont('FreeSerif', 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, 0.45 * inch,
                      'Mballa Andela Rose — Courtier digital indépendant')
    body_start = getattr(doc, '_body_start', 2)
    if doc.page < body_start:
        label = ROMAN.get(doc.page, str(doc.page))
    else:
        label = str(doc.page - body_start + 1)
    canvas.drawRightString(PAGE_W - MARGIN, 0.45 * inch, label)
    canvas.restoreState()

# ------------------------------------------------------------------ helpers
def heading(text, style, level=0):
    key = 'h_' + hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph(f'<a name="{key}"/><b>{text}</b>', style)
    p.bookmark_name = key
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p

def h1_block(text, first_para=None):
    """H1 + filet accent (+ premier paragraphe) avec anti-orphelin."""
    els = [CondPageBreak(H1_ORPHAN), heading(text, S['h1'], 0),
           HRFlowable(width='100%', color=ACCENT, thickness=1.4,
                      spaceBefore=0, spaceAfter=10)]
    if first_para is not None:
        els.append(first_para)
    return els

def h2_block(text, first_para=None):
    els = [CondPageBreak(70), heading(text, S['h2'], 1)]
    if first_para is not None:
        return [KeepTogether(els + [first_para])]
    return els

def _fr(txt):
    """Empêche le tiret cadratin de débuter une ligne (espace insécable avant)."""
    return txt.replace(' — ', ' — ')

def para(txt, style='body'):
    return Paragraph(_fr(txt), S[style])

def bullets(items):
    return [Paragraph(_fr(t), S['bullet'], bulletText='•') for t in items]

def fit_image(path, max_w, max_h):
    im = PILImage.open(path)
    ow, oh = im.size
    r = min(max_w / ow, max_h / oh, 1.0)
    return Image(path, width=ow * r, height=oh * r)

def chart_block(png, caption, max_h=250):
    img = fit_image(os.path.join(ASSETS, png), AVAIL_W * 0.96, max_h)
    cap = Paragraph(_fr(caption), S['caption'])
    return [Spacer(1, 14), KeepTogether([img, Spacer(1, 6), cap]), Spacer(1, 12)]

def make_table(header, rows, ratios, aligns=None, bold_rows=(), caption=None,
               font_size=9.5):
    """Tableau : en-tête HEADER_FILL + zébrures TABLE_STRIPE, cellules Paragraph."""
    n = len(header)
    aligns = aligns or ['l'] * n
    stmap = {'l': 'td', 'c': 'tdc', 'r': 'tdr'}
    th = ParagraphStyle('th2', parent=S['th'], fontSize=font_size)
    data = [[Paragraph(f'<b>{_fr(h)}</b>', th) for h in header]]
    for ri, row in enumerate(rows):
        bold = ri in bold_rows
        cells = []
        for ci, cell in enumerate(row):
            base = stmap[aligns[ci]]
            st = S[('tdb' if aligns[ci] == 'l' else
                    ('tdbc' if aligns[ci] == 'c' else 'tdbr'))] if bold else S[base]
            st2 = ParagraphStyle(f'c{ri}{ci}', parent=st, fontSize=font_size)
            cells.append(Paragraph(_fr(str(cell)), st2))
        data.append(cells)
    widths = [r * AVAIL_W for r in ratios]
    assert abs(sum(ratios) - 1.0) < 0.01, 'ratios must sum to 1'
    t = Table(data, colWidths=widths, hAlign='CENTER', repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 5.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5.5),
    ]
    for i in range(1, len(data)):
        style.append(('BACKGROUND', (0, i), (-1, i),
                      TABLE_ROW_ODD if i % 2 == 0 else TABLE_ROW_EVEN))
    t.setStyle(TableStyle(style))
    out = [Spacer(1, 12), t]
    if caption:
        out += [Spacer(1, 4), Paragraph(_fr(caption), S['caption'])]
    out += [Spacer(1, 10)]
    return out

def callout_row(stats):
    """Rangée de 3-4 blocs chiffres clés (CalloutBox)."""
    cells = []
    for val, lab in stats:
        inner = [Paragraph(f'<b>{val}</b>', S['stat']),
                 Paragraph(lab, S['statlab'])]
        cells.append(inner)
    w = AVAIL_W / len(stats)
    t = Table([cells], colWidths=[w] * len(stats), hAlign='CENTER')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
        ('BOX', (0, 0), (-1, -1), 0.8, ACCENT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return [Spacer(1, 8), KeepTogether(t), Spacer(1, 12)]

# ================================================================== story
story = []

# --- Sommaire ---------------------------------------------------------------
toc = TableOfContents()
toc.levelStyles = [S['toc0'], S['toc1']]
story.append(Paragraph('<b>Sommaire</b>', S['toctitle']))
story.append(HRFlowable(width='100%', color=ACCENT, thickness=1.4, spaceAfter=14))
story.append(toc)
story.append(PageBreak())

# --- Marqueur de début de corps (numérotation arabe) ------------------------
_marker = Spacer(1, 0.1)
_marker.body_marker = True
story.append(_marker)

# --- 1. Résumé exécutif -------------------------------------------------------
story += h1_block('1. Résumé exécutif', para(
    "MboaAssur est une plateforme de courtage d'assurance digitale conçue pour le "
    "marché camerounais, portée par un courtier digital indépendant et destinée à "
    "devenir le point de passage unique entre les assurés et les compagnies d'assurance "
    "de la zone CIMA. L'application regroupe la comparaison des offres de plusieurs "
    "compagnies partenaires, la souscription en ligne avec paiement Mobile Money, la "
    "délivrance d'attestations numériques certifiées par QR code, ainsi que des modules "
    "spécialisés pour les professionnels du BTP, les importateurs et la diaspora. Le "
    "présent business plan établit, sur la base des statistiques publiées par le "
    "régulateur ASAC et des données régionales FANAF et CIMA, la viabilité économique "
    "du projet : un marché en croissance soutenue de près de 300 milliards de FCFA, un "
    "modèle de revenus éprouvé fondé sur les commissions d'apport, une structure de "
    "coûts maîtrisée et un seuil de rentabilité atteignable dès la deuxième année "
    "d'exploitation.", 'lead'))

story += callout_row([
    ('288,7 Mds', 'FCFA — chiffre d\u2019affaires du marché camerounais en 2024 (ASAC)'),
    ('+6 à +7 %', 'croissance annuelle moyenne du marché depuis 2022'),
    ('50 M FCFA', 'besoin de financement initial du projet'),
    ('210,4 M', 'FCFA de chiffre d\u2019affaires projeté en année 3'),
])

story.append(para(
    "Le choix du statut de courtier — plutôt que celui de compagnie d'assurance — est "
    "stratégique : il permet d'opérer avec un capital de démarrage de l'ordre de 50 "
    "millions de FCFA, alors que la création d'une compagnie exigerait un capital social "
    "minimum de 3 à 10 milliards de FCFA selon la branche, conformément au Code CIMA. "
    "Le modèle économique repose exclusivement sur les commissions d'apport versées par "
    "les compagnies partenaires, un mécanisme éprouvé du secteur qui ne prélève aucun "
    "frais supplémentaire sur l'assuré. Les projections 2027-2029 aboutissent à un "
    "chiffre d'affaires de 20,0 millions de FCFA la première année, 86,5 millions la "
    "deuxième et 210,4 millions la troisième, avec un résultat net positif dès la "
    "seconde année. Le projet s'inscrit enfin dans une trajectoire régionale : le cadre "
    "réglementaire commun de la zone CIMA, qui compte quatorze États membres, rend le "
    "modèle directement réplicable au-delà du Cameroun une fois la preuve économique "
    "établie sur le marché domestique."))

# --- 2. Le projet MboaAssur ---------------------------------------------------
story += h1_block('2. Le projet MboaAssur', para(
    "MboaAssur — « votre certitude au Cameroun » — répond à trois défaillances "
    "structurelles du marché camerounais de l'assurance : l'opacité des offres, qui "
    "contraint le souscripteur à se déplacer d'agence en agence pour obtenir des devis ; "
    "la méfiance du public à l'égard des délais d'indemnisation et de l'authenticité des "
    "documents ; et la faible pénétration de l'assurance dans les foyers, conséquence "
    "d'un déficit d'éducation financière. La plateforme traite ces trois problèmes par "
    "la transparence tarifaire, la digitalisation complète du parcours de souscription "
    "et un module pédagogique dédié. Elle positionne MboaAssur non pas comme un "
    "concurrent des assureurs, mais comme leur canal de distribution digital le plus "
    "efficient."))

story += h2_block('2.1 Une offre structurée en six modules', para(
    "Le produit s'appuie sur l'étude fonctionnelle validée dans les dossiers de "
    "conception du projet, qui détaille plus de 120 écrans répartis en six modules "
    "complémentaires couvrant l'ensemble du cycle de vie du contrat d'assurance :"))
story += bullets([
    "<b>Moteur de recherche et comparateur multi-critères</b> : accès instantané aux "
    "produits Auto, Santé, Scolaire, Pro & BTP et Maritime & Import de plusieurs "
    "compagnies (SAAR, Activa, SUNU, AREA...), avec tarifs annuels en FCFA, notes "
    "utilisateurs et badges de différenciation (meilleur prix, remboursement le plus "
    "rapide, couverture complète).",
    "<b>Souscription directe et attestation digitale instantanée</b> : parcours d'achat "
    "guidé, paiement par Orange Money ou MTN Mobile Money, délivrance immédiate d'une "
    "attestation certifiée avec QR code vérifiable, réduisant la fraude documentaire.",
    "<b>Espace Pro & BTP</b> : cautions de soumission pour les marchés publics, "
    "assurances maritimes et d'importation (Port Autonome de Douala et de Kribi), "
    "gestion en ligne des appels d'offres — un segment à forte valeur ajoutée et peu "
    "digitalisé.",
    "<b>Module pédagogique « Assurance Facile »</b> : vidéos animées expliquant les "
    "droits des assurés et la traçabilité des cotisations, levier d'inclusion "
    "financière et d'acquisition organique.",
    "<b>Espace « Mes Contrats », profil et notifications</b> : tableau de bord des "
    "polices actives, historique des paiements et alertes de renouvellement, qui "
    "réduit le défaut d'assurance par oubli d'échéance et sécurise la récurrence des "
    "commissions.",
    "<b>Déclaration simplifiée de sinistre</b> : dépôt des pièces justificatives par "
    "photo et suivi du statut du dossier en ligne, qui fluidifie l'étape la plus "
    "critique de la relation client.",
])

story += h2_block('2.2 Un positionnement de courtier, pas d\u2019assureur', para(
    "MboaAssur opère comme intermédiaire d'assurance : la plateforme porte les contrats "
    "de ses utilisateurs auprès de compagnies agréées, qui conservent la charge du "
    "risque, de la provision technique et du règlement des sinistres. Ce positionnement "
    "présente trois avantages décisifs pour un lancement entrepreneurial. Premièrement, "
    "l'investissement en capital est sans commune mesure avec celui d'une compagnie : "
    "le courtier doit justifier d'une garantie financière de dix millions de FCFA et "
    "d'une assurance de responsabilité civile professionnelle, contre plusieurs "
    "milliards de capital social pour un assureur. Deuxièmement, le modèle est "
    "immédiatement bénéficiaire sur le plan unitaire : chaque contrat apporté génère "
    "une commission sans coût de sinistralité associé. Troisièmement, la valeur "
    "créée pour les compagnies — un flux de clients pré-qualifiés à coût "
    "d'acquisition réduit — aligne les incentives de tous les acteurs et facilite la "
    "signature des partenariats d'apport."))

# --- 3. Analyse du marché -----------------------------------------------------
story += h1_block('3. Analyse du marché', para(
    "Le dimensionnement commercial repose sur les statistiques officielles de l'Agence "
    "de Régulation et de Contrôle des Assurances (ASAC) pour le Cameroun, sur les "
    "données agrégées de la FANAF pour l'Afrique de l'Ouest francophone et sur le cadre "
    "de la Conférence Interafricaine des Marchés d'Assurances (CIMA) pour la zone "
    "régionale. Les chiffres cités proviennent des publications de ces institutions "
    "relayées par la presse économique spécialisée ; ils sont réunis en fin de "
    "document."))

story += h2_block('3.1 Le marché camerounais : près de 300 milliards de FCFA', para(
    "Selon les données de l'ASAC, le marché camerounais de l'assurance a généré un "
    "chiffre d'affaires de 274,65 milliards de FCFA en 2023, en croissance d'environ "
    "6 % sur un an, puis 288,7 milliards de FCFA en 2024. Les estimations de clôture "
    "2025 convergent vers environ 300 milliards de FCFA. La branche non-vie — dont "
    "l'assurance automobile obligatoire est le premier contributeur — représente "
    "environ deux tiers des émissions (185,78 milliards de FCFA en 2023, après "
    "168,63 milliards en 2022 selon le Conseil national du crédit et financier), tandis "
    "que la branche vie, plus jeune, affiche la croissance la plus rapide (+9,3 % en "
    "2024). Cette dynamique, régulière depuis quatre exercices, fait du Cameroun le "
    "premier marché d'assurance de la zone CEMAC et le troisième de la zone CIMA."))

story += make_table(
    ['Branche', '2023', '2024', '2025 (p.)'],
    [
        ['Non-vie', '185,78', '191,6', '197,3'],
        ['Vie', '88,8', '97,1', '102,67'],
        ['Total marché (Mds FCFA)', '274,65', '288,7', '≈ 300'],
        ['Croissance annuelle', '+6,0 %', '+5,1 %', '+3,9 %'],
    ],
    [0.34, 0.22, 0.22, 0.22],
    aligns=['l', 'r', 'r', 'r'],
    bold_rows={2},
    caption='Tableau 1 — Évolution du marché camerounais par branche, en milliards de '
            'FCFA. Sources : ASAC (via FAIR, Investir au Cameroun, Business Finance, '
            'EcoMatin) ; 2025 provisionnel.')

story += chart_block('chart1_marche.png',
    'Figure 1 — Évolution des émissions d\u2019assurance au Cameroun, 2023-2025 '
    '(milliards de FCFA). Source : chiffres ASAC relayés par la presse spécialisée.',
    max_h=240)

story += h2_block('3.2 Le contexte régional : FANAF et zone CIMA', para(
    "Le marché camerounais s'insère dans l'espace CIMA, qui harmonise la réglementation "
    "des assurances dans quatorze États d'Afrique centrale et de l'Ouest. Au sein de "
    "cet espace, la FANAF — la fédération des sociétés d'assurance des pays de la zone "
    "franc — a recensé 2 041,2 milliards de FCFA de primes collectées en 2023 pour les "
    "marchés qu'elle couvre, dont la Côte d'Ivoire et le Sénégal sont les locomotives. "
    "L'agrégation des marchés CEMAC portés par le Cameroun porte l'ensemble de la zone "
    "CIMA à un volume d'émissions estimé à plus de 3 000 milliards de FCFA par an. Pour "
    "un courtier, cette architecture réglementaire commune est un actif : les "
    "conditions d'exercice (agrément ministériel, capacité professionnelle, garantie "
    "financière) sont définies par le Code CIMA de manière uniforme, ce qui rend le "
    "modèle MboaAssur déployable dans les treize autres États membres sans "
    "refonte du produit."))

story += make_table(
    ['Indicateur régional', 'Valeur', 'Source'],
    [
        ['Primes collectées zone FANAF (2023)', '2 041,2 Mds FCFA', 'FANAF'],
        ['États membres de la CIMA', '14 États', 'CIMA'],
        ['Émissions estimées zone CIMA', '> 3 000 Mds FCFA/an', 'Estimation FANAF + CEMAC'],
        ['Capital minimum compagnie non-vie', '5 Mds FCFA', 'Code CIMA (réforme 2016)'],
        ['Capital minimum compagnie vie', '3 Mds FCFA', 'Code CIMA (réforme 2016)'],
        ['Capital minimum microassurance', '500 M FCFA', 'Réglementation CIMA (2026)'],
    ],
    [0.42, 0.26, 0.32],
    aligns=['l', 'c', 'l'],
    caption='Tableau 2 — Repères du marché régional de l\u2019assurance francophone.')

story += h2_block('3.3 Un potentiel largement inexploité', para(
    "Le taux de pénétration de l'assurance au Cameroun — le rapport des primes au PIB — "
    "s'établit entre 0,7 % et 0,9 % selon les estimations de l'ASAC et d'Atlas "
    "Magazine, contre environ 1 % en moyenne dans la zone CIMA, 2 % en Afrique et plus "
    "de 6 % dans les pays de l'OCDE. La densité d'assurance, soit la prime par "
    "habitant, demeure l'une des plus faibles du continent à environ 13,8 dollars par "
    "an. Loin d'être un frein, cet écart constitue la thèse d'investissement du projet : "
    "chaque point de pénétration rattrapé représente plusieurs dizaines de milliards de "
    "FCFA de primes nouvelles, et les canaux digitaux sont historiquement le levier le "
    "plus efficace pour toucher les populations non couvertes — travailleurs du secteur "
    "informel, zones éloignées des agences physiques, diaspora. La démographie "
    "camerounaise (environ 29 millions d'habitants, population urbaine jeune et très "
    "équipée en Mobile Money) offre le socle naturel de cette croissance."))

story += chart_block('chart2_penetration.png',
    'Figure 2 — Taux de pénétration de l\u2019assurance en % du PIB. Cameroun : moyenne '
    'des estimations 0,7-0,9 % (ASAC, Atlas Magazine). Sources : ASAC, CIMA, FAIR, '
    'OCDE (2024).',
    max_h=215)

story += h2_block('3.4 Segments cibles et dimensionnement TAM / SAM / SOM', para(
    "Le marché adressable se décompose en deux cercles. Le marché total disponible "
    "(TAM) est l'ensemble des émissions d'assurance camerounaises, valorisées à environ "
    "325 milliards de FCFA à l'horizon 2029 en prolongeant la croissance observée. Le "
    "marché accessible (SAM) correspond aux segments que la plateforme peut "
    "effectivement digitaliser : l'auto obligatoire et tous risques, la santé "
    "individuelle et familiale, la scolaire, les cautions et assurances des "
    "professionnels du BTP et l'assurance maritime des importateurs — soit à peu près "
    "les deux tiers du marché non-vie, environ 190 milliards de FCFA. Le marché "
    "réalisable (SOM) est l'objectif commercial de MboaAssur à trois ans : 1,46 "
    "milliard de FCFA de primes apportées, soit moins de 0,5 % du marché national — "
    "un objectif volontairement prudent au regard de la dynamique de croissance du "
    "canal digital sur le continent."))

story += make_table(
    ['Niveau', 'Définition', 'Taille estimée'],
    [
        ['TAM', 'Ensemble des émissions d\u2019assurance au Cameroun (horizon 2029)', '≈ 325 Mds FCFA'],
        ['SAM', 'Segments non-vie digitalisables (auto, santé, scolaire, BTP, maritime)', '≈ 190 Mds FCFA'],
        ['SOM', 'Primes apportées par MboaAssur en année 3 (objectif)', '≈ 1,46 Md FCFA'],
    ],
    [0.12, 0.58, 0.30],
    aligns=['c', 'l', 'c'],
    caption='Tableau 3 — Dimensionnement du marché, du général au réaliste.')

# --- 4. Modèle de revenus -----------------------------------------------------
story += h1_block('4. Modèle de revenus : les commissions d\u2019apport', para(
    "Le cœur du modèle économique de MboaAssur est la commission de courtage : pour "
    "chaque contrat souscrit via la plateforme, la compagnie partenaire verse au "
    "courtier un pourcentage de la prime annuelle. Ce mécanisme, standard de la "
    "distribution assurancielle, présente l'avantage décisif de ne pas renchérir le "
    "prix payé par l'assuré — la commission est prélevée sur la marge de distribution "
    "de l'assureur, en rémunération de l'apport de clientèle et du suivi du contrat. "
    "Elle s'accompagne de commissions de gestion perçues lors des renouvellements, qui "
    "transforment chaque client acquis en flux de revenus récurrents."))

story += h2_block('4.1 Statut juridique et cadre réglementaire', para(
    "L'exercice de la profession de courtier en assurance est réglementé par le Code "
    "des assurances CIMA et contrôlé au Cameroun par l'ASAC. La plateforme, sa société "
    "porteuse et son dirigeant devront satisfaire les exigences suivantes avant toute "
    "intermédiation commerciale :"))

story += make_table(
    ['Exigence', 'Référence', 'Détail'],
    [
        ['Agrément de courtier', 'Art. 530 du Code CIMA',
         'Autorisation délivrée par le Ministre en charge des assurances, après avis '
         'de l\u2019ASAC ; inscription au registre des intermédiaires.'],
        ['Capacité professionnelle', 'Art. 508 du Code CIMA',
         'Diplôme ou expérience professionnelle attestée en assurance du dirigeant.'],
        ['Honorabilité', 'Art. 506 du Code CIMA',
         'Conditions d\u2019honorabilité et d\u2019assurance contre la fraude.'],
        ['Garantie financière', 'Dossier d\u2019agrément ASAC',
         'Caution bancaire d\u2019au moins 10 millions de FCFA couvrant les fonds '
         'susceptibles d\u2019être détenus.'],
        ['Responsabilité civile professionnelle', 'Usage ASAC',
         'Assurance couvrant les conséquences pécuniaires des fautes '
         'professionnelles.'],
    ],
    [0.24, 0.22, 0.54],
    aligns=['l', 'l', 'l'],
    caption='Tableau 4 — Conditions d\u2019exercice du courtage d\u2019assurance au Cameroun.')

story.append(para(
    "Le délai d'instruction d'un dossier d'agrément complet est généralement estimé à "
    "trois à six mois ; le plan de financement intègre cette période comme phase de "
    "préparation sans revenus. Ce cadre, loin d'être une contrainte, constitue une "
    "barrière à l'entrée protectrice : une fois l'agrément obtenu, la plateforme "
    "devient l'un des rares canaux de distribution digitale formellement autorisés à "
    "rémunérer l'apport de contrats dans l'espace CIMA."))

story += h2_block('4.2 Barème de commissions par branche', para(
    "Les taux de commission appliqués en courtage d'assurance non-vie s'établissent "
    "généralement entre 10 % et 30 % de la prime selon la branche et la complexité du "
    "dossier, en pratique de marché aussi bien en Afrique francophone qu'en Europe ou "
    "en Amérique du Nord. Les niveaux retenus dans les hypothèses de ce business plan "
    "se situent volontairement dans le bas de fourchette pour sécuriser le modèle :"))

story += make_table(
    ['Branche', 'Commission d\u2019apport', 'Commission de gestion (renouvellement)'],
    [
        ['Auto (responsabilité civile et tous risques)', '10 % à 20 %', '5 % à 10 %'],
        ['Santé et prévoyance', '10 % à 20 %', '5 % à 10 %'],
        ['Scolaire (groupes et individuel)', '10 % à 15 %', '≈ 5 %'],
        ['Cautions et assurance BTP', '15 % à 30 %', 'n.d.'],
        ['Maritime, transport et import', '12,5 % à 20 %', 'n.d.'],
        ['Vie et capitalisation', '5 % à 10 %', '2,5 % à 5 %'],
    ],
    [0.42, 0.27, 0.31],
    aligns=['l', 'c', 'c'],
    caption='Tableau 5 — Fourchettes de commissions de courtage par branche '
            '(pratiques de marché ; taux définitifs fixés dans les conventions '
            'de courtage avec chaque compagnie).')

story += h2_block('4.3 Économie unitaire par produit', para(
    "La combinaison du mix produit visé et des taux de commission conduit à une prime "
    "moyenne pondérée d'environ 95 000 FCFA par contrat en première année, montant qui "
    "progressera avec la montée en puissance des segments professionnels (cautions, "
    "maritime) les plus rémunérateurs. Le tableau ci-dessous fixe l'économie unitaire "
    "de référence de chaque produit :"))

story += make_table(
    ['Produit', 'Prime moyenne annuelle', 'Taux retenu', 'Commission / contrat'],
    [
        ['Auto responsabilité civile (véhicule particulier)', '60 000 FCFA', '15 %', '9 000 FCFA'],
        ['Auto tous risques', '220 000 FCFA', '17,5 %', '38 500 FCFA'],
        ['Santé individuelle / famille', '150 000 FCFA', '12,5 %', '18 750 FCFA'],
        ['Scolaire (par élève)', '8 000 FCFA', '12 %', '960 FCFA'],
        ['Caution de soumission BTP', '120 000 FCFA', '20 %', '24 000 FCFA'],
        ['Maritime & import (par conteneur)', '250 000 FCFA', '15 %', '37 500 FCFA'],
        ['Vie / éducation', '90 000 FCFA', '7,5 %', '6 750 FCFA'],
    ],
    [0.40, 0.22, 0.15, 0.23],
    aligns=['l', 'r', 'c', 'r'],
    caption='Tableau 6 — Économie unitaire de référence par produit (ordres de grandeur '
            'du marché camerounais ; taux médians des fourchettes du tableau 5).')

story += h2_block('4.4 Flux de revenus complémentaires', para(
    "Au-delà des commissions d'apport, le modèle mobilise trois sources de revenus "
    "complémentaires qui diversifient et consolident la trajectoire. Les commissions de "
    "gestion, perçues à chaque renouvellement à un taux réduit, capitalisent le "
    "portefeuille constitué les années précédentes : elles représentent 33,3 millions "
    "de FCFA en année 3, sans coût d'acquisition associé. Les services B2B, introduits "
    "en année 3, consistent à offrir aux compagnies partenaires un back-office de "
    "gestion des cautions et des appels d'offres du module Pro & BTP sous forme "
    "d'abonnement annuel, valorisé à environ 14 millions de FCFA. Enfin, les données "
    "anonymisées de comparaison (grilles tarifaires, taux de conversion, délais de "
    "remboursement) peuvent à terme faire l'objet de restitutions premium aux "
    "assureurs ; ce flux, non chiffré dans les projections par prudence, constitue une "
    "option de valeur."))

story += chart_block('chart3_flux.png',
    'Figure 3 — Répartition du chiffre d\u2019affaires projeté en année 3 (2029), en '
    'millions de FCFA.',
    max_h=205)

# --- 5. Structure de coûts ----------------------------------------------------
story += h1_block('5. Structure de coûts', para(
    "La structure de coûts de MboaAssur reflète la logique d'une startup de courtage "
    "digitale : un investissement initial concentré sur le produit logiciel et "
    "l'obtention de l'agrément, puis des charges d'exploitation dominées par les "
    "ressources humaines et l'acquisition client. Aucun actif lourd n'est requis — "
    "l'hébergement est mutualisé dans le cloud, et le paiement est délégué aux "
    "plateformes Mobile Money nationales, dont les frais sont directement proportionnels "
    "aux primes encaissées. Cette légèreté structurelle est la condition du délai court "
    "de retour sur investissement présenté au chapitre 6."))

story += h2_block('5.1 Investissement initial', para(
    "L'investissement de démarrage s'élève à 27,5 millions de FCFA de dépenses "
    "d'établissement et d'immobilisations, complétés par un fonds de roulement de 22,5 "
    "millions de FCFA destiné à couvrir la perte d'exploitation de la première année et "
    "la marge de sécurité. Le besoin total de financement s'établit ainsi à 50 millions "
    "de FCFA, à quoi s'ajoute la constitution d'une garantie financière de 10 millions "
    "de FCFA sous forme de caution bancaire — un engagement restitué, non consommé, "
    "exigé par l'agrément."))

story += make_table(
    ['Poste d\u2019investissement', 'Montant (M FCFA)'],
    [
        ['Développement de la plateforme (applications mobiles, back-office assureurs, '
         'moteur de comparaison)', '18,0'],
        ['Design UX/UI et identité de marque', '2,5'],
        ['Sécurité, hébergement initial et audits techniques', '2,5'],
        ['Constitution de la société, dossier d\u2019agrément ASAC, honoraires juridiques', '3,0'],
        ['Matériel informatique et divers', '1,5'],
        ['Sous-total dépenses d\u2019établissement', '27,5'],
        ['Fonds de roulement (couverture de la perte d\u2019exploitation An 1 et réserve)', '22,5'],
        ['Besoin total de financement', '50,0'],
    ],
    [0.78, 0.22],
    aligns=['l', 'r'],
    bold_rows={5, 7},
    caption='Tableau 7 — Plan d\u2019investissement initial. S\u2019y ajoute la garantie '
            'financière de 10 M FCFA constituée en caution bancaire (engagement restitué).')

story += h2_block('5.2 Charges d\u2019exploitation sur trois ans', para(
    "Les charges d'exploitation progressent de 41,0 millions de FCFA en première année "
    "à 138,8 millions en troisième, mais leur composition se déplace : la part des "
    "coûts variables — frais de paiement Mobile Money et commissions du réseau "
    "d'ambassadeurs introduit en année 2 — passe de 6 % à 36 % du total, signe d'un "
    "modèle dont les coûts suivent le chiffre d'affaires. L'effectif passe de quatre "
    "personnes (la fondatrice-courtier, un développeur, deux chargés de gestion et de "
    "support) à une dizaine en année 3, avec l'arrivée de profils gestion sinistres, "
    "marketing et partenariats assureurs."))

story += make_table(
    ['Poste de charges (M FCFA)', 'An 1 (2027)', 'An 2 (2028)', 'An 3 (2029)'],
    [
        ['Personnel (4 puis 7 puis 10 collaborateurs)', '25,2', '42,0', '60,0'],
        ['Hébergement, licences et API', '2,4', '4,0', '5,5'],
        ['Frais de paiement Mobile Money (≈ 1,8 % des primes)', '2,4', '9,6', '26,2'],
        ['Marketing digital et acquisition', '6,0', '10,0', '14,0'],
        ['Commissions du réseau d\u2019affiliés (12 % du CA commissions)', '0,0', '10,4', '23,6'],
        ['Local, déplacements, honoraires et divers', '5,0', '7,4', '9,5'],
        ['Charges totales', '41,0', '83,4', '138,8'],
    ],
    [0.46, 0.18, 0.18, 0.18],
    aligns=['l', 'r', 'r', 'r'],
    bold_rows={6},
    caption='Tableau 8 — Budget de charges d\u2019exploitation 2027-2029.')

# --- 6. Projections financières ----------------------------------------------
story += h1_block('6. Projections financières 2027-2029', para(
    "Les projections reposent sur un entonnoir de conversion volontairement mesuré : "
    "sur 30 000 téléchargements la première année, 40 % d'utilisateurs inscrits, et "
    "environ 12 % des inscrits souscrivent effectivement un contrat, soit 1 400 polices "
    "nouvelles. Ce taux de conversion, conservateur au regard des standards du commerce "
    "mobile en Afrique francophone, s'améliore mécaniquement au fil des versions : "
    "l'élargissement de l'offre aux segments professionnels et l'effet de la notation "
    "collaborative portent la base à 9 000 polices nouvelles en année 3, auxquelles "
    "s'ajoutent les renouvellements des cohortes précédentes à un taux de rétention de "
    "50 %."))

story += make_table(
    ['Indicateur commercial', 'An 1 (2027)', 'An 2 (2028)', 'An 3 (2029)'],
    [
        ['Téléchargements cumulés', '30 000', '120 000', '260 000'],
        ['Utilisateurs inscrits cumulés', '12 000', '45 000', '95 000'],
        ['Nouvelles polices souscrites', '1 400', '4 800', '9 000'],
        ['Renouvellements facturés', '0', '700', '2 750'],
        ['Prime moyenne pondérée (FCFA)', '95 000', '110 000', '125 000'],
        ['Primes apportées (M FCFA)', '133,0', '601,3', '1 457,8'],
        ['Taux de commission moyen', '15,0 %', '14,4 %', '13,5 %'],
    ],
    [0.40, 0.20, 0.20, 0.20],
    aligns=['l', 'r', 'r', 'r'],
    caption='Tableau 9 — Hypothèses de volumes commerciaux 2027-2029.')

story += h2_block('6.1 Compte de résultat prévisionnel', para(
    "La trajectoire résultante dessine le profil classique d'une plateforme de "
    "distribution : une première année d'investissement commercial (résultat net de "
    "-21,0 millions de FCFA, intégralement couvert par le fonds de roulement), le "
    "franchissement du point d'équilibre en cours de deuxième année (+3,1 millions), "
    "puis une troisième année à pleine marge (+71,6 millions de FCFA) où les "
    "renouvellements cumulés amortissent entièrement le coût d'acquisition. La marge "
    "nette de 34 % atteinte en année 3 est caractéristique des courtiers digitaux, dont "
    "le coût marginal par contrat tend vers les seuls frais de paiement."))

story += make_table(
    ['Compte de résultat (M FCFA)', 'An 1 (2027)', 'An 2 (2028)', 'An 3 (2029)'],
    [
        ['Commissions d\u2019apport (nouvelles polices)', '20,0', '79,2', '163,1'],
        ['Commissions de gestion (renouvellements)', '0,0', '7,3', '33,3'],
        ['Services B2B aux assureurs', '0,0', '0,0', '14,0'],
        ['Chiffre d\u2019affaires total', '20,0', '86,5', '210,4'],
        ['Charges totales (tableau 8)', '41,0', '83,4', '138,8'],
        ['Résultat net', '-21,0', '+3,1', '+71,6'],
        ['Marge nette', 'n.s.', '3,6 %', '34,0 %'],
    ],
    [0.40, 0.20, 0.20, 0.20],
    aligns=['l', 'r', 'r', 'r'],
    bold_rows={3, 5},
    caption='Tableau 10 — Compte de résultat prévisionnel simplifié 2027-2029.')

story += chart_block('chart4_pnl.png',
    'Figure 4 — Trajectoire financière 2027-2029 : chiffre d\u2019affaires, charges et '
    'résultat net (millions de FCFA).',
    max_h=245)

story += h2_block('6.2 Seuil de rentabilité et trésorerie', para(
    "Le seuil de rentabilité correspond à environ 4 450 contrats actifs par an au taux "
    "de commission moyen de la deuxième année, soit un volume de primes apportées proche "
    "de 490 millions de FCFA. Avec 4 800 polices nouvelles programmées en 2028, ce "
    "point mort est franchi entre le quinzième et le dix-huitième mois d'exploitation "
    "commerciale. La trésorerie reste maîtrisée tout au long de la trajectoire : le "
    "creux maximal — environ 27 millions de FCFA consommés à la fin de la première "
    "année, hors dépenses d'établissement déjà immobilisées — demeure inférieur au "
    "fonds de roulement constitué, ce qui évite tout besoin de financement "
    "relais avant la rentabilité."))

story += h2_block('6.3 Analyse de sensibilité', para(
    "La robustesse du plan a été testée sur trois scénarios d'activité en année 3. "
    "Dans le scénario pessimiste, les volumes sont dégradés de 35 % — équivalent d'un "
    "retard de six mois dans la signature des partenariats assureurs ou d'une "
    "concurrence accrue sur l'acquisition digitale — et le projet demeure bénéficiaire "
    "grâce à la structure de coûts partiellement variables. Dans le scénario optimiste, "
    "l'effet réseau du module scolaire et des cautions BTP accélère l'acquisition de "
    "30 %, portant le résultat net à plus de 113 millions de FCFA."))

story += make_table(
    ['Scénario (An 3, 2029)', 'Chiffre d\u2019affaires', 'Résultat net', 'Marge nette'],
    [
        ['Pessimiste — volumes -35 %', '136,8 M FCFA', '+14,5 M FCFA', '10,6 %'],
        ['Central — plan de référence', '210,4 M FCFA', '+71,6 M FCFA', '34,0 %'],
        ['Optimiste — volumes +30 %', '273,5 M FCFA', '+113,5 M FCFA', '41,5 %'],
    ],
    [0.40, 0.20, 0.20, 0.20],
    aligns=['l', 'r', 'r', 'r'],
    caption='Tableau 11 — Sensibilité du résultat net d\u2019année 3 aux volumes.')

# --- 7. Financement & feuille de route ---------------------------------------
story += h1_block('7. Plan de financement et feuille de route', para(
    "Le financement de 50 millions de FCFA combine quatre sources complémentaires, "
    "calibrées pour préserver l'autonomie de la fondatrice et la capacité à lever de "
    "nouveaux fonds si l'expansion régionale s'accélère. L'apport fondateur et les "
    "fonds d'amorçage privés couvrent l'essentiel des dépenses d'établissement, tandis "
    "que la dette bancaire — adossée aux immobilisations logicielles et aux programmes "
    "publics de garantie des PME — finance le fonds de roulement. Les subventions et "
    "concours d'innovation dédiés à l'inclusion financière, nombreux dans l'espace "
    "CEMAC et au sein des programmes d'appui à l'entrepreneuriat numérique, "
    "complètent le montage sans dilution supplémentaire."))

story += make_table(
    ['Source de financement', 'Montant (M FCFA)', 'Part'],
    [
        ['Apport de la fondatrice', '5,0', '10 %'],
        ['Business angels et fonds d\u2019amorçage', '20,0', '40 %'],
        ['Subventions, concours d\u2019innovation et incubation', '10,0', '20 %'],
        ['Dette bancaire et financement d\u2019actifs', '15,0', '30 %'],
        ['Total', '50,0', '100 %'],
    ],
    [0.56, 0.24, 0.20],
    aligns=['l', 'r', 'c'],
    bold_rows={4},
    caption='Tableau 12 — Plan de financement du démarrage.')

story.append(para(
    "La feuille de route opérationnelle séquence le déploiement en quatre phases "
    "nécessairement ordonnées : aucune commercialisation n'est possible avant "
    "l'obtention de l'agrément, et l'extension à de nouvelles branches suppose la "
    "stabilité technique du socle auto-santé-scolaire. Chaque phase est assortie "
    "d'indicateurs de passage mesurables, qui servent de jalons au dialogue avec les "
    "investisseurs."))

story += make_table(
    ['Phase', 'Période', 'Jalons clés'],
    [
        ['1. Fondations', 'T1-T2 2027',
         'Constitution de la société, dépôt du dossier d\u2019agrément ASAC, mise en '
         'place de la garantie financière, signature de 3 conventions de courtage, '
         'développement du MVP.'],
        ['2. Lancement', 'T3-T4 2027',
         'Mise en ligne des applications (auto, santé, scolaire) à Yaoundé et Douala, '
         'campagne de lancement, objectif : 1 400 polices souscrites.'],
        ['3. Extension', '2028',
         'Ouverture des modules Pro & BTP et maritime/import, déploiement du réseau '
         'd\u2019affiliés, intégration de 2 assureurs supplémentaires, franchissement '
         'du point mort.'],
        ['4. Consolidation', '2029',
         'Lancement des services B2B aux assureurs, optimisation du taux de '
         'renouvellement, préparation de la certification multi-pays en vue du déploiement '
         'zone CIMA.'],
    ],
    [0.17, 0.14, 0.69],
    aligns=['l', 'l', 'l'],
    caption='Tableau 13 — Feuille de route opérationnelle 2027-2029.')

# --- 8. Risques ---------------------------------------------------------------
story += h1_block('8. Risques et mesures d\u2019atténuation', para(
    "Le registre des risques identifie les six aléas les plus susceptibles d'affecter "
    "la trajectoire, avec pour chacun une évaluation qualitative et la mesure "
    "d'atténuation intégrée au plan. Deux d'entre eux — le calendrier d'agrément et la "
    "dépendance aux compagnies partenaires — sont structurants et font l'objet d'un "
    "suivi mensuel par la direction ; les quatre autres sont opérationnels et relèvent "
    "des processus internes de la plateforme."))

story += make_table(
    ['Risque', 'Probabilité', 'Impact', 'Mesure d\u2019atténuation'],
    [
        ['Retard d\u2019obtention de l\u2019agrément ASAC', 'Moyenne', 'Élevé',
         'Dossier préparé avec conseil juridique spécialisé dès 2026 ; phase de '
         'pré-lancement sans intermédiation (comparateur, contenu pédagogique) pour '
         'construire l\u2019audience.'],
        ['Dépendance aux compagnies partenaires', 'Élevée', 'Élevé',
         'Diversifier 4 à 6 partenaires dès l\u2019An 1 sur toutes les branches ; '
         'conventions pluriannuelles ; aucune compagnie ne doit dépasser 35 % des '
         'commissions.'],
        ['Fraude documentaire et identité', 'Moyenne', 'Moyen',
         'Attestations numériques à QR code vérifiable ; contrôle des pièces par le '
         'back-office ; signalement croisé avec les compagnies.'],
        ['Cybersécurité et données personnelles', 'Moyenne', 'Élevé',
         'Chiffrement de bout en bout, hébergement sécurisé, conformité à la loi '
         'n° 2010/012 sur la cybersécurité, audits annuels indépendants.'],
        ['Irruption de concurrents (canaux directs, agrégateurs)', 'Moyenne', 'Moyen',
         'Différenciation par la niche BTP/maritime, la notation collaborative et '
         'l\u2019éducation financière ; vitesse d\u2019exécution produit.'],
        ['Évolution réglementaire et tarifaire', 'Faible', 'Moyen',
         'Veille ASAC/CIMA permanente ; modèle de commissions ajustable par simple '
         'mise à jour des conventions ; marge de prudence dans les projections.'],
    ],
    [0.24, 0.11, 0.10, 0.55],
    aligns=['l', 'c', 'c', 'l'],
    font_size=9,
    caption='Tableau 14 — Registre des risques principaux du projet.')

# --- 9. Conclusion ------------------------------------------------------------
story += h1_block('9. Conclusion', para(
    "Ce business plan établit que MboaAssur conjugue trois conditions rarement réunies "
    "dans un même projet entrepreneurial camerounais : un marché réel, chiffré et en "
    "croissance continue depuis quatre exercices, porté par des statistiques publiques "
    "vérifiables ; un modèle économique éprouvé, celui du courtage d'apport, dont la "
    "rémunération est intégrée dans la chaîne de valeur assurancielle sans alourdir le "
    "coût de l'assuré ; et un cadre réglementaire — le Code CIMA — qui protège les "
    "intermédiaires agréés tout en offrant une trajectoire d'expansion naturelle vers "
    "quatorze États. La structure de coûts, dominée par des charges semi-variables, "
    "borne la perte d'apprentissage à 21 millions de FCFA et conduit à une rentabilité "
    "dès la deuxième année pour un investissement de 50 millions de FCFA."))
story.append(para(
    "Au-delà des chiffres, le projet répond à un enjeu de politiques publiques "
    "clairement identifié par le régulateur lui-même : porter la pénétration de "
    "l'assurance au-delà de 1 % du PIB. En rendant la souscription aussi simple qu'un "
    "transfert Mobile Money, en certifiant l'authenticité des attestations et en "
    "éduquant le public, MboaAssur se positionne comme l'infrastructure de confiance "
    "dont le marché a besoin pour croître. La priorité immédiate est l'exécution du "
    "calendrier réglementaire : la constitution du dossier d'agrément et la signature "
    "des trois premières conventions de courtage conditionnent le lancement commercial "
    "au troisième trimestre 2027, et constituent l'objet du plan de financement "
    "présenté ici."))

# --- Sources ------------------------------------------------------------------
story += h1_block('Sources et références', para(
    "Les données de marché citées dans ce document proviennent des publications "
    "suivantes. Les statistiques de l'ASAC sont citées telles que relayées par la "
    "presse économique spécialisée et les fédérations professionnelles ; les montants "
    "projetés relèvent des hypothèses du présent business plan.", 'body'))

BIB = [
    "ASAC (Agence de Régulation et de Contrôle des Assurances) — chiffre d'affaires "
    "2023 du marché camerounais : 274,65 milliards de FCFA, cité par la Fédération "
    "Afro-Asiatique des Assureurs et Réassureurs (FAIR), fiche marché Cameroun, 2024.",
    "Cameroon Tribune (12 juin 2024), citant l'ASAC — primes émises 2023 : 272,55 "
    "milliards de FCFA (provisionnel) ; Business in Cameroon (10 juin 2024) — "
    "croissance de 6 % en 2023, pénétration estimée à 0,7 %.",
    "Investir au Cameroun (19 février 2026) — « Secteur des assurances au Cameroun : "
    "une solidité confirmée en 2024 avec 288,7 milliards FCFA de chiffre d'affaires », "
    "données ASAC.",
    "Business Finance (12 février 2025) — branche vie 2024 : 97,1 milliards de FCFA, "
    "+9,3 % ; EcoMatin et Financial Afrik (25 mars 2026) — marché 2025 proche de "
    "300 milliards de FCFA, branche vie 102,67 milliards (+5,5 %).",
    "Conseil national du crédit et financier (CNEF), Cameroun — primes non-vie : "
    "168,63 milliards de FCFA en 2022, 185,78 milliards en 2023 (+10,17 %).",
    "FANAF (Fédération des Sociétés d'Assurances de Droit National des États membres) "
    "— collecte 2023 : 2 041,2 milliards de FCFA, citée par 221 Assurances "
    "(11 avril 2025).",
    "CIMA (Conférence Interafricaine des Marchés d'Assurances) — Code des assurances, "
    "art. 506, 508 et 530 (agrément et exercice du courtage) ; réforme des capitaux "
    "minimums des compagnies (5 Mds FCFA non-vie, 3 Mds FCFA vie), Financial Afrik et "
    "Agence Ecofin.",
    "Atlas Magazine — marché de l'assurance au Cameroun et en zone CIMA : taux de "
    "pénétration 0,91 %, densité 13,8 USD par habitant.",
    "BVM-AC — composition du dossier d'agrément des courtiers d'assurance au "
    "Cameroun : garantie financière d'un montant au moins égal à 10 millions de FCFA.",
    "OCDE — Global Insurance Market Trends 2025 : pénétration moyenne de 6,2 % dans "
    "les pays de l'OCDE en 2024.",
    "ACFI Solutions (2025), AgentCo (2026), Smalltox — pratiques de rémunération du "
    "courtage : commissions d'apport de 10 % à 30 % selon les branches, commissions "
    "de gestion de 5 % à 10 %.",
    "Mballa Andela Rose — Étude fonctionnelle, technologique et business de la "
    "plateforme MboaAssur (dossiers 1 à 6), Université Matemfen de Yaoundé, 2025-2026.",
]
for b in BIB:
    story.append(Paragraph(_fr(b), S['biblio']))

# ================================================================== build
doc = TocDocTemplate(
    OUT_BODY, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
    title=DOC_TITLE, author='Z.ai', creator='Z.ai',
    subject='Business plan du courtier digital MboaAssur — marché, modèle de revenus, '
            'coûts et projections 2027-2029',
)
doc._body_start = 2
doc.multiBuild(story, onFirstPage=_page_decor, onLaterPages=_page_decor)
print('OK — corps généré :', OUT_BODY)


