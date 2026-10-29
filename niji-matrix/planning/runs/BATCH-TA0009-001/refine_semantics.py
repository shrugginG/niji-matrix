"""Apply primary-reviewer evidence and boundary refinements to drafted packages."""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "matrix/tactics/TA0009-collection/techniques"


def paragraph(zh, en):
    return {"paragraphs": [{"zh": zh, "en": en}]}


def read(pattern):
    matches = list(BASE.glob(pattern))
    assert len(matches) == 1, (pattern, matches)
    return matches[0], yaml.safe_load(matches[0].read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


path, archive = read("NJT-0133-*/technique.yaml")
archive["evidence"]["reference_refs"] = list(dict.fromkeys(archive["evidence"]["reference_refs"] + ["REF-000512", "REF-000426"]))
archive["stealth_mechanisms"][1]["evidence_refs"] = list(dict.fromkeys(archive["stealth_mechanisms"][1]["evidence_refs"] + ["REF-000512"]))
archive["research"]["limitations"] = {"paragraphs": [
    {"zh": "ATT&CK 固定版锚定归档行为，却不能单独证明 Niji 子项的规避意图。Unit 42 的口令 RAR、ESET 的内置 Zlib 与外部 WinRAR，以及 Bitdefender 直接把收集文件压缩为 pak 产物的分析分别支持不同实现。进程内归档的检测差异具有明确技术基础，但没有事件级资料量化告警下降，故保持中等置信度；暂存、分卷和删除不能被归入同一个归档机理。",
     "en": "The ATT&CK technique description anchors archival behavior but does not alone establish evasive intent for these variants. Unit 42's passworded RAR, ESET's integrated Zlib and external WinRAR, and Bitdefender's direct compression of collected files into a pak artifact support distinct implementation facts. The in-process detection difference has a clear technical basis, but no event-level evidence quantifies reduced alerts, so it remains medium confidence. Staging, splitting, and deletion must not be folded into one archive mechanism."},
    {"zh": "Microsoft Safe Attachments 的口令限制仅针对该邮件检查产品；不能据此宣称所有端点和网关都无法识别外层归档。若 Windows 文件读取审计没有开启、归档流从不落盘或产物被多次重写，源到产物的防御关联会不完整。正式分析需要在实际环境验证源文件读取、产物解析状态与出口对象之间的键。",
     "en": "Microsoft Safe Attachments' password limitation applies to that mail-inspection product and does not imply that all endpoints or gateways lose outer-archive visibility. Source-to-output correlation is incomplete when Windows file-read audit is absent, the archive stream never lands on disk, or output is repeatedly rewritten. The analytic must validate keys among source reads, parse status, and outbound objects in the actual environment."}
]}
write(path, archive)

path, inprocess = read("NJT-0133-*/subtechniques/NJS-0133-002-*/subtechnique.yaml")
inprocess["stealth_mechanisms"][0]["evidence_refs"] = list(dict.fromkeys(inprocess["stealth_mechanisms"][0]["evidence_refs"] + ["REF-000512"]))
inprocess["evidence"]["reference_refs"] = list(dict.fromkeys(inprocess["evidence"]["reference_refs"] + ["REF-000512"]))
inprocess["research"]["limitations"] = paragraph(
    "ESET 的内置 Zlib 主要描述内部数据与注册表材料；Bitdefender 直接显示收集文件在恶意程序内形成压缩 pak。两者共同支持无独立归档工具的实现路径，但均未实测对进程名告警的规避率。源读取审计缺失或正常应用集成归档时，应降低结论置信度。",
    "ESET's integrated Zlib passage chiefly describes internal data and Registry material, while Bitdefender directly shows collected files compressed into a pak by malware code. Together they support a path without a separate archive utility, but neither measures evasion of process-name alerts. Missing source-read audit or legitimate integrated packaging lowers confidence.")
write(path, inprocess)

path, staging = read("NJT-0134-*/technique.yaml")
staging["definition_and_concept"] = {"paragraphs": [
    {"zh": "匿迹型数据暂存是攻击者在已取得数据之后、最终取走或外传之前，将多个来源的内容写入受控中间节点，并改变数据来源与出口节点之间可见关系的 Collection 技术。直接对象是暂存拓扑及其源、落点、后继取用链，而不是文件类型、归档格式或某个本地或远程位置标签。集中点可让攻击者从少数节点取走数据，而来源主机只显示内部复制。",
     "en": "Stealth-Oriented Data Staging is a Collection technique in which an adversary writes acquired content from several origins to a controlled intermediate node before final retrieval or exfiltration, changing the visible relationship between sources and egress. Its direct object is the staging topology and the source, destination, and later-use chain, not file type, archive format, or a local-versus-remote label. Aggregation can let the actor retrieve data from few nodes while source hosts show internal copying."},
    {"zh": "普通暂存只是数据处理步骤；本适配技术要求攻击者控制的暂存安排使单一观察面的判断发生变化。T1119 管理数据的重复自动获取，T1560 管理已收集数据的归档转换，真正的外传由后继战术描述。三者可以同现，但对暂存的判断必须依赖源到中间点再到取用者的独立证据。",
     "en": "Ordinary staging is a data-processing step; this adapted technique requires an attacker-controlled arrangement that changes what one defensive vantage can conclude. T1119 governs repeated automated acquisition, T1560 governs archival transformation of collected data, and later exfiltration belongs to its own tactic. They may coexist, but a staging verdict requires independent evidence linking sources to the intermediate point and then to retrieval."}
]}
staging["stealth_characteristics"] = {"paragraphs": [
    {"zh": "多台受影响主机的数据先进入同一中间节点时，出口传感器只见到该节点的少量取用或外联，难从外联主机清单估计真正的来源数量。攻击者把原本分散的直接外联痕迹转成内部共享访问和目标文件写入；这些痕迹没有消失，并可能在汇聚节点形成异常的写入峰值。",
     "en": "When data from several affected hosts first enters one intermediate node, an egress sensor sees only a few retrievals or outbound connections from that node and cannot estimate all source hosts from the egress list. The adversary trades dispersed direct egress for internal share access and target-file writes. Those traces remain and may create an unusual write spike at the aggregation point."},
    {"zh": "匿迹收益取决于防守方是否把内部文件与网络事件连接到最终出口。如果共享访问、目标创建和取回请求可按主机、对象和时间关联，暂存反而呈现多源汇入、少点外联的明显图形。目录位置、加密归档或快速清理可能另有作用，却不构成本批已证实的出口汇聚子项边界。",
     "en": "The stealth benefit depends on whether defenders join internal file and network events to final egress. With share access, target creation, and retrieval requests linked by host, object, and time, staging instead forms a conspicuous many-source-inbound, few-node-outbound graph. Directory location, encrypted archives, or rapid cleanup may have other effects but do not define the egress-convergence child established in this batch."}
]}
staging["scope_boundary_definition"] = {"paragraphs": [
    {"zh": "纳入已取得数据被多个来源送往攻击者可控中间节点，且后续从少数节点取用导致来源主机的直接外联观察发生变化的行为。至少应证实源侧复制、目标写入和后继取用中的两个相邻环节；只有目录存在或共享权限检查、没有成功写入时，不能宣称完成汇聚。",
     "en": "Include acquired data sent from multiple sources to an attacker-controlled intermediate node where later retrieval through few nodes changes observation of direct source-host egress. At least two adjacent stages among source copying, destination creation, and later retrieval should be established. A directory's existence or a share permission check without successful writes does not establish completed convergence."},
    {"zh": "批准备份、邮件迁移、集中 ETL 和合法数据仓库可形成相似多源拓扑，须结合身份、任务范围、落点和取用者判断。归档容器属于 T1560，自动取得数据属于 T1119，外传后的清理属于相邻防御规避技术。隐藏目录、Web 资源路径与注册表缓冲作为未收敛轴保留研究，不由其外观单独认定本子项。",
     "en": "Approved backup, mailbox migration, centralized ETL, and legitimate data warehouses can form similar many-source topology and require comparison with identity, job scope, destination, and retriever. Archive containers belong to T1560, automated acquisition to T1119, and post-exfiltration cleanup to adjacent defense evasion. Hidden paths, web-resource paths, and Registry buffers remain research axes whose appearance alone does not establish this child."}
]}
staging["application_scenarios_and_threat_model"] = {
    "application_scenarios": paragraph(
        "攻击者取得文件共享、邮箱或数据库访问后，可利用已控制的文件或 Web 服务器作为中间汇聚点，再从该点集中取走数据。Volexity 的 OWA 邮箱导出链和 SecureWorks 的 BRONZE UNION 中间服务器链证明这种路径可在实际入侵中出现；澳大利亚联合建议还记录 Scattered Spider 使用 ETL 将多源数据汇入中央数据库。公开材料没有量化这些事件中的告警下降。",
        "After gaining access to shares, mailboxes, or databases, an adversary may use a controlled file or web server as an intermediate aggregation point and retrieve data from there. Volexity's OWA mailbox-export chain and SecureWorks' BRONZE UNION intermediate-server chain show such paths in intrusions; an Australian joint advisory also records Scattered Spider using ETL to bring many sources into a central database. The public reports do not quantify reduced alerts in those incidents."),
    "threat_model": {
        "attacker_model": paragraph(
            "攻击者需要读取多个来源、写入同一中间点并再次取用的权限，通常还需跨主机或跨服务移动数据。其可控制汇聚节点、写入账户和取走时机，却承担内部复制增加、暂存容量与权限暴露的成本；若只控制一台主机，便无法成立多源收敛变量。",
            "The adversary needs authority to read multiple sources, write one intermediate point, and retrieve from it, often across hosts or services. The actor may control the aggregation node, writing identities, and retrieval time but incurs more internal copying, storage demand, and permission exposure. Control of only one source host does not establish a many-source convergence variable."),
        "defender_model": paragraph(
            "防守方可从目标服务器的共享访问、文件创建、Web 请求和网络流量恢复链条，但单看出口会低估源主机数量。Windows 5145 是访问检查而非成功写入证明，需要与文件创建事件连接；如果中间节点通过非 SMB 方式接收数据，须另有对应传输日志。身份、资产和文件键跨设备不一致时，结论应保持为部分谱系。",
            "Defenders can recover the chain through share access, file creation, web requests, and network flows at the destination server, but an egress-only view undercounts source hosts. Windows 5145 is an access check rather than proof of a successful write and needs a file-create join. Other transfer logs are needed when the intermediate point receives data outside SMB. Inconsistent identity, asset, or file keys across devices leave only partial lineage.")}}
staging["research"]["limitations"] = {"paragraphs": [
    {"zh": "ATT&CK 固定版直接说明集中暂存可减少到 C2 的连接，但没有给出特定事件中的来源数、出口数或告警结果。Volexity、SecureWorks 与澳大利亚联合建议证明中间点或多源数据库的使用，无法单独证明每次选择都以规避检测为主观目的。案例还包含归档、改名和外传步骤，效果不得全部归因于暂存。",
     "en": "The fixed ATT&CK baseline explicitly states that central staging can reduce C2 connections but gives no incident-specific source count, egress count, or alert outcome. Volexity, SecureWorks, and the Australian joint advisory establish intermediate points or a multi-source database but do not prove that every choice was subjectively intended to evade detection. The cases also include archiving, renaming, and exfiltration, whose effects cannot all be attributed to staging."},
    {"zh": "多源到单点也是正常备份、邮件迁移和 ETL 的常见形态。共享审计或文件创建数据缺失时，不能仅凭 5145 的权限检查判断成功暂存；Web 请求可证明取用尝试，但不一定证明完整内容已离开网络。低审查命名空间与非文件缓冲仍有研究线索，因与既有正式对象边界未收敛而未设为本批 NJS。",
     "en": "Many-source-to-one-node paths are also ordinary for backup, mailbox migration, and ETL. Without share audit or file-create data, a 5145 permission check alone cannot prove successful staging; a web request may show retrieval attempt without proving complete transfer. Low-scrutiny namespaces and non-file buffers remain research leads and were not made Niji children in this batch because their boundaries with existing formal objects have not converged."}
]}
write(path, staging)

path, ref = next((p, yaml.safe_load(p.read_text(encoding="utf-8"))) for p in (ROOT / "references").glob("REF-000512-*.yaml"))
ref["locator"] = "FilePak packaging of collected documents with zLib into pak/pak.z (pp. 14–15); FilePakMonitor ft.data checkpoint and changed-since-last-listing collection (pp. 17–18)"
write(path, ref)

path, claim = next((p, yaml.safe_load(p.read_text(encoding="utf-8"))) for p in (ROOT / "claims").glob("CLM-000708-*.yaml"))
claim["evidence_refs"] = ["REF-000506", "REF-000512", "REF-000230"]
write(path, claim)

path, analytic = next((p, yaml.safe_load(p.read_text(encoding="utf-8"))) for p in (ROOT / "analytics").glob("NJA-000153-*.yaml"))
analytic["evidence_refs"] = list(dict.fromkeys(analytic["evidence_refs"] + ["REF-000512"]))
write(path, analytic)

path, strategy = next((p, yaml.safe_load(p.read_text(encoding="utf-8"))) for p in (ROOT / "detections").glob("DET-000146-*.yaml"))
strategy["evidence_refs"] = list(dict.fromkeys(strategy["evidence_refs"] + ["REF-000512"]))
write(path, strategy)

print("Applied primary reviewer refinements to archive and staging evidence and boundaries")
