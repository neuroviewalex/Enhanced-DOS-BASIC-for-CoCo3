# EDB v15 BASIC Program Reference - BENCH Disk

**Release synchronization status (2026-11-28):** BENCH FIX13 is the owner-approved authoritative repository baseline; its image and extracted payloads are synchronized. BOOT and TOOLS are unchanged. The v15 BENCH attachment is verified FIX11; use the current repository image until FIX13 attachment and tag synchronization. See [release synchronization status](RELEASE_SYNC.md).

**Coverage:** Eight BASIC programs in the verified 45-file extraction, with updated approved XMM behavior. Latest approved BENCH repository SHA-256 `fcb67dd772c976720138c32746285d139cc95accdf060b322737df577e80de3e`. See [manifest](../extracted/MANIFEST.json) for the exact current extraction.

## Complete BENCH file inventory

| Category | Files | Count |
| --- | --- | ---: |
| BASIC | HELP.BAS, XMM.BAS, XMENU.BAS, XMALL.BAS, XMBCPU.BAS, XBENCH.BAS, SMBENCH.BAS, XMSHOW.BAS | 8 |
| Screen templates | XMMMENU.X32, BENCH1–5.X32, XMMALL1–10.X32 | 16 |
| Native engines and UI | XMM6809.BIN, XMM6309.BIN, XHOVER.BIN, XKEY.DRV, HRTANDY.DRV, XMMHW.DRV, XMATH.DRV | 7 |
| Diagnostic modules | XTHW.DRV, XTALLOC.DRV, XTARENA.DRV, XTAPI.DRV, XTOBJ.DRV, XTGC.DRV, XTMATH.DRV, XTSIGN.DRV, XTPAGE.DRV | 9 |
| Data/configuration | XMSCORE.DAT, XBSCORE.DAT, XBREF.DAT, SMBSCORE.DAT, volume.inf | 5 |

## HELP.BAS - Integrated HELP copy

**HELP audit:** The owner-approved compact HELP.BAS on TOOLS and BENCH is byte-for-byte identical (10,812 bytes). It corrects EDIT, XMM, XBENCH and FIND wording, removes obsolete XMEM terminology, and recovers one granule per disk. The BOOT dispatcher is distinct. Targeted VCC-EDB tests passed on the 6809 and 6309, including WIDTH 32/40/80 on the 6309; not every HELP topic was exercised.

**Use:** Full topic-based EDB HELP reference, stored on BENCH as a convenience. The full HELP payload is identical on TOOLS and BENCH (Git blob afb82a867e4b36168a9c7b7b82634ae0cb29597f).

**Routines and behavior:** Main lines 10-60 parse the command tail; 70-240 search REM topic markers in the tokenized BASIC program and patch the dynamic jump line; 300 displays "No help for this topic"; 400-500 resolve the dispatch target. Each 10000-40100 topic block provides on-screen help.

