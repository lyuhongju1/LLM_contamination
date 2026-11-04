## R2. Conditions D and D' restricted to samples that do not identify the experiment

Identity rates first: share of D / D' samples naming the successor (frozen successor key, applied even where the key was leakage-excluded for A-C) or the baseline experiment itself (the redaction patterns). LHCb has no frozen successor key; an ad hoc 'Upgrade I / Run 3' expression is used here and flagged.

| pair | model | D succ. | D succ. or baseline | D' succ. | D' succ. or baseline |
|---|---|---|---|---|---|
| darkside | S4.5 | 8 [3, 19] | 18 [10, 31] | 10 [3, 30] | 30 [15, 52] |
| darkside | S4.6 | 68 [54, 79] | 98 [90, 100] | 85 [64, 95] | 100 [84, 100] |
| protodune | S4.5 | 4 [1, 13] | 74 [60, 84] | 0 [0, 16] | 70 [48, 85] |
| protodune | S4.6 | 24 [14, 37] | 100 [93, 100] | 5 [1, 24] | 85 [64, 95] |
| xenon1t | S4.5 | 8 [3, 19] | 12 [6, 24] | 20 [8, 42] | 25 [11, 47] |
| xenon1t | S4.6 | 40 [28, 54] | 62 [48, 74] | 85 [64, 95] | 90 [70, 97] |
| lux | S4.5 | 6 [2, 16] | 6 [2, 16] | 35 [18, 57] | 45 [26, 66] |
| lux | S4.6 | 60 [46, 72] | 74 [60, 84] | 90 [70, 97] | 100 [84, 100] |
| icecube | S4.5 | 68 [54, 79] | 88 [76, 94] | 70 [48, 85] | 80 [58, 92] |
| icecube | S4.6 | 88 [76, 94] | 100 [93, 100] | 100 [84, 100] | 100 [84, 100] |
| gerda | S4.5 | 10 [4, 21] | 40 [28, 54] | 25 [11, 47] | 70 [48, 85] |
| gerda | S4.6 | 90 [79, 96] | 98 [90, 100] | 95 [76, 99] | 100 [84, 100] |
| exo200 | S4.5 | 12 [6, 24] | 14 [7, 26] | 35 [18, 57] | 35 [18, 57] |
| exo200 | S4.6 | 100 [93, 100] | 100 [93, 100] | 95 [76, 99] | 95 [76, 99] |
| lhcb | S4.5 | 20 [11, 33] | 54 [40, 67] | 15 [5, 36] | 60 [39, 78] |
| lhcb | S4.6 | 62 [48, 74] | 98 [90, 100] | 70 [48, 85] | 100 [84, 100] |
| sno | S4.5 | 6 [2, 16] | 26 [16, 40] | 30 [15, 52] | 60 [39, 78] |
| sno | S4.6 | 62 [48, 74] | 100 [93, 100] | 90 [70, 97] | 100 [84, 100] |
| aligo | S4.5 | 4 [1, 13] | 54 [40, 67] | 0 [0, 16] | 45 [26, 66] |
| aligo | S4.6 | 12 [6, 24] | 98 [90, 100] | 0 [0, 16] | 100 [84, 100] |

Technology and design items, all samples vs. samples that name neither the successor nor the baseline (n = retained samples).

