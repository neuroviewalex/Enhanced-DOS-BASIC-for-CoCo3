# EDB v15 release synchronization

**Owner-designated authority (2026-11-28):** BOOT and TOOLS remain the verified v15 attachments. BENCH FIX13 is the authoritative [repository image](https://raw.githubusercontent.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/main/EDB_v15_512k_bench.dsk). GitHub metadata confirms the previous FIX11 attachment is published; FIX13 attachment replacement and tag synchronization are pending. The table records the current release attachment digests, not the new BENCH baseline.

| Asset | SHA-256 |
| --- | --- |
| [EDB_v15_512k_BOOT.dsk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_BOOT.dsk) | `990b08b28987ada7a137ef1df7696a44286de88325f6eb09e56c4285303dc7bf` |
| [EDB_v15_512k_TOOLS.dsk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_TOOLS.dsk) | `4f0c097bb6d8b7119c374495c778ad83db793329119f85885d55c3bfa5d054f5` |
| [EDB_v15_512k_BENCH.dsk](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_bench.dsk) | `747838009a90129a3f9f3d96b2e28def533f7c0a8c63020c162edad36125b385` |

## Approved behavior

### EDIT R3

`EDIT` with no argument opens the first existing line in RAM; if no program is loaded, it reports `No program loaded.` and returns to the prompt. `EDIT filename` (for example, `EDIT VCC` or `EDIT VCC.BAS`) loads the BASIC listing, opens its first existing line, and leaves it in RAM for subsequent editing or SAVE. A missing filename reports failure without replacing the current listing. `EDIT n` edits the requested existing line. SHIFT + Up/Down browses existing line numbers; ENTER commits and exits. BREAK cancellation remains under investigation; do not rely on it to discard edits until verified. Save valuable unsaved work before loading another program.

### XMM Display Restoration R2

XMM clears before each diagnostic and benchmark stage, including the first, and on button activation. System Info uses a six-TIMER-tick pause (approximately 100 ms at 60 Hz), outside measured benchmark intervals. For transitions, blank both screen buffers before changing video mode, suppress the palette while drawing, then reveal the completed screen. XMM temporarily uses WIDTH 32 but preserves the inherited width, palette (all 16 entries), border and text attributes across program chains and restores them on normal exit. All future EDB graphical applications must restore their inherited video environment, not a fixed default; reuse this template for ASKBENCH. Abnormal exit and full 6809 regression coverage remain outstanding.

Sockmaster's original 60-tick interpreted BASIC loop runs four times without printing or disk I/O inside the timed loop. `SMBENCH.BAS` calculates a rounded mean per 60 ticks, not the sum, and saves independent CPU score/clock pairs in `SMBSCORE.DAT` using the `SMBSCORE2` format after a successful run. At 60 TIMER ticks/sec each trial lasts one second; the benchmark interface displays only basic test/score information, not sample count or duration. In the full suite the viewer opens at page 1; press S or navigate to page 5. Direct aliases `XMM CLASSIC`, `XMM SOCK` and `XMM SOCKMASTER` launch just this test and open page 5 after successful saving.

## Verification and outstanding synchronization

**Verification scope:** On the approved local candidates, VCC-EDB 6309 at 125.28 MHz successfully completed full XMM benchmark and System Info routes from WIDTH 80 with cyan/red colors, plus menu exits from WIDTH 40 (yellow/blue) and WIDTH 32 (green/black). Before/after visible RGB colors matched. The EDIT R3 local candidate passed bare EDIT, empty memory, named and numbered entry, missing-file preservation and LAST tracking; R2 also passed SAVE/NEW/LOAD/RUN and short tests at WIDTH 32/40/80. BREAK, long lines, disk-read failure, abnormal-exit recovery, and further 6809 regression testing are still outstanding. These are earlier candidate test results, not a new test of the uploaded release bytes.

At the preceding synchronization, all three uploaded binaries matched their release hashes and repository/extraction. After the FIX11 promotion, only BOOT and TOOLS retain that exact release-attachment equivalence. BENCH's updated root image and extraction are verified separately. The v15 attachment and tag require a separate update; do not treat the GitHub-generated source archives or old BENCH attachment as the FIX11 baseline.

## Approved compact HELP and final BOOT upload

The owner-approved compact HELP.BAS on TOOLS and BENCH is byte-for-byte identical (10,812 bytes). It corrects EDIT, XMM, XBENCH and FIND wording, removes obsolete XMEM terminology, and recovers one granule per disk. The BOOT dispatcher is distinct. Targeted VCC-EDB tests passed on the 6809 and 6309, including WIDTH 32/40/80 on the 6309; not every HELP topic was exercised.

The final BOOT upload has 54 active files and 6 free granules, with 114 byte differences outside its active file payloads compared with the prior BOOT. TOOLS has 17 active files and 46 free granules; BENCH has 45 active files and 6 free granules. At that earlier HELP synchronization, only the two full HELP payloads changed; all 114 other extracted payloads were identical. No new executable code was generated during synchronization. The exact approved images are the distribution authority.

## Approved Sockmaster dual-CPU score baseline

Page 5 displays independent measured 6809 and 6309 scores and their cached clock speeds, with no fixed-clock gate. SMBENCH reads the CPU name and MHz from the BOOT disk's cached SYSINFO.INF (not live CPU detection); after changing processor or clock, refresh the cache through the normal EDB startup path before benchmarking. The latest run updates only that CPU's pair; the other pair survives. Unmeasured CPU rows show --. The multiplier columns compare the most recently measured score to the historical 6809 bases 100 and 200. The historical 13,544-point result remains a documentation reference, not a substitute for a measured row.

SMBSCORE.DAT uses the SMBSCORE2 marker after the first successful new save, followed by last CPU index (0=6809, 1=6309), 6809 score, 6809 MHz, 6309 score, 6309 MHz, each on its own BASIC sequential-file record. A zero score/clock pair indicates unmeasured. The distributed legacy SMBSCORE15 record is preserved byte-for-byte; it has no CPU tag and must not be assigned to either CPU row. The viewer can still use its untagged score for the multiplier columns. The first successful benchmark migrates it without assigning its old value to a processor. SMBENCH reopens the new record and checks the CPU index and both score/clock pairs before continuing. A valid cache and a writable BENCH working disk are required. Back up score records; the overwrite is not transactional.

Approved dual-CPU candidate tests: direct 6809 at cached 125.28 MHz (13,194 points), then 6309 at 125.28 MHz (13,237), preserving the 6809 row, and 6309 at 101.12 MHz (10,596), preserving the earlier 6809 result. Full 6309 XMM suite and WIDTH 80 cyan-on-red restoration passed. Full 6809 suite regression and disk-error recovery remain untested. These are candidate test results, not scores seeded in the distributed image.

Only SMBENCH.BAS and XMSHOW.BAS changed relative to the immediately preceding BENCH baseline. Six free granules, original timing loop, the legacy distributed score file, all 43 other BENCH payloads, BOOT and TOOLS remain unchanged. No new runtime tests were performed by publication.

## Approved BENCH Color FIX11 (viewer) baseline

**Approved BENCH FIX11 viewer baseline (2026-11-28):** All 16 screen templates use adjacent yellow uppercase buttons on black. Hover flashes the label without inversion; the lowercase white x is steady over buttons and blinks elsewhere. The FIX9 fractional timer targets 90% of FIX6 frequency; FIX10 cursor behavior is retained. FIX11 renders PASS, results, values and scores green, and separators white. FAIL is not a PASS indicator. The live legacy benchmark/test console still uses monochrome 32-column text: applying green PASS and values there is outstanding. Cached SYSINFO.INF CPU identity and score formats are preserved; the successful benchmark continuation fixes are included. Menu/hover/navigation and viewer behavior were exercised in VCC-EDB during candidate testing; the full scoring suite has not been rerun on FIX11. The exact approved 184,320-byte image has 45 active files, six free granules and 22 changed payloads relative to the prior repository BENCH; 23 unchanged payloads, BOOT and TOOLS are preserved.

- FIX11 BENCH SHA-256: `747838009a90129a3f9f3d96b2e28def533f7c0a8c63020c162edad36125b385`
- FIX11 BENCH Git blob SHA: `58085192077f6bebc38b41b171d7d63a9f2a2f31`
- [Current repository BENCH download](https://raw.githubusercontent.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/main/EDB_v15_512k_bench.dsk)
- FIX11 release attachment subsequently verified from GitHub metadata (asset 804796309).

## Approved BENCH FIX13 baseline

**Approved BENCH FIX13 baseline (2026-11-28):** Normal button labels and delimiters are yellow on black. During hover, only the label flashes white/black; angle-bracket delimiters stay yellow. The white lowercase x stays visible during hover and blinks elsewhere. The FIX9 fractional timing, green PASS and score/value colors, white separators, cached CPU identification and benchmark handoff are preserved. Compared with FIX11, only 18 disk bytes in XHOVER.BIN changed; 44 other files and all 16 templates are identical. Static verification passed; FIX13 live testing and a full scoring regression remain outstanding. Live legacy-console multicolor rendering remains outstanding. The disk has 45 files and six free granules.

- Current BENCH SHA-256: `fcb67dd772c976720138c32746285d139cc95accdf060b322737df577e80de3e`
- Current BENCH Git blob SHA: `d78bbfe7d787e3ed5a5e08ec3acd7fa3e8d3c8d9`
- [Current repository BENCH download](https://raw.githubusercontent.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/main/EDB_v15_512k_bench.dsk)
- FIX13 release attachment and tag synchronization pending.
