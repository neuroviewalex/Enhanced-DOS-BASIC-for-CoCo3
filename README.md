# Enhanced DOS BASIC for the Tandy Color Computer 3

### The CoCo 3 BASIC environment, expanded into a capable DOS-style workspace

**Enhanced DOS BASIC (EDB) v15** is a comprehensive command, programming, disk-management, and diagnostics environment for the **Tandy Color Computer 3 with 512K RAM**. It builds on the familiar CoCo BASIC experience, adding native extensions, BASIC command utilities, flexible disk navigation, integrated help, editor improvements, file and disk maintenance, configurable startup profiles, and a native 512K memory management and benchmarking suite.

The project has roots dating to **1989**, with continued development in **2026**. The goal is straightforward: preserve the experience of programming and using a CoCo 3 while making it easier to develop software, organize projects, manage disks, configure the machine, and measure what it can do.

EDB is not simply a launcher or a handful of demonstration programs. Its **BOOT**, **TOOLS** and **BENCH** disks work together through tokenized BASIC programs, native `.DRV` and `.BIN` modules, system state, and persistent configuration files.

[**Official v15 User Manual**](docs/USER_MANUAL.md) | [**All 46 BASIC programs and functions**](docs/BASIC_PROGRAM_REFERENCE.md) | [**Baseline history**](BASELINE_HISTORY.md)

## Project overview

| Area | Capabilities |
| --- | --- |
| **Command environment** | File, disk, display, startup, and system information commands accessible from BASIC |
| **BASIC development** | Native line editing, SHIFT + arrow navigation, LOAD/SAVE history, FIND and TYPE |
| **Disk management** | Drive/volume selection, filtered listings, 35/40-track checks, verified copies, backups and repair |
| **RAM-disk integration** | Cached drive support, physical/RAM routing, cache refresh and VCC-EDB playlist integration |
| **Personal configuration** | USER, ADMIN and STARTUP profiles, automatic launches, 32/40/80 columns, 64 named colours, key repeat |
| **Memory and diagnostics** | 512K XMM memory tools, memory maps, native test modules, CPU-specific 6809/6309 engines |
| **Benchmarks** | Memory-service tests, CPU-native measurements and Sockmaster Classic BASIC comparison page |
| **Documentation** | On-screen HELP, complete user handbook, per-program technical references, verified extracted source and history |

**Current promoted v15 core:** 54 files on BOOT, 16 on TOOLS, and 24 on BENCH - **94 files**, including **46 tokenized BASIC program entries** (26 BOOT, 14 TOOLS, 6 BENCH).

## How EDB works

The environment brings together three kinds of functionality:

1. **Built-in BASIC operations**, including `LOAD`, `SAVE`, `LIST`, `RUN` and native disk functions.
2. **Native extensions and drivers** such as `DOSCORE.DRV`, `EDIT.DRV`, `RAMBOOT.DRV`, `CDSEQ.DRV`, `XKEY.DRV`, memory services, and CPU-specific native test engines.
3. **BASIC command programs** such as `CD.BAS`, `DIR.BAS`, `UPGRADE.BAS`, `FIND.BAS`, `CHKDSK.BAS`, `XMM.BAS`, and `SMBENCH.BAS`.

A command implemented by a BASIC utility can replace the program currently stored in BASIC memory. Save unsaved work before running one. Many utilities read their command tail from a shared location, and a trailing question mark can invoke the in-environment HELP service.

The CoCo's disk filesystem is still relevant. EDB uses directory entries and allocation chains, and the core image format represented here is **40 tracks x 18 sectors x 256 bytes**. EDB includes checkers for both 35-track and 40-track disks.

## Key features

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

The current BOOT baseline includes an improved native `EDIT.DRV`, with **bare EDIT** for browsing existing BASIC lines. **SHIFT + Up/Down** moves between real line numbers and respects the end-of-program boundary. `EDIT n` opens a chosen numbered line. Press **ENTER** to commit an edit or **BREAK** to cancel.

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

**UPGRADE is a system-maintenance command.** A cache refresh can alter RAM-disk state, and a targeted/full upgrade can overwrite installed files. Do not mix random driver revisions or upgrade from an unverified disk. The project's baseline history documents previous cache and refresh repairs.

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

XMM tests hardware behavior, page allocation, arenas, native API calls, object services, garbage collection, math, signed arithmetic and page mapping. The BENCH disk includes CPU-specific `XMM6809.BIN` and `XMM6309.BIN` engines, native `XT*.DRV` test modules, and separate measurement programs.