| item | model | D all | D anonymous (n) | D' all | D' anonymous (n) |
|---|---|---|---|---|---|
| darkside.sipm_adoption | S4.5 | 100 [93, 100] | 100 [91, 100] (41) | 100 [84, 100] | 100 [78, 100] (14) |
| darkside.sipm_adoption | S4.6 | 100 [93, 100] | 100 [21, 100] (1) | 100 [84, 100] | -- (0) |
| darkside.veto_upgrade_gd | S4.5 | 78 [65, 87] | 80 [66, 90] (41) | 85 [64, 95] | 93 [69, 99] (14) |
| darkside.veto_upgrade_gd | S4.6 | 98 [90, 100] | 100 [21, 100] (1) | 100 [84, 100] | -- (0) |
| protodune.xarapuca | S4.5 | 100 [93, 100] | 100 [77, 100] (13) | 55 [34, 74] | 50 [19, 81] (6) |
| protodune.xarapuca | S4.6 | 100 [93, 100] | -- (0) | 100 [84, 100] | 100 [44, 100] (3) |
| protodune.coverage_increase | S4.5 | 0 [0, 7] | 0 [0, 23] (13) | 0 [0, 16] | 0 [0, 39] (6) |
| protodune.coverage_increase | S4.6 | 2 [0, 10] | -- (0) | 0 [0, 16] | 0 [0, 56] (3) |
| xenon1t.radon_column | S4.5 | 30 [19, 44] | 30 [18, 44] (44) | 60 [39, 78] | 73 [48, 89] (15) |
| xenon1t.radon_column | S4.6 | 24 [14, 37] | 16 [6, 38] (19) | 35 [18, 57] | 50 [9, 91] (2) |
| xenon1t.neutron_veto | S4.5 | 18 [10, 31] | 18 [10, 32] (44) | 50 [30, 70] | 67 [42, 85] (15) |
| xenon1t.neutron_veto | S4.6 | 54 [40, 67] | 58 [36, 77] (19) | 65 [43, 82] | 50 [9, 91] (2) |
| lux.xenon_skin | S4.5 | 8 [3, 19] | 9 [3, 20] (47) | 0 [0, 16] | 0 [0, 26] (11) |
| lux.xenon_skin | S4.6 | 12 [6, 24] | 8 [1, 33] (13) | 5 [1, 24] | -- (0) |
| lux.outer_detector | S4.5 | 4 [1, 13] | 4 [1, 14] (47) | 5 [1, 24] | 9 [2, 38] (11) |
| lux.outer_detector | S4.6 | 40 [28, 54] | 38 [18, 64] (13) | 25 [11, 47] | -- (0) |
| icecube.mdom | S4.5 | 100 [93, 100] | 100 [61, 100] (6) | 100 [84, 100] | 100 [51, 100] (4) |
| icecube.mdom | S4.6 | 100 [93, 100] | -- (0) | 100 [84, 100] | -- (0) |
| icecube.degg | S4.5 | 24 [14, 37] | 33 [10, 70] (6) | 30 [15, 52] | 50 [15, 85] (4) |
| icecube.degg | S4.6 | 58 [44, 71] | -- (0) | 70 [48, 85] | -- (0) |
| gerda.inverted_coaxial | S4.5 | 78 [65, 87] | 73 [56, 86] (30) | 100 [84, 100] | 100 [61, 100] (6) |
| gerda.inverted_coaxial | S4.6 | 100 [93, 100] | 100 [21, 100] (1) | 100 [84, 100] | -- (0) |
| gerda.argon_instrumentation | S4.5 | 20 [11, 33] | 20 [10, 37] (30) | 30 [15, 52] | 0 [0, 39] (6) |
| gerda.argon_instrumentation | S4.6 | 6 [2, 16] | 0 [0, 79] (1) | 25 [11, 47] | -- (0) |
| exo200.sipm_adoption | S4.5 | 100 [93, 100] | 100 [92, 100] (43) | 100 [84, 100] | 100 [77, 100] (13) |
| exo200.sipm_adoption | S4.6 | 100 [93, 100] | -- (0) | 100 [84, 100] | 100 [21, 100] (1) |
| exo200.tonne_scale | S4.5 | 0 [0, 7] | 0 [0, 8] (43) | 30 [15, 52] | 31 [13, 58] (13) |
| exo200.tonne_scale | S4.6 | 14 [7, 26] | -- (0) | 55 [34, 74] | 0 [0, 79] (1) |
| lhcb.velopix | S4.5 | 0 [0, 7] | 0 [0, 14] (23) | 0 [0, 16] | 0 [0, 32] (8) |
| lhcb.velopix | S4.6 | 26 [16, 40] | 0 [0, 79] (1) | 10 [3, 30] | -- (0) |
| lhcb.scifi | S4.5 | 72 [58, 83] | 57 [37, 74] (23) | 85 [64, 95] | 62 [31, 86] (8) |
| lhcb.scifi | S4.6 | 88 [76, 94] | 0 [0, 79] (1) | 95 [76, 99] | -- (0) |
| lhcb.software_trigger | S4.5 | 24 [14, 37] | 17 [7, 37] (23) | 40 [22, 61] | 38 [14, 69] (8) |
| lhcb.software_trigger | S4.6 | 76 [63, 86] | 100 [21, 100] (1) | 45 [26, 66] | -- (0) |
| sno.scintillator_fill | S4.5 | 10 [4, 21] | 14 [6, 28] (37) | 25 [11, 47] | 25 [7, 59] (8) |
| sno.scintillator_fill | S4.6 | 48 [35, 61] | -- (0) | 55 [34, 74] | -- (0) |
| sno.tellurium | S4.5 | 0 [0, 7] | 0 [0, 9] (37) | 0 [0, 16] | 0 [0, 32] (8) |
| sno.tellurium | S4.6 | 10 [4, 21] | -- (0) | 20 [8, 42] | -- (0) |
| aligo.fd_squeezing | S4.5 | 100 [93, 100] | 100 [86, 100] (23) | 100 [84, 100] | 100 [74, 100] (11) |
| aligo.fd_squeezing | S4.6 | 100 [93, 100] | 100 [21, 100] (1) | 100 [84, 100] | -- (0) |
| aligo.filter_cavity | S4.5 | 94 [84, 98] | 91 [73, 98] (23) | 60 [39, 78] | 45 [21, 72] (11) |
| aligo.filter_cavity | S4.6 | 100 [93, 100] | 100 [21, 100] (1) | 90 [70, 97] | -- (0) |

