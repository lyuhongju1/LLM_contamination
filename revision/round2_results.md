# Round-2 reanalysis (exploratory)

## 1. Per-template saturation: number of the five templates in which an item is >=90% (or <=10%)

| model | cond | items >=90 in all 5 | in >=4 | in >=1 | items <=10 in all 5 | in >=4 | in >=1 |
|---|---|---|---|---|---|---|---|
| S4.5 | A | 2 | 7 | 9 | 5 | 7 | 16 |
| S4.5 | B | 2 | 4 | 7 | 9 | 9 | 18 |
| S4.5 | D | 5 | 5 | 7 | 3 | 7 | 13 |
| S4.6 | A | 5 | 8 | 12 | 4 | 6 | 11 |
| S4.6 | B | 4 | 6 | 10 | 11 | 12 | 12 |
| S4.6 | D | 8 | 9 | 14 | 1 | 2 | 5 |

Items >=90 under the original template but not under all five (model, cond: item [templates >=90 of 5]):

- S4.5 A: protodune.xarapuca [4], gerda.inverted_coaxial [1], exo200.sipm_adoption [4], lhcb.velopix [1], lhcb.scifi [4], aligo.fd_squeezing [4], aligo.filter_cavity [4]
- S4.5 D: aligo.filter_cavity [3]
- S4.6 A: darkside.successor_named [4], lhcb.scifi [4], aligo.filter_cavity [4]
- S4.6 D: gerda.successor_named [3]

## 2. Binomial null for the five-template range

Null: the five templates share the cell's pooled rate; each template is Binomial(n_t, p_pooled). 20,000 draws per cell. p = P(null range >= observed).

| model | cond | cells | median obs. range | median null range | cells p<0.05 | expected by chance | cells range>30 | of which p<0.05 |
|---|---|---|---|---|---|---|---|---|
| S4.5 | A | 26 | 18 | 11 | 15 | 1.3 | 9 | 9 |
| S4.5 | B | 26 | 23 | 10 | 12 | 1.3 | 10 | 10 |
| S4.5 | D | 26 | 18 | 10 | 16 | 1.3 | 6 | 6 |
| S4.6 | A | 26 | 24 | 10 | 16 | 1.3 | 11 | 11 |
| S4.6 | B | 26 | 6 | 4 | 11 | 1.3 | 8 | 8 |
| S4.6 | D | 26 | 24 | 10 | 13 | 1.3 | 10 | 10 |

Benjamini-Hochberg at FDR 5% over all 156 cells: 73 cells show template dependence beyond binomial noise.

Mid-range cells only (pooled rate 10-90%):

- S4.5 A: 15 mid-range cells, 11 with p<0.05, median obs range 54
- S4.5 B: 15 mid-range cells, 12 with p<0.05, median obs range 54
- S4.5 D: 12 mid-range cells, 10 with p<0.05, median obs range 34
- S4.6 A: 13 mid-range cells, 13 with p<0.05, median obs range 50
- S4.6 B: 9 mid-range cells, 9 with p<0.05, median obs range 38
- S4.6 D: 14 mid-range cells, 11 with p<0.05, median obs range 36

## 3. Content-level leakage sensitivity (exclude GERDA argon instrumentation and LHCb VeloPix)

| model | cond | 26 items: >=90 / <=10 / median | 24 items: >=90 / <=10 / median |
|---|---|---|---|
| H4.5 | A | 2 / 16 / 5 | 2 / 15 / 5 |
| H4.5 | D | 2 / 19 / 4 | 2 / 17 / 4 |
| S4.5 | A | 9 / 8 / 37 | 8 / 8 / 37 |
| S4.5 | D | 6 / 12 / 19 | 6 / 11 / 21 |
| O4.5 | A | 7 / 9 / 28 | 7 / 9 / 28 |
| O4.5 | D | 8 / 8 / 28 | 8 / 6 / 31 |
| S4.6 | A | 8 / 7 / 42 | 8 / 7 / 42 |
| S4.6 | D | 9 / 3 / 61 | 9 / 2 / 65 |
| S5 | A | 6 / 13 / 23 | 5 / 12 / 23 |
| S5 | D | 8 / 5 / 71 | 8 / 5 / 71 |
| H5.5 | A | 4 / 12 / 14 | 4 / 12 / 11 |
| H5.5 | D | 5 / 12 / 19 | 5 / 11 / 20 |
| S5.5 | A | 8 / 8 / 59 | 8 / 7 / 59 |
| S5.5 | D | 11 / 4 / 80 | 11 / 3 / 86 |
| O5.5 | A | 13 / 5 / 89 | 12 / 5 / 89 |
| O5.5 | D | 13 / 4 / 90 | 13 / 3 / 96 |
| F5.1 | A | 7 / 7 / 55 | 6 / 6 / 55 |
| F5.1 | D | 9 / 5 / 64 | 9 / 4 / 66 |

- A-D Newcombe, 26 items: 11 positive, 10 negative, 31 null
- A-D Newcombe, 24 items: 9 positive, 10 negative, 29 null
- Content-leak items, rates A/B/C/D: lhcb.velopix S4.5: 96/86/92/0; lhcb.velopix S4.6: 66/14/70/26; gerda.argon_instrumentation S4.5: 22/26/14/20; gerda.argon_instrumentation S4.6: 16/52/44/6

