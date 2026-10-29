"""Assemble reviewed candidate-specific prose into formal TA0009 packages."""

from copy import deepcopy
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
DATE = "2026-09-22"
LIFECYCLE = {"status": "draft", "version": "1.0.0", "created": DATE, "modified": DATE,
             "contributors": ["Niji Matrix Research"], "reviewers": []}


def block(zh, en):
    return {"paragraphs": [{"zh": zh, "en": en}]}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


handoffs = {tid: yaml.safe_load((RUN / f"{tid}-handoff.yaml").read_text(encoding="utf-8"))
            for tid in ("T1560", "T1074", "T1119")}

refmap = {
    "T1560_ATTACK_PARENT_19_1": "REF-000504", "T1560_TONESHELL_PASSWORD": "REF-000505",
    "T1560_MS_PASSWORD_SCAN": "REF-000507", "T1560_ESET_INVISIMOLE": "REF-000506",
    "T1560_ATTACK_CHILD_LIBRARY_19_1": "REF-000504", "T1560_SYSMON_EVENTS": "REF-000230",
    "T1074_REF_ATTACK_PARENT": "REF-000508", "T1074_REF_ATTACK_REMOTE": "REF-000508",
    "T1074_REF_SECUREWORKS": "REF-000426", "T1074_REF_VOLEXITY": "REF-000509",
    "T1074_REF_SCATTERED": "REF-000510", "T1074_REF_MS_4663": "REF-000379",
    "T1074_REF_MS_SYSMON": "REF-000230", "T1074_REF_MS_5145": "REF-000474",
    "T1119_REF_ATTACK19": "REF-000511", "T1119_REF_BITDEFENDER_FUNNYDREAM": "REF-000512",
    "T1119_REF_MS_4663": "REF-000379", "T1119_REF_AWS_S3_EVENTS": "REF-000513",
}


def mechanisms(items):
    output = []
    for source in items:
        value = {k: deepcopy(source[k]) for k in ("mechanism_ref", "role", "summary", "analysis", "confidence")}
        value["evidence_refs"] = list(dict.fromkeys(refmap[k] for k in source.get("evidence_keys", []) if k in refmap))
        if not value["evidence_refs"]:
            raise ValueError(f"Missing evidence: {source}")
        output.append(value)
    return output


def defense(strategies, mitigation):
    return {"detections": {"coverage": "available", "strategy_refs": strategies},
            "mitigations": {"coverage": "available", "mitigation_refs": [mitigation]}}


def formal_parent(tid, nid, slug, name, summary, children, taxonomy, claim_refs, case_refs,
                  reference_refs, strategies, mitigation, origin):
    handoff = handoffs[tid]
    content = handoff["proposed_content"]
    root = ROOT / "matrix/tactics/TA0009-collection/techniques" / f"{nid}-{slug}"
    record = {
        "schema_version": "2.0.0", "type": "technique", "id": nid, "name": name,
        "summary": summary, "aliases": [],
        "classification": {"tactic_refs": ["TA0009"],
                           "origin": {"kind": origin, "source_attack_id": tid, "source_attack_version": "19.1"},
                           "decision_ref": f"DEC-TA0009-{tid}"},
        "definition_and_concept": deepcopy(content["definition_and_concept"]),
        "stealth_characteristics": deepcopy(content["stealth_characteristics"]),
        "scope_boundary_definition": deepcopy(content["scope_boundary_definition"]),
        "application_scenarios_and_threat_model": deepcopy(content["application_scenarios_and_threat_model"]),
        "stealth_mechanisms": mechanisms(content["stealth_mechanisms"]),
        "subtechnique_taxonomy": {"narrative": taxonomy, "coverage": "established", "subtechnique_refs": children},
        "defense": defense(strategies, mitigation),
        "evidence": {"claim_refs": claim_refs, "case_refs": case_refs, "reference_refs": reference_refs},
        "research": {"limitations": deepcopy(handoff["research"]["limitations"])},
        "lifecycle": deepcopy(LIFECYCLE),
    }
    if tid == "T1074":
        # The namespace child is deferred. Keep only the established egress mechanism
        # in the formal parent until its boundary with NJT-0114 is resolved.
        record["stealth_mechanisms"] = record["stealth_mechanisms"][:1]
        record["stealth_mechanisms"][0]["summary"] = {
            "zh": "通过内部多源汇聚减少来源主机的直接外联痕迹",
            "en": "Reduce direct source-host egress traces through internal many-source aggregation"}
        record["stealth_mechanisms"][0]["analysis"] = block(
            "攻击者将多台来源主机的数据先复制到受控中间点，再从该点取走。只观察外联的防守方会把多个来源压缩为一个出口节点，难以直接估计受影响主机数量；共享访问、目标写入和内部传输没有消失。跨主机与出口关联能重建多源汇入、少点外联的图形，因此收益取决于观察面之间的关联缺口。",
            "The adversary first copies data from several source hosts to a controlled intermediate point and then retrieves it there. A defender watching egress alone sees many sources collapsed into one outbound node and cannot directly estimate the affected host count. Share access, destination writes, and internal transfers remain. Joining host and egress telemetry can reconstruct the many-to-one graph, so the benefit depends on a correlation gap between observation points.")
        record["stealth_mechanisms"][0]["evidence_refs"] = ["REF-000508", "REF-000426", "REF-000509", "REF-000510"]
    save(root / "technique.yaml", record)
    return root


