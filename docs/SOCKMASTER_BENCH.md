# EDB v15 — Sockmaster Classic BASIC benchmark

**Release synchronization status (2026-11-27):** The owner-designated v15 release attachments, repository disk images and extracted payloads now match exactly. The source inventory is verified; earlier candidate emulator results are not new tests of these uploaded bytes. See [release synchronization status](RELEASE_SYNC.md).

**Status:** Approved four-trial implementation in the BENCH Display Restoration R2 development lineage. The owner-designated release is authoritative; exact extraction is verified.

**Attribution:** Original three-line BASIC loop credited to Sockmaster.

## Disk image and verification

The latest approved behavior uses four trials, a simplified score display, clean transitions and inherited display restoration.

[Download the official BENCH disk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_BENCH.dsk)

| Property | Value |
| --- | --- |
| Image size | 184,320 bytes |
| SHA-256 | `15293d31bcc4a81e16f5298640fbf75c08d1f4c6ab04bf31e4824b57565b581a` |
| Git blob SHA | `bb3d55a03ea151b8568fd949bab9fe2deed9a762` |
| Contents | 45 files; 73 allocated and 5 free granules |

GitHub reports the release asset digest above. The [manifest](../extracted/MANIFEST.json) records the verified current extracted snapshot.

## Using the benchmark

Sockmaster's original 60-tick interpreted BASIC loop runs four times without printing or disk I/O inside the timed loop. `SMBENCH.BAS` calculates a rounded mean per 60 ticks, not the sum, and preserves the `SMBSCORE.DAT` record format (`SMBSCORE15` is a compatibility marker, not the current number of trials). At 60 TIMER ticks/sec each trial lasts one second; the benchmark interface displays only basic test/score information, not sample count or duration. In the full suite the viewer opens at page 1; press S or navigate to page 5. Direct aliases `XMM CLASSIC`, `XMM SOCK` and `XMM SOCKMASTER` launch just this test and open page 5 after successful saving.

The current page 5 layout compares the saved score to the historical 6809 bases 100 (1 MHz) and 200 (2 MHz). It has separate 125.28 MHz point fields for 6809 and 6309. A fresh run with matching CPU/clock profile supplies the applicable field; the 6309 field otherwise retains the project author's historical EDB reference of 13,544. The saved Sockmaster record contains no CPU or MHz tag; it is not two independently persisted CPU scores. Do not attribute a previously saved score to a CPU without the run context. The full historical reference table remains in the documentation, not all on the current screen.

Higher scores mean greater interpreted BASIC loop throughput, not pure native CPU speed.

### Original Sockmaster loop

```basic
10 A=0:TIMER=0
20 IF TIMER<60 THEN A=A+1:GOTO20
30 PRINT A:RUN
```

EDB preserves the timed workload from lines 10 and 20, but performs four trials and collects one final average instead of continually restarting.

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

The reported four-sample average is directly comparable as a **one-second-equivalent** interpreted BASIC loop count. No reference score is generated or changed by the upgrade.

## Preservation and verification

**Verification scope:** On the approved local candidates, VCC-EDB 6309 at 125.28 MHz successfully completed full XMM benchmark and System Info routes from WIDTH 80 with cyan/red colors, plus menu exits from WIDTH 40 (yellow/blue) and WIDTH 32 (green/black). Before/after visible RGB colors matched. The EDIT R3 local candidate passed bare EDIT, empty memory, named and numbered entry, missing-file preservation and LAST tracking; R2 also passed SAVE/NEW/LOAD/RUN and short tests at WIDTH 32/40/80. BREAK, long lines, disk-read failure, abnormal-exit recovery, and further 6809 regression testing are still outstanding. These are earlier candidate test results, not a new test of the uploaded release bytes.
