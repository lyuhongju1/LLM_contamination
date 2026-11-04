Records: paraphrase final 6960; cells P1/P2 sizes [50]; T sizes [20]

## R1 Saturation (items >= 90% in D on the original template must stay >= 75% in D under P1 and P2)

| item | model | O | P1 | P2 | pass |
|---|---|---|---|---|---|
| darkside.sipm_adoption | S4.5 | 100 | 100 | 100 | yes |
| darkside.sipm_adoption | S4.6 | 100 | 100 | 100 | yes |
| darkside.veto_upgrade_gd | S4.6 | 98 | 100 | 100 | yes |
| protodune.xarapuca | S4.5 | 100 | 96 | 100 | yes |
| protodune.xarapuca | S4.6 | 100 | 100 | 100 | yes |
| icecube.mdom | S4.5 | 100 | 100 | 100 | yes |
| icecube.mdom | S4.6 | 100 | 100 | 100 | yes |
| gerda.successor_named | S4.6 | 90 | 100 | 68 | NO |
| gerda.inverted_coaxial | S4.6 | 100 | 100 | 100 | yes |
| exo200.sipm_adoption | S4.5 | 100 | 100 | 100 | yes |
| exo200.sipm_adoption | S4.6 | 100 | 100 | 100 | yes |
| aligo.fd_squeezing | S4.5 | 100 | 100 | 100 | yes |
| aligo.fd_squeezing | S4.6 | 100 | 100 | 100 | yes |
| aligo.filter_cavity | S4.5 | 94 | 34 | 100 | NO |
| aligo.filter_cavity | S4.6 | 100 | 92 | 100 | yes |

R1: 13 of 15 pass

## R2 VeloPix on Sonnet 4.5: A - D >= 50 points under each family

- O: A 96, D 0, A-D +96
- P1: A 2, D 0, A-D +2 [-5, +10] -> FAIL
- P2: A 88, D 0, A-D +88 [+74, +94] -> pass

## R3 Cutoff suppression on Sonnet 4.6 (A -> B, Newcombe interval excludes zero under each family)

| item | O A->B | P1 A->B [CI] | P2 A->B [CI] | pass |
|---|---|---|---|---|
| darkside.successor_named | 90 -> 22 | 96 -> 80 [+3, +29] | 90 -> 40 [+32, +64] | yes |
| gerda.inverted_coaxial | 78 -> 4 | 52 -> 2 [+34, +63] | 94 -> 0 [+82, +98] | yes |
| lhcb.velopix | 66 -> 14 | 22 -> 22 [-16, +16] | 68 -> 34 [+14, +50] | NO |
| sno.successor_named | 46 -> 0 | 28 -> 0 [+15, +42] | 46 -> 0 [+31, +60] | yes |

## R4 Anchoring: originally significant negative A - D cells keep a negative point estimate

| item | model | O A-D | P1 A-D | P2 A-D | pass |
|---|---|---|---|---|---|
| darkside.veto_upgrade_gd | S4.5 | -56 | -46 | -46 | yes |
| xenon1t.neutron_veto | S4.5 | -16 | -32 | -70 | yes |
| lux.successor_named | S4.6 | -42 | -34 | -12 | yes |
| lux.outer_detector | S4.6 | -36 | -72 | -24 | yes |
| icecube.degg | S4.5 | -20 | -38 | -48 | yes |
| icecube.degg | S4.6 | -50 | -82 | -48 | yes |
| gerda.successor_named | S4.6 | -78 | -96 | -56 | yes |
| gerda.inverted_coaxial | S4.6 | -22 | -48 | -6 | yes |
| exo200.tonne_scale | S4.6 | -14 | -42 | -30 | yes |
| lhcb.software_trigger | S4.6 | -50 | -54 | +2 | NO |

R4: 9 of 10 pass

## All items, all templates (rate %; O = original template)

