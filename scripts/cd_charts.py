# -*- coding: utf-8 -*-
"""Graphiques du plan de conception & développement Unirances — palette Template 07."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Palette Template 07 (famille bleue unique)
ACCENT   = '#2d7ab3'   # XS
DEEP     = '#1a4a7a'   # M
LIGHT1   = '#7aa8cc'
LIGHT2   = '#b8d0e4'
BORDER   = '#c0d0e2'
TEXTP    = '#142840'
MUTED    = '#5a7a96'
BG       = '#ffffff'

OUT = '/home/z/my-project/scripts/assets'
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------
# Graphique 1 — Gantt des 9 phases (nov. 2026 -> déc. 2028, 26 mois)
# ------------------------------------------------------------------
# m0 = novembre 2026 ... m26 = décembre 2028
phases = [
    ('P0 · Cadrage & financement',        0.0,  2.0,  LIGHT1),
    ('P1 · Conception produit & UX',      1.0,  3.0,  LIGHT1),
    ('P2 · Conception technique',         1.0,  3.0,  LIGHT1),
    ('P3 · Conformité & partenariats',    2.0,  6.0,  ACCENT),
    ('P4 · Développement du MVP',         3.0,  5.0,  ACCENT),
    ('P5 · Qualité, sécurité & tests',    7.0,  2.0,  ACCENT),
    ('P6 · Pilote terrain',               8.0,  2.5,  DEEP),
    ('P7 · Lancement commercial',        10.0,  3.0,  DEEP),
    ('P8 · Industrialisation & V2',      12.0, 14.0,  DEEP),
]
milestones = [
    ('J0 GO', 2.0, 0), ('J1 GO', 4.0, 2), ('J2 GO', 8.5, 5), ('J3 Lancement', 12.0, 7),
]

fig, ax = plt.subplots(figsize=(7.8, 3.9), dpi=200, constrained_layout=True)
fig.patch.set_facecolor(BG)
for i, (name, start, dur, col) in enumerate(phases):
    ax.barh(i, dur, left=start, height=0.52, color=col, edgecolor='none', zorder=3)
for label, x, row in milestones:
    ax.scatter([x], [row], marker='D', s=46, color=TEXTP, zorder=5)
    ax.annotate(label, (x, row), textcoords='offset points', xytext=(0, 9),
                ha='center', fontsize=8, fontweight='bold', color=TEXTP, zorder=6)
ax.set_yticks(range(len(phases)))
ax.set_yticklabels([p[0] for p in phases], fontsize=9.5, color=TEXTP)
ax.invert_yaxis()
ax.set_xlim(0, 26.5)
ticks = [0, 3, 6, 9, 12, 15, 18, 21, 24, 26]
labels = ['T4 2026', 'T1 2027', 'T2 2027', 'T3 2027', 'T4 2027',
          'T1 2028', 'T2 2028', 'T3 2028', 'T4 2028', '']
ax.set_xticks(ticks)
ax.set_xticklabels(labels, fontsize=9, color=MUTED)
ax.grid(axis='x', linestyle='--', linewidth=0.5, alpha=0.2, color=DEEP)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(BORDER)
ax.spines['bottom'].set_color(BORDER)
ax.tick_params(colors=MUTED, labelsize=9)
import matplotlib.patches as mpatches
leg = [mpatches.Patch(color=LIGHT1, label='Conception'),
       mpatches.Patch(color=ACCENT, label='Construction'),
       mpatches.Patch(color=DEEP, label='Lancement & scale'),
       plt.Line2D([0], [0], marker='D', color='none', markerfacecolor=TEXTP,
                  markersize=7, label='Jalon GO / NO-GO')]
ax.legend(handles=leg, loc='upper left', bbox_to_anchor=(0, 1.13), ncol=4,
          frameon=False, fontsize=8.5, handlelength=1.2)
fig.savefig(f'{OUT}/cd_gantt.png', facecolor=BG)
plt.close(fig)

# ------------------------------------------------------------------
# Graphique 2 — Répartition du budget de développement 50 M FCFA (donut)
# ------------------------------------------------------------------
postes = ['Équipe produit & tech',
          'Conformité & juridique',
          'Pilote & lancement',
          'Infrastructure & outils',
          'Réserve imprévus',
          'Partenariats & intégrations']
montants = [18, 8, 8, 6, 6, 4]
cols = [DEEP, ACCENT, LIGHT1, LIGHT2, BORDER, '#9dbcd6']

fig, ax = plt.subplots(figsize=(7.6, 3.3), dpi=200, constrained_layout=True)
fig.patch.set_facecolor(BG)
wedges, _ = ax.pie(montants, colors=cols, startangle=90, counterclock=False,
                   wedgeprops=dict(width=0.34, edgecolor=BG))
ax.text(0, 0.07, '50', ha='center', va='center', fontsize=22,
        fontweight='bold', color=TEXTP)
ax.text(0, -0.26, 'M FCFA', ha='center', va='center', fontsize=9.5, color=MUTED)
total = sum(montants)
legend_labels = [f'{p}  —  {m} M ({m/total*100:.0f} %)' for p, m in zip(postes, montants)]
ax.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(1.02, 0.5),
          frameon=False, fontsize=9.5, labelspacing=1.15, handlelength=1.0)
ax.set_aspect('equal')
fig.savefig(f'{OUT}/cd_budget.png', facecolor=BG)
plt.close(fig)

# ------------------------------------------------------------------
# Graphique 3 — Effectifs de l'équipe coeur sur 26 mois
# ------------------------------------------------------------------
months = [0, 1, 2, 3, 7, 8, 11, 12, 13, 16, 20, 24, 26]
heads  = [2, 3, 4, 6, 6, 8, 8, 9, 10, 10, 11, 12, 12]

fig, ax = plt.subplots(figsize=(7.6, 3.1), dpi=200, constrained_layout=True)
fig.patch.set_facecolor(BG)
ax.step(months, heads, where='post', color=ACCENT, linewidth=2.5, zorder=4)
ax.fill_between(months, heads, step='post', color=ACCENT, alpha=0.14, zorder=2)
pts_x = [0, 8, 13, 26]
pts_y = [2, 8, 10, 12]
ax.scatter(pts_x, pts_y, s=26, color=DEEP, zorder=5)
for px, py in zip(pts_x, pts_y):
    ax.annotate(f'{py}', (px, py), textcoords='offset points', xytext=(0, 8),
                ha='center', fontsize=9.5, fontweight='bold', color=TEXTP)
ax.set_xlim(0, 26.5)
ax.set_ylim(0, 14.5)
ax.set_xticks(ticks)
ax.set_xticklabels(labels, fontsize=9, color=MUTED)
ax.set_ylabel('Personnes (équipe coeur)', fontsize=10, color=MUTED)
ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.2, color=DEEP)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color(BORDER)
ax.tick_params(colors=MUTED, labelsize=9)
ax.annotate('Cadrage', (1, 2), xytext=(0, -16), textcoords='offset points',
            ha='center', fontsize=8.5, color=MUTED)
ax.annotate('Pilote & lancement', (10.5, 8), xytext=(0, -16),
            textcoords='offset points', ha='center', fontsize=8.5, color=MUTED)
ax.annotate('Scale CEMAC', (24, 12), xytext=(-4, -16), textcoords='offset points',
            ha='center', fontsize=8.5, color=MUTED)
fig.savefig(f'{OUT}/cd_effectifs.png', facecolor=BG)
plt.close(fig)

print('OK — 3 graphiques du plan de développement générés dans', OUT)
