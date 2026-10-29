# Future-wave staging

This directory preserves the pre-existing draft shared-library objects that informed the YAML-only 2.0 redevelopment of T1584, T1587, T1585, T1683, T1588, and T1608.

The drafts were moved out of the canonical libraries on 2026-09-09 because their technique packages had not yet been authored and several files used invalid flow-style YAML containing unquoted commas. On 2026-09-10 the six candidates were rechecked against the current taxonomy and shared catalog, resolved as reuse, extend, create, split, or defer, and rewritten as canonical YAML-only 2.0 packages. These files now retain research-audit value only and are superseded by the canonical objects and the batch integration summary; they must not be referenced or copied back into the libraries.

All former reservations were synchronized to canonical objects, and the final reserved-ID list is empty. DET-000043 and MIT-000042 were extended only for the exact T1608 trusted-service object-level use that their existing logic and measures already support. T1584 and T1585 were split into DET-000049/NJA-000023/MIT-000048 and DET-000050/NJA-000024/MIT-000049 because their data requirements and control actions differ from the acquired-infrastructure and taken-over-account objects.
