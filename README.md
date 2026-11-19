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

## EDB v15 Tools — current confirmed baseline (2026-11-19)

The `EDB_v15_512k_tools.dsk` image is the protected-copy Tools baseline, explicitly promoted after the user reported that the test candidate works.

SHA-256: `5e06c643982dfd53be169a77ae160136f17dc5a5b650da77ef5f41e5bdfd863e`

### Changes since the preceding Tools baseline

- **DISKCOPY.BAS, file-by-file mode:** Replaced destination KILL-before-COPY with a staged copy to `EDBTEMP.TMP`, exact-length and content verification, native same-drive RENAME promotion, and preservation of the existing destination under `EDBOLD.BAK` until the replacement is checked.
- **INSTALL.BAS, install/backup and overwrite paths:** Applied the same staged, verified copy/replacement process, retaining the existing overwrite confirmation and separate copied/overwritten/skipped counts.
- **Recovery and capacity guards in both programs:** Check destination FAT free granules and directory slots before copying; refuse staging-name collisions; write `EDBSWAP.JRN` before replacement; support interrupted-copy rollback/recovery. A journal consumes one additional granule during a transaction.
- **INSTALL.BAS BASIC string space:** Increased the reservation from 1,024 to 2,048 bytes for the verification buffers.

Only `DISKCOPY.BAS` and `INSTALL.BAS` changed from the previous Tools baseline. The previously approved `DISKCOPY FULL` 35/40-track logic, bare DISKCOPY, FIND, COMPARE, and INSTALL empty-flip guard remain intact. The authoritative Boot disk is unchanged.

### Verification and limitations

- All 37 Tools files verified present; FAT chains and directory entries validated; all other 35 payloads unchanged.
- The user reported the candidate works and explicitly requested promotion.
- 16 interruption-state scenarios, four failure classes, and 35/40-track space arithmetic were checked in a model. Power-failure recovery and native RENAME operation under every hardware configuration have **not** been separately verified by physical interruption testing. Use disposable media for those tests.

## EDB v15 Tools — prior confirmed baseline (2026-11-19; superseded)

The previous `EDB_v15_512k_tools.dsk` image was explicitly promoted by the user after the INSTALL empty-configuration fix.

SHA-256: `d431635e259dd4a85ba3dabe9322d9bb907eee3f4688339e4175cf125bcbe488`

### Change since the preceding Tools baseline

- **INSTALL.BAS, line 155:** Added `IF L$="" THEN 180` after reading `flip.inf:3`. Empty configuration lines now use the existing invalid-configuration fallback instead of reaching `ASC("")` in the character-scanning loop.

Only `INSTALL.BAS` was modified relative to the preceding Tools baseline. All other 36 Tools files—including the confirmed DISKCOPY, FIND, and COMPARE fixes—remain unchanged. The Boot baseline is untouched.

## EDB v15 Tools — prior confirmed baseline (2026-11-19; superseded)

The current `EDB_v15_512k_tools.dsk` image was explicitly promoted by the user after the COMPARE message correction.

SHA-256: `e82134ba762443ad747fa95c67f3e597f63689b1a6c6bd4cde74f112281a412e`

### Change since the preceding Tools baseline

- **COMPARE.BAS, lines 370 and 380:** Corrected `IS NEWER.` to `IS LARGER.` when comparing file sizes. File size does not establish modification time. The actual size calculation, byte-for-byte comparison, and all other logic remain unchanged.

Only `COMPARE.BAS` was changed relative to the preceding Tools baseline. The previously confirmed DISKCOPY FULL, bare DISKCOPY, and FIND fixes are retained. The Boot image and all other 36 Tools files remain unchanged.

## EDB v15 Tools — prior confirmed baseline (2026-11-19; superseded)

The `EDB_v15_512k_tools.dsk` image is the user-confirmed v15 Tools baseline.

SHA-256: `e919ab51c9716997ea74aaecc54eca79210e0e8701b4a95b7abc3ab54854e142`

### Fixes included

- **DISKCOPY FULL:** Detects 35-track or 40-track media on both drives before the copy, uses the corresponding track count, and rejects mismatched geometries before overwriting the destination.
- **DISKCOPY without arguments:** Prevents the `?FC BUG! AT 580` caused by passing an empty string to `ASC` in the uppercase-conversion routine. An argument-free invocation can now display usage instructions.
- **FIND command-buffer protection:** Checks the command-tail length before inserting its three-byte prefix at `$FC80`. Oversized arguments now exit with `FIND: command too long` instead of overwriting adjacent memory.

Only `DISKCOPY.BAS` and `FIND.BAS` were modified within this Tools image. The user reported that the fixes work in testing and explicitly promoted the image to baseline.

**Extracted-source note:** The `extracted/` directory still reflects the original disk extraction and has not been regenerated. Its copies of `CD.BAS`, `DISKCOPY.BAS`, `FIND.BAS`, `COMPARE.BAS`, and `INSTALL.BAS` are older snapshots; the two DSK images above are the authoritative current payloads.
