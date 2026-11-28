# EDB v15 — Sockmaster Classic BASIC benchmark

**Release synchronization status (2026-11-27):** The owner-designated v15 release attachments, repository disk images and extracted payloads now match exactly. The source inventory is verified; the approved compact HELP passed targeted 6809/6309 VCC tests. Earlier candidate tests are not a full new system regression. See [release synchronization status](RELEASE_SYNC.md).

**Status:** Approved four-trial implementation in the BENCH Display Restoration R2 development lineage. The owner-designated release is authoritative; exact extraction is verified.

**Attribution:** Original three-line BASIC loop credited to Sockmaster.

## Disk image and verification

The latest approved behavior uses four trials, independently persisted CPU-tagged scores with dynamic cached clocks, clean transitions and inherited display restoration.

[Download the official BENCH disk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_BENCH.dsk)

| Property | Value |
| --- | --- |
| Image size | 184,320 bytes |
| SHA-256 | `0cf48fc3ce74c4d96bd13730eb57a126240ab34b6c1297c49f856918caeaaa5d` |
| Git blob SHA | `9d25179e5b0ac7a5564c1725ea461f8fb013040c` |
| Contents | 45 files; 72 allocated and 6 free granules |

GitHub reports the release asset digest above. The [manifest](../extracted/MANIFEST.json) records the verified current extracted snapshot.

## Using the benchmark

Sockmaster's original 60-tick interpreted BASIC loop runs four times without printing or disk I/O inside the timed loop. `SMBENCH.BAS` calculates a rounded mean per 60 ticks, not the sum, and saves independent CPU score/clock pairs in `SMBSCORE.DAT` using the `SMBSCORE2` format after a successful run. At 60 TIMER ticks/sec each trial lasts one second; the benchmark interface displays only basic test/score information, not sample count or duration. In the full suite the viewer opens at page 1; press S or navigate to page 5. Direct aliases `XMM CLASSIC`, `XMM SOCK` and `XMM SOCKMASTER` launch just this test and open page 5 after successful saving.

Page 5 displays independent measured 6809 and 6309 scores and their cached clock speeds, with no fixed-clock gate. SMBENCH reads the CPU name and MHz from the BOOT disk's cached SYSINFO.INF (not live CPU detection); after changing processor or clock, refresh the cache through the normal EDB startup path before benchmarking. The latest run updates only that CPU's pair; the other pair survives. Unmeasured CPU rows show --. The multiplier columns compare the most recently measured score to the historical 6809 bases 100 and 200. The historical 13,544-point result remains a documentation reference, not a substitute for a measured row.

SMBSCORE.DAT uses the SMBSCORE2 marker after the first successful new save, followed by last CPU index (0=6809, 1=6309), 6809 score, 6809 MHz, 6309 score, 6309 MHz, each on its own BASIC sequential-file record. A zero score/clock pair indicates unmeasured. The distributed legacy SMBSCORE15 record is preserved byte-for-byte; it has no CPU tag and must not be assigned to either CPU row. The viewer can still use its untagged score for the multiplier columns. The first successful benchmark migrates it without assigning its old value to a processor. SMBENCH reopens the new record and checks the CPU index and both score/clock pairs before continuing. A valid cache and a writable BENCH working disk are required. Back up score records; the overwrite is not transactional.

Higher scores mean greater interpreted BASIC loop throughput, not pure native CPU speed.

### Original Sockmaster loop

```basic
10 A=0:TIMER=0
20 IF TIMER<60 THEN A=A+1:GOTO20
30 PRINT A:RUN
```

EDB preserves the timed workload from lines 10 and 20, but performs four trials and collects one final average instead of continually restarting.

## Saved result and comparison viewer

Navigate using mouse PREV/NEXT or keyboard N/P. S jumps to page 5, and the centered `<exit>` button or Q returns to the main menu. Both viewers use native GIME colors, inverse hover and a blinking lowercase x. A writable BENCH working disk is required; if saving fails the program prints a warning and the score must not be treated as verified persisted data. A new run replaces only the measured CPU's score/clock pair, retaining the other pair; retain copies for comparisons.

## Comparison references

| Sockmaster historical configuration | Score |
| --- | ---: |
| Motorola 6809 at 1 MHz | 100 |
| Hitachi 6309 native at 1 MHz | 114 |
| Motorola 6809 at 2 MHz | 200 |
| Hitachi 6309 native at 2 MHz | 228 |
| Motorola 6809 with doubled-clock accelerator | 268 |
| Hitachi 6309 native with doubled-clock accelerator | 275 |

**Separate EDB reference:** 13,544 — the project author's recorded EDB v15 result with a 6309 native CPU at 125.28 MHz in VCC-EDB. This is a historical reference only; page 5 displays independently measured scores or --.

The reported four-sample average is directly comparable as a **one-second-equivalent** interpreted BASIC loop count. No reference score is generated or changed by the upgrade.

## Preservation and verification

**Verification scope:** On the approved local candidates, VCC-EDB 6309 at 125.28 MHz successfully completed full XMM benchmark and System Info routes from WIDTH 80 with cyan/red colors, plus menu exits from WIDTH 40 (yellow/blue) and WIDTH 32 (green/black). Before/after visible RGB colors matched. The EDIT R3 local candidate passed bare EDIT, empty memory, named and numbered entry, missing-file preservation and LAST tracking; R2 also passed SAVE/NEW/LOAD/RUN and short tests at WIDTH 32/40/80. BREAK, long lines, disk-read failure, abnormal-exit recovery, and further 6809 regression testing are still outstanding. These are earlier candidate test results, not a new test of the uploaded release bytes.

**Dual-CPU verification:** Approved dual-CPU candidate tests: direct 6809 at cached 125.28 MHz (13,194 points), then 6309 at 125.28 MHz (13,237), preserving the 6809 row, and 6309 at 101.12 MHz (10,596), preserving the earlier 6809 result. Full 6309 XMM suite and WIDTH 80 cyan-on-red restoration passed. Full 6809 suite regression and disk-error recovery remain untested. These are candidate test results, not scores seeded in the distributed image.