def formal_child(root, nid, parent, slug, name, summary, content, mechanisms_value,
                 claim_refs, case_refs, reference_refs, strategies, mitigation, limitations):
    record = {
        "schema_version": "2.0.0", "type": "evasion-subtechnique", "id": nid,
        "parent_ref": parent, "name": name, "summary": summary, "aliases": [],
        "lineage": {"attck_subtechnique_inherited": False},
        "definition_and_concept": deepcopy(content["definition_and_concept"]),
        "stealth_characteristics": deepcopy(content["stealth_characteristics"]),
        "scope_boundary_definition": deepcopy(content["scope_boundary_definition"]),
        "application_scenarios_and_threat_model": deepcopy(content["application_scenarios_and_threat_model"]),
        "stealth_mechanisms": mechanisms_value,
        "defense": defense(strategies, mitigation),
        "evidence": {"claim_refs": claim_refs, "case_refs": case_refs, "reference_refs": reference_refs},
        "research": {"limitations": limitations}, "lifecycle": deepcopy(LIFECYCLE),
    }
    assert record["stealth_characteristics"]["paragraphs"][0]["zh"].startswith(name["zh"])
    assert record["stealth_characteristics"]["paragraphs"][0]["en"].startswith(name["en"])
    save(root / "subtechniques" / f"{nid}-{slug}" / "subtechnique.yaml", record)


archive_root = formal_parent(
    "T1560", "NJT-0133", "archive-collected-data",
    {"zh": "归档已收集数据", "en": "Archive Collected Data"}, handoffs["T1560"]["proposed_content"]["summary"],
    ["NJS-0133-001", "NJS-0133-002"],
    block("本技术按归档过程中防守方失去何种观察来划分：受保护归档内容遮蔽改变内部数据的可恢复性，进程内归档谱系压缩则移除独立归档工具的进程启动边。两者可以同现，但前者由密钥可得性与内容解析状态验证，后者由源读取、同进程转换与产物或外联关系验证；工具、库和自定义算法只是实现。分卷、存放位置和文件改名分别留给传输、暂存或身份伪装边界。",
          "The children divide what defenders lose during archival: Protected Archive Content Obscuration changes recoverability of inner data, while In-Process Archival Lineage Compression removes a separate archiver launch edge. They can coexist, but the former is tested through key availability and parse status, and the latter through source reads and output or egress by the same process. Utility, library, and custom algorithm are implementations. Volume splitting, storage location, and renaming remain with transfer, staging, or identity-disguise boundaries."),
    ["CLM-000706", "CLM-000707", "CLM-000708"], ["CASE-000181", "CASE-000182"],
    ["REF-000504", "REF-000505", "REF-000506", "REF-000507", "REF-000230", "REF-000366", "REF-000379", "REF-000475"],
    ["DET-000146"], "MIT-000135", "attack-retained")

