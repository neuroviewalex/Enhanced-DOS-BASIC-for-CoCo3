# Enhanced DOS BASIC for the Tandy Color Computer 3

**Release synchronization status (2026-11-27):** The owner-designated v15 release attachments are the authoritative disks. This documentation reflects the approved EDIT R3 and XMM Display Restoration R2 behavior. The repository disk images and extracted payloads still represent the previous snapshot; do not treat their hashes or source line maps as verified against the new release until re-extraction is complete. See [release synchronization status](docs/RELEASE_SYNC.md).

### The CoCo 3 BASIC environment, expanded into a capable DOS-style workspace

**Enhanced DOS BASIC (EDB) v15** is a comprehensive command, programming, disk-management, and diagnostics environment for the **Tandy Color Computer 3 with 512K RAM**. It builds on the familiar CoCo BASIC experience, adding native extensions, BASIC command utilities, flexible disk navigation, integrated help, editor improvements, file and disk maintenance, configurable startup profiles, and a native 512K memory management and benchmarking suite.

The project has roots dating to **1989**, with continued development in **2026**. The goal is straightforward: preserve the experience of programming and using a CoCo 3 while making it easier to develop software, organize projects, manage disks, configure the machine, and measure what it can do.

EDB is not simply a launcher or a handful of demonstration programs. Its **BOOT**, **TOOLS** and **BENCH** disks work together through tokenized BASIC programs, native `.DRV` and `.BIN` modules, system state, and persistent configuration files.

[**Official v15 User Manual**](docs/USER_MANUAL.md) | [**BASIC program and function reference**](docs/BASIC_PROGRAM_REFERENCE.md) | [**Download v15**](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/tag/v15)

## Project overview

| Area | Capabilities |
| --- | --- |
| **Command environment** | File, disk, display, startup, and system information commands accessible from BASIC |
| **BASIC development** | Native line editing, SHIFT + arrow navigation, LOAD/SAVE history, FIND and TYPE |
| **Disk management** | Drive/volume selection, filtered listings, 35/40-track checks, verified copies, backups and repair |
| **RAM-disk integration** | Cached drive support, physical/RAM routing, cache refresh and VCC-EDB playlist integration |
| **Personal configuration** | USER, ADMIN and STARTUP profiles, automatic launches, 32/40/80 columns, 64 named colours, key repeat |
| **Memory and diagnostics** | 512K XMM memory tools, memory maps, native test modules, CPU-specific 6809/6309 engines |
| **Benchmarks** | Automatic native CPU, services/vector/math and Sockmaster benchmarks; five-page full-color mouse viewer |
| **Documentation** | On-screen HELP, complete user handbook, per-program technical references and verified extracted source |

**Previous verified v15 core inventory (new release counts pending):** 54 BOOT, 17 TOOLS and 45 BENCH files — **116 files**, including **49 tokenized BASIC entries** (26 BOOT, 15 TOOLS, 8 BENCH).

## How EDB works

The environment brings together three kinds of functionality:

1. **Built-in BASIC operations**, including `LOAD`, `SAVE`, `LIST`, `RUN` and native disk functions.
2. **Native extensions and drivers** such as `DOSCORE.DRV`, `EDIT.DRV`, `RAMBOOT.DRV`, `CDSEQ.DRV`, `XKEY.DRV`, memory services, and CPU-specific native test engines.
3. **BASIC command programs** such as `CD.BAS`, `DIR.BAS`, `UPGRADE.BAS`, `FIND.BAS`, `CHKDSK.BAS`, `XMM.BAS`, and `SMBENCH.BAS`.

A command implemented by a BASIC utility can replace the program currently stored in BASIC memory. Save unsaved work before running one. Many utilities read their command tail from a shared location, and a trailing question mark can invoke the in-environment HELP service.

The CoCo's disk filesystem is still relevant. EDB uses directory entries and allocation chains, and the core image format represented here is **40 tracks x 18 sectors x 256 bytes**. EDB includes checkers for both 35-track and 40-track disks.

## Key features

### Reliable keyboard input

