# EDB v15 - Complete BASIC Program and Function Reference

**Official program inventory for the current promoted v15 disks**  
**Source baseline:** `EDB_v15_512k_boot.dsk` SHA-256 `974d15a700765469fdc4e8672b0f0d0ea5c5a5d0b2f038823c72c399d80d50f7`, plus the unchanged official TOOLS and BENCH disks.  
**Documentation coverage:** **45 of 45** current `.BAS` directory entries audited and documented, including the literal `*.BAS` file and all three HELP.BAS variants/copies.  
**Validation:** Static inspection of tokenized CoCo BASIC files from `extracted/` on GitHub. These descriptions are not a claim of new VCC-EDB or hardware testing.

## Start here

- [**Official EDB v15 User Manual**](USER_MANUAL.md) - user-oriented command syntax, FIND/LOAD/EDIT/SAVE examples and troubleshooting.
- [**BOOT BASIC programs and functions**](BASIC_PROGRAMS_BOOT.md) - **26 entries**. Startup, profiles, disk navigation, display, editor dispatcher, file commands and upgrades.
- [**TOOLS BASIC programs and functions**](BASIC_PROGRAMS_TOOLS.md) - **14 entries**. HELP, FIND/TYPE, disk checks, guarded copying, installation and memory reporting.
- [**BENCH BASIC programs and functions**](BASIC_PROGRAMS_BENCH.md) - **5 entries**. XMM diagnostics, service/native benchmarks and results viewer.

Every program section explains its purpose, command syntax where applicable, implementation paths, important GOSUB routine entry points, dependencies, side effects, and known limitations. A `GOSUB` line number is local to its own BASIC file; it is not a command name.

## BOOT disk - 26 BASIC entries

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

## TOOLS disk - 14 BASIC entries

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
| `MEM.BAS` | [Memory status/map](BASIC_PROGRAMS_TOOLS.md#membas---basic-memory-status-and-map) | [File](../extracted/tools/MEM.BAS) |
| `SYSMAP.BAS` | [Memory map explainer](BASIC_PROGRAMS_TOOLS.md#sysmapbas---legacy-and-512k-map-overview) | [File](../extracted/tools/SYSMAP.BAS) |
| `T40.BAS` | [Compatibility CHKDSK wrapper](BASIC_PROGRAMS_TOOLS.md#t40bas---geometry-checker-compatibility-wrapper) | [File](../extracted/tools/T40.BAS) |
| `TYPE.BAS` | [TYPE and FIND engine](BASIC_PROGRAMS_TOOLS.md#typebas---disk-file-viewer-and-find-engine) | [File](../extracted/tools/TYPE.BAS) |

## BENCH disk - 5 BASIC entries

| File | Documentation | Direct source |
| --- | --- | --- |
| `HELP.BAS` | [Duplicate full help engine](BASIC_PROGRAMS_BENCH.md#helpbas---integrated-help-copy) | [File](../extracted/bench/HELP.BAS) |
| `XBENCH.BAS` | [XMEM/XMATH service benchmark](BASIC_PROGRAMS_BENCH.md#xbenchbas---legacy-xmemxmath-service-benchmark) | [File](../extracted/bench/XBENCH.BAS) |
| `XMBCPU.BAS` | [6809 / 6309 native tests](BASIC_PROGRAMS_BENCH.md#xmbcpubas---6809-and-6309-native-memory-comparison) | [File](../extracted/bench/XMBCPU.BAS) |
| `XMM.BAS` | [Diagnostics controller](BASIC_PROGRAMS_BENCH.md#xmmbas---xmm-diagnostics-controller) | [File](../extracted/bench/XMM.BAS) |
| `XMSHOW.BAS` | [Saved benchmark viewer](BASIC_PROGRAMS_BENCH.md#xmshowbas---saved-results-viewer) | [File](../extracted/bench/XMSHOW.BAS) |

## Key cross-program interactions

### Programming and editing

    FIND.BAS -> TYPE.BAS -> saved disk .BAS
    LOAD "FILE.BAS" -> BASIC RAM program
    EDIT [line] -> native EDIT.DRV
    EDIT filename -> EDIT.BAS wrapper -> file loader
    SAVE "FILE.BAS" -> DOSCORE.DRV save hook
    LAST.BAS -> last-load / last-run / next-save records

See the [complete user workflow](USER_MANUAL.md#2-the-five-command-programming-workflow). FIND is **file-based**; it is not a live search of edited BASIC RAM.

### Disk and filesystem services

    CD.BAS -> VOL.BAS -> optional AUTORUN profile
    CD.BAS -> CDSEQ.DRV or CDINIT.DRV
    CHKDSK.BAS -> CHKDSK35.BAS or CHKDSK40.BAS
    DISKCOPY.BAS / INSTALL.BAS -> staged copy + journal + verify
    UPGRADE.BAS -> RAMBOOT.DRV -> cached file refresh
    REN.BAS -> COPY + compare bytes + KILL old file

### Profiles and boot behavior

    *.BAS -> BOOT.DRV
    USER.BAS / ADMIN.BAS -> startup.inf -> REBOOT.BAS
    STARTUP.BAS -> startup.inf (no automatic reboot)
    AUTORUN.BAS -> autorun.inf -> CD.BAS launch policy

### XMM and benchmarks

    XMM.BAS -> native XT*.DRV tests
    XMM.BAS -> XBENCH.BAS -> XBSCORE.DAT
    XMM.BAS -> XMBCPU.BAS -> XMSCORE.DAT
    XMM.BAS -> XMSHOW.BAS -> saved measurements/reference

## Source, terminology and scope

- The official BOOT, TOOLS and BENCH disks are represented in [`extracted/`](../extracted/) and verified by [`MANIFEST.json`](../extracted/MANIFEST.json). In total there are 93 extracted files, of which **45** end in `.BAS`.
- Files are stored in their original tokenized CoCo BASIC format. Text shown in the reference was reconstructed from BASIC tokens and reviewed by program line number; it was **not** substituted into the disks.
- `*.BAS` is a **literal directory filename** on BOOT; do not count it as a wildcard file collection.
- The three `HELP.BAS` directory entries are counted separately. TOOLS and BENCH hold the same full program; BOOT holds a different small dispatcher.
- A **local routine** refers to a numbered BASIC code block, usually called by `GOSUB`, often including return, error and cleanup paths. The disk-specific chapters identify the primary routines and roles rather than claiming every individual BASIC statement is a public API.
- Native `.DRV` and `.BIN` programs are described as dependencies when called. A complete native machine-code API manual would be a separate companion project.
- Behaviors based only on static source inspection are described as such. Hardware-dependent behavior, error recovery and timing require emulator/hardware tests before being presented as runtime guarantees.

## Updating the reference

For each authorized future change to an EDB `.BAS` file:

1. Read the current official source and existing relevant documentation.
2. Update the appropriate disk-specific entry, including syntax, internal routines, dependencies and important cautions.
3. Keep the index and the main user manual consistent; preserve existing content not involved in the update.
4. Commit documentation changes with a clear explanation and verify the Git diff.
5. Never silently modify EDB binaries or declare a new software baseline as part of a manual-only edit.

The authoritative reference always lives on GitHub in these Markdown files, alongside [`USER_MANUAL.md`](USER_MANUAL.md).