**Reference:** See the [TOOLS HELP.BAS documentation](BASIC_PROGRAMS_TOOLS.md#helpbas---integrated-topic-reference) for the topic catalogue, corrected FIND wording, and dispatcher implementation.

**Note:** The separate BOOT `HELP.BAS` is only a dispatcher; it is not identical to this compact 10,812-byte HELP engine.

## XBENCH.BAS - Legacy XMEM/XMATH service benchmark

**Intended entry:** Second stage of RUN BENCHMARK TESTS (B), or the standalone command `XMM BENCH`. Direct invocation without the expected XMM history flags prints `Use XMM BENCH` and exits.

**Use:** Benchmark the legacy `XMMHW.DRV` and `XMATH.DRV` native service layer. It measures driver reload time, object create/free/statistics throughput, object reads/writes, signed vector and scalar math, and comparative BASIC-versus-XMATH dot products.

**Main phases:**

| Lines | Function |
| --- | --- |
| 1-115 | Check XMM entry state, screen mode and CPU identity, read `sysinfo.inf` clock estimate. |
| 120-170 | Adaptive timing of XMMHW/XMATH driver reload. |
| 180-350 | Initialize native services, create objects, time status/read/write and verify status. |
| 360-480 | Prepare test vectors and exercise DOT8, SUM8, SAD8, signed DOT8S, DOTQ7 operations. |
| 530-695 | Compare BASIC dot-product timing to native XMATH, verify status, release objects, check MMU register restoration. |

**Internal subroutines:**

| Lines | Purpose |
| --- | --- |
| 9000 | TIMER difference with wrap handling. |
| 9100 | Convert completed operations and ticks into throughput. |
| 9200-9270 | Initialize a math test, verify expected numeric result, adaptive timing and cycles/element reporting. |
| 9300 | Read the native 32-bit math result from `$62D8-$62DB`. |
| 57000-57260 | Resolve/load services and optional `sysinfo.inf`. |
| 58000 | Verify saved MMU PAR contents were restored. |
| 59000 | Paginated output with key release handling; automatic suite mode bypasses these pauses. |
| 61900 | Detect CPU type through a small embedded machine-code helper. |
| 62000-62390 | Maintain CPU-specific `XBSCORE.DAT` records; validate input magic, save, then read back and verify. |
| 63000-63900 | Guarded exit, BREAK/ESC handling and cleanup; successful suite mode hands off through XMM to Sockmaster. |

**Persistent files:** `XBSCORE.DAT` stores service benchmark measurements separately for Motorola 6809 and Hitachi 6309. The first record is `XBSCORE1`; invalid existing data is preserved rather than silently overwritten.

**Dependencies:** `XMMHW.DRV`, `XMATH.DRV`, `XKEY.DRV`, optional `sysinfo.inf` and native XMM routing state. Memory manager code, scratch addresses and MMU mappings are touched deliberately.

**Caution:** Performance is affected by emulator clock, CPU core, allocated memory and service-driver versions. Results should be compared only under controlled conditions. The score file is written on successful completion.

## XMBCPU.BAS - 6809 and 6309 native memory comparison

**Intended entry:** First stage of RUN BENCHMARK TESTS (B); use the menu to ensure the intended context.

**Use:** Select an appropriate CPU-specific native manager, benchmark memory operations, verify correctness and save separate results for Motorola 6809 and Hitachi 6309.

**CPU engines:** `XMM6809.BIN` for the 6809; `XMM6309.BIN` for a Hitachi 6309. The program probes CPU identity using embedded machine code, not only a displayed label; it also references the saved `sysinfo.inf` profile if available.

**Timed test sequence:**

| Phase | Source lines | Operation |
| --- | --- | --- |
| 1 | 190-260 | Fill a 16 KiB allocation repeatedly; compute KiB/s. |
| 2 | 270-380 | Sweep page mappings and verify sentinel bytes in all 64 physical pages. |
| 3 | 390-520 | Write/read a 256-byte buffer through the native paging API, then compare every byte. |
| 4 | 550-630 | Repeatedly allocate and free pages; compute pairs per second. |

Timing uses an adaptive number of repetitions aimed at roughly 30 timer ticks. It also measures clock frequency via a native routine and reports speed comparisons where a previous CPU record is available.

**Internal subroutines:**

| Lines | Purpose |
| --- | --- |
| 7000-7280 | Read prior `XMSCORE.DAT`, maintain separate CPU measurements, write updated results and compare both CPUs. |
| 7300-7360 | Reopen saved scores to verify numeric/clock fields after write. |
| 8200-8250 | Missing/invalid score file and I/O error recovery. |
| 8500-8540 | Standalone return path; successful suite mode advances to the services benchmark. |
| 8800-8914 | Native-test and CPU-profile failure cleanup, with NO SAVE. |
| 8930-8960 | Embedded native CPU/clock helper DATA. |
| 9000-9020 | TIMER wrap-aware elapsed tick calculation. |

**Score storage:** `XMSCORE.DAT` contains `XMMSCORE1`, five metrics per CPU and their measured MHz values. Missing scores can be created; invalid existing records are preserved.

**Safety:** A failed verification prints `NATIVE TEST FAILED - NOT SAVED`; the code attempts to free any live allocation and returns to the menu. These are real native memory tests, not merely arithmetic printouts.

**Interpretation:** Run the same benchmark on both CPU configurations to populate a meaningful comparison; until both have valid records, the program reports the comparison as pending.

## Approved XMM application template

XMM clears before each diagnostic and benchmark stage, including the first, and on button activation. System Info uses a six-TIMER-tick pause (approximately 100 ms at 60 Hz), outside measured benchmark intervals. For transitions, blank both screen buffers before changing video mode, suppress the palette while drawing, then reveal the completed screen. XMM temporarily uses WIDTH 32 but preserves the inherited width, palette (all 16 entries), border and text attributes across program chains and restores them on normal exit. All future EDB graphical applications must restore their inherited video environment, not a fixed default; reuse this template for ASKBENCH. Abnormal exit and full 6809 regression coverage remain outstanding.

## SMBENCH.BAS - Sockmaster Classic BASIC benchmark

Sockmaster's original 60-tick interpreted BASIC loop runs four times without printing or disk I/O inside the timed loop. `SMBENCH.BAS` calculates a rounded mean per 60 ticks, not the sum, and saves independent CPU score/clock pairs in `SMBSCORE.DAT` using the `SMBSCORE2` format after a successful run. At 60 TIMER ticks/sec each trial lasts one second; the benchmark interface displays only basic test/score information, not sample count or duration. In the full suite the viewer opens at page 1; press S or navigate to page 5. Direct aliases `XMM CLASSIC`, `XMM SOCK` and `XMM SOCKMASTER` launch just this test and open page 5 after successful saving.

Page 5 displays independent measured 6809 and 6309 scores and their cached clock speeds, with no fixed-clock gate. SMBENCH reads the CPU name and MHz from the BOOT disk's cached SYSINFO.INF (not live CPU detection); after changing processor or clock, refresh the cache through the normal EDB startup path before benchmarking. The latest run updates only that CPU's pair; the other pair survives. Unmeasured CPU rows show --. The multiplier columns compare the most recently measured score to the historical 6809 bases 100 and 200. The historical 13,544-point result remains a documentation reference, not a substitute for a measured row.

SMBSCORE.DAT uses the SMBSCORE2 marker after the first successful new save, followed by last CPU index (0=6809, 1=6309), 6809 score, 6809 MHz, 6309 score, 6309 MHz, each on its own BASIC sequential-file record. A zero score/clock pair indicates unmeasured. The distributed legacy SMBSCORE15 record is preserved byte-for-byte; it has no CPU tag and must not be assigned to either CPU row. The viewer can still use its untagged score for the multiplier columns. The first successful benchmark migrates it without assigning its old value to a processor. SMBENCH reopens the new record and checks the CPU index and both score/clock pairs before continuing. A valid cache and a writable BENCH working disk are required. Back up score records; the overwrite is not transactional.

| Lines | Function |
| --- | --- |
| 8–30 | Four timed samples and rounded mean |
| 40–63 | Read cached identity and existing record; update one CPU pair, save and read back both pairs |
| 79–90 | Suite success opens page 1; standalone success opens page 5 |
| 890, 900–901 | Invalid-cache or save/verification error and cleanup |
| 1000–1091 | Read cached CPU/MHz from BOOT SYSINFO.INF |
| 1100–1191 | Load and validate old/new score record; legacy migration |

See [Sockmaster benchmark documentation](SOCKMASTER_BENCH.md).

## XMM.BAS - XMM diagnostics controller

SHOW SYSTEM INFO checks hardware/MMU isolation, allocation, arenas, the callable API, object management, garbage collection, vector/math, signed/fixed-point arithmetic and native CPU-specific memory operations. The native-engine check runs before the numbered test chain; the signed tests are included in the math chain. Pager test 9 is excluded from this workflow; `XMM PAGE` and `XTPAGE.DRV` remain available separately. The diagnostic path verifies the expected history hooks, a compatible 512K profile and conflicting live allocations before sensitive operations. Save work first; do not run with incompatible memory managers active.

The ten XMMALL templates have only placeholders, not prefilled PASS or CPU results. The controller clears a runtime status block and the checks write outcomes. PASS means the corresponding check succeeded; FAIL means a reported failure; `--` means not confirmed/not reached. CPU identity, engine filename, engine-loaded status and post-free difference are populated at runtime. Early aborts or prerequisite failures can leave subsequent checks unconfirmed; an unconfirmed check is never a successful result.

The menu itself is XMENU.BAS. XMM.BAS retains the command-tail parser at 60000–60150, the prerequisites/engine selection at 61000–61680, and native cleanup at 62000-series routines. The native allocation/write/read/free test is at 7000–7091, with the 6309 fill/read check at 7200–7295. Lines 200–201 open XMENU; 430–440 initialize the runtime status block and launch the diagnostic chain/viewer; 450–461 dispatch the benchmark chain and handle an incomplete suite. The state markers at $78F8–$78FA coordinate the handoff; they are internal, not a public API.

Named commands retained: XMM HW, ALLOC, ARENA, API, OBJ, GC, MATH/MUL, SIGNED, PAGE, ALL, BENCH, STATUS, CLASSIC/SOCK/SOCKMASTER and ?. Prefix each argument with XMM. XMM ALL runs system info; XMM BENCH is services-only; normal B selection runs the full sequence. The compact HELP topics describe the current B/S/Q menu, viewer navigation, inherited display restoration, and XMM service names.

## XMENU.BAS - Mouse-driven main menu

Mount a writable copy of BENCH, select its drive, save any BASIC program in memory, and enter `XMM`. The full-color, mouse-driven main menu has exactly two test selections:

| Selection | Keyboard | Action |
| --- | --- | --- |
| RUN BENCHMARK TESTS | B | Runs CPU memory comparison, legacy services/vector/math timings and Sockmaster automatically; opens the five-page BENCH viewer at page 1. |
| SHOW SYSTEM INFO | S | Runs the native integrity checks and tests 1–8; opens the ten-page diagnostic viewer at page 1. |
| `<exit>` | Q | Leaves XMM and returns to the EDB prompt. |

Both viewers support mouse PREV/NEXT with wraparound, the centered `<exit>` button to return to the main menu, and keyboard N/P/Q. S jumps to page 5 in the benchmark viewer or page 1 in the system-information viewer. The white lowercase x cursor blinks outside buttons and remains continuously visible over a button while its label flashes white/black and its angle-bracket delimiters stay yellow; moving away restores steady yellow text and cursor blinking. The FIX9 fractional timer (90% of FIX6 frequency) and FIX10 cursor behavior are preserved. Position the pointer over a button before clicking; very fast movement and clicking together can select the previous sample. The UI renders native GIME 32-column attributes: yellow standard text and buttons, green PASS, measured values and scores, white separators and cursor, black background. No inverse hover. It restores the exact inherited display on normal exit. The original progress text is still used during tests; mouse polling and color rendering are not part of the timed loops.

Lines 10–14 initialize the keyboard/mouse/display and load XMMMENU.X32. Lines 20–25 dispatch B/S/Q. Lines 800–802 restore input/display state and return to EDB or chain to XMM. Lines 9000–9060 calibrate the mouse timing using the system clock profile; 9100–9164 sample the mouse, debounce selection and determine hover targets. XHOVER.BIN is the common renderer.

## XMALL.BAS - System information viewer

Reads the runtime diagnostic block at $5500 (guard signature $5560–$5561), not a saved result file. Lines 5000–5005 load the selected template and dispatch; 5100 fills the summary; 5200–5206 populate CPU, engine status and post-free difference; 5300–5513 convert status to PASS/FAIL/-- and overlay fields. Lines 700–782 implement ten-page navigation and 800–801 restore the display and return to XMM. The ten templates hold 54 status placeholders and four native metadata fields. No test result is prefilled.

## XMSHOW.BAS - Saved results viewer

The timed suite measures the **currently configured CPU only**; it does not switch CPUs. Run separately on each CPU with comparable clock, ROM and emulator settings to collect both columns. `XMSCORE.DAT` (XMMSCORE1) stores five native metrics and clock text per CPU; `XBSCORE.DAT` (XBSCORE1) stores 18 service/math values per CPU; `XBREF.DAT` supplies fallback service values. The viewer also has built-in CPU reference values at 125.28 MHz and can scale the missing CPU column to the measured clock. The 32-column templates do not mark every reference value individually: a populated column is not proof of a fresh measurement. Missing/unavailable values may appear as `--`. Keep the score records and test configuration with any published comparison. The three timed programs verify successful score writes before normal suite handoff; a failed suite must not be treated as a fresh complete result.

| Page | BENCH results | System information |
| ---: | --- | --- |
| 1 | CPU/native memory throughput | Overall diagnostic summary |
| 2 | Scalar services | Hardware / MMU |
| 3 | Vector speeds and BASIC/XMATH dot products | Allocator |
| 4 | Math acceleration and cycles per element | Arena |
| 5 | Sockmaster comparison | Callable API |
| 6 | — | Objects |
| 7 | — | Garbage collection |
| 8 | — | Math / vector |
| 9 | — | Signed / fixed-point |
| 10 | — | Native engine and post-free difference |

Lines 20–95 load CPU records; 2000–2643 load service/reference data, calculate fallback values and handle initial page selection; 5000–5600-series routines load templates and fill numeric fields; 16500–16595 read and validate legacy or CPU-tagged Sockmaster scores; 5530–5532 draw the per-CPU clock/score fields. Lines 700–801 provide navigation, cleanup and return. Page 5 uses the current template's selected historical comparisons, not all six historical ratios. See the Sockmaster notes for provenance limitations.

## Display and input architecture

The original native 723-byte X32 files contain a 480-byte screen payload (32 columns × 15 rows) and a native loader. BASIC loads the template and overlays only dynamic fields in the legacy screen buffer. XHOVER.BIN provides a compact 6809-compatible native GIME attribute renderer used by XMENU, XMALL and XMSHOW. It maps characters to native text mode, applies colors, handles the timer-based white/black label hover (yellow delimiters) and white x (steady over a button, blinking elsewhere), and restores the original display/palette on exit. HRTANDY.DRV handles high-resolution mouse sampling and XKEY.DRV provides keyboard input. The viewers share the same centered exit location and navigation behavior; moving button positions in a template also requires updating the associated mouse hitboxes.

## BENCH dependency overview

    XMM.BAS -> XMENU.BAS
      B -> XMBCPU.BAS -> XBENCH.BAS -> SMBENCH.BAS -> XMSHOW.BAS (5 pages)
      S -> native engine + XT*.DRV checks -> XMALL.BAS (10 pages)
      XMENU / XMSHOW / XMALL -> XKEY.DRV + HRTANDY.DRV + XHOVER.BIN + X32 templates
      Viewer EXIT -> XMM menu; menu EXIT -> EDB

## Scope and preservation

**Verification scope:** On the approved local candidates, VCC-EDB 6309 at 125.28 MHz successfully completed full XMM benchmark and System Info routes from WIDTH 80 with cyan/red colors, plus menu exits from WIDTH 40 (yellow/blue) and WIDTH 32 (green/black). Before/after visible RGB colors matched. The EDIT R3 local candidate passed bare EDIT, empty memory, named and numbered entry, missing-file preservation and LAST tracking; R2 also passed SAVE/NEW/LOAD/RUN and short tests at WIDTH 32/40/80. BREAK, long lines, disk-read failure, abnormal-exit recovery, and further 6809 regression testing are still outstanding. These are earlier candidate test results, not a new test of the uploaded release bytes.

The executable files and templates in [extracted/bench](../extracted/bench/) are exact tokenized/binary disk payloads. This is a BASIC and integration reference, not an instruction-by-instruction native driver disassembly.

**Sockmaster dual-CPU verification:** Approved dual-CPU candidate tests: direct 6809 at cached 125.28 MHz (13,194 points), then 6309 at 125.28 MHz (13,237), preserving the 6809 row, and 6309 at 101.12 MHz (10,596), preserving the earlier 6809 result. Full 6309 XMM suite and WIDTH 80 cyan-on-red restoration passed. Full 6809 suite regression and disk-error recovery remain untested. These are candidate test results, not scores seeded in the distributed image.


**Approved BENCH FIX13 baseline (2026-11-28):** Normal button labels and delimiters are yellow on black. During hover, only the label flashes white/black; angle-bracket delimiters stay yellow. The white lowercase x stays visible during hover and blinks elsewhere. The FIX9 fractional timing, green PASS and score/value colors, white separators, cached CPU identification and benchmark handoff are preserved. Compared with FIX11, only 18 disk bytes in XHOVER.BIN changed; 44 other files and all 16 templates are identical. Static verification passed; FIX13 live testing and a full scoring regression remain outstanding. Live legacy-console multicolor rendering remains outstanding. The disk has 45 files and six free granules.
