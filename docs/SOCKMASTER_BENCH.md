# EDB v15 — Sockmaster Classic BASIC benchmark

**Status:** Included in the official full-color XMM BENCH release; repository and release images match.

**Attribution:** Original three-line BASIC loop credited to Sockmaster.

## Disk image and verification

[Download the official BENCH disk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_BENCH.dsk)

| Property | Value |
| --- | --- |
| Image size | 184,320 bytes |
| SHA-256 | `d731fadab3c6d9972ec58e795538264d75b4f775f3d4b6781052eb67f40b5df0` |
| Git blob SHA | `d4a9b6990326bb5ddf121631a0798f304f6448d5` |
| Contents | 45 files; 71 allocated and 7 free granules |

The official release and extracted files were synchronized and verified against the [manifest](../extracted/MANIFEST.json).

## Using the benchmark

Sockmaster's original 60-tick interpreted BASIC loop runs 15 times without printing or disk I/O inside the timed loop. `SMBENCH.BAS` calculates `INT(S/15+.5)` (rounded mean iterations per 60 ticks, not the total), saves and rereads `SMBSCORE.DAT` with marker `SMBSCORE15`. Older SMBSCORE1 records are not accepted as averages. At 60 TIMER ticks/sec the measurement window is approximately 15 seconds; other tick rates must be accounted for when comparing results. In the full suite the viewer opens at page 1; press S or navigate to page 5. Direct aliases `XMM CLASSIC`, `XMM SOCK` and `XMM SOCKMASTER` launch just this test and open page 5 after successful saving.

The current page 5 layout compares the saved score to the historical 6809 bases 100 (1 MHz) and 200 (2 MHz). It has separate 125.28 MHz point fields for 6809 and 6309. A fresh run with matching CPU/clock profile supplies the applicable field; the 6309 field otherwise retains the project author's historical EDB reference of 13,544. The saved Sockmaster record contains no CPU or MHz tag; it is not two independently persisted CPU scores. Do not attribute a previously saved score to a CPU without the run context. The full historical reference table remains in the documentation, not all on the current screen.

Higher scores mean greater interpreted BASIC loop throughput, not pure native CPU speed.

### Original Sockmaster loop

```basic
10 A=0:TIMER=0
20 IF TIMER<60 THEN A=A+1:GOTO20
30 PRINT A:RUN
```

EDB preserves the timed workload from lines 10 and 20, but performs 15 trials and collects one final average instead of continually restarting.

## Saved result and comparison viewer

Navigate using mouse PREV/NEXT or keyboard N/P. S jumps to page 5, and the centered `<exit>` button or Q returns to the main menu. Both viewers use native GIME colors, inverse hover and a blinking lowercase x. A writable BENCH working disk is required; if saving fails the program prints a warning and the score must not be treated as verified persisted data. A new run replaces the single Sockmaster score record; retain copies for comparisons.

## Comparison references

| Sockmaster historical configuration | Score |
| --- | ---: |
| Motorola 6809 at 1 MHz | 100 |
| Hitachi 6309 native at 1 MHz | 114 |
| Motorola 6809 at 2 MHz | 200 |
| Hitachi 6309 native at 2 MHz | 228 |
| Motorola 6809 with doubled-clock accelerator | 268 |
| Hitachi 6309 native with doubled-clock accelerator | 275 |

**Separate EDB reference:** 13,544 — the project author's recorded EDB v15 result with a 6309 native CPU at 125.28 MHz in VCC-EDB. Page 5 retains the reference in the 6309 field when no applicable fresh measurement is available.

The reported 15-sample average is directly comparable as a **one-second-equivalent** interpreted BASIC loop count. No reference score is generated or changed by the upgrade.

## Preservation and verification

**Verification scope:** The two-menu predecessor completed both workflows under VCC-EDB x64 in Motorola 6809 and Hitachi 6309 configurations. Subsequent native-GIME/full-color/clean-template changes were tested in 6809 mode, including all ten dynamically populated system-information pages, viewer navigation and exit. The earlier diagnostic failure-injection test verified FAIL and unconfirmed fields on a disposable disk; it was not repeated on the final release. Fresh full timed-suite and 6309 runs of the final color revision, physical CoCo 3 testing and standard-clock stress testing remain outstanding. The release images and extracted files were checksum-verified in [synchronization commit 25312509](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/commit/25312509dfe36b52f5f7141199dcac3e14c31297); this documentation update performs no new runtime test.