The November 26, 2026 owner-approved keyboard revision uses XMM/KEYPEEK-derived interrupt-protected eight-column PIA matrix scans, fresh physical key presses, stable release and input-buffer isolation. COLOR NAMES and COLOR CHART advance once per deliberate press/release. FORMAT requires a fresh Y confirmation; CD profile selection uses physical F1/F2 detection. TYPE retains Q-to-quit and clears residual input before returning. HELP COLOR delegates its wait to COLOR via the private NAMES! argument; the November 26 full HELP copies were identical. The BOOT HELP dispatcher, KEYPEEK SHIFT logic, EDIT, mouse routines, layouts and persistent KEYREP settings are unchanged. The owner confirmed testing of that earlier revision; the current release HELP copies require re-extraction.

### A more practical command prompt

Explore the system without writing a new BASIC utility for every task:

```text
VER
CPUID
DIR
CD TOOLS
PATH
LAST
HELP CD
```

`HELP` is an indexed, on-screen command reference. BOOT contains a small dispatcher that locates the complete HELP program on TOOLS or BENCH. Its topics include startup, drives, files, editing, memory, diagnostics, and companion utilities.

### Search, edit, save and resume BASIC programs

`EDIT` with no argument opens the first existing line in RAM; if no program is loaded, it reports `No program loaded.` and returns to the prompt. `EDIT filename` (for example, `EDIT VCC` or `EDIT VCC.BAS`) loads the BASIC listing, opens its first existing line, and leaves it in RAM for subsequent editing or SAVE. A missing filename reports failure without replacing the current listing. `EDIT n` edits the requested existing line. SHIFT + Up/Down browses existing line numbers; ENTER commits and exits. BREAK cancellation remains under investigation; do not rely on it to discard edits until verified. Save valuable unsaved work before loading another program.

The tools disk's `FIND` and `TYPE` programs support searching and viewing disk files. `LAST` shows the recorded Last load, Last run and Next save filenames. Together they form a convenient but important-to-understand workflow:

```basic
FIND "SCORE" "GAME.BAS"
LOAD "GAME.BAS"
EDIT 120
SAVE "GAME2.BAS"
LOAD "GAME2.BAS"
RUN
```

Here FIND reports matching line numbers in the **saved disk file**. EDIT changes the BASIC program **in RAM**. SAVE persists that change. Reloading the new file tests what was actually written.

**Important:** FIND does **not** scan unsaved changes in BASIC memory. It runs a file-scanning utility using `TYPE.BAS`; save work and reload the target program before editing it. The current native SAVE correction initializes tokenized file type/ASCII flags, but overwriting an existing program is not an atomic, failure-proof operation.

