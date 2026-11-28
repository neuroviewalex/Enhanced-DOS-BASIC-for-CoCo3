# EDB v15 BASIC Program Reference - BOOT Disk

**Release synchronization status (2026-11-27):** The owner-designated v15 release attachments, repository disk images and extracted payloads now match exactly. The source inventory is verified; the approved compact HELP passed targeted 6809/6309 VCC tests. Earlier candidate tests are not a full new system regression. See [release synchronization status](RELEASE_SYNC.md).

**Coverage:** All 26 `.BAS` directory entries in the promoted v15 BOOT disk, including the literal file named `*.BAS`.  
**Method:** Inspected the tokenized BASIC source in `extracted/boot/` and identified command paths, local GOSUB routines, dependencies and side effects.  
**Status:** Source-level documentation - not a new hardware/emulator test.  
**Companion references:** [Complete program index](BASIC_PROGRAM_REFERENCE.md) | [User manual](USER_MANUAL.md) | [TOOLS programs](BASIC_PROGRAMS_TOOLS.md) | [BENCH programs](BASIC_PROGRAMS_BENCH.md).

The filenames below are the **actual files on the BOOT disk**. A `GOSUB` line number is an internal routine entry point, not a separate EDB command. EDB's input command tail is often stored at `$FC80`; many programs read it using PEEK and use their line-60000 helper to detect a trailing question mark and call the separate HELP program. Entries marked **destructive** or **system state** deserve particular care.

## Command summary

