# -*- coding: utf-8 -*-
"""Unirances — Plan de Conception et Développement (corps du document, ReportLab)."""
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

OUT_BODY = '/home/z/my-project/scripts/assets/cd_body.pdf'
ASSETS = '/home/z/my-project/scripts/assets'
DOC_TITLE = 'Unirances — Plan de Conception et Développement'
FOOTER_LINE = 'Mballa Andela Rose — Fondatrice, projet Unirances'

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
            # Le marqueur est re-rencontré à chaque passe de multiBuild :
            # on prend TOUJOURS sa page du passage courant (le sommaire
            # peut passer de 1 à 2 pages entre les passes).
            self._body_start = self.page
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            display_page = self.page - getattr(self, '_body_start', 2) + 1
            # Sommaire imprimé : chapitres uniquement (niveau 0) — garantit
            # une page de sommaire unique et une numérotation stable.
            # Les sous-sections restent navigables via les signets PDF.
            if level == 0:
                self.notify('TOCEntry', (level, text, display_page, key))
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=False)

ROMAN = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v', 6: 'vi'}

def _page_decor(canvas, doc):
    canvas.saveState()
    canvas.setFont('FreeSerif', 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, PAGE_H - 0.55 * inch, DOC_TITLE)
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(MARGIN, PAGE_H - 0.62 * inch, PAGE_W - MARGIN, PAGE_H - 0.62 * inch)
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 0.62 * inch, PAGE_W - MARGIN, 0.62 * inch)
    canvas.setFont('FreeSerif', 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, 0.45 * inch, FOOTER_LINE)
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
    return txt.replace(' — ', '\u00a0— ')

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
    "Unirances (anciennement MboaAssur) est une plateforme d'assurance digitale conçue "
    "pour le marché camerounais et la zone CIMA, qui regroupe la comparaison des offres, "
    "la souscription en ligne avec paiement Mobile Money, la délivrance d'attestations "
    "numériques certifiées par QR code et la déclaration simplifiée de sinistres. Le "
    "projet dispose déjà de deux actifs majeurs : un ensemble de dossiers de conception "
    "fonctionnelle et technologique d'environ 515 pages couvrant plus de 120 écrans, et "
    "un business plan chiffré aux sources officielles (ASAC, FANAF, CIMA) qui établit la "
    "viabilité économique du modèle sur 2027-2029. Le présent document fait la "
    "synthèse opérationnelle des deux : il organise la transformation de la conception "
    "en produit commercial à travers un plan d'exécution en neuf phases, jalonné de "
    "points de décision GO/NO-GO, étalé de novembre 2026 à décembre 2028.", 'lead'))

story += callout_row([
    ('9 phases', 'de cadrage à l\u2019industrialisation, jalonnées GO / NO-GO'),
    ('26 mois', 'novembre 2026 à décembre 2028'),
    ('50 M FCFA', 'budget de développement aligné sur le business plan'),
    ('T3 2027', 'lancement commercial (trajectoire BP : 20 M FCFA en an 1)'),
])

story.append(para(
    "La démarche retenue est hybride : la conception produit et technique suit une "
    "logique séquentielle de cycle en V, tandis que le développement s'exécute en "
    "sprints agiles de deux semaines avec démonstration systématique. La conformité "
    "réglementaire — agrément d'intermédiaire auprès de l'ASAC, garantie financière "
    "prévue par l'article 530 du Code CIMA, conventions d'apport avec les compagnies — "
    "est traitée comme le chemin critique du projet et démarre dès la septième semaine, "
    "en parallèle de la conception. Le budget total de 50 millions de FCFA identifié "
    "par le business plan est réparti par phase et par poste, avec une réserve de "
    "12 % pour les imprévus. Chaque phase se conclut par des critères de sortie "
    "explicites : un jalon ne franchit le seuil GO que si ces critères sont remplis, "
    "ce qui protège le financement et évite l'engagement de coûts sur des bases "
    "fragiles."))

story.append(para(
    "Le document se lit de deux manières. Le chapitre 3 donne la vue d'ensemble du "
    "calendrier avec le diagramme de Gantt et la table de synthèse des neuf phases. "
    "Les chapitres 4 à 12 détaillent ensuite chaque phase selon une structure "
    "identique — objectifs, activités clés, livrables, jalon et critères de sortie — "
    "de sorte que chaque responsable peut extraire directement sa feuille de route. "
    "Le chapitre 13 regroupe enfin les moyens transverses : équipe et effectifs, "
    "budget détaillé, gouvernance de pilotage et registre des risques avec leurs "
    "mesures d'atténuation."))

# --- 2. Périmètre, référentiels et démarche -----------------------------------
story += h1_block('2. Périmètre, référentiels et démarche', para(
    "Le plan couvre l'intégralité du cycle de mise en oeuvre du projet : cadrage "
    "stratégique, conception produit et technique, mise en conformité réglementaire, "
    "développement du produit minimum viable (MVP), qualification qualité et "
    "sécurité, pilote terrain, lancement commercial et industrialisation. Il ne "
    "revient ni sur le diagnostic de marché ni sur les projections financières, qui "
    "sont traités dans le business plan 2027-2029 auquel il se réfère en permanence. "
    "Son périmètre de décision s'arrête à la fin de l'année 2028, point où le "
    "business plan attend un chiffre d'affaires de l'ordre de 86,5 millions de FCFA "
    "et un résultat net positif confirmé."))

story += h2_block('2.1 Les fondations documentaires du projet', para(
    "Le plan s'appuie sur les documents déjà produits par le projet, dont il "
    "consolide et hiérarchise les enseignements. Cette table établit la traçabilité "
    "entre les référentiels existants et leur usage dans le plan d'exécution :"))
story += make_table(
    ['Référentiel', 'Contenu', 'Apport au plan d\u2019exécution'],
    [
        ['Étude fonctionnelle et dossiers 4 à 6',
         'Parcours détaillés : devis, souscription et attestation digitale, contrats, '
         'profil et notifications, sinistres',
         'Périmètre fonctionnel du MVP et spécifications des écrans (chapitres 5 et 8)'],
        ['Dossier de conception final (312 p.)',
         'Vision produit, règles métier, architecture fonctionnelle, feuille de route initiale',
         'Règles métier priorisées, harmonisation des parcours, base du design system'],
        ['Business plan 2027-2029',
         'Marché chiffré ASAC/FANAF/CIMA, modèle de commissions d\u2019apport, projections, '
         'besoin de 50 M FCFA',
         'Cadre financier, cibles commerciales et indicateurs de succès (chapitres 11 à 13)'],
        ['Cadre réglementaire CIMA / ASAC',
         'Code CIMA (art. 506, 508, 530), régime des intermédiaires, garantie financière',
         'Feuille de route de conformité et partenariats (chapitre 7)'],
    ],
    [0.24, 0.40, 0.36],
    caption='Table 1 — Les référentiels du projet et leur usage dans le plan.')

