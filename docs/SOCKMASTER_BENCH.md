# EDB v15 - Sockmaster Classic BASIC Benchmark

**Status:** Official EDB v15 BENCH baseline, Sockmaster Classic BASIC FIX2. Release image and repository disk SHA-256 checksums match.  
**Attribution:** Classic three-line BASIC loop credited to **Sockmaster**.  
**Scope:** BENCH disk, extracted source, score format, and XMSHOW comparison page. BOOT and TOOLS are unchanged.

## Official BENCH download

[Download verified v15 BENCH disk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_bench.dsk) | [Repository disk image](../EDB_v15_512k_bench.dsk)

SHA-256: `9ea442c53e9d73e0cc30f457818f28f937939e3d77021bce22df95744611e67a`  
Git blob SHA: `788456b9474ad23c23d829aa78a41bf88c276a0a`

The published BENCH Release asset matches this repository image, including the fifth XMSHOW comparison page.  
Image size: 184,320 bytes; 24 files; 31 free granules.

## How to use

With the official BENCH disk available to EDB:

1. Enter `XMM` to open the existing diagnostics menu.
2. Press **L - Classic** to run the one-second Sockmaster benchmark.
3. The timed loop runs once and writes a new `SMBSCORE.DAT` file on the **current default drive**, if writable.
4. The program reopens the saved score to verify it, then opens **XMSHOW page 5/5** automatically.
5. From XMSHOW, use **N** for next, **P** for previous, **S** for the Sockmaster comparison page, and **Q** for the XMM menu. FIX2 retains key input for the S shortcut and wraps backward from page 1 to page 5.

The command `XMM CLASSIC` (also `XMM SOCK` or `XMM SOCKMASTER`) can launch the test without using the interactive menu. **XMM's existing internal S diagnostic shortcut remains unchanged.**

### Original algorithm

```basic
10 A=0:TIMER=0
20 IF TIMER<60 THEN A=A+1:GOTO20
30 PRINT A:RUN
```

The program retains lines **10** and **20** as the timed workload. After line 20 reaches 60 ticks, it captures `A`, rather than executing the original `PRINT A:RUN` endless output/restart loop. All file operations, reporting, and page display happen **outside** the timing window.

**Metric:** One-second interpreted BASIC loop count. Higher is better. It depends on CPU, interpreter/ROM, clock and emulation. It is not a pure machine-code CPU measurement.

## Historical comparison table

| Configuration | Sockmaster historical score |
| --- | ---: |
| Motorola 6809 - 1 MHz | 100 |
| Hitachi 6309 native - 1 MHz | 114 |
| Motorola 6809 - 2 MHz | 200 |
| Hitachi 6309 native - 2 MHz | 228 |
| Motorola 6809 - doubled-clock accelerator | 268 |
| Hitachi 6309 native - doubled-clock accelerator | 275 |

**Separate EDB reference:** 13,544 - Hitachi 6309 native mode, 125.28 MHz, EDB v15 on VCC-EDB with custom ROMs; supplied by the project author. This is a recorded observation, not a computed Sockmaster baseline.

The new viewer **page 5/5** displays all six historical scores, the measured score (or `--` if not yet run), its ratio to each baseline, and the 13,544 EDB reference plus its current-score ratio. The on-screen legend distinguishes historical Sockmaster results from the EDB reference.

## Changed/new BASIC files

| File | Change |
| --- | --- |
| `SMBENCH.BAS` | New single-run Sockmaster loop, persistent score/verification, automatic viewer handoff; FIX2 corrects tokenized GOTO/THEN on lines 20, 40 and 70 |
| `XMM.BAS` | Added `L` menu entry and CLASSIC/SOCK command aliases, preserving all existing diagnostic keys |
| `XMSHOW.BAS` | Five-page navigation, dedicated Sockmaster score comparison and S shortcut; FIX2 corrects 15 ASCII control-flow keywords in 14 changed lines, restores S input, fixes backward wrap and headings |

A fresh runtime measurement is saved as **`SMBSCORE.DAT`**, a new file with format `SMBSCORE1` followed by the numeric score. It is created on first successful run, **not** pre-injected into the official disk, so a genuine measurement is distinguishable from the fixed reference.

If writing/verification fails, SMBENCH displays the result and an error instead of claiming to have saved it. The viewer shows "CURRENT SCORE --" when there is no valid record.


## Implementation and compatibility

The benchmark retains Sockmaster's original 60-tick interpreted BASIC loop. Its result is captured once, stored in a versioned score file when the active drive is writable, verified by readback, and displayed on XMSHOW page **5/5**.

The native CoCo BASIC statements are correctly tokenized. XMSHOW supports **N/P** page navigation, **S** for the Sockmaster page, **Q** to return to XMM, and correct wraparound across all five pages.

This release is the user-promoted FIX2 BENCH baseline. The source and disk-image structure have been verified; independent emulator/hardware runtime testing is a separate validation activity.

## Preservation and verification

The promoted BENCH disk retains all 23 files from the previous official baseline and adds one. Only the contents of `XMM.BAS` and `XMSHOW.BAS` changed; all 21 other original files are byte-for-byte identical. All FAT and directory changes were confined to those two files and the new program; no unrelated data sectors were changed. BOOT and TOOLS remain unchanged; BENCH on GitHub `main` is now the user-promoted FIX2 image.

**Verification:** The official BENCH disk and all its extracted files have passed static integrity checks. Its published Release asset also matches the official disk checksum.
