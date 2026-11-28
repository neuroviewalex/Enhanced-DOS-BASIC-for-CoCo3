# Enhanced DOS BASIC (EDB) v15 - Official User Manual

**Release synchronization status (2026-11-27):** The owner-designated v15 release attachments, repository disk images and extracted payloads now match exactly. The source inventory is verified; the approved compact HELP passed targeted 6809/6309 VCC tests. Earlier candidate tests are not a full new system regression. See [release synchronization status](RELEASE_SYNC.md).

**Platform:** Tandy Color Computer 3 with 512K RAM  
**Edition:** Complete BASIC-program user handbook - 2026-11-27  
**Baseline:** The owner-designated v15 BOOT, TOOLS and BENCH release attachments are authoritative; repository and extracted source synchronization is verified.

**BENCH download:** [Official v15 Release image](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3/releases/download/v15/EDB_v15_512k_BENCH.dsk) (SHA-256 `0cf48fc3ce74c4d96bd13730eb57a126240ab34b6c1297c49f856918caeaaa5d`).

This is the **main, living EDB v15 handbook**. It explains the entire current BASIC utility environment - startup, volumes, program editing, files, backups, colour, keyboard, memory management, diagnostics and benchmarks - rather than only the original five-command programming workflow.

The authoritative text is versioned in GitHub alongside the verified source extractions. For installation and current downloads, see the [repository README](../README.md).



## Contents