story += h2_block('2.2 Une démarche hybride : séquentielle pour concevoir, agile pour construire', para(
    "La conception ne s'improvise pas en mode agile : les parcours de souscription et "
    "de sinistre touchent des obligations réglementaires et des règles métier qui "
    "exigent une spécification stable avant développement. Le plan adopte donc une "
    "démarche en deux régimes. Les phases 0 à 2 avancent en logique séquentielle avec "
    "des livrables de conception validés formellement. À partir de la phase 4, le "
    "projet bascule en sprints de deux semaines, chaque sprint livrant un incrément "
    "démontrable de la plateforme. Entre les deux régimes, quatre jalons GO/NO-GO "
    "structurent la prise de décision :"))
story += make_table(
    ['Jalon', 'Moment', 'Décision engagée', 'Conditions minimales'],
    [
        ['J0 — GO conception', 'décembre 2026',
         'Lancement des phases 1 et 2 (produit et technique)',
         'Financement noyau bouclé, MVP priorisé, équipe de conception en place'],
        ['J1 — GO développement', 'février 2027',
         'Engagement des sprints de développement du MVP',
         'Maquettes validées, architecture choisie, POC Mobile Money concluant'],
        ['J2 — GO pilote', 'juin 2027',
         'Ouverture de la bêta privée auprès des utilisateurs pilotes',
         'MVP complet, tests critiques au vert, au moins une convention d\u2019apport'],
        ['J3 — GO lancement', 'septembre 2027',
         'Ouverture commerciale grand public',
         'KPI du pilote atteints, agrément effectif, deux compagnies partenaires'],
    ],
    [0.17, 0.13, 0.33, 0.37],
    caption='Table 2 — Les quatre jalons GO/NO-GO du plan.')
story.append(para(
    "Un NO-GO n'est jamais un abandon : il déclenche un plan de reprise ciblé sur les "
    "critères manquants, avec une réévaluation à date fixe. Ce mécanisme est le "
    "principal garde-fou financier du projet, car il plafonne l'exposition de chaque "
    "étape au montant de sa phase et empêche l'effet d'engrenage des dépenses."))

# --- 3. Feuille de route : vue d'ensemble --------------------------------------
story += h1_block('3. Feuille de route : vue d\u2019ensemble', para(
    "Le plan d'exécution s'étale sur vingt-six mois, de novembre 2026 à décembre "
    "2028, et se décompose en neuf phases dont cinq sont partiellement parallèles. "
    "Le diagramme ci-dessous matérialise cet enchaînement : les phases de conception "
    "(P0 à P2) s'ouvrent dès la fin 2026, la construction (P3 à P5) occupe le premier "
    "semestre 2027, puis le lancement et la montée en charge (P6 à P8) conduisent la "
    "plateforme jusqu'à son régime de croisière fin 2028. Les losanges noirs "
    "marquent les quatre jalons de décision décrits au chapitre précédent."))
story += chart_block('cd_gantt.png',
    'Figure 1 — Feuille de route des neuf phases (novembre 2026 à décembre 2028).',
    max_h=300)
story += make_table(
    ['Phase', 'Période', 'Durée', 'Jalon de sortie'],
    [
        ['P0 · Cadrage et financement', 'nov. - déc. 2026', '4 semaines',
         'J0 — GO conception'],
        ['P1 · Conception produit et UX', 'déc. 2026 - févr. 2027', '6 semaines',
         'Maquettes validées'],
        ['P2 · Conception technique', 'déc. 2026 - févr. 2027', '8 semaines',
         'J1 — GO développement'],
        ['P3 · Conformité et partenariats', 'janv. - juin 2027', '20 semaines',
         'Agrément + 2 conventions'],
        ['P4 · Développement du MVP', 'févr. - juin 2027', '16 semaines (8 sprints)',
         'MVP complet'],
        ['P5 · Qualité, sécurité et tests', 'juin - juil. 2027', '4 semaines',
         'J2 — GO pilote'],
        ['P6 · Pilote terrain', 'juil. - sept. 2027', '6 semaines',
         'KPI pilote atteints'],
        ['P7 · Lancement commercial', 'sept. - nov. 2027', '8 semaines',
         'J3 — GO lancement'],
        ['P8 · Industrialisation et V2', 'nov. 2027 - déc. 2028', '14 mois',
         'Trajectoire BP 2028'],
    ],
    [0.30, 0.24, 0.20, 0.26],
    aligns=['l', 'c', 'c', 'l'],
    caption='Table 3 — Synthèse des phases, durées et jalons de sortie.')
story.append(para(
    "Trois recouvrements structurent l'efficacité du calendrier. D'abord, la "
    "conception produit (P1) et la conception technique (P2) avancent en parallèle "
    "et se nourrissent mutuellement : chaque écran maquetté est arbitré contre ses "
    "exigences techniques, ce qui évite l'effet tunnel. Ensuite, la conformité "
    "réglementaire (P3) démarre avant même la fin de la conception, car les délais "
    "administratifs d'agrément et de signature des conventions d'apport ne se "
    "compressent pas : c'est le chemin critique du projet. Enfin, la phase de "
    "qualité (P5) recouvre les deux derniers sprints de développement, les tests de "
    "régression accompagnant chaque incrément livré. Cette organisation tasse la "
    "durée totale à vingt-six mois tout en conservant des responsabilités claires."))

# --- 4. Phase 0 — Cadrage et financements --------------------------------------
story += h1_block('4. Phase 0 — Cadrage et financement', para(
    "La phase 0 transforme l'intention en organisation de projet. Son objectif est "
    "double : définir précisément ce qui sera construit en priorité, et sécuriser les "
    "moyens de le construire. Elle s'exécute en quatre semaines, de novembre à "
    "décembre 2026, par une équipe resserrée de deux à trois personnes — la fondatrice "
    "porteuse du projet, le futur directeur technique et un consultant financier "
    "ponctuel. Son produit essentiel est un périmètre de MVP réaliste, débarrassé de "
    "l'ambition des 120 écrans de l'étude complète, et un financement débloqué."))
