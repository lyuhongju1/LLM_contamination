# Answer-key dating table (adoption commitment vs. baseline date)

Classification rule: PRE = commitment more than ~12 months before the baseline's arXiv v1 date; CONTEMPORANEOUS = within ~12 months either side; POST = more than ~12 months after; INDETERMINATE = no reliable source found.
I checked all arXiv dates against the arXiv API (v1 `published` field). I checked LHCb report dates on INSPIRE, because CDS blocked automated access. I checked LIGO DCC dates on dcc.ligo.org.
Where I quote a document's content, I checked it in the full text (ar5iv HTML or PDF), unless the row says otherwise.

## Baseline dates (arXiv v1)

| pair | baseline | v1 date |
|---|---|---|
| darkside | arXiv:1802.07198 (DarkSide-50 532-day) | 2018-02-20 |
| protodune | arXiv:2108.01902 (ProtoDUNE-SP design/construction/operation) | 2021-08-04 |
| xenon1t | arXiv:1708.07051 (XENON1T instrument) | 2017-08-23 |
| lux | arXiv:1211.3788 (LUX experiment) | 2012-11-16 |
| icecube | arXiv:1612.05093 (IceCube instrumentation) | 2016-12-15 |
| gerda | arXiv:1212.4067 (GERDA experiment) | 2012-12-17 |
| exo200 | arXiv:1202.2192 (EXO-200 detector part I) | 2012-02-10 |
| lhcb | arXiv:1412.6352 (LHCb detector performance) | 2014-12-19 |
| sno | arXiv:nucl-ex/9910016 (SNO detector) | 1999-10-25 |
| aligo | arXiv:1411.4547 (Advanced LIGO) | 2014-11-17 |

## Item table