1. [Getting started](#1-getting-started)
2. [Command map and conventions](#2-command-map-and-conventions)
3. [Booting and startup profiles](#3-booting-and-startup-profiles)
4. [Drives, volumes and directory navigation](#4-drives-volumes-and-directory-navigation)
5. [BASIC programming, finding and editing](#5-basic-programming-finding-and-editing)
6. [Files, disk maintenance and backups](#6-files-disk-maintenance-and-backups)
7. [Display and keyboard controls](#7-display-and-keyboard-controls)
8. [System identification and memory information](#8-system-identification-and-memory-information)
9. [XMM diagnostics and benchmarking](#9-xmm-diagnostics-and-benchmarking)
10. [Practical recipes](#10-practical-recipes)
11. [Troubleshooting and data protection](#11-troubleshooting-and-data-protection)
12. [BASIC program reference](#12-all-46-candidate-basic-program-entries)
13. [Technical notes and function reference](#13-technical-notes-and-function-reference)
14. [Maintaining this manual](#14-maintaining-this-manual)
15. [AI-assisted application development](#15-ai-assisted-application-development)


## 1. Getting started

EDB v15 is an enhanced BASIC and disk-command environment for the 512K CoCo 3. It can be used on compatible real hardware or with [VCC-EDB](https://github.com/neuroviewalex/VCC-EDB). Some EDB capabilities require the matching emulator.

The repository publishes three companion disk images:

| Image | Purpose |
| --- | --- |
| `EDB_v15_512k_boot.dsk` | Operating environment and native command extensions, including EDIT and filename history. |
| `EDB_v15_512k_tools.dsk` | HELP, FIND, TYPE, file-management and disk utilities. |
| `EDB_v15_512k_bench.dsk` | XMM benchmarks, diagnostics, and associated score data. |

Mount the appropriate disks and start EDB. Useful commands to explore include:

```basic
DIR
LAST
HELP
HELP FIND
HELP EDIT
```

The integrated `HELP` program resides on the Tools disk. Commands and filenames in examples are illustrative and should be adjusted to your disks.

**Important distinction:** A BASIC program in RAM is not the same thing as a copy saved on disk. Changes made with EDIT exist in memory until SAVE writes them to disk.

<a id="11-related-edb-commands"></a>

## 2. Command map and conventions

EDB combines **native BASIC statements**, **native machine-code extensions** and **BASIC utilities** stored as files. The distinction matters:

- **Native statements**, such as `LOAD`, `SAVE`, `RUN`, `COPY` and `DRIVE`, are understood by the BASIC environment directly.
- **Native extensions**, such as the current line-editing functionality in `EDIT.DRV`, add operations without requiring a matching user BASIC program to stay in RAM.
- **Command utilities**, such as `DIR.BAS`, `CD.BAS`, `FIND.BAS` and `XMM.BAS`, are BASIC programs invoked by EDB's command environment. Running one can replace whatever BASIC program you had loaded.

**Save important work before invoking a utility BASIC program.** A successful `RUN` from memory does not prove that a disk copy is current.

Most user commands accept a trailing question mark for their built-in help. The more extensive `HELP` database is on TOOLS (and also on BENCH). The BOOT `HELP.BAS` finds that database when available.

### Quick command directory

| Area | Commands and utilities |
| --- | --- |
| Start, log in, configure | `*` (boot stub), `DOS`, `STARTUP`, `USER`, `ADMIN`, `AUTORUN`, `REBOOT`, `UPGRADE` |
| Disks and paths | `CD`, `JUMP`, `FLIP`, `DIR`, `VOL`, `LABEL`, `PATH`, `DRIVE` |
| BASIC development | `LOAD`, `SAVE`, `RUN`, `LIST`, `LAST`, `FIND`, `EDIT`, `TYPE` |
| Files and backups | `DEL`, `REN`, `COMPARE`, `DISKCOPY`, `INSTALL`, `CHKDSK`, `T40`, `FORMAT`, `COPY`, `KILL`, `RENAME` |
| Screen and keyboard | `WIDTH`, `COLOR`, `CURSOR`, `KEYREP` |
| System information | `VER`, `ID`, `CPUID`, `VCC`, `MEM`, `MEM MAP`, `SYSMAP`, `HELP` |
| XMM and performance | `XMM` (full suite or system info), `XMM ALL`, `XMM BENCH` (services only), `XMM CLASSIC` (Sockmaster only) |

Only use examples on an appropriately mounted drive. A colon and drive number, such as `"GAME.BAS:1"`, explicitly addresses a disk drive in compatible BASIC file commands.

### Where a command lives

The BOOT disk is the startup environment. TOOLS provides HELP, disk utilities, FIND/TYPE and supporting commands. BENCH contains XMM controller and CPU benchmark programs. Some commands dispatch to machine-code `.DRV` or `.BIN` programs, which are documented as dependencies in this manual.

**A warning for `*.BAS`:** This is a literal filename used for BOOT startup, not a request to run or edit every `.BAS` file.


## 3. Booting and startup profiles

### Boot startup - * and DOS

The BOOT disk contains the literal `*.BAS` startup stub. It checks the expected FD-50X-style disk environment, rejects incompatible CoCoSDC configurations, initializes palette and width, then starts `BOOT.DRV`.

The `DOS` command enters the native Enhanced DOS BASIC environment. Do not use `*.BAS` as a wildcard command. The supported system is a CoCo 3 with 512K RAM; VCC-EDB provides the enhanced emulator integrations described in the repository README.

### STARTUP - edit the active profile

```text
STARTUP
```

STARTUP edits the BOOT disk's `startup.inf` fields: username, `WIDTH` setting, `COLOR` setting and an optional program to run before the command prompt. It reads the current values, prompts for replacements and verifies the saved profile by reading it back. Unlike USER/ADMIN, it normally does **not** reboot immediately.

Example configuration values:

```text
Username: Guest
Width: WIDTH 80
Color: COLOR YELLOW ON BLACK
Program:
```

An empty answer usually preserves the shown username/width/color, while the program field can be cleared. The command refuses to run while the resident XEDIT signature is active.

### USER and ADMIN - profiles and login

```text
USER
USER LOGIN
ADMIN
ADMIN LOGIN
```

`USER` edits `user.inf`; `ADMIN` edits `admin.inf`. Each stores a four-field profile and updates `startup.inf`, then invokes REBOOT. The `LOGIN` forms select the matching stored profile as active and restart without opening the full editor.

`CD.BAS` also contains a boot profile selector, with USER and ADMIN pathways. Changes to an active profile affect startup behavior, not just the appearance of the current screen.

### AUTORUN - disk-specific startup action

```text
AUTORUN
AUTORUN ON
AUTORUN OFF
AUTORUN 1
```

No argument displays current autorun status. ON/OFF updates the global launch flag. An explicit drive number from 0 to 3 edits that disk's `autorun.inf`, supplying an application name, width, colour and optional program to launch when `CD` selects that disk.

The BOOT drive cannot be configured with this edit mode. **When AUTORUN is enabled, a subsequent CD can start another program.** Use `AUTORUN OFF` before disk exploration when you do not want automatic launches.

### REBOOT - restart the system

```text
REBOOT
```

Restores a standard startup display state and invokes the native reboot entry point. Any BASIC program edits not saved first are lost.

### UPGRADE - installation and cache refreshing

```text
UPGRADE
UPGRADE CACHE
UPGRADE EDIT.DRV:3
```

`UPGRADE` without arguments installs a set of files from the drive-3 source to BOOT; `UPGRADE CACHE` requests a refresh of the RAM-backed drive-3 cache; a filename optionally qualified by source drive selects a targeted upgrade. The program calls `RAMBOOT.DRV` and includes a manifest-generation path. It protects disk-specific `volume.inf` from the single-file upgrade mode.

**Treat UPGRADE as a system-maintenance command, not a read-only refresh.** It may overwrite installed files and alter cache state. Make a backup before running it. The current cache/driver implementation is specific to this EDB baseline.

### HELP - on-disk documentation

```text
HELP
HELP CD
HELP XMM
HELP EDIT
```

The BOOT `HELP.BAS` searches mounted disks for a full HELP and XMM installation. The compact 10,812-byte HELP engine appears on TOOLS and BENCH. Use `HELP BOOT1`, `HELP BOOT2`, `HELP TOOLS1` and `HELP TOOLS2` for built-in indexes. If it cannot find a full HELP installation, BOOT displays mounting instructions.

The compact HELP now documents bare EDIT, filename loading, XMM and FIND consistently with the manual; see Chapter 5.


## 4. Drives, volumes and directory navigation

### CD - change drive or find a disk by name

```text
CD
CD 1
CD TOOLS
CD ALL
CD ..
```

`CD` selects drive 0 when no argument is supplied. Drives 0-3 can be selected numerically. A name such as `TOOLS` searches `volume.inf` labels case-insensitively, starting with visible drives. `CD ALL` lists mounted disk labels; period/slash forms can return to drive 0.

On compatible VCC-EDB versions, a miss among visible drives can trigger a search of drive 3's disk-image playlist via native `CDSEQ.DRV`. That extension is **not** a generic real-CoCo feature. `CD` also coordinates volume display, screen preferences, and optional AUTORUN launching.

### DIR - see files and free space

```text
DIR
DIR 2
DIR *.BAS
DIR .DRV
DIR GAME.BAS
DIR INFO
```

`DIR [0-3] [name|.ext|INFO]` lists disk directory entries, filters by filename or extension and reports file count and approximate free disk space. It formats output for 32-, 40- or 80-column screens.

The utility reads FAT and directory sectors directly. If a disk is missing `volume.inf`, its error recovery may create a default label file, so the listing is **not guaranteed read-only**. It concludes using `NEW`, so save a loaded BASIC program before running it.

### VOL and LABEL - display or change volume names

```text
VOL
VOL 2
LABEL
LABEL 2
```

`VOL` displays the name in `volume.inf` for the current or selected disk. If the label is absent and a disk is writable, it can create a `New disk` placeholder. `LABEL` prompts for and writes a new volume name. EDB volume names are **file-backed labels**, not media geometry.

Labels make `CD TOOLS` and other name-based navigation practical.

### PATH - see search order

```text
PATH
```

Displays the search priority: current drive, distinct RAM-cache drive, distinct boot drive, then other drives 0-3. PATH reports this order without modifying drive settings.

### JUMP - change drive and optionally run

```text
JUMP 2
JUMP 2 GAME.BAS
```

JUMP attempts drive selection, applies compatible RAM/physical routing where required, and either lists the destination directory or runs the named program. A supplied file replaces the active BASIC program. If it reports a skipped FLIP operation, verify the active drive rather than assuming a switch occurred.

### FLIP - RAM/physical drive routing

```text
FLIP
FLIP 3
FLIP 0
```

FLIP manipulates EDB's RAM-cache and physical-disk routing after checking expected 512K driver signatures, and then displays the resulting volume or hands control to CD.

**Current v15 caveat:** The `FLIP.BAS` source has an immediate branch that routes a requested `FLIP 2` to its "Drive 2 is physical" message before the later drive-2 toggle code. Do not rely on `FLIP 2` as an available toggle in this baseline without testing and a separately approved repair.

**Native DRIVE:** BASIC's `DRIVE n` directly chooses the default disk number (0-3); it does not search by volume name or playlist.


## 5. BASIC programming, finding and editing

These commands form one workflow for editing the current BASIC program. Read the filename-history rules carefully - `FIND` searches a disk file, while native `EDIT` changes RAM.

<a id="2-the-five-command-programming-workflow"></a>

### The five-command programming workflow

Five EDB commands form a useful programming workflow:

| Command | What it does |
| --- | --- |
| `LAST` | Displays the Last load, Last run, and Next save filename records. |
| `LOAD` | Loads a BASIC program from a disk file into memory. |
| `FIND` | Searches a disk file for text and reports matching BASIC line numbers. |
| `EDIT` | Edits or navigates the BASIC program in memory. |
| `SAVE` | Saves the program currently in memory to a disk file. |

A reliable search-and-edit sequence is:

```text
FIND  ->  LOAD  ->  EDIT  ->  SAVE  ->  LOAD  ->  RUN
```

The initial FIND step can be omitted if you already know which line needs editing. Using `LOAD` **after** FIND is intentional: the current FIND utility runs BASIC helper code and searches the disk file, so it should not be treated as an in-memory editor or assumed to preserve the previously loaded program.

<a id="3-last---filename-history"></a>

### LAST - filename history

#### Syntax

```basic
LAST
```

LAST reports EDB's filename history. Example output:

```text
Last load: GAME.BAS
Last run: GAME.BAS
Next save: GAME2.BAS
```

- **Last load** - the last recorded BASIC load filename.
- **Last run** - the last recorded program run filename.
- **Next save** - the filename EDB has prepared for a subsequent filename-free save.

These values are history records, **not** proof that the named file exists or that the program currently in RAM is identical to the saved file.

The native history storage is separate from the program text. In the v15 implementation, LAST displays the strings beginning at `$5EE0` (Last load), `$5EED` (Last run), and `$78DE` (Next save). These addresses are provided for technical reference, not as locations applications should modify.

#### When to use LAST

Use LAST before an omitted-filename LOAD or SAVE to check which file EDB intends to use. If there is any doubt, use an explicit quoted filename instead.

<a id="4-load---selecting-a-basic-program"></a>

### LOAD - selecting a BASIC program

#### Syntax

```basic
LOAD "filename"
LOAD
```

Examples:

```basic
LOAD "GAME.BAS"
LIST
RUN
```

A name without an extension defaults to the normal BASIC file extension where supported:

```basic
LOAD "GAME"
```

EDB v15 also provides filename-free `LOAD`. The command uses the available **Next save / Last load** history, rather than asking for a filename. Because those records can change during work, **explicit filenames are preferred for important programs**.

Loading a program replaces the BASIC program presently in memory. SAVE unsaved changes first if they matter.

#### After searching with FIND

To edit a matching line reported by FIND, first load the intended file:

```basic
LOAD "GAME.BAS"
EDIT 120
```

This makes it clear which file's contents you are changing.

<a id="5-find---locating-text"></a>

### FIND - locating text

#### Syntax

```basic
FIND "text" "filename"
FIND "text"
```

FIND is supplied on the Tools disk. It searches tokenized BASIC files or suitable text files and prints matching content, including BASIC line numbers when available.

For example:

```basic
FIND "SCORE" "GAME.BAS"
```

Illustrative results:

```text
120 SCORE=SCORE+100
450 PRINT "SCORE:";SCORE
730 IF SCORE>9999 THEN SCORE=9999
```

FIND's text matching is case-insensitive.

#### Omitting the filename

```basic
FIND "SCORE"
```

In the current v15 implementation, FIND obtains the **Last load** filename and uses it only when it ends in `.BAS`. It then searches **the corresponding saved disk file**, not the contents of BASIC RAM.

The corrected `HELP FIND` screen and underlying `FIND.BAS` / `TYPE.BAS` implementation agree: the search is file-based.

#### Why a saved copy matters

If you modify line 120 with EDIT but have not yet saved the program, searching the disk file will still return the previous saved text. SAVE before searching for changes you just made.

FIND runs its search through `TYPE.BAS`, preloading the source to a temporary `EDBSCAN.TMP` file. It needs a suitable, writable disk location and free space. It attempts to clean up the temporary file afterward.

**Do not assume FIND preserves an unsaved BASIC program in RAM.** Save valuable changes and LOAD the program again before using EDIT.

#### Useful FIND messages

- `No matches.` - no matching text was found.
- `FIND: no loaded BASIC program` - the filename-free form could not identify a suitable Last load `.BAS` entry; this does not prove what is currently in RAM.
- `FIND: binary file` - the file was not interpreted as supported search text/BASIC.
- A preload/read error - check the filename, mounted disks, available space, and source/destination access.

<a id="6-edit---changing-program-lines"></a>

### EDIT - changing program lines

#### Syntax

```basic
EDIT 120
EDIT
EDIT VCC
EDIT VCC.BAS
```

Use `EDIT 120` to edit an existing line 120 in the BASIC program currently in memory. The number is an example; use the number FIND reports.

```basic
EDIT 120
```

You might change:

```basic
120 SCORE=SCORE+100
```

to:

```basic
120 SCORE=SCORE+200
```

Press **ENTER** to commit the edited line to the program in RAM.

#### Navigation without a line number

Bare `EDIT` enters the native editor at the first existing line; empty memory returns to the prompt. The approved EDIT R3 behavior supports:

| Key | Action |
| --- | --- |
| SHIFT + Up arrow | Select the previous existing BASIC line. |
| SHIFT + Down arrow | Select the next existing BASIC line. |
| ENTER | Commit the current edit. |
| BREAK | Intended to cancel; reliability remains unverified. |

The editor moves through existing line numbers, not by adding 1 to the current number. For example, it can navigate through lines 100, 120, 200, and 350.

At the beginning and end of the program, navigation stops on the boundary line. The FIX5 correction prevents the program terminator from being misinterpreted as an enormous line number.

**Commit changes with ENTER before navigating to another line.** Navigating must not silently discard an unfinished change.

#### What EDIT changes

EDIT updates the program held in memory; it does **not** save the file automatically. Once the changed program runs correctly, use SAVE to keep it.

`EDIT` with no argument opens the first existing line in RAM; if no program is loaded, it reports `No program loaded.` and returns to the prompt. `EDIT filename` (for example, `EDIT VCC` or `EDIT VCC.BAS`) loads the BASIC listing, opens its first existing line, and leaves it in RAM for subsequent editing or SAVE. A missing filename reports failure without replacing the current listing. `EDIT n` edits the requested existing line. SHIFT + Up/Down browses existing line numbers; ENTER commits and exits. BREAK cancellation remains under investigation; do not rely on it to discard edits until verified. Save valuable unsaved work before loading another program.

<a id="7-save---writing-a-basic-program"></a>

### SAVE - writing a BASIC program

#### Syntax

```basic
SAVE "filename"
SAVE "filename",A
SAVE
```

Normal SAVE stores a **tokenized BASIC** program:

```basic
SAVE "GAME.BAS"
```

The `,A` option requests an ASCII-format save:

```basic
SAVE "GAME.BAS",A
```

For routine EDB BASIC development, prefer the normal tokenized format unless you specifically need a text-format copy.

#### Saving without a filename

The v15 filename-history support allows:

```basic
SAVE
```

EDB selects a recorded filename from its Next save / Last load state. Because the selected filename may not be the one you expect, first inspect `LAST` or supply a name explicitly.

#### Overwriting an existing file

```basic
SAVE "GAME.BAS"
```

If `GAME.BAS` already exists, EDB's ordinary SAVE path can replace it. **This replacement is not transactional:** the old file may be deleted before the new write is complete. A disk-full condition or write error can destroy the previous version.

For important work, preserve the original:

```basic
SAVE "GAME2.BAS"
```

#### Save-format correction in v15 FIX5

The user-promoted v15 FIX5 BOOT baseline restores `STX $0957` in `DOSCORE.DRV` before tokenized SAVE. This resets the BASIC file type and ASCII flags, preventing stale values from an earlier operation from being reused in a new directory entry.

This correction does **not** make overwrite atomic, and it does not remove the need to verify a saved program after reloading.

<a id="9-type---viewing-disk-files"></a>

### TYPE - viewing disk files

The Tools disk also includes TYPE, a viewing utility often used alongside FIND:

```basic
TYPE "GAME.BAS"
```

TYPE can display supported text and BASIC files page by page. At its `-- more --` prompt, use **Q** to quit or another key to continue, as described by the built-in HELP text.

TYPE is for viewing; use EDIT to modify a loaded BASIC program. Like FIND, TYPE is a utility BASIC program, so do not treat running it as preserving unsaved program memory.

## 6. Files, disk maintenance and backups

### DEL, KILL and REN - delete and rename

```text
DEL OLD.BAS
REN OLD.BAS TO NEW.BAS
```

`DEL` wraps BASIC's `KILL` and deletes the specified file on the active or explicitly addressed drive. **Deletion cannot be undone.**

`REN` implements a guarded rename: it copies the source file to the destination, opens both as random-record files, verifies length **and every byte**, and then deletes the original. It supports drive-qualified names. On verification failure it attempts to preserve the source. Keep backups when the destination may already exist.

BASIC's native `RENAME`, `KILL` and `COPY` statements are separate facilities; unlike the REN wrapper, their behavior does not automatically include the extra readback checks described above.

### COMPARE - inspect two files

```text
COMPARE GAME.BAS TO GAME2.BAS
```

Opens both as random-record files, reports the byte lengths, and compares each byte if lengths are equal. The result distinguishes identical files from different contents and differing lengths. No file contents are modified by the comparison routine.

### DISKCOPY - file backup or full disk image copy

```text
DISKCOPY 0 TO 1
DISKCOPY FULL 0 TO 1
```

**Normal mode** iterates the source directory and copies files using temporary staging, size/byte verification, a recovery journal and conditional overwrite prompts. It reserves names such as `EDBTEMP.TMP`, `EDBOLD.BAK`, and `EDBSWAP.JRN`. It requires sufficient temporary free space and directory slots.

**FULL mode** copies complete disk sectors, writing track 17 (FAT and directory) last. It requires matching 35-track or 40-track geometry and **overwrites the entire destination disk**.

For either mode, select source and destination carefully. Avoid deleting recovery journals by hand after an interrupted operation; inspect the destination first.

### INSTALL - protected file installation and backup

```text
INSTALL
INSTALL BACKUP
```

Moves files between the configured physical/RAM-cache environment in installation or reverse backup direction. It uses a staged copy, comparison, optional overwrite confirmation and journal-assisted rollback, similar to normal DISKCOPY.

It depends on the correct 512K FLIP driver/cache configuration and physical disk; it is not a general-purpose installer that can safely run on every emulation or hardware setup. Both forms write files.

### CHKDSK - examine disk allocation and integrity

```text
CHKDSK
CHKDSK 1
CHKDSK 1 REPAIR
```

CHKDSK determines whether the disk has a 35-track/68-granule or 40-track/78-granule layout and runs the matching worker program, `CHKDSK35.BAS` or `CHKDSK40.BAS`.

The check reports files, used/free granules, lost granules, crosslinks, broken chains, loops and invalid links. The **REPAIR** form can change FAT links, directory entries or file data sectors and then rescan to report what remains.

On the 40-track worker, a specialized FAT-extension recovery checks a known expected directory signature and refuses ambiguous layouts. It is not a universal disk-reconstruction algorithm.

**Recommended sequence:** Back up the disk image, run diagnostic `CHKDSK`, inspect the report, then use `CHKDSK ... REPAIR` only on a backed-up copy.

### T40 - compatibility diagnostic

```text
T40
```

T40 is a small dispatcher into CHKDSK, not a separate 40-track-only formatter or repair engine. CHKDSK still probes the disk geometry. It may clear the inherited command argument buffer before chaining to CHKDSK.

### FORMAT - initialize disk filesystem metadata

```text
FORMAT
FORMAT 2
```

Prompts for a target drive if omitted, warns that all disk data will be lost, and requires `Y` to continue. It overwrites the disk's FAT and directory allocation metadata and then creates a `volume.inf` label.

**Destructive:** It does not first make a backup or verify that the destination is disposable. This procedure is a filesystem initialization rather than proof of a physical low-level track format. Never use it on the only copy of a disk.

### Filesystem reference

CoCo disk files live in directory sectors and a granule allocation table. Ordinary EDB file operations still depend on sufficient free granules and correct directory metadata. On failure, **stop writing to the suspect disk** and preserve an image before attempting recovery.


## 7. Display and keyboard controls

### Keyboard handling (November 26 baseline)

The November 26, 2026 owner-approved keyboard revision uses XMM/KEYPEEK-derived interrupt-protected eight-column PIA matrix scans, fresh physical key presses, stable release and input-buffer isolation. COLOR NAMES and COLOR CHART advance once per deliberate press/release. FORMAT requires a fresh Y confirmation; CD profile selection uses physical F1/F2 detection. TYPE retains Q-to-quit and clears residual input before returning. HELP COLOR delegates its wait to COLOR via the private NAMES! argument; the November 26 full HELP copies were identical. The BOOT HELP dispatcher, KEYPEEK SHIFT logic, EDIT, mouse routines, layouts and persistent KEYREP settings are unchanged. The owner confirmed testing of that earlier keyboard revision. The owner-approved compact HELP.BAS on TOOLS and BENCH is byte-for-byte identical (10,812 bytes). It corrects EDIT, XMM, XBENCH and FIND wording, removes obsolete XMEM terminology, and recovers one granule per disk. The BOOT dispatcher is distinct. Targeted VCC-EDB tests passed on the 6809 and 6309, including WIDTH 32/40/80 on the 6309; not every HELP topic was exercised.

### WIDTH - text columns

```text
WIDTH 32
WIDTH 40
WIDTH 80
WIDTH
```

Selects 32-, 40- or 80-column text. With no argument, prompts for a width. The utility preserves palette/control registers during the switch.

**Caution:** The current `WIDTH.BAS` implementation ends with `NEW`, which clears the BASIC program in memory. SAVE anything important first. An active XEDIT resident mode blocks the width change.

### COLOR - named foreground/background colours

```text
COLOR
COLOR YELLOW ON BLACK
COLOR ON BLUE
COLOR NAMES
COLOR CHART
```

No arguments displays the current foreground and background. `COLOR fg ON bg` (or supported short forms) changes the palette; `COLOR NAMES` pages through all 64 named colours; `COLOR CHART` shows a graphical palette and restores the previous screen/palette after exit.

Common colour names have aliases such as `BLUE` meaning `BRIGHT-BLUE`. Use `COLOR NAMES` for the exact 64-name list instead of guessing spellings.

### CURSOR - restore standard cursor

```text
CURSOR
```

Restores cursor behavior appropriate for the current 32/40/80 display mode. It writes the associated screen/cursor machine-code bytes as necessary. This is not a cosmetic setting alone.

### KEYREP - keyboard repeat rate and delay

```text
KEYREP
KEYREP ON
KEYREP OFF
KEYREP 20 .5
KEYREP BOOT
```

No arguments shows current settings. ON sets approximately 20 repeats/second with 0.5 seconds initial delay; OFF maps to 1 repeat/second with 4 seconds delay. Numeric rates accept 1-60 repeats/sec, and delay accepts 0.1-4 seconds. `KEYREP BOOT` records the current values as BOOT defaults in `keyrep.inf`.

The program updates keyboard timing state directly and reports failure if it cannot save BOOT defaults.


## 8. System identification and memory information

### VER - EDB version

```text
VER
```

Displays the Enhanced DOS BASIC version using the current version marker, falling back to v15 if the marker is absent. It is a version display, not a hardware verification test.

### ID and CPUID - cached system profile

```text
ID
CPUID
```

`ID` reads the cached `sysinfo.inf` string and displays the system identification. `CPUID` routes to ID on the EDB cache drive. These report **boot-detected/cached** data, not a fresh processor probe.

### VCC - emulator identification signal

```text
VCC
```

Checks the expected VCC-EDB signature in several memory-mapped registers. A successful message indicates that particular expected signature was detected; it is not a generic emulator compatibility benchmark.

### MEM and MEM MAP - BASIC workspace

```text
MEM
MEM MAP
```

MEM displays BASIC workspace free, string reserve, string used/free, and total memory available to BASIC. `MEM MAP` displays the program, array, string and BASIC-top addresses read from interpreter pointers.

The utility uses `XKEY.DRV` for a hold-BREAK exit. Its memory display is informational, not a request to change the native MMU allocation.

### SYSMAP - overview of memory architecture

```text
SYSMAP
```

Prints a short comparison of the historical 128K CoCo architecture and the current 512K XMM arrangement, including 64 physical 8K banks and the XMM native-code region.

The printed 128K text is historical background, **not** a current feature restriction. SYSMAP is a static explanation rather than a full runtime bank scan.

### HELP - available topics

```text
HELP
HELP MEM
HELP SAVE
HELP TOOLS1
```

See Chapter 3 for finding the full HELP database. HELP uses topic tables within a BASIC program; its wording may occasionally lag an approved code fix. The official manual and detailed source reference document verified implementation differences.


## 9. XMM diagnostics and benchmarking

The BENCH disk contains 45 files, including eight BASIC programs and 16 X32 templates. It requires the compatible EDB 512K environment.

### XMM - diagnostics menu and controller

Mount a writable copy of BENCH, select its drive, save any BASIC program in memory, and enter `XMM`. The full-color, mouse-driven main menu has exactly two test selections:

| Selection | Keyboard | Action |
| --- | --- | --- |
| RUN BENCHMARK TESTS | B | Runs CPU memory comparison, legacy services/vector/math timings and Sockmaster automatically; opens the five-page BENCH viewer at page 1. |
| SHOW SYSTEM INFO | S | Runs the native integrity checks and tests 1–8; opens the ten-page diagnostic viewer at page 1. |
| `<exit>` | Q | Leaves XMM and returns to the EDB prompt. |

Both viewers support mouse PREV/NEXT with wraparound, the centered `<exit>` button to return to the main menu, and keyboard N/P/Q. S jumps to page 5 in the benchmark viewer or page 1 in the system-information viewer. The mouse uses a blinking lowercase x, reveals the underlying character between blink phases, and inverts the hovered button (black on yellow). Position the pointer over a button before clicking; very fast movement and clicking together can select the previous sample. The UI renders native GIME 32-column color attributes: cyan headings, white labels, green PASS, red FAIL and blue buttons. It restores the exact inherited display on normal exit. The original progress text is still used during tests; mouse polling and color rendering are not part of the timed loops.

XMM clears before each diagnostic and benchmark stage, including the first, and on button activation. System Info uses a six-TIMER-tick pause (approximately 100 ms at 60 Hz), outside measured benchmark intervals. For transitions, blank both screen buffers before changing video mode, suppress the palette while drawing, then reveal the completed screen. XMM temporarily uses WIDTH 32 but preserves the inherited width, palette (all 16 entries), border and text attributes across program chains and restores them on normal exit. All future EDB graphical applications must restore their inherited video environment, not a fixed default; reuse this template for ASKBENCH. Abnormal exit and full 6809 regression coverage remain outstanding.

### SHOW SYSTEM INFO

SHOW SYSTEM INFO checks hardware/MMU isolation, allocation, arenas, the callable API, object management, garbage collection, vector/math, signed/fixed-point arithmetic and native CPU-specific memory operations. The native-engine check runs before the numbered test chain; the signed tests are included in the math chain. Pager test 9 is excluded from this workflow; `XMM PAGE` and `XTPAGE.DRV` remain available separately. The diagnostic path verifies the expected history hooks, a compatible 512K profile and conflicting live allocations before sensitive operations. Save work first; do not run with incompatible memory managers active.

The ten XMMALL templates have only placeholders, not prefilled PASS or CPU results. The controller clears a runtime status block and the checks write outcomes. PASS means the corresponding check succeeded; FAIL means a reported failure; `--` means not confirmed/not reached. CPU identity, engine filename, engine-loaded status and post-free difference are populated at runtime. Early aborts or prerequisite failures can leave subsequent checks unconfirmed; an unconfirmed check is never a successful result.

### RUN BENCHMARK TESTS

The timed suite measures the **currently configured CPU only**; it does not switch CPUs. Run separately on each CPU with comparable clock, ROM and emulator settings to collect both columns. `XMSCORE.DAT` (XMMSCORE1) stores five native metrics and clock text per CPU; `XBSCORE.DAT` (XBSCORE1) stores 18 service/math values per CPU; `XBREF.DAT` supplies fallback service values. The viewer also has built-in CPU reference values at 125.28 MHz and can scale the missing CPU column to the measured clock. The 32-column templates do not mark every reference value individually: a populated column is not proof of a fresh measurement. Missing/unavailable values may appear as `--`. Keep the score records and test configuration with any published comparison. The three timed programs verify successful score writes before normal suite handoff; a failed suite must not be treated as a fresh complete result.

### XBENCH - XMM/XMATH services

Measures driver reload, object services, read/write throughput, DOT8, SUM8, SAD8, DOT8S, DOTQ7 and BASIC versus XMATH dot products. It checks results and MMU restoration. Direct `XMM BENCH` invokes only this legacy-services stage with its expected entry state, not the entire suite.

### XMBCPU - native 6809 versus 6309 comparison

First stage of the normal benchmark sequence. Selects XMM6809.BIN or XMM6309.BIN for the detected CPU, times memory fill, page sweep, buffered write/read and allocation/free, and validates data before saving. Save a copy of scores after each controlled run.

### XMSHOW - results browser

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

### Sockmaster Classic BASIC - benchmark and comparison

**Attribution:** Sockmaster, for the original three-line BASIC loop:

```basic
10 A=0:TIMER=0
20 IF TIMER<60 THEN A=A+1:GOTO20
30 PRINT A:RUN
```

Sockmaster's original 60-tick interpreted BASIC loop runs four times without printing or disk I/O inside the timed loop. `SMBENCH.BAS` calculates a rounded mean per 60 ticks, not the sum, and saves independent CPU score/clock pairs in `SMBSCORE.DAT` using the `SMBSCORE2` format after a successful run. At 60 TIMER ticks/sec each trial lasts one second; the benchmark interface displays only basic test/score information, not sample count or duration. In the full suite the viewer opens at page 1; press S or navigate to page 5. Direct aliases `XMM CLASSIC`, `XMM SOCK` and `XMM SOCKMASTER` launch just this test and open page 5 after successful saving.

Page 5 displays independent measured 6809 and 6309 scores and their cached clock speeds, with no fixed-clock gate. SMBENCH reads the CPU name and MHz from the BOOT disk's cached SYSINFO.INF (not live CPU detection); after changing processor or clock, refresh the cache through the normal EDB startup path before benchmarking. The latest run updates only that CPU's pair; the other pair survives. Unmeasured CPU rows show --. The multiplier columns compare the most recently measured score to the historical 6809 bases 100 and 200. The historical 13,544-point result remains a documentation reference, not a substitute for a measured row.

SMBSCORE.DAT uses the SMBSCORE2 marker after the first successful new save, followed by last CPU index (0=6809, 1=6309), 6809 score, 6809 MHz, 6309 score, 6309 MHz, each on its own BASIC sequential-file record. A zero score/clock pair indicates unmeasured. The distributed legacy SMBSCORE15 record is preserved byte-for-byte; it has no CPU tag and must not be assigned to either CPU row. The viewer can still use its untagged score for the multiplier columns. The first successful benchmark migrates it without assigning its old value to a processor. SMBENCH reopens the new record and checks the CPU index and both score/clock pairs before continuing. A valid cache and a writable BENCH working disk are required. Back up score records; the overwrite is not transactional.

| Historical Sockmaster configuration | Score |
| --- | ---: |
| 6809, 1 MHz | 100 |
| 6309 native, 1 MHz | 114 |
| 6809, 2 MHz | 200 |
| 6309 native, 2 MHz | 228 |
| 6809, doubled-clock accelerator | 268 |
| 6309 native, doubled-clock accelerator | 275 |

The separate 13,544 reference was reported by the project author on VCC-EDB with a native Hitachi 6309 at 125.28 MHz and custom ROMs. Higher Sockmaster scores mean higher interpreted BASIC loop throughput, not necessarily higher native instruction throughput.

### Advanced diagnostic commands

`XMM ALL` runs the system-information workflow. The source retains named individual commands `XMM HW`, `ALLOC`, `ARENA`, `API`, `OBJ`, `GC`, `MATH` / `MUL`, `SIGNED`, `PAGE` and `STATUS` (each prefixed with XMM). These are separate diagnostic paths, not extra menu buttons. `XMM ?` dispatches to HELP; the compact on-disk HELP describes the current interface.

### BENCH HELP.BAS

BENCH and TOOLS contain the full HELP engine; BOOT has the smaller dispatcher. The owner-approved compact HELP.BAS on TOOLS and BENCH is byte-for-byte identical (10,812 bytes). It corrects EDIT, XMM, XBENCH and FIND wording, removes obsolete XMEM terminology, and recovers one granule per disk. The BOOT dispatcher is distinct. Targeted VCC-EDB tests passed on the 6809 and 6309, including WIDTH 32/40/80 on the 6309; not every HELP topic was exercised. See [BENCH technical reference](BASIC_PROGRAMS_BENCH.md) for program internals and [Sockmaster notes](SOCKMASTER_BENCH.md) for measurement details.

**Verification scope:** On the approved local candidates, VCC-EDB 6309 at 125.28 MHz successfully completed full XMM benchmark and System Info routes from WIDTH 80 with cyan/red colors, plus menu exits from WIDTH 40 (yellow/blue) and WIDTH 32 (green/black). Before/after visible RGB colors matched. The EDIT R3 local candidate passed bare EDIT, empty memory, named and numbered entry, missing-file preservation and LAST tracking; R2 also passed SAVE/NEW/LOAD/RUN and short tests at WIDTH 32/40/80. BREAK, long lines, disk-read failure, abnormal-exit recovery, and further 6809 regression testing are still outstanding. These are earlier candidate test results, not a new test of the uploaded release bytes.

## 10. Practical recipes

### Explore EDB without changing a disk

```text
VER
CPUID
MEM
PATH
HELP TOOLS1
```

These primarily report state. If a utility program is required, save any BASIC program currently in RAM first. Unlike the commands above, `VOL` and `DIR` can initialize a missing `volume.inf` as part of their recovery behavior.

### Find a program by disk label

```text
CD ALL
CD TOOLS
DIR .BAS
HELP FIND
```

On supported VCC-EDB versions, CD can also search a configured drive-3 image playlist. With AUTORUN enabled, CD may launch a configured program; disable it first when exploring unknown disks.

### Find, edit, save and verify BASIC

```text
FIND "LASER" "GAME.BAS"
LOAD "GAME.BAS"
EDIT 350
SAVE "GAME2.BAS"
LOAD "GAME2.BAS"
LIST
RUN
```

The line number 350 is illustrative. Choose the line FIND actually reports. Because FIND searches a disk file through a utility program, LOAD it **again** before EDIT. The fresh LOAD after SAVE verifies the disk copy, not merely the in-memory program.

### Keep one original and a working copy

```text
LOAD "GAME.BAS"
EDIT
SAVE "GAME2.BAS"
LOAD "GAME2.BAS"
RUN
```

Use SHIFT + Up/Down in EDIT to browse existing line numbers and ENTER to commit and exit. BREAK cancellation remains unresolved. Do not overwrite your only known-good version.

### Check disk health before trying repairs

```text
CHKDSK 1
```

Review reported free/used granules, lost chains and crosslinks. Create a backup before any `REPAIR` action. A 40-track special-case recovery is intentionally conservative and does not apply to every disk.

### Back up a set of files versus a full disk

```text
DISKCOPY 0 TO 1
```

Copies files with staging/verification. By contrast:

```text
DISKCOPY FULL 0 TO 1
```

overwrites every sector on the destination disk. Double-check both drives before using FULL.

### Read existing benchmark scores

```text
XMM
```

Choose RUN BENCHMARK TESTS (B) to measure the current CPU and open the five-page viewer. Use S within that viewer for Sockmaster, or choose SHOW SYSTEM INFO from the main menu to run the diagnostic suite. The normal menu no longer has a V-only viewer option; navigation itself does not rerun tests.


<a id="8-worked-examples"></a>

### More worked examples

#### A. Find, change, save, and verify a program

You want to change the value awarded for scoring in `GAME.BAS`.

**1 - Search the disk file**

```basic
FIND "SCORE" "GAME.BAS"
```

Suppose FIND shows the statement on line 120.

**2 - Load the program**

```basic
LOAD "GAME.BAS"
```

**3 - Edit the matching line**

```basic
EDIT 120
```

Change the award and press ENTER to commit the line.

**4 - Test the in-memory program**

```basic
RUN
```

**5 - Save a separate copy**

```basic
SAVE "GAME2.BAS"
```

**6 - Reload the saved copy**

```basic
LOAD "GAME2.BAS"
LIST
RUN
```

If the reloaded copy behaves correctly, your edited file has passed a basic save-and-reload test.

#### B. Make several changes using line navigation

```basic
LOAD "GAME.BAS"
EDIT
```

Use SHIFT + Down and SHIFT + Up to move to nearby lines. Press ENTER to commit each changed line before navigating. Then:

```basic
SAVE "GAME2.BAS"
LOAD "GAME2.BAS"
RUN
```

#### C. Search again after saving

```basic
SAVE "GAME2.BAS"
FIND "SHIELD" "GAME2.BAS"
LOAD "GAME2.BAS"
EDIT 480
```

The line number 480 is illustrative. Use the number actually reported by FIND.

#### D. Check filename history before saving

```basic
LAST
SAVE "TEST2.BAS"
LAST
```

Compare the history records to the filename you intended to use. Do not rely on filename-free SAVE when there is any risk of overwriting your source file.

<a id="10-troubleshooting-and-data-protection"></a>

## 11. Troubleshooting and data protection

| Symptom | What to check |
| --- | --- |
| FIND reports a match, but EDIT opens the wrong contents | LOAD the intended `.BAS` file again after FIND, then EDIT the reported line number. |
| FIND cannot identify a loaded program | Inspect LAST, then supply an explicit filename to FIND. |
| FIND does not show recently edited text | The edits are unsaved; SAVE, then search the saved copy. |
| EDIT reports `line not found` | Check the line number and confirm the current EDIT R3 BOOT release is in use. |
| Editing works in RAM but the saved copy fails to run | Preserve the original, try a new destination filename, LOAD the saved copy, and inspect LIST before RUN. |
| SAVE over an existing file fails | The overwrite path is not failure-safe; use a disposable disk and retain backup copies. |
| Filename-free SAVE or LOAD targets the wrong file | Use LAST for context and supply the filename explicitly. |
| FIND fails during preload | Check the temporary-file disk, free space, filename, and write permissions. |

A safe habit for valuable programs is **save to a new name, reload, inspect, and run**. Do not overwrite your only working copy.


### Other common questions

| Situation | Recommended action |
| --- | --- |
| `CD TOOLS` cannot locate a volume | Use `CD ALL`, `DIR`, and `VOL`; check which drives or playlist are actually mounted. |
| A disk command unexpectedly launches a program | Inspect `AUTORUN` and the disk's autorun.inf; use `AUTORUN OFF` for manual navigation. |
| A loaded program disappears after WIDTH or DIR | Those BASIC utilities can end using `NEW` or replace the in-memory program. Save first. |
| `DISKCOPY` or `INSTALL` stops with swap files present | Preserve the image and its journal/temp files. Do not delete them until recovery state has been examined. |
| `CHKDSK` reports crosslinks or loops | Back up the disk before `REPAIR`; treat recovery as best effort. |
| `UPGRADE CACHE` fails or disk cache differs | Check the supported 512K routing and the promoted boot/cache driver versions. Do not mix unrelated driver revisions. |
| `FLIP 2` cannot select drive 2 | The current branch in FLIP.BAS makes the later drive-2 code unreachable; document or test a separately approved fix. |
| XMM reports busy or mismatched history hooks | Leave active native allocations intact; restore normal XMM environment or reboot after saving work. |
| A CPU comparison column seems too fast or unexpected | Inspect saved CPU and clock records; the viewer may use reference/fallback projections without a per-value source marker. |

The disk-maintenance commands have different risk profiles. `TYPE`, `COMPARE` and ordinary `CHKDSK` are analysis/view workflows, whereas `FORMAT`, `REPAIR`, `DISKCOPY FULL`, `UPGRADE` and `INSTALL` can deliberately write substantial data. Even a seemingly read-oriented utility can create a missing volume label or temporary scan file.


<a id="13-complete-basic-program-and-function-reference"></a>
<a id="12-all-45-basic-program-entries"></a>
<a id="12-all-46-candidate-basic-program-entries"></a>

## 12. BASIC program reference

The current disk images contain **26 BOOT + 15 TOOLS + 8 BENCH = 49** BASIC entries, including the literal `*.BAS` startup file. The TOOLS and BENCH HELP copies are identical; the BOOT dispatcher is distinct.

This table is included **inside the user manual** so every filename is discoverable here. Each link opens a source-audited entry with internal function/subroutine descriptions; the program behavior and syntax are explained in the relevant chapters above.

### BOOT - 26 programs

| File | Documentation | Direct source |
| --- | --- | --- |
| `*.BAS` | [Startup stub](BASIC_PROGRAMS_BOOT.md#bas---boot-entry-stub) | [File](../extracted/boot/*.BAS) |
| `ADMIN.BAS` | [Administrator profile](BASIC_PROGRAMS_BOOT.md#adminbas---administrator-profile) | [File](../extracted/boot/ADMIN.BAS) |
| `AUTORUN.BAS` | [Autorun state and profile](BASIC_PROGRAMS_BOOT.md#autorunbas---per-disk-autorun) | [File](../extracted/boot/AUTORUN.BAS) |
| `CD.BAS` | [Drive/volume and playlist navigation](BASIC_PROGRAMS_BOOT.md#cdbas---drive-and-volume-navigation) | [File](../extracted/boot/CD.BAS) |
| `COLOR.BAS` | [Foreground/background/palette](BASIC_PROGRAMS_BOOT.md#colorbas---text-colour-and-palette) | [File](../extracted/boot/COLOR.BAS) |
| `CPUID.BAS` | [Hardware-identity dispatcher](BASIC_PROGRAMS_BOOT.md#cpuidbas---hardware-identification) | [File](../extracted/boot/CPUID.BAS) |
| `CURSOR.BAS` | [Cursor restoration](BASIC_PROGRAMS_BOOT.md#cursorbas---cursor-restoration) | [File](../extracted/boot/CURSOR.BAS) |
| `DEL.BAS` | [Delete file](BASIC_PROGRAMS_BOOT.md#delbas---delete-a-file) | [File](../extracted/boot/DEL.BAS) |
| `DIR.BAS` | [Directory filters and free space](BASIC_PROGRAMS_BOOT.md#dirbas---directory-and-free-space) | [File](../extracted/boot/DIR.BAS) |
| `EDIT.BAS` | [Filename-based editor dispatcher](BASIC_PROGRAMS_BOOT.md#editbas---edit-filename-dispatcher) | [File](../extracted/boot/EDIT.BAS) |
| `FORMAT.BAS` | [Directory/FAT initialization](BASIC_PROGRAMS_BOOT.md#formatbas---initialize-a-disk-directory) | [File](../extracted/boot/FORMAT.BAS) |
| `HELP.BAS` | [Help dispatcher](BASIC_PROGRAMS_BOOT.md#helpbas---boot-help-dispatcher) | [File](../extracted/boot/HELP.BAS) |
| `ID.BAS` | [Cached system information](BASIC_PROGRAMS_BOOT.md#idbas---cached-system-information) | [File](../extracted/boot/ID.BAS) |
| `KEYREP.BAS` | [Key repeat settings](BASIC_PROGRAMS_BOOT.md#keyrepbas---keyboard-repeat) | [File](../extracted/boot/KEYREP.BAS) |
| `LABEL.BAS` | [Volume label editor](BASIC_PROGRAMS_BOOT.md#labelbas---change-volume-label) | [File](../extracted/boot/LABEL.BAS) |
| `LAST.BAS` | [File history](BASIC_PROGRAMS_BOOT.md#lastbas---filename-history) | [File](../extracted/boot/LAST.BAS) |
| `PATH.BAS` | [Disk search order](BASIC_PROGRAMS_BOOT.md#pathbas---drive-search-order) | [File](../extracted/boot/PATH.BAS) |
| `REBOOT.BAS` | [Native reboot](BASIC_PROGRAMS_BOOT.md#rebootbas---restart-edb) | [File](../extracted/boot/REBOOT.BAS) |
| `REN.BAS` | [Verified rename](BASIC_PROGRAMS_BOOT.md#renbas---verified-file-rename) | [File](../extracted/boot/REN.BAS) |
| `STARTUP.BAS` | [Startup profile](BASIC_PROGRAMS_BOOT.md#startupbas---active-startup-profile) | [File](../extracted/boot/STARTUP.BAS) |
| `UPGRADE.BAS` | [Install and cache refresh](BASIC_PROGRAMS_BOOT.md#upgradebas---install-and-refresh-cache) | [File](../extracted/boot/UPGRADE.BAS) |
| `USER.BAS` | [User profile](BASIC_PROGRAMS_BOOT.md#userbas---user-profile-and-login) | [File](../extracted/boot/USER.BAS) |
| `VCC.BAS` | [Emulator signature](BASIC_PROGRAMS_BOOT.md#vccbas---emulator-check) | [File](../extracted/boot/VCC.BAS) |
| `VER.BAS` | [EDB version](BASIC_PROGRAMS_BOOT.md#verbas---version-information) | [File](../extracted/boot/VER.BAS) |
| `VOL.BAS` | [Disk volume display](BASIC_PROGRAMS_BOOT.md#volbas---volume-name) | [File](../extracted/boot/VOL.BAS) |
| `WIDTH.BAS` | [32/40/80 text mode](BASIC_PROGRAMS_BOOT.md#widthbas---text-display-width) | [File](../extracted/boot/WIDTH.BAS) |

### TOOLS - 15 programs

| File | Documentation | Direct source |
| --- | --- | --- |
| `CHKDSK.BAS` | [Geometry dispatcher](BASIC_PROGRAMS_TOOLS.md#chkdskbas---geometry-aware-checker-dispatcher) | [File](../extracted/tools/CHKDSK.BAS) |
| `CHKDSK35.BAS` | [35-track engine](BASIC_PROGRAMS_TOOLS.md#chkdsk35bas---35-track-fat-audit-and-repair) | [File](../extracted/tools/CHKDSK35.BAS) |
| `CHKDSK40.BAS` | [40-track engine](BASIC_PROGRAMS_TOOLS.md#chkdsk40bas---40-track-fat-audit-and-repair) | [File](../extracted/tools/CHKDSK40.BAS) |
| `COMPARE.BAS` | [File comparison](BASIC_PROGRAMS_TOOLS.md#comparebas---byte-for-byte-file-comparison) | [File](../extracted/tools/COMPARE.BAS) |
| `DISKCOPY.BAS` | [Verified copy / FULL](BASIC_PROGRAMS_TOOLS.md#diskcopybas---verified-file-copy-or-full-disk-backup) | [File](../extracted/tools/DISKCOPY.BAS) |
| `FIND.BAS` | [FIND dispatcher](BASIC_PROGRAMS_TOOLS.md#findbas---find-dispatcher) | [File](../extracted/tools/FIND.BAS) |
| `FLIP.BAS` | [RAM and physical drive routing](BASIC_PROGRAMS_TOOLS.md#flipbas---ram-and-physical-drive-routing) | [File](../extracted/tools/FLIP.BAS) |
| `HELP.BAS` | [Full help engine](BASIC_PROGRAMS_TOOLS.md#helpbas---integrated-topic-reference) | [File](../extracted/tools/HELP.BAS) |
| `INSTALL.BAS` | [Guarded install/backup](BASIC_PROGRAMS_TOOLS.md#installbas---guarded-file-install-and-backup) | [File](../extracted/tools/INSTALL.BAS) |
| `JUMP.BAS` | [Drive/program navigation](BASIC_PROGRAMS_TOOLS.md#jumpbas---drive-navigation-with-optional-program) | [File](../extracted/tools/JUMP.BAS) |
| `KEYPEEK.BAS` | Keyboard diagnostic (tokenized source) | [File](../extracted/tools/KEYPEEK.BAS) |
| `MEM.BAS` | [Memory status/map](BASIC_PROGRAMS_TOOLS.md#membas---basic-memory-status-and-map) | [File](../extracted/tools/MEM.BAS) |
| `SYSMAP.BAS` | [Memory map explainer](BASIC_PROGRAMS_TOOLS.md#sysmapbas---legacy-and-512k-map-overview) | [File](../extracted/tools/SYSMAP.BAS) |
| `T40.BAS` | [Compatibility CHKDSK wrapper](BASIC_PROGRAMS_TOOLS.md#t40bas---geometry-checker-compatibility-wrapper) | [File](../extracted/tools/T40.BAS) |
| `TYPE.BAS` | [TYPE and FIND engine](BASIC_PROGRAMS_TOOLS.md#typebas---disk-file-viewer-and-find-engine) | [File](../extracted/tools/TYPE.BAS) |

### BENCH - 8 programs

| File | Documentation | Direct source |
| --- | --- | --- |
| `HELP.BAS` | [Duplicate full help engine](BASIC_PROGRAMS_BENCH.md#helpbas---integrated-help-copy) | [File](../extracted/bench/HELP.BAS) |
| `XBENCH.BAS` | [XMEM/XMATH service benchmark](BASIC_PROGRAMS_BENCH.md#xbenchbas---legacy-xmemxmath-service-benchmark) | [File](../extracted/bench/XBENCH.BAS) |
| `XMBCPU.BAS` | [6809 / 6309 native tests](BASIC_PROGRAMS_BENCH.md#xmbcpubas---6809-and-6309-native-memory-comparison) | [File](../extracted/bench/XMBCPU.BAS) |
| `SMBENCH.BAS` | [Sockmaster Classic BASIC](BASIC_PROGRAMS_BENCH.md#smbenchbas---sockmaster-classic-basic-benchmark) | [File](../extracted/bench/SMBENCH.BAS) |
| `XMM.BAS` | [Diagnostics controller](BASIC_PROGRAMS_BENCH.md#xmmbas---xmm-diagnostics-controller) | [File](../extracted/bench/XMM.BAS) |
| `XMSHOW.BAS` | [Saved benchmark viewer](BASIC_PROGRAMS_BENCH.md#xmshowbas---saved-results-viewer) | [File](../extracted/bench/XMSHOW.BAS) |
| `XMENU.BAS` | [Full-color main menu](BASIC_PROGRAMS_BENCH.md#xmenubas---mouse-driven-main-menu) | [File](../extracted/bench/XMENU.BAS) |
| `XMALL.BAS` | [System information viewer](BASIC_PROGRAMS_BENCH.md#xmallbas---system-information-viewer) | [File](../extracted/bench/XMALL.BAS) |


## 13. Technical notes and function reference

This manual is written for people using EDB. The [source-audited BASIC program reference](BASIC_PROGRAM_REFERENCE.md) complements it with internal BASIC function-group documentation, including GOSUB addresses, dependencies, native hooks and limits.

**Per-disk technical reference:**

- [BOOT - 26 BASIC entries](BASIC_PROGRAMS_BOOT.md) - startup, profiles, CD, file utilities, display and cache maintenance.
- [TOOLS - 15 BASIC entries](BASIC_PROGRAMS_TOOLS.md) - disk checkers, guarded copying, HELP, FIND/TYPE and routing.
- [BENCH - 8 BASIC entries](BASIC_PROGRAMS_BENCH.md) - XMM menu, 6809/6309 native benchmarks and result handling.

### How the commands communicate

Many EDB BASIC wrappers use the command text at `$FC80` and a 60000-series function to dispatch a trailing `?` request to HELP. `TYPE.BAS` detokenizes BASIC programs for display and powers FIND. `EDIT.BAS` finds/loads a BASIC file by name, while `EDIT.DRV` performs native line editing. `DOSCORE.DRV` extends native BASIC file operations and records relevant filename history.

### Native dependencies are separate programs

Some important routines are machine code, not `.BAS`:

- `BOOT.DRV`, `DOSCORE.DRV`, `EDIT.DRV`, `CDINIT.DRV`, `CDSEQ.DRV`, `RAMBOOT.DRV` - native boot, editing, disk and cache integration.
- `XKEY.DRV`, `HISTORY.DRV`, the `XT*.DRV` diagnostic modules and `XMM6809.BIN` / `XMM6309.BIN` - keyboard/history and native XMM tests.
- `XMMHW.DRV` and `XMATH.DRV` - the legacy service interfaces timed by XBENCH.

A complete instruction-level driver reference is outside the scope of a BASIC-program manual. Do not treat undocumented memory-mapped addresses as stable public APIs.

### Verification standard

The 49 BASIC entries are indexed above. The new BENCH descriptions reflect the synchronized disk source; this documentation edit is not an additional VCC-EDB or physical CoCo execution test.


<a id="12-maintaining-this-manual"></a>

## 14. Maintaining this manual

The authoritative manual is this file: [`docs/USER_MANUAL.md`](USER_MANUAL.md), on the repository's `main` branch.

- Add or revise chapters in this file, preserving existing material unless the user approves a change.
- Verify command descriptions against the current extracted EDB implementation, built-in HELP, and promoted disk baseline.
- Where HELP text and code disagree, describe the actual observed/source-supported behavior and identify the discrepancy.
- Keep examples consistent with the current software baseline and distinguish static source analysis from emulator or hardware testing.
- Manual-only changes must not silently alter disk images, BASIC programs, or binary drivers.
- Record documentation changes through Git commits. Changes to the official EDB software baseline continue to require the user's explicit authorization.

**Source references:** 46 existing program reference entries with documented dependencies; `KEYPEEK.BAS` is additionally available in `extracted/tools/`.


## 15. AI-assisted application development

EDB users can use an AI assistant such as ChatGPT to create BASIC applications **for Enhanced DOS BASIC v15**, while following the system's own programming conventions rather than relying on generic CoCo BASIC examples.

The companion file [`EDB_AI_PROGRAMMING_PROMPT.md`](EDB_AI_PROGRAMMING_PROMPT.md) is a ready-to-paste instruction set for ChatGPT. It is a **development aid**, not a new EDB command or a guarantee of executable code.

### What you need

- A working installation of **VCC-EDB** and its matching ROMs, or supported real CoCo 3 hardware.
- The **EDB v15** disk images that match your installed system, especially BOOT and TOOLS; BENCH is useful for relevant diagnostics.
- Access to the [official EDB repository](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3), particularly `docs/` and `extracted/`, or local copies of the corresponding reference materials.
- A ChatGPT conversation capable of reading the documentation, relevant source files, or uploaded disk images. Access varies by configuration; share files directly when needed.

### Get started

1. Open `EDB_AI_PROGRAMMING_PROMPT.md` and paste the **MASTER PROMPT** section into a new ChatGPT conversation.
2. Supply the official EDB source repository link and state which EDB/VCC-EDB/ROM versions you actually installed. Attach relevant source or disk files if the AI cannot access the repository or decode tokenized BASIC.
3. Describe your application and the target screen or hardware mode. For example: “Create a mouse-controlled BASIC application for EDB in WIDTH 80, using working EDB examples, and save it on a separate application disk.”
4. Review the AI's source references and proposed file changes. Approve modifications to existing files **before** they are made.
5. Run the program in VCC-EDB. If an error occurs, provide the exact `?SN BUG!`, `?DS BUG!`, `?OM BUG!`, or other message, the line number when shown, and the action that produced it.

### EDB-specific rules for AI-generated programs

- Use **the installed EDB baseline and its real examples as the authority**. Read the [BASIC program reference](BASIC_PROGRAM_REFERENCE.md) and the [BOOT](BASIC_PROGRAMS_BOOT.md), [TOOLS](BASIC_PROGRAMS_TOOLS.md), and [BENCH](BASIC_PROGRAMS_BENCH.md) guides before reimplementing existing functionality.
- Distinguish **native BASIC statements**, **native extensions**, and **BASIC command utilities**. A utility such as FIND or TYPE can replace the BASIC program currently in memory; it is not necessarily safe to invoke as a subroutine from an application.
- Reuse verified display, keyboard, mouse, file, disk, and native-driver patterns. Do not invent undocumented commands, memory addresses, or calling conventions.
- Save ordinary EDB `.BAS` programs in **tokenized BASIC format** unless an ASCII export is deliberately requested. Use `SAVE "NAME.BAS",A` only when an ASCII-format file is intended.
- Prefer **separate application disks**. Preserve the original BOOT, TOOLS, BENCH, ROM, emulator, and other official files.
- Never treat static code review as proof of execution. Actual VCC-EDB or hardware testing is required before claiming the program works.

### Preservation and verification

The AI should first inspect originals, list its proposed changes, obtain explicit approval, modify only approved material, and verify against the original files. It must not declare a new software baseline without the owner's explicit confirmation.

Generated code can still have errors. Keep working backup disk images; provide reproducible test results; identify whether behavior was **documented**, **source-checked**, or **runtime-tested**. Remember that EDB's ordinary SAVE overwrite is not transactional.

### Related references

- [AI development master prompt](EDB_AI_PROGRAMMING_PROMPT.md)
- [Complete BASIC program and function reference](BASIC_PROGRAM_REFERENCE.md)
- [EDB source repository](https://github.com/neuroviewalex/Enhanced-DOS-BASIC-for-CoCo3)
- [VCC-EDB emulator](https://github.com/neuroviewalex/VCC-EDB)

---

*Enhanced DOS BASIC v15 - Living user manual. Documents the full-color XMM diagnostic and benchmark suite and the EDB BASIC command environment.*

**Sockmaster dual-CPU verification:** Approved dual-CPU candidate tests: direct 6809 at cached 125.28 MHz (13,194 points), then 6309 at 125.28 MHz (13,237), preserving the 6809 row, and 6309 at 101.12 MHz (10,596), preserving the earlier 6809 result. Full 6309 XMM suite and WIDTH 80 cyan-on-red restoration passed. Full 6809 suite regression and disk-error recovery remain untested. These are candidate test results, not scores seeded in the distributed image.