| item | model | A O/P1/P2 | B O/P1/P2 | D O/P1/P2 | max shift |
|---|---|---|---|---|---|
| darkside.successor_named | S4.5 | 56/10/62 | 58/14/40 | 8/14/10 | 52 |
| darkside.successor_named | S4.6 | 90/96/90 | 22/80/40 | 68/98/80 | 58 |
| darkside.sipm_adoption | S4.5 | 100/100/100 | 98/94/94 | 100/100/100 | 4 |
| darkside.sipm_adoption | S4.6 | 100/100/100 | 100/100/100 | 100/100/100 | 0 |
| darkside.veto_upgrade_gd | S4.5 | 22/0/38 | 32/0/20 | 78/46/84 | 38 |
| darkside.veto_upgrade_gd | S4.6 | 88/44/84 | 74/26/70 | 98/100/100 | 48 |
| protodune.xarapuca | S4.5 | 96/10/90 | 94/14/86 | 100/96/100 | 86 |
| protodune.xarapuca | S4.6 | 100/100/100 | 98/94/98 | 100/100/100 | 4 |
| protodune.coverage_increase | S4.5 | 0/4/0 | 0/0/2 | 0/8/0 | 8 |
| protodune.coverage_increase | S4.6 | 0/2/0 | 0/0/0 | 2/2/0 | 2 |
| xenon1t.radon_column | S4.5 | 36/54/36 | 52/70/46 | 30/64/86 | 56 |
| xenon1t.radon_column | S4.6 | 70/66/60 | 58/70/72 | 24/76/48 | 52 |
| xenon1t.neutron_veto | S4.5 | 2/0/0 | 4/0/0 | 18/32/70 | 52 |
| xenon1t.neutron_veto | S4.6 | 38/8/40 | 14/18/18 | 54/70/80 | 32 |
| lux.successor_named | S4.5 | 38/10/34 | 14/12/8 | 6/30/22 | 28 |
| lux.successor_named | S4.6 | 18/64/44 | 2/26/0 | 60/98/56 | 46 |
| lux.xenon_skin | S4.5 | 2/0/14 | 12/0/2 | 8/2/2 | 14 |
| lux.xenon_skin | S4.6 | 8/0/8 | 0/0/0 | 12/14/8 | 8 |
| lux.outer_detector | S4.5 | 0/2/2 | 2/0/0 | 4/6/2 | 4 |
| lux.outer_detector | S4.6 | 4/2/6 | 6/2/0 | 40/74/30 | 44 |
| icecube.mdom | S4.5 | 100/100/100 | 100/100/100 | 100/100/100 | 0 |
| icecube.mdom | S4.6 | 92/98/100 | 90/100/84 | 100/100/100 | 16 |
| icecube.degg | S4.5 | 4/0/8 | 0/0/10 | 24/38/56 | 32 |
| icecube.degg | S4.6 | 8/10/16 | 0/0/0 | 58/92/64 | 34 |
| gerda.successor_named | S4.5 | 16/0/2 | 6/0/0 | 10/26/24 | 16 |
| gerda.successor_named | S4.6 | 12/4/12 | 0/0/0 | 90/100/68 | 32 |
| gerda.inverted_coaxial | S4.5 | 92/0/24 | 56/0/2 | 78/86/90 | 92 |
| gerda.inverted_coaxial | S4.6 | 78/52/94 | 4/2/0 | 100/100/100 | 42 |
| gerda.argon_instrumentation | S4.5 | 22/18/18 | 26/22/4 | 20/14/30 | 22 |
| gerda.argon_instrumentation | S4.6 | 16/72/42 | 52/94/12 | 6/2/12 | 82 |
| exo200.sipm_adoption | S4.5 | 100/86/90 | 98/56/22 | 100/100/100 | 76 |
| exo200.sipm_adoption | S4.6 | 100/100/100 | 100/98/50 | 100/100/100 | 50 |
| exo200.tonne_scale | S4.5 | 2/0/4 | 0/0/0 | 0/18/16 | 18 |
| exo200.tonne_scale | S4.6 | 0/0/4 | 0/2/0 | 14/42/34 | 28 |
| lhcb.velopix | S4.5 | 96/2/88 | 86/0/72 | 0/0/0 | 94 |
| lhcb.velopix | S4.6 | 66/22/68 | 14/22/34 | 26/46/56 | 46 |
| lhcb.scifi | S4.5 | 98/44/96 | 98/24/78 | 72/58/42 | 74 |
| lhcb.scifi | S4.6 | 100/72/100 | 82/76/86 | 88/100/94 | 28 |
| lhcb.software_trigger | S4.5 | 66/58/74 | 58/54/76 | 24/42/26 | 22 |
| lhcb.software_trigger | S4.6 | 26/12/54 | 34/20/32 | 76/66/52 | 42 |
| sno.successor_named | S4.5 | 22/18/16 | 2/8/0 | 6/10/2 | 8 |
| sno.successor_named | S4.6 | 46/28/46 | 0/0/0 | 62/96/94 | 34 |
| sno.scintillator_fill | S4.5 | 58/0/40 | 32/0/10 | 10/2/0 | 58 |
| sno.scintillator_fill | S4.6 | 30/4/18 | 0/0/0 | 48/74/70 | 26 |
| sno.tellurium | S4.5 | 2/0/0 | 0/0/0 | 0/2/2 | 2 |
| sno.tellurium | S4.6 | 2/2/6 | 0/0/0 | 10/20/36 | 26 |
| aligo.fd_squeezing | S4.5 | 100/86/100 | 100/38/98 | 100/100/100 | 62 |
| aligo.fd_squeezing | S4.6 | 100/100/100 | 100/96/92 | 100/100/100 | 8 |
| aligo.filter_cavity | S4.5 | 96/16/98 | 100/0/90 | 94/34/100 | 100 |
| aligo.filter_cavity | S4.6 | 100/88/98 | 100/96/96 | 100/92/100 | 12 |
| aligo.successor_named | S4.5 | 2/2/10 | 0/0/2 | 4/0/8 | 8 |
| aligo.successor_named | S4.6 | 6/4/14 | 2/0/0 | 12/24/0 | 24 |

