# EDB v15 BASIC Program Reference - BENCH Disk

**Coverage:** All 5 `.BAS` entries on the authoritative v15 BENCH disk.  
**Method:** Reviewed the tokenized BASIC source and the native files it calls.  
**Status:** Source-level reference; no new CPU benchmark or emulator run was performed in producing this documentation.  
**Links:** [Complete program index](BASIC_PROGRAM_REFERENCE.md) | [User manual](USER_MANUAL.md) | [BOOT](BASIC_PROGRAMS_BOOT.md) | [TOOLS](BASIC_PROGRAMS_TOOLS.md).

The BENCH disk contains the current XMM diagnostic and benchmark environment. Some native tests intentionally write and remap allocated memory pages; do not run them while other incompatible memory managers or active user data occupy the same facilities.

## Complete BENCH file inventory

| Program | Role | Main internal routines |
| --- | --- | --- |
| [HELP.BAS](#helpbas---integrated-help-copy) | Full HELP reference copied from TOOLS | Dynamic topic lookup and 10000-series help topics |
| [XBENCH.BAS](#xbenchbas---legacy-xmem-xmath-service-benchmark) | Benchmark legacy XMEM/XMATH services | 9000, 9100, 9200, 9300, 57000-62400, 63000 |
| [XMBCPU.BAS](#xmbcpubas---6809-and-6309-native-memory-comparison) | Benchmark and compare native CPU-specific memory manager paths | 7000-7350, 8500, 8800, 9000 |
| [XMM.BAS](#xmmbas---xmm-diagnostics-controller) | XMM menu and native test dispatcher | 7000, 61000, 61600, 62000 |
| [XMSHOW.BAS](#xmshowbas---saved-results-viewer) | Compare stored CPU and service results | 500, 600, 1500, 1600, 1700, 1710, 2000-2640 |

## HELP.BAS - Integrated HELP copy

**Use:** Full topic-based EDB HELP reference, stored on BENCH as a convenience. The file is **byte-identical** to `extracted/tools/HELP.BAS` in the promoted v15 baseline (Git blob `81662be3d31c4c15eeb3182a86cd8d3ea39b93eb`).

**Routines and behavior:** Main lines 10-60 parse the command tail; 70-240 search REM topic markers in the tokenized BASIC program and patch the dynamic jump line; 300 displays "No help for this topic"; 400-500 resolve the dispatch target. Each 10000-40100 topic block provides on-screen help.

**Reference:** See the [TOOLS HELP.BAS documentation](BASIC_PROGRAMS_TOOLS.md#helpbas---integrated-topic-reference) for the topic catalogue, known FIND wording discrepancy, and dispatcher implementation.

**Note:** The separate BOOT `HELP.BAS` is only a dispatcher; it is not identical to this 480-line HELP engine.

## XBENCH.BAS - Legacy XMEM/XMATH service benchmark

**Intended entry:** `XMM BENCH` or BENCH option B. Direct invocation without the expected XMM history flags prints `Use XMM BENCH` and exits.

**Use:** Benchmark the legacy `XMEMHW.DRV` and `XMATH.DRV` native service layer. It measures driver reload time, object create/free/statistics throughput, object reads/writes, signed vector and scalar math, and comparative BASIC-versus-XMATH dot products.

**Main phases:**

| Lines | Function |
| --- | --- |
| 1-115 | Check XMM entry state, screen mode and CPU identity, read `sysinfo.inf` clock estimate. |
| 120-170 | Adaptive timing of XMEMHW/XMATH driver reload. |
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
| 59000 | Paginated output with key release handling. |
| 61900 | Detect CPU type through a small embedded machine-code helper. |
| 62000-62390 | Maintain CPU-specific `XBSCORE.DAT` records; validate input magic, save, then read back and verify. |
| 63000-63900 | Guarded exit, BREAK/ESC handling, XKEY.DRV cleanup and return to XMM menu. |

**Persistent files:** `XBSCORE.DAT` stores service benchmark measurements separately for Motorola 6809 and Hitachi 6309. The first record is `XBSCORE1`; invalid existing data is preserved rather than silently overwritten.

**Dependencies:** `XMEMHW.DRV`, `XMATH.DRV`, `XKEY.DRV`, optional `sysinfo.inf` and native XMM routing state. Memory manager code, scratch addresses and MMU mappings are touched deliberately.

**Caution:** Performance is affected by emulator clock, CPU core, allocated memory and service-driver versions. Results should be compared only under controlled conditions. The score file is written on successful completion.

## XMBCPU.BAS - 6809 and 6309 native memory comparison

**Intended entry:** XMM menu option C (`XMM` then C). A fresh direct run can bypass preparatory menu context.

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
| 8500-8540 | Key prompt and return to XMM menu. |
| 8800-8914 | Native-test and CPU-profile failure cleanup, with NO SAVE. |
| 8930-8960 | Embedded native CPU/clock helper DATA. |
| 9000-9020 | TIMER wrap-aware elapsed tick calculation. |

**Score storage:** `XMSCORE.DAT` contains `XMMSCORE1`, five metrics per CPU and their measured MHz values. Missing scores can be created; invalid existing records are preserved.

**Safety:** A failed verification prints `NATIVE TEST FAILED - NOT SAVED`; the code attempts to free any live allocation and returns to the menu. These are real native memory tests, not merely arithmetic printouts.

**Interpretation:** Run the same benchmark on both CPU configurations to populate a meaningful comparison; until both have valid records, the program reports the comparison as pending.

## XMM.BAS - XMM diagnostics controller

**Syntax:** `XMM` opens the menu; supported arguments include `XMM HW`, `XMM ALLOC`, `XMM ARENA`, `XMM API`, `XMM OBJ`, `XMM GC`, `XMM MATH`/`MUL`, `XMM SIGNED`, `XMM PAGE`, `XMM ALL`, `XMM BENCH`, `XMM STATUS`, and `XMM ?`.

**Menu:**

| Key | Test/action | Dependency |
| --- | --- | --- |
| 1 | Hardware test | `XTHW.DRV` |
| 2 | Allocator test | `XTALLOC.DRV` |
| 3 | Arena test | `XTARENA.DRV` |
| 4 | API test | `XTAPI.DRV` |
| 5 | Object services | `XTOBJ.DRV` |
| 6 | Garbage collection | `XTGC.DRV` |
| 7 | Math | `XTMATH.DRV` |
| 8 | Signed arithmetic | `XTSIGN.DRV` |
| 9 | Page mapping | `XTPAGE.DRV` |
| A | Run all tests | Native/test-module sequence |
| B | Legacy-service benchmark | `XBENCH.BAS` |
| C | CPU comparison benchmark | `XMBCPU.BAS` |
| V | Saved result viewer | `XMSHOW.BAS` |
| N | Native manager test | CPU-specific XMM engine |

The menu also recognizes diagnostic letters P, Q, R, S, T and U for development; they are **not** part of the ordinary public workflow.

**Routines:**

| Lines | Purpose |
| --- | --- |
| 1-160 | Inherited-history state and argument-directed test routing. |
| 200-426 | Interactive menu, guarded keyboard polling and test dispatch. |
| 7000-7090 | Native manager initialize/allocate/write/read/free tests; verify buffer contents. |
| 7150-7190 | `- MORE -` keyboard pause. |
| 7200-7295 | Extra Hitachi 6309 page-fill and readback verification. |
| 8000-8050 | Hold BREAK/ESC exit and restoration of menu/keyboard state. |
| 60000-60150 | Parse command arguments and HELP. |
| 61000-61310 | Check expected history hooks, 512K hardware profile, and live service/allocation conflicts. |
| 61600-61680 | Select `XMM6809.BIN` or `XMM6309.BIN` based on CPU profile. |
| 62000-62900 | Restore `HISTORY.DRV` and report failures requiring reboot. |

**Dependencies:** `XKEY.DRV`, `HISTORY.DRV`, `sysinfo.inf`, native XMM6809/XMM6309 binaries, `XT*.DRV` test modules, XBENCH/XMBCPU/XMSHOW and XMM-specific memory signatures.

**Caution:** XMM operates on real native memory allocation and MMU mappings. The code checks for live pages, expected memory hook signatures and compatible 512K profile before significant operations. Never interpret the existence of an XMM option as authorization to disrupt a separate live manager.

## XMSHOW.BAS - Saved results viewer

**Intended entry:** V from the XMM diagnostics menu.

**Use:** Read and present up to four screens of saved CPU-native and XMEM/XMATH service benchmark results. Distinguishes measured values (**M**) from saved reference/fallback estimates (**R**) and missing entries.

**Navigation:** N = next page, P = previous page, Q = return to XMM menu. The source handles keyboard polling and key-release logic.

**Pages:**

| Page | Contents |
| --- | --- |
| 1 | CPU native memory metrics and reported MHz for 6809 versus 6309. |
| 2 | XMEM service reload, object/status, read/write throughput. |
| 3 | Math/vector operations and BASIC/XMATH dot rates. |
| 4 | Math/cycles and additional service statistics. |

**Internal routines:**

| Lines | Purpose |
| --- | --- |
| 20-95 | Read `XMSCORE.DAT`, handle absent/invalid data. |
| 500-640 | Format native CPU columns, measured clocks and ratios. |
| 700-800 | Keyboard/page navigation and return to XMM. |
| 1200-1430 | Render service benchmark pages 2-4. |
| 1500-1710 | Column headers, metric formatting and speedup ratios. |
| 2000-2110 | Read `XBSCORE.DAT`; handle missing values. |
| 2300-2420 | Load `XBREF.DAT` fallback data where measurements are missing. |
| 2500-2640 | Supply built-in native reference values and adjust a reference to the measured clock if possible. |
| 30000-31010 | Data labels and built-in reference records. |

**Persistent files:** `XMSCORE.DAT` (native CPU), `XBSCORE.DAT` (legacy services), `XBREF.DAT` (reference data). Source-level viewer code opens these for input and uses local arrays; it does not overwrite their score records.

**Caution:** Reference and clock-projected figures are not fresh measurements. Use actual saved measurements from each CPU when comparing hardware or emulator performance.

---

## BENCH dependency overview

    XMM.BAS
      | - XTHW / XTALLOC / XTARENA / XTAPI
      | - XTOBJ / XTGC / XTMATH / XTSIGN / XTPAGE
      | - XBENCH.BAS -> XMEMHW.DRV + XMATH.DRV -> XBSCORE.DAT
      | - XMBCPU.BAS -> XMM6809.BIN or XMM6309.BIN -> XMSCORE.DAT
      | - XMSHOW.BAS -> XMSCORE.DAT + XBSCORE.DAT + XBREF.DAT
      | - HELP.BAS (shared topic reference)

## Scope and preservation

This document covers **every BASIC file** in the five-file BENCH inventory. It does not claim to disassemble or document every native DRV/BIN instruction. For those programs, see the source dependencies listed above. The original BENCH scores and images were not regenerated, erased, or altered during this documentation audit.