The test suite can exercise real MMU page mappings; it checks expected resident drivers and conflicting active allocation state before sensitive operations. Results depend on the configured processor, emulator, clock, native code, and BASIC interpreter. Use the tests as diagnostics and comparisons, not as absolute specifications.

### Performance comparisons - including Sockmaster Classic BASIC

**XMM's benchmark system** includes:

| Program | Purpose | Saved data |
| --- | --- | --- |
| `XBENCH.BAS` | Timings for legacy XMEM/XMATH services and vector arithmetic | `XBSCORE.DAT` |
| `XMBCPU.BAS` | Native 6809/6309 memory fill, mapping, I/O and allocation tests | `XMSCORE.DAT` |
| `XMSHOW.BAS` | Five pages of current, saved, measured and reference results | Reads the score/reference files |
| `SMBENCH.BAS` | One-second Sockmaster interpreted BASIC loop | `SMBSCORE.DAT` |

The **Sockmaster Classic BASIC** feature was explicitly promoted from FIX2 as part of the official v15 BENCH baseline. It keeps the original loop:

```basic
10 A=0:TIMER=0
20 IF TIMER<60 THEN A=A+1:GOTO20
30 PRINT A:RUN
```

The integrated version runs the timed portion **once** without repeated printing or restart, records its score, saves/verifies the result when the current drive is writable, and opens **XMSHOW page 5/5**. The original loop contains no disk I/O, so score reporting happens after the timed section.

**To run:** enter `XMM` and press **L - Classic**, or type `XMM CLASSIC`. In the viewer use **N/P** to change among five pages, **S** to jump to page 5 and **Q** to return to XMM. The original internal XMM S diagnostic remains preserved; the benchmark uses L.

| Historical Sockmaster reference | Score |
| --- | ---: |
| Motorola 6809 - 1 MHz | 100 |
| Hitachi 6309 native - 1 MHz | 114 |
| Motorola 6809 - 2 MHz | 200 |
| Hitachi 6309 native - 2 MHz | 228 |
| Motorola 6809 - doubled-clock accelerator | 268 |
| Hitachi 6309 native - doubled-clock accelerator | 275 |

**Separate EDB reference:** **13,544** from a Hitachi 6309 in native mode running EDB v15 at **125.28 MHz** on VCC-EDB with custom ROMs. That measurement was provided by the project author; it is neither an additional Sockmaster historical baseline nor a new result generated automatically by EDB.

The fifth page shows the current measured score, comparisons to all six historical references, and the comparison against the separate EDB reference. A missing saved score displays `--`. It measures **interpreted BASIC loop throughput**, not pure machine-code CPU speed.

[**Sockmaster benchmark documentation and FIX2 notes**](docs/SOCKMASTER_BENCH.md)

## Official v15 downloads

**For the latest user-promoted v15 images, download directly from this repository's `main` branch.** The three official disk images each contain 184,320 bytes (40 tracks x 18 sectors x 256 bytes).

