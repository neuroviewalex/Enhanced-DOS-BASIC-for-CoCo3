# EDB v15 release synchronization

**Owner-designated authority:** The uploaded BOOT, TOOLS and BENCH attachments at [Release v15](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/tag/v15) supersede earlier local candidates and repository copies. All three are 184,320 bytes. GitHub-reported asset digests:

| Asset | SHA-256 |
| --- | --- |
| [EDB_v15_512k_BOOT.dsk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_BOOT.dsk) | `990b08b28987ada7a137ef1df7696a44286de88325f6eb09e56c4285303dc7bf` |
| [EDB_v15_512k_TOOLS.dsk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_TOOLS.dsk) | `4f0c097bb6d8b7119c374495c778ad83db793329119f85885d55c3bfa5d054f5` |
| [EDB_v15_512k_BENCH.dsk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_BENCH.dsk) | `212e747ff88e376156f0998715dedc8de5cbcd2d6e71caec7e6ee7b510cee11d` |

## Approved behavior

### EDIT R3

`EDIT` with no argument opens the first existing line in RAM; if no program is loaded, it reports `No program loaded.` and returns to the prompt. `EDIT filename` (for example, `EDIT VCC` or `EDIT VCC.BAS`) loads the BASIC listing, opens its first existing line, and leaves it in RAM for subsequent editing or SAVE. A missing filename reports failure without replacing the current listing. `EDIT n` edits the requested existing line. SHIFT + Up/Down browses existing line numbers; ENTER commits and exits. BREAK cancellation remains under investigation; do not rely on it to discard edits until verified. Save valuable unsaved work before loading another program.

### XMM Display Restoration R2

XMM clears before each diagnostic and benchmark stage, including the first, and on button activation. System Info uses a six-TIMER-tick pause (approximately 100 ms at 60 Hz), outside measured benchmark intervals. For transitions, blank both screen buffers before changing video mode, suppress the palette while drawing, then reveal the completed screen. XMM temporarily uses WIDTH 32 but preserves the inherited width, palette (all 16 entries), border and text attributes across program chains and restores them on normal exit. All future EDB graphical applications must restore their inherited video environment, not a fixed default; reuse this template for ASKBENCH. Abnormal exit and full 6809 regression coverage remain outstanding.

Sockmaster's original 60-tick interpreted BASIC loop runs four times without printing or disk I/O inside the timed loop. `SMBENCH.BAS` calculates a rounded mean per 60 ticks, not the sum, and preserves the `SMBSCORE.DAT` record format (`SMBSCORE15` is a compatibility marker, not the current number of trials). At 60 TIMER ticks/sec each trial lasts one second; the benchmark interface displays only basic test/score information, not sample count or duration. In the full suite the viewer opens at page 1; press S or navigate to page 5. Direct aliases `XMM CLASSIC`, `XMM SOCK` and `XMM SOCKMASTER` launch just this test and open page 5 after successful saving.

## Verification and outstanding synchronization

**Verification scope:** On the approved local candidates, VCC-EDB 6309 at 125.28 MHz successfully completed full XMM benchmark and System Info routes from WIDTH 80 with cyan/red colors, plus menu exits from WIDTH 40 (yellow/blue) and WIDTH 32 (green/black). Before/after visible RGB colors matched. The EDIT R3 local candidate passed bare EDIT, empty memory, named and numbered entry, missing-file preservation and LAST tracking; R2 also passed SAVE/NEW/LOAD/RUN and short tests at WIDTH 32/40/80. BREAK, long lines, disk-read failure, abnormal-exit recovery, and further 6809 regression testing are still outstanding. These are earlier candidate test results, not a new test of the uploaded release bytes.

All three uploaded asset binaries match the verified release SHA-256 and Git blob hashes. The repository root images and 116 extracted files are exact copies, with FAT and directory integrity verified. The owner-approved compact HELP.BAS on TOOLS and BENCH is byte-for-byte identical (10,812 bytes). It corrects EDIT, XMM, XBENCH and FIND wording, removes obsolete XMEM terminology, and recovers one granule per disk. The BOOT dispatcher is distinct. Targeted VCC-EDB tests passed on the 6809 and 6309, including WIDTH 32/40/80 on the 6309; not every HELP topic was exercised. The v15 tag is advanced to the synchronized commit only after the verified files are committed, so GitHub-generated Source code (zip) and (tar.gz) refer to the current source.

## Approved compact HELP and final BOOT upload

The owner-approved compact HELP.BAS on TOOLS and BENCH is byte-for-byte identical (10,812 bytes). It corrects EDIT, XMM, XBENCH and FIND wording, removes obsolete XMEM terminology, and recovers one granule per disk. The BOOT dispatcher is distinct. Targeted VCC-EDB tests passed on the 6809 and 6309, including WIDTH 32/40/80 on the 6309; not every HELP topic was exercised.

The final BOOT upload has 54 active files and 6 free granules, with 114 byte differences outside its active file payloads compared with the prior BOOT. TOOLS has 17 active files and 46 free granules; BENCH has 45 active files and 6 free granules. Only the two full HELP payloads changed; all 114 other extracted payloads are identical. No new executable code was generated during synchronization. The exact approved images are the distribution authority.
