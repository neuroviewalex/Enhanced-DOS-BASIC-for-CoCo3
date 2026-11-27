# EDB v15 BASIC Program Reference - TOOLS Disk

**Coverage:** All 14 `.BAS` files on the promoted v15 TOOLS disk.  
**Method:** Source audit of the tokenized BASIC in `extracted/tools/`; internal numbered routines are listed by their entry lines.  
**Status:** Static source-level behavior, not a fresh VCC-EDB runtime certification.  
**Links:** [Full program index](BASIC_PROGRAM_REFERENCE.md) | [User manual](USER_MANUAL.md) | [BOOT](BASIC_PROGRAMS_BOOT.md) | [BENCH](BASIC_PROGRAMS_BENCH.md).

TOOLS includes a number of potentially destructive disk utilities. **CHKDSK without REPAIR is diagnostic; CHKDSK REPAIR and DISKCOPY FULL modify the target disk.** Keep backup images before running repair, copy or install commands.

## Complete TOOLS file inventory

| Program | Purpose | Main subroutines |
| --- | --- | --- |
| [CHKDSK.BAS](#chkdskbas---geometry-aware-checker-dispatcher) | Dispatch to 35/40-track checker | 9500 |
| [CHKDSK35.BAS](#chkdsk35bas---35-track-fat-audit-and-repair) | Audit/repair 68-granule FAT | 500, 600, 700, 760, 780, 790, 800, 850, 880, 9400, 9500 |
| [CHKDSK40.BAS](#chkdsk40bas---40-track-fat-audit-and-repair) | Audit/repair 78-granule FAT | Same core routines, plus 9600 |
| [COMPARE.BAS](#comparebas---byte-for-byte-file-comparison) | Compare files by length and bytes | No local GOSUB calls |
| [DISKCOPY.BAS](#diskcopybas---verified-file-copy-or-full-disk-backup) | Guarded file copy or full-sector backup | 3000-series transaction routines |
| [FIND.BAS](#findbas---find-dispatcher) | Reuse TYPE search engine | 60000 |
| [FLIP.BAS](#flipbas---ram-and-physical-drive-routing) | Switch physical and RAM disk routing | 60000 |
| [HELP.BAS](#helpbas---integrated-topic-reference) | Dynamic topic lookup and display | 400 and topic tables |
| [INSTALL.BAS](#installbas---guarded-file-install-and-backup) | Install or back up files | 3000-series transaction routines |
| [JUMP.BAS](#jumpbas---drive-navigation-with-optional-program) | Switch drive, run file or list contents | No local GOSUB calls |
| [MEM.BAS](#membas---basic-memory-status-and-map) | Memory statistics and map | 60000 |
| [SYSMAP.BAS](#sysmapbas---legacy-and-512k-map-overview) | Short map explainer | No GOSUB |
| [T40.BAS](#t40bas---geometry-checker-compatibility-wrapper) | Route to CHKDSK | 60000 |
| [TYPE.BAS](#typebas---disk-file-viewer-and-find-engine) | View text/BASIC, token decode, search | 1000, 2000, 2500, 3000, 5000, 5100, 5200, 7000, 8000, 8100, 8500, 8600 |

## CHKDSK.BAS - Geometry-aware checker dispatcher

**Syntax:** `CHKDSK [0-3] [REPAIR]`.

**Use:** Probe whether the requested/current drive is 40 tracks (read track 35) or 35 tracks (read track 34); report geometry; chain to `CHKDSK40.BAS` or `CHKDSK35.BAS`, using the Tools disk fallback search paths.

**Routines:** 9500-9540 reads a command-tail word; 5-45 parses optional drive/REPAIR; 60-200 probes geometry; 300-450 loads the appropriate checker; 900 prints usage. Read failures display unreadable-disk errors.

**Caution:** `REPAIR` requests write access and is not a non-destructive scan. Check disk geometry and keep an image backup.

## CHKDSK35.BAS - 35-track FAT audit and repair

**Syntax:** Internal worker loaded by CHKDSK; the source also recognizes `[0-3] [REPAIR]`.

**Use:** Audit a 68-granule disk allocation table on track 17. Counts active files, used/free granules, crosslinks, lost granules, broken chains, loops, and invalid links. Without REPAIR, reports errors without intentionally rewriting the FAT. With REPAIR, attempts repairs and rescans.

| Lines | Internal function |
| --- | --- |
| 120-180 | Read FAT and directory sectors; maintain active-file ownership. |
| 300-495 | Count/report errors and rescan repair output. |
| 500-580 | Traverse a file's FAT chain; detect loop, crosslink, invalid and free links. |
| 600-680 | Parse directory entries and locate each file's start granule. |
| 700-746 | Relocate crosslinked chains to free granules where available. |
| 760-766 | Copy a granule's nine physical sectors. |
| 780-800 | Truncate corrupt chain or free a lost granule. |
| 850; 880 | Rewrite FAT and change a FAT link in the in-memory image. |
| 9400-9450; 9500-9540 | Filename trimming and command-tail parsing. |
| 63000-63020 | Cleanup; optionally return to XMM or INFO via routing flags. |

**Cautions:** Repair modifies directory/FAT sectors and can copy data sectors. Filesystem recovery is best-effort; some broken or shared chains may not be recoverable. No claim is made that every kind of corruption can be repaired automatically.

## CHKDSK40.BAS - 40-track FAT audit and repair

**Syntax:** Same user-facing CHKDSK interface, with 78 physical granules on a 40-track disk.

**Use:** Performs the same allocation-chain, directory, lost-granule and crosslink checks as CHKDSK35 over 78 FAT entries. Also detects a very specific state in which the extra ten 40-track FAT entries appear cleared.

**Functions:** Core 500-880 mirror the 35-track audit/repair engine; 9400-9540 handle names and arguments; 9600-9690 validate and optionally restore the 40-track FAT extension; 63000-63020 cleanup/return routing.

**Special recovery limitation:** The 9600-series code does **not** blindly regenerate extra FAT entries. It checks a detailed expected directory and allocation signature, including particular EDB file names and locations, before attempting the known extension restoration. An ambiguous layout produces `40-TRACK FAT RECOVERY AMBIGUOUS` and no changes.

**Caution:** The signature applies only to the expected disk layout. Do not infer that this repair safely reconstructs the FAT extension on arbitrary third-party images. Use `CHKDSK` to inspect first, and `REPAIR` only on a backed-up copy.

## COMPARE.BAS - Byte-for-byte file comparison

**Syntax:** `COMPARE FILE1 TO FILE2`.

**Use:** Parse two filenames separated by the TO token or spaces; open both as one-byte random-record files, obtain their lengths, and compare every byte if the lengths agree.

**Main functions:** 10-290 extract and normalize two file arguments, 300-380 print sizes and detect a length mismatch, 390-460 compare corresponding records, 470 closes files, 500-530 provide usage.

**Output:** Reports which file is larger, identical files, or equal size but different content. The source has no separate GOSUB routines.

**Caution:** Read-only comparison, but opening either file can fail if the drive or filename is unavailable.

## DISKCOPY.BAS - Verified file copy or full disk backup

**Syntax:**

    DISKCOPY 0 TO 1
    DISKCOPY FULL 0 TO 1

**Modes:** Normal mode walks the source directory and copies each file with a temporary-file verification/journal workflow. FULL mode copies the complete disk sector-by-sector, deferring track 17 (directory and FAT) until last.

**Important subroutines:**

| Lines | Function |
| --- | --- |
| 500-590 | Parse source, destination, FULL and TO. |
| 1000-1230 | File-by-file copy from source directory. |
| 2100-2180 | Probe 35/40-track geometry and reject mismatched FULL disks. |
| 3000-3090 | Guarded copy transaction with swap journal, temp and old-file backup. |
| 3100-3120 | Ask permission before overwriting an existing destination. |
| 3200-3220 | Generate reserved temp/backup/journal filenames. |
| 3400-3460 | Scan destination for existing files, free directory entries and swap state. |
| 3500-3525 | Count destination free granules. |
| 3600-3690 | Verify file size and all data bytes using 128-byte records. |
| 3700-3790 | Recover an incomplete journaled transaction. |
| 3970-3990 | Attempt recovery after failures and stop safely. |

**Reserved names:** `EDBTEMP.TMP`, `EDBOLD.BAK`, `EDBSWAP.JRN`. If these are already present, the program can stop rather than silently overwrite them.

**Warning:** FULL copies the entire destination disk and **overwrites its previous contents**. Normal mode's safeguards do not make FULL non-destructive. Normal mode also requires sufficient free granules and directory slots for safe staging; on errors verify/recover before further copying.

## FIND.BAS - FIND dispatcher

**Syntax:** `FIND "text" [filename]`.

**Use:** Parse the original command tail, prefix a private `@F` mode marker and chain to `TYPE.BAS`, which performs the actual file search. The dispatcher itself does not scan BASIC RAM or file contents.

**Internal routines:** 10-50 transform command buffer; 60 invokes `TYPE.BAS`; 60000-60060 routes `?` to HELP.

**Important:** When filename is omitted, TYPE selects the recorded **Last load** `.BAS` disk file. Searching is not performed against unsaved BASIC program memory. See [FIND in the user manual](USER_MANUAL.md#5-find---locating-text).

**Implementation note:** A command-length warning exists at line 35, but the forward loop at lines 20-30 branches directly to 40 on NUL, so do not assume the warning constitutes a comprehensive buffer bound.

## FLIP.BAS - RAM and physical drive routing

**Examples:** `FLIP`, `FLIP 3`, `FLIP 0`; a `J` suffix is recognized to hand off to CD/JUMP-style directory behavior.

**Use:** Manipulate RAM/physical disk presentation through EDB's 512K cached drive infrastructure, checking driver signatures and current physical/cache assignments before touching routing memory. Displays resulting drive and volume information via `VOL.BAS` or `CD.BAS`.

**Main functions:** 5-67 parse options; 100-180 validate capability and routing; 200-265 contain drive-2 routing code; 300-399 swap cache/physical drive-3 routing and restore; 700-714 dispatch follow-up commands; 800-890 report errors; 60000-60060 HELP.

**Current-source quirk:** In this v15 file, line 143 immediately routes `N=2` to line 890 (`Drive 2 is physical`). The subsequent branch at line 145 for `N=2` cannot be reached through that path. Thus the present source does **not** justify documenting `FLIP 2` as an always-working toggle. This is a documentation observation, **not a code change**.

**Caution:** Changes disk routing and may influence which drive receives subsequent writes.

## HELP.BAS - Integrated topic reference

**Keyboard revision:** The COLOR topic at 14554 sets the private NAMES! command tail and chains to COLOR, which owns physical press/release handling. This avoids extra memory use in HELP and prevents a held key from skipping the first page.

**Syntax:** `HELP`, `HELP topic`, or supported commands followed by `?`.

**Use:** The comprehensive HELP engine on TOOLS. Reads the command argument from `$FC80`, normalizes it to uppercase, locates the matching `REM` topic in its own BASIC program, then patches a dispatch line and prints the topic's help screen.

**Internal mechanics:** 10-60 command-tail parsing, 70-210 scan BASIC's linked-line text for REM topic names, 100/400-410 locate the editable dynamic dispatch area, 220-240 patch a five-digit target, 450-500 dispatch, 300 unknown topic. Topics are grouped in source line blocks 10000-40100. An active XEDIT signature leads to an advisory, not help dispatch.

**Topics include:** Boot and Tools command indexes; `*`, `DOSBOOT`, `USER`, `ADMIN`, `STARTUP`, `AUTORUN`, `CD`, `COLOR`, `UPGRADE`, `XMM`, `ASK`, `COPY`, `DRIVE`, `KILL`, `RENAME`, `CURSOR`, `VCC`, `CPUID`, `DEL`, `DIR`, `DISKCOPY`, `EDIT`, `FORMAT`, `ID`, `LABEL`, `LAST`, `LOAD`, `PATH`, `REBOOT`, `REN`, `KEYREP`, `SAVE`, `VER`, `VOL`, `WIDTH`, `JUMP`, `INSTALL`, `INFO`, `SYSMAP`, `COMPARE`, `FIND`, `CHKDSK`, `FLIP`, `TYPE`, `T40`, `MEM`, `XBENCH`, `XEDIT` and related companion-disk tools.

**Duplicate:** The BENCH copy of `HELP.BAS` is byte-identical to TOOLS' HELP.BAS in the current baseline. The small BOOT `HELP.BAS` is a dispatcher, not this same program.

**Known discrepancy:** The current HELP description of `FIND` without a filename implies an in-memory BASIC search, while the `FIND.BAS` + `TYPE.BAS` implementation searches the Last load disk file. The manual documents the code and flags the difference.

## INSTALL.BAS - Guarded file install and backup

**Syntax:** `INSTALL` or `INSTALL BACKUP`.

**Use:** Install files from the physical disk behind the 512K cache to the configured target, or back up files in the reverse direction. Requires matching FLIP driver/cache state and a compatible physical drive. It walks the source directory and stages, verifies and conditionally replaces destination files.

**Important routines:**

| Lines | Function |
| --- | --- |
| 10-90 | Parse optional BACKUP flag. |
| 100-270 | Check FLIP driver signatures, `flip.inf`, physical/cache routing. |
| 300-540 | Iterate source entries, count copied, overwritten and skipped files. |
| 900 | Restore routing state. |
| 3000-3090 | Guarded copy with journaling, verified temp and backup names. |
| 3100 | User confirmation before replacing an existing file. |
| 3200, 3400, 3500 | Reserve swap names, check directory, count free granules. |
| 3600 | Compare copied data byte-for-byte. |
| 3700 | Recover/rollback incomplete operations. |
| 3970-3990 | Report and stop on verification/transaction problems. |

**Dependencies:** `flip.inf`, `$5Dxx` RAM-drive routing state, disk allocation and random record I/O. Shares a transaction design with DISKCOPY, but they remain separate BASIC programs.

**Caution:** INSTALL and BACKUP **write destination files**. Leave extra free granules and directory entries for staging. On recovery ambiguity, stop and inspect the disk rather than deleting journal files manually.

## JUMP.BAS - Drive navigation with optional program

**Syntax:** `JUMP n [program]`, with drive `n` from 0 to 3.

**Use:** Attempt to select the requested drive, switch RAM/physical disk routing where appropriate and supported, then RUN an optional program. With no program, display the directory by chaining to `DIR.BAS`.

**Functions:** 5-65 parse drive and program argument; 100-390 inspect and change routing; 690/700-730 report routing failures, select drive and dispatch. No local GOSUB entry points.

**Caution:** Driver checks can skip unavailable FLIP operations and continue; verify which drive actually became active. If a filename is supplied, it is passed to RUN, replacing the active BASIC program.

## MEM.BAS - BASIC memory status and map

**Syntax:** `MEM`, `MEM MAP`.

**Use:** Display free workspace and string reserve/usage, or the BASIC program, array and string-area addresses obtained from interpreter zero-page pointers.

**Main functions:** 100-180 display capacity statistics; 200-297 display address map; 60000-60400 parse MAP or HELP; 63000-63160 provide a key-queue-aware exit with a hold-BREAK check and optional return to XMM/INFO.

**Dependencies:** `XKEY.DRV` keyboard support; interpreter pointers at `$19`, `$1B`, `$1D`, `$1F`, `$21`, `$23` and `$27`. The program is diagnostic and should not be mistaken for the native XMM allocator itself.

## SYSMAP.BAS - Legacy and 512K map overview

**Syntax:** `SYSMAP`.

**Use:** Prints a compact comparison between the historical 128K memory layout and the 512K XMM architecture (64 physical 8K RAM banks, XMM native code at `$6000-$6FFF`).

**Functions:** Lines 10-120 print static explanatory text; no GOSUB routines, no disk writes and no dynamic MMU scan.

**Note:** Mentioning 128K is historical context, not a restriction on the current 512K configuration.

## T40.BAS - Geometry checker compatibility wrapper

**Syntax:** `T40`.

**Use:** Clear the inherited command-tail buffer and invoke the geometry-aware `CHKDSK.BAS` utility, looking first in the Tools disk's candidate drive paths.

**Routines:** 60000-60060 HELP parser; 10-70 dispatch with error fallback. Despite its name, it delegates detection to CHKDSK rather than blindly assuming a 40-track disk.

**Caution:** Does not itself execute format or repair.

## TYPE.BAS - Disk-file viewer and FIND engine

**Keyboard revision:** The pager calls 57000–57300 at line 8075 for fresh physical key detection, Q recognition, stable release and buffer cleanup. FIND retains its existing non-paginated search path.

**Syntax:** `TYPE filename`; FIND uses its internal private `@F` mode. `@M` is recognized for ordinary viewer mode.

**Use:** Display text or tokenized BASIC files page by page, detokenize program lines, and implement case-insensitive FIND. Current FIND copies the source to `EDBSCAN.TMP` on the cache drive before scanning, then attempts cleanup.

| Lines | Internal function |
| --- | --- |
| 10-90 | Choose mode, parse filename and open suitable disk file. |
| 110-180; 300-330 | Detect tokenized BASIC and iterate text or tokenized records. |
| 1000-1070 | Parse quoted or unquoted command words. |
| 2000 | Read one byte through a one-byte random record. |
| 2500-2570 | Assemble one ASCII text line. |
| 2700-2750 | Detect non-printable binary data. |
| 3000-3170 | Decode BASIC line numbers, tokens, functions and quoted text. |
| 5000-5220; 6000-6070 | Map token bytes to BASIC keyword/function names. |
| 7000-7040 | Uppercase a search string for case-insensitive matching. |
| 8000-8095 | Print or paginate output, with `-- more --` and Q-to-quit. |
| 8100-8140 | Test search matches and print BASIC or text line numbers. |
| 8500-8530 | Remove temporary scan file after a search. |
| 8600-8690 | Resolve filename-free FIND through Last load `$5EE0`, restricted to `.BAS`. |

**Warnings:** FIND does not search unsaved BASIC RAM; a disk file is searched. The scan requires enough cache-drive space to create a temporary file. TYPE executes a BASIC utility, so save unsaved work before using it. The display token table is fixed to current supported CoCo BASIC tokens.

---

## Shared TOOLS patterns

- Some programs are true commands (`COMPARE`, `DISKCOPY`) while others chain to a separate worker (`FIND`, `T40`, `CHKDSK`).
- The CHKDSK workers operate on different **68-granule versus 78-granule** layouts and must not be interchanged manually without checking geometry.
- Verified file-copy and recovery-journal logic improves preservation but does not guarantee recovery from every write failure or an abruptly removed disk.
- Native `.DRV` dependencies are not themselves BASIC programs; they are referenced where the .BAS code invokes them.

**Source audit:** All 14 v15 TOOLS `.BAS` entries. No BOOT, TOOLS or BENCH disk images or executables are modified by this documentation.