archive_protected = {
    "definition_and_concept": block(
        "受保护归档内容遮蔽是攻击者把已取得数据放入需口令或密钥才能恢复内部条目的归档容器，并使无密钥的检查点只能处理外层字节。其直接目标是在随后暂存或外传前限制防守方对数据类别、来源文件及敏感内容的检查。口令算法和归档格式不是分类边界，关键是检查点能否恢复内部语义。",
        "Protected Archive Content Obscuration places acquired data in an archive whose inner members require a password or key to recover, leaving a keyless inspection point with outer bytes only. Its immediate purpose is to restrict inspection of data class, source files, and sensitive contents before later staging or exfiltration. Password algorithm and archive format do not define the category; recoverability at the inspection point does."),
    "stealth_characteristics": block(
        "受保护归档内容遮蔽把可读的文件和部分成员元数据变成无法直接分类的加密负载，内容规则不能据外层扫描结果排除敏感数据。容器头、大小、创建者、源文件读取与外联仍可见；防守方若获得密钥、在加密前执行 DLP，或关联源侧敏感对象与产物，效果就会减弱。",
        "Protected Archive Content Obscuration turns readable files and some member metadata into encrypted payload that cannot be classified directly, so an outer scan cannot rule out sensitive data. Container headers, size, creator, source-file reads, and egress remain visible. The effect weakens when defenders obtain the key, classify sources before encryption, or link sensitive source objects to the archive output."),
    "scope_boundary_definition": block(
        "纳入已收集数据到受保护容器的可证转换，且检查点缺少必要密钥。合法加密备份、受批准传输及隐私保护归档是反例；高熵或受保护文件本身不能证明恶意收集。普通可解压归档属于父级但不属于本子项；把归档放到隐藏目录是 T1074 或相邻伪装边界，分卷和上传则需分别判断。",
        "Include a demonstrated transformation from collected data to a protected container where the inspection point lacks the necessary key. Approved encrypted backups, authorized transfers, and privacy archives are counterexamples; high entropy or protection alone does not prove malicious collection. An ordinarily parseable archive remains in the parent but not this child. Placement in a concealed directory belongs to T1074 or adjacent disguise boundaries, while splitting and upload require separate classification."),
    "application_scenarios_and_threat_model": {
        "application_scenarios": block("攻击者在端点或服务器取得文件、导出数据库或收集配置之后，可能先用口令归档集中这些内容，再交给暂存或外传链。TONESHELL 事件证明这种受保护归档用于实际外传；并不证明所有目标都采用相同检查路径。",
                                       "After obtaining files, database exports, or configuration on an endpoint or server, an adversary may consolidate them into a passworded archive before staging or exfiltration. The TONESHELL incident establishes such protected archival in an observed transfer chain but does not show that every target used the same inspection path."),
        "threat_model": {
            "attacker_model": block("攻击者需有目标数据的读取权、可生成归档的执行能力及不暴露给防守检查点的口令或密钥。若归档在被防守方掌握的密钥服务中创建，或源文件在加密前已被审计，内容遮蔽收益会下降。",
                                    "The adversary needs read access to the target data, the ability to build an archive, and a password or key unavailable at the defensive inspection point. The benefit falls if the archive uses a key service controlled by defenders or source files were audited before encryption."),
            "defender_model": block("防守方可观察文件读取、归档创建、容器格式、大小、进程与传输，却可能无法解析内部成员。只有配置源侧分类、归档解析状态和后继对象关联的检查面，才能在不能解密时仍给出数据暴露风险，而不是把解析失败当作阴性。",
                                    "Defenders may see file reads, archive creation, format, size, process, and transfer while being unable to parse inner members. Source-side classification, archive parse status, and downstream object linkage are needed to assess exposure without decryption, rather than treating parser failure as a negative result.")}},
}
formal_child(archive_root, "NJS-0133-001", "NJT-0133", "protected-archive-content-obscuration",
             {"zh": "受保护归档内容遮蔽", "en": "Protected Archive Content Obscuration"},
             {"zh": "以密钥不可得的归档容器承载已收集数据，使内容检查失去内部文件语义。",
              "en": "Carry collected data in an archive whose key is unavailable to inspection, removing direct access to inner file semantics."},
             archive_protected,
             [{"mechanism_ref": "NM-DO", "role": "primary", "summary": {"zh": "密钥缺失使归档内部数据不能在检查点恢复", "en": "A missing key prevents archive contents from being recovered at inspection"},
               "analysis": block("攻击者先读取源文件，再把内容加密进归档。检查点只能处理容器字节而不能恢复原文件，内容分类和逐成员规则因此失去输入；源侧读取、外层产物和传输元数据仍为可用线索。只有把源、归档与后继取用关联，才能避免把解析失败误认作无敏感内容。",
                                 "The adversary reads source files and encrypts their contents into an archive. The inspection point sees container bytes rather than original files, depriving content classifiers and member rules of input. Source reads, outer artifact, and transfer metadata remain. Joining source, archive, and retrieval prevents a parse failure from being mistaken for absence of sensitive data."),
               "evidence_refs": ["REF-000505", "REF-000507"], "confidence": "high"}],
             ["CLM-000707"], ["CASE-000181"], ["REF-000504", "REF-000505", "REF-000507", "REF-000379", "REF-000475"],
             ["DET-000146"], "MIT-000135",
             block("Unit 42 报告证明口令归档用于外传，但没有实测防御产品漏报；Microsoft 的缺口描述仅适用于所述邮件检查产品。其他检查点仍可能依据外层结构、源侧访问或密钥托管识别风险。",
                   "Unit 42 proves passworded archival in an exfiltration chain but does not measure missed detections. Microsoft's inspection limitation applies to the described mail-security product. Other checkpoints may still identify risk through outer structure, source access, or key custody."))