story += callout_row([
    ('4 semaines', 'novembre - décembre 2026'),
    ('2 à 3', 'personnes mobilisées'),
    ('28 écrans', 'périmètre MVP priorisé sur 120'),
    ('50 M FCFA', 'financement à boucler (J0)'),
])
story += h2_block('4.1 Activités clés', para(
    "Les activités de cadrage s'enchaînent en quatre semaines structurées, chacune "
    "produisant un livrable contrôlable :"))
story += make_table(
    ['Activité', 'Livrable', 'Responsable', 'Durée'],
    [
        ['Atelier de priorisation MoSCoW des 120 écrans',
         'Périmètre MVP (28 écrans, 6 modules)', 'Fondatrice + CTO', '1 semaine'],
        ['Consolidation des 46 règles métier en spécifications',
         'Backlog produit initial estimé', 'CTO', '1 semaine'],
        ['Finalisation du dossier de financement (apport, investisseur, subventions tech)',
         'Plan de financement 50 M FCFA', 'Fondatrice', '3 semaines'],
        ['Recrutement du noyau (développeur back, développeur front, designer)',
         'Lettres d\u2019engagement, planning', 'Fondatrice + CTO', '3 semaines'],
        ['Mise en place des outils (dépôt Git, gestion de projet, espaces de travail)',
         'Environnement de collaboration', 'CTO', '1 semaine'],
    ],
    [0.38, 0.26, 0.20, 0.16],
    aligns=['l', 'l', 'l', 'c'],
    caption='Table 4 — Activités de la phase 0.')
story.append(para(
    "La priorisation suit la méthode MoSCoW appliquée aux six modules de l'étude "
    "fonctionnelle. Entrent dans le MVP le comparateur et les devis, la souscription "
    "avec paiement Mobile Money et attestation digitale, l'espace contrats avec "
    "notifications de renouvellement, la déclaration de sinistre par photo et le "
    "back-office d'administration. Sortent du MVP, au profit des phases ultérieures, "
    "l'espace Pro et BTP avec les cautions de soumission, l'assurance maritime et "
    "import, la diaspora en tant que module dédié et les fonctions sociales avancées. "
    "Cette discipline de périmètre est la première protection du calendrier : elle "
    "replace les ambitions différenciantes de la plateforme après la preuve de "
    "concept commerciale, sans jamais les sacrifier."))
story += h2_block('4.2 Critères de sortie et jalon J0', para(
    "La phase 0 est close au jalon J0 lorsque trois conditions sont réunies "
    "simultanément. Primo, le plan de financement est bouclé ou sécurisé à au moins "
    "60 % — les fonds couvrant les phases 1 et 2 sont engagés, le solde fait l'objet "
    "d'engagements conditionnés aux jalons suivants. Secundo, le périmètre MVP est "
    "signé par la fondatrice et le CTO, avec un backlog estimé et un calendrier de "
    "huit sprints. Tertio, le noyau de l'équipe de conception est engagé par écrit. "
    "À défaut, le démarrage des phases 1 et 2 est différé de quatre semaines maximum, "
    "le temps de combler le ou les critères manquants."))

# --- 5. Phase 1 — Conception produit et UX -------------------------------------
story += h1_block('5. Phase 1 — Conception produit et UX', para(
    "Cette phase traduit les 515 pages de conception théorique en interfaces "
    "exécutables. Son enjeu n'est pas de redessiner le produit mais de le rendre "
    "réaliste : chaque parcours issu des dossiers est éprouvé contre les contraintes "
    "réelles du terrain camerounais — téléphones d'entrée de gamme, connexions 3G "
    "irrégulières, usagers découvrant l'assurance. La phase mobilise quatre personnes "
    "pendant six semaines et produit le design system, les maquettes haute fidélité "
    "du parcours MVP et un prototype cliquable testé par de futurs utilisateurs."))
story += h2_block('5.1 Activités clés', para(
    "Le travail s'organise en quatre chantiers séquencés, du socle graphique aux "
    "tests utilisateurs :"))
story += bullets([
    "<b>Design system Unirances</b> : tokens graphiques (typographies, palette bleue "
    "dérivée de la charte du projet, espacements), bibliothèque de composants "
    "réutilisables (champs, cartes produits, boutons de paiement, badges d'état), "
    "et règles d'écriture en français simple pour les mentions d'assurance.",
    "<b>Maquettes haute fidélité du parcours MVP</b> : de la recherche de devis à "
    "l'attestation digitale en passant par le paiement Mobile Money et l'espace "
    "contrats, en reprenant écran par écran les spécifications des dossiers 4 à 6.",
    "<b>Harmonisation des parcours divergents</b> : le parcours de sinistre est "
    "figé sur la version en six étapes du dossier final, qui prime sur les "
    "variantes antérieures des dossiers séparés — cette décision lève l'une des "
    "incohérences relevées lors de l'analyse des documents.",
    "<b>Prototype cliquable et tests utilisateurs</b> : mise en situation de douze "
    "profils à Yaoundé et Douala (salariés, commerçants, étudiants, professionnels "
    "du BTP) sur téléphones d'entrée de gamme et connexion 3G, mesure des points "
    "de friction et itération des écrans critiques.",
])
story.append(para(
    "Les tests utilisateurs portent une attention particulière à deux moments : la "
    "compréhension du devis (l'utilisateur doit savoir ce qu'il achète sans appel "
    "d'assistance) et la confiance dans l'attestation numérique (le QR code doit "
    "inspirer plus de confiance qu'un document papier). Les résultats sont notés "
    "dans un rapport de tests qui alimente directement les correctifs de maquettes "
    "avant le jalon J1."))
story += h2_block('5.2 Critères de sortie', para(
    "La phase 1 se conclut quand l'intégralité du parcours MVP est maquettée en "
    "haute fidélité, quand le prototype a été testé par au moins dix utilisateurs "
    "sans blocage majeur non résolu, et quand le design system est publié dans un "
    "dépôt consultable par les développeurs. La mesure de succès est simple : un "
    "développeur doit pouvoir implémenter chaque écran sans poser de question de "
    "conception. Ce critère, apparemment exigeant, est celui qui différencie un "
    "dossier de conception d'un produit délivrable."))

