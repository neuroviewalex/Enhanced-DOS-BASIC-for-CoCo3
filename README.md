# Enhanced DOS BASIC for the CoCo 3

### Your CoCo 3. Your BASIC. A whole lot more possibilities.

**Enhanced DOS BASIC (EDB) v15** brings a friendlier, more capable command environment to the Tandy Color Computer 3. It keeps the familiar BASIC experience at the heart of the machine while making everyday jobs—finding files, moving between disks, making backups, configuring your workspace, and checking your system—far easier.

EDB is for people who love the CoCo 3 and want to *use it*: write programs, explore disks, organize projects, experiment with 512K memory, and get things done without constantly juggling little utility programs.

## What can you do with EDB?

### Find your way around your disks

- **Jump to a disk by its name.** With `CD TOOLS`, for example, EDB looks for the volume named `TOOLS` instead of making you remember a drive number.
- **See what's there.** `DIR` lists files, shows available space, and can narrow the results to a name or file type.
- **Keep disks recognizable.** `VOL` shows a disk's volume name; `LABEL` lets you change it.
- **Move between your working disks.** `CD`, `JUMP`, and `FLIP` make it easier to navigate mounted disks and, on supported setups, RAM-backed drives.
- **Explore an emulator's disk playlist.** With a matching VCC-EDB setup, `CD` can find a named disk in drive 3's playlist and switch to it automatically.

### Take better care of your files

- **Find what you're looking for.** `FIND` searches text in your current BASIC program or in a file on disk.
- **Read files comfortably.** `TYPE` displays text or BASIC files a page at a time.
- **Rename and remove files.** `REN` and `DEL` give common file-management jobs simple commands.
- **Check whether two files really match.** `COMPARE` compares file sizes and contents.
- **Inspect a disk for problems.** `CHKDSK` checks a disk and offers a separate, explicitly requested repair mode.

### Make backups with confidence

EDB includes more than a quick file copy:

- **`DISKCOPY`** copies files using a guarded, verified workflow.
- **`DISKCOPY FULL`** makes a full disk-to-disk copy on matching 35- or 40-track media.
- **`INSTALL`** helps transfer a working set of files, including a backup mode.

The copying tools are designed to check their work and protect existing files where possible. You still stay in control: a full disk copy **overwrites the destination disk**, so choose your drives carefully.

### Make the CoCo feel like yours

- **Choose your screen.** Switch between 32-, 40-, and 80-column text with `WIDTH`.
- **Give it some color.** `COLOR` supports named colors and a palette chart, not just numeric settings.
- **Tune the keyboard.** `KEYREP` adjusts how quickly keys repeat and how long they wait before repeating.
- **Set up your startup experience.** `STARTUP`, `USER`, and `ADMIN` let you manage names, display preferences, and startup programs.
- **Pick up where you left off.** `LAST` and the familiar BASIC load/save commands help keep track of your recent work.

### Explore the power of 512K

EDB v15 includes **XMM**, its current memory-management and diagnostic environment for a 512K CoCo 3.

- Run focused memory checks or the complete test collection.
- See memory and BASIC workspace information with `MEM` and `INFO`.
- Run `XMM BENCH` to explore memory-service performance.
- Use supported RAM-disk and disk-switching features to make a multi-disk workflow more convenient.

You don't need to understand memory maps to get value from these tools. EDB gives you readable results and helps you find out what your machine can do.

### Get help without leaving BASIC

The **Tools disk includes integrated EDB HELP**, covering the available commands, arguments, and common options.

Try `HELP CD`, `HELP DISKCOPY`, or `XMM ?`. If the Tools disk isn't mounted, the Boot disk explains where to find the full help system. Help pages are written for the CoCo screen, not a modern wide display.

## Start exploring

Boot EDB, mount the Tools disk, and try a few commands at the prompt:

```text
DIR
CD TOOLS
HELP
HELP CD
INFO
XMM
```

Or start with a task:

| I want to… | Try… |
| --- | --- |
| See the files on a disk | `DIR` |
| Find a disk by its volume name | `CD name` |
| Learn how a command works | `HELP command` |
| Search for text | `FIND` |
| View a text or BASIC file | `TYPE filename` |
| Check a disk | `CHKDSK` |
| Compare two files | `COMPARE` |
| Copy or back up disks | `DISKCOPY` |
| Change screen width | `WIDTH 80` |
| Choose display colors | `COLOR` |
| See system information | `INFO` |
| Explore 512K memory tools | `XMM` |

## The disks in this repository

| Disk image | What's on it |
| --- | --- |
| [`EDB_v15_512k_boot.dsk`](EDB_v15_512k_boot.dsk) | The EDB startup environment, everyday disk commands, display and startup preferences, and the Boot help fallback. |
| [`EDB_v15_512k_tools.dsk`](EDB_v15_512k_tools.dsk) | Integrated HELP, disk maintenance and backup tools, file utilities, system information, and XMM diagnostics. |

The [`extracted/`](extracted/) directory contains the original files from both official disk images for browsing and development. Some BASIC files are stored in their original tokenized CoCo format.

EDB also has **separate companion disks** for additional creative and productivity tools, including editing, graphics, sound, and the ASK environment. Those companion disks are not included in the two downloads above.

## What do I need?

EDB v15 is built around the **CoCo 3 with 512K RAM** and an EDB-compatible disk environment. Some conveniences—especially searching and switching through a drive-3 disk-image playlist—need the matching **VCC-EDB** emulator enhancements.

YOU MUST DOWNLOAD THE LATEST VERSION OF VCC-EDB to properly use Enhanced DOS BASIC v15!

https://github.com/neuroviewalex/VCC-EDB

You can run EDB v15 on real CoCo3 hardware but it will be as slow as 40 years ago. ;) I strongly suggest using VCC-EDB at 125.28Mhz (default install)

The two official disk images and their promotion history are maintained together in this repository. See [`BASELINE_HISTORY.md`](BASELINE_HISTORY.md) for the currently promoted versions and the changes behind them.

---

**The spirit of EDB is simple:** keep the joy of the Color Computer 3, and make the things you want to do with it easier, faster, and more fun.
