# Enhanced-DOS-BASIC-for-CoCo3

Enhanced DOS BASIC for CoCo 3.

## Baseline record

A disk image becomes an authoritative EDB baseline only after the user explicitly confirms it. Every confirmed baseline update is documented here with its date, changed components, and SHA-256. Unrelated files are preserved.

## EDB v15 Boot — confirmed baseline (2026-11-19)

The `EDB_v15_512k_boot.dsk` image replaces the previous GitHub Boot image with the user-approved, user-confirmed v15 Boot baseline.

SHA-256: `8bbda19306f26a92b4c3ac18a7aa50fba3ddc35d13224e166635b55c238e381d`

### Fix included

- **CD.BAS startup buffer guard:** Added BASIC line `3543 IF LEN(CA$)>63 THEN 3560` immediately before the saved color preference is copied into the `$FC80` command buffer. A malformed or unusually long saved color setting now skips the unsafe copy. Normal color restoration and drive-changing behavior remain unchanged.

Only `CD.BAS` was modified within this Boot image; all other 48 disk files were verified unchanged against the authoritative user-supplied Boot source. The user explicitly promoted this candidate to baseline.

## EDB v15 Tools — confirmed baseline (2026-11-19)

The `EDB_v15_512k_tools.dsk` image is the user-confirmed v15 Tools baseline.

SHA-256: `e919ab51c9716997ea74aaecc54eca79210e0e8701b4a95b7abc3ab54854e142`

### Fixes included

- **DISKCOPY FULL:** Detects 35-track or 40-track media on both drives before the copy, uses the corresponding track count, and rejects mismatched geometries before overwriting the destination.
- **DISKCOPY without arguments:** Prevents the `?FC BUG! AT 580` caused by passing an empty string to `ASC` in the uppercase-conversion routine. An argument-free invocation can now display usage instructions.
- **FIND command-buffer protection:** Checks the command-tail length before inserting its three-byte prefix at `$FC80`. Oversized arguments now exit with `FIND: command too long` instead of overwriting adjacent memory.

Only `DISKCOPY.BAS` and `FIND.BAS` were modified within this Tools image. The user reported that the fixes work in testing and explicitly promoted the image to baseline.

**Extracted-source note:** The `extracted/` directory still reflects the original disk extraction and has not been regenerated. Its copies of `CD.BAS`, `DISKCOPY.BAS`, and `FIND.BAS` are older snapshots; the two DSK images above are the authoritative current payloads.