# --- 6. Phase 2 — Conception technique et architecture --------------------------
story += h1_block('6. Phase 2 — Conception technique et architecture', para(
    "L'analyse des dossiers de conception avait identifié l'absence de choix "
    "techniques comme la principale lacune du projet : la vision fonctionnelle est "
    "mature, mais aucune stack, aucune architecture et aucun plan d'intégration "
    "n'étaient fixés. La phase 2 comble ce vide en huit semaines, en parallèle de la "
    "phase 1, avec une équipe de trois personnes (CTO, développeur back senior, "
    "consultant DevOps). Son livrable pivot est le dossier d'architecture technique "
    "(DAT), complété par une preuve de concept du paiement Mobile Money réalisée en "
    "conditions réelles."))
story += h2_block('6.1 Stack technique proposée', para(
    "Les choix suivants privilégient la simplicité opérationnelle, le coût maîtrisé "
    "et l'adéquation au contexte mobile camerounais ; ils seront consolidés dans le "
    "DAT puis mis en oeuvre dès la phase 4 :"))
story += make_table(
    ['Couche', 'Choix proposé', 'Justification'],
    [
        ['Client', 'PWA (Progressive Web App) mobile-first',
         'Installable sans store, poids léger adapté aux forfaits data, une seule '
         'base de code web et mobile'],
        ['Front-end', 'React + TypeScript',
         'Écosystème mature, composants alignés sur le design system, recrutement '
         'facile au Cameroun'],
        ['API et logique métier', 'API REST — Node.js (NestJS) ou Django',
         'Cadres robustes, validations serveur des 46 règles métier, documentation '
         'auto-générée (OpenAPI)'],
        ['Données', 'PostgreSQL + stockage objets (S3 compatible)',
         'Intégrité transactionnelle des contrats, stockage chiffré des pièces '
         'justificatives et attestations'],
        ['Hébergement', 'Cloud avec CDN (région Europe ou Afrique)',
         'Latence maîtrisée depuis Douala et Yaoundé, sauvegardes automatisées, '
         'coût de démarrage inférieur à 150 000 FCFA par mois'],
        ['Livraison', 'CI/CD (GitHub Actions), environnements dev / staging / prod',
         'Déploiements reproductibles, rollbacks rapides, tests automatisés à chaque '
         'commit'],
    ],
    [0.16, 0.30, 0.54],
    caption='Table 5 — Stack technique cible du MVP.')
story += h2_block('6.2 Sécurité, données et intégrations', para(
    "La plateforme traite des données personnelles et financières sensibles : le "
    "socle de sécurité est conçu dès cette phase, non rattrapé après. Le plan "
    "retient les exigences suivantes, détaillées dans le DAT : chiffrement TLS sur "
    "tous les échanges et chiffrement au repos des documents, authentification par "
    "numéro de téléphone avec code à usage unique, journaux d'audit des actions "
    "sensibles, et conformité à la loi camerounaise n° 2010/012 relative à la "
    "protection des données personnelles, avec déclaration auprès de la CNDP avant "
    "tout traitement en production. Côté intégrations, la preuve de concept porte "
    "sur les API de collecte Mobile Money de MTN et d'Orange — point le plus risqué "
    "du MVP — ainsi que sur le mécanisme de vérification des attestations par QR "
    "code. Les échanges avec les compagnies partenaires s'effectuent en version 1 "
    "par échanges de fichiers sécurisés quotidiens, l'interconnexion temps réel "
    "étant repoussée à la phase d'industrialisation."))
story += h2_block('6.3 Critères de sortie et jalon J1', para(
    "La phase 2 s'achève au jalon J1 lorsque le DAT est validé par le comité de "
    "pilotage, que la preuve de concept de paiement a atteint un taux de succès "
    "d'au moins 95 % sur une batterie de tests réels, et que les environnements de "
    "développement et de staging sont opérationnels avec leur chaîne de livraison "
    "continue. C'est également à ce jalon que l'équipe de développement complète "
    "(quatre à six personnes) est engagée, sur la base des estimations du backlog "
    "affinées par le CTO."))

# --- 7. Phase 3 — Conformité réglementaire et partenariats ----------------------
story += h1_block('7. Phase 3 — Conformité réglementaire et partenariats', para(
    "Sans agrément ni conventions d'apport, la plateforme n'encaisse aucune "
    "commission : cette phase est le chemin critique du projet et elle est traitée "
    "comme telle. Elle démarre dès la septième semaine — avant même la fin de la "
    "conception — car les délais administratifs ne se compressent pas, et elle "
    "s'étale sur vingt semaines, de janvier à juin 2027. Elle mobilise la fondatrice, "
    "un conseil juridique spécialisé en droit des assurances OHADA et CIMA, et un "
    "effort commercial permanent auprès des compagnies ciblées."))
story += h2_block('7.1 Le chemin de l\u2019agrément et des conventions', para(
    "Unirances opère comme intermédiaire d'assurance (courtier), statut qui exige "
    "un capital modeste comparé à celui d'une compagnie mais un dossier de "
    "conformité rigoureux. Les étapes suivantes sont engagées séquentiellement dès "
    "que possible, avec recouvrement lorsque le règlement le permet :"))
story += make_table(
    ['Étape', 'Autorité / référence', 'Durée estimée', 'Dépendance'],
    [
        ['Constitution de la société (SARL) et immatriculation',
         'Registre du commerce, OHADA', '2 à 3 semaines', 'Aucune'],
        ['Dépôt du dossier d\u2019agrément d\u2019intermédiaire (courtier)',
         'ASAC — régime des intermédiaires, Code CIMA art. 506-508', '6 à 10 semaines',
         'Société constituée, programme d\u2019activité'],
        ['Constitution de la garantie financière',
         'Code CIMA art. 530 — 10 M FCFA', '3 à 4 semaines',
         'Personne morale, compte bancaire pro'],
        ['Assurance de responsabilité civile professionnelle',
         'Compagnie agréée', '1 à 2 semaines', 'Aucune'],
        ['Conventions d\u2019apport avec 2 à 4 compagnies cibles',
         'SAAR, Activa, SUNU, AREA (cibles des dossiers)', '6 à 12 semaines',
         'Dossier d\u2019agrément déposé, démonstrations'],
        ['Contrat marchand Mobile Money',
         'MTN MoMo / Orange Money', '3 à 5 semaines', 'Société constituée'],
    ],
    [0.34, 0.28, 0.16, 0.22],
    caption='Table 6 — Feuille de route réglementaire et contractuelle.')
