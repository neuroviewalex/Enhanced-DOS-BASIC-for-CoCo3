# EDB v15 — Sockmaster Classic BASIC benchmark

**Status:** Owner-approved **15-second-average** BENCH baseline in the repository. The GitHub v15 Release BENCH attachment still contains the previous version until the owner updates it manually.

**Attribution:** Original three-line BASIC loop credited to Sockmaster.

## Disk image and verification

[Download the current BENCH disk from `main`](https://raw.githubusercontent.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/main/EDB_v15_512k_bench.dsk)

| Property | Value |
| --- | --- |
| Image size | 184,320 bytes |
| SHA-256 | `005453f873ef2deec20eecbc62601f336d858be27414f3866c9735ba2d633549` |
| Git blob SHA | `24fc14b502a2d8a649dbb3b8954d25bf13483191` |
| Contents | 24 files; 47 allocated and 31 free granules |
| Updated programs | `SMBENCH.BAS` and `XMSHOW.BAS` |
| Unchanged | Remaining 22 BENCH files and all BOOT/TOOLS disk images |

The disk was verified against the prior official BENCH image. All file contents outside the two updated BASIC programs are byte-identical; the existing FAT and directory allocation are preserved. The original tokenized BASIC and new linked-line structure were validated.

**Release publication:** The [v15 Release page](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/tag/v15) still contains the prior BENCH attachment with SHA-256 `9ea442c53e9d73e0cc30f457818f28f937939e3d77021bce22df95744611e67a`. Updating `main` does not replace Release attachments automatically.

## Using the benchmark

Run `XMM` and choose **L — Classic**, or launch through `XMM CLASSIC`, `XMM SOCK` or `XMM SOCKMASTER`.

The program takes **15 consecutive one-second (60-TIMER-tick) measurements**. Each measurement runs the original Sockmaster loop without printing or disk access. The 15 loop counts are accumulated and the score is calculated as `SC=INT(S/15+.5)` — the rounded **mean number of BASIC loop iterations per second**, not the 15-second total.

The test runs for approximately 15 seconds plus small setup overhead. Higher scores indicate more interpreted BASIC loop throughput; this is not a native machine-code CPU benchmark.

### Original Sockmaster loop

```basic
10 A=0:TIMER=0
20 IF TIMER<60 THEN A=A+1:GOTO20
30 PRINT A:RUN
```

EDB preserves the timed workload from lines 10 and 20, but performs 15 trials and collects one final average instead of continually restarting.

## Saved result and comparison viewer

After measurement, `SMBENCH.BAS` writes `SMBSCORE.DAT` to the writable current drive and verifies the saved data by reopening it. The file records the identifier `SMBSCORE15` followed by the measured numeric average. Older `SMBSCORE1` files are **not** displayed as 15-second averages.

When saving succeeds, the program opens **XMSHOW page 5/5** automatically. The viewer labels the result `15S AVG SCORE`; absent or invalid score data displays `15S AVG SCORE --`. Use **N** for next page, **P** for previous, **S** to jump to Sockmaster page 5 and **Q** to return to XMM. The preexisting XMM S diagnostic is unaffected.

If saving or verification fails, the measured score is still displayed with a warning rather than falsely reported as persisted.

## Comparison references

| Sockmaster historical configuration | Score |
| --- | ---: |
| Motorola 6809 at 1 MHz | 100 |
| Hitachi 6309 native at 1 MHz | 114 |
| Motorola 6809 at 2 MHz | 200 |
| Hitachi 6309 native at 2 MHz | 228 |
| Motorola 6809 with doubled-clock accelerator | 268 |
| Hitachi 6309 native with doubled-clock accelerator | 275 |

**Separate EDB reference:** 13,544 — the project author's previously recorded EDB v15 result with a 6309 native CPU at 125.28 MHz in VCC-EDB. The viewer preserves this comparison separately from Sockmaster's historical references.

The reported 15-sample average is directly comparable as a **one-second-equivalent** interpreted BASIC loop count. No reference score is generated or changed by the upgrade.

## Preservation

This change was explicitly promoted by the project owner after receiving the candidate for VCC-EDB testing. Tokenized-BASIC structure, FAT/directory integrity and byte-for-byte preservation of unrelated files were verified. These static tests do not constitute a separate live emulator or hardware run by the assistant.
