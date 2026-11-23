# Enhanced DOS BASIC (EDB) v15 - Official User Manual

**Platform:** Tandy Color Computer 3, 512K RAM  
**Manual status:** Living manual - comprehensive BASIC program reference added, 2026-11-22  
**Software baseline covered:** EDB v15 BOOT, user-promoted EDIT SHIFT navigation / SAVE correction / end-of-program FIX5.

This is the official, version-controlled EDB v15 user manual. It lives alongside the EDB source extracts and disk images so additions and corrections can be reviewed in GitHub history. This initial edition concentrates on loading, finding, editing, and saving BASIC programs. Other commands will be documented in subsequent editions; the absence of a command here does not mean EDB lacks it.

For the current software images, see the [repository README](../README.md) and [baseline history](../BASELINE_HISTORY.md). 

## Contents

1. [Getting started](#1-getting-started)
2. [The five-command programming workflow](#2-the-five-command-programming-workflow)
3. [LAST - filename history](#3-last---filename-history)
4. [LOAD - selecting a BASIC program](#4-load---selecting-a-basic-program)
5. [FIND - locating text](#5-find---locating-text)
6. [EDIT - changing program lines](#6-edit---changing-program-lines)
7. [SAVE - writing a BASIC program](#7-save---writing-a-basic-program)
8. [Worked examples](#8-worked-examples)
9. [TYPE - viewing disk files](#9-type---viewing-disk-files)
10. [Troubleshooting and data protection](#10-troubleshooting-and-data-protection)
11. [Related EDB commands](#11-related-edb-commands)
12. [Maintaining this manual](#12-maintaining-this-manual)
13. [Complete BASIC program and function reference](#13-complete-basic-program-and-function-reference)

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

## 2. The five-command programming workflow

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

## 3. LAST - filename history

### Syntax

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

### When to use LAST

Use LAST before an omitted-filename LOAD or SAVE to check which file EDB intends to use. If there is any doubt, use an explicit quoted filename instead.

## 4. LOAD - selecting a BASIC program

### Syntax

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

### After searching with FIND

To edit a matching line reported by FIND, first load the intended file:

```basic
LOAD "GAME.BAS"
EDIT 120
```

This makes it clear which file's contents you are changing.

## 5. FIND - locating text

### Syntax

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

### Omitting the filename

```basic
FIND "SCORE"
```

In the current v15 implementation, FIND obtains the **Last load** filename and uses it only when it ends in `.BAS`. It then searches **the corresponding saved disk file**, not the contents of BASIC RAM.

This is a key difference from the brief text in the existing `HELP FIND` screen, which describes the omitted-filename search as a loaded-program search. The underlying `FIND.BAS` and `TYPE.BAS` code is authoritative: the search is file-based.

### Why a saved copy matters

If you modify line 120 with EDIT but have not yet saved the program, searching the disk file will still return the previous saved text. SAVE before searching for changes you just made.

FIND runs its search through `TYPE.BAS`, preloading the source to a temporary `EDBSCAN.TMP` file. It needs a suitable, writable disk location and free space. It attempts to clean up the temporary file afterward.

**Do not assume FIND preserves an unsaved BASIC program in RAM.** Save valuable changes and LOAD the program again before using EDIT.

### Useful FIND messages

- `No matches.` - no matching text was found.
- `FIND: no loaded BASIC program` - the filename-free form could not identify a suitable Last load `.BAS` entry; this does not prove what is currently in RAM.
- `FIND: binary file` - the file was not interpreted as supported search text/BASIC.
- A preload/read error - check the filename, mounted disks, available space, and source/destination access.

## 6. EDIT - changing program lines

### Syntax

```basic
EDIT 120
EDIT
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

### Navigation without a line number

Bare `EDIT` enters the native editor's line-browsing mode. The v15 FIX5 baseline supports:

| Key | Action |
| --- | --- |
| SHIFT + Up arrow | Select the previous existing BASIC line. |
| SHIFT + Down arrow | Select the next existing BASIC line. |
| ENTER | Commit the current edit. |
| BREAK | Cancel the current edit. |

The editor moves through existing line numbers, not by adding 1 to the current number. For example, it can navigate through lines 100, 120, 200, and 350.

At the beginning and end of the program, navigation stops on the boundary line. The FIX5 correction prevents the program terminator from being misinterpreted as an enormous line number.

**Commit changes with ENTER before navigating to another line.** Navigating must not silently discard an unfinished change.

### What EDIT changes

EDIT updates the program held in memory; it does **not** save the file automatically. Once the changed program runs correctly, use SAVE to keep it.

The `EDIT filename` command shown in the built-in help is a separate filename-loading form. For the search/edit workflow in this manual, use `LOAD "filename"` followed by `EDIT line-number` or bare `EDIT`.

## 7. SAVE - writing a BASIC program

### Syntax

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

### Saving without a filename

The v15 filename-history support allows:

```basic
SAVE
```

EDB selects a recorded filename from its Next save / Last load state. Because the selected filename may not be the one you expect, first inspect `LAST` or supply a name explicitly.

### Overwriting an existing file

```basic
SAVE "GAME.BAS"
```

If `GAME.BAS` already exists, EDB's ordinary SAVE path can replace it. **This replacement is not transactional:** the old file may be deleted before the new write is complete. A disk-full condition or write error can destroy the previous version.

For important work, preserve the original:

```basic
SAVE "GAME2.BAS"
```

### Save-format correction in v15 FIX5

The user-promoted v15 FIX5 BOOT baseline restores `STX $0957` in `DOSCORE.DRV` before tokenized SAVE. This resets the BASIC file type and ASCII flags, preventing stale values from an earlier operation from being reused in a new directory entry.

This correction does **not** make overwrite atomic, and it does not remove the need to verify a saved program after reloading.

## 8. Worked examples

### A. Find, change, save, and verify a program

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

### B. Make several changes using line navigation

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

### C. Search again after saving

```basic
SAVE "GAME2.BAS"
FIND "SHIELD" "GAME2.BAS"
LOAD "GAME2.BAS"
EDIT 480
```

The line number 480 is illustrative. Use the number actually reported by FIND.

### D. Check filename history before saving

```basic
LAST
SAVE "TEST2.BAS"
LAST
```

Compare the history records to the filename you intended to use. Do not rely on filename-free SAVE when there is any risk of overwriting your source file.

## 9. TYPE - viewing disk files

The Tools disk also includes TYPE, a viewing utility often used alongside FIND:

```basic
TYPE "GAME.BAS"
```

TYPE can display supported text and BASIC files page by page. At its `-- more --` prompt, use **Q** to quit or another key to continue, as described by the built-in HELP text.

TYPE is for viewing; use EDIT to modify a loaded BASIC program. Like FIND, TYPE is a utility BASIC program, so do not treat running it as preserving unsaved program memory.

## 10. Troubleshooting and data protection

| Symptom | What to check |
| --- | --- |
| FIND reports a match, but EDIT opens the wrong contents | LOAD the intended `.BAS` file again after FIND, then EDIT the reported line number. |
| FIND cannot identify a loaded program | Inspect LAST, then supply an explicit filename to FIND. |
| FIND does not show recently edited text | The edits are unsaved; SAVE, then search the saved copy. |
| EDIT reports `line not found` | Check the line number and confirm the v15 FIX5 BOOT baseline is in use. |
| Editing works in RAM but the saved copy fails to run | Preserve the original, try a new destination filename, LOAD the saved copy, and inspect LIST before RUN. |
| SAVE over an existing file fails | The overwrite path is not failure-safe; use a disposable disk and retain backup copies. |
| Filename-free SAVE or LOAD targets the wrong file | Use LAST for context and supply the filename explicitly. |
| FIND fails during preload | Check the temporary-file disk, free space, filename, and write permissions. |

A safe habit for valuable programs is **save to a new name, reload, inspect, and run**. Do not overwrite your only working copy.

## 11. Related EDB commands

The full v15 environment has additional capabilities not yet covered in depth by this initial edition:

| Command | General purpose |
| --- | --- |
| `DIR` | List files and disk space. |
| `CD` / `JUMP` / `FLIP` | Navigate drives and disk images. |
| `HELP` | Consult the integrated command reference on the Tools disk. |
| `COMPARE` | Compare files. |
| `CHKDSK` | Check disk structures. |
| `DISKCOPY` / `INSTALL` | Disk/file copy and backup workflows. |
| `MEM` / `INFO` / `XMM` | Memory information and diagnostics. |
| `WIDTH` / `COLOR` / `KEYREP` | Screen and keyboard configuration. |

Future chapters should document these commands from their actual v15 sources, with tested syntax, examples, error cases, and limitations.

## 12. Maintaining this manual

The authoritative manual is this file: [`docs/USER_MANUAL.md`](USER_MANUAL.md), on the repository's `main` branch.

- Add or revise chapters in this file, preserving existing material unless the user approves a change.
- Verify command descriptions against the current extracted EDB implementation, built-in HELP, and promoted disk baseline.
- Where HELP text and code disagree, describe the actual observed/source-supported behavior and identify the discrepancy.
- Keep examples consistent with the current software baseline and distinguish static source analysis from emulator or hardware testing.
- Manual-only changes must not silently alter disk images, BASIC programs, or binary drivers.
- Record documentation changes through Git commits. Changes to the official EDB software baseline continue to require the user's explicit authorization.

**Source references for this edition:** `extracted/boot/LAST.BAS`, `EDIT.BAS`, `EDIT.DRV`, `DOSCORE.DRV`, `extracted/tools/FIND.BAS`, `TYPE.BAS`, `HELP.BAS`, and `BASELINE_HISTORY.md`.


## 13. Complete BASIC program and function reference

The current promoted v15 BOOT, TOOLS and BENCH disks include **45 `.BAS` directory entries** (26 BOOT, 14 TOOLS, 5 BENCH). Every entry has an individual source-audited reference section, including its role, command usage where applicable, important internal GOSUB routines, dependencies, side effects and cautions.

- **[Complete 45-program alphabetical/disk index](BASIC_PROGRAM_REFERENCE.md)** - every .BAS file, linked to its description and original extracted source.
- **[BOOT BASIC programs](BASIC_PROGRAMS_BOOT.md)** - startups, profiles, CD/autorun, editing, disk commands, upgrades and display routines.
- **[TOOLS BASIC programs](BASIC_PROGRAMS_TOOLS.md)** - HELP, FIND/TYPE, CHKDSK engines, guarded file copies, INSTALL and memory status.
- **[BENCH BASIC programs](BASIC_PROGRAMS_BENCH.md)** - XMM, native 6809/6309 benchmark controller, service benchmark and saved-results viewer.

The directory entry `*.BAS` is a literal BOOT file, not a wildcard. The three HELP.BAS entries are each accounted for (with the TOOLS and BENCH copies identical). Native .DRV and .BIN dependencies are identified but not individually disassembled in this BASIC-specific reference.

For new command features or software changes, the relevant program page and this manual should be updated together - with separate approval for any EDB code or disk-image changes.

---

*Enhanced DOS BASIC v15 - Official living user manual. This first edition covers program search, editing, and disk persistence; expansion is ongoing.*