[**Complete BASIC editing chapter**](docs/USER_MANUAL.md#5-basic-programming-finding-and-editing)

### Navigate disks by number, volume label or emulator playlist

```text
CD ALL
CD TOOLS
CD 2
VOL
LABEL 2
DIR .BAS
JUMP 1
PATH
```

- **CD** switches drives by number or matches a name in the disk's `volume.inf`.
- **DIR** lists and filters directory entries and displays approximate free capacity.
- **VOL** reads a disk label and may create a placeholder for an unlabeled writable disk.
- **LABEL** writes a new volume name.
- **PATH** displays the effective lookup order across the current, cache, BOOT and other drives.
- **JUMP** switches a drive and can optionally run a program.
- **FLIP** manages supported physical/RAM-drive routing on compatible setups.

With the matching **VCC-EDB** emulator integration, `CD` can search a disk-image playlist exposed through drive 3 using `CDSEQ.DRV` / `CDINIT.DRV`. This is an extended emulator workflow, not a claim that an original stock drive controller implements playlists.

`AUTORUN` controls whether entering a disk through CD can launch an `autorun.inf` configuration. Use `AUTORUN OFF` when you want to explore a disk without launching its program.

### Back up, inspect and repair disks

| Command | What it does |
| --- | --- |
| `TYPE filename` | Display supported BASIC or text files, with pagination |
| `FIND "text" filename` | Case-insensitive file-content search |
| `COMPARE FILE1 TO FILE2` | Compare file lengths and bytes |
| `REN old TO new` | Copy, verify and then remove original filename |
| `DEL filename` | Delete a file using BASIC disk I/O |
| `DISKCOPY 0 TO 1` | Verified, guarded file-by-file copy |
| `DISKCOPY FULL 0 TO 1` | Copy a whole disk, subject to compatible geometry |
| `INSTALL` / `INSTALL BACKUP` | Stage and verify file installation / reverse backup |
| `CHKDSK 1` | Diagnose FAT allocation and directory problems |
| `CHKDSK 1 REPAIR` | Attempt repair on a backed-up disk |
| `T40` | Compatibility dispatcher for the geometry-aware disk check |
| `FORMAT 1` | Initialize disk filesystem metadata and volume label |

EDB's normal DISKCOPY and INSTALL workflows use temporary files, length and byte comparisons, overwrite prompts, and journal-based error recovery. These are valuable safeguards, **not guarantees of recovery after every interrupted write**.

CHKDSK distinguishes a **35-track / 68-granule** format from a **40-track / 78-granule** format. It reports chain loops, crosslinks, invalid links, lost granules and directory issues. The specialized 40-track FAT extension recovery operates only when it recognizes a specific expected layout.

**Safety:** `DISKCOPY FULL` overwrites the destination disk. `FORMAT` removes old filesystem allocations. `CHKDSK REPAIR`, `INSTALL` and `UPGRADE` can rewrite important data. Keep verified backups before attempting repairs or major changes.

### Customize startup, display and keyboard

```text
STARTUP
USER
ADMIN
USER LOGIN
AUTORUN
WIDTH 80
COLOR YELLOW ON BLACK
COLOR NAMES
COLOR CHART
KEYREP 20 .5
KEYREP BOOT
CURSOR
REBOOT
```

- **STARTUP**, **USER** and **ADMIN** manage startup profiles with username, width, colour and optional startup program.
- **USER LOGIN** and **ADMIN LOGIN** select a profile and reboot.
- **AUTORUN** can configure launches associated with individual disks.
- **WIDTH** selects 32-, 40-, or 80-column text.
- **COLOR** includes 64 named colours and a chart.
- **KEYREP** sets repeat rate and delay, with persistent BOOT defaults.
- **CURSOR** restores expected cursor behavior for the selected display mode.

Some setup changes reboot the system or clear current BASIC memory. Save unfinished work first.

### Install updates and refresh the 512K disk cache

```text
UPGRADE
UPGRADE CACHE
UPGRADE filename.ext:3
```

EDB's `UPGRADE.BAS` utility installs files from configured source drives, supports targeted file upgrades, and refreshes the cached drive through the native `RAMBOOT.DRV` path. The RAM cache depends on a consistent set of native and BASIC components; the v15 BOOT baseline includes cache-manifest fixes and the dependencies used for sequence / disk playlist operations.

**UPGRADE is a system-maintenance command.** A cache refresh can alter RAM-disk state, and a targeted/full upgrade can overwrite installed files. Do not mix random driver revisions or upgrade from an unverified disk.

### 512K memory management, CPU identity and native diagnostics

```text
MEM
MEM MAP
SYSMAP
XMM
XMM STATUS
XMM BENCH
```

- **MEM** displays BASIC workspace memory statistics; `MEM MAP` shows program, array and string workspace addresses.
- **SYSMAP** explains the 512K memory arrangement and the historical context of earlier CoCo configurations.
- **ID** and **CPUID** report cached startup CPU/system information from `sysinfo.inf`.
- **VCC** checks the expected VCC-EDB register signature.
- **XMM** manages the native memory diagnostic suite.

The XMM suite tests MMU isolation, allocation, arenas, API calls, objects, garbage collection, math, signed arithmetic and the native engine. Pager test 9 is available separately but excluded from SHOW SYSTEM INFO.

The test suite can exercise real MMU page mappings; it checks expected resident drivers and conflicting active allocation state before sensitive operations. Results depend on the configured processor, emulator, clock, native code, and BASIC interpreter. Use the tests as diagnostics and comparisons, not as absolute specifications.

### XMM — full-color diagnostics and benchmarks

XMM clears before each diagnostic and benchmark stage, including the first, and on button activation. System Info uses a six-TIMER-tick pause (approximately 100 ms at 60 Hz), outside measured benchmark intervals. For transitions, blank both screen buffers before changing video mode, suppress the palette while drawing, then reveal the completed screen. XMM temporarily uses WIDTH 32 but preserves the inherited width, palette (all 16 entries), border and text attributes across program chains and restores them on normal exit. All future EDB graphical applications must restore their inherited video environment, not a fixed default; reuse this template for ASKBENCH. Abnormal exit and full 6809 regression coverage remain outstanding.

Mount a writable copy of BENCH, select its drive, save any BASIC program in memory, and enter `XMM`. The full-color, mouse-driven main menu has exactly two test selections:

| Selection | Keyboard | Action |
| --- | --- | --- |
| RUN BENCHMARK TESTS | B | Runs CPU memory comparison, legacy services/vector/math timings and Sockmaster automatically; opens the five-page BENCH viewer at page 1. |
| SHOW SYSTEM INFO | S | Runs the native integrity checks and tests 1–8; opens the ten-page diagnostic viewer at page 1. |
| `<exit>` | Q | Leaves XMM and returns to the EDB prompt. |

Both viewers support mouse PREV/NEXT with wraparound, the centered `<exit>` button to return to the main menu, and keyboard N/P/Q. S jumps to page 5 in the benchmark viewer or page 1 in the system-information viewer. The mouse uses a blinking lowercase x, reveals the underlying character between blink phases, and inverts the hovered button (black on yellow). Position the pointer over a button before clicking; very fast movement and clicking together can select the previous sample. The UI renders native GIME 32-column color attributes: cyan headings, white labels, green PASS, red FAIL and blue buttons. It restores the exact inherited display on normal exit. The original progress text is still used during tests; mouse polling and color rendering are not part of the timed loops.

SHOW SYSTEM INFO checks hardware/MMU isolation, allocation, arenas, the callable API, object management, garbage collection, vector/math, signed/fixed-point arithmetic and native CPU-specific memory operations. The native-engine check runs before the numbered test chain; the signed tests are included in the math chain. Pager test 9 is excluded from this workflow; `XMM PAGE` and `XTPAGE.DRV` remain available separately. The diagnostic path verifies the expected history hooks, a compatible 512K profile and conflicting live allocations before sensitive operations. Save work first; do not run with incompatible memory managers active.

The ten XMMALL templates have only placeholders, not prefilled PASS or CPU results. The controller clears a runtime status block and the checks write outcomes. PASS means the corresponding check succeeded; FAIL means a reported failure; `--` means not confirmed/not reached. CPU identity, engine filename, engine-loaded status and post-free difference are populated at runtime. Early aborts or prerequisite failures can leave subsequent checks unconfirmed; an unconfirmed check is never a successful result.

The timed suite measures the **currently configured CPU only**; it does not switch CPUs. Run separately on each CPU with comparable clock, ROM and emulator settings to collect both columns. `XMSCORE.DAT` (XMMSCORE1) stores five native metrics and clock text per CPU; `XBSCORE.DAT` (XBSCORE1) stores 18 service/math values per CPU; `XBREF.DAT` supplies fallback service values. The viewer also has built-in CPU reference values at 125.28 MHz and can scale the missing CPU column to the measured clock. The 32-column templates do not mark every reference value individually: a populated column is not proof of a fresh measurement. Missing/unavailable values may appear as `--`. Keep the score records and test configuration with any published comparison. The three timed programs verify successful score writes before normal suite handoff; a failed suite must not be treated as a fresh complete result.

Sockmaster's original 60-tick interpreted BASIC loop runs four times without printing or disk I/O inside the timed loop. `SMBENCH.BAS` calculates a rounded mean per 60 ticks, not the sum, and preserves the `SMBSCORE.DAT` record format (`SMBSCORE15` is a compatibility marker, not the current number of trials). At 60 TIMER ticks/sec each trial lasts one second; the benchmark interface displays only basic test/score information, not sample count or duration. In the full suite the viewer opens at page 1; press S or navigate to page 5. Direct aliases `XMM CLASSIC`, `XMM SOCK` and `XMM SOCKMASTER` launch just this test and open page 5 after successful saving.

The current page 5 layout compares the saved score to the historical 6809 bases 100 (1 MHz) and 200 (2 MHz). It has separate 125.28 MHz point fields for 6809 and 6309. A fresh run with matching CPU/clock profile supplies the applicable field; the 6309 field otherwise retains the project author's historical EDB reference of 13,544. The saved Sockmaster record contains no CPU or MHz tag; it is not two independently persisted CPU scores. Do not attribute a previously saved score to a CPU without the run context. The full historical reference table remains in the documentation, not all on the current screen.

**Verification scope:** On the approved local candidates, VCC-EDB 6309 at 125.28 MHz successfully completed full XMM benchmark and System Info routes from WIDTH 80 with cyan/red colors, plus menu exits from WIDTH 40 (yellow/blue) and WIDTH 32 (green/black). Before/after visible RGB colors matched. The EDIT R3 local candidate passed bare EDIT, empty memory, named and numbered entry, missing-file preservation and LAST tracking; R2 also passed SAVE/NEW/LOAD/RUN and short tests at WIDTH 32/40/80. BREAK, long lines, disk-read failure, abnormal-exit recovery, and further 6809 regression testing are still outstanding. These are earlier candidate test results, not a new test of the uploaded release bytes.

See the [BENCH technical reference](docs/BASIC_PROGRAMS_BENCH.md), [user manual](docs/USER_MANUAL.md#9-xmm-diagnostics-and-benchmarking) and [Sockmaster benchmark notes](docs/SOCKMASTER_BENCH.md).

## Official v15 disk images

**The owner-designated [v15 Release attachments](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/tag/v15) are authoritative.** Each contains 184,320 bytes (40 tracks x 18 sectors x 256 bytes). Repository copies and extracted sources are awaiting exact binary synchronization.

| Disk | Files | Contents | Download |
| --- | ---: | --- | --- |
| **BOOT** | 54 (prior) | Core command environment, native editor, profiles, history and disk/cache drivers | [BOOT image](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_BOOT.dsk) |
| **TOOLS** | 17 (prior) | HELP, KEYPEEK, FIND/TYPE, disk checks, copy/install and file utilities | [TOOLS image](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_TOOLS.dsk) |
| **BENCH** | 45 (prior) | Full-color XMM menu, eight BASIC programs, 16 X32 templates, native diagnostics and timed benchmarks | [BENCH image](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_BENCH.dsk) |

**Authoritative release asset SHA-256 checksums (GitHub metadata):**

```text
EDB_v15_512k_boot.dsk
2869705a904eabafb1b9de541d0f265a8db4d6ace0851e0aad661e47b16e6175

EDB_v15_512k_tools.dsk
3afcb90370d9aff975be06ff1cdde0ce5aea89e7abb959c7324617cc4f1b196e

EDB_v15_512k_bench.dsk
15293d31bcc4a81e16f5298640fbf75c08d1f4c6ab04bf31e4824b57565b581a
```

**Distribution status:** The release digests above are verified from GitHub metadata. Local repository images and extracted payloads have not yet been synchronized against these exact assets.

The [`extracted/`](extracted/) tree contains 116 files from the previous verified snapshot. See [release synchronization status](docs/RELEASE_SYNC.md) before using the extracted code.

## Getting started with EDB v15

**Recommended for all features:** the [VCC-EDB emulator](https://github.com/neuroviewalex/VCC-EDB). The project previously identified [VCC-EDB v2.1.9.34](https://github.com/neuroviewalex/VCC-EDB/releases/tag/v2.1.9.34) as a compatible build; check its current documentation and releases for updates.

1. Configure a compatible VCC-EDB installation with 512K RAM and the EDB-compatible ROM/driver environment.
2. Download all three disks from the v15 Release.
3. Boot from BOOT. Mount TOOLS when using the full HELP and file utilities, and BENCH for XMM diagnostics/benchmark comparisons.
4. At EDB's prompt, explore:

```text
VER
CPUID
DIR
CD ALL
LAST
HELP
XMM
```

5. Open **XMM** and choose **RUN BENCHMARK TESTS** or **SHOW SYSTEM INFO**, or consult [Chapter 5 of the User Manual](docs/USER_MANUAL.md#5-basic-programming-finding-and-editing) for programming and editing examples.

**Physical CoCo 3:** The project is centered on a 512K Color Computer 3. Traditional disk/BASIC tasks can work with compatible real hardware. VCC-specific features - notably certain high-speed execution options, custom-ROM integrations and disk-image playlists - depend on the VCC-EDB environment rather than a stock machine. A VCC clock setting such as 125.28 MHz is an emulator configuration, not a stock 6809 clock rate.

## Repository structure and exact source extracts

```text
EDB_v15_512k_boot.dsk       Official BOOT disk
EDB_v15_512k_tools.dsk      Official TOOLS disk
EDB_v15_512k_bench.dsk      Official BENCH disk

extracted/
  boot/                     54 extracted BOOT files
  tools/                    17 extracted TOOLS files
  bench/                    45 extracted BENCH files
  MANIFEST.json             Hashes, disk geometry, file counts, integrity checks

docs/
  USER_MANUAL.md            Complete v15 user-facing handbook
  BASIC_PROGRAM_REFERENCE.md  BASIC program index and source links
  BASIC_PROGRAMS_BOOT.md    BOOT program functions and dependencies
  BASIC_PROGRAMS_TOOLS.md   TOOLS functions and maintenance utilities
  BASIC_PROGRAMS_BENCH.md   XMM, measurements, Sockmaster and viewer
  SOCKMASTER_BENCH.md       Classic loop, reference scores and comparison viewer

README.md                   This project introduction and current downloads
```

**The extracted `.BAS` files are genuine tokenized CoCo BASIC files**, not ordinary ASCII `.bas` listings. They are preserved byte-for-byte as stored on disk. Other `.DRV` and `.BIN` files contain native code and should not be confused with BASIC wrappers. The BOOT disk also contains a **literal filename `*.BAS`**, which serves a startup purpose and is not a wildcard instruction.

The source inventory and technical documents identify internal GOSUB routines, function groups, dependencies, and side effects. This makes it possible to learn how a command works, audit it, and maintain it without guessing from a command name alone.

## Documentation and technical references

- [**Complete EDB v15 User Manual**](docs/USER_MANUAL.md) - daily commands, configuration, programming, file management, XMM, examples and precautions.
- [**Complete BASIC program/function index**](docs/BASIC_PROGRAM_REFERENCE.md) - all **49** `.BAS` entries, with disk locations and links.
- [BOOT program reference](docs/BASIC_PROGRAMS_BOOT.md) - startup, drive/volume commands, editing, configuration, upgrade and cache functions.
- [TOOLS program reference](docs/BASIC_PROGRAMS_TOOLS.md) - HELP, FIND/TYPE, DISKCOPY, CHKDSK, INSTALL, MEM and related commands.
- [BENCH program reference](docs/BASIC_PROGRAMS_BENCH.md) - XMM, 6809/6309 native benchmarks, Sockmaster and comparison page details.
- [Sockmaster Classic BASIC](docs/SOCKMASTER_BENCH.md) - reference scores, EDB comparison, measured score format and viewer usage.
- [Extraction manifest](extracted/MANIFEST.json) - image sizes, granule allocation and exact-extraction verification.

The repository contains the **core BOOT / TOOLS / BENCH suite**. EDB also has separate related companion disks/projects for specialized editors, graphics, sound and development work; this three-disk core is not a catalog of every companion project.

## Preservation and development process

EDB development is managed around explicitly approved baselines. A new experiment does not automatically replace the official distribution.

The project protocol is:

1. Read and audit the current source and disk images first.
2. List proposed changes and their effects before implementation.
3. Obtain explicit permission.
4. Modify only the approved files and behaviors.
5. Verify every changed file against the originals, preserving unrelated files.
6. Promote a gold master or baseline **only after the project owner confirms it**.

Because EDB includes native code, tokenized BASIC and binary disk images, careful verification matters. Appropriate checks include BASIC token/linked-line structure, byte-for-byte source extraction, directory/FAT chain integrity, checksum comparisons, and clear separation of **static analysis** from **VCC-EDB / hardware runtime tests**.

The previous extraction is recorded in [MANIFEST.json](extracted/MANIFEST.json). The latest release assets remain untouched; this documentation-only update does not create a new executable baseline.

## The spirit of EDB

The Color Computer 3 remains a distinctive and enjoyable programming system. EDB's purpose is to let its users spend more time creating, experimenting and learning - and less time retyping utilities, juggling drive numbers, or losing track of a useful program.

**It's still BASIC. It's still the CoCo 3. It's a far more capable place to work.**
