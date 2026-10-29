"""Synchronize the reviewed five-candidate result and TA0011 machine closure state."""

from pathlib import Path
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
path = ROOT / "planning/tactics/TA0011.yaml"
plan = yaml.safe_load(path.read_text())
RESULT = {
    "T1571": ("NJT-0221", "adapt；新建端口预期语义错配父级，零 NJS。四层证据门要求真实语义、当地服务预期、防守差分及后继 C2；公开案例不能单独证明每个目标的策略效果。", "Adapt; NJT-0221 models port-expectation semantic mismatch with no children. Its four-part evidence gate requires actual semantics, local service expectation, defensive differential, and successor C2; public cases alone do not prove each victim's policy effect."),
    "T1572": ("NJT-0222", "retain；新建嵌套协议会话隧道及三项原生 NJS，分别改变端点关系、内层流到外层连接的基数和跨事务连续性。", "Retain; NJT-0222 and three native children cover endpoint relationship, inner-flow to outer-connection cardinality, and continuity across outer transactions."),
    "T1573": ("NJT-0223", "adapt；新建攻击者密钥控制通道保护及三项原生 NJS，按可复用秘密、运行时秘密与嵌套检查边界划分；对称/非对称未直接导入。", "Adapt; NJT-0223 and three native children cover reusable secrets, runtime-scoped secrets, and the nested inspection boundary; symmetric and asymmetric ATT&CK labels were not imported."),
    "T1659": ("NJT-0052", "retain；跨战术复用并逐字段重写 NJT-0052 和三项既有 NJS，补充持续 C2 的独立证据与 DET/NJA/MIT；竞速响应的 C2 用途保持假设。", "Retain; reused and field-by-field rewrote NJT-0052 and its three existing children for both tactics, with independent continuing-C2 evidence and DET/NJA/MIT. C2 use of racing responses remains a hypothesis."),
    "T1665": ("NJT-0224", "adapt；新建选择性 C2 基础设施暴露及两项原生 NJS，按请求资格和防守观察者抑制划分；操作时窗暴露待独立证据。", "Adapt; NJT-0224 and two native children distinguish request qualification from defender-observer suppression; operational-window exposure awaits independent evidence."),
}

assert plan["attack_baseline"] == {"domain": "enterprise-attack", "version": "19.1"}
assert len(plan["work_items"]) == 18
for batch in plan["batches"]:
    if batch["id"] == "BATCH-TA0011-005":
        batch["status"] = "review"
for item in plan["work_items"]:
    tid = item["source_attack_id"]
    if tid in RESULT:
        parent, notes_zh, notes_en = RESULT[tid]
        item["decision_ref"] = f"DEC-TA0011-{tid}"
        item["resulting_technique_ref"] = parent
        item["stage"] = "review"
        item["notes_zh"] = notes_zh
        item["notes_en"] = notes_en
plan["status"] = "review"
plan["gap_analysis"] = {
    "status": "complete",
    "notes_zh": "固定 Enterprise 19.1 的 18 个父候选全部完成准入和正式归宿；开放搜索覆盖 C2 消息、承载、路径、状态、端点、授权、密码、内容注入和基础设施暴露，未发现兼具独立父行为、结论级证据与差异化防御的额外 Niji 原生父级。T1665 操作时窗等证据不足的轴保留在研究层，不伪装为已关闭的子项。人工领域评审仍未进行。",
    "notes_en": "All eighteen fixed Enterprise 19.1 parent candidates have admission decisions and formal outcomes. Open search covered C2 messages, carriage, paths, state, endpoints, authorization, cryptography, content injection, and infrastructure exposure and found no additional Niji-native parent with an independent behavior, conclusion-level evidence, and distinct defense. Evidence-limited axes such as T1665 operational-window exposure remain in research. Human domain review is still pending.",
}
plan["review"] = {"taxonomy": "passed", "evidence": "passed", "bilingual": "passed", "reviewers": []}
path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=120))
print("TA0011 plan: 18/18 decisions, status review, native-gap assessment recorded")