Items whose anonymous-subset rate drops by 15 points or more (n_retained >= 10): [('lhcb.scifi', 'S4.5', 'D', 72, 57, 23)]

Cells with fewer than 10 anonymous samples (estimate unreliable): [('darkside.sipm_adoption', 'S4.6', 'D', 1), ('darkside.sipm_adoption', 'S4.6', 'Dp', 0), ('darkside.veto_upgrade_gd', 'S4.6', 'D', 1), ('darkside.veto_upgrade_gd', 'S4.6', 'Dp', 0), ('protodune.xarapuca', 'S4.5', 'Dp', 6), ('protodune.xarapuca', 'S4.6', 'D', 0), ('protodune.xarapuca', 'S4.6', 'Dp', 3), ('protodune.coverage_increase', 'S4.5', 'Dp', 6), ('protodune.coverage_increase', 'S4.6', 'D', 0), ('protodune.coverage_increase', 'S4.6', 'Dp', 3), ('xenon1t.radon_column', 'S4.6', 'Dp', 2), ('xenon1t.neutron_veto', 'S4.6', 'Dp', 2), ('lux.xenon_skin', 'S4.6', 'Dp', 0), ('lux.outer_detector', 'S4.6', 'Dp', 0), ('icecube.mdom', 'S4.5', 'D', 6), ('icecube.mdom', 'S4.5', 'Dp', 4), ('icecube.mdom', 'S4.6', 'D', 0), ('icecube.mdom', 'S4.6', 'Dp', 0), ('icecube.degg', 'S4.5', 'D', 6), ('icecube.degg', 'S4.5', 'Dp', 4), ('icecube.degg', 'S4.6', 'D', 0), ('icecube.degg', 'S4.6', 'Dp', 0), ('gerda.inverted_coaxial', 'S4.5', 'Dp', 6), ('gerda.inverted_coaxial', 'S4.6', 'D', 1), ('gerda.inverted_coaxial', 'S4.6', 'Dp', 0), ('gerda.argon_instrumentation', 'S4.5', 'Dp', 6), ('gerda.argon_instrumentation', 'S4.6', 'D', 1), ('gerda.argon_instrumentation', 'S4.6', 'Dp', 0), ('exo200.sipm_adoption', 'S4.6', 'D', 0), ('exo200.sipm_adoption', 'S4.6', 'Dp', 1), ('exo200.tonne_scale', 'S4.6', 'D', 0), ('exo200.tonne_scale', 'S4.6', 'Dp', 1), ('lhcb.velopix', 'S4.5', 'Dp', 8), ('lhcb.velopix', 'S4.6', 'D', 1), ('lhcb.velopix', 'S4.6', 'Dp', 0), ('lhcb.scifi', 'S4.5', 'Dp', 8), ('lhcb.scifi', 'S4.6', 'D', 1), ('lhcb.scifi', 'S4.6', 'Dp', 0), ('lhcb.software_trigger', 'S4.5', 'Dp', 8), ('lhcb.software_trigger', 'S4.6', 'D', 1), ('lhcb.software_trigger', 'S4.6', 'Dp', 0), ('sno.scintillator_fill', 'S4.5', 'Dp', 8), ('sno.scintillator_fill', 'S4.6', 'D', 0), ('sno.scintillator_fill', 'S4.6', 'Dp', 0), ('sno.tellurium', 'S4.5', 'Dp', 8), ('sno.tellurium', 'S4.6', 'D', 0), ('sno.tellurium', 'S4.6', 'Dp', 0), ('aligo.fd_squeezing', 'S4.6', 'D', 1), ('aligo.fd_squeezing', 'S4.6', 'Dp', 0), ('aligo.filter_cavity', 'S4.6', 'D', 1), ('aligo.filter_cavity', 'S4.6', 'Dp', 0)]

