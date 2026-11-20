# Enhanced-DOS-BASIC-for-CoCo3

Enhanced DOS BASIC for CoCo 3.

## EDB v15 — Official 512K Tools R14 baseline (2026-11-19)

- Disk image: [EDB_v15_512k_tools.dsk](EDB_v15_512k_tools.dsk) (40 tracks, 184,320 bytes).
- SHA-256: `74ee70eb476a0c5145bb8b6749d89b7e3cb285234bfed6ceabd0700026ca8bbf`
- XMM repair: `XMM.BAS` now releases XMM's physical pages before BASIC performs its 256-byte readback comparison. This addresses the previously observed unresponsive keyboard after native memory testing.
- VCC regression tests passed: `XMM` menu **N**, `XMM` menu **A**, `XMM STATUS`, and `XMM ALL`; the BASIC keyboard remained responsive after exit in all four.
- The full 256-byte verification remains enabled. `XMM6809.BIN` and the PIA keyboard routines are unchanged.
- Includes cumulative `XBENCH.BAS` return/pause/recovery improvements and the preserved XMM diagnostic paths.
- Compared with the prior repository-root Tools image, only `XMM.BAS` and `XBENCH.BAS` differ; the other 36 disk files remain byte-identical.
- Physical CoCo 3 hardware testing is still outstanding.

**Preservation:** `EDB_v15_512k_boot.dsk` and the `extracted/` historical snapshot are unchanged. `extracted/MANIFEST.json` describes that earlier extraction and is not a manifest of the current R14 Tools image.