story.append(para(
    "L'argumentaire auprès des compagnies est préparé dès la phase 1 et répété "
    "pendant toute la phase : Unirances apporte des clients pré-qualifiés à coût "
    "d'acquisition inférieur au réseau d'agences physiques, sans prétendre au risque "
    "ni aux provisions. Les démonstrations s'appuient sur le prototype cliquable de "
    "la phase 1, bien plus convaincant qu'une présentation théorique. La cible est "
    "d'obtenir au moins deux conventions signées avant l'ouverture du pilote — le "
    "lancement commercial en exigera quatre. La garantie financière de dix millions "
    "de FCFA est constituée de préférence par caution bancaire, dont le coût annuel "
    "(environ 1,2 à 1,5 million de FCFA) est budgété au chapitre 13 ; le dépôt "
    "bloqué reste l'alternative si la banque l'exige."))
story += h2_block('7.2 Critères de sortie', para(
    "Cette phase n'a pas de jalon propre mais deux seuils contraignants pour les "
    "phases aval. Le pilote (phase 6) ne s'ouvre qu'avec au moins une convention "
    "d'apport effective et l'agrément en état d'être délivré ; le lancement "
    "commercial (phase 7) exige l'agrément effectif et deux conventions. En cas de "
    "dérive de plus de six semaines sur ces seuils, le comité de pilotage déclenche "
    "le plan de repli : élargissement du panel de compagnies approchées et "
    "resserrement du périmètre du pilote sur les produits déjà couverts par les "
    "conventions obtenues."))

# --- 8. Phase 4 — Développement du MVP ------------------------------------------
story += h1_block('8. Phase 4 — Développement du MVP', para(
    "Seize semaines, huit sprints de deux semaines, une équipe de six personnes : "
    "c'est le bloc de construction du produit. Chaque sprint livre un incrément "
    "démontrable de la plateforme, passé en revue avec deux utilisateurs référents "
    "et la fondatrice. Le rythme est volontairement régulier — planification le "
    "lundi de sprint impair, revue et rétrospective le vendredi de sprint pair — et "
    "la démonstration de fin de sprint est un engagement public de l'équipe, pas une "
    "option. La Definition of Done d'une fonctionnalité inclut ses tests unitaires, "
    "sa revue de code et sa mise en conformité avec les maquettes validées."))
story += callout_row([
    ('8 sprints', 'sprints de 2 semaines, févr. - juin 2027'),
    ('6 personnes', 'équipe de développement au complet'),
    ('28 écrans', 'périmètre MVP issu de la phase 0'),
    ('≥ 70 %', 'couverture de tests unitaires visée'),
])
story += h2_block('8.1 Le plan de sprints', para(
    "L'ordre des sprints suit la logique de risque : d'abord le socle et les "
    "intégrations à incertitude élevée (paiement Mobile Money), ensuite la chaîne "
    "de valeur commerciale (devis, souscription, attestation), enfin la fidélisation "
    "et l'outillage interne :"))
story += make_table(
    ['Sprint', 'Semaines', 'Périmètre', 'Démonstration de fin de sprint'],
    [
        ['S1', 'S13-S14', 'Socle technique : authentification OTP, profils, '
         'infrastructure CI/CD, données de référence des produits',
         'Inscription et connexion fonctionnelles en staging'],
        ['S2-S3', 'S15-S18', 'Comparateur et moteur de devis multi-compagnies '
         'avec les règles tarifaires des produits Auto et Scolaire',
         'Devis Auto et Scolaire complets sur données réelles'],
        ['S4-S5', 'S19-S22', 'Souscription, paiement Mobile Money (MTN et Orange), '
         'génération de l\u2019attestation et du QR code',
         'Souscription de bout en bout avec paiement de test'],
        ['S6', 'S23-S24', 'Espace « Mes contrats », historique des paiements, '
         'notifications de renouvellement (push et SMS)',
         'Tableau de bord contrats avec alerte d\u2019échéance'],
        ['S7', 'S25-S26', 'Déclaration de sinistre par photo, pièces justificatives, '
         'suivi du statut du dossier',
         'Parcours sinistre en six étapes complet'],
        ['S8', 'S27-S28', 'Back-office : administration des produits, gestion des '
         'dossiers, export vers les compagnies, tableau de bord de reporting',
         'Dossier remonté d\u2019un bout à l\u2019autre (front et back-office)'],
    ],
    [0.10, 0.13, 0.42, 0.35],
    caption='Table 7 — Plan des huit sprints de développement du MVP.')
story += h2_block('8.2 Pratiques d\u2019ingénierie', para(
    "Quatre pratiques non négociables encadrent les sprints. La couverture de tests "
    "unitaires des modules métier est maintenue à au moins 70 % dès le premier "
    "sprint — la rattraper en fin de projet coûte trois fois plus cher. La chaîne "
    "CI/CD exécute tests et vérifications à chaque commit, et aucun code n'entre en "
    "staging sans revue de code. Les intégrations externes (Mobile Money, échanges "
    "assureurs) sont développées contre des simulateurs puis confrontées aux "
    "environnements réels dès que les contrats marchands le permettent. Enfin, un "
    "registre des décisions techniques consigne chaque arbitrage notable, afin que "
    "l'équipe qui rejoindra le projet en phase d'industrialisation comprenne le "
    "pourquoi de chaque choix. Les deux derniers sprints recouvrent la phase de "
    "qualité décrite au chapitre suivant."))
story += h2_block('8.3 Critères de sortie', para(
    "La phase 4 est close lorsque l'ensemble du périmètre MVP est fonctionnel en "
    "staging : parcours de devis, souscription, paiement, attestation, contrats, "
    "sinistres et back-office. Les critères mesurables sont la couverture de tests "
    "unitaires d'au moins 70 % sur les modules métier, l'absence de bug bloquant ou "
    "majeur ouvert sur le parcours critique, et la démonstration de bout en bout "
    "réalisée devant la fondatrice avec des données réelles anonymisées."))