## R3. All A-D gaps with Newcombe 95% intervals (Claude, N=50 per cell)

| item | model | A | D | A-D [95% CI] | sign |
|---|---|---|---|---|---|
| darkside.successor_named | S4.5 | 56 | 8 | +48 [+31, +62] | + |
| darkside.successor_named | S4.6 | 90 | 68 | +22 [+6, +37] | + |
| darkside.sipm_adoption | S4.5 | 100 | 100 | +0 [-7, +7] | 0 |
| darkside.sipm_adoption | S4.6 | 100 | 100 | +0 [-7, +7] | 0 |
| darkside.veto_upgrade_gd | S4.5 | 22 | 78 | -56 [-69, -37] | - |
| darkside.veto_upgrade_gd | S4.6 | 88 | 98 | -10 [-22, +1] | 0 |
| protodune.xarapuca | S4.5 | 96 | 100 | -4 [-13, +4] | 0 |
| protodune.xarapuca | S4.6 | 100 | 100 | +0 [-7, +7] | 0 |
| protodune.coverage_increase | S4.5 | 0 | 0 | +0 [-7, +7] | 0 |
| protodune.coverage_increase | S4.6 | 0 | 2 | -2 [-10, +5] | 0 |
| xenon1t.radon_column | S4.5 | 36 | 30 | +6 [-12, +24] | 0 |
| xenon1t.radon_column | S4.6 | 70 | 24 | +46 [+27, +61] | + |
| xenon1t.neutron_veto | S4.5 | 2 | 18 | -16 [-29, -4] | - |
| xenon1t.neutron_veto | S4.6 | 38 | 54 | -16 [-34, +3] | 0 |
| lux.successor_named | S4.5 | 38 | 6 | +32 [+16, +46] | + |
| lux.successor_named | S4.6 | 18 | 60 | -42 [-57, -23] | - |
| lux.xenon_skin | S4.5 | 2 | 8 | -6 [-17, +4] | 0 |
| lux.xenon_skin | S4.6 | 8 | 12 | -4 [-17, +9] | 0 |
| lux.outer_detector | S4.5 | 0 | 4 | -4 [-13, +4] | 0 |
| lux.outer_detector | S4.6 | 4 | 40 | -36 [-50, -20] | - |
| icecube.mdom | S4.5 | 100 | 100 | +0 [-7, +7] | 0 |
| icecube.mdom | S4.6 | 92 | 100 | -8 [-19, +1] | 0 |
| icecube.degg | S4.5 | 4 | 24 | -20 [-34, -6] | - |
| icecube.degg | S4.6 | 8 | 58 | -50 [-64, -32] | - |
| gerda.successor_named | S4.5 | 16 | 10 | +6 [-8, +20] | 0 |
| gerda.successor_named | S4.6 | 12 | 90 | -78 [-87, -62] | - |
| gerda.inverted_coaxial | S4.5 | 92 | 78 | +14 [-0, +28] | 0 |
| gerda.inverted_coaxial | S4.6 | 78 | 100 | -22 [-35, -10] | - |
| gerda.argon_instrumentation | S4.5 | 22 | 20 | +2 [-14, +18] | 0 |
| gerda.argon_instrumentation | S4.6 | 16 | 6 | +10 [-3, +23] | 0 |
| exo200.sipm_adoption | S4.5 | 100 | 100 | +0 [-7, +7] | 0 |
| exo200.sipm_adoption | S4.6 | 100 | 100 | +0 [-7, +7] | 0 |
| exo200.tonne_scale | S4.5 | 2 | 0 | +2 [-5, +10] | 0 |
| exo200.tonne_scale | S4.6 | 0 | 14 | -14 [-26, -4] | - |
| lhcb.velopix | S4.5 | 96 | 0 | +96 [+84, +99] | + |
| lhcb.velopix | S4.6 | 66 | 26 | +40 [+21, +55] | + |
| lhcb.scifi | S4.5 | 98 | 72 | +26 [+12, +40] | + |
| lhcb.scifi | S4.6 | 100 | 88 | +12 [+2, +24] | + |
| lhcb.software_trigger | S4.5 | 66 | 24 | +42 [+23, +57] | + |
| lhcb.software_trigger | S4.6 | 26 | 76 | -50 [-64, -31] | - |
| sno.successor_named | S4.5 | 22 | 6 | +16 [+2, +30] | + |
| sno.successor_named | S4.6 | 46 | 62 | -16 [-34, +3] | 0 |
| sno.scintillator_fill | S4.5 | 58 | 10 | +48 [+30, +62] | + |
| sno.scintillator_fill | S4.6 | 30 | 48 | -18 [-35, +1] | 0 |
| sno.tellurium | S4.5 | 2 | 0 | +2 [-5, +10] | 0 |
| sno.tellurium | S4.6 | 2 | 10 | -8 [-19, +2] | 0 |
| aligo.fd_squeezing | S4.5 | 100 | 100 | +0 [-7, +7] | 0 |
| aligo.fd_squeezing | S4.6 | 100 | 100 | +0 [-7, +7] | 0 |
| aligo.filter_cavity | S4.5 | 96 | 94 | +2 [-8, +13] | 0 |
| aligo.filter_cavity | S4.6 | 100 | 100 | +0 [-7, +7] | 0 |
| aligo.successor_named | S4.5 | 2 | 4 | -2 [-12, +7] | 0 |
| aligo.successor_named | S4.6 | 6 | 12 | -6 [-18, +6] | 0 |

