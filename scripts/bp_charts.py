# -*- coding: utf-8 -*-
"""Graphiques du business plan MboaAssur — palette Template 07 Crystal Blue."""
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
DEEP     = '#1a4a7a'   # M (table header)
LIGHT1   = '#7aa8cc'
LIGHT2   = '#b8d0e4'
BORDER   = '#c0d0e2'
TEXTP    = '#142840'
MUTED    = '#5a7a96'
BG       = '#ffffff'

OUT = '/home/z/my-project/scripts/assets'
os.makedirs(OUT, exist_ok=True)

def style_ax(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(BORDER)
    ax.tick_params(colors=MUTED, labelsize=10)
    ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.2, color=DEEP)
    ax.set_axisbelow(True)

# ------------------------------------------------------------------
# Graphique 1 — Évolution du marché camerounais 2022-2025 (ASAC)
# ------------------------------------------------------------------
years = ['2023', '2024', '2025 (p.)']
non_vie = [185.78, 191.6, 197.3]
vie     = [88.8, 97.1, 102.67]
totals  = [n + v for n, v in zip(non_vie, vie)]

fig, ax = plt.subplots(figsize=(7.6, 3.6), dpi=200, constrained_layout=True)
fig.patch.set_facecolor(BG)
x = np.arange(len(years))
b1 = ax.bar(x, non_vie, 0.46, label='Non-vie', color=DEEP, edgecolor='none')
b2 = ax.bar(x, vie, 0.46, bottom=non_vie, label='Vie', color=LIGHT1, edgecolor='none')
for i, t in enumerate(totals):
    ax.text(x[i], t + 6, f'{t:,.1f}'.replace(',', ' '), ha='center', va='bottom',
            fontsize=10.5, fontweight='bold', color=TEXTP)
for i, n in enumerate(non_vie):
    ax.text(x[i], n / 2, f'{n:,.1f}'.replace(',', ' '), ha='center', va='center',
            fontsize=8.5, color='white')
ax.set_xticks(x); ax.set_xticklabels(years)
ax.set_ylabel('Milliards de FCFA', fontsize=10, color=MUTED)
ax.set_ylim(0, 360)
ax.legend(loc='upper left', bbox_to_anchor=(0, 1.14), ncol=2, frameon=False,
          fontsize=10, handlelength=1.2, handleheight=1.0)
style_ax(ax)
fig.savefig(f'{OUT}/chart1_marche.png', facecolor=BG)
plt.close(fig)

# ------------------------------------------------------------------
# Graphique 2 — Taux de pénétration comparés (barres horizontales)
# ------------------------------------------------------------------
labels = ['Cameroun (ASAC, 2023)', 'Zone CIMA', 'Afrique (moyenne)', 'Pays OCDE']
vals   = [0.8, 1.0, 2.0, 6.2]
cols   = [ACCENT, LIGHT1, LIGHT2, BORDER]

fig, ax = plt.subplots(figsize=(7.6, 2.9), dpi=200, constrained_layout=True)
fig.patch.set_facecolor(BG)
y = np.arange(len(labels))
bars = ax.barh(y, vals, 0.56, color=cols, edgecolor='none')
for i, v in enumerate(vals):
    ax.text(v + 0.09, y[i], f'{v:.1f} %'.replace('.', ','), va='center', ha='left',
            fontsize=10.5, fontweight='bold', color=TEXTP)
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=10, color=TEXTP)
ax.invert_yaxis()
ax.set_xlim(0, 7.4)
ax.set_xlabel("Primes d'assurance en % du PIB", fontsize=10, color=MUTED)
ax.grid(axis='x', linestyle='--', linewidth=0.5, alpha=0.2, color=DEEP)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(BORDER)
ax.spines['bottom'].set_color(BORDER)
ax.tick_params(colors=MUTED, labelsize=10)
ax.set_axisbelow(True)
fig.savefig(f'{OUT}/chart2_penetration.png', facecolor=BG)
plt.close(fig)

# ------------------------------------------------------------------
# Graphique 3 — Répartition du chiffre d'affaires An 3 (donut)
# ------------------------------------------------------------------
flux_labels = ['Commissions d\u2019apport\n(nouvelles polices)',
               'Commissions de gestion\n(renouvellements)',
               'Services B2B\n(back-office cautions)']
flux_vals = [163.1, 33.3, 14.0]
flux_cols = [DEEP, ACCENT, LIGHT2]

fig, ax = plt.subplots(figsize=(7.6, 3.2), dpi=200, constrained_layout=True)
fig.patch.set_facecolor(BG)
wedges, _ = ax.pie(flux_vals, colors=flux_cols, startangle=90,
                   counterclock=False, wedgeprops=dict(width=0.34, edgecolor=BG))
ax.text(0, 0.06, '210,4', ha='center', va='center', fontsize=20,
        fontweight='bold', color=TEXTP)
ax.text(0, -0.24, 'M FCFA (An 3)', ha='center', va='center', fontsize=9.5, color=MUTED)
total = sum(flux_vals)
legend_labels = [f'{l}  \u2014  {v:,.1f} M ({v/total*100:.1f} %)'.replace(',', ' ')
                 for l, v in zip(flux_labels, flux_vals)]
ax.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(1.02, 0.5),
          frameon=False, fontsize=9.5, labelspacing=1.2, handlelength=1.0)
ax.set_aspect('equal')
fig.savefig(f'{OUT}/chart3_flux.png', facecolor=BG)
plt.close(fig)

# ------------------------------------------------------------------
# Graphique 4 — Trajectoire financière 2027-2029
# ------------------------------------------------------------------
periods = ['Année 1 (2027)', 'Année 2 (2028)', 'Année 3 (2029)']
ca      = [20.0, 86.5, 210.4]
charges = [41.0, 83.4, 138.8]
res     = [-21.0, 3.1, 71.6]

fig, ax = plt.subplots(figsize=(7.6, 3.6), dpi=200, constrained_layout=True)
fig.patch.set_facecolor(BG)
x = np.arange(3)
w = 0.34
ax.bar(x - w/2, ca, w, label='Chiffre d\u2019affaires', color=DEEP, edgecolor='none')
ax.bar(x + w/2, charges, w, label='Charges totales', color=LIGHT2, edgecolor='none')
ax.plot(x, res, color=ACCENT, linewidth=2.5, marker='o', markersize=5,
        label='Résultat net', zorder=5)
for i in range(3):
    ax.text(x[i] - w/2, ca[i] + 6, f'{ca[i]:,.1f}'.replace(',', ' '),
            ha='center', fontsize=9, fontweight='bold', color=TEXTP)
    ax.text(x[i] + w/2, charges[i] + 6, f'{charges[i]:,.1f}'.replace(',', ' '),
            ha='center', fontsize=9, color=MUTED)
    off = 10 if res[i] >= 0 else -16
    ax.text(x[i], res[i] + off, f'{res[i]:+,.1f}'.replace(',', ' '),
            ha='center', fontsize=9.5, fontweight='bold', color=ACCENT)
ax.axhline(0, color=BORDER, linewidth=0.8)
ax.set_xticks(x); ax.set_xticklabels(periods, fontsize=10)
ax.set_ylabel('Millions de FCFA', fontsize=10, color=MUTED)
ax.set_ylim(-45, 265)
ax.legend(loc='upper left', bbox_to_anchor=(0, 1.16), ncol=3, frameon=False,
          fontsize=9.5, handlelength=1.2)
style_ax(ax)
fig.savefig(f'{OUT}/chart4_pnl.png', facecolor=BG)
plt.close(fig)

print('OK — 4 graphiques générés dans', OUT)