# --- 9. Phase 5 — Qualité, sécurité et tests -------------------------------------
story += h1_block('9. Phase 5 — Qualité, sécurité et tests', para(
    "Quatre semaines de qualification interviennent à cheval sur la fin du "
    "développement et préparent le jalon J2. L'objectif n'est pas de chasser le "
    "zéro défaut — inaccessible — mais de garantir que les parcours qui portent "
    "l'argent et la confiance de l'assuré sont irréprochables : souscrire, payer, "
    "recevoir une attestation valide, déclarer un sinistre. La phase mobilise "
    "l'ingénieur QA, l'équipe de développement pour les correctifs, et un "
    "prestataire externe pour le test d'intrusion."))
story += make_table(
    ['Type de test', 'Objectif', 'Critère de passage'],
    [
        ['Tests unitaires et d\u2019intégration',
         'Valider les 46 règles métier et les connecteurs (MoMo, échanges assureurs)',
         'Couverture ≥ 70 %, 100 % des cas de test d\u2019intégration au vert'],
        ['Tests de bout en bout',
         'Parcourir les scénarios critiques réels de bout en bout',
         '100 % des scénarios critiques passés sur staging'],
        ['Tests de performance',
         'Supporter les pics d\u2019usage sur réseau dégradé',
         'Temps de réponse < 3 s en 3G simulée, 100 utilisateurs simultanés sans '
         'erreur'],
        ['Test d\u2019intrusion externe',
         'Détecter les failles applicatives et d\u2019infrastructure',
         'Aucune vulnérabilité critique ou haute non corrigée'],
        ['Recette métier (UAT)',
         'Faire valider les parcours par la courtière responsable et un panel interne',
         'Validation formelle signée des six modules'],
    ],
    [0.24, 0.42, 0.34],
    caption='Table 8 — Plan de qualification du MVP.')
story.append(para(
    "La sécurité fait l'objet d'une attention singulière parce que la plateforme "
    "détient des pièces d'identité, des données de paiement et des attestations "
    "opposables. Outre le test d'intrusion, la revue de sécurité vérifie le "
    "chiffrement au repos des documents, la politique de conservation des données, "
    "la conformité de la déclaration CNDP et la procédure de gestion d'incident, "
    "qui doit être écrite et testée avant l'ouverture au public. Les correctifs "
    "issus des tests sont priorisés par sévérité et les vulnérabilités critiques "
    "sont traitées sous quarante-huit heures."))
story += h2_block('9.1 Critères de sortie et jalon J2', para(
    "Le jalon J2 ouvre le pilote lorsque tous les critères de passage de la table 8 "
    "sont remplis, qu'au moins une convention d'apport est effective et que le "
    "processus de support client (numéro WhatsApp, procédure de traitement des "
    "réclamations) est opérationnel. Un seul critère manquant suffit à repousser le "
    "pilote d'un cycle de deux semaines — le calendrier global conserve cette "
    "marge."))

# --- 10. Phase 6 — Pilote terrain et itérations -----------------------------------
story += h1_block('10. Phase 6 — Pilote terrain et itérations', para(
    "Le pilote met le produit dans les mains de ses futurs clients avant "
    "l'engagement marketing : une bêta privée de 200 à 500 utilisateurs recrutés "
    "dans le réseau de la fondatrice, sur les campus, dans les PME du BTP et dans "
    "les associations de la diaspora, à Yaoundé et Douala. Deux familles de produits "
    "seulement — Auto et Scolaire — auprès d'une à deux compagnies partenaires : le "
    "pilote cherche la vérité du terrain, pas le volume. Six semaines, des "
    "itérations hebdomadaires, et des indicateurs qui décident du lancement."))
story += callout_row([
    ('≥ 8 %', 'conversion devis → souscription (cible pilote)'),
    ('≥ 95 %', 'paiements Mobile Money aboutis'),
    ('NPS ≥ 40', 'satisfaction nette des bêta-testeurs'),
    ('≤ 48 h', 'délai de correction des bugs majeurs'),
])
story += h2_block('10.1 Déroulement du pilote', para(
    "Les bêta-testeurs sont accompagnés par un canal WhatsApp dédié et leur parcours "
    "est instrumenté : chaque étape du tunnel devis-souscription-paiement est mesurée "
    "pour localiser précisément les abandons. Chaque semaine, l'équipe priorise les "
    "correctifs et ajustements d'usage, livre une itération, et publie un point de "
    "situation aux indicateurs. En parallèle, la phase prépare le lancement : "
    "production des contenus pédagogiques « Assurance Facile » (vidéos courtes sur "
    "les droits des assurés), calendrier de communication, script du support client "
    "et procédures d'escalade vers les compagnies en cas de sinistre sensible. Les "
    "retours qualitatifs sont codifiés dans un registre unique qui alimentera la "
    "roadmap V2 décrite au chapitre 12."))
story += h2_block('10.2 Critères de sortie', para(
    "Le pilote est concluant lorsque les quatre indicateurs ci-dessus sont atteints "
    "sur les deux dernières semaines glissantes du pilote — et non sur la moyenne "
    "globale, pour confirmer la tendance — ainsi que la stabilité technique (aucune "
    "panne de plus d'une heure sur les quinze derniers jours). À défaut, le pilote "
    "est prolongé de deux semaines avec un plan d'action ciblé ; deux prolongations "
    "successives déclenchent une revue stratégique du comité de pilotage sur le "
    "produit lui-même."))

# --- 11. Phase 7 — Lancement commercial -------------------------------------------
story += h1_block('11. Phase 7 — Lancement commercial', para(
    "Le lancement ouvre la plateforme au grand public au troisième trimestre 2027, "
    "en cohérence directe avec le business plan : le chiffre d'affaires de 20 "
    "millions de FCFA de la première année est celui d'un exercice de lancement "
    "partiel, l'année 2028 portant la charge de la trajectoire à 86,5 millions. "
    "Huit semaines pour installer les mécaniques d'acquisition, de support et de "
    "pilotage commercial qui feront la différence entre un lancement événementiel "
    "et une activité durable."))
story += h2_block('11.1 Plan d\u2019acquisition', para(
    "Le mix d'acquisition privilégie les canaux à coût maîtrisé, dans la droite "
    "ligne de l'hypothèse du business plan selon laquelle la pédagogie est le "
    "premier moteur de la pénétration de l'assurance :"))