Significantly positive (A>D): 11 of 52 item-model cells: [('darkside.successor_named', 'S4.5', 48), ('darkside.successor_named', 'S4.6', 22), ('xenon1t.radon_column', 'S4.6', 46), ('lux.successor_named', 'S4.5', 32), ('lhcb.velopix', 'S4.5', 96), ('lhcb.velopix', 'S4.6', 40), ('lhcb.scifi', 'S4.5', 26), ('lhcb.scifi', 'S4.6', 12), ('lhcb.software_trigger', 'S4.5', 42), ('sno.successor_named', 'S4.5', 16), ('sno.scintillator_fill', 'S4.5', 48)]

Significantly negative (D>A): 10 of 52: [('darkside.veto_upgrade_gd', 'S4.5', -56), ('xenon1t.neutron_veto', 'S4.5', -16), ('lux.successor_named', 'S4.6', -42), ('lux.outer_detector', 'S4.6', -36), ('icecube.degg', 'S4.5', -20), ('icecube.degg', 'S4.6', -50), ('gerda.successor_named', 'S4.6', -78), ('gerda.inverted_coaxial', 'S4.6', -22), ('exo200.tonne_scale', 'S4.6', -14), ('lhcb.software_trigger', 'S4.6', -50)]

Interval includes zero: 31 of 52

## R4. Full distribution over the 26 audited items

### 26 items

| model | cond | 0-10 | 10-25 | 25-50 | 50-75 | 75-90 | 90-100 | median |
|---|---|---|---|---|---|---|---|---|
| S4.5 | A | 8 | 4 | 2 | 3 | 0 | 9 | 37 |
| S4.5 | B | 9 | 2 | 3 | 4 | 1 | 7 | 32 |
| S4.5 | C | 7 | 3 | 6 | 2 | 0 | 8 | 44 |
| S4.5 | D | 10 | 6 | 1 | 1 | 2 | 6 | 19 |
| S4.5 | Dp | 6 | 1 | 8 | 4 | 2 | 5 | 32 |
| S4.6 | A | 7 | 3 | 4 | 2 | 2 | 8 | 42 |
| S4.6 | B | 12 | 3 | 1 | 3 | 1 | 6 | 14 |
| S4.6 | C | 7 | 3 | 4 | 4 | 2 | 6 | 44 |
| S4.6 | D | 2 | 5 | 3 | 5 | 2 | 9 | 61 |
| S4.6 | Dp | 3 | 2 | 4 | 4 | 1 | 12 | 77 |

### 24 independent units