archive_inprocess = {
    "definition_and_concept": block("进程内归档谱系压缩是攻击者让已经运行的收集组件直接调用内部压缩例程或已链接库，把已收集数据形成归档或编码输出，而不启动独立归档工具。其直接目的在于完成归档转换；匿迹变量是是否出现可被进程创建遥测识别的工具启动边，不是使用了哪一种库或算法。",
                                    "In-Process Archival Lineage Compression has an already running collector call an internal routine or linked library to turn acquired data into archive or encoded output without launching a separate archiver utility. Its direct purpose is archival transformation; the stealth variable is whether a utility-launch edge appears in process telemetry, not the chosen library or algorithm."),
    "stealth_characteristics": block("进程内归档谱系压缩使 7z、rar 或 tar 等独立工具命令行及父子进程边不出现，按工具名检测的规则因此失去匹配对象。源文件读取、同进程写入、加载的压缩模块或同进程外联仍可能暴露链条；仅仅没有看见工具也可能是日志缺失或合法应用内置压缩，不能作阳性判断。",
                                     "In-Process Archival Lineage Compression removes a separate 7z, rar, or tar command line and parent-child edge, leaving tool-name rules without a match. Source reads, writes by the same process, compression modules, or same-process egress may still expose the chain. A missing tool event alone can also reflect missing logs or legitimate integrated compression and is not a positive finding."),
    "scope_boundary_definition": block("纳入可证实的源数据读取与同一现有进程内封装输出，且没有独立归档工具启动的路径。合法备份代理、浏览器下载器与数据库导出器可使用相同架构，必须结合未授权敏感数据目标和后继取用判断。纯粹内存中直接传输而无归档转换不属于本子项；口令造成的内容不可检查性可与兄弟项共现。",
                                       "Include a demonstrated path from source reads to packaging output inside an existing process without a separate archiver launch. Legitimate backup agents, browsers, and database exporters can use the same architecture, so unauthorized sensitive targets and later retrieval matter. Direct memory-to-network transfer without archival transformation is outside this child; password-based inspection loss may coexist with its sibling."),
    "application_scenarios_and_threat_model": {
        "application_scenarios": block("植入程序在端点长期运行并定期取得内部数据时，可把压缩代码直接放入自身处理路径，减少另起归档工具的可见动作。ESET 对 InvisiMole 的分析提供内置 Zlib 与外部 WinRAR 路径的实际对照，但没有证明所有收集内容都走内部路径。",
                                       "An implant that already runs on an endpoint and periodically acquires data can place compression code in its own pipeline, avoiding an extra archiver launch. ESET's InvisiMole analysis provides an observed contrast between integrated Zlib and external WinRAR paths, without proving that every collected item used the integrated path."),
        "threat_model": {
            "attacker_model": block("攻击者需要控制已经能够读取目标数据的进程，并把压缩例程集成在该进程中；若只能调用系统工具，则此变量不成立。内置实现增加开发和内存处理成本，仍可能产生可见模块、缓冲、输出文件及网络传输。",
                                    "The adversary must control an existing process with access to target data and integrate a compression routine within it. The variable does not hold when only a system utility can be invoked. Integration raises implementation and memory-processing cost while still leaving possible modules, buffers, output files, and network traffic."),
            "defender_model": block("防守方若只保留进程启动与已知工具命令行，将缺少该路径的关键事件；文件读取、写入、模块加载与网络事件在充分采集时仍能按进程身份连接。没有源文件读取审计或稳定进程标识时，只能提出未解析的输出来源，不能断言进程内归档。",
                                    "A defender retaining only process starts and known archiver commands lacks a key event for this path. With sufficient collection, file reads, writes, module loads, and network events can still be joined by process identity. Without source-read audit or a stable process key, the output origin remains unresolved rather than proven in-process archival.")}},
}
formal_child(archive_root, "NJS-0133-002", "NJT-0133", "in-process-archival-lineage-compression",
             {"zh": "进程内归档谱系压缩", "en": "In-Process Archival Lineage Compression"},
             {"zh": "在既有收集进程中完成封装，减少独立归档工具的进程谱系痕迹。",
              "en": "Package data within an existing collection process, removing a separate archiver utility from process lineage."},
             archive_inprocess,
             [{"mechanism_ref": "NM-BT", "role": "primary", "summary": {"zh": "归档转换不产生独立工具启动边", "en": "Archival transformation produces no separate utility-launch edge"},
               "analysis": block("攻击者将压缩例程放在既有植入进程中，源文件进入该进程后直接成为归档输出。只依赖独立归档工具进程和命令行的检测不再有匹配事件，但同进程读取、模块、写入及外联可以恢复转换链。此差异是技术推断，不能由单个缺失事件或所有内置压缩行为自动推出规避意图。",
                                 "The adversary places compression in an existing implant, so source files enter that process and become archive output directly. Detection dependent on a separate utility process and command line has no event to match, but same-process reads, modules, writes, and egress can restore the conversion chain. This difference is a technical inference, not proof of evasive intent from one missing event or from every integrated compressor."),
               "evidence_refs": ["REF-000506", "REF-000230"], "confidence": "medium"}],
             ["CLM-000708"], ["CASE-000182"], ["REF-000504", "REF-000506", "REF-000230", "REF-000366", "REF-000379", "REF-000475"],
             ["DET-000146"], "MIT-000135",
             block("InvisiMole 报告显示内置 Zlib 处理内部数据，但未对每个目标文件给出源读、输出与外联的完整事件链。缺少独立工具进程只能作为待验证差异，传感器丢失、正常集成归档及直接编码通信需分别排除。",
                   "The InvisiMole report shows integrated Zlib processing internal data but does not provide a complete source-read, output, and egress chain for every target file. Absence of a separate utility remains a difference to verify; sensor loss, legitimate integrated archives, and direct encoded communication require separate exclusion."))