story += bullets([
    "<b>Lancement événementiel et presse</b> : événement de lancement à Douala et "
    "Yaoundé, relations presse économique locale, démonstration publique du "
    "parcours d'achat et de l'attestation vérifiable par QR code.",
    "<b>Acquisition organique</b> : la série pédagogique « Assurance Facile » "
    "diffusée sur WhatsApp et les réseaux sociaux, optimisation pour les "
    "recherches locales, parrainage entre assurés.",
    "<b>Acquisition payante maîtrisée</b> : campagnes sociales ciblées plafonnées "
    "à un coût par lead de 1 500 FCFA, suspendues dès que le seuil est dépassé, "
    "avec réinvestissement sur les canaux les plus convertissants.",
    "<b>Canal diaspora</b> : le parrainage des proches depuis l'étranger, circuit "
    "d'acquisition à coût quasi nul identifié dans les dossiers de conception.",
    "<b>Support client</b> : WhatsApp et téléphone aux heures de bureau, objectif "
    "de première réponse inférieure à trente minutes, base de connaissances "
    "évolutive.",
])
story += h2_block('11.2 Pilotage commercial et critères de sortie', para(
    "Le pilotage hebdomadaire repose sur un tableau de bord unique : polices "
    "actives, commissions facturées aux compagnies, taux de renouvellement des "
    "échéances, coût d'acquisition et réclamations clients. Les cibles à trois mois "
    "du lancement sont de 500 polices actives, un chiffre d'affaires de commissions "
    "cumulé d'au moins 4 millions de FCFA, deux nouvelles conventions d'apport "
    "signées et un coût d'acquisition par client inférieur à 2 000 FCFA. La phase 7 "
    "se clôt lorsque ces cibles sont atteintes ou lorsque leur trajectoire confirme "
    "l'atteinte à M+4 ; le projet bascule alors en régime d'industrialisation "
    "décrit au chapitre suivant, avec une revue trimestrielle systématique de "
    "l'écart au business plan."))

# --- 12. Phase 8 — Industrialisation et évolutions ---------------------------------
story += h1_block('12. Phase 8 — Industrialisation et évolutions', para(
    "La phase 8, la plus longue du plan (quatorze mois, de novembre 2027 à "
    "décembre 2028), transforme un produit lancé en plateforme qui scale. Elle "
    "mène de front trois chantiers : la consolidation opérationnelle (disponibilité, "
    "support, qualité de service), l'enrichissement produit selon la roadmap V2, et "
    "la préparation de l'expansion régionale au sein de la zone CIMA, où le cadre "
    "réglementaire commun quatorze États rend le modèle directement réplicable."))
story += h2_block('12.1 La roadmap produit V2', para(
    "Les évolutions sont priorisées sur la base du registre des retours du pilote "
    "et du lancement, puis arbitrées en comité produit mensuel :"))
story += bullets([
    "<b>Interconnexion temps réel avec les compagnies</b> : passage des échanges "
    "de fichiers quotidiens à des API intégrées, réduisant les délais d'émission "
    "des attestations et de remontée des sinistres.",
    "<b>Espace Pro et BTP complet</b> : cautions de soumission pour les marchés "
    "publics et assurances maritimes et import — les segments à forte valeur "
    "ajoutée identifiés dans l'étude fonctionnelle, porteurs de commissions "
    "moyennes supérieures.",
    "<b>Assistant intelligent de devis</b> : pré-remplissage assisté, lecture des "
    "documents (carte grise, attestation précédente) et recommandation de "
    "garanties, pour réduire encore le temps de souscription.",
    "<b>Application native</b> : envisagée seulement si les données d'usage "
    "démontrent un plafond de la PWA (rétention, notifications), afin de ne pas "
    "dilater la dette de maintenance avant l'heure.",
    "<b>Préparation multi-pays</b> : étude de marché Gabon et Congo, cartographie "
    "des compagnies partenaires régionales et conception d'une architecture "
    "multi-pays (référentiels produits et tarifs par marché).",
])
story += h2_block('12.2 Jalons 2028 et critères de sortie', para(
    "L'année 2028 est jalonnée de quatre revues trimestrielles : au premier "
    "trimestre, l'interconnexion temps réel avec au moins deux compagnies et "
    "l'ouverture de l'espace Pro et BTP ; au deuxième, dix mille polices cumulées "
    "et la bêta de l'assistant de devis ; au troisième, la conclusion de l'étude "
    "multi-pays avec un plan d'entrée chiffré pour un premier marché ; au "
    "quatrième, la revue annuelle de l'écart au business plan, dont la cible "
    "centrale est un chiffre d'affaires de l'ordre de 86,5 millions de FCFA et un "
    "résultat net positif confirmé. La disponibilité de la plateforme est pilotée "
    "sur un objectif de service de 99,5 %, avec 20 % de la capacité de "
    "développement systématiquement allouée à la dette technique et à la "
    "fiabilité."))

# --- 13. Équipe, gouvernance, budget et risques -------------------------------------
story += h1_block('13. Équipe, gouvernance, budget et risques', para(
    "Ce dernier chapitre rassemble les moyens transverses du plan : qui fait quoi "
    "et quand, avec quel argent, sous quelle gouvernance, et contre quels risques. "
    "Il est le chapitre de référence du comité de pilotage, qui s'y reportera à "
    "chaque jalon pour vérifier que les moyens annoncés restent alignés sur les "
    "besoins réels du projet."))

story += h2_block('13.1 Équipe et effectifs', para(
    "L'équipe cœur croît par paliers calés sur les phases : deux personnes au "
    "cadrage, quatre à six en conception, six en développement, huit à dix au "
    "pilote et au lancement, puis douze en régime d'industrialisation. Certains "
    "rôles sont externalisés au démarrage — conseil juridique, design en "
    "mi-temps, DevOps — puis internalisés lorsque la charge le justifie :"))
story += chart_block('cd_effectifs.png',
    'Figure 2 — Effectifs de l\u2019équipe cœur sur la durée du plan.',
    max_h=230)
story += make_table(
    ['Rôle', 'Arrivée', 'Mission principale'],
    [
        ['Fondatrice — courtière responsable', 'S1',
         'Vision produit, relations compagnies, conformité, lancement'],
        ['Directeur technique (CTO)', 'S1',
         'Architecture, équipe de développement, choix techniques'],
        ['Développeur back-end', 'S5', 'API, règles métier, intégrations MoMo et assureurs'],
        ['Développeur front-end / PWA', 'S5', 'Interfaces, design system, performance mobile'],
        ['Designer UX/UI (mi-temps)', 'S5', 'Maquettes, tests utilisateurs, évolutions d\u2019usage'],
        ['Conseil juridique et conformité (externe)', 'S7',
         'Dossier d\u2019agrément, conventions, contrats, CNDP'],
        ['Ingénieur QA', 'S20', 'Plan de tests, automatisation, recette métier'],
        ['Responsable croissance et communication', 'S30',
         'Acquisition, contenus pédagogiques, support client'],
        ['Support client (2 postes)', 'S35', 'WhatsApp et téléphone, traitement des réclamations'],
        ['DevOps / data (mi-temps)', 'T1 2028', 'Fiabilité, supervision, reporting décisionnel'],
    ],
    [0.34, 0.12, 0.54],
    aligns=['l', 'c', 'l'],
    caption='Table 9 — Plan de recrutement et missions par rôle.')

