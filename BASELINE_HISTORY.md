# EDB v15 baseline history

## 2026-11-21 — XMM CPU benchmark FIX7, XMSHOW R1, fresh extraction — promoted

**Official TOOLS disk baseline (user-approved after VCC verification)**

- `EDB_v15_512k_tools.dsk` — SHA-256 `be960c1b25720e54ebf4da4b63dd6464a30c1dfc0f7bfd78fcfadd2d3d4804b3`; Git blob `4d17d47135fd30284401da89fb075af23dd8afef`; 40 active files.
- `EDB_v15_512k_boot.dsk` — **unchanged**; SHA-256 `f9f9ec7d947c1c4810180c91a2bc3e523b823c88be8508b06c0f47fd5287bbcb`; 51 active files.
- The new TOOLS image supersedes the 2026-11-20 TOOLS image only. The BOOT baseline is unaffected.

### XMM CPU comparison

- `XMBCPU.BAS` performs four timed native memory tests on Motorola 6809 and Hitachi 6309, verifies memory transfers and allocation integrity, stores separate scores in `XMSCORE.DAT`, and compares both CPU results when available.
- `XMM6309.BIN` provides the separate Hitachi native path; the prior `XMM6809.BIN` is preserved.
- Clock measurement uses the existing EDB `CPU.DRV` boot method, not a new benchmark-only calibration.
- `XMSHOW.BAS` displays both saved CPUs' scores and measured MHz side by side; the XMM menu includes **C** (CPU benchmark) and **V** (saved viewer).
- The user tested the benchmarking, CPU-specific score retention, clock readout, and viewer in VCC-EDB, then explicitly approved this disk as the official TOOLS baseline.
- Packaged `XMSCORE.DAT` contains initialized **zero scores**; measurements saved in the user's local VCC image were not copied into the published disk.

### Fresh extraction (same approved update)

- `extracted/boot/`: 51 files checked against the unchanged official BOOT disk; all 51 already matched, so no BOOT extracts needed modification.
- `extracted/tools/`: all 40 files extracted and checked against the new official TOOLS image. The five changed/new Git entries are `XMBCPU.BAS`, `XMM.BAS`, `XMM6309.BIN`, `XMSCORE.DAT`, and `XMSHOW.BAS`. The other 35 existing extracts were byte-identical.
- `extracted/MANIFEST.json`: regenerated source blob references, active-file counts, allocated and free granules, and verification metadata for both current disk images.
- 91 extracted files total; directory chains, granule ownership, file lengths, and orphan checks pass on both 40-track disk images.
- `README.md` and every other unrelated repository file are preserved without modification.

### Preservation

This commit was constructed against the existing `main` tree. The repository's existing BOOT disk and all unrelated files remain unchanged. Future EDB changes require a new audit, an explicit change list, authorization, and independent verification.

---

## 2026-11-20 — CD initialization split and XMM cleanup, promoted

**New authoritative disk images (user-uploaded, byte-for-byte verified)**

- `EDB_v15_512k_boot.dsk` — SHA-256 `f9f9ec7d947c1c4810180c91a2bc3e523b823c88be8508b06c0f47fd5287bbcb`; 51 files, 2 free granules in the 35-track range.
- `EDB_v15_512k_tools.dsk` — SHA-256 `b4437121c16847e8a42ca474b1463aa92fd3b83ba27aa5ccfbb3d9a8d1ebc272`; 36 files, 6 free granules in the 35-track range.

These images supersede the Boot playlist-CD R3 and Tools playlist-HELP R2 baselines documented below. The user supplied both exact candidate images and authorized their promotion.

### Boot changes relative to the previous promoted image

- `CD.BAS`: moved initialization logic into a dedicated helper, reducing the command's BASIC program memory footprint.
- `CDINIT.DRV`: added the extracted CD initialization routine.
- `RAMBOOT.DRV`: updated to cache/load `CDINIT.DRV` alongside `CDSEQ.DRV`.
- The other 48 existing Boot files are byte-identical to the previous Boot baseline.

### Tools changes relative to the previous promoted image

- Removed obsolete `XK27.DRV`; active keyboard behavior remains in `XKEY.DRV`.
- Removed `XSTAT.DRV` after the cross-disk dependency audit found no documented caller.
- Kept `XMEMTST.BAS` as a non-destructive informational compatibility command pointing to `XMM ALL` and `XMM BENCH`.
- Updated `SYSMAP.BAS` to distinguish the historical 128K layout from 512K physical banks and current XMM services, with mixed-case lines no wider than 31 columns.
- The other 34 retained Tools files are byte-identical to the previous Tools baseline; two granules were reclaimed.

### Preservation and scope

- The two uploaded `.dsk` files were verified byte-for-byte against the inspected candidates before promotion.
- This GitHub promotion changes only the two root-level disk images and this history file.
- `README.md`, `extracted/`, and `extracted/MANIFEST.json` are intentionally unchanged. The extracted tree remains an older historical snapshot, not a mirror of the promoted disk images.
- No other disks from the 14-disk suite are promoted by this commit.
- Disk structure and preservation were checked statically; no new emulator/hardware-runtime test is asserted by this promotion.

---

## 2026-11-20 — Playlist-aware CD, promoted

**Authoritative disk images**

- `EDB_v15_512k_boot.dsk` — SHA-256 `fc0fc80a75c32fdc747ee1e8f664bb66aa75ab1e70bbb07d4f5b7aa4b225d869`.
- `EDB_v15_512k_tools.dsk` — SHA-256 `9b81833c34f5ec949a68b0ce30b56682a2fa878c456bbf045699f443280d4462`.

The user confirmed the playlist search worked correctly in VCC-EDB Stage A MPI R3 after the signature/version/count test returned `237, 1, 4`. This promotion supersedes the previous Boot and Tools disk baselines; no earlier disk file was deleted from history.

### Boot changes relative to the prior promoted disk

- `CD.BAS` delegates a visible-drive volume miss to the separate playlist helper.
- `RAMBOOT.DRV` caches `CDSEQ.DRV` for use across drive flips.
- New `CDSEQ.DRV` searches the drive-3 playlist through the VCC opt-in status protocol, selects entries **1 through count**, confirms a new completion counter and mounted/requested indexes, and restores the previous selection and drive routing on an unsuccessful search where possible.
- A fail-closed check prevents a scan when the originally mounted drive-3 image is outside the playlist: protocol v1 cannot restore an unlisted image after temporarily replacing it.

### Tools changes relative to the prior promoted disk

- `HELP.BAS` documents playlist-aware `CD` behavior, its mounted-drive and special-path forms, and the VCC protocol dependency. Its mixed-case output remains within 31 columns.

### Emulator dependency and caveats

- Requires the matching VCC-EDB Stage A MPI R3 baseline, with opt-in readback activated by writing `$ED` to `$7F02`.
- The 8-byte status interface is intended for VCC-EDB. Activation writes still affect underlying emulated RAM, so callers must preserve and restore the activation byte.
- If the drive-3 image is outside the configured AutoSequence playlist, add it to that playlist before requesting a reversible `CD` scan.

The two `.dsk` files above are authoritative. The repository's older `extracted/` directory and extraction manifest are historical snapshots and have **not** been regenerated by this promotion; do not treat them as byte-for-byte mirrors of these new images.

The README was deliberately left unchanged.