| model | cond | 0-10 | 10-25 | 25-50 | 50-75 | 75-90 | 90-100 | median |
|---|---|---|---|---|---|---|---|---|
| S4.5 | A | 8 | 4 | 2 | 3 | 0 | 7 | 29 |
| S4.5 | B | 9 | 2 | 3 | 4 | 1 | 5 | 29 |
| S4.5 | C | 7 | 3 | 6 | 2 | 0 | 6 | 34 |
| S4.5 | D | 10 | 6 | 1 | 1 | 2 | 4 | 14 |
| S4.5 | Dp | 6 | 1 | 8 | 3 | 2 | 4 | 30 |
| S4.6 | A | 7 | 3 | 4 | 2 | 2 | 6 | 34 |
| S4.6 | B | 12 | 3 | 1 | 3 | 1 | 4 | 10 |
| S4.6 | C | 7 | 3 | 4 | 4 | 2 | 4 | 43 |
| S4.6 | D | 2 | 5 | 3 | 5 | 2 | 7 | 59 |
| S4.6 | Dp | 3 | 2 | 4 | 4 | 1 | 10 | 68 |

Reviewer's counts check (S4.5, condition A, 26 items): >=90%: 9, <=22%: 12, >=90% in D: 6

### Per-item rates, all conditions (rate %, N=50; D' N=20)

| item | class | S4.5 A/B/C/D/D' | S4.6 A/B/C/D/D' |
|---|---|---|---|
| darkside.successor_named | identity_recall | 56 / 58 / 42 / 8 / 10 | 90 / 22 / 66 / 68 / 85 |
| darkside.sipm_adoption | technology_recall | 100 / 98 / 100 / 100 / 100 | 100 / 100 / 100 / 100 / 100 |
| darkside.veto_upgrade_gd | technology_recall | 22 / 32 / 48 / 78 / 85 | 88 / 74 / 58 / 98 / 100 |
| protodune.xarapuca | technology_recall | 96 / 94 / 100 / 100 / 55 | 100 / 98 / 100 / 100 / 100 |
| protodune.coverage_increase | design_recall | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 2 / 0 |
| xenon1t.radon_column | technology_recall | 36 / 52 / 48 / 30 / 60 | 70 / 58 / 66 / 24 / 35 |
| xenon1t.neutron_veto | technology_recall | 2 / 4 / 2 / 18 / 50 | 38 / 14 / 42 / 54 / 65 |
| lux.successor_named | identity_recall | 38 / 14 / 26 / 6 / 35 | 18 / 2 / 18 / 60 / 90 |
| lux.xenon_skin | technology_recall | 2 / 12 / 8 / 8 / 0 | 8 / 0 / 0 / 12 / 5 |
| lux.outer_detector | technology_recall | 0 / 2 / 0 / 4 / 5 | 4 / 6 / 2 / 40 / 25 |
| icecube.mdom | technology_recall | 100 / 100 / 100 / 100 / 100 | 92 / 90 / 88 / 100 / 100 |
| icecube.degg | technology_recall | 4 / 0 / 8 / 24 / 30 | 8 / 0 / 0 / 58 / 70 |
| gerda.successor_named | identity_recall | 16 / 6 / 26 / 10 / 25 | 12 / 0 / 12 / 90 / 95 |
| gerda.inverted_coaxial | technology_recall | 92 / 56 / 74 / 78 / 100 | 78 / 4 / 76 / 100 / 100 |
| gerda.argon_instrumentation | design_recall | 22 / 26 / 14 / 20 / 30 | 16 / 52 / 44 / 6 / 25 |
| exo200.sipm_adoption | technology_recall | 100 / 98 / 100 / 100 / 100 | 100 / 100 / 98 / 100 / 100 |
| exo200.tonne_scale | design_recall | 2 / 0 / 4 / 0 / 30 | 0 / 0 / 0 / 14 / 55 |
| lhcb.velopix | technology_recall | 96 / 86 / 92 / 0 / 0 | 66 / 14 / 70 / 26 / 10 |
| lhcb.scifi | technology_recall | 98 / 98 / 96 / 72 / 85 | 100 / 82 / 100 / 88 / 95 |
| lhcb.software_trigger | design_recall | 66 / 58 / 46 / 24 / 40 | 26 / 34 / 44 / 76 / 45 |
| sno.successor_named | identity_recall | 22 / 2 / 10 / 6 / 30 | 46 / 0 / 36 / 62 / 90 |
| sno.scintillator_fill | technology_recall | 58 / 32 / 50 / 10 / 25 | 30 / 0 / 24 / 48 / 55 |
| sno.tellurium | technology_recall | 2 / 0 / 0 / 0 / 0 | 2 / 0 / 0 / 10 / 20 |
| aligo.fd_squeezing | technology_recall | 100 / 100 / 100 / 100 / 100 | 100 / 100 / 100 / 100 / 100 |
| aligo.filter_cavity | technology_recall | 96 / 100 / 100 / 94 / 60 | 100 / 100 / 98 / 100 / 90 |
| aligo.successor_named | identity_recall | 2 / 0 / 14 / 4 / 0 | 6 / 2 / 4 / 12 / 0 |

