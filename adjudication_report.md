# Systematic Adjudication Report (2026-08-05)
Protocol: ten responses sampled (seed 0) from each of eight headline cells of the
N=50 Claude dataset; regex verdict compared against manual reading of each response
in context. Criterion: does the response contain the frozen key's specific referent.

Cells and outcomes (agreement / 10):
- lhcb.velopix, A, S4.5 (96%): 10/10. All hits are explicit VeloPix ASIC proposals with specifications.
- lhcb.velopix, D, S4.5 (0%): 10/10. True zeros; responses propose MAPS/ALPIDE-style sensors instead (the frozen distractor).
- gerda.successor_named, D, S4.6 (90%): 9/10. One FALSE NEGATIVE: "GERDA/LEGEND-style" phrasing not matched by the frozen expression. Direction: conservative.
- darkside.sipm_adoption, D, S4.5 (100%): 10/10. Genuine adoption proposals naming FBK/Hamamatsu cryogenic SiPMs.
- aligo.fd_squeezing, D, S4.6 (100%): 10/10. Genuine frequency-dependent squeezing proposals with filter cavities.
- gerda.inverted_coaxial, B, S4.6 (4%): 10/10. Correct negatives; responses propose BEGe detectors (era-correct at the 2013 cutoff) in place of post-cutoff ICPC. Qualitative evidence of era-consistent substitution.
- sno.scintillator_fill, A, S4.5 (58%): 10/10. Negatives are construct-correct (6Li neutron strings, veto panels, Gd counters are not a detector-volume fill).
- darkside.successor_named, B, S4.6 (22%): 10/10. Residual mentions sometimes justify DarkSide-20k as predating the 2018 cutoff explicitly; some date-level reasoning coexists with class-level suppression.

Aggregate: 79/80 agreement (98.75%), zero false positives, one conservative false negative.
