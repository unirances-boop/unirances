# -*- coding: utf-8 -*-
"""Fusion couverture + corps -> PDF final normalisé A4."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

def normalize(page):
    w, h = float(page.mediabox.width), float(page.mediabox.height)
    if abs(w - A4_W) > 0.1 or abs(h - A4_H) > 0.1:
        page.scale_to(A4_W, A4_H)
    return page

writer = PdfWriter()
writer.add_page(normalize(PdfReader('/home/z/my-project/scripts/assets/bp_cover.pdf').pages[0]))
for p in PdfReader('/home/z/my-project/scripts/assets/bp_body.pdf').pages:
    writer.add_page(normalize(p))
writer.add_metadata({
    '/Title': 'MboaAssur — Business Plan 2027-2029',
    '/Author': 'Z.ai',
    '/Creator': 'Z.ai',
    '/Subject': 'Business plan du courtier digital MboaAssur — marché chiffré '
                '(ASAC, FANAF, CIMA), modèle de revenus, coûts, projections 3 ans',
})
out = '/home/z/my-project/download/MboaAssur_Business_Plan_2027-2029.pdf'
with open(out, 'wb') as f:
    writer.write(f)
print('OK —', out)