Max across-template shift per item-model (over A, B, D): median 32, 75th pct 52, max 100 points; 27 of 52 exceed 30 points

## Extended-thinking arm (original templates, N=20) vs original no-thinking (N=50)

Rates %. 'think-only' = share of samples where the item appears in the thinking text but not in the final answer.

| item | model | A no-think / think | B no-think / think | D no-think / think | think-only A/B/D |
|---|---|---|---|---|---|
| darkside.successor_named | S4.5 | 56 / 55 | 58 / 35 | 8 / 15 | 5/0/5 |
| darkside.successor_named | S4.6 | 90 / 50 | 22 / 20 | 68 / 80 | 0/0/5 |
| darkside.sipm_adoption | S4.5 | 100 / 100 | 98 / 100 | 100 / 100 | 0/0/0 |
| darkside.sipm_adoption | S4.6 | 100 / 100 | 100 / 100 | 100 / 100 | 0/0/0 |
| darkside.veto_upgrade_gd | S4.5 | 22 / 15 | 32 / 5 | 78 / 85 | 0/0/0 |
| darkside.veto_upgrade_gd | S4.6 | 88 / 70 | 74 / 65 | 98 / 100 | 5/0/0 |
| protodune.xarapuca | S4.5 | 96 / 95 | 94 / 100 | 100 / 100 | 0/0/0 |
| protodune.xarapuca | S4.6 | 100 / 100 | 98 / 100 | 100 / 100 | 0/0/0 |
| protodune.coverage_increase | S4.5 | 0 / 0 | 0 / 0 | 0 / 0 | 0/0/0 |
| protodune.coverage_increase | S4.6 | 0 / 0 | 0 / 5 | 2 / 0 | 0/0/0 |
| icecube.mdom | S4.5 | 100 / 100 | 100 / 100 | 100 / 100 | 0/0/0 |
| icecube.mdom | S4.6 | 92 / 95 | 90 / 100 | 100 / 100 | 5/0/0 |
| icecube.degg | S4.5 | 4 / 15 | 0 / 0 | 24 / 35 | 5/5/5 |
| icecube.degg | S4.6 | 8 / 15 | 0 / 0 | 58 / 35 | 0/0/15 |
| gerda.successor_named | S4.5 | 16 / 10 | 6 / 0 | 10 / 20 | 0/0/15 |
| gerda.successor_named | S4.6 | 12 / 5 | 0 / 0 | 90 / 55 | 0/0/40 |
| gerda.inverted_coaxial | S4.5 | 92 / 45 | 56 / 35 | 78 / 100 | 0/0/0 |
| gerda.inverted_coaxial | S4.6 | 78 / 80 | 4 / 0 | 100 / 100 | 0/0/0 |
| gerda.argon_instrumentation | S4.5 | 22 / 5 | 26 / 15 | 20 / 15 | 0/5/0 |
| gerda.argon_instrumentation | S4.6 | 16 / 25 | 52 / 30 | 6 / 5 | 5/25/0 |
| exo200.sipm_adoption | S4.5 | 100 / 100 | 98 / 100 | 100 / 100 | 0/0/0 |
| exo200.sipm_adoption | S4.6 | 100 / 100 | 100 / 100 | 100 / 100 | 0/0/0 |
| exo200.tonne_scale | S4.5 | 2 / 0 | 0 / 0 | 0 / 5 | 0/0/0 |
| exo200.tonne_scale | S4.6 | 0 / 0 | 0 / 0 | 14 / 0 | 0/0/0 |
| lhcb.velopix | S4.5 | 96 / 100 | 86 / 100 | 0 / 0 | 0/0/0 |
| lhcb.velopix | S4.6 | 66 / 60 | 14 / 35 | 26 / 20 | 0/0/5 |
| lhcb.scifi | S4.5 | 98 / 95 | 98 / 100 | 72 / 70 | 0/0/10 |
| lhcb.scifi | S4.6 | 100 / 100 | 82 / 100 | 88 / 75 | 0/0/15 |
| lhcb.software_trigger | S4.5 | 66 / 55 | 58 / 60 | 24 / 30 | 5/0/5 |
| lhcb.software_trigger | S4.6 | 26 / 15 | 34 / 10 | 76 / 45 | 0/5/5 |
| sno.successor_named | S4.5 | 22 / 5 | 2 / 0 | 6 / 30 | 0/0/5 |
| sno.successor_named | S4.6 | 46 / 35 | 0 / 0 | 62 / 75 | 10/0/10 |
| sno.scintillator_fill | S4.5 | 58 / 70 | 32 / 20 | 10 / 35 | 0/0/0 |
| sno.scintillator_fill | S4.6 | 30 / 25 | 0 / 0 | 48 / 50 | 0/0/0 |
| sno.tellurium | S4.5 | 2 / 0 | 0 / 0 | 0 / 0 | 0/0/0 |
| sno.tellurium | S4.6 | 2 / 0 | 0 / 0 | 10 / 0 | 0/0/20 |
| aligo.fd_squeezing | S4.5 | 100 / 100 | 100 / 100 | 100 / 100 | 0/0/0 |
| aligo.fd_squeezing | S4.6 | 100 / 100 | 100 / 95 | 100 / 100 | 0/0/0 |
| aligo.filter_cavity | S4.5 | 96 / 100 | 100 / 100 | 94 / 100 | 0/0/0 |
| aligo.filter_cavity | S4.6 | 100 / 100 | 100 / 100 | 100 / 100 | 0/0/0 |
| aligo.successor_named | S4.5 | 2 / 15 | 0 / 10 | 4 / 10 | 0/0/0 |
| aligo.successor_named | S4.6 | 6 / 0 | 2 / 0 | 12 / 0 | 5/0/0 |

- S4.5 A: mean change with thinking -3.3 points over 21 items; items moving >= 20 points: 1
- S4.5 B: mean change with thinking -3.0 points over 21 items; items moving >= 20 points: 3
- S4.5 D: mean change with thinking +5.8 points over 21 items; items moving >= 20 points: 3
- S4.6 A: mean change with thinking -4.0 points over 21 items; items moving >= 20 points: 1
- S4.6 B: mean change with thinking -0.6 points over 21 items; items moving >= 20 points: 3
- S4.6 D: mean change with thinking -5.6 points over 21 items; items moving >= 20 points: 3