# Unirances — Plateforme d'assurance digitale pour le Cameroun & la zone CEMAC

> **Note** : projet anciennement nommé *MboaAssur*, rebaptisé **Unirances**.

**Unirances** est un projet d'insurtech visant à digitaliser le parcours d'assurance de bout en bout — **devis → souscription → gestion des sinistres** — sur un marché camerounais et CEMAC à très fort potentiel mais encore faiblement pénétré (pénétration assurance de **0,7 à 0,9 %** du PIB selon l'ASAC).

Ce dépôt rassemble l'ensemble des documents de conception et le business plan chiffré du projet.

## 📁 Contenu du dépôt

| Dossier | Contenu |
|---|---|
| [`download/`](./download) | **Business Plan 2027–2029** (PDF, 17 pages) — marché chiffré, modèle de revenus, coûts, projections |
| [`upload/`](./upload) | **Études fonctionnelles & technologiques** — 5 dossiers PDF (~515 pages) couvrant la vision produit, les parcours (devis, souscription, contrats, sinistres) et l'architecture |
| [`scripts/`](./scripts) | Scripts Python de génération du business plan (graphiques matplotlib, corps ReportLab, couverture, fusion) |
| [`research/`](./research) | Sources de recherche datées et vérifiées (ASAC, FANAF, CIMA, CNEF, presse économique) |

## 📊 Chiffres clés du business plan (2027–2029)

- **Marché adressé** : primes d'assurance Cameroun ≈ 288,7 Mds FCFA (2024, ASAC) ; zone FANAF ≈ 2 041 Mds FCFA (2023)
- **Modèle de revenus** : commissions d'apport (10–30 % des primes selon branche, pratiques marché)
- **Chiffre d'affaires projeté** : 20,0 M → 86,5 M → 210,4 M FCFA (an 1 → an 3)
- **Résultat net** : −21,0 M → +3,1 M → +71,6 M FCFA
- **Break-even** : mois 15–18
- **Besoin de financement initial** : 50 M FCFA

## 📜 Cadre réglementaire de référence

- **Code CIMA** (art. 506, 508, 530) — garantie financière de 10 M FCFA, agrément
- **ASAC** — Agence de Supervision des Assurances de la CEMAC (régulateur régional)
- **FANAF** — Fédération Africaine des Sociétés d'Assurances (statistiques marché)

## 🛠️ Reproduire le business plan

```bash
pip install matplotlib reportlab pypdf
python scripts/bp_charts.py   # génère les 4 graphiques
python scripts/bp_body.py     # génère le corps du document (ReportLab)
python scripts/bp_merge.py    # fusionne couverture + corps
```
