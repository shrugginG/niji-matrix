"""Serialize the reviewed TA0009-001 evidence and admission decisions.

The propositions below are candidate-specific editorial decisions. This script only
places them in canonical YAML and never expands prose by substituting names.
"""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
DATE = "2026-09-22"


def save(folder, filename, data):
    path = ROOT / folder / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


refs = [
    ("REF-000504", "mitre-t1560-collection-archive", "归档已收集数据，技术 T1560", "Archive Collected Data, Technique T1560", "https://attack.mitre.org/techniques/T1560/", "official-documentation", "MITRE ATT&CK", "Enterprise 19.1 parent behavior, Collection mapping, and archive detection guidance; child list is planning context only"),
    ("REF-000505", "unit42-toneshell-password-archive", "Stately Taurus 使用 TONESHELL 与口令 RAR", "Stately Taurus Abuses VSCode in Southeast Asian Espionage", "https://unit42.paloaltonetworks.com/stately-taurus-abuses-vscode-southeast-asian-espionage/", "incident-report", "Palo Alto Networks Unit 42", "TONESHELL password-protected RAR archive for exfiltration; no measured detector miss"),
    ("REF-000506", "eset-invisimole-integrated-zlib", "InvisiMole 内置 Zlib 与归档工具路径", "InvisiMole: Equipped Spyware, Undercover", "https://www.welivesecurity.com/2018/06/07/invisimole-equipped-spyware-undercover/", "threat-report", "ESET Research", "Integrated Zlib packaging of internal data and separate WinRAR tool in the observed working directory"),
    ("REF-000507", "microsoft-safe-attachments-password-archives", "Microsoft Safe Attachments 对口令归档的检查限制", "Safe Attachments in Microsoft Defender for Office 365", "https://learn.microsoft.com/en-us/defender-office-365/safe-attachments-about", "official-documentation", "Microsoft Learn", "Password-protected archive inspection limits of this mail-security product, not a universal endpoint claim"),
    ("REF-000508", "mitre-t1074-data-staged", "数据暂存，技术 T1074", "Data Staged, Technique T1074", "https://attack.mitre.org/techniques/T1074/", "official-documentation", "MITRE ATT&CK", "Enterprise 19.1 staging behavior and centralized staging's stated reduction of C2 connections"),
    ("REF-000509", "volexity-dark-halo-owa-staging", "Dark Halo 通过 OWA 暂存邮箱导出", "Dark Halo Leverages SolarWinds Compromise to Breach Organizations", "https://www.volexity.com/blog/2020/12/14/dark-halo-leverages-solarwinds-compromise-to-breach-organizations/", "incident-report", "Volexity", "Mailbox export, OWA-hosted archive path, and HTTP retrieval URL; archiving is a separate behavior"),
    ("REF-000510", "au-scattered-spider-etl-staging", "Scattered Spider 多源 ETL 与中央数据库暂存", "Scattered Spider Joint Advisory", "https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/scattered-spider", "official-documentation", "Australian Cyber Security Centre", "Actor-installed ETL tools bring multiple sources into a centralized database before exfiltration; no measured detection outcome"),
    ("REF-000511", "mitre-t1119-automated-collection", "自动收集，技术 T1119", "Automated Collection, Technique T1119", "https://attack.mitre.org/techniques/T1119/", "official-documentation", "MITRE ATT&CK", "Enterprise 19.1 parent automation behavior and Collection mapping; no ATT&CK children"),
    ("REF-000512", "bitdefender-funnydream-filepakmonitor", "FunnyDream FilePakMonitor 状态化文档收集分析", "The Chinese APT FunnyDream: FilePakMonitor Analysis", "https://www.bitdefender.com/files/News/CaseStudies/study/379/Bitdefender-Whitepaper-Chinese-APT.pdf", "threat-report", "Bitdefender", "Reverse engineering of ft.data checkpoint, twelve-hour listings, and changed-since-last-listing selection; no measured stealth outcome"),
    ("REF-000513", "aws-s3-cloudtrail-data-events", "Amazon S3 的 CloudTrail 对象数据事件", "Logging Amazon S3 API Calls Using AWS CloudTrail", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudtrail-logging-s3-info.html", "official-documentation", "Amazon Web Services", "S3 object-level GetObject/PutObject data events and enablement limits"),
    ("REF-000514", "microsoft-iis-w3c-logging-fields", "配置 IIS W3C 访问日志", "Configure Logging in IIS", "https://learn.microsoft.com/en-us/iis/manage/provisioning-and-managing-iis/configure-logging-in-iis", "official-documentation", "Microsoft Learn", "IIS W3C request log fields including client IP, URI stem, status, and byte counts"),
]

for rid, slug, zh, en, url, kind, publisher, locator in refs:
    save("references", f"{rid}-{slug}.yaml", {
        "schema_version": "1.0.0", "type": "reference", "id": rid,
        "title_zh": zh, "title_en": en, "source_type": kind,
        "authors": [publisher], "publisher": publisher, "published": None,
        "url": url, "accessed": DATE, "locator": locator, "archive_url": None,
        "credibility": "high", "notes_zh": "按标注的具体段落与结论层级引用；不能把来源的行为描述升级为实测匿迹效果。",
        "notes_en": "Use only for the stated passage and conclusion level; behavioral reporting does not establish a measured evasion outcome."
    })


def claim(cid, slug, kind, zh, en, subjects, evidence, mode, confidence):
    save("claims", f"{cid}-{slug}.yaml", {
        "schema_version": "1.0.0", "type": "claim", "id": cid, "claim_type": kind,
        "statement_zh": zh, "statement_en": en, "subject_refs": subjects,
        "evidence_refs": evidence, "evidence_mode": mode,
        "confidence": confidence, "status": "review"
    })


claim("CLM-000706", "collected-data-archive-transformation", "technique-relevance",
      "攻击者在外传前把已收集数据压缩或加密为容器或编码流，改变源文件内容在检查点的可见表示；归档行为须由源数据到产物的转换证明。",
      "Before exfiltration, an adversary compresses or encrypts collected data into a container or encoded stream, changing the representation visible at inspection; the archive behavior requires an input-to-output transformation.",
      ["NJT-0133"], ["REF-000504"], "strongly-inferred", "high")
claim("CLM-000707", "protected-archive-inspection-limit", "subtechnique-existence",
      "现场确有口令保护的外传归档；缺少口令的内容检查点无法完整恢复内部数据，但外层元数据和前序源文件访问仍可见。",
      "Password-protected archives have been used for exfiltration. An inspection point without the password cannot fully recover inner data, while outer metadata and preceding source-file access remain visible.",
      ["NJT-0133", "NJS-0133-001"], ["REF-000505", "REF-000507"], "strongly-inferred", "high")
claim("CLM-000708", "in-process-archive-lineage", "subtechnique-existence",
      "植入程序内置压缩例程可在不启动独立归档工具的情况下封装数据，因而仅靠归档工具进程名的检测无法覆盖该路径；这并不表示文件或网络痕迹消失。",
      "An implant's integrated compression routine can package data without a separate archiver process, so detection keyed only to archiver process names misses that path; file and network traces do not thereby disappear.",
      ["NJT-0133", "NJS-0133-002"], ["REF-000506", "REF-000230"], "strongly-inferred", "medium")
claim("CLM-000709", "staging-observation-scope", "technique-relevance",
      "已取得数据的中间汇聚可以减少来源主机的直接外联，但只在暂存拓扑改变防守观察时构成匿迹型数据暂存；普通中间复制不足以判断。",
      "Intermediate aggregation of acquired data can reduce direct egress from source hosts, but it is stealth-oriented staging only when the topology changes defender observation; an ordinary intermediate copy is insufficient.",
      ["NJT-0134"], ["REF-000508", "REF-000426", "REF-000509"], "strongly-inferred", "high")
claim("CLM-000710", "many-source-one-egress-graph", "subtechnique-existence",
      "多源数据在被控中间点汇聚后由少量节点取走，会把来源主机外联转为内部复制和单点外联；跨主机共享访问、目标写入与出口流量仍可重建多对一图形。",
      "When data from many sources converges on a controlled intermediate point and leaves through few nodes, direct source egress becomes internal copying plus concentrated egress; cross-host share access, target writes, and outbound flows can still reconstruct the many-to-one graph.",
      ["NJT-0134", "NJS-0134-001"], ["REF-000508", "REF-000510", "REF-000426", "REF-000509"], "strongly-inferred", "medium")
claim("CLM-000711", "automation-needs-observation-change", "technique-relevance",
      "自动化获取属于 Collection 行为，但定时任务、脚本或 API 调用本身不能证明匿迹；需证明可控范围或时机使获取痕迹和防守观察发生变化。",
      "Automated acquisition belongs to Collection, but a task, script, or API call alone does not prove stealth; a controlled scope or timing variable must alter acquisition traces and defender observation.",
      ["NJT-0135"], ["REF-000511", "REF-000512"], "strongly-inferred", "medium")
claim("CLM-000712", "filepakmonitor-change-checkpoint", "subtechnique-existence",
      "FilePakMonitor 首轮之后利用 ft.data 中的上次列举时间，仅选择该时间之后变化的文件进入后续收集轮次。",
      "After its first pass, FilePakMonitor uses the prior listing time in ft.data to select only files changed since that time for later collection passes.",
      ["NJT-0135", "NJS-0135-001"], ["REF-000512"], "directly-observed", "high")
claim("CLM-000713", "incremental-short-window-limit", "mechanism-mapping",
      "当源文件变化率较低且检测依赖短窗批量读取时，增量选择可降低后续单轮读取规模并要求跨轮重建；该匿迹效果是条件推断而非报告实测。",
      "When source-file change rates are low and detection depends on short-window bulk reads, incremental selection can reduce later per-pass volume and require cross-pass reconstruction; this stealth effect is conditional inference, not a measured outcome in the report.",
      ["NJT-0135", "NJS-0135-001"], ["REF-000512", "REF-000379"], "strongly-inferred", "medium")
claim("CLM-000714", "collection-read-telemetry-preconditions", "detection",
      "Windows 4663 仅在目标对象 SACL 和文件系统审计启用时提供主体、进程、对象与 ReadData 读取证据；云端 S3 GetObject 还须显式开启对象数据事件。",
      "Windows 4663 supplies subject, process, object, and ReadData evidence only with object SACL and file-system auditing enabled; S3 GetObject additionally requires object data events to be enabled explicitly.",
      ["NJT-0135", "NJS-0135-001"], ["REF-000379", "REF-000513"], "strongly-inferred", "high")


def case(cid, slug, zh, en, actor, desc_zh, desc_en, subjects, evidence, time_range=None):
    save("cases", f"{cid}-{slug}.yaml", {
        "schema_version": "1.0.0", "type": "case", "id": cid,
        "name_zh": zh, "name_en": en, "actor_or_campaign": actor,
        "subject_refs": subjects, "description_zh": desc_zh, "description_en": desc_en,
        "time_range": time_range, "target_sectors_zh": [], "target_sectors_en": [],
        "evidence_refs": evidence, "confidence": "high", "status": "review"
    })


case("CASE-000181", "toneshell-password-protected-archive", "TONESHELL 的口令归档", "TONESHELL Password-Protected Archive", "Stately Taurus / TONESHELL",
     "Unit 42 观察到攻击者用 TONESHELL 形成供外传的 RAR 归档，并使用每次不同的 13 字符口令。此事实支持受保护归档的现场使用；报道没有量化任何防御产品的漏报率。",
     "Unit 42 observed TONESHELL create RAR archives for exfiltration with a different 13-character password each time. This supports observed protected archival use; the report did not quantify missed detections in any defensive product.",
     ["NJT-0133", "NJS-0133-001"], ["REF-000505"])
case("CASE-000182", "invisimole-integrated-compression", "InvisiMole 的内置压缩路径", "InvisiMole Integrated Compression Path", "InvisiMole",
     "ESET 报告同时记录工作目录中的 WinRAR.exe 和恶意程序二进制内的 Zlib 例程，后者用于封装内部数据。该对照证明进程内实现路径存在，却不证明每份目标文件均无落盘归档。",
     "ESET reported both WinRAR.exe in the working directory and a Zlib routine inside the malware binary that packaged internal data. The contrast establishes an integrated path, not that every target file avoided an on-disk archive.",
     ["NJT-0133", "NJS-0133-002"], ["REF-000506"])
case("CASE-000183", "dark-halo-owa-mailbox-staging", "Dark Halo 的 OWA 邮箱导出暂存", "Dark Halo OWA Mailbox Export Staging", "Dark Halo",
     "Volexity 记录邮箱导出生成 PST，攻击者把受密码保护的归档置于 OWA 服务器可通过 HTTP 取回的路径，并构造取回 URL。这证明中间服务器与取用链，不能单独量化外联收敛比例或实际漏报。",
     "Volexity recorded a mailbox export to PST followed by a password-protected archive placed in an HTTP-retrievable path on an OWA server, with a retrieval URL. The case establishes an intermediate server and retrieval chain, not a measured egress convergence ratio or detector miss.",
     ["NJT-0134"], ["REF-000509"])
case("CASE-000184", "funnydream-stateful-file-collection", "FunnyDream 的状态化文件收集", "FunnyDream Stateful File Collection", "FunnyDream / FilePakMonitor",
     "Bitdefender 逆向分析显示 FilePakMonitor 首轮后保存上次列举时间，后续约每 12 小时只选择该时间之后变化的目标文件。报告证明增量逻辑与检查点残留，不证明具体防御系统的告警下降。",
     "Bitdefender reverse engineering showed FilePakMonitor retain the previous listing time after its first pass and select only target files changed since that time in later roughly twelve-hour passes. The report establishes incremental logic and checkpoint residue, not lower alerts in a particular defensive system.",
     ["NJT-0135", "NJS-0135-001"], ["REF-000512"])
case("CASE-000185", "scattered-spider-multisource-database-staging", "Scattered Spider 的多源数据库暂存", "Scattered Spider Multi-Source Database Staging", "Scattered Spider",
     "澳大利亚联合建议记录攻击者安装 ETL 工具，将多个数据源汇入中央数据库，为外传前准备数据。该事实证明多源汇聚，但没有量化出口节点数、告警变化或实际取走的完整对象集合。",
     "The Australian joint advisory records actor-installed ETL tools bringing several data sources into a central database before exfiltration. This establishes many-source aggregation but does not quantify outbound node count, alert changes, or the complete set eventually retrieved.",
     ["NJT-0134", "NJS-0134-001"], ["REF-000510"])


bronze = ROOT / "cases/CASE-000148-bronze-union-archive-deletion-share-teardown.yaml"
if not bronze.exists():
    matches = list((ROOT / "cases").glob("CASE-000148-*.yaml"))
    assert len(matches) == 1
    bronze = matches[0]
d = yaml.safe_load(bronze.read_text(encoding="utf-8"))
d["subject_refs"] = [ref for ref in d["subject_refs"] if ref != "NJS-0134-001"]
for subject in ("NJT-0134",):
    if subject not in d["subject_refs"]:
        d["subject_refs"].append(subject)
bronze.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


for tid, nid, decision, name_zh, name_en, evidence, confidence in [
    ("T1560", "NJT-0133", "retain", "归档已收集数据", "Archive Collected Data", ["REF-000504", "REF-000505", "REF-000506"], "high"),
    ("T1074", "NJT-0134", "adapt", "数据暂存", "Data Staged", ["REF-000508", "REF-000426", "REF-000509", "REF-000510"], "high"),
    ("T1119", "NJT-0135", "adapt", "自动收集", "Automated Collection", ["REF-000511", "REF-000512"], "medium"),
]:
    handoff = yaml.safe_load((RUN / f"{tid}-handoff.yaml").read_text(encoding="utf-8"))
    rationale = handoff["recommendation"]["rationale"]["paragraphs"]
    scope = handoff["recommendation"].get("scope_notes")
    if scope is None:
        scope = {
            "T1560": {"zh": "保留已取得数据向归档容器或编码流的转换；暂存位置、自动获取、分卷传输与后续删除分别由相邻对象处理。正式子项按内容可检查性和归档进程谱系划分，不导入 ATT&CK 的工具、库、自定义方法类别。", "en": "Retain transformation of acquired data into an archive container or encoded stream. Staging location, automated acquisition, transfer chunking, and later deletion belong to adjacent objects. Children divide content inspectability and archiver process lineage, not ATT&CK utility, library, or custom-method categories."},
            "T1119": {"zh": "适配为有证据证明获取集合或触发时机改变观察的自动收集；仅有周期任务、脚本、API 调用或文件类型过滤不构成匿迹。暂存与归档分别由 T1074 和 T1560 处理，ATT&CK 无子项亦不影响开放式 Niji 分类。", "en": "Adapt to automated collection with evidence that the acquisition set or trigger timing changes observation. A periodic task, script, API call, or extension filter alone is not stealth. Staging and archiving belong to T1074 and T1560, and the absence of ATT&CK children does not constrain open-ended Niji taxonomy."},
        }[tid]
    save("matrix/tactics/TA0009-collection/decisions", f"DEC-TA0009-{tid}.yaml", {
        "schema_version": "1.1.0", "type": "technique-decision", "id": f"DEC-TA0009-{tid}", "tactic_ref": "TA0009",
        "candidate": {"source_type": "attack", "source_attack_id": tid, "source_attack_version": "19.1", "name_en": name_en, "name_zh": name_zh},
        "decision": decision,
        "rationale_zh": "\n\n".join(p["zh"] for p in rationale), "rationale_en": "\n\n".join(p["en"] for p in rationale),
        "scope_notes_zh": scope["zh"], "scope_notes_en": scope["en"],
        "gap_statement_zh": None, "gap_statement_en": None,
        "original_attack_subtechniques_imported": False, "resulting_technique_ref": nid,
        "evidence_refs": evidence, "confidence": confidence,
        "review": {"status": "review", "authors": ["Niji Matrix Research"], "reviewers": [],
                   "review_notes_zh": "已完成首批准入与跨技术边界复核；机器与双语 Web 门禁通过后维持 review，待人工领域评审。",
                   "review_notes_en": "First-batch admission and cross-technique boundaries were reviewed; keep in review after machine and bilingual Web gates pending human domain review."}
    })

print("Serialized 11 references, 9 claims, 5 cases, 3 decisions; extended CASE-000148")