| item | baseline date | adoption-commitment date + source | technology first described + source | class | confidence | note |
|---|---|---|---|---|---|---|
| darkside.successor_named | 2018-02 | 2017-07: arXiv:1707.08145 (DarkSide Collab., "DarkSide-20k: A 20 Tonne Two-Phase LAr TPC…", EPJ Plus 133 (2018) 131). An INSPIRE title search for "DarkSide-20k" before 2017-08 returns only this record | n/a | CONTEMPORANEOUS | high | 7 months before baseline. The referee's claim that DS-20k came first is correct, but the gap is under 12 months. DS-50 baseline text does not mention DS-20k (full-text grep). |
| darkside.sipm_adoption | 2018-02 | 2017-07: arXiv:1707.08145 (SiPM photodetector modules are the design; "SiPM" is a keyword) | Generic SiPM technology long predates this (not sourced here). DS-20k-specific: JINST 15 (2020) C03038, doi:10.1088/1748-0221/15/03/C03038 | CONTEMPORANEOUS | medium | I found no earlier arXiv DarkSide SiPM commitment. A non-arXiv proposal (LNGS/INFN, 2015–16) may exist but is not public. |
| darkside.veto_upgrade_gd | 2018-02 | Gd-loaded PMMA veto: Rossi, "The DarkSide-20k neutron veto", Nuovo Cim. C 44 (2021) 11, doi:10.1393/ncc/i2021-21011-0 (conference record C20-09-14, i.e. Sep 2020; abstract: "a gadolinium-doped veto was developed"). Earlier slides: PATRAS 2019 talk (indico.desy.de event 22598), which has no report number | Gd-loaded LS appears only as one candidate dopant in a figure of arXiv:1707.08145 (2017-07). That paper's baseline veto was a **boron**-loaded LS sphere (TMB) | POST | medium | The 2017 design used a boron LSV. The Gd-PMMA design came from the 2019–2020 redesign. The earliest citable Gd commitment I found is 2020–21, but conference slides from 2019 exist. |
| protodune.successor_named | 2021-08 | 2015-12: arXiv:1512.06148 (LBNF/DUNE CDR Vol. 2, far detector). 2020-02: arXiv:2002.02967 (DUNE FD TDR Vol. I) | Vertical drift: NuFact2021 proceedings, PoS(NuFact2021)173, doi:10.22323/1.402.0173 (conference Sep 2021, published 2022-03). FD2-VD TDR arXiv:2312.03130 (2023-12) | PRE | high | **The baseline itself** says ProtoDUNE-SP "is a prototype for the first far detector module of DUNE". The "far detector"/"horizontal drift" match is therefore not a future item at all. Only the "vertical drift" sub-pattern is contemporaneous or post. |
| protodune.xarapuca | 2021-08 | 2020-02: arXiv:2002.03010 (DUNE FD TDR Vol. IV): "The X-ARAPUCA, adopted as the baseline design" | 2018-04: arXiv:1804.01407 (Machado et al., "The X-ARAPUCA…") | PRE | high | ProtoDUNE-SP already ran 2 ARAPUCA modules (baseline text). |
| protodune.coverage_increase | 2021-08 | Sep 2021: PoS(NuFact2021)173, doi:10.22323/1.402.0173 ("enhanced photo-detection system… on the cryostat walls and the cathode"). Formal: arXiv:2312.03130 (VD TDR, 2023-12) | Same | CONTEMPORANEOUS | low | The item is vague. The baseline reports ~12.5% APA-surface coverage. If the key means VD's cathode/wall PDS, the first public proposal is about 1 month after the baseline and the TDR is POST. |
| xenon1t.successor_named | 2017-08 | 2015-12: arXiv:1512.07501 (XENON1T physics reach; Sec. 7.1 "Sensitivity projection towards XENONnT") | n/a | PRE | high | The baseline itself also describes XENONnT as "already in the technical design phase". |
| xenon1t.radon_column | 2017-08 | 2017-02: arXiv:1702.06942 (XENON100 online Rn distillation): "For… XENON1T, XENONnT… a radon distillation column… is currently under investigation". Firm design: arXiv:2007.08796 (2020-07), arXiv:2205.11492 (2022-05) | Online Rn removal R&D noted in arXiv:1512.07501 (2015-12) | CONTEMPORANEOUS | medium | The baseline (1708.07051) already describes the online Rn-removal demonstration using a reversed Kr column. This is arguably in the baseline itself. |
| xenon1t.neutron_veto | 2017-08 | 2020-07: arXiv:2007.08796 ("the addition of a new neutron veto"; Gd-loaded water tank) | Generic Gd-water neutron tagging predates this (not sourced) | POST | medium | Earliest arXiv source I found. Earlier talks (2018–19) may exist. Adoption caveat: per arXiv:2412.05264, the NV ran with **demineralized water (no Gd)** in the first science runs. Gd was added later. |
| lux.successor_named | 2012-11 | 2011-10: arXiv:1110.0103 (Malling et al., "After LUX: The LZ Program", "LZ program (LUX-ZEPLIN)") | n/a | PRE | high | 13 months before the baseline, at the edge of the window. The merged LZ collaboration followed in 2012 (I have no primary source for the formation date). |
| lux.xenon_skin | 2012-11 | 2015-09: arXiv:1509.02910 (LZ CDR: "active Xe 'skin' layer") | LXe active veto layer in XENON100: arXiv:1107.2155 (2011-07). I did not verify this in full text | POST | medium | Not in 1110.0103 (grep). Not in Snowmass CF1 report arXiv:1310.8327. Possibly in unpublished 2013–14 LZ documents. |
| lux.outer_detector | 2012-11 | Generic: 2011-10, arXiv:1110.0103 Sec. II.6 ("organic scintillator volume surrounding the active region… instrumented with large-area PMTs"). Gd-loaded LAB: 2015-09, arXiv:1509.02910 | ZEPLIN-III Gd-loaded plastic veto (cited in the CDR; not separately sourced) | PRE (generic) / POST (Gd-specific) | medium | The class depends on whether the key requires "Gd-loaded". |
| icecube.successor_named | 2016-12 | 2014-12: arXiv:1412.5106 (IceCube-Gen2 vision). 2014-01: arXiv:1401.2046 (PINGU LoI). IceCube Upgrade: arXiv:1908.09441 (2019-08) | n/a | PRE | high | The baseline itself has Sec. 7.1 "IceCube Gen2 and PINGU". |
| icecube.mdom | 2016-12 | 2014-01: arXiv:1401.2046v1 (PINGU LoI §14.2 "Multi-PMT Optical Modules (mDOMs)", as an R&D direction; §5.4.1 in v2). Firm deployment: IceCube Upgrade, arXiv:1908.09441 (2019-08) | Same LoI (KM3NeT multi-PMT concept is earlier; not sourced) | PRE | medium | First collaboration proposal is PRE. Firm adoption (Upgrade) is POST. |
| icecube.degg | 2016-12 | 2015-10: arXiv:1510.05228 (IceCube-Gen2 ICRC 2015 contributions, PoS(ICRC2015)1137, "A dual-PMT optical module (D-Egg) for IceCube-Gen2", first prototype) | n/a | PRE | medium | Corrected 2026-11-04: the PINGU LoI v1 (2014-01) does not mention D-Egg; its D-Egg section (§5.4.2) was added in v2. 14 months before the baseline, so PRE stands. Firm adoption (Upgrade) is POST. |
| gerda.successor_named | 2012-12 | 2017-09: arXiv:1709.01980 (LEGEND) | n/a | POST | high | |
| gerda.inverted_coaxial | 2012-12 | 2017-09: arXiv:1709.01980 ("larger PPC… via an 'inverted-coaxial' design") | Cooper et al., NIM A 665 (2011) 25, doi:10.1016/j.nima.2011.10.008 | POST | high | Technology predates the baseline. The adoption commitment is post. |
| gerda.argon_instrumentation | 2012-12 | 2004-04: arXiv:hep-ex/0404039 (GERDA proposal; "optionally active" cryostat, §7.7 "Instrumentation of liquid argon"). The baseline 1212.4067 itself states "Gerda decided to implement a LAr scintillation light veto for Phase II" | LArGe test facility (cited in the baseline). LArGe paper arXiv:1501.05762 (2015) | PRE | high | This is **in the baseline paper**, so it is not a future upgrade. Phase II realisation: arXiv:1711.01452 (2017-11). |
| exo200.successor_named | 2012-02 | 2013-10: arXiv:1310.4340 (Snowmass "Neutrinos" report: "The EXO collaboration is planning a 5-ton detector called nEXO"; cites a Gratta 2013 nEXO white paper, which is not on arXiv) | n/a | POST | medium | No "nEXO" in the baseline or in arXiv:1205.5608 (2012-05). An INSPIRE title search finds no nEXO before 2014-10. The name may have been used in 2012 talks (not found). |
| exo200.sipm_adoption | 2012-02 | 2015-02: arXiv:1502.07837 ("SiPMs are photodetectors under investigation for use in nEXO") | Generic (not sourced) | POST | high | EXO-200 used LAAPDs (baseline). |
| exo200.tonne_scale | 2012-02 | 2000-02: arXiv:hep-ex/0002003 (Danilov et al., original EXO concept: "1 to 2 tons of Xe-136"). The baseline itself says EXO-200 is "a technology test bed for a future, larger detector". 5 t: arXiv:1310.4340 (2013-10) | Same | PRE | high | The tonne-scale goal is the program's founding concept. The specific 5-tonne figure is POST. |
| lhcb.velopix | 2014-12 | 2013-11: CERN-LHCC-2013-021 / LHCb-TDR-013 (VELO Upgrade TDR; abstract: "read out by the custom developed VeloPix front end ASIC"), INSPIRE 1614086 | Same TDR (Timepix3 lineage; not sourced) | PRE | high | 13 months before the baseline. **The baseline 1412.6352 cites this TDR** (ref. [96]). |
| lhcb.scifi | 2014-12 | 2014-02: CERN-LHCC-2014-001 / LHCb-TDR-015 (Tracker Upgrade TDR), INSPIRE 1614088 | Not checked. The SciFi option may appear in the 2012 Framework TDR, but the abstract does not mention it | CONTEMPORANEOUS | medium | 10 months before the baseline. **The baseline cites this TDR** (ref. [98]). The SciFi content of the TDR comes from its title and general knowledge. I did not read the TDR text itself. |
| lhcb.software_trigger | 2014-12 | 2011-03: CERN-LHCC-2011-001 (LoI for the LHCb Upgrade; abstract: "read out at 40 MHz, a much more flexible software-based triggering strategy"), INSPIRE 1391029. Trigger & Online TDR: CERN-LHCC-2014-016 (2014-05) | Same | PRE | high | The baseline cites the LoI and all TDRs (refs. [94]–[99]). |
| sno.successor_named | 1999-10 | 2004-09 (NOW 2004) / published 2005: M.C. Chen, "The SNO liquid scintillator project", Nucl. Phys. B Proc. Suppl. 145 (2005) 65, doi:10.1016/j.nuclphysbps.2005.03.037. Name "SNO+": Kraus, Prog. Part. Nucl. Phys. 57 (2006) 150, doi:10.1016/j.ppnp.2005.12.001 | n/a | POST | high | |
| sno.scintillator_fill | 1999-10 | Same as above (2004–05) | LAB as the specific scintillator: not verified in these abstracts | POST | high (LS fill) / low (LAB-specific date) | |
| sno.tellurium | 1999-10 | 2014-05: arXiv:1405.3401 (Biller, "SNO+ with Tellurium"). Status: arXiv:1508.05759 (2015-08) | Not sourced | POST | high | Earlier plan was Nd loading (e.g. AIP Conf. Proc. 942 (2007) 101, doi:10.1063/1.2805112). Te replaced Nd around 2013–14. |
| aligo.fd_squeezing | 2014-11 | 2014-12-01: LIGO-T1400316-v4 (LSC Instrument Science White Paper, §3.1 "A+", "16 m filter cavity"). 2014-10: arXiv:1410.5882 (Miller et al., LIGO-authored upgrade study) | 2000-08: arXiv:gr-qc/0008026 (Kimble et al., PRD 65 022002) | CONTEMPORANEOUS | high | Implemented in O4: Ganapathy et al., PRX 13, 041021 (2023-10), doi:10.1103/PhysRevX.13.041021. |
| aligo.filter_cavity | 2014-11 | Same as above (2014-10 / 2014-12) | gr-qc/0008026 (2000-08). Realistic FCs for advanced detectors: arXiv:1305.1599 (2013-05) | CONTEMPORANEOUS | high | If 1305.1599 (Evans et al., LIGO-affiliated authors) counts as a commitment, the class becomes PRE (18 months). I treat it as a technology study, not a collaboration commitment. |
| aligo.successor_named | 2014-11 | 2014-12-01: LIGO-T1400316-v4 (§2.1 / §3.1 "A+"). A+ design curve: LIGO-T1800042 (2018-03) | n/a | CONTEMPORANEOUS | high (A+) / indeterminate ("aLIGO+") | Earlier T1400316 versions (v1–v3) may predate v4. I did not check them. I found no source for the "aLIGO+" spelling. |