## R6. Open-weight comparison on shared cells, with a length control

- S4.5: median output tokens 2246, median characters 7419
- S4.6: median output tokens 3202, median characters 11392
- Q32: median output tokens 680, median characters 3586
- Q72: median output tokens 962, median characters 4836

Pairs with paper conditions on BOTH Qwen sizes: ['aligo', 'darkside', 'exo200', 'lux', 'xenon1t']. D is available for all ten pairs on both sizes.

Claude rates are shown in full and truncated to the median Qwen-72B response length (characters) of the same pair and condition. Truncation is a crude lower bound: it removes later-listed proposals, whereas a shorter answer would choose what to include.

| item | cond | Q32 | Q72 | S4.5 full | S4.5 trunc | S4.6 full | S4.6 trunc |
|---|---|---|---|---|---|---|---|
| darkside.successor_named | A | 40 | 2 | 56 | 4 | 90 | 64 |
| darkside.successor_named | D | 0 | 0 | 8 | 6 | 68 | 50 |
| darkside.sipm_adoption | A | 42 | 48 | 100 | 100 | 100 | 100 |
| darkside.sipm_adoption | D | 6 | 80 | 100 | 100 | 100 | 100 |
| darkside.veto_upgrade_gd | A | 6 | 24 | 22 | 18 | 88 | 14 |
| darkside.veto_upgrade_gd | D | 10 | 0 | 78 | 68 | 98 | 0 |
| protodune.xarapuca | D | 0 | 0 | 100 | 100 | 100 | 100 |
| protodune.coverage_increase | D | 0 | 0 | 0 | 0 | 2 | 2 |
| xenon1t.radon_column | A | 20 | 72 | 36 | 32 | 70 | 46 |
| xenon1t.radon_column | D | 0 | 2 | 30 | 30 | 24 | 4 |
| xenon1t.neutron_veto | A | 24 | 6 | 2 | 0 | 38 | 0 |
| xenon1t.neutron_veto | D | 8 | 10 | 18 | 12 | 54 | 0 |
| lux.successor_named | A | 14 | 2 | 38 | 12 | 18 | 14 |
| lux.successor_named | D | 0 | 0 | 6 | 4 | 60 | 32 |
| lux.xenon_skin | A | 0 | 0 | 2 | 2 | 8 | 8 |
| lux.xenon_skin | D | 0 | 0 | 8 | 8 | 12 | 0 |
| lux.outer_detector | A | 0 | 0 | 0 | 0 | 4 | 0 |
| lux.outer_detector | D | 0 | 0 | 4 | 2 | 40 | 0 |
| icecube.mdom | D | 28 | 36 | 100 | 100 | 100 | 100 |
| icecube.degg | D | 0 | 0 | 24 | 24 | 58 | 56 |
| gerda.successor_named | D | 0 | 0 | 10 | 6 | 90 | 76 |
| gerda.inverted_coaxial | D | 0 | 0 | 78 | 78 | 100 | 100 |
| gerda.argon_instrumentation | D | 0 | 0 | 20 | 20 | 6 | 4 |
| exo200.sipm_adoption | A | 64 | 94 | 100 | 100 | 100 | 100 |
| exo200.sipm_adoption | D | 26 | 98 | 100 | 100 | 100 | 100 |
| exo200.tonne_scale | A | 0 | 0 | 2 | 0 | 0 | 0 |
| exo200.tonne_scale | D | 0 | 0 | 0 | 0 | 14 | 4 |
| lhcb.velopix | D | 0 | 2 | 0 | 0 | 26 | 14 |
| lhcb.scifi | D | 2 | 2 | 72 | 72 | 88 | 54 |
| lhcb.software_trigger | D | 0 | 4 | 24 | 22 | 76 | 24 |
| sno.successor_named | D | 0 | 4 | 6 | 6 | 62 | 24 |
| sno.scintillator_fill | D | 0 | 0 | 10 | 10 | 48 | 18 |
| sno.tellurium | D | 0 | 0 | 0 | 0 | 10 | 2 |
| aligo.fd_squeezing | A | 0 | 2 | 100 | 100 | 100 | 100 |
| aligo.fd_squeezing | D | 2 | 4 | 100 | 100 | 100 | 100 |
| aligo.filter_cavity | A | 2 | 0 | 96 | 96 | 100 | 100 |
| aligo.filter_cavity | D | 0 | 0 | 94 | 94 | 100 | 100 |
| aligo.successor_named | A | 0 | 0 | 2 | 2 | 6 | 0 |
| aligo.successor_named | D | 0 | 0 | 4 | 0 | 12 | 10 |