## 4. Post-baseline items, by pair (rates %, A / D)

| pair | item | H4.5 | S4.5 | O4.5 | S4.6 | S5 | H5.5 | S5.5 | O5.5 | F5.1 |
|---|---|---|---|---|---|---|---|---|---|---|
| darkside | veto_upgrade_gd | 32/44 | 22/78 | 44/96 | 88/98 | 36/92 | 42/88 | 84/100 | 100/100 | 16/54 |
| lux | xenon_skin | 0/2 | 2/8 | 30/18 | 8/12 | 4/2 | 0/2 | 64/12 | 70/66 | 60/36 |
| gerda | successor_named | 0/4 | 16/10 | 2/28 | 12/90 | 6/60 | 0/18 | 2/96 | 12/74 | 2/62 |
| gerda | inverted_coaxial | 6/10 | 92/78 | 80/100 | 78/100 | 2/100 | 16/46 | 42/100 | 98/100 | 76/100 |
| exo200 | sipm_adoption | 96/98 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 |
| sno | successor_named | 0/8 | 22/6 | 0/14 | 46/62 | 54/38 | 0/8 | 2/30 | 4/86 | 20/36 |
| sno | scintillator_fill | 0/0 | 58/10 | 22/8 | 30/48 | 0/0 | 0/2 | 0/12 | 0/0 | 4/8 |
| sno | tellurium | 0/0 | 2/0 | 0/2 | 2/10 | 0/0 | 0/0 | 0/2 | 0/0 | 4/2 |

| model | cond | items >=90 (of 8) | pairs with any item >=90 (of 5) | items <=10 | pairs with all items <=10 |
|---|---|---|---|---|---|
| H4.5 | A | 1 | 1 | 6 | 3 |
| H4.5 | D | 1 | 1 | 6 | 3 |
| S4.5 | A | 2 | 2 | 2 | 1 |
| S4.5 | D | 1 | 1 | 5 | 2 |
| O4.5 | A | 1 | 1 | 3 | 0 |
| O4.5 | D | 3 | 3 | 2 | 0 |
| S4.6 | A | 1 | 1 | 2 | 1 |
| S4.6 | D | 4 | 3 | 1 | 0 |
| S5 | A | 1 | 1 | 5 | 2 |
| S5 | D | 3 | 3 | 3 | 1 |
| H5.5 | A | 1 | 1 | 5 | 2 |
| H5.5 | D | 1 | 1 | 4 | 2 |
| S5.5 | A | 1 | 1 | 4 | 1 |
| S5.5 | D | 4 | 3 | 1 | 0 |
| O5.5 | A | 3 | 3 | 3 | 1 |
| O5.5 | D | 3 | 3 | 2 | 0 |
| F5.1 | A | 1 | 1 | 3 | 0 |
| F5.1 | D | 2 | 2 | 2 | 0 |

## 5. Nine models: items >=90 and <=10 (of 26), median, conditions A / D / D'

| model | A >=90 | A <=10 | A med | D >=90 | D <=10 | D med | D' >=90 | D' med |
|---|---|---|---|---|---|---|---|---|
| H4.5 | 2 | 16 | 5 | 2 | 19 | 4 | 3 | 5 |
| S4.5 | 9 | 8 | 37 | 6 | 12 | 19 | 5 | 32 |
| O4.5 | 7 | 9 | 28 | 8 | 8 | 28 | 6 | 48 |
| S4.6 | 8 | 7 | 42 | 9 | 3 | 61 | 12 | 78 |
| S5 | 6 | 13 | 23 | 8 | 5 | 71 | 8 | 50 |
| H5.5 | 4 | 12 | 14 | 5 | 12 | 19 | 4 | 28 |
| S5.5 | 8 | 8 | 59 | 11 | 4 | 80 | 10 | 75 |
| O5.5 | 13 | 5 | 89 | 13 | 4 | 90 | 11 | 85 |
| F5.1 | 7 | 7 | 55 | 9 | 5 | 64 | 8 | 60 |

## 6. Absence items on all nine models (A/B/C/D/D')

- sno.tellurium: H4.5 0/0/0/0/0; S4.5 2/0/0/0/0; O4.5 0/0/0/2/5; S4.6 2/0/0/10/20; S5 0/0/0/0/0; H5.5 0/0/0/0/0; S5.5 0/0/0/2/0; O5.5 0/0/0/0/0; F5.1 4/0/0/2/0
- exo200.tonne_scale: H4.5 0/0/0/0/0; S4.5 2/0/4/0/30; O4.5 0/0/0/4/20; S4.6 0/0/0/14/55; S5 0/0/2/18/15; H5.5 0/0/0/2/30; S5.5 6/0/2/74/65; O5.5 28/14/32/46/80; F5.1 6/4/20/16/55

## 7. Sample counts

- raw_v2.jsonl: 4000 distinct samples
- raw_dprime.jsonl: 400 distinct samples
- raw_local.jsonl: 2800 distinct samples
- raw_v1_superseded.jsonl: 1600 distinct samples