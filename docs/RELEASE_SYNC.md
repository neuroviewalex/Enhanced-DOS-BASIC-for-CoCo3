# EDB v15 release synchronization

**Owner-designated authority:** The uploaded BOOT, TOOLS and BENCH attachments at [Release v15](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/tag/v15) supersede earlier local candidates and repository copies. All three are 184,320 bytes. GitHub-reported asset digests:

| Asset | SHA-256 |
| --- | --- |
| [EDB_v15_512k_BOOT.dsk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_BOOT.dsk) | `2869705a904eabafb1b9de541d0f265a8db4d6ace0851e0aad661e47b16e6175` |
| [EDB_v15_512k_TOOLS.dsk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_TOOLS.dsk) | `3afcb90370d9aff975be06ff1cdde0ce5aea89e7abb959c7324617cc4f1b196e` |
| [EDB_v15_512k_BENCH.dsk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_BENCH.dsk) | `15293d31bcc4a81e16f5298640fbf75c08d1f4c6ab04bf31e4824b57565b581a` |

## Approved behavior

### EDIT R3

`EDIT` with no argument opens the first existing line in RAM; if no program is loaded, it reports `No program loaded.` and returns to the prompt. `EDIT filename` (for example, `EDIT VCC` or `EDIT VCC.BAS`) loads the BASIC listing, opens its first existing line, and leaves it in RAM for subsequent editing or SAVE. A missing filename reports failure without replacing the current listing. `EDIT n` edits the requested existing line. SHIFT + Up/Down browses existing line numbers; ENTER commits and exits. BREAK cancellation remains under investigation; do not rely on it to discard edits until verified. Save valuable unsaved work before loading another program.

### XMM Display Restoration R2

XMM clears before each diagnostic and benchmark stage, including the first, and on button activation. System Info uses a six-TIMER-tick pause (approximately 100 ms at 60 Hz), outside measured benchmark intervals. For transitions, blank both screen buffers before changing video mode, suppress the palette while drawing, then reveal the completed screen. XMM temporarily uses WIDTH 32 but preserves the inherited width, palette (all 16 entries), border and text attributes across program chains and restores them on normal exit. All future EDB graphical applications must restore their inherited video environment, not a fixed default; reuse this template for ASKBENCH. Abnormal exit and full 6809 regression coverage remain outstanding.

Sockmaster's original 60-tick interpreted BASIC loop runs four times without printing or disk I/O inside the timed loop. `SMBENCH.BAS` calculates a rounded mean per 60 ticks, not the sum, and preserves the `SMBSCORE.DAT` record format (`SMBSCORE15` is a compatibility marker, not the current number of trials). At 60 TIMER ticks/sec each trial lasts one second; the benchmark interface displays only basic test/score information, not sample count or duration. In the full suite the viewer opens at page 1; press S or navigate to page 5. Direct aliases `XMM CLASSIC`, `XMM SOCK` and `XMM SOCKMASTER` launch just this test and open page 5 after successful saving.

## Verification and outstanding synchronization

**Verification scope:** On the approved local candidates, VCC-EDB 6309 at 125.28 MHz successfully completed full XMM benchmark and System Info routes from WIDTH 80 with cyan/red colors, plus menu exits from WIDTH 40 (yellow/blue) and WIDTH 32 (green/black). Before/after visible RGB colors matched. The EDIT R3 local candidate passed bare EDIT, empty memory, named and numbered entry, missing-file preservation and LAST tracking; R2 also passed SAVE/NEW/LOAD/RUN and short tests at WIDTH 32/40/80. BREAK, long lines, disk-read failure, abnormal-exit recovery, and further 6809 regression testing are still outstanding. These are earlier candidate test results, not a new test of the uploaded release bytes.

The three uploaded asset binaries could not be downloaded in this session. The previous repository images and extracted sources remain unchanged, with their actual prior hashes retained in [MANIFEST.json](../extracted/MANIFEST.json). Do not substitute prior candidates for the release attachments. After retrieving all three exact images, verify each SHA-256, parse FAT chains and directory entries, extract all payloads, compare HELP copies and update their EDIT/XMM topics if necessary as a separately verified disk revision, then update the root images, extracted files, manifest, documentation and release source archive/tag. Preserve the owner-approved release binaries; no unapproved edits or baseline promotions.
