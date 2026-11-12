# Round-3 reanalysis (exploratory)

Frozen regex scores are unchanged by everything below.

## 1. Nine models, original template

Counts of items at >=90%. Units: 24 independent units (SiPM items averaged; squeezing and filter cavity scored as one). Post: of the 8 post-baseline items (number of pairs in parentheses). Length: median output tokens minus reasoning tokens, conditions A-D.

| model | A >=90 (26) | A median | D >=90 (26) | D units >=90 (24) | D post >=90 (8) | D median | length |
|---|---|---|---|---|---|---|---|
| H4.5 | 2 | 5 | 2 | 2 | 1 (1) | 4 | 2306 |
| S4.5 | 9 | 37 | 6 | 4 | 1 (1) | 19 | 2246 |
| O4.5 | 7 | 28 | 8 | 6 | 3 (3) | 28 | 1808 |
| S4.6 | 8 | 42 | 9 | 7 | 4 (3) | 61 | 3202 |
| S5 | 6 | 23 | 8 | 6 | 3 (3) | 71 | 2413 |
| H5.5 | 4 | 14 | 5 | 3 | 1 (1) | 19 | 1716 |
| S5.5 | 8 | 59 | 11 | 9 | 4 (3) | 80 | 3552 |
| O5.5 | 13 | 89 | 13 | 11 | 3 (3) | 90 | 3793 |
| F5.1 | 7 | 55 | 9 | 7 | 2 (2) | 64 | 3482 |

## 2. VeloPix, condition A, by template

- S4.5: K15 12, K5 0, O 96, P1 2, P2 88, P3 86, P4 88
- S4.6: K15 46, K5 40, O 66, P1 22, P2 68, P3 88, P4 68

K5 and K15 share the P1 opening; on Sonnet 4.5 VeloPix is at the floor under that opening, so breadth sensitivity cannot be tested there.

## 3. Items <=10% in every cell (frozen keys)

Sonnet 4 models: conditions A, C, D, D' (original) and A, D under P1-P4 (12 cells; condition B excluded because its instruction suppresses items by design). Other models: A and D, original template only.

- H4.5: 16: protodune.xarapuca, protodune.coverage_increase, xenon1t.neutron_veto, lux.successor_named, lux.xenon_skin, lux.outer_detector, icecube.degg, gerda.successor_named, gerda.inverted_coaxial, exo200.tonne_scale, lhcb.velopix, lhcb.software_trigger, sno.successor_named, sno.scintillator_fill, sno.tellurium, aligo.successor_named
- S4.5: 3: protodune.coverage_increase, lux.outer_detector, sno.tellurium
- O4.5: 5: protodune.coverage_increase, lux.outer_detector, exo200.tonne_scale, sno.tellurium, aligo.successor_named
- S4.6: 1: protodune.coverage_increase
- S5: 5: protodune.coverage_increase, lux.xenon_skin, sno.scintillator_fill, sno.tellurium, aligo.successor_named
- H5.5: 9: protodune.xarapuca, protodune.coverage_increase, lux.xenon_skin, lux.outer_detector, exo200.tonne_scale, sno.successor_named, sno.scintillator_fill, sno.tellurium, aligo.successor_named
- S5.5: 4: protodune.coverage_increase, gerda.argon_instrumentation, sno.tellurium, aligo.successor_named
- O5.5: 3: protodune.coverage_increase, sno.scintillator_fill, sno.tellurium
- F5.1: 5: protodune.coverage_increase, gerda.argon_instrumentation, sno.scintillator_fill, sno.tellurium, aligo.successor_named

## 4. False-negative check on the Sonnet 4 low cells

Rates per cell under the frozen key -> frozen key or broader concept expression.

- sno.tellurium S4.5: O/A 2->4 O/C 0->0 O/D 0->0 O/Dp 0->0 P1/A 0->0 P1/D 2->2 P2/A 0->2 P2/D 2->2 P3/A 0->4 P3/D 2->4 P4/A 2->2 P4/D 8->8
- sno.tellurium S4.6: O/A 2->2 O/C 0->0 O/D 10->10 O/Dp 20->25 P1/A 2->2 P1/D 20->24 P2/A 6->6 P2/D 36->42 P3/A 10->12 P3/D 46->58 P4/A 20->24 P4/D 62->70
- lux.outer_detector S4.5: O/A 0->0 O/C 0->0 O/D 4->4 O/Dp 5->35 P1/A 2->2 P1/D 6->12 P2/A 2->2 P2/D 2->2 P3/A 0->0 P3/D 6->8 P4/A 0->0 P4/D 4->4
- lux.outer_detector S4.6: O/A 4->8 O/C 2->8 O/D 40->56 O/Dp 25->40 P1/A 2->6 P1/D 74->78 P2/A 6->8 P2/D 30->36 P3/A 4->10 P3/D 34->42 P4/A 4->6 P4/D 38->50

ProtoDUNE coverage increase is the known regex failure (adjudicated 19 of 20). Broad-pattern candidates among scored misses are listed in round3_fn_snippets.md for reading.

## 5. Threshold sensitivity of the low-item count (Sonnet 4 models, 12 cells)

ProtoDUNE coverage increase excluded (known regex failure).

| model | expression | max<=10 | max<=15 | max<=25 | pooled<=5 | pooled<=10 | pooled<=15 |
|---|---|---|---|---|---|---|---|
| S4.5 | frozen | 2 | 2 | 3 | 2 | 5 | 5 |
| S4.5 | concept | 1 | 1 | 2 | 2 | 5 | 5 |
| S4.6 | frozen | 0 | 0 | 1 | 0 | 1 | 2 |
| S4.6 | concept | 0 | 0 | 1 | 0 | 1 | 2 |

Items with pooled rate <=15 (max over cells, pooled rate):

- S4.5 frozen: lux.xenon_skin max 24 pooled 8.2; lux.outer_detector max 6 pooled 2.5; exo200.tonne_scale max 30 pooled 6.8; sno.tellurium max 8 pooled 1.6; aligo.successor_named max 42 pooled 8.9
- S4.5 concept: lux.xenon_skin max 24 pooled 8.2; lux.outer_detector max 35 pooled 4.2; exo200.tonne_scale max 30 pooled 6.8; sno.tellurium max 8 pooled 2.5; aligo.successor_named max 42 pooled 8.9
- S4.6 frozen: lux.xenon_skin max 16 pooled 6.5; aligo.successor_named max 26 pooled 10.7
- S4.6 concept: lux.xenon_skin max 16 pooled 6.5; aligo.successor_named max 26 pooled 10.7

Probability that an item with true rate p in every cell clears the bar in all 12 cells (11 cells N=50, D' N=20):

- p=0.03: bar 10%: 0.94, bar 15%: 1.00
- p=0.05: bar 10%: 0.61, bar 15%: 0.95
