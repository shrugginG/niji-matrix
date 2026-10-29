"""Serialize candidate-specific Collection defenses from reviewed research handoffs."""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
DATE = "2026-09-22"
LIFE = {"status": "draft", "version": "1.0.0", "created": DATE, "modified": DATE,
        "contributors": ["Niji Matrix Research"], "reviewers": []}


def para(zh, en):
    return {"paragraphs": [{"zh": zh, "en": en}]}


def pair(zh, en):
    return {"zh": zh, "en": en}


def save(folder, filename, item):
    path = ROOT / folder / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(item, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


h = {tid: yaml.safe_load((RUN / f"{tid}-handoff.yaml").read_text(encoding="utf-8"))
     for tid in ("T1560", "T1074", "T1119")}


def analytic_source(tid, key):
    return next(x for x in h[tid]["defense_candidates"]["detection_analytics"] if x["temporary_key"] == key)


def requirement(source_type, zh, en, fields, channel=None):
    return {"source_type": source_type, "name": pair(zh, en), "channel": channel,
            "required_fields": fields}


def strategy(sid, slug, name, summary, desc, targets, analytics, refs):
    save("detections", f"{sid}-{slug}.yaml", {
        "schema_version": "2.0.0", "type": "detection-strategy", "id": sid,
        "name": name, "summary": summary, "description": desc,
        "detects_refs": targets, "domains": ["enterprise"], "analytic_refs": analytics,
        "evidence_refs": refs, "lifecycle": LIFE.copy()})


def analytic(aid, slug, sid, name, summary, platforms, logic, data, obs, window,
             dimensions, false_positives, blind_spots, tuning, refs):
    save("analytics", f"{aid}-{slug}.yaml", {
        "schema_version": "2.0.0", "type": "detection-analytic", "id": aid,
        "strategy_ref": sid, "name": name, "summary": summary,
        "domains": ["enterprise"], "platforms": platforms,
        "logic": para(logic["zh"], logic["en"]), "data_requirements": data,
        "observables": obs, "correlation": {"window": window, "dimensions": dimensions},
        "false_positives": false_positives, "blind_spots": blind_spots,
        "tuning_guidance": tuning, "evidence_refs": refs, "lifecycle": LIFE.copy()})


strategy("DET-000146", "archive-input-output-inspection-lineage",
         pair("归档输入—产物—出口与可检查性关联", "Archive Input–Output–Egress and Inspectability Correlation"),
         pair("关联敏感源读取、归档产物的可解析状态与后续取用，并识别没有独立工具进程的封装路径。",
              "Join sensitive source reads, archive inspectability, and downstream use, including packaging without a separate utility process."),
         para("策略要求证明已取得数据被转成归档容器或编码流，再区分内容因缺密钥不可检查和转换发生在既有进程内两种观察缺口。NJA-000152 以解析状态、源敏感性及出口对象关联评估受保护归档；NJA-000153 以同一进程的读取、输出和网络行为重建进程内路径。两个分析都不能仅凭文件后缀、缺失工具进程或高熵确认恶意。",
              "The strategy first establishes transformation of acquired data into an archive or encoded stream, then distinguishes keyless content inspection from in-process conversion. NJA-000152 joins parse state, source sensitivity, and outbound object; NJA-000153 reconstructs the same process's reads, output, and network behavior. Neither confirms malice from an extension, missing utility process, or high entropy alone."),
         ["NJT-0133", "NJS-0133-001", "NJS-0133-002"], ["NJA-000152", "NJA-000153"],
         ["REF-000504", "REF-000505", "REF-000506", "REF-000507", "REF-000379", "REF-000230", "REF-000366", "REF-000475"])

src = analytic_source("T1560", "T1560_NJA_PROTECTED_ARCHIVE")
analytic("NJA-000152", "protected-archive-source-inspection-egress", "DET-000146",
         pair("受保护归档源侧证据与出口关联", "Protected Archive Source Evidence and Egress Correlation"),
         pair("对不可解析的受保护归档保留明确状态，并要求敏感源读取或后续出口关系形成。",
              "Preserve an explicit uninspectable state for protected archives and require sensitive-source or downstream-egress linkage."),
         ["Windows"], src["logic"],
         [requirement("windows-file-read-audit", "Windows 敏感文件读取审计", "Windows sensitive-file read audit",
                      ["timestamp", "device_id", "subject_logon_id", "object_path", "access_mask", "process_id", "process_name"], "Security/4663"),
          requirement("endpoint-file-create", "端点文件创建与写入", "Endpoint file creation and write",
                      ["timestamp", "device_id", "file_path", "file_hash", "file_size", "writer_process_id"], "Sysmon/11 or DeviceFileEvents"),
          requirement("archive-parse-result", "归档格式与解析结果", "Archive format and parse result",
                      ["timestamp", "artifact_id", "true_format", "password_required", "member_parse_state"]),
          requirement("sensitive-source-inventory", "敏感源对象清单", "Sensitive source-object inventory",
                      ["device_id", "file_path", "sensitivity_label"]),
          requirement("outbound-object-transfer", "对象外传或共享复制", "Outbound object transfer or share copy",
                      ["timestamp", "device_id", "artifact_id", "destination", "transfer_result"])],
         [pair("敏感源读取后出现需要口令且无法展开的归档", "A password-required, unexpandable archive follows sensitive-source reads"),
          pair("同一产物随后被上传或复制到非批准出口", "The same artifact is later uploaded or copied to an unapproved destination")],
         pair("从首个敏感源读取前 30 分钟至归档最后一次传出后 30 分钟关联，并按环境实际任务长度调整。",
              "Correlate from thirty minutes before the first sensitive-source read through thirty minutes after the last archive transfer, adjusted to local job duration."),
         ["device_id", "subject_logon_id", "writer_process_id", "artifact_id", "file_hash", "destination", "time"],
         [src["false_positives"]], [src["blind_spots"]], para(src["tuning"]["zh"], src["tuning"]["en"]),
         ["REF-000505", "REF-000507", "REF-000379", "REF-000230", "REF-000475"])

src = analytic_source("T1560", "T1560_NJA_IN_PROCESS_ARCHIVE")
analytic("NJA-000153", "same-process-sensitive-read-archive-output", "DET-000146",
         pair("同进程敏感读取与归档输出关联", "Same-Process Sensitive Reads and Archive Output Correlation"),
         pair("识别读取敏感输入并自行形成归档输出的进程，以正向输入输出链替代工具名告警。",
              "Identify processes that read sensitive inputs and package output themselves, using a positive input-to-output chain instead of utility names."),
         ["Windows"], src["logic"],
         [requirement("windows-file-read-audit", "Windows 敏感文件读取审计", "Windows sensitive-file read audit",
                      ["timestamp", "device_id", "object_path", "access_mask", "process_id", "process_name"], "Security/4663"),
          requirement("endpoint-file-create", "端点归档产物创建", "Endpoint archive-output creation",
                      ["timestamp", "device_id", "file_path", "writer_process_id", "file_size"], "Sysmon/11 or DeviceFileEvents"),
          requirement("process-lineage", "进程启动与父子谱系", "Process launch and parent-child lineage",
                      ["timestamp", "device_id", "process_id", "parent_process_id", "image", "command_line"], "Sysmon/1"),
          requirement("archive-output-classifier", "归档输出格式判定", "Archive output-format classifier",
                      ["timestamp", "artifact_id", "true_format", "producer_process_id"]),
          requirement("process-network", "进程网络连接", "Process network connection",
                      ["timestamp", "device_id", "process_id", "destination_ip", "destination_port"], "Sysmon/3")],
         [pair("单个既有进程读取多个敏感源并形成可证归档产物", "One existing process reads several sensitive sources and produces a verifiable archive"),
          pair("同一进程随后外联，且进程树中没有独立归档工具", "The same process later connects outward without a separate archiver in its process tree")],
         pair("覆盖敏感源读取前后各 30 分钟，并保留完整进程生存期以排除更早启动的外部工具。",
              "Cover thirty minutes before and after sensitive reads and retain the full process lifetime to rule out an earlier utility launch."),
         ["device_id", "process_id", "parent_process_id", "source_path", "artifact_id", "destination_ip", "time"],
         [src["false_positives"]], [src["blind_spots"]], para(src["tuning"]["zh"], src["tuning"]["en"]),
         ["REF-000506", "REF-000379", "REF-000230", "REF-000366", "REF-000475"])

strategy("DET-000147", "many-source-staging-to-egress-lineage",
         pair("多源暂存—单点外联谱系重建", "Many-Source Staging to Single-Egress Lineage"),
         pair("重建敏感数据从多个来源汇入被控节点再由少数出口取走的路径。",
              "Reconstruct paths in which sensitive data from multiple origins converges on a controlled node and leaves through few egress points."),
         para("策略以来源主机、共享写入、暂存节点文件创建和后继取用为事实链。NJA-000154 将 SMB 权限检查与实际文件创建及 Web 取回分开验证，输出多源入站和单点外联的图形。仅有中央服务器、归档文件或一个外联连接不足以确认异常暂存；应先核对批准的备份、迁移和 ETL 作业。",
              "The strategy traces source hosts, share writes, creation at the staging node, and later retrieval. NJA-000154 verifies SMB access checks separately from actual file creation and web retrieval, then emits a many-source ingress and concentrated-egress graph. A central server, archive, or single outbound connection alone is insufficient; approved backup, migration, and ETL jobs must be checked first."),
         ["NJT-0134", "NJS-0134-001"], ["NJA-000154"],
         ["REF-000508", "REF-000426", "REF-000509", "REF-000510", "REF-000474", "REF-000230", "REF-000514"])

src = analytic_source("T1074", "T1074_NJA_FUNNEL")
analytic("NJA-000154", "share-write-file-create-http-retrieval", "DET-000147",
         pair("共享写入—文件创建—外部取回关联", "Share Write–File Create–External Retrieval Correlation"),
         pair("将多个源主机的成功暂存写入与同一服务器的外部取回请求连接。",
              "Join successful staging writes from multiple source hosts to external retrieval from the same server."),
         ["Windows"], src["logic"],
         [requirement("windows-share-access", "Windows 详细文件共享访问", "Windows detailed file-share access",
                      ["timestamp", "server_id", "source_ip", "subject_sid", "share_name", "relative_path", "access_mask"], "Security/5145"),
          requirement("server-file-create", "服务器文件创建", "Server file creation",
                      ["timestamp", "server_id", "writer_process_id", "target_path", "file_size"], "Sysmon/11"),
          requirement("http-access-log", "Web 服务器访问日志", "Web server access log",
                      ["timestamp", "server_id", "client_ip", "uri_path", "response_status", "response_bytes"], "IIS W3C or equivalent"),
          requirement("source-asset-map", "来源主机资产映射", "Source host asset map",
                      ["source_ip", "asset_id", "owner_id"])],
         [src["observables"]],
         pair("以 24 小时为初始窗口连接多源写入和取回；按合法备份周期调整，同时保留先写后读顺序。",
              "Use twenty-four hours as the initial window for many-source writes and retrieval, adapting to legitimate backup cycles while preserving write-before-read order."),
         ["server_id", "source_ip", "asset_id", "subject_sid", "share_name", "relative_path", "uri_path", "time"],
         [src["false_positives"]], [src["blind_spots"]], para(src["tuning"]["zh"], src["tuning"]["en"]),
         ["REF-000508", "REF-000426", "REF-000509", "REF-000510", "REF-000474", "REF-000230", "REF-000514"])

strategy("DET-000148", "repeated-source-read-pass-correlation",
         pair("自动收集轮次与敏感源读取关联", "Automated Collection Pass and Sensitive-Source Read Correlation"),
         pair("跨轮次关联文件或云对象读取，区分增量选择、正常同步与异常自动获取。",
              "Correlate file or cloud-object reads across passes to distinguish incremental selection, normal synchronization, and anomalous automated acquisition."),
         para("策略针对获取阶段的源读取，不把归档、暂存或外传当作自动收集的定义。NJA-000155 在已启用敏感文件读取审计的 Windows 主机上重建首轮及后续变化文件读取；NJA-000156 在显式开启 S3 对象数据事件的桶上识别重复 GetObject。云端分析只覆盖父技术的自动获取模式，不把尚无案例支持的云端增量行为升级为正式子项证据。",
              "The strategy targets source reads during acquisition; archiving, staging, and exfiltration do not define automated collection. NJA-000155 reconstructs initial and later changed-file reads on Windows hosts with sensitive-file read auditing. NJA-000156 finds repeated GetObject calls in S3 buckets with object data events explicitly enabled. The cloud analytic covers parent-level automation and does not promote cloud incremental behavior to a formal child without case evidence."),
         ["NJT-0135", "NJS-0135-001"], ["NJA-000155", "NJA-000156"],
         ["REF-000511", "REF-000512", "REF-000379", "REF-000513", "REF-000475"])

src = analytic_source("T1119", "T1119_NJA_WINDOWS_INCREMENTAL")
analytic("NJA-000155", "windows-changed-file-read-passes", "DET-000148",
         src["name"],
         pair("检测未授权主体跨轮选择变化文件的读取模式，并保留首轮与检查点关系。",
              "Detect unauthorized changed-file reads across passes while retaining the initial-pass and checkpoint relationship."),
         ["Windows"], src["logic"],
         [requirement("windows-file-read-audit", "Windows 敏感文件读取审计", "Windows sensitive-file read audit",
                      ["timestamp", "device_id", "subject_sid", "logon_id", "object_path", "access_mask", "process_id", "process_name"], "Security/4663"),
          requirement("file-change-inventory", "文件变更清单", "File change inventory",
                      ["timestamp", "device_id", "file_path", "change_type"]),
          requirement("authorized-job-inventory", "授权自动作业清单", "Authorized automation job inventory",
                      ["principal_id", "process_path", "covered_paths", "approved_schedule"])],
         [pair("首轮广泛读取后，后续轮次主要触及新变更文件", "A broad initial pass is followed by later reads concentrated on newly changed files"),
          pair("非批准进程的检查点更新与敏感目录读取周期相符", "Checkpoint updates by an unapproved process align with sensitive-directory read passes")],
         pair("至少保留 7 至 30 天读取与变更历史以覆盖多个轮次；短于两个轮次时仅输出待观察状态。",
              "Retain at least seven to thirty days of read and change history to cover multiple passes; with fewer than two passes, report an observation-pending state."),
         ["device_id", "subject_sid", "logon_id", "process_id", "object_path", "time"],
         src["false_positives"], src["blind_spots"],
         para("按目录变更率训练每轮文件数和变化重合率，按身份、目录及有效期排除具体批准备份；不得仅以 12 小时周期或 ft.data 名称匹配。首次基线扫描与后续轮次应分开比较。",
              "Train files-per-pass and changed-set overlap against each directory's change rate. Exempt a specific approved backup only by identity, path scope, and validity period; never match a universal twelve-hour period or ft.data name. Compare the initial baseline pass separately from later passes."),
         ["REF-000512", "REF-000379", "REF-000475"])

src = analytic_source("T1119", "T1119_NJA_S3_REPEATED_READ")
analytic("NJA-000156", "s3-repeated-object-read-passes", "DET-000148",
         src["name"],
         pair("在已启用对象数据事件的敏感桶上识别异常主体的重复 GetObject 收集轮次。",
              "Find repeated GetObject collection passes by unusual principals in sensitive buckets with object data events enabled."),
         ["IaaS"], src["logic"],
         [requirement("cloudtrail-s3-object-read", "CloudTrail S3 对象读取", "CloudTrail S3 object reads",
                      ["event_time", "event_name", "principal_arn", "source_ip", "user_agent", "bucket_name", "object_key"], "CloudTrail S3 data events"),
          requirement("cloud-job-inventory", "云端批准作业清单", "Approved cloud-job inventory",
                      ["role_arn", "bucket_scope", "approved_schedule"]),
          requirement("s3-object-change", "S3 对象变更记录", "S3 object-change records",
                      ["timestamp", "bucket_name", "object_key", "change_type"])],
         [pair("少见角色跨多个轮次读取同一敏感桶的大量不同对象", "An unusual role reads many distinct objects in the same sensitive bucket across passes"),
          pair("多次读取与批准 ETL 或备份作业的身份及时间不符", "Repeated reads do not match approved ETL or backup identity and schedule")],
         pair("关联 7 至 30 天的对象读取和变更记录，并确保至少覆盖两个预期业务作业周期。",
              "Correlate seven to thirty days of object reads and changes and include at least two expected business-job cycles."),
         ["principal_arn", "bucket_name", "object_key", "source_ip", "user_agent", "time"],
         src["false_positives"], src["blind_spots"],
         para("先对高价值桶启用对象数据事件，再按批准角色、前缀和作业时段建立基线；仅对未知主体、意外前缀或异常跨轮覆盖提高风险，不把所有程序化 API 读取视为恶意。",
              "Enable object data events on high-value buckets, then baseline approved roles, prefixes, and job windows. Raise risk for unknown principals, unexpected prefixes, or anomalous cross-pass coverage rather than treating all programmatic API reads as malicious."),
         ["REF-000511", "REF-000513"])


def measure(key, name, description, control_type):
    return {"key": key, "name": name, "description": description, "control_type": control_type}


def application(target, use, effect, limits):
    return {"target_ref": target, "use": use, "expected_effect": effect, "limitations": limits}


def mitigation(mid, slug, name, summary, description, measures, applications, refs):
    save("mitigations", f"{mid}-{slug}.yaml", {
        "schema_version": "2.0.0", "type": "mitigation", "id": mid,
        "name": name, "summary": summary, "description": description,
        "domains": ["enterprise"], "measures": measures, "applications": applications,
        "evidence_refs": refs, "lifecycle": LIFE.copy()})


archive_mit = h["T1560"]["defense_candidates"]["mitigations"][0]
archive_names = [pair("源数据最小权限与归档前分类", "Source Least Privilege and Pre-Archive Classification"),
                 pair("受保护归档出口审核", "Protected Archive Egress Review"),
                 pair("归档任务及应用内导出范围治理", "Archive Job and In-App Export Scope Governance")]
archive_measures = [measure(x["key"].replace("_", "-"), archive_names[i], para(x["action"]["zh"], x["action"]["en"]), x["control_type"])
                    for i, x in enumerate(archive_mit["measures"])]
archive_apps = [application(target, para(x["use"]["zh"], x["use"]["en"]),
                            para(x["expected_effect"]["zh"], x["expected_effect"]["en"]),
                            para(x["limitations"]["zh"], x["limitations"]["en"]))
                for target, x in zip(["NJT-0133", "NJS-0133-001", "NJS-0133-002"], archive_mit["applications"])]
mitigation("MIT-000135", "sensitive-source-and-archive-egress-governance",
           pair("敏感源与归档出口治理", "Sensitive-Source and Archive-Egress Governance"),
           pair("限制归档前的敏感数据读取，并把无法检查的归档送入有证据的出口审核。",
                "Constrain sensitive reads before archiving and route uninspectable archives through evidence-based egress review."),
           para("控制先在源数据仍可分类时降低读取权，再要求归档产物与批准的接收方、任务和密钥处理方式相符。对无法解析的口令归档保留不可检查状态；对内置压缩进程，限制其输入范围与外联权限。这样既控制内容遮蔽，也保留进程内归档路径的源侧边界。",
                "The control reduces read rights while source data is still classifiable, then requires archive outputs to match approved recipients, jobs, and key handling. Passworded archives retain an explicit uninspectable state; processes with integrated compression have constrained inputs and egress. This addresses content blindness while preserving a source-side boundary for in-process packaging."),
           archive_measures, archive_apps,
           ["REF-000504", "REF-000505", "REF-000507", "REF-000379", "REF-000475"])

staging_mit = h["T1074"]["defense_candidates"]["mitigations"][0]
staging_names = [pair("敏感导出批准落点", "Approved Sensitive-Export Destinations"),
                 pair("汇聚节点出口职责分离", "Aggregation-Node Egress Role Separation"),
                 pair("暂存点独立审计", "Independent Staging-Point Audit")]
staging_measures = [measure(x["key"].replace("_", "-"), staging_names[i], para(x["action"]["zh"], x["action"]["en"]), x["control_type"])
                    for i, x in enumerate(staging_mit["measures"])]
staging_apps = [application(target, para(x["use"]["zh"], x["use"]["en"]),
                            para(x["expected_effect"]["zh"], x["expected_effect"]["en"]),
                            para(x["limitations"]["zh"], x["limitations"]["en"]))
                for target, x in zip(["NJT-0134", "NJS-0134-001"], staging_mit["applications"][:2])]
mitigation("MIT-000136", "constrained-staging-destinations-and-egress",
           staging_mit["name"],
           pair("限定敏感数据可写的暂存点及其外联权限，并保留多源写入与取用的独立审计。",
                "Constrain writable staging points and their egress rights for sensitive data while retaining independent audit of many-source writes and retrieval."),
           para("为邮箱导出、共享复制和数据库转储指定受控落点，并把能接收多源数据的服务器与互联网可取回服务的职责分离。审计源写入、目标文件创建和后继访问，以便发现被盗账户或允许路径被滥用。措施降低可用汇聚点数量，但不能把任何中央服务器自动视为恶意。",
                "Assign controlled destinations for mailbox exports, share copies, and database dumps, and separate servers that receive many sources from Internet-retrievable service roles. Audit source writes, target creation, and later access to expose misuse of stolen accounts or allowed paths. The measures reduce usable aggregation points without treating every central server as malicious."),
           staging_measures, staging_apps,
           ["REF-000508", "REF-000426", "REF-000509", "REF-000474", "REF-000514"])

auto_mit = h["T1119"]["defense_candidates"]["mitigations"][0]
auto_names = [pair("敏感源读取授权收敛", "Sensitive-Source Read Authorization Reduction"),
              pair("多轮读取谱系保留", "Cross-Pass Read-Lineage Retention")]
auto_measures = [measure(x["key"].replace("_", "-"), auto_names[i],
                         para(x["description"]["zh"], x["description"]["en"]), x["control_type"])
                 for i, x in enumerate(auto_mit["measures"])]
auto_apps = [application(target, para(x["use"]["zh"], x["use"]["en"]),
                         para(x["expected_effect"]["zh"], x["expected_effect"]["en"]),
                         para(x["limitations"]["zh"], x["limitations"]["en"]))
             for target, x in zip(["NJT-0135", "NJS-0135-001"], auto_mit["applications"])]
mitigation("MIT-000137", "collection-source-read-and-audit-governance",
           auto_mit["name"],
           pair("缩小自动收集可读取的敏感对象范围，并保留足以连接多轮小规模读取的审计。",
                "Reduce sensitive objects accessible to automated collectors and retain audit sufficient to join several small read passes."),
           para("按身份和工作职责限制高价值目录与云桶的读取范围，单列批准的备份、索引和 ETL 作业。对这些源启用有针对性的读取审计和跨轮保留，记录身份、目标范围、检查点或作业窗口；这些措施削减失陷身份的批量读取能力，并使增量模式有可比较的正常基线。",
                "Restrict high-value directories and cloud buckets by identity and job duty, and separately inventory approved backup, indexing, and ETL jobs. Enable targeted read auditing and cross-pass retention for those sources, recording identity, target scope, and checkpoint or job window. These controls reduce bulk-read reach of a compromised identity and provide a normal baseline against which incremental patterns can be compared."),
           auto_measures, auto_apps,
           ["REF-000511", "REF-000512", "REF-000379", "REF-000513"])

print("Serialized 3 strategies, 5 analytics, and 3 target-specific mitigations in draft")