| BASIC file | Primary use | Type |
| --- | --- | --- |
| [\*.BAS](#bas---boot-entry-stub) | Detect boot environment, select width, load BOOT.DRV | Startup stub |
| [ADMIN.BAS](#adminbas---administrator-profile) | Administrator profile and login | Configuration |
| [AUTORUN.BAS](#autorunbas---per-disk-autorun) | Enable autorun, edit disk launch profile | Configuration |
| [CD.BAS](#cdbas---drive-and-volume-navigation) | Select drive/volume, playlist search and launch | Command / dispatcher |
| [COLOR.BAS](#colorbas---text-colour-and-palette) | Select foreground/background, colour chart | Display command |
| [CPUID.BAS](#cpuidbas---hardware-identification) | Display cached hardware identity | Dispatcher |
| [CURSOR.BAS](#cursorbas---cursor-restoration) | Restore keyboard cursor behavior | System utility |
| [DEL.BAS](#delbas---delete-a-file) | Delete named file | Destructive command |
| [DIR.BAS](#dirbas---directory-and-free-space) | List/filter directory, report free space | Command |
| [EDIT.BAS](#editbas---edit-filename-dispatcher) | Find BASIC file and load for editing | Dispatcher |
| [FORMAT.BAS](#formatbas---initialize-a-disk-directory) | Clear allocation/directory and label disk | Destructive command |
| [HELP.BAS](#helpbas---boot-help-dispatcher) | Find integrated HELP disk or explain absence | Dispatcher |
| [ID.BAS](#idbas---cached-system-information) | Read cached system identification | Command |
| [KEYREP.BAS](#keyrepbas---keyboard-repeat) | Set repeat rate/delay and boot defaults | Configuration |
| [LABEL.BAS](#labelbas---change-volume-label) | Write volume.inf label | File utility |
| [LAST.BAS](#lastbas---filename-history) | Show last load/run and next save | Command |
| [PATH.BAS](#pathbas---drive-search-order) | Display effective drive search priority | Command |
| [REBOOT.BAS](#rebootbas---restart-edb) | Restart via machine-code entry point | System utility |
| [REN.BAS](#renbas---verified-file-rename) | Copy, verify and remove original | File utility |
| [STARTUP.BAS](#startupbas---active-startup-profile) | Edit startup.inf | Configuration |
| [UPGRADE.BAS](#upgradebas---install-and-refresh-cache) | Install/refresh cached files | System utility |
| [USER.BAS](#userbas---user-profile-and-login) | Edit user.inf and startup.inf | Configuration |
| [VCC.BAS](#vccbas---emulator-check) | Inspect VCC identity signal | Diagnostic |
| [VER.BAS](#verbas---version-information) | Display EDB version | Command |
| [VOL.BAS](#volbas---volume-name) | Read/create volume.inf, integrate with CD | Command |
| [WIDTH.BAS](#widthbas---text-display-width) | Switch 32/40/80 column mode | System command |

## *.BAS - BOOT entry stub

**Source:** [extracted/boot/\*.BAS](../extracted/boot/*.BAS) - the asterisk is part of this CoCo directory filename, not an instruction to run every BASIC file.

**Use:** Internal startup path; not a general-purpose editing or file command. It detects the CoCoSDC / FD-50X environment, refuses incompatible hardware, initializes video palette and text width, then runs `BOOT.DRV`.

**Inputs:** Optional width in the command tail (32, 40 or 80); default 40.

**Internal routines:** Lines 100-220 handle the silent controller gate; 60000-60060 route the question-mark help convention. Lines 45-80 reset palette and launch BOOT.DRV.

**Side effects:** Reinitializes display registers and invokes the native boot driver. This file is not a disk wildcard operation.

## ADMIN.BAS - Administrator profile

**Use:** `ADMIN` edits BOOT's `admin.inf`; `ADMIN LOGIN` selects the administrator profile by copying it into `startup.inf` and rebooting.

**Profile fields:** Username, WIDTH instruction, COLOR instruction, optional pre-prompt program. Editing prompts preserve a nonempty existing value; the program prompt accepts an empty entry to clear it.

**Internal routines:** 9000-9080 uppercase/normalize configuration strings; 9200-9260 reopen and verify all four saved lines; 60000-60060 parse `LOGIN` or HELP request; lines 800-820 recover disk state and report save stage.

**Dependencies and effects:** Reads/writes `admin.inf` and `startup.inf`; uses boot-drive and prompt-state locations, restores current drive and flags, invokes `REBOOT.BAS` after normal saved changes. Refuses operation when the XEDIT resident signature is active. **Configuration writes and reboot.**

## AUTORUN.BAS - Per-disk autorun

**Syntax:**

    AUTORUN
    AUTORUN ON
    AUTORUN OFF
    AUTORUN 0
    AUTORUN 1

**Use:** Queries or enables/disables CD-triggered autorun. Drive number 0-3 opens that disk's `autorun.inf` profile editor; editing the BOOT drive is explicitly refused.

**Internal routines:** 9000-9080 normalize configuration text; 9200-9260 verify the four profile lines written back; 60000-60060 HELP convention. Main command parsing occupies 5-80; profile editing 120-310.

**Dependencies and effects:** Flag `$5FDD` controls global autorun; `autorun.inf` supplies application name, WIDTH, COLOR and launch program; `CD.BAS` interprets these when switching disks. Saves a disk file and temporarily switches drives. **A CD operation can launch a program automatically while autorun is on.**

## CD.BAS - Drive and volume navigation

**Keyboard revision:** Lines 8650–8800 and 57100–57220 use an interrupt-protected physical matrix scan, including F1/F2 bits, neutral/release detection and the existing profile-selection interval. The USER/ADMIN selection logic is retained.

**Examples:**

    CD
    CD 2
    CD TOOLS
    CD ALL
    CD ..

**Use:** Select a drive by number or by a case-insensitive substring of `volume.inf`; `CD ALL` lists mounted volume labels. Relative forms such as `CD .`, `CD ..`, `CD /` return to drive 0 as implemented. A missing visible-volume match can invoke VCC-EDB's drive-3 playlist search via `CDSEQ.DRV`, if supported.

**Main control flow:** Lines 5-190 parse commands, search current drive, cache drive, boot drive, remaining drives, then optionally the playlist; 195-400 select the drive and dispatch the volume/autorun display.

**Internal routines:**

| Line(s) | Function |
| --- | --- |
| 500-760 | Interpret startup WIDTH and apply 32/40/80 columns while preserving palette state. |
| 900-1020 | Scan target directory for a configured autorun program. |
| 1200-1260 | Case/space normalization for names. |
| 1300-1520 | Enumerate mounted volumes for CD ALL. |
| 1700-1800 | Render banner and restore prompt display state. |
| 1900-1980 | Parse/apply startup colour values. |
| 2000-2210 | Read volume.inf and find case-insensitive substring matches. |
| 2990; 8600-8995 | Bootstrap/menu and profile selection, including user/admin boot configuration. |
| 50000-50050 | Format long volume labels for display. |

**Dependencies:** `CDINIT.DRV`, `CDSEQ.DRV`, `VOL.BAS`, `DIR.BAS`, `USER.BAS`, `ADMIN.BAS`, `SPINNER.DRV`, `sysinfo.inf`, `autorun.inf`, `startup.inf`, and VCC-EDB playlist protocol. Native-state flags influence cache routing.

**Caution:** CD can change the active drive, screen mode and colours and may launch an autorun program. Playlist searching is emulator-specific; do not assume it works on real hardware.

## COLOR.BAS - Text colour and palette

**Keyboard revision:** Lines 11050, 11110 and 20200 call 57000–57300. The routine waits for a fresh physical press and stable release (four TIMER ticks), then clears residual input and preserves keyboard settings. The private NAMES! entry at line 11 accepts the HELP COLOR handoff. Both eight-page displays keep their original layouts.

**Examples:**

    COLOR
    COLOR YELLOW ON BLACK
    COLOR ON BLACK
    COLOR NAMES
    COLOR CHART

**Use:** Display the current foreground/background; set either or both colours; page through 64 named colours or a graphical chart. Aliases normalize common names (for example BLUE to BRIGHT-BLUE).

**Internal routines:** 1000-1070 parse words; 500-680 map a name through the 64-entry DATA palette and update video registers; 700-770 reverse-map values to names; 10000-10150 define all 64 names; 11000-11140 paginate a text list; 20000-20970 show/restore an HSCREEN chart and palette, including BREAK cleanup; 60000-60060 route HELP.

**Side effects:** Video palette/hardware registers are modified. Some startup-specific paths return to CD. In chart mode, width and palettes are preserved and restored.

## CPUID.BAS - Hardware identification

**Syntax:** `CPUID`.

**Use:** Selects `ID.BAS` on the current cache drive (read from `$5D3B`) to display EDB's boot-detected CPU/system identification.

**Internal routines:** 60000-60060 routes HELP. Main line 5 validates that cache-drive routing is within 0-3 and line 10 chains to `ID.BAS`.

**Caution:** Reports cached identity data, **not a fresh hardware probe**. Requires an accessible `ID.BAS` and `sysinfo.inf`.

## CURSOR.BAS - Cursor restoration

**Syntax:** `CURSOR`.

**Use:** Applies cursor restoration appropriate to the current 32-, 40-, or 80-column mode.

**Internal routines:** Lines 10-40 detect mode; 100-120 restore 32-column cursor variables/code; 200-220 load byte values from DATA into the display routine region and reset cursor settings for 40/80.

**Side effects:** Writes machine-code RAM at addresses such as `$F787` and `$A19B`. Not a pure display-only status command. Rejects unsupported modes.

## DEL.BAS - Delete a file

**Syntax:** `DEL filename`.

**Use:** Parses the filename from EDB's command tail, calls BASIC `KILL`, then prints the deleted name.

**Internal routines:** Lines 10-50 parse filename; 60000-60060 HELP support.

**Caution:** **Destructive** and not reversible. A missing filename is rejected; disk errors are passed to BASIC.

## DIR.BAS - Directory and free space

**Syntax:** `DIR [0-3] [name|.ext|INFO]`.

**Examples:** `DIR`, `DIR 2`, `DIR *.BAS`, `DIR .DRV`, `DIR INFO`.

**Use:** Reads CoCo directory sectors, prints filenames in columns matched to the current screen width, filters by base filename/full filename/extension, counts active files, and calculates approximate free KiB from the allocation table. INFO invokes native BASIC DIR.

**Internal routines:** 700-760 tokenize command tail; 800-856 parse drive, INFO and filters; 860-880 uppercase names; 500-520 32-column presentation; 50000-50050 wrap volume label; 60000-60060 route HELP. Main 150-397 scans the directory and FAT.

**Dependencies:** `volume.inf`, `DSKI$`, directory track 17 and FAT sector. May create a placeholder `volume.inf` if missing, so a listing is not guaranteed read-only. Ending with `NEW` clears BASIC program memory.

## EDIT.BAS - EDIT filename dispatcher

**Examples:** `EDIT GAME.BAS`, `EDIT MYPROG.DRV` and `EDIT ?`.

**Use:** `EDIT` with no argument opens the first existing line in RAM; if no program is loaded, it reports `No program loaded.` and returns to the prompt. `EDIT filename` (for example, `EDIT VCC` or `EDIT VCC.BAS`) loads the BASIC listing, opens its first existing line, and leaves it in RAM for subsequent editing or SAVE. A missing filename reports failure without replacing the current listing. `EDIT n` edits the requested existing line. SHIFT + Up/Down browses existing line numbers; ENTER commits and exits. BREAK cancellation remains under investigation; do not rely on it to discard edits until verified. Save valuable unsaved work before loading another program.

**Implementation:** The current wrapper parses the filename, checks directory entries for BASIC type, and installs the native edit-entry hook. EDIT R3 corrects the interpreter handoff and transient-command ownership so the loaded listing stays in memory and LAST tracks the selected file. Lines 495–550 implement the load hook and handoff; lines 700–887 retain directory checks and graceful failure.

**Important architecture distinction:** Native `EDIT line-number`, bare `EDIT`, and SHIFT + Up/Down navigation are handled by the **machine-code `EDIT.DRV`**, not the filename dispatcher. EDIT R3 retains the earlier EOF navigation repair and uses controlled redraws with the original ROM typing/keyboard-repeat path.

**Release VCC.BAS:** The owner-uploaded copy includes the period in the positive VCC result message; the negative result ends with an exclamation point.

**Caution:** Loading an editor target changes current BASIC memory. Back up unsaved program edits first.

## FORMAT.BAS - Initialize a disk directory

**Keyboard revision:** Line 230 calls 57000–57300. Confirmation requires a fresh physical Y press and stable release; other input cancels. The actual filesystem-writing routines are unchanged.

**Syntax:** `FORMAT [0-3]` (drive prompt appears if omitted).

**Use:** Displays a destructive warning and waits for `Y`; clears FAT and directory sectors on the selected disk, then writes a new `volume.inf` label.

**Internal routines:** Lines 10-150 parse or prompt for a drive; 200-250 obtain confirmation; 300-420 write FAT/directory and label; 60000-60060 HELP handling.

**Critical caution:** **Destructive.** This BASIC utility operates by writing filesystem metadata sectors. It is not evidence of an exhaustive physical low-level disk format; it makes existing file allocations inaccessible. Back up the target disk, and verify the correct drive before confirming.

## HELP.BAS - BOOT help dispatcher

**Syntax:** `HELP`, `HELP command`.

**Use:** BOOT's small dispatcher checks mounted drives for a `HELP.BAS` **alongside** `XMM.BAS`, then runs the full HELP program on the matching disk. If no suitable disk is present, it displays instructions to mount TOOLS. It refuses to run during the resident XEDIT mode.

**Internal routines:** Lines 10-120 scan directory sectors on drives 0-3; 300 handles disk errors; 400-510 print fallback guidance; 590 reports the XEDIT requirement.

**Dependencies:** The full `HELP.BAS` appears on TOOLS and BENCH; the verified release copies are identical. The BOOT dispatcher is a different program with the same filename.

## ID.BAS - Cached system information

**Syntax:** `ID`.

**Use:** Reads `sysinfo.inf` from the cache drive, splits the recorded string into a two-line display and exits with `NEW`.

**Internal routines:** Lines 10-70 read and display the info file; 200 error fallback; 60000-60060 HELP convention.

**Dependencies:** Cached `sysinfo.inf` and `$5D3B` drive routing. Does not measure or re-detect CPU hardware.

## KEYREP.BAS - Keyboard repeat

**Syntax:**

    KEYREP
    KEYREP ON
    KEYREP OFF
    KEYREP rate [delay]
    KEYREP BOOT

**Use:** Display or change keyboard repeat frequency and initial delay. `ON` maps to 20 repeats/sec and 0.5s delay; `OFF` to 1 repeat/sec and 4s delay. Numeric rate accepts 1-60/sec and delay 0.1-4 seconds. `BOOT` saves current values as startup defaults.

**Internal routines:** 5-200 parse settings and convert values to 60Hz ticks; 600-690 save `keyrep.inf` on the boot drive; 700-740 display current rate/delay; 800/900 end and usage; 60000-60060 HELP.

**Side effects:** Pokes keyboard timing locations `$0E7F`, `$0E76`, `$0E98`; can overwrite `keyrep.inf`.

## LABEL.BAS - Change volume label

**Syntax:** `LABEL [0-3]` (otherwise current drive).

**Use:** Prompts for a volume name and saves it in `volume.inf`. An empty response can retain an existing label or initialize a blank label to "New volume".

**Internal routines:** 6-12 parse optional drive; 50-120 detect/read `volume.inf`; 130-160 save the label; 60000-60060 HELP.

**Side effects:** Writes on the selected drive. It changes the logical label file, not the disk's physical geometry.

## LAST.BAS - Filename history

**Syntax:** `LAST`.

**Use:** Print Last load, Last run and Next save filenames for the command-history hooks.

**Internal routines:** 10-20 read `$5EE0-$5EEC`; 30-40 read `$5EED-$5EF9`; 41-45 read `$78DE-$78EA`; 60000-60060 HELP.

**Caution:** A history entry is not proof that the file still exists or that the loaded BASIC program is saved. See the [programming chapter](USER_MANUAL.md#3-last---filename-history).

## PATH.BAS - Drive search order

**Syntax:** `PATH`.

**Use:** Display the order of lookup: current drive; cache drive if distinct; boot drive if distinct; remaining drives 0-3.

**Internal routines:** Main 10-70 prints the order; 60000-60060 handles HELP.

**State:** `$095A` current drive, `$5D3B` cache drive and `$78F2` boot routing. This command reports the order; it does not modify it.

## REBOOT.BAS - Restart EDB

**Syntax:** `REBOOT`.

**Use:** Returns to WIDTH 32, clears display and version marker bytes at `$6FF8-$6FFF`, resets a BASIC location and executes the native reboot entry point `$8C1B`.

**Internal routines:** Lines 240-250 perform the restart; 60000-60060 HELP.

**Side effects:** **Immediate restart; unsaved program work is lost.**

## REN.BAS - Verified file rename

**Syntax:** `REN old.ext TO new.ext`. Explicit drive suffixes are supported where valid.

**Use:** Safely attempt a rename across or within drives by copying the source to the destination, comparing file lengths and then **every byte**, and deleting the original only after verification. It refuses identical source/destination names.

**Internal routines:** 1000-1070 parse quoted tokens; 1200-1240 normalize case; 1300-1460 normalize and validate drive suffixes; 1500-1570 probe disk readiness. Main 130-310 carries out copy, verify and delete. Lines 900-990 report error conditions.

**Caution:** This protects the original against many verification failures, but copying over a pre-existing destination is not guaranteed transactional. Keep backups of important files.

## STARTUP.BAS - Active startup profile

**Syntax:** `STARTUP`.

**Use:** Edit `startup.inf` on the BOOT disk: username, WIDTH, COLOR, and optional pre-prompt program. It validates output by reopening all four saved lines.

**Internal routines:** 9000-9080 normalize text to uppercase; 9200-9260 read-back verification; 60000-60060 HELP; 800-820 restore state on failure.

**Dependencies:** `startup.inf` and boot-drive state. Unlike USER and ADMIN, this command does not automatically reboot after saving. Refuses editing while XEDIT resident mode is active.

## UPGRADE.BAS - Install and refresh cache

**Syntax:**

    UPGRADE
    UPGRADE CACHE
    UPGRADE filename.ext[:N]

**Use:** Install files from drive 3 to BOOT drive 0, refresh the drive-3 RAM cache, or upgrade a specific named file from a selected drive. `volume.inf` is explicitly excluded from single-file upgrading.

**Internal routines:** 20-90 parse command; 200-310 full install; 500-510 cache refresh; 600-795 targeted copy and refresh; 800-840 normalize filenames; 1000-1150 enumerate disk directory; 2000-2030 remove destination if present; 3000-3080 generate `UPGRADE.DRV` data manifest; 900-950 report failures; 60000-60060 HELP.

**Dependencies:** Native `RAMBOOT.DRV`, cache drive 3 and filesystem operations. The approved cache baseline includes SEQ.BIN and CDSEQ/CDINIT dependencies.

**Caution:** **System-file overwrite and RAM cache mutation.** It can replace installed programs and change BOOT or cache content. Use only with verified disks and backups.

## USER.BAS - User profile and login

**Syntax:** `USER`, `USER LOGIN`.

**Use:** Edit `user.inf`, write the same four-field startup profile to `startup.inf`, verify both files, then reboot. LOGIN copies the user profile to the active startup profile before rebooting.

**Internal routines:** 9000-9080 uppercase text normalization; 9200-9260 four-line read-back verifier; 60000-60060 parse LOGIN/HELP; 800-820 failure recovery.

**Dependencies and side effects:** `user.inf`, `startup.inf`, `REBOOT.BAS`; saves and reboots. Refuses changes when XEDIT is active.

## VCC.BAS - Emulator check

**Syntax:** `VCC`.

**Use:** Reads several memory-mapped registers at `$FF90`, `$FF91`, `$FF94`, `$FF98`, `$FF9C`, `$FF9F`. If all are decimal 27, prints that EDB v15 is running on VCC; otherwise prints the VCC requirement.

**Internal routines:** No GOSUB subroutines; lines 10-40 implement the check.

**Scope:** Detects the expected emulator register signature, not a generic emulator-identification API.

## VER.BAS - Version information

**Syntax:** `VER`.

**Use:** Checks the EDB version signature at `$6FF8` and prints its recorded version digits; defaults to v15 when the signature is absent.

**Internal routines:** 30-100 read/print version; 200-270 contain an optional volume.inf read path; 500-540 format the volume label; 60000-60060 HELP. The volume-label routines are present in the source but not called by the main version output path.

## VOL.BAS - Volume name

**Syntax:** `VOL [0-3]` (default current drive).

**Use:** Display `volume.inf` for the selected drive. If missing and writable, it tries to create a placeholder volume called "New disk". Special state flags can hand control back to `CD.BAS` after display.

**Internal routines:** 30-100 parse drive; 105-190 open or initialize volume.inf with error recovery; 200-230 CD handoff; 50000-50050 wrap long volume names; 60000-60060 HELP.

**Caution:** Despite being a display command, VOL can create `volume.inf` on a writable disk.

## WIDTH.BAS - Text display width

**Syntax:** `WIDTH 32`, `WIDTH 40`, `WIDTH 80`, or `WIDTH` for a prompt.

**Use:** Switch text mode and preserve/restore display palette, colour and screen-control values.

**Internal routines:** 5-45 parse/validate width; 50-70 perform the switch, restore palette and execute BASIC `NEW`; 60000-60060 HELP.

**Side effects:** Clears the current BASIC program via `NEW` and changes display registers. **Save unsaved BASIC work before changing WIDTH.** Refuses switching when XEDIT is active.

---

## Shared BOOT implementation patterns

- Many interactive wrappers read `$FC80` for command-tail arguments and implement `? -> HELP.BAS` at lines 60000-60060.
- Native system files ending in `.DRV` are separate from the BASIC wrappers. This reference documents the BASIC caller and dependencies, not the machine-code internals of every driver.
- `volume.inf`, `startup.inf`, `user.inf`, `admin.inf`, `autorun.inf`, `keyrep.inf`, and `sysinfo.inf` are persistent files with distinct purposes.
- Approved EDIT R3 adds filename handoff and first-line entry; the earlier FIX5 `DOSCORE.DRV` SAVE correction is retained in the local candidate. Details belong in the [main manual](USER_MANUAL.md).

**Source audit:** All 26 v15 BOOT `.BAS` directory entries; contents are original tokenized CoCo BASIC. Subroutine descriptions identify ranges visible in the saved source, not independent emulator tests.