story += h2_block('13.2 Budget de développement', para(
    "Le budget total de 50 millions de FCFA, identifié par le business plan comme "
    "besoin de financement initial, est réparti en six postes dont une réserve de "
    "12 % — proportion minimale recommandée pour un projet à intégrations "
    "externes. La garantie financière prévue par l'article 530 du Code CIMA est "
    "constituée par caution bancaire, dont le coût annuel est porté par le poste "
    "conformité ; le dépôt bloqué de dix millions resterait une alternative "
    "financée hors de ce budget opérationnel :"))
story += chart_block('cd_budget.png',
    'Figure 3 — Répartition du budget de développement de 50 millions de FCFA.',
    max_h=240)
story += make_table(
    ['Poste budgétaire', 'Montant', 'Contenu principal'],
    [
        ['Équipe produit et tech', '18 M FCFA',
         'Salaires et charges de l\u2019équipe de développement sur la période de '
         'construction (phases 1 à 5)'],
        ['Conformité et juridique', '8 M FCFA',
         'Constitution, dossier d\u2019agrément, caution de la garantie financière, '
         'RC professionnelle, conseil CNDP'],
        ['Pilote et lancement commercial', '8 M FCFA',
         'Bêta, événement de lancement, communication, acquisition payante du '
         'premier trimestre'],
        ['Infrastructure et outils', '6 M FCFA',
         'Hébergement cloud, CI/CD, licences, SMS et notifications (26 mois)'],
        ['Réserve pour imprévus', '6 M FCFA',
         '12 % du budget — déclenchée sur décision du comité de pilotage'],
        ['Partenariats et intégrations', '4 M FCFA',
         'Frais de tests MoMo, outillage des échanges assureurs, déplacements et '
         'démonstrations'],
    ],
    [0.28, 0.14, 0.58],
    aligns=['l', 'c', 'l'],
    caption='Table 10 — Détail du budget de développement (total : 50 M FCFA).')

story += h2_block('13.3 Gouvernance de pilotage', para(
    "Le projet est piloté par un comité de pilotage mensuel — fondatrice, CTO, et à "
    "partir de J1 le responsable financier — qui examine l'avancement des phases, "
    "la consommation budgétaire et le registre des risques. Les quatre jalons "
    "GO/NO-GO font l'objet de comités dédiés avec décision formelle consignée. Le "
    "suivi financier est rapproché trimestriellement des hypothèses du business "
    "plan, tout écart supérieur à 15 % déclenchant une revue de trajectoire. Enfin, "
    "le reporting opérationnel repose sur le tableau de bord produit (indicateurs "
    "d'usage et commerciaux) et le tableau de bord technique (disponibilité, "
    "incidents, dette technique), tous deux accessibles au comité en continu."))

story += h2_block('13.4 Registre des risques et mesures d\u2019atténuation', para(
    "Six risques majeurs sont identifiés, évalués en probabilité et en impact, et "
    "accompagnés chacun d'une mesure d'atténuation active. Ce registre est revu à "
    "chaque comité de pilotage :"))
story += make_table(
    ['Risque', 'Probabilité', 'Impact', 'Mesure d\u2019atténuation'],
    [
        ['Retard de l\u2019agrément ASAC', 'Élevée', 'Critique',
         'Démarrage anticipé à S7, dossier complet dès le premier dépôt, conseil '
         'spécialisé, suivi hebdomadaire'],
        ['Conventions d\u2019apport non signées à temps', 'Moyenne', 'Critique',
         'Panel de 4 compagnies approchées (cible 2), argumentaire coût '
         'd\u2019acquisition, démonstrations précoces'],
        ['Instabilité des paiements Mobile Money', 'Moyenne', 'Élevé',
         'POC dès la phase 2, double intégration MTN et Orange, procédure de '
         'rejeu et support dédié'],
        ['Financement incomplet', 'Moyenne', 'Critique',
         'Séquençage par jalons, engagement conditionnel des fonds, recherche '
         'complémentaire (subventions tech africaines)'],
        ['Incident de sécurité ou fuite de données', 'Faible', 'Critique',
         'Test d\u2019intrusion externe, chiffrement systématique, conformité '
         'CNDP, plan de réponse testé'],
        ['Adoption plus lente que prévu', 'Moyenne', 'Élevé',
         'Pilote avant tout engagement lourd, contenu pédagogique, ajustement du '
         'mix d\u2019acquisition au coût par lead'],
    ],
    [0.30, 0.13, 0.11, 0.46],
    aligns=['l', 'c', 'c', 'l'],
    caption='Table 11 — Registre des risques du plan d\u2019exécution.')
story.append(para(
    "La force de ce plan tient moins dans chaque disposition prise isolément que "
    "dans leur cohérence d'ensemble : un périmètre MVP tenu, un chemin réglementaire "
    "démarré avant d'être bloquant, des jalons qui protègent le financement, et une "
    "équipe qui croît au rythme des preuves apportées. C'est cette discipline qui "
    "donne à Unirances sa probabilité de tenir la trajectoire 2027-2029 fixée par "
    "le business plan, et la capacité de devenir, au-delà du Cameroun, la plateforme "
    "de référence de la distribution d'assurance digitale dans l'espace CIMA."))

# ================================================================== build
doc = TocDocTemplate(OUT_BODY, pagesize=A4,
                     leftMargin=MARGIN, rightMargin=MARGIN,
                     topMargin=MARGIN, bottomMargin=MARGIN,
                     title=DOC_TITLE, author='Z.ai', creator='Z.ai',
                     subject="Plan de conception et développement du projet "
                             "Unirances — 9 phases, jalons GO/NO-GO, budget et risques")
doc.multiBuild(story, onFirstPage=_page_decor, onLaterPages=_page_decor)
print('OK —', OUT_BODY)
