# BATCH-TA0007-006 — single-candidate Group Policy Discovery pilot

## Scope and delivery control

The current user request is interpreted as TA0007 Discovery, following the immediately preceding TA0007 audit and the explicit TA0007 scope and reporting requirements. Its references to Persistence and TA0011 are template remnants. TA0011.yaml was inspected and is already in review with its gap analysis complete; it does not define the remaining Discovery inventory. The user explicitly limited this delivery to one candidate and authorized a research sub-agent.

The fixed baseline remains MITRE ATT&CK Enterprise 19.1 in matrix.yaml. The complete TA0007 program has 34 parent candidates, 12 completed decisions, 11 formal techniques, four formal native children, and 22 candidates awaiting TA0007 admission before this batch. The only delivery candidate is WORK-TA0007-T1615, Group Policy Discovery / 组策略发现, fixed inventory position 13. T1680 and T1654 are moved from the previously planned three-candidate batch 006 to planned batch 015; they remain untriaged. No subsequent candidate enters canonical authoring in this pilot.

Batch 003's recorded candidate, evidence, bilingual, bundle and Web gates passed. The immediately preceding audit in this chat reran make quality successfully on the current preflight content: 4,202 objects, zero content/planning errors or warnings, zero exact or unresolved possible duplicates, and 12 infrastructure tests. Reserved-ID inspection was empty. A fresh preflight is also run for this delivery before canonical integration. Existing unrelated TA0006 edits remain owned by their existing work and must be preserved.

## Candidate anchor and boundaries

T1615's direct object is information about configured or effective Group Policy, including policy content, application scope, links and settings. Discovery of policy information is distinct from changing policy (T1484.001), stealing authentication secrets from policy files (T1552.006), general directory/file enumeration (T1083), general account/group discovery (T1087/T1069), trust topology discovery (T1482), and subsequent persistence or execution through policy. Reading normal administrative information is not by itself proof of evasion intent.

Preserve the fixed parent behavior unless an evidence-supported Niji scope adaptation is needed. The admission must precede official NJT/NJS allocation. Examine existing canonical Group Policy modification, SYSVOL secret acquisition, directory discovery, and defense objects before proposing new shared objects. Never extend an object's scope solely because a name or artifact overlaps.

## Taxonomy and evidence requirements

ATT&CK Enterprise 19.1 T1615 has zero ATT&CK children. This is ordinary breadth context, not a reason to stop searching or a Niji child quota. Independently examine at least policy reads through the directory/file planes, preexisting local policy/resultant-policy copies, scoped versus broad queries, and timing or legitimate-client provenance. Formalize only a stable, attacker-controlled stealth variable with a supported trace change, defender-observation difference, credible prerequisites, and distinct defense value. A justified empty or deferred Niji taxonomy is acceptable.

The fixed ATT&CK page establishes parent behavior and mapping; material stealth, child-existence, data-availability and mitigation-effect conclusions require primary technical documentation or incident evidence at their own conclusion level. Distinguish direct incident observations, documented platform capabilities, analytic inferences and hypotheses. Do not equate absence of a default Windows event with invisibility, or assume that every directory/file read is logged. Keep read-only versus mutation audit events explicit.

## Research delegation contract

One sub-agent researches only T1615 and returns a structured handoff based on planning/templates/technique-research-handoff.yaml in this directory as T1615-research-handoff.yaml. Use temporary prefix B006-T1615 for new reference, claim, case, child and defense candidates. Confirmed existing library IDs may be cited. The sub-agent must read the project skill, relevant references/specifications, NJT-0001 exemplar, and this brief; browse primary sources; and provide bilingual proposed content, retain/adapt/exclude recommendation, taxonomy review, exact source URLs, evidence strength, implementable DET/NJA suggestions and target-specific MIT suggestions. It may write research material only below this batch directory. It must not allocate official IDs or modify canonical matrix, shared libraries, reservations or tactic plans.

The primary agent waits for the complete research handoff before deciding admission, cross-technique scope, taxonomy and shared-library identity. Only the primary agent allocates and writes official objects. Scripts may serialize reviewed prose and perform mechanical operations, but may not originate semantic content through name substitution.

## Acceptance and reporting

Compare every admitted parent and child with NJT-0001 by field responsibility, causal completeness, evidence calibration, residual observations and bilingual naturalness. Run shared-library identity checks, ID sync, make quality, bundle build, npm test in the Review Web, and actual Chinese/English page inspection including defense expansion and raw YAML. Leave formal content and the batch at review pending human domain review. Record actual check results in integration-summary.yaml and report this delivery's decision, new NJT/NJS and shared objects, validation, and TA0007 completed/remaining counts separately from the tactic's still-open gap analysis.
