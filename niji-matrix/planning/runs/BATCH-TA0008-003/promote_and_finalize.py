#!/usr/bin/env python3
from pathlib import Path
import glob,yaml
ROOT=Path(__file__).resolve().parents[3]
ids=["NJT-0183","NJS-0183-001","NJS-0183-002","DET-000211","NJA-000257","NJA-000258",
     *[f"CLM-{i:06d}" for i in range(900,905)],*[f"CASE-{i:06d}" for i in range(263,266)],
     "MIT-000052","MIT-000172","CLM-000507","CASE-000104"]
for id in ids:
 matches=[]
 for folder in ["matrix/tactics","detections","analytics","mitigations","claims","cases"]:
  matches+=glob.glob(str(ROOT/folder/"**"/(id+"-*.yaml")),recursive=True)
  matches+=glob.glob(str(ROOT/folder/"**"/(id+"-*")/"technique.yaml"),recursive=True)
  matches+=glob.glob(str(ROOT/folder/"**"/(id+"-*")/"subtechnique.yaml"),recursive=True)
 matches=list(dict.fromkeys(matches));assert len(matches)==1,(id,matches)
 p=Path(matches[0]);d=yaml.safe_load(p.read_text())
 if "lifecycle" in d:d["lifecycle"]["status"]="review"
 else:d["status"]="review"
 p.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False,width=120))
p=ROOT/"matrix"/"tactics"/"TA0008-lateral-movement"/"decisions"/"DEC-TA0008-T1021.yaml"
d=yaml.safe_load(p.read_text());d["review"].update(status="review",
 review_notes_zh="证据、8 子项覆盖、两遍原生分类、双语正文、专用防御、查重、质量、Bundle 和 Web 定向门禁通过，等待人工领域评审。",
 review_notes_en="Evidence, eight-child coverage, two-pass native taxonomy, bilingual prose, targeted defense, deduplication, quality, bundle, and focused Web gates pass pending human domain review.")
p.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False,width=120))
# Plan stage; T1550 research remains ready but not canonical.
p=ROOT/"planning"/"tactics"/"TA0008.yaml";d=yaml.safe_load(p.read_text())
for b in d["batches"]:
 if b["id"]=="BATCH-TA0008-003":b["status"]="review"
 if b["id"]=="BATCH-TA0008-004":b["status"]="active"
for x in d["work_items"]:
 if x["source_attack_id"]=="T1021":
  x["stage"]="review";x["notes_zh"]="adapt；NJT-0183 以角色贴合的远程管理路径和中继来源远程会话间接化建立两项 Niji 原生 NJS；固定 8 子项覆盖表、第二遍 taxonomy、质量、Bundle 与定向 Web 门禁通过，等待人工领域评审。";x["notes_en"]="Adapt; NJT-0183 establishes two native children for a role-conforming remote administration path and intermediary-origin session indirection. The fixed eight-child coverage table, second taxonomy pass, quality, bundle, and focused Web gates pass pending human domain review."
 if x["source_attack_id"]=="T1550":x["stage"]="researching"
p.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False,width=120))
summary={"schema_version":"1.0.0","type":"batch-integration-summary","batch_ref":"BATCH-TA0008-003","status":"review",
"delivery_control":{"overall_candidate_count":9,"batch_candidate_count":1,
"batch_size_rationale":{"zh":"T1021 固定基线有 8 个实现子项，作为复杂单候选批次完成覆盖表和第二遍 taxonomy；T1550 只并行研究，未提前污染正式 ID。","en":"T1021 has eight fixed-baseline implementation children and was handled as a complex single-candidate batch with explicit coverage and a second taxonomy pass. T1550 research ran in parallel without early canonical IDs."},"previous_batch_gate_passed":True},
"candidate_results":[{"source_attack_id":"T1021","decision":"adapt","technique_ref":"NJT-0183","subtechnique_refs":["NJS-0183-001","NJS-0183-002"]}],
"shared_library_resolutions":{"reuse":["REF-000278","REF-000289","REF-000377","REF-000598","REF-000604","REF-000614","CLM-000507","CASE-000104","MIT-000052","MIT-000172"],"extend":["CLM-000507","CASE-000104","MIT-000052","MIT-000172"],"create_ranges":{"references":"REF-000842..REF-000848","claims":"CLM-000900..CLM-000904","cases":"CASE-000263..CASE-000265","detection_strategies":"DET-000211","detection_analytics":"NJA-000257..NJA-000258","mitigations":None,"relationships":None}},
"deferred_hypotheses":["攻击者自有远程会话长寿化、低交互、分时连接及 service-broker 子轴缺结论级证据或独立防御差异。"],"duplicate_resolution_refs":["NJT-0055/NJT-0183","NJS-0055-002/NJS-0183-001","NJS-0168-002/NJS-0183-002","NJS-0151-001/NJS-0183-002"],
"semantic_validation":{"candidate_level_gates_passed":True,"conclusion_level_evidence_passed":True,"njt_0001_field_responsibility_reviewed":True,"bilingual_argument_depth_passed":True,"boilerplate_review_passed":True,"taxonomy_breadth_reviewed":True,"attack_breadth_gap_explained":True,"canonical_prose_bulk_generated":False},
"validation":{"matrix_objects":3089,"schema_errors":0,"schema_warnings":0,"unresolved_duplicate_candidates":0,"reviewed_similarity_resolutions":4,"infrastructure_tests":12,"web_tests":None,"focused_web_tests":2,"web_api_issues":None,"bundles_built":["NJT-0183"]},
"review_notes_zh":"T1021 经 adapt 形成 NJT-0183 与两项按内部管理关系贴合、中继来源间接化划分的原生 NJS；8 个 ATT&CK 子项只作宽度并完成逐项覆盖和第二遍 taxonomy。新建 1 DET 与 2 NJA，扩展 MIT-000052/172。矩阵、规划、查重、正文审计、12 项基础设施测试、Bundle 与 2 项定向 Web 测试通过；完整 Web/API 将在 review 状态复测。等待人工领域评审。",
"review_notes_en":"T1021 was adapted as NJT-0183 with two native children for internal management-relationship conformity and intermediary-origin indirection. Eight ATT&CK children remain breadth context with explicit coverage and a second taxonomy pass. One DET and two NJA were created and MIT-000052/172 extended. Matrix, planning, deduplication, prose audit, twelve infrastructure tests, bundle, and two focused Web tests pass; full Web/API will be rerun in review state. Human domain review is pending."}
(ROOT/"planning"/"runs"/"BATCH-TA0008-003"/"integration-summary.yaml").write_text(yaml.safe_dump(summary,allow_unicode=True,sort_keys=False,width=120))
print("promoted T1021 package and activated T1550 formal batch")
