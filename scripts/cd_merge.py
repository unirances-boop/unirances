# -*- coding: utf-8 -*-
"""Fusion couverture + corps -> PDF final normalisé A4 (Unirances — Plan de Conception et Développement)."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

def normalize(page):
    w, h = float(page.mediabox.width), float(page.mediabox.height)
    if abs(w - A4_W) > 0.1 or abs(h - A4_H) > 0.1:
        page.scale_to(A4_W, A4_H)
    return page

writer = PdfWriter()
writer.add_page(normalize(PdfReader('/home/z/my-project/scripts/assets/cd_cover.pdf').pages[0]))
for p in PdfReader('/home/z/my-project/scripts/assets/cd_body.pdf').pages:
    writer.add_page(normalize(p))
writer.add_metadata({
    '/Title': 'Unirances — Plan de Conception et Développement',
    '/Author': 'Z.ai',
    '/Creator': 'Z.ai',
    '/Subject': "Plan d'exécution du projet Unirances : 9 phases de conception et "
                'développement, jalons GO/NO-GO, budget 50 M FCFA, risques — aligné '
                'sur le business plan 2027-2029',
})
out = '/home/z/my-project/download/Unirances_Plan_Conception_Developpement.pdf'
with open(out, 'wb') as f:
    writer.write(f)
print('OK —', out)
