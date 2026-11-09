# BATCH-TA0007-010 — T1018 single-candidate development

## Baseline and delivery scope

The fixed baseline is MITRE ATT&CK Enterprise 19.1, as recorded in `matrix.yaml`. TA0007 has 34 inventoried parent candidates. The preceding accepted batch, BATCH-TA0007-016, leaves 22 formal parents, ten native children, one exclusion, and eleven candidates awaiting admission. Its integration summary records passed evidence, semantic-content, quality, bundle, and bilingual Web gates; human domain review remains pending. The current task requests one candidate as a complete development trial, so this delivery contains only T1018 Remote System Discovery / 远程系统发现. Later candidates remain outside this delivery.

The user also named `planning/tactics/TA0011.yaml`. That plan concerns Command and Control, has a different candidate inventory, and is already at review. It is checked for context; TA0007 and its fixed-baseline Discovery inventory determine this candidate. No baseline migration is included.

## Direct object and adjacent boundaries

T1018 concerns obtaining identifiers or indications of other systems in an already accessed environment. A directory or cached host record can identify a candidate system without proving current reachability, a listening service, or successful remote access. Distinguish the operation that obtains the remote-system fact from the transport, data source, and eventual lateral-movement outcome.

The principal neighbors are NJT-0234/T1046 for remote service facts, NJT-0235/T1135 for share facts, NJT-0181/T1482 for domain-trust relationships, NJT-0236/T1040 for passive traffic observation, NJT-0233/T1654 for log enumeration, NJT-0179/T1613 for container resources, NJT-0139/T1580 for cloud infrastructure, and the still-untriaged T1016/T1049/T1673 candidates for local network configuration, local connections, and hosted virtual-machine inventory. NJT-0001 supplies structural quality and scan-variable boundary comparisons, but its reconnaissance children must not be copied into Discovery.

## Evidence, admission, and taxonomy contract

The sub-agent first recommends retain, adapt, or exclude with a candidate-specific rationale. The primary agent makes and records the admission decision before any formal NJT/NJS or semantic-library allocation. The fixed-baseline T1018 has no ATT&CK children; confirm this against the local versioned workbook. Zero ATT&CK children requires an open native-axis search rather than stopping at the first plausible axis.

Research preexisting host-knowledge reuse, read-only directory views, existing management inventories, resident-carrier execution, targeted versus broad probing, and time/source distribution. Resolve each as formal, parent-core, adjacent, or evidence-deferred. Local cache reads are not automatically passive network collection, and a command having an option does not establish adversary use or a measured stealth benefit. Every proposed native child needs a stable intentional variable, explicit trace difference, defender-observation consequence, evidence at that level, and useful defense distinction. There is no required child count.

Prefer authoritative implementation documentation and original incident research. Verify what APIs actually return, whether reads refresh caches or contact a remote system, whether values can be stale, and whether claimed telemetry includes results rather than merely commands, requests, or permissions. Separate documented capability, observed actor activity, inferred purpose, and measured effect. A fixed ATT&CK parent source anchors behavior and tactic mapping only.

## Shared libraries and canonical ownership

Only the primary agent allocates IDs or edits canonical content and shared libraries. The researcher may query `dist/catalogs/library-catalog.json`, `scripts/library_lookup.py`, and canonical YAML. New proposals use the unique prefix `B010-T1018-`; confirmed existing IDs may be cited with an exact reuse rationale. Existing source identity, incident identity, analytic logic, and mitigation measures must be examined before proposing new objects.

The sub-agent writes only `planning/runs/BATCH-TA0007-010/T1018-research-handoff.yaml` and evidence files below this batch directory. It must not edit the tactic plan, reservations, formal matrix, or shared libraries. It must not allocate formal IDs.

## Writing and defense acceptance

Use the research-handoff template and provide complete paired bilingual prose for the parent, any admitted child, material claims, and defense proposals. Compare each field with NJT-0001 for responsibility, causal completeness, calibrated uncertainty, and natural language. Definition, stealth properties, scope, scenarios, attacker prerequisites, defender observation, mechanism analysis, and limitations must remain distinct. Use as many of the allowed one-to-four paragraphs as the argument requires; no name-substitution templates.

DET proposals define the objective and subjects. NJA proposals specify validated data sources and fields, logic, correlation, false positives, blind spots, and tuning. MIT proposals supply actionable measures and target-specific use, effects, and limitations without promising to eliminate ordinary system administration. Do not assume command execution proves successful enumeration or that a directory/cache entry is an active host.

## Research and integration sequence

One sub-agent researches the one parent while the primary agent independently checks adjacent boundaries and shared identities. The primary waits for the complete handoff before admission convergence, allocation, or canonical writing. It then resolves every temporary object as reuse, extend, create, split, or defer and records taxonomy and semantic review. Scripts may serialize reviewed content, allocate IDs, build bundles, and validate; they must not originate reader prose by name substitution.

Acceptance requires shared-library deduplication, ID synchronization, `make quality`, a successful technique bundle, Review Web tests, and actual Chinese and English browser inspection of all fixed parent/child sections and linked defense objects. All admitted objects remain review pending human domain approval. Report this batch's changed objects, new NJT/NJS counts, evidence limitations, validation results, and TA0007 completed and remaining counts. This single-candidate trial does not close the tactic.