staging_root = formal_parent(
    "T1074", "NJT-0134", "stealth-oriented-data-staging",
    {"zh": "匿迹型数据暂存", "en": "Stealth-Oriented Data Staging"}, handoffs["T1074"]["proposed_content"]["summary"],
    ["NJS-0134-001"],
    block("正式子项以多源数据是否先汇聚到少数外联节点为轴，而不使用 ATT&CK 的本地与远程位置标签。出口汇聚暂存改变源主机到边界的可见拓扑，跨主机共享访问、目标写入和外联图是其直接防守差异。低审查命名空间和注册表缓冲有案例线索，但与既有资源身份拟态及非文件载体遮蔽边界未充分收敛，暂留研究记录。",
          "The formal child uses whether multiple source hosts first converge on few outbound nodes, rather than ATT&CK local and remote location labels. Egress-Convergent Staging changes the source-host-to-boundary topology, with cross-host share access, target writes, and outbound graph as its distinct defender view. Low-scrutiny namespaces and Registry buffers have case leads, but their boundaries with existing resource-identity mimicry and non-file carrier concealment remain unresolved and are deferred in research."),
    ["CLM-000709", "CLM-000710"], ["CASE-000183", "CASE-000148", "CASE-000185"],
    ["REF-000508", "REF-000426", "REF-000509", "REF-000510", "REF-000379", "REF-000474", "REF-000230"],
    ["DET-000147"], "MIT-000136", "attack-adapted")