- Mean over shared A items: Q32: 16, Q72: 19, S4.5: 43, S4.5t: 36, S4.6: 56, S4.6t: 42
- Mean over shared D items: Q32: 3, Q72: 9, S4.5: 38, S4.5t: 37, S4.6: 60, S4.6t: 41

Within-Qwen 32B -> 72B, condition D, all ten pairs (identity vs technology items):

| item | class | Q32 D | Q72 D |
|---|---|---|---|
| darkside.successor_named | identity_recall | 0 [0, 7] | 0 [0, 7] |
| darkside.sipm_adoption | technology_recall | 6 [2, 16] | 80 [67, 89] |
| darkside.veto_upgrade_gd | technology_recall | 10 [4, 21] | 0 [0, 7] |
| protodune.xarapuca | technology_recall | 0 [0, 7] | 0 [0, 7] |
| protodune.successor_named | identity_recall | 0 [0, 7] | 0 [0, 7] |
| protodune.coverage_increase | design_recall | 0 [0, 7] | 0 [0, 7] |
| xenon1t.successor_named | identity_recall | 4 [1, 13] | 0 [0, 7] |
| xenon1t.radon_column | technology_recall | 0 [0, 7] | 2 [0, 10] |
| xenon1t.neutron_veto | technology_recall | 8 [3, 19] | 10 [4, 21] |
| lux.successor_named | identity_recall | 0 [0, 7] | 0 [0, 7] |
| lux.xenon_skin | technology_recall | 0 [0, 7] | 0 [0, 7] |
| lux.outer_detector | technology_recall | 0 [0, 7] | 0 [0, 7] |
| icecube.successor_named | identity_recall | 2 [0, 10] | 0 [0, 7] |
| icecube.mdom | technology_recall | 28 [17, 42] | 36 [24, 50] |
| icecube.degg | technology_recall | 0 [0, 7] | 0 [0, 7] |
| gerda.successor_named | identity_recall | 0 [0, 7] | 0 [0, 7] |
| gerda.inverted_coaxial | technology_recall | 0 [0, 7] | 0 [0, 7] |
| gerda.argon_instrumentation | design_recall | 0 [0, 7] | 0 [0, 7] |
| exo200.successor_named | identity_recall | 0 [0, 7] | 0 [0, 7] |
| exo200.sipm_adoption | technology_recall | 26 [16, 40] | 98 [90, 100] |
| exo200.tonne_scale | design_recall | 0 [0, 7] | 0 [0, 7] |
| lhcb.velopix | technology_recall | 0 [0, 7] | 2 [0, 10] |
| lhcb.scifi | technology_recall | 2 [0, 10] | 2 [0, 10] |
| lhcb.software_trigger | design_recall | 0 [0, 7] | 4 [1, 13] |
| sno.successor_named | identity_recall | 0 [0, 7] | 4 [1, 13] |
| sno.scintillator_fill | technology_recall | 0 [0, 7] | 0 [0, 7] |
| sno.tellurium | technology_recall | 0 [0, 7] | 0 [0, 7] |
| aligo.fd_squeezing | technology_recall | 2 [0, 10] | 4 [1, 13] |
| aligo.filter_cavity | technology_recall | 0 [0, 7] | 0 [0, 7] |
| aligo.successor_named | identity_recall | 0 [0, 7] | 0 [0, 7] |

## Minor: VeloPix, both models

- S4.5: A 96 [87, 99], D 0 [0, 7], D' 0 [0, 16]
- S4.6: A 66 [52, 78], D 26 [16, 40], D' 10 [3, 30]