| Disk | Files | Contents | Download |
| --- | ---: | --- | --- |
| **BOOT** | 54 | Core command environment, native editor, profiles, history and disk/cache drivers | [BOOT image](https://raw.githubusercontent.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/main/EDB_v15_512k_boot.dsk) |
| **TOOLS** | 16 | HELP, FIND/TYPE, disk checks, copy/install and file utilities | [TOOLS image](https://raw.githubusercontent.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/main/EDB_v15_512k_tools.dsk) |
| **BENCH** | 24 | XMM diagnostics, native benchmarks, XMSHOW page 5 and Sockmaster FIX2 | [BENCH image](https://raw.githubusercontent.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/main/EDB_v15_512k_bench.dsk) |

**SHA-256 checksums:**

```text
EDB_v15_512k_boot.dsk
974d15a700765469fdc4e8672b0f0d0ea5c5a5d0b2f038823c72c399d80d50f7

EDB_v15_512k_tools.dsk
4a2889cfc395f1536e78352041144a0a6463183fa71054985f3a1665f9c7a09b

EDB_v15_512k_bench.dsk
9ea442c53e9d73e0cc30f457818f28f937939e3d77021bce22df95744611e67a
```

**GitHub Release attachments:** The existing BOOT and BENCH binary attachments on the [v15 Release page](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/tag/v15) may predate the promoted images above. Publishing to `main` does not automatically replace Release assets. **Use the direct links and hashes above** until those release attachments are updated. The TOOLS baseline is unchanged.

The matching [`extracted/`](extracted/) tree includes all 94 files from the three current official disks. In particular, `extracted/bench/XMM.BAS`, `XMSHOW.BAS`, and the new `SMBENCH.BAS` correspond to the promoted BENCH image byte-for-byte.

## Getting started with EDB v15

**Recommended for all features:** the [VCC-EDB emulator](https://github.com/neuroviewalex/VCC-EDB). The project previously identified [VCC-EDB v2.1.9.34](https://github.com/neuroviewalex/VCC-EDB/releases/tag/v2.1.9.34) as a compatible build; check its current documentation and releases for updates.

1. Configure a compatible VCC-EDB installation with 512K RAM and the EDB-compatible ROM/driver environment.
2. Download the official BOOT, TOOLS and BENCH disk images using the repository links above.
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

5. Run **XMM → L** for Sockmaster Classic BASIC, or consult [Chapter 5 of the User Manual](docs/USER_MANUAL.md#5-basic-programming-finding-and-editing) for programming and editing examples.

**Physical CoCo 3:** The project is centered on a 512K Color Computer 3. Traditional disk/BASIC tasks can work with compatible real hardware. VCC-specific features - notably certain high-speed execution options, custom-ROM integrations and disk-image playlists - depend on the VCC-EDB environment rather than a stock machine. A VCC clock setting such as 125.28 MHz is an emulator configuration, not a stock 6809 clock rate.

## Repository structure and exact source extracts

```text
EDB_v15_512k_boot.dsk       Official BOOT disk
EDB_v15_512k_tools.dsk      Official TOOLS disk
EDB_v15_512k_bench.dsk      Official BENCH disk

extracted/
  boot/                     54 extracted BOOT files
  tools/                    16 extracted TOOLS files
  bench/                    24 extracted BENCH files
  MANIFEST.json             Hashes, disk geometry, file counts, integrity checks

docs/
  USER_MANUAL.md            Complete v15 user-facing handbook
  BASIC_PROGRAM_REFERENCE.md  All 46 BASIC entries, linked to the source
  BASIC_PROGRAMS_BOOT.md    BOOT program functions and dependencies
  BASIC_PROGRAMS_TOOLS.md   TOOLS functions and maintenance utilities
  BASIC_PROGRAMS_BENCH.md   XMM, measurements, Sockmaster and viewer
  SOCKMASTER_BENCH.md       Classic loop, historical references, FIX2 history

BASELINE_HISTORY.md         User-confirmed promoted baselines and checksums
README.md                   This project introduction and current downloads
```

**The extracted `.BAS` files are genuine tokenized CoCo BASIC files**, not ordinary ASCII `.bas` listings. They are preserved byte-for-byte as stored on disk. Other `.DRV` and `.BIN` files contain native code and should not be confused with BASIC wrappers. The BOOT disk also contains a **literal filename `*.BAS`**, which serves a startup purpose and is not a wildcard instruction.

The source inventory and technical documents identify internal GOSUB routines, function groups, dependencies, and side effects. This makes it possible to learn how a command works, audit it, and maintain it without guessing from a command name alone.

## Documentation and technical references

- [**Complete EDB v15 User Manual**](docs/USER_MANUAL.md) - daily commands, configuration, programming, file management, XMM, examples and precautions.
- [**Complete BASIC program/function index**](docs/BASIC_PROGRAM_REFERENCE.md) - all **46** `.BAS` entries, with disk locations and links.
- [BOOT program reference](docs/BASIC_PROGRAMS_BOOT.md) - startup, drive/volume commands, editing, configuration, upgrade and cache functions.
- [TOOLS program reference](docs/BASIC_PROGRAMS_TOOLS.md) - HELP, FIND/TYPE, DISKCOPY, CHKDSK, INSTALL, MEM and related commands.
- [BENCH program reference](docs/BASIC_PROGRAMS_BENCH.md) - XMM, 6809/6309 native benchmarks, Sockmaster and comparison page details.
- [Sockmaster Classic BASIC](docs/SOCKMASTER_BENCH.md) - historic baseline comparison, EDB reference score, data file format and FIX2 history.
- [Baseline history](BASELINE_HISTORY.md) - exact promoted releases, source changes, verification and checksum records.
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

The promoted Sockmaster FIX2 update changes only `XMM.BAS` and `XMSHOW.BAS` among the previous BENCH programs and adds `SMBENCH.BAS`. BOOT and TOOLS remain byte-for-byte unchanged. The corresponding extracted source and documentation are maintained together with the official image.

## The spirit of EDB

The Color Computer 3 remains a distinctive and enjoyable programming system. EDB's purpose is to let its users spend more time creating, experimenting and learning - and less time retyping utilities, juggling drive numbers, or losing track of a useful program.

**It's still BASIC. It's still the CoCo 3. It's a far more capable place to work.**