egress = next(x for x in handoffs["T1074"]["proposed_subtechniques"] if x["temporary_key"] == "T1074_CHILD_EGRESS_CONVERGENCE")
formal_child(staging_root, "NJS-0134-001", "NJT-0134", "egress-convergent-staging",
             egress["name"], egress["summary"], egress["proposed_content"],
             mechanisms(egress["proposed_content"]["stealth_mechanisms"]),
             ["CLM-000710"], ["CASE-000185"],
             ["REF-000508", "REF-000426", "REF-000509", "REF-000510", "REF-000474", "REF-000230"],
             ["DET-000147"], "MIT-000136",
             block(egress["evidence_limit"]["zh"] + " 正常备份汇聚、集中 ETL 和邮件迁移可形成相似图形，需要授权与业务基线区分。",
                   egress["evidence_limit"]["en"] + " Legitimate backup aggregation, centralized ETL, and mailbox migration can form similar graphs and require authorization and workflow baselines."))

auto_root = formal_parent(
    "T1119", "NJT-0135", "stealth-constrained-automated-collection",
    {"zh": "匿迹约束的自动收集", "en": "Stealth-Constrained Automated Collection"},
    handoffs["T1119"]["proposed_content"]["summary"], ["NJS-0135-001"],
    block("目前只有变化检查点约束的增量收集通过稳定变量、痕迹差异和证据门槛：它改变后续轮次的读取集合，需要跨轮关联。来源到达触发、工作流触发、固定周期和扩展名筛选均已研究，但前两者缺少独立匿迹效果证据，后两者只是普通自动化或目标条件；子项不按工具、数据类型或 ATT&CK 子项划分。",
          "Only Change-Checkpoint-Constrained Incremental Collection currently passes the stable-variable, trace-difference, and evidence gates: it changes later read sets and requires cross-pass correlation. Source-arrival and workflow triggers, fixed periods, and extension filters were examined, but the first two lack distinct stealth-effect evidence and the latter two are ordinary automation or target criteria. Children are not divided by tool, data type, or ATT&CK child."),
    ["CLM-000711", "CLM-000712", "CLM-000713", "CLM-000714"], ["CASE-000184"],
    ["REF-000511", "REF-000512", "REF-000379", "REF-000513", "REF-000475"],
    ["DET-000148"], "MIT-000137", "attack-adapted")

incremental = next(x for x in handoffs["T1119"]["proposed_subtechniques"] if x["temporary_key"] == "T1119_CHILD_INCREMENTAL")
formal_child(auto_root, "NJS-0135-001", "NJT-0135", "change-checkpoint-incremental-collection",
             incremental["name"], incremental["proposed_content"]["summary"], incremental["proposed_content"],
             mechanisms(incremental["proposed_content"]["stealth_mechanisms"]),
             ["CLM-000712", "CLM-000713", "CLM-000714"], ["CASE-000184"],
             ["REF-000511", "REF-000512", "REF-000379", "REF-000475"],
             ["DET-000148"], "MIT-000137", incremental["proposed_content"]["limitations"])

print("Serialized 3 parent and 4 child Technique packages in draft")