## Summary

Counts (30 items):
- **PRE-baseline: 12.** protodune.successor_named, protodune.xarapuca, xenon1t.successor_named, lux.successor_named, lux.outer_detector (generic LS veto; POST if Gd-specific), icecube.successor_named, icecube.mdom, icecube.degg, gerda.argon_instrumentation, exo200.tonne_scale, lhcb.velopix, lhcb.software_trigger.
- **CONTEMPORANEOUS: 8.** darkside.successor_named, darkside.sipm_adoption, protodune.coverage_increase, xenon1t.radon_column, lhcb.scifi, aligo.fd_squeezing, aligo.filter_cavity, aligo.successor_named.
- **POST-baseline: 10.** darkside.veto_upgrade_gd, xenon1t.neutron_veto, lux.xenon_skin, gerda.successor_named, gerda.inverted_coaxial, exo200.successor_named, exo200.sipm_adoption, sno.successor_named, sno.scintillator_fill, sno.tellurium.
- **INDETERMINATE: 0.** No item lacks a source entirely. Sub-claims flagged in the notes are marked low or indeterminate.

Items that are effectively **in the baseline paper's own text or references**:
- protodune.successor_named: the far detector is named in the baseline.
- gerda.argon_instrumentation: the Phase II LAr veto decision is stated in the baseline.
- xenon1t.successor_named: XENONnT is described in the baseline.
- xenon1t.radon_column: online Rn removal is described in the baseline.
- icecube.successor_named: the baseline has a Gen2/PINGU section.
- exo200.tonne_scale: the baseline says EXO-200 is a "test bed for a future, larger detector".
- lhcb.velopix, lhcb.scifi, lhcb.software_trigger: the baseline cites the upgrade LoI and TDRs.

Adoption caveats:
- darkside.veto_upgrade_gd: the Gd design replaced the 2017 boron-LS plan.
- xenon1t.neutron_veto: early runs used water without Gd.
- icecube.mdom and icecube.degg: proposed as R&D in 2014, firmly adopted in 2019.
- sno.tellurium: Te replaced the earlier Nd plan.
