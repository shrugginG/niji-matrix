"""Serialize individually reviewed TA0040 batch-one content into canonical YAML.

All bilingual content below is authored per object from the two evidence handoffs.
The helpers only order fields and serialize YAML; they do not generate prose from names.
"""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
TACTIC = ROOT / "matrix/tactics/TA0040-impact"
TODAY = "2026-09-22"


def B(zh, en):
    return {"zh": zh, "en": en}


def P(zh, en):
    return {"paragraphs": [B(zh, en)]}


def PP(*pairs):
    return {"paragraphs": [B(zh, en) for zh, en in pairs]}


def life(version="0.1.0"):
    return {"status": "review", "version": version, "created": TODAY,
            "modified": TODAY, "contributors": ["Niji Matrix Research"], "reviewers": []}


def write(relative, data):
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")


REFS = [
    (647, "MITRE ATT&CK", "Data Destruction, Technique T1485", "数据销毁，技术 T1485", "official-documentation", "https://attack.mitre.org/versions/v19/techniques/T1485", "Parent description, Impact mapping, and boundary with Disk Wipe", "锚定数据销毁父行为和战术；不把破坏结果直接当作匿迹证据。", "Anchors parent destruction and tactic; the impact outcome alone is not stealth evidence."),
    (648, "Amazon Web Services", "Expiring Objects", "Amazon S3 对象到期处理", "official-documentation", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-expire-general-considerations.html", "Lifecycle expiration timing and version-state consequences", "说明服务异步执行和版本状态差异，不证明真实受害事件。", "Establishes asynchronous service execution and version-state differences, not a victim incident."),
    (649, "Palo Alto Networks", "Ransomware in the Cloud", "云中的勒索软件", "vendor-report", "https://www.paloaltonetworks.com/blog/cloud-security/ransomware-data-protection-cloud/", "Indirect Deletion Using Lifecycle Policy section", "给出恶意生命周期规则的攻击路径和对象监控盲区分析；属于威胁建模，不是已证实受害案例。", "Models malicious lifecycle rules and the object-monitoring gap; it is threat analysis, not a verified victim case."),
    (650, "Amazon Web Services", "Configuring S3 Lifecycle Event Notifications", "配置 S3 生命周期事件通知", "official-documentation", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configure-notification.html", "LifecycleExpiration event names, service principal, bucket/key and configuration fields", "说明可选通知的服务主体和对象字段；未启用通知时不能假定有此遥测。", "Documents service-principal and object fields in optional notifications; telemetry is absent if not enabled."),
    (651, "Amazon Web Services", "Amazon S3 EventBridge Events", "Amazon S3 EventBridge 事件", "official-documentation", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventBridge.html", "Object Deleted detail reason and deletion-type", "区分生命周期到期与直接删除及删除标记和永久删除的事件表示。", "Distinguishes lifecycle expiration from direct deletion and delete-marker from permanent-deletion event forms."),
    (652, "Amazon Web Services", "Object Lock Considerations", "对象锁使用注意事项", "official-documentation", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html", "Lifecycle interaction and delete-marker behavior", "用于界定受保护版本与当前视图消失的区别。", "Supports the distinction between protected versions and disappearance from the current view."),
    (653, "Amazon Web Services", "Working with Delete Markers", "使用删除标记", "official-documentation", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeleteMarker.html", "Current-version delete marker and 404 behavior", "404 和当前版本不可见不能单独证明旧版本不可恢复。", "A 404 and absent current view do not alone establish that prior versions are unrecoverable."),
    (654, "Amazon Web Services", "Locking Objects with Object Lock", "使用对象锁保护对象", "official-documentation", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html", "Version-level WORM retention and governance/compliance modes", "同时支持销毁和加密候选的旧版本保护与例外边界。", "Supports protected prior versions and control limits for both destruction and encryption candidates."),
    (655, "Amazon Web Services", "Amazon S3 API Actions and Permissions", "Amazon S3 API 操作与权限", "official-documentation", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-policy-actions.html", "PutBucketLifecycle permission row", "证实修改生命周期配置所需权限，不能以对象删除权限代替。", "Establishes lifecycle-configuration permission, which is distinct from object-delete permission."),
    (656, "Microsoft", "Security Event 4660", "安全事件 4660", "official-documentation", "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4660", "Deletion event and handle correlation to 4663", "4660 可证实删除但不含对象名，需结合 4663 和审计配置。", "4660 can confirm deletion but omits object name; correlate with 4663 and audit configuration."),
    (657, "Amazon Web Services", "Bucket Policies for Amazon S3", "Amazon S3 存储桶策略", "official-documentation", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html", "Lifecycle action exception to object-delete bucket policy", "对象删除拒绝策略不能代替生命周期配置权限治理。", "An object-delete deny policy does not replace lifecycle-configuration authority governance."),
    (658, "MITRE ATT&CK", "Data Encrypted for Impact, Technique T1486", "为影响而加密数据，技术 T1486", "official-documentation", "https://attack.mitre.org/versions/v19/techniques/T1486", "Parent description, Impact mapping, and no-subtechnique inventory", "锚定以密钥不可得造成数据不可读的父行为，不独立证明新的匿迹子项。", "Anchors parent denial of reading through key custody; does not independently prove new stealth children."),
    (659, "SentinelOne Labs", "Ransomware Developers Turn to Intermittent Encryption to Evade Detection", "勒索软件开发者采用间歇加密规避检测", "sample-analysis", "https://www.sentinelone.com/labs/crimeware-trends-ransomware-developers-turn-to-intermittent-encryption-to-evade-detection/", "Introduction and analyzed intermittent encryption layouts", "样本分析支持文件内改写密度、较低写入量和整文件统计盲区，不提供通用阈值。", "Sample analysis supports regional rewrite density, lower I/O, and whole-file statistical blind spots, not a universal threshold."),
    (660, "Amazon Web Services", "Preventing Unintended Encryption of Amazon S3 Objects", "防止 Amazon S3 对象遭非预期加密", "incident-report", "https://aws.amazon.com/blogs/security/preventing-unintended-encryption-of-amazon-s3-objects/", "AWS CIRT observed mass SSE-C CopyObject overwrites and policy guidance", "记录被窃有效凭据与大量 SSE-C 重加密；未披露单一受害者身份或完整读取验证。", "Records stolen valid credentials and mass SSE-C re-encryption; no named victim or complete read validation is disclosed."),
    (661, "Amazon Web Services", "Auditing S3 Server-Side Encryption Methods for Object Uploads", "审计 S3 对象上传的服务端加密方法", "official-documentation", "https://aws.amazon.com/blogs/storage/auditing-amazon-s3-server-side-encryption-methods-for-object-uploads/", "CloudTrail object data-event example and encryption request fields", "支持对象数据事件的加密参数观察；不得把客户密钥材料写入日志。", "Supports encryption-parameter observation in object data events; do not collect customer key material."),
    (662, "Microsoft", "Controlled Folder Access Overview", "受控文件夹访问概述", "official-documentation", "https://learn.microsoft.com/en-us/defender-endpoint/controlled-folders", "Protected-folder scope and application-control behavior", "说明受控目录对未经批准写入的限制，不保证受信任应用不会被滥用。", "Explains restrictions on unapproved writes to protected folders, not protection against every abused trusted app."),
    (663, "Amazon Web Services", "Default SSE-C Setting for New Buckets FAQ", "新建存储桶 SSE-C 默认设置常见问题", "official-documentation", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-s3-c-encryption-setting-faq.html", "April 2026 default SSE-C block and explicit enablement conditions", "2026 年默认阻止改变攻击前提；必须核查桶当前配置及配置变更权限。", "The 2026 default block changes attack prerequisites; check bucket configuration and change authority."),
]

for n, publisher, en, zh, kind, url, locator, nz, ne in REFS:
    write(f"references/REF-{n:06d}-{ {647:'mitre-t1485',648:'aws-lifecycle-expiry',649:'palo-alto-cloud-ransomware',650:'aws-lifecycle-notifications',651:'aws-s3-eventbridge',652:'aws-object-lock-considerations',653:'aws-delete-markers',654:'aws-object-lock',655:'aws-s3-api-permissions',656:'microsoft-event-4660',657:'aws-bucket-policies',658:'mitre-t1486',659:'sentinelone-intermittent-encryption',660:'aws-sse-c-incident',661:'aws-s3-encryption-audit',662:'microsoft-controlled-folders',663:'aws-sse-c-default'}[n]}.yaml", {
        "schema_version": "1.0.0", "type": "reference", "id": f"REF-{n:06d}",
        "title_zh": zh, "title_en": en, "source_type": kind, "authors": [publisher],
        "publisher": publisher, "published": None, "url": url, "accessed": TODAY,
        "locator": locator, "archive_url": None, "credibility": "high",
        "notes_zh": nz, "notes_en": ne})


CLAIMS = [
    (778, "technique-relevance", "攻击者删除或覆写业务文件和对象可使合法读取或处理失败；是否能恢复取决于版本和独立副本，破坏结果本身不证明匿迹。", "Adversary deletion or overwrite of business files and objects can deny legitimate reading or processing; recoverability depends on versions and independent copies, and impact alone does not prove stealth.", ["NJT-0156"], ["REF-000647", "REF-000648"], "strongly-inferred", "high"),
    (779, "subtechnique-existence", "攻击者改动对象到期规则后由存储服务在另一时间执行删除，使规则写入主体与结果事件的服务主体分离；对象事件需要回连配置版本才能归因。", "After an adversary changes an object-expiry rule, the storage service deletes later, separating the rule-writing principal from the service principal of the result event; attribution requires joining object events to configuration versions.", ["NJT-0156", "NJS-0156-001", "NM-BT"], ["REF-000648", "REF-000649", "REF-000650", "REF-000651"], "strongly-inferred", "medium"),
    (780, "technique-boundary", "版本化对象的删除标记可使当前读取失败而旧版本仍在；将当前视图消失报告为永久销毁必须另查版本清单和保留控制。", "A delete marker on a versioned object can deny current reading while an older version survives; reporting permanent destruction from current-view absence requires separate checks of version inventory and retention controls.", ["NJT-0156", "NJS-0156-001"], ["REF-000652", "REF-000653", "REF-000654"], "directly-observed", "high"),
    (781, "technique-relevance", "攻击者未授权加密或重加密数据并控制当前状态的解密密钥时，文件或对象仍可存在而合法读取失败；勒索通知不是必要条件。", "When an adversary encrypts or re-encrypts data without authorization and controls the current state's decryption key, files or objects may remain present while legitimate reading fails; a ransom notice is not required.", ["NJT-0157"], ["REF-000658", "REF-000660"], "directly-observed", "high"),
    (782, "subtechnique-existence", "已观察到的间歇加密只改写文件内间隔区段，使写入量与整文件密文统计信号下降，同时保留可由区域比较和跨文件进程关联发现的痕迹。", "Observed intermittent encryption rewrites spaced regions within a file, reducing write volume and whole-file ciphertext statistics while retaining traces discoverable by regional comparison and cross-file process correlation.", ["NJT-0157", "NJS-0157-001", "NM-FD"], ["REF-000659"], "directly-observed", "high"),
    (783, "subtechnique-existence", "AWS 已观察到持被窃有效凭据者使用 SSE-C CopyObject 批量重加密现有对象；重加密发生在服务数据面，须用对象数据事件和加密参数而非主机文件写入重建。", "AWS observed actors with stolen valid credentials use SSE-C CopyObject to re-encrypt existing objects at scale; execution occurs in the service data plane and must be reconstructed from object data events and encryption parameters rather than host file writes.", ["NJT-0157", "NJS-0157-002", "NM-BT"], ["REF-000660", "REF-000661", "REF-000663"], "directly-observed", "high"),
]
for n, kind, zh, en, subjects, refs, mode, confidence in CLAIMS:
    write(f"claims/CLM-{n:06d}-ta0040-impact-batch-one.yaml", {
        "schema_version": "1.0.0", "type": "claim", "id": f"CLM-{n:06d}",
        "claim_type": kind, "statement_zh": zh, "statement_en": en,
        "subject_refs": subjects, "evidence_refs": refs,
        "evidence_mode": mode, "confidence": confidence, "status": "review"})

write("cases/CASE-000216-aws-cirt-sse-c-object-ransomware.yaml", {
    "schema_version": "1.0.0", "type": "case", "id": "CASE-000216",
    "name_zh": "AWS CIRT 观察到的 S3 SSE-C 对象重加密活动",
    "name_en": "AWS CIRT Observed S3 SSE-C Object Re-encryption",
    "actor_or_campaign": "Unattributed actors observed by AWS CIRT",
    "subject_refs": ["NJT-0157", "NJS-0157-002"],
    "description_zh": "AWS 安全团队报告，攻击者取得客户的有效凭据后，使用带客户提供密钥的 SSE-C CopyObject 对大量已有 S3 对象进行覆写式重加密。公开报告给出恶意操作模式与防御响应，但未披露单一受害者身份、完整时序或逐对象读取验证；本案例只记录其实际观察范围。",
    "description_en": "AWS security teams reported actors obtaining valid customer credentials and using SSE-C CopyObject with customer-provided keys to overwrite and re-encrypt many existing S3 objects. The public report describes the malicious operation pattern and defensive response but does not identify one victim or disclose a full timeline or per-object read validation; this case records only that observed scope.",
    "time_range": "Reported by 2025-01",
    "target_sectors_zh": ["使用 Amazon S3 的客户环境；具体行业未披露"],
    "target_sectors_en": ["Amazon S3 customer environments; sectors undisclosed"],
    "evidence_refs": ["REF-000660"], "confidence": "high", "status": "review"})

DECISION_ROOT = "matrix/tactics/TA0040-impact/decisions"
DECISIONS = [
    ("T1485", B("数据销毁", "Data Destruction"), "medium",
     B("数据销毁属于影响释放，但直接删除或覆写并不自动具备匿迹特性。本矩阵将父行为适配为具有证据支持的观察分离式破坏：攻击者改动删除规则，由存储服务在后来执行对象移除，使规则写入者与对象损失事件分离。其他销毁方式用于界定父级范围，却不能仅凭危害结果升级成原生子技术；当前证据尚无完整受害者案例证明此子项的业务损失链。", "Data destruction is Impact, but direct deletion or overwrite is not automatically stealthy. This matrix adapts the parent to evidenced observation-separated destruction: an adversary changes a deletion rule and a storage service later removes objects, separating the rule writer from the object-loss event. Other destructive forms define the parent boundary but cannot become native children from harm alone; current evidence lacks a complete victim case for this child's business-loss chain."),
     B("纳入文件与对象业务可用性损失及有证据的决策—执行观察差异；不吸收加密、磁盘结构擦除、恢复副本抑制、仍可使用的数据值篡改或攻击工具清理。T1485.001 只作为研究广度资料，不被导入。", "Include business-data loss through file or object destruction and evidenced decision-to-execution observation differences. Exclude encryption, disk-structure wiping, recovery-copy suppression, usable-data value manipulation, and cleanup of attacker tools. T1485.001 is research-breadth context only, not imported."),
     ["REF-000647", "REF-000648", "REF-000649", "REF-000650", "REF-000651", "REF-000654"], "NJT-0156"),
    ("T1486", B("为影响而加密数据", "Data Encrypted for Impact"), "high",
     B("攻击者令原本可读的数据因未授权加密和密钥控制而不可读，属于影响释放。Niji 适配其正式范围为两类有独立证据的匿迹设计：文件内部稀疏改写降低整文件统计和写入信号，或利用有效云凭据让存储服务在客户密钥下重加密现有对象，把活动移出主机文件观察面。勒索要求、算法和文件后缀不构成匿迹证据。", "An adversary denying reading of formerly usable data through unauthorized encryption and key control is Impact. Niji adapts the formal scope to two independently supported stealth designs: sparse within-file rewriting weakens whole-file and write signals, or valid cloud credentials cause a storage service to re-encrypt existing objects under a customer key, moving activity outside host file observation. Ransom demands, ciphers, and file suffixes are not stealth evidence."),
     B("直接对象是仍存在但在组织正常密钥上下文中不可读的内容或对象版本；数据删除归 T1485，磁盘擦除归 T1561，恢复抑制归 T1490，选择性跳过目标与来宾观察域隔离沿用既有 Niji 分类。ATT&CK T1486 无子项，Niji 两个子项来自独立匿迹变量研究。", "The direct object is surviving content or an object version unreadable under normal organizational key custody. Data deletion belongs to T1485, disk wiping to T1561, recovery inhibition to T1490, and selective target skipping and guest observation-domain isolation remain with existing Niji owners. ATT&CK T1486 has no children; its two Niji children arise from independent stealth-variable research."),
     ["REF-000658", "REF-000659", "REF-000660", "REF-000661", "REF-000663"], "NJT-0157")]
for attack, name, confidence, rationale, scope, refs, result in DECISIONS:
    write(f"{DECISION_ROOT}/DEC-TA0040-{attack}.yaml", {
        "schema_version": "1.1.0", "type": "technique-decision", "id": f"DEC-TA0040-{attack}",
        "tactic_ref": "TA0040", "candidate": {"source_type": "attack", "source_attack_id": attack,
            "source_attack_version": "19.1", "name_en": name["en"], "name_zh": name["zh"]},
        "decision": "adapt", "rationale_zh": rationale["zh"], "rationale_en": rationale["en"],
        "scope_notes_zh": scope["zh"], "scope_notes_en": scope["en"],
        "gap_statement_zh": None, "gap_statement_en": None,
        "original_attack_subtechniques_imported": False, "resulting_technique_ref": result,
        "evidence_refs": refs, "confidence": confidence,
        "review": {"status": "review", "authors": ["Niji Matrix Research"], "reviewers": [],
            "review_notes_zh": "证据、准入和原生分类经首批主审收敛；机器与双语 Web 验收后仍需人工领域评审。",
            "review_notes_en": "Batch-one primary review converged evidence, admission, and native taxonomy; human domain review remains after machine and bilingual Web gates."}})

def mechanism(ref, role, summary, analysis, refs, confidence):
    return {"mechanism_ref": ref, "role": role, "summary": summary,
            "analysis": analysis, "evidence_refs": refs, "confidence": confidence}


def defense(strategies, mitigations):
    return {"detections": {"coverage": "available", "strategy_refs": strategies},
            "mitigations": {"coverage": "available", "mitigation_refs": mitigations}}


def context(scenario, attacker, defender):
    return {"application_scenarios": scenario,
            "threat_model": {"attacker_model": attacker, "defender_model": defender}}


"""Impact data destruction: deletion decision and service execution are a single mechanism.
Direct overwrite stays a boundary comparator until its separate stealth claim is evidenced.
"""
T1485_DIR = "matrix/tactics/TA0040-impact/techniques/NJT-0156-data-destruction"
write(f"{T1485_DIR}/technique.yaml", {
    "schema_version": "2.0.0", "type": "technique", "id": "NJT-0156",
    "name": B("数据销毁", "Data Destruction"),
    "summary": B("攻击者使业务数据失去原有用途，并利用破坏决策与后续服务执行的分离增加归因难度。", "Adversaries make business data unusable and separate the destructive decision from later service execution to complicate attribution."),
    "aliases": [],
    "classification": {"tactic_refs": ["TA0040"], "origin": {"kind": "attack-adapted", "source_attack_id": "T1485", "source_attack_version": "19.1"}, "decision_ref": "DEC-TA0040-T1485"},
    "definition_and_concept": PP(
        ("数据销毁是攻击者删除或覆写可识别的文件、数据对象或其有效内容，使业务数据不能继续按原用途读取和处理的影响行为。其结果可以是仍有旧版本可恢复的当前视图缺失，也可以是现存副本无法补救的内容损坏；具体删除命令、扩展名和存储产品都不是概念单位。", "Data Destruction removes or overwrites identifiable files, objects, or useful content so business data cannot continue to be read or processed as intended. The result may be absence from the current view with an older version still recoverable, or content damage that surviving copies cannot repair. A deletion command, extension, or storage product is not the conceptual unit."),
        ("本矩阵关注攻击者怎样让破坏的原始决策与守方首先看到的数据损失脱节。直接批量删除和覆写界定父行为，但只有其实施方式有可支持的匿迹因果链时才属于正式匿迹研究对象；夜间执行、使用系统命令或备份薄弱本身不足以证明这种设计。", "The Niji subject is how an adversary separates the original destructive decision from the loss first observed by defenders. Direct bulk deletion and overwrite define the parent behavior, but only an implementation with a supported stealth causal chain enters the formal stealth analysis. Nighttime execution, native commands, or weak backup alone do not establish that design.")),
    "stealth_characteristics": PP(
        ("攻击者若先改变数据保留规则，再由存储服务异步执行对象过期，单次控制面写入会变成稍后由服务主体产生的大量结果事件。只看对象数据事件或一个短窗口的防守方可能把正常到期当作原因，无法从每条对象事件直接找到写规则的人；这种分离改变的是归因路径，不会让数据损失本身消失。", "When an adversary first changes retention rules and a storage service later expires objects asynchronously, one control-plane write becomes many later result events under a service principal. A defender watching only object data events or one short window may treat routine expiry as the cause and cannot identify the rule writer from each object event. The split changes the attribution path; it does not erase the loss."),
        ("规则差分、配置变更身份、生命周期通知、桶与对象键、删除标记、受保护版本和业务读取失败仍可串联。若控制面配置快照与服务结果被长期关联，匿迹优势会缩小；直接密集删除或覆写通常另有明显文件访问和业务中断信号，不能被推定具有同样观察分离。", "Rule diffs, configuration-change identity, lifecycle notifications, bucket and object keys, delete markers, protected versions, and failed business reads remain joinable. Long-horizon correlation between configuration snapshots and service outcomes weakens the stealth effect. Concentrated direct deletion or overwrite usually has conspicuous file-access and service-disruption signals and cannot be assumed to create the same observation split.")),
    "scope_boundary_definition": PP(
        ("纳入攻击者使业务文件或对象失去用途并能证明破坏实施改变守方观察方式的行为。判断损失时要查明对象版本：删除标记可能只隐藏当前视图，旧版本仍可恢复；非版本化对象到期或内容覆写则可能产生更重损失。对恢复程度的判断须与攻击者意图和匿迹效果分开记录。", "Include adversary actions that make business files or objects unusable and have a demonstrable change to defender observation. Determine version state before describing loss: a delete marker may only hide the current view while an older version remains, whereas unversioned expiry or content overwrite may cause greater loss. Record recoverability separately from adversary intent and stealth effect."),
        ("删除攻击工具或日志以清理痕迹归 TA0005；加密且以密钥控制阻碍读取归 T1486；磁盘扇区或引导结构擦除归 T1561；快照和恢复副本抑制归 T1490；数据仍可用但值遭篡改归 T1565。获批保留期届满、容量清理、误删和备份轮转可能产生相似事件，必须结合审批、变更主体、规则覆盖和业务结果识别。", "Deleting attacker tools or logs to clean traces belongs to TA0005; encryption denying reading through key custody belongs to T1486; disk-sector or boot-structure wiping to T1561; snapshot and recovery-copy suppression to T1490; and malicious changes to still-usable values to T1565. Approved retention expiry, capacity cleanup, accidental deletion, and backup rotation can resemble these events, so classification needs approval, change actor, rule scope, and business outcome.")),
    "application_scenarios_and_threat_model": context(
        P("在控制业务数据桶的生命周期配置后，攻击者可扩大删除规则的前缀或标签范围，或缩短当前及非当前版本的保留期，让服务在下一轮评估中清除符合条件的对象。该路径适用于无需逐一调用对象删除 API、却能等待服务执行的破坏；异步调度、版本控制与对象锁决定实际影响。", "After gaining control over a business-data bucket's lifecycle configuration, an adversary can broaden a deletion rule's prefix or tag scope or shorten current and noncurrent version retention, letting the service remove eligible objects at a later evaluation. This path suits destruction without per-object delete calls when the actor can wait for service execution. Asynchronous scheduling, versioning, and Object Lock determine the actual impact."),
        P("攻击者需要修改目标桶生命周期规则的权限、对关键对象范围的了解以及让规则保持生效的时间。在 AWS 实例中这要求生命周期配置权限而非逐对象删除权限。错误的过滤条件、配置被及时还原、受保护旧版本或保留锁都会缩小损失，也使单凭对象缺失难以证明永久毁损。", "The adversary needs permission to alter the target bucket's lifecycle rule, knowledge of critical object scope, and time for the rule to remain active. In the AWS instance this requires lifecycle-configuration authority rather than per-object delete permission. Wrong filters, prompt rollback, protected prior versions, or retention locks reduce loss and make permanent destruction harder to infer from object absence alone."),
        P("防守方可取得控制面管理事件、保存前后生命周期规则、对象过期通知或 EventBridge 结果、对象版本及业务读取情况。按桶、规则、过滤器、身份和时间跨平面关联才能从服务主体回溯原始写入者；若未保留旧规则或仅监测用户发起的对象 API，归因链会断裂。通知未开启和服务执行延迟也是明确的观察限制。", "Defenders can collect management events, before-and-after lifecycle rules, object-expiry notifications or EventBridge outcomes, object versions, and business-read results. Joining bucket, rule, filter, identity, and time across planes is needed to trace a service-principal outcome back to the writer. Missing historical rules or monitoring only user-initiated object APIs breaks that lineage; disabled notifications and service delay are further visibility limits.")),
    "stealth_mechanisms": [mechanism("NM-BT", "primary", B("服务执行将规则写入者与对象损失事件分离", "Service execution separates the rule writer from object-loss events"),
        P("攻击者改写对象到期规则，把破坏决策留在配置事件中，随后存储服务按自身调度和身份生成对象删除或标记事件。对象侧监测看到服务执行而缺少原操作者和规则差分，单平面分析因而难以解释损失的发起原因；连接管理事件、历史规则与结果事件可重新恢复这条因果链。", "An adversary rewrites an object-expiry rule, leaving the destructive decision in a configuration event. The storage service later produces deletion or marker events on its own schedule and under its own identity. Object-side monitoring sees service execution without the original actor or rule diff, making the initiating cause harder to explain from one plane. Joining management events, historical rules, and outcomes restores the chain."),
        ["REF-000648", "REF-000649", "REF-000650", "REF-000651", "REF-000513"], "medium")],
    "subtechnique_taxonomy": {"narrative": PP(
        ("当前原生分类只保留委托执行式数据销毁：其变量是破坏规则写入者与数据删除执行者在身份、时间及遥测平面上的分离。ATT&CK 的生命周期功能提供实例，但子技术边界不按云平台或规则名称划分；直接删除、覆写及删除对象类型属于父级行为，尚无证据证明其他独立匿迹轴。", "The current native taxonomy retains only Delegated-Execution Data Destruction. Its variable is separation of the destructive rule writer from the data-deletion executor across identity, time, and telemetry plane. ATT&CK's lifecycle feature supplies an example, but neither platform nor rule name defines the child. Direct deletion, overwrite, and object type remain parent behavior without evidence for another independent stealth axis."),
        ("选择性保留关键目标已有 NJT-0117 负责，来宾传感器隔离已有 NJS-0111-004 负责；慢速销毁和保留路径的覆写仍待结论级证据。一个真实事件可能结合这些行为，但组合不应消除各自不同的直接对象和防守关联方法。", "NJT-0117 owns selective preservation, and NJS-0111-004 owns guest sensor isolation. Slow destruction and namespace-preserving overwrite remain deferred pending conclusion-level evidence. One incident can combine these behaviors, but co-occurrence does not erase their different direct objects and defensive joins.")),
        "coverage": "established", "subtechnique_refs": ["NJS-0156-001"]},
    "defense": defense(["DET-000173", "DET-000174"], ["MIT-000158"]),
    "evidence": {"claim_refs": ["CLM-000778", "CLM-000779", "CLM-000780"], "case_refs": [],
                 "reference_refs": ["REF-000647", "REF-000648", "REF-000649", "REF-000650", "REF-000651", "REF-000652", "REF-000653", "REF-000654", "REF-000655", "REF-000656", "REF-000657", "REF-000379", "REF-000513"]},
    "research": {"limitations": PP(
        ("官方资料确证生命周期规则权限、异步执行和事件形态，Palo Alto Networks 的威胁分析支持间接删除如何绕开仅看对象访问的监测；现有公开资料没有把某个真实受害者完整追溯为恶意规则写入、服务过期和业务不可用。故该子技术的恶意实例为受约束的攻击路径推断，不能填造受害案例。", "Official documentation establishes lifecycle authority, asynchronous execution, and event shapes, while Palo Alto Networks' threat analysis supports how indirect deletion evades object-access-only monitoring. Public evidence does not trace one real victim end to end from malicious rule write through service expiry to business outage. The malicious instance is therefore a bounded attack-path inference, not a fabricated victim case."),
        ("实际删除时点、可恢复性和漏检与否取决于桶配置、版本控制、对象锁、通知和跨平面日志留存。4663 删除权限事件也可能反映重命名，必须用完成事件或对象状态核实；父级 Windows 文件分析不能被当作云生命周期子项的直接证据。", "Actual deletion timing, recovery, and missed detection depend on bucket configuration, versioning, Object Lock, notifications, and cross-plane log retention. A Windows 4663 delete-access event may also indicate rename and needs a completion event or object-state check. The parent-level Windows file analytic is not direct evidence for the cloud lifecycle child."))},
    "lifecycle": life()})

write(f"{T1485_DIR}/subtechniques/NJS-0156-001-delegated-execution-data-destruction/subtechnique.yaml", {
    "schema_version": "2.0.0", "type": "evasion-subtechnique", "id": "NJS-0156-001",
    "parent_ref": "NJT-0156", "name": B("委托执行式数据销毁", "Delegated-Execution Data Destruction"),
    "summary": B("攻击者改写销毁规则，让存储服务稍后删除目标对象，使原始操作者与损失事件分离。", "An adversary changes a destructive rule so a storage service later deletes target objects, separating the original operator from the loss event."),
    "aliases": [], "lineage": {"attck_subtechnique_inherited": False},
    "definition_and_concept": PP(
        ("委托执行式数据销毁是攻击者更改会被平台自动消费的对象删除规则，将后续数据移除交给存储服务执行。直接影响仍是业务对象无法按原用途读取；分类变量是规则写入者与实际删除者在身份、时点和遥测平面上的分离，不是对象存储介质或生命周期产品功能本身。", "Delegated-Execution Data Destruction is an adversary change to an object-deletion rule automatically consumed by a platform, leaving subsequent data removal to the storage service. The impact remains loss of business use; the classification variable is separation of rule writer and actual deleter across identity, timing, and telemetry plane, not the storage medium or lifecycle feature itself."),
        ("目前有结论级支持的实现是对象存储生命周期配置：一个已授权配置写入可以覆盖许多对象，而结果由服务异步产生。不能从这一实现推断所有策略引擎都有相同审计语义，正式范围由可证明的决策到执行因果链限定。", "The conclusion-level supported implementation is object-storage lifecycle configuration: one authorized configuration write can cover many objects, while the service creates outcomes asynchronously. This example does not establish identical audit semantics across policy engines. A demonstrable decision-to-execution chain bounds the formal scope.")),
    "stealth_characteristics": PP(
        ("委托执行式数据销毁把一次攻击者规则变更转化成后来由服务主体产生的过期事件。仅按对象删除 API 告警的防守方可能看不到逐对象的攻击者调用，或从结果事件只读到服务身份；历史规则、变更身份、生命周期原因、对象键与版本仍能恢复归因。", "Delegated-Execution Data Destruction turns one adversary rule change into later expiry events under a service principal. Defenders alerting only on object-delete APIs may see no per-object attacker call, or only the service identity in result events. Historical rules, change identity, lifecycle reason, object key, and version can still restore attribution."),
        ("服务调度还使配置写入与损失落在不同观察窗口，造成事前风险与事后故障看似分离。事件不会必然缺失：开启了 CloudTrail 生命周期数据事件、EventBridge 或通知并保存规则快照时，这种分离可被跨平面关联反制。", "Service scheduling can place configuration change and loss in different observation windows, making a pre-impact risk and later outage appear unrelated. Events are not necessarily absent: CloudTrail lifecycle data events, EventBridge or notifications, and preserved rule snapshots allow cross-plane correlation to counter the split.")),
    "scope_boundary_definition": PP(
        ("只有攻击者更改了已启用规则，使关键对象或版本更早到期，并能连接之后由平台执行的删除，才纳入本项。正常保留到期、获批变更、直接 DeleteObject 和单独删除备份均不属于它。对象返回 404 时必须检查删除标记与旧版本，不能自动宣称永久损失。", "Include only an adversary change to an enabled rule that makes critical objects or versions expire earlier and can be joined to later platform deletion. Ordinary retention expiry, approved changes, direct DeleteObject, and separate backup deletion fall outside this child. A 404 requires checking delete markers and prior versions rather than assuming permanent loss."),
        ("该子项不按云服务商、桶类型、前缀或保留天数拆分；若攻击者仅设置规则而没有对象达到条件，证据最多支持企图或前期配置异常。与 T1486 的客户密钥服务端重加密不同，本项的结果是服务删除或隐藏对象，不是以新密钥保留密文。", "The child is not split by provider, bucket type, prefix, or retention days. If no object becomes eligible after the rule change, evidence supports an attempt or pre-impact configuration anomaly at most. Unlike T1486 customer-key service re-encryption, this outcome removes or hides objects rather than preserving ciphertext under a new key.")),
    "application_scenarios_and_threat_model": context(
        P("攻击者拥有关键业务桶的生命周期配置权却未必有逐对象删除权时，可以扩大前缀或标签过滤器、压短当前或非当前版本到期条件，让服务在下一次评估中移除目标。防守方按用户发起的大量删除请求设阈值时，规则变更可能先于值班窗口而服务事件后来才出现。", "An adversary with lifecycle configuration authority over a critical business bucket, but not necessarily per-object delete rights, can broaden prefix or tag filters or shorten current or noncurrent version expiry so the service removes targets at its next evaluation. A defender thresholding mass user-initiated delete calls may see the rule change in one shift and service outcomes in another."),
        P("攻击者需要改写生命周期规则的权限、知道关键对象过滤范围并容忍非即时结果。版本控制、对象锁、不同对象的资格状态和及时回滚都限制影响；恶意规则若被审计或审批拦截，结果可能尚未发生。", "The attacker needs lifecycle-rule edit authority, knowledge of critical object filters, and tolerance for delayed results. Versioning, Object Lock, object eligibility, and prompt rollback limit impact. If audit or approval catches the malicious rule, an outcome may not yet have occurred."),
        P("防守方应保留 CloudTrail 管理事件、规则前后配置快照、生命周期结果事件、版本清单和受影响业务对象清单，按桶、过滤器、规则版本和时间连接。仅保留对象数据事件无法重建写规则主体；仅有规则写入也不能断言对象已损失。服务异步执行和缺失通知会降低精确关联度。", "Defenders should retain CloudTrail management events, before-and-after rule snapshots, lifecycle result events, version inventories, and lists of affected business objects, joining by bucket, filter, rule revision, and time. Object data events alone cannot reconstruct the rule writer; a rule write alone does not prove object loss. Asynchronous service action and absent notifications reduce join precision.")),
    "stealth_mechanisms": [mechanism("NM-BT", "primary", B("存储服务执行掩盖先前规则写入主体", "Storage-service execution obscures the earlier rule writer"),
        P("攻击者扩大或提前对象到期规则，控制面记录其配置写入，随后存储服务在另一时间以服务身份产生删除或删除标记。只看结果事件的防守方失去原操作者和规则意图，跨平面归因成本上升；把规则差分、批准记录和生命周期原因连至对象版本即可恢复链条。", "The adversary broadens or accelerates an object-expiry rule, leaving a control-plane configuration write. Later, the storage service creates deletion or delete-marker events under its own identity. A defender seeing only outcomes lacks the original operator and rule intent, raising cross-plane attribution cost; joining rule diffs and approvals to lifecycle reasons and object versions restores the chain."),
        ["REF-000648", "REF-000649", "REF-000650", "REF-000651", "REF-000513"], "medium")],
    "defense": defense(["DET-000174"], ["MIT-000158"]),
    "evidence": {"claim_refs": ["CLM-000779", "CLM-000780"], "case_refs": [],
                 "reference_refs": ["REF-000648", "REF-000649", "REF-000650", "REF-000651", "REF-000652", "REF-000653", "REF-000654", "REF-000655", "REF-000513"]},
    "research": {"limitations": PP(
        ("AWS 文档能确认服务执行、通知和版本结果，Palo Alto Networks 的分析支持恶意规则如何避开仅监视直接对象访问的逻辑；它不是已披露受害事件。尚不能声称实际受害者的业务损失、攻击者主观意图或通用漏检率，故不设子项案例引用。", "AWS documents service execution, notifications, and version effects, while Palo Alto Networks' analysis supports how a malicious rule can evade direct-object-access-only monitoring. It is not a disclosed victim incident. Actual victim loss, subjective intent, and a general miss rate cannot be asserted, so this child has no case reference."),
        ("规则资格、执行延迟和是否产生永久删除因桶的版本与保留设置而异；管理事件字段和通知的规则标识也要在目标环境验证。若守方保留规则修订并观察服务事件，这一分类仍成立，但预期匿迹收益会显著降低。", "Rule eligibility, execution lag, and permanent removal vary with bucket version and retention settings. Management-event fields and notification rule identifiers require validation in the target environment. The taxonomy remains valid when defenders retain revisions and observe service events, but expected stealth benefit falls substantially."))},
    "lifecycle": life()})

T1486_DIR = "matrix/tactics/TA0040-impact/techniques/NJT-0157-data-encrypted-for-impact"
write(f"{T1486_DIR}/technique.yaml", {
    "schema_version": "2.0.0", "type": "technique", "id": "NJT-0157",
    "name": B("为影响而加密数据", "Data Encrypted for Impact"),
    "summary": B("攻击者使原本可读的数据因未授权加密及密钥控制而不可读，并改变加密覆盖或执行位置以削弱早期发现。", "Adversaries deny reading through unauthorized encryption and key control while changing encryption coverage or execution location to weaken early detection."),
    "aliases": [],
    "classification": {"tactic_refs": ["TA0040"], "origin": {"kind": "attack-adapted", "source_attack_id": "T1486", "source_attack_version": "19.1"}, "decision_ref": "DEC-TA0040-T1486"},
    "definition_and_concept": PP(
        ("为影响而加密数据是攻击者对原本供业务读取的内容实施未授权加密或重加密，并控制或隐瞒当前状态所需解密密钥，使合法用户无法按原用途使用数据。判断单位是可读状态和密钥归属的变化；文件或对象仍可能存在，服务也可能正常响应，但组织原有密钥和工作流无法恢复当前内容。", "Data Encrypted for Impact is unauthorized encryption or re-encryption of content previously usable by business workflows, with the adversary controlling or withholding the key needed for the current state. The unit of analysis is changed readability and key custody. Files or objects may remain, and a service may respond normally, while the organization's existing keys and workflow cannot recover current content."),
        ("Niji 的匿迹问题是加密过程如何削弱早期观察，而不是勒索通知是否出现。文件内局部改写会使写入量和整文件密文外观下降；由存储服务在客户密钥下重加密则把执行位置移出主机文件传感器。权限取得、载荷部署、后续删除备份和勒索谈判可构成同一行动链，却不是此父技术的直接对象。", "The Niji stealth question is how the encryption process weakens early observation, not whether a ransom note appears. Regional within-file rewriting lowers write volume and whole-file ciphertext appearance; storage-service re-encryption under a customer key moves execution outside host file sensors. Privilege acquisition, payload deployment, later backup deletion, and extortion can form one operation but are not this parent's direct object.")),
    "stealth_characteristics": PP(
        ("大规模全文件加密常造成密集文件改写、明显内容统计变化和快速业务故障。稀疏加密保留大量明文区段，降低整文件熵和短窗写入量的判别力；服务端重加密保留对象键并借有效身份调用正常对象复制 API，使主机端点没有对应加密进程。两者改变的观察面不同，均不消除数据不可读的结果。", "Mass full-file encryption commonly creates dense rewrites, conspicuous content-statistic changes, and rapid business failures. Sparse encryption preserves much plaintext, weakening whole-file entropy and short-window write-volume discrimination. Service-side re-encryption preserves object keys and uses normal copy APIs under a valid identity, leaving no corresponding host encryptor process. These change different observation surfaces without removing the unreadable-data outcome."),
        ("同一进程跨多个业务文件的写入、文件内被改变区域、解析失败、对象数据事件中的客户密钥参数、对象版本和后续读失败仍可调查。若防守方只用整文件阈值或只部署主机 EDR，早期信号会不足；保留前版本、内容抽样及云数据事件时，攻击者的低可见设计会留下可以关联的反证。", "One process writing many business files, changed file regions, parse failures, customer-key parameters in object data events, object versions, and later failed reads remain investigable. Whole-file thresholds or host-only EDR may have too little early signal. Preserved prior versions, content sampling, and cloud data events provide correlatable counterevidence to the lower-visibility designs.")),
    "scope_boundary_definition": PP(
        ("纳入攻击者有意造成的密文状态转换：数据先前可由组织正常密钥读取，随后当前文件或对象版本因加密与密钥归属改变而失去合法可读性，并有证据表明覆盖或执行位置改变了守方观察。单个高熵文件、加密 API、SSE-C 参数或勒索字条都不能单独证明这条链。", "Include adversary-caused ciphertext state changes where data was readable under normal organizational keys and the current file or object version later becomes unreadable through encryption and changed key custody, with evidence that coverage or execution location changed defender observation. One high-entropy file, cryptographic API call, SSE-C parameter, or ransom note alone cannot establish this chain."),
        ("删除或覆写原件造成的数据消失另归 T1485，磁盘内容或结构擦除归 T1561，恢复副本及快照抑制归 T1490；仅改 ACL 或 KMS 授权而不改密文属于访问控制问题。正常静态加密、组织仍掌握密钥的批准迁移和外传前打包加密是反例。选择性跳过文件及来宾虚拟机观察隔离分别由 NJT-0117、NJS-0111-004 负责。", "Deletion or overwrite removing the original belongs separately to T1485, disk-content or structure wiping to T1561, and recovery-copy or snapshot inhibition to T1490. Changing ACL or KMS grants without changing ciphertext is an access-control issue. Ordinary at-rest encryption, approved migration retaining organizational key custody, and encryption solely packaging exfiltrated data are counterexamples. NJT-0117 and NJS-0111-004 own selective file skipping and guest-VM observation isolation respectively.")),
    "application_scenarios_and_threat_model": context(
        P("在终端或文件服务器，勒索载荷可间隔改写文档或业务数据文件中的区域，让应用打开失败而整文件仍留有大量原始内容。在云对象存储，攻击者可用已窃有效凭据通过服务端客户密钥重加密已有对象，使对象名仍在但正常读取者没有所需密钥。两者都可能伴随横向移动或备份损伤，不能用伴随行为代替加密证据。", "On endpoints or file servers, an encryptor may rewrite spaced regions of documents or business data so applications fail to open them while much original content remains. In object storage, an actor with stolen valid credentials can have the service re-encrypt existing objects under a customer key, preserving object names while normal readers lack the key. Lateral movement or backup damage may accompany either path but cannot substitute for encryption evidence."),
        P("攻击者需要写入目标文件内容，或有权读取并覆写已有对象，同时控制区域改写布局或服务端客户密钥。局部改写太少可能无法破坏业务解析；在当前 AWS S3 配置中，SSE-C 还必须被目标桶允许，或者攻击者需另有修改桶加密配置的权限。进程来源、文件写入、API 主体和对象版本仍形成成本与暴露面。", "The attacker needs authority to write target file content or read and overwrite existing objects, plus control over regional rewrite layout or the service-side customer key. Too little regional change may not disrupt business parsing. In current AWS S3 configurations, the target bucket must also permit SSE-C or the actor needs separate authority to change bucket encryption configuration. Process lineage, file writes, API principals, and object versions remain costs and traces."),
        P("防守方可能有端点文件事件、进程身份、可安全比较的前版本、对象数据事件、桶加密配置和业务读结果。文件事件本身不提供区域熵，主机 EDR 也不能见到服务端对象重加密；须分别建立进程到文件结构差异和云主体到密钥参数、对象版本的关联。未管理文件共享、未启用数据事件及获批主体被盗均降低证据强度。", "Defenders may have endpoint file events, process identity, safely comparable prior versions, object data events, bucket encryption configuration, and business-read results. File events alone do not provide regional entropy, and host EDR cannot see service-side object re-encryption. Separate joins are needed from process to structural file difference and from cloud principal to key parameter and object version. Unmanaged shares, disabled data events, and compromise of an approved principal weaken confidence.")),
    "stealth_mechanisms": [
        mechanism("NM-FD", "primary", B("保留明文区域削弱整文件密文与写入特征", "Preserved plaintext regions weaken whole-file ciphertext and write features"),
            P("攻击者只改写文件内部间隔区域，因而每个文件的写入字节与整文件密文比例低于完整加密。依赖总写入速率或整文件熵的检测较难把早期操作与合法批量编辑区分；按同一进程聚合多文件修改并对前后版本做区域比较仍能显露重复的密文布局和读取失败。", "An adversary rewrites spaced regions within files, lowering written bytes and the whole-file ciphertext fraction relative to full encryption. Detectors relying on total write rate or whole-file entropy have less ability to separate early activity from bulk editing. Grouping modifications by process and comparing regions of prior and current versions still exposes repeated ciphertext layout and failed reads."), ["REF-000659"], "high"),
        mechanism("NM-BT", "secondary", B("服务端重加密离开主机文件观察面", "Service-side re-encryption leaves host file-observation scope"),
            P("持有有效对象权限的攻击者请求存储服务以客户提供密钥覆写已有对象，加密计算和版本变化发生在服务数据面而非受害主机文件系统。主机传感器因此不见对应的大量文件写入，若未采集对象数据事件就难以发现当前版本的密钥归属变化；CopyObject 序列、客户密钥参数与版本仍可由云侧审计重建。", "An actor with valid object authority asks a storage service to overwrite existing objects under a customer-provided key. Encryption and version change occur in the service data plane rather than a victim host filesystem. Host sensors therefore see no corresponding mass file writes, and without object data events the changed key custody of current versions is hard to detect. CopyObject sequences, customer-key parameters, and versions remain reconstructable in cloud audit."), ["REF-000660", "REF-000661", "REF-000663"], "high")],
    "subtechnique_taxonomy": {"narrative": PP(
        ("文件内稀疏加密按单一文件中被改写区段的密度和布局划界，改变端点写入与内容统计；客户密钥服务端重加密按执行权限及密钥归属移入存储服务划界，改变主机与对象数据面的观察关系。两个变量可共现，但一个不蕴含另一个，检测数据和缓解施加点也不同。", "Sparse In-File Encryption is bounded by the density and layout of rewritten regions within one file, changing endpoint write and content statistics. Customer-Key Service-Side Re-encryption is bounded by execution authority and key custody moving into a storage service, changing host-versus-object-data-plane observation. The variables can co-occur, but neither implies the other, and their detection data and control points differ."),
        ("算法、扩展名、恶意软件家族、文件类别和平台不构成原生子项；选择性不处理关键目标与在无宿主传感器的来宾运行分别归既有 NJT-0117 和 NJS-0111-004。ATT&CK T1486 没有子项，本分类来自开放搜索和独立技术证据，不存在导入关系。", "Cipher, extension, malware family, file category, and platform do not define native children. NJT-0117 owns selective preservation and NJS-0111-004 owns execution in a guest outside host sensing. ATT&CK T1486 has no children; this taxonomy arises from open search and independent technical evidence, not import.")),
        "coverage": "established", "subtechnique_refs": ["NJS-0157-001", "NJS-0157-002"]},
    "defense": defense(["DET-000175", "DET-000176"], ["MIT-000115", "MIT-000159"]),
    "evidence": {"claim_refs": ["CLM-000781", "CLM-000782", "CLM-000783"], "case_refs": ["CASE-000216"],
                 "reference_refs": ["REF-000658", "REF-000659", "REF-000660", "REF-000661", "REF-000662", "REF-000663", "REF-000654", "REF-000475"]},
    "research": {"limitations": PP(
        ("SentinelOne Labs 的样本分析证明几种勒索程序采用间歇区段改写，却没有给出适用于所有文件类型和传感器的通用阈值。AWS CIRT 的报告确认恶意 SSE-C 大量覆写，但未披露每个客户的完整读取测试或主观匿迹动机；应分别报告样本事实、服务实现和检测推断。", "SentinelOne Labs' sample analysis establishes regional rewriting in several ransomware families but no universal threshold across file types or sensors. AWS CIRT confirms malicious mass SSE-C overwrites without publishing each customer's full read test or subjective stealth motive. Sample facts, service behavior, and detection inference must be reported separately."),
        ("缺少前版本时，端点文件事件最多提示异常写入，不能证明局部密文布局；缺少对象数据事件时，主机安静不能证明服务端未加密。2026 年后 S3 的 SSE-C 默认阻止使云路径依赖具体桶配置或额外配置权限，受保护旧版本可能恢复数据，但不能否认当前版本短时不可用。", "Without a prior version, endpoint file events suggest abnormal writes at most and cannot prove sparse ciphertext layout. Without object data events, a quiet host cannot rule out service-side encryption. S3's post-2026 default SSE-C block makes the cloud path contingent on bucket configuration or additional configuration authority. Protected prior versions may aid recovery without negating a temporary current-version outage."))},
    "lifecycle": life()})

write(f"{T1486_DIR}/subtechniques/NJS-0157-001-sparse-in-file-encryption/subtechnique.yaml", {
    "schema_version": "2.0.0", "type": "evasion-subtechnique", "id": "NJS-0157-001",
    "parent_ref": "NJT-0157", "name": B("文件内稀疏加密", "Sparse In-File Encryption"),
    "summary": B("攻击者只加密每个目标文件的间隔区段，使数据不可读而保留较低写入量和较多原始内容。", "An adversary encrypts spaced regions within each target file, denying use while retaining lower write volume and more original content."),
    "aliases": [], "lineage": {"attck_subtechnique_inherited": False},
    "definition_and_concept": PP(
        ("文件内稀疏加密是在每个被选文件内部改写间隔分布的字节区域，同时保留其他区域的原始内容，使文件对原业务程序失效。其稳定控制变量是单一文件的区域覆盖密度和布局；处理了多少文件、选择何种扩展名或密码算法只是另外的实施参数。", "Sparse In-File Encryption rewrites spaced byte regions inside each selected file while preserving other original regions, making the file unusable to its business reader. Its stable control variable is regional coverage density and layout within one file; the number of files, selected extensions, and cipher are separate implementation parameters."),
        ("攻击者的取舍是以更少写入换取足够业务破坏：过少区域变化可能保留可读性，过多则接近全文件加密并恢复强烈的 I/O 和整文件密文信号。研究对象是这种对痕迹强度与影响结果同时施加约束的设计。", "The attacker trades lower write volume for enough business damage. Too little regional change may leave the file usable; too much approaches full-file encryption and restores strong I/O and whole-file ciphertext signals. The object of study is this design constraining trace strength and impact together.")),
    "stealth_characteristics": PP(
        ("文件内稀疏加密使文件保留大块原始明文而只在指定区域产生密文，因而总写入量和整文件熵变化可低于完整加密。依赖整文件统计或单次高 I/O 峰值的监测更难在影响完成前识别它；修改区域、同一进程跨文件重复的布局和业务解析失败仍会留下证据。", "Sparse In-File Encryption leaves large original plaintext regions and ciphertext only in selected spans, so total writes and whole-file entropy shifts can be lower than with complete encryption. Monitoring based on whole-file statistics or one high-I/O burst becomes less discriminating before impact completes. Modified regions, repeated layouts across files by one process, and business parse failure still leave evidence."),
        ("该子项降低的是每个文件内部的可见加密比例，而不是不处理某些文件。若防守方保存受保护前版本或诱饵文件并安全比较区域，低总体熵也无法掩盖结构性差分；没有这种内容证据时应只报告疑似加密写入。", "This child lowers the visible encrypted proportion inside each file rather than skipping some files. Safe regional comparison against protected prior versions or canaries can recover the structural differential despite low overall entropy. Without that content evidence, report suspected encryption writes rather than a confirmed sparse layout.")),
    "scope_boundary_definition": PP(
        ("纳入原本可用的文件被未授权加密为明文与密文交错的状态、正常读取受阻，且改写布局与更弱整文件或写入信号相连的情况。常规分块加密、压缩、数据库页更新以及获批重加密会产生局部变化，必须结合写入者、前版本、业务用途和密钥归属排除。", "Include previously usable files transformed without authorization into interleaved plaintext and ciphertext, with impaired normal reading and a layout tied to weaker whole-file or write signals. Ordinary chunked encryption, compression, database page updates, and approved rekeying can also change regions; writer identity, prior version, business use, and key custody are needed to exclude them."),
        ("只跳过完整文件、目录或主机以维持系统运行的行为属于 NJT-0117；使用虚拟机让宿主看不到进程属于 NJS-0111-004。稀疏布局可与这些行为共现，但子项的证据必须在单个受损文件内部，而不能由总体受损比例代替。", "Skipping entire files, directories, or hosts to maintain operation belongs to NJT-0117; using a VM to conceal processes from the host belongs to NJS-0111-004. Sparse layout may co-occur with either, but evidence for this child must be inside an affected file, not inferred from the overall fraction of damaged files.")),
    "application_scenarios_and_threat_model": context(
        P("勒索进程在终端或文件服务器遍历业务文件并仅改写各文件的间隔区段，可在短时间内令文档或其他结构化内容无法解析，同时避免全文件写入带来的巨大流量。即使本地日志只显示较低字节写入率，跨多个目录由同一进程修改业务文件仍可形成调查线索。", "An encryptor on an endpoint or file server can traverse business files and rewrite only spaced regions of each, quickly breaking documents or other structured content without full-file write traffic. Even if local logs show lower byte-write rates, one process modifying business files across directories remains an investigative lead."),
        P("攻击者需取得文件内容写权限，能选出足以破坏解析的区域，并允许读取、定位和重复写入所产生的进程痕迹。不同格式对局部损坏的容忍度不同，固定字节步长不保证对所有文件有效；该设计的低写入收益与破坏可靠性互相制约。", "The attacker needs file-content write authority, an ability to choose regions that disrupt parsing, and tolerance for process traces from reading, seeking, and repeated writing. File formats differ in their tolerance of local damage, so one byte stride does not work universally. Lower write volume and reliable damage constrain each other."),
        P("防守方按设备和进程唯一键关联多文件写入，再从受保护前版本或诱饵安全取得改写偏移、区域熵及解析结果。Microsoft DeviceFileEvents 能支持文件与进程关联，却不提供区域熵；若文件服务器未受管理、前版本不存在或文件本来已加密，子项判定会变弱。", "Defenders join multi-file writes by device and process unique key, then safely derive changed offsets, regional entropy, and parse results from protected prior versions or canaries. Microsoft DeviceFileEvents supports file and process correlation but does not supply regional entropy. An unmanaged file server, absent prior version, or already encrypted content weakens child classification.")),
    "stealth_mechanisms": [mechanism("NM-FD", "primary", B("保留明文区域降低整文件加密外观", "Preserved plaintext regions reduce whole-file encryption appearance"),
        P("攻击者把密文限制在间隔区域，每个文件仍包含大量原始字节，单文件总写入和整文件熵变化弱于全量加密。只比较整文件指标的守方更难把该变化与普通批量编辑区分，形成特征伪装；对同一写入者跨文件的偏移模式和局部内容差分进行检查仍可识别。", "The attacker confines ciphertext to spaced regions, leaving much original data in each file and reducing per-file writes and whole-file entropy change relative to full encryption. Defenders using only whole-file indicators have more difficulty separating it from bulk editing, producing feature disguise. Cross-file offset patterns and local content differences for the same writer remain detectable."), ["REF-000659"], "high")],
    "defense": defense(["DET-000175"], ["MIT-000115"]),
    "evidence": {"claim_refs": ["CLM-000782"], "case_refs": [], "reference_refs": ["REF-000659", "REF-000475", "REF-000662"]},
    "research": {"limitations": PP(
        ("SentinelOne Labs 观察了多个使用间歇加密的家族及具体区域模式，足以支持此变量的存在，但不能推出所有部分覆写都是恶意，亦无适用于所有文件格式和传感器的阈值。样本层面的匿迹意图描述与具体受害环境的检测成败应分开。", "SentinelOne Labs observed several families and regional patterns, supporting the variable's existence, but neither every partial overwrite is malicious nor one threshold fits all formats and sensors. Sample-level descriptions of evasion intent must be separated from detection outcomes in a particular victim environment."),
        ("区域比较需要可信前版本、受控诱饵或安全的内容抽样，大型文件会增加存储和隐私成本。仅有 DeviceFileEvents 时可以调查批量写入，但不能声称已观察到稀疏密文布局。", "Regional comparison needs a trusted prior version, controlled canary, or safe content sample and can raise storage and privacy costs for large files. DeviceFileEvents alone supports investigation of bulk writes but cannot establish observed sparse ciphertext layout."))},
    "lifecycle": life()})

write(f"{T1486_DIR}/subtechniques/NJS-0157-002-customer-key-service-reencryption/subtechnique.yaml", {
    "schema_version": "2.0.0", "type": "evasion-subtechnique", "id": "NJS-0157-002",
    "parent_ref": "NJT-0157", "name": B("客户密钥服务端重加密", "Customer-Key Service-Side Re-encryption"),
    "summary": B("攻击者借有效对象权限让存储服务用攻击者掌握的客户密钥重加密现有对象，移出主机文件监测范围。", "An adversary uses valid object authority to have a storage service re-encrypt existing objects under an attacker-held customer key, moving outside host file monitoring."),
    "aliases": [], "lineage": {"attck_subtechnique_inherited": False},
    "definition_and_concept": PP(
        ("客户密钥服务端重加密是攻击者使用有权读取和覆写对象的身份，让存储服务对已有对象产生一个以攻击者掌握的客户密钥保护的当前版本。原对象名和服务路径可保持正常，但组织缺少读取当前版本所需密钥；分类变量是加密执行主体和密钥归属从主机工作流移到对象服务，不是云供应商名称。", "Customer-Key Service-Side Re-encryption uses an identity authorized to read and overwrite objects to make a storage service create a current version protected by a customer key held by the attacker. Object names and service routes may remain normal while the organization lacks the key for current-version reading. The variable is the encryption executor and key custody moving from host workflow to object service, not a cloud vendor name."),
        ("当前结论级证据是 AWS CIRT 观察到的 SSE-C CopyObject 大量覆写。它证明该服务实例的行为和审计面，却不足以假定所有对象存储服务都有相同参数、默认许可或版本语义；其他平台须另证执行与观察差异。", "Current conclusion-level evidence is AWS CIRT's observed mass SSE-C CopyObject overwrites. It establishes that service instance and audit surface, not identical parameters, default permission, or version semantics in every object store. Other platforms need separate proof of the execution and observation difference.")),
    "stealth_characteristics": PP(
        ("客户密钥服务端重加密保留对象键和存储 API 的正常响应表象，却不会在受害主机产生同等规模的加密进程或文件改写。持有效凭据的 CopyObject 在操作类别上接近合法复制，主机侧或仅看管理事件的监控难以识别密钥归属变化；对象数据事件里的客户密钥算法参数、同主体大量覆写和新版本仍能暴露行为。", "Customer-Key Service-Side Re-encryption preserves object keys and an apparently normal storage API surface without a comparable encryptor process or file-write burst on victim hosts. CopyObject under valid credentials resembles authorized copying at the operation level, so host or management-only monitoring misses changed key custody. Customer-key algorithm parameters in object data events, mass same-principal overwrites, and new versions remain visible."),
        ("若目标桶维持 SSE-C 阻止状态，攻击路径会在写入前受限；若有例外或攻击者先改配置，解除阻止的配置事件又增加一个可见前驱。版本控制或对象锁可能保留旧版本，但无法凭此否定当前版本一度不可读。", "If the target bucket retains SSE-C blocking, the pathway is constrained before writes. An exception or attacker change to the setting adds an observable precursor configuration event. Versioning or Object Lock may preserve older versions without disproving that the current version was temporarily unreadable.")),
    "scope_boundary_definition": PP(
        ("纳入已有对象被未授权地由服务端重加密、当前密钥不在组织正常控制中且合法读取受阻，并能查明客户密钥请求和对象版本变化的情形。合规 SSE-C 且组织保有密钥、正常重密钥迁移、只改变 ACL 或 KMS 授权而没有重加密都不属于本项。", "Include unauthorized service-side re-encryption of existing objects where the current key is outside normal organizational custody and legitimate reading is impaired, with customer-key requests and object-version change established. Approved SSE-C with organizational key custody, normal rekeying, or changing only ACL or KMS grants without re-encryption falls outside this child."),
        ("攻击者若先通过 PutBucketEncryption 移除默认阻止，这只是前置配置变化；没有随后对象覆写不能宣称子项已完成。客户密钥参数本身也不证明密钥由攻击者掌握，需要批准作业、密钥治理和安全读取验证交叉确认。", "If an actor first removes a default block through PutBucketEncryption, that is a precursor configuration change. Without subsequent object overwrites, the child has not occurred. A customer-key parameter alone does not prove adversary key custody; approved jobs, key governance, and safe read tests must corroborate it.")),
    "application_scenarios_and_threat_model": context(
        P("AWS CIRT 报告攻击者取得客户有效凭据后，以 SSE-C CopyObject 重加密许多现有 S3 对象。当前 AWS 环境中，攻击者需选中允许 SSE-C 的桶，或另有权启用该类型，再批量覆写对象；防守方的主机文件改写告警不会覆盖这条服务端路径。", "AWS CIRT reported actors obtaining valid customer credentials and re-encrypting many existing S3 objects with SSE-C CopyObject. In current AWS environments, the actor needs a bucket permitting SSE-C or separate authority to enable it before bulk overwrites. Host file-rewrite alerts do not cover this service-side path."),
        P("攻击者需可读取并复制覆写目标对象，能提供并控制客户密钥，并了解桶是否阻止 SSE-C。2026 年的新桶默认阻止以及部分既有桶的默认阻止提高前置条件；若攻击者有配置权限，PutBucketEncryption 变更会留下额外痕迹。身份、来源地址、对象键和版本标识仍可归集。", "The actor needs permission to read and copy-overwrite targets, control a customer-provided key, and know whether the bucket blocks SSE-C. The 2026 default block on new and some existing buckets raises prerequisites. If the actor can change configuration, PutBucketEncryption leaves another trace. Identity, source address, object keys, and version IDs remain aggregatable."),
        P("防守方按桶清点 BlockedEncryptionTypes，保留 PutBucketEncryption 管理事件，并为关键桶开启 S3 对象数据事件。对 CopyObject 的客户密钥参数按主体、来源和对象键跨窗口聚合，再核验批准作业、版本和合法读取结果；只看主机 EDR、未采对象事件或合法 SSE-C 应用被盗用都会使恶意判断变弱。", "Defenders inventory BlockedEncryptionTypes by bucket, retain PutBucketEncryption management events, and enable S3 object data events for critical buckets. They aggregate customer-key parameters on CopyObject by principal, source, and object key, then verify approved jobs, versions, and legitimate read results. Host-only EDR, absent object events, or compromise of an approved SSE-C app weakens maliciousness assessment.")),
    "stealth_mechanisms": [mechanism("NM-BT", "primary", B("服务端重加密跨越主机文件传感器边界", "Service-side re-encryption crosses the host file-sensor boundary"),
        P("攻击者以有权身份把现有对象的重加密交给存储服务，并由自己掌握客户密钥；加密与版本变化落在服务数据面，受害主机不会产生同等文件写入。仅监控主机的防守方因观察域缺失而漏看这一影响，但云数据事件中的 CopyObject、SSE-C 参数及对象版本仍可揭示。", "Using an authorized identity, the attacker delegates re-encryption of existing objects to the storage service under a customer key the attacker holds. Encryption and version change occur in the service data plane without comparable victim-host file writes. Host-only defenders miss the impact across that observation boundary, while cloud data events for CopyObject, SSE-C parameters, and object versions can reveal it."), ["REF-000660", "REF-000661", "REF-000663"], "high")],
    "defense": defense(["DET-000176"], ["MIT-000159"]),
    "evidence": {"claim_refs": ["CLM-000783"], "case_refs": ["CASE-000216"], "reference_refs": ["REF-000660", "REF-000661", "REF-000663", "REF-000654", "REF-000513"]},
    "research": {"limitations": PP(
        ("AWS CIRT 确认恶意大规模 SSE-C 覆写并给出对象数据事件线索，但未公开逐受害者的完整读取验证或时间线。该案例可证明观察到的操作模式，不能证明每个对象均永久无法恢复，也不能推广成所有云平台的通用 API 字段。", "AWS CIRT confirms malicious mass SSE-C overwrites and object-data-event leads but does not publish a complete read test or timeline for each victim. The case proves the observed operation pattern, not permanent unrecoverability for every object or universal API fields across cloud platforms."),
        ("AWS 在 2026 年默认阻止多类桶的新 SSE-C 写入，因此必须按桶核实当前允许状态和配置变更；历史攻击报告不能代表现在所有桶都易受此路径影响。组织持有旧版本时可能恢复，但当前版本的读取中断仍须独立确认。", "AWS's 2026 default blocks new SSE-C writes for multiple bucket classes, so permission state and configuration changes must be checked per bucket. A historical incident report does not establish susceptibility of every bucket today. Older versions may aid recovery, while current-version read interruption requires independent verification."))},
    "lifecycle": life()})

def strategy(n, name, summary, description, targets, analytic, refs):
    write(f"detections/DET-{n:06d}-ta0040-impact-batch-one.yaml", {
        "schema_version": "2.0.0", "type": "detection-strategy", "id": f"DET-{n:06d}",
        "name": name, "summary": summary, "description": description,
        "detects_refs": targets, "domains": ["enterprise"], "analytic_refs": [analytic],
        "evidence_refs": refs, "lifecycle": life()})


def analytic(n, strategy_id, name, summary, platforms, logic, requirements, observables,
             window, dimensions, false_positives, blind_spots, tuning, refs):
    write(f"analytics/NJA-{n:06d}-ta0040-impact-batch-one.yaml", {
        "schema_version": "2.0.0", "type": "detection-analytic", "id": f"NJA-{n:06d}",
        "strategy_ref": strategy_id, "name": name, "summary": summary,
        "domains": ["enterprise"], "platforms": platforms, "logic": logic,
        "data_requirements": requirements, "observables": observables,
        "correlation": {"window": window, "dimensions": dimensions},
        "false_positives": false_positives, "blind_spots": blind_spots,
        "tuning_guidance": tuning, "evidence_refs": refs, "lifecycle": life()})


def requirement(kind, name, channel, fields):
    return {"source_type": kind, "name": name, "channel": channel, "required_fields": fields}


strategy(173, B("关键文件删除与业务损失关联", "Critical-File Deletion and Business-Loss Correlation"),
    B("把文件删除权限和完成事件连接到关键路径、写入者及业务读取失败，识别数据销毁结果。", "Join file-delete access and completion to critical paths, actors, and business-read failures to identify destructive outcomes."),
    PP(("此策略针对 T1485 父级的端点文件损失，不把每个删除请求视为匿迹。分析先从启用 SACL 的业务目录恢复 4663 与 4660 的对象和句柄链，再按进程、账户、路径及资产基线判断是否出现异常集中损失；应用读取失败提升影响置信度。云生命周期子项由另一套控制面到服务结果策略负责。", "This strategy addresses T1485 parent-level endpoint file loss without treating every deletion request as stealth. The analytic reconstructs object and handle lineage from 4663 and 4660 on SACL-audited business directories, then evaluates unusual concentrated loss by process, account, path, and asset baseline; application-read failure raises impact confidence. The cloud lifecycle child uses a separate control-plane-to-service-outcome strategy.")),
    ["NJT-0156"], "NJA-000189", ["REF-000647", "REF-000379", "REF-000656"])
analytic(189, "DET-000173", B("Windows 删除句柄与业务对象损失分析", "Windows Delete-Handle and Business-Object Loss Analytic"),
    B("将 4663 的对象名和删除权限与 4660 的删除完成事件按句柄关联，并相对业务基线聚合损失。", "Correlate object names and delete rights in 4663 with completion in 4660 by handle, then aggregate loss against a business baseline."),
    ["Windows"],
    PP(("对受保护业务目录配置对象访问 SACL，采集 Security 4663 的 ObjectName、AccessMask、ProcessId、HandleId、SubjectUserSid 与时间；在同主机同句柄和进程的短间隔内关联 4660，确认对象被删除。4663 的 DELETE 权限也可能对应重命名，未关联完成或对象状态时只标记删除企图。", "Configure object-access SACLs for protected business directories and ingest Security 4663 ObjectName, AccessMask, ProcessId, HandleId, SubjectUserSid, and time. Join 4660 on the same host, handle, and process within a short interval to confirm deletion. DELETE access in 4663 may also accompany rename; without completion or object state, mark an attempt only."),
       ("按资产、账户、进程与关键根目录在可调的 10 至 30 分钟窗口计数不同对象，比较批准清理任务、变更单和正常维护覆盖率。多个业务目录快速损失或与应用读失败相交时升级；保留原事件 ID、路径和主体供还原。此逻辑不从删除数量推断攻击者的匿迹意图。", "Count distinct objects by asset, account, process, and critical root over a tunable 10 to 30 minute window and compare approved cleanup jobs, change tickets, and normal maintenance coverage. Escalate loss across business directories or intersecting application-read failures; preserve source event IDs, paths, and principals. The logic does not infer stealth intent from deletion count.")),
    [requirement("windows-security-object-access", B("Windows 安全对象访问事件", "Windows Security object-access events"), "Security 4663 and 4660", ["event.timestamp", "host.id", "event.id", "object.name", "access.mask", "process.id", "handle.id", "subject.user.sid"]),
     requirement("protected-file-inventory", B("受保护业务文件清单", "Protected business-file inventory"), None, ["asset.id", "object.path", "business.owner", "criticality", "approved.change.id"])],
    [B("同一进程在多个关键目录上出现已确认删除", "Confirmed deletions by one process across multiple critical directories"), B("相对批准维护基线的不同业务文件损失突增", "A rise in distinct business-file losses relative to approved maintenance")],
    B("对 4663 与 4660 先用秒级句柄关联；对业务损失使用按资产调优的 10 至 30 分钟窗口。", "First join 4663 and 4660 by handle over seconds; aggregate business loss in an asset-tuned 10 to 30 minute window."),
    ["host.id", "handle.id", "process.id", "subject.user.sid", "object.path", "event.timestamp"],
    [B("获批批量清理、迁移或部署回滚会删除多个文件", "Approved cleanup, migration, or deployment rollback can delete many files")],
    [B("未配置 SACL、4660 未采集、重命名歧义或存储控制器外部删除会破坏确认链", "Missing SACLs or 4660, rename ambiguity, or deletion outside host audit breaks confirmation")],
    P("按文件服务器、目录与维护任务建立删除覆盖基线；只对多个关键目录、异常主体或后续读取失败的组合升高严重度。对 4663 未确认事件保留低置信分类，不能为消除误报而全局放行有权服务账户。", "Baseline deletion coverage by server, directory, and maintenance job; raise severity on combinations of multiple critical roots, unusual principal, or subsequent read failure. Keep unconfirmed 4663 events at lower confidence rather than globally allowing privileged service accounts to avoid false positives."),
    ["REF-000379", "REF-000656", "REF-000647"])

strategy(174, B("生命周期规则到服务删除谱系", "Lifecycle Rule to Service Deletion Lineage"),
    B("在对象损失前发现未授权的破坏性规则扩张，并把后续服务过期事件回连规则写入者。", "Detect unauthorized destructive rule expansion before loss and link later service-expiry events to the rule writer."),
    PP(("此策略直接覆盖委托执行式数据销毁：先在配置写入时比较生命周期规则的删除范围和保留期，发出事前告警；随后利用服务到期事件、对象版本和业务读取结果验证影响。分析必须分别保存控制面身份和数据面服务身份，不能以服务事件缺少攻击者用户名为无异常，也不能在只有规则变更时宣称实际删除。", "This strategy directly covers delegated-execution destruction. It compares lifecycle-rule scope and retention at configuration write for pre-impact alerting, then verifies impact with service-expiry events, object versions, and business-read outcomes. The analytic preserves control-plane actor and data-plane service identity separately; a service event without the attacker username is not benign, and a rule change alone does not prove deletion.")),
    ["NJT-0156", "NJS-0156-001"], "NJA-000190", ["REF-000648", "REF-000649", "REF-000650", "REF-000651", "REF-000655", "REF-000513"])
analytic(190, "DET-000174", B("S3 生命周期规则变更与对象过期关联", "S3 Lifecycle Rule Change and Object Expiry Correlation"),
    B("比较规则前后配置并连接服务到期事件、版本状态和关键对象受损结果。", "Compare before-and-after rules and join service expiry, version state, and critical-object loss."),
    ["IaaS"],
    PP(("在 CloudTrail 管理事件出现 PutBucketLifecycle 或 PutBucketLifecycleConfiguration 时，独立抓取并规范化规则前后快照，包括启用状态、过滤前缀和标签、当前与非当前版本到期条件。计算是否新增到期、缩短保留期或扩大关键对象覆盖，并与变更审批和桶所有者基线比较；未授权扩张立即作为事前风险告警。", "When CloudTrail management records PutBucketLifecycle or PutBucketLifecycleConfiguration, independently capture normalized before-and-after rule snapshots including status, prefix and tag filters, and current and noncurrent version expiry. Compute new expiry, shorter retention, or broader critical-object coverage and compare change approval and bucket-owner baseline; alert on unauthorized expansion before impact."),
       ("在 72 小时或规则到期上限中较长的观察范围内，按桶和可判定的过滤条件连接 EventBridge Object Deleted 中的 Lifecycle Expiration、通知或 CloudTrail 生命周期数据事件，再核对版本与合法读取结果。通知配置 ID 不一定等于规则 ID，需在本环境验证对应关系；删除标记与永久版本移除分开输出。", "Over 72 hours or the longer rule-expiry horizon, join by bucket and verifiable filters to EventBridge Object Deleted with Lifecycle Expiration, notifications, or CloudTrail lifecycle data events, then check versions and legitimate reads. Notification configuration IDs need not equal rule IDs and require local mapping validation. Emit delete-marker and permanent-version-removal outcomes separately.")),
    [requirement("s3-management-event", B("S3 生命周期管理事件", "S3 lifecycle management events"), "CloudTrail management events", ["event.time", "event.name", "user.identity.arn", "source.ip", "bucket.name", "event.status"]),
     requirement("s3-lifecycle-version", B("生命周期规则版本快照", "Lifecycle rule version snapshots"), None, ["bucket.name", "rule.id", "rule.status", "filter.prefix", "expiration.days", "revision.time", "approval.id"]),
     requirement("s3-lifecycle-outcome", B("S3 生命周期结果事件", "S3 lifecycle outcome events"), "EventBridge Object Deleted or S3 Lifecycle notification", ["event.time", "bucket.name", "object.key", "deletion.reason", "deletion.type"])],
    [B("未获批准的启用到期规则扩大关键前缀覆盖", "An unapproved enabled expiry rule broadens critical prefix coverage"), B("服务到期结果出现在被更改规则覆盖的对象上", "Service-expiry outcomes affect objects covered by the changed rule")],
    B("配置变更立即检查；结果关联至少 72 小时，并按规则到期条件延长。", "Check configuration writes immediately; retain outcome correlation for at least 72 hours and extend it to the rule's expiry horizon."),
    ["bucket.name", "rule.id", "filter.prefix", "object.key", "revision.time", "event.time"],
    [B("获批保留策略调整、旧版本清理和测试桶迁移会产生相似规则与过期事件", "Approved retention changes, old-version cleanup, and test-bucket migration produce similar rules and expiry events")],
    [B("缺少历史规则快照、结果通知未启用、服务延迟或版本清单缺失会削弱因果与损失判断", "Missing historical rule snapshots, disabled outcome notifications, service delay, or absent version inventory weaken causality and loss assessment")],
    P("为关键桶维护批准规则摘要、最低保留期及前缀所有者清单。允许经审批的保留变更，但不得全局忽略服务主体的过期事件；根据版本状态区分事前规则风险、当前视图丢失和永久数据损失。", "Maintain approved rule digests, retention floors, and prefix owners for critical buckets. Allow approved retention changes without globally ignoring service-principal expiry; separate pre-impact rule risk, current-view loss, and permanent data loss by version state."),
    ["REF-000648", "REF-000649", "REF-000650", "REF-000651", "REF-000655", "REF-000513"])

strategy(175, B("低写入量加密的进程与区域内容关联", "Process and Regional-Content Correlation for Low-Write Encryption"),
    B("跨业务文件聚合同一进程的写入，并用前后区域比较发现低 I/O 的加密影响。", "Aggregate one process's writes across business files and use regional before-and-after comparison to reveal low-I/O encryption impact."),
    PP(("此策略覆盖 T1486 的端点路径及文件内稀疏加密。分析以文件和进程事件筛选同一写入者造成的异常业务文件广度，再由独立内容完整性传感器确认被改写区域与保留区域并存、原业务格式不可读。文件事件并不提供区域熵，因此两个数据层的判断和置信度必须分开；云对象服务端重加密由对象数据事件策略负责。", "This strategy covers the endpoint path of T1486 and Sparse In-File Encryption. The analytic uses file and process events to identify unusual business-file breadth by one writer, then an independent content-integrity sensor confirms altered regions alongside preserved regions and failed business parsing. File events do not supply regional entropy, so judgments and confidence from the two data layers remain separate. Object data events handle service-side cloud re-encryption.")),
    ["NJT-0157", "NJS-0157-001"], "NJA-000191", ["REF-000658", "REF-000659", "REF-000475", "REF-000662"])
analytic(191, "DET-000175", B("业务文件进程写入与稀疏密文差分分析", "Business-File Process Writes and Sparse Ciphertext Differential Analytic"),
    B("输出异常写入者跨文件改写及经内容传感器确认的稀疏密文区域。", "Emit unusual cross-file rewriting by one process and sparse ciphertext regions confirmed by a content sensor."),
    ["Windows"],
    PP(("采集 DeviceFileEvents 的文件创建、修改和重命名，按 DeviceId、InitiatingProcessUniqueId 及可调 15 分钟窗口聚合不同业务路径。与批准备份、同步、构建和加密迁移任务比较；多个目录受同一异常写入者修改时产生候选，不要求勒索字条、新扩展名或整文件高熵。", "Ingest DeviceFileEvents file creation, modification, and rename, grouping distinct business paths by DeviceId, InitiatingProcessUniqueId, and a tunable 15-minute window. Compare approved backup, sync, build, and encryption-migration jobs. An unusual writer changing files across directories creates a candidate without requiring a ransom note, new extension, or high whole-file entropy."),
       ("对候选文件由独立内容或完整性传感器安全比较前后版本的改写偏移、局部熵和格式解析结果。多个文件显示相似稀疏区段、保留大量原文且业务打开失败时升级子项置信度；DeviceFileEvents 的标准字段没有这些内容差分，因此无该传感器时只输出可疑批量改写，不声称确认局部加密。", "For candidate files, a separate content or integrity sensor safely compares changed offsets, regional entropy, and parse results between versions. Similar sparse regions across files, much preserved original content, and failed business reads raise child confidence. Standard DeviceFileEvents fields lack these content differences; without that sensor emit suspicious bulk rewriting, not confirmed regional encryption.")),
    [requirement("defender-device-file-events", B("Defender 设备文件事件", "Defender device file events"), "DeviceFileEvents", ["timestamp", "device.id", "action.type", "folder.path", "file.name", "initiating.process.unique.id", "initiating.process.account"]),
     requirement("regional-content-integrity", B("文件区域内容与完整性比较", "File regional content and integrity comparison"), None, ["device.id", "file.id", "version.before", "version.after", "changed.offsets", "regional.entropy", "parse.result"])],
    [B("同一异常写入进程在多个业务目录中修改文件", "One unusual writer modifies files in multiple business directories"), B("文件内被改写高熵区段与保留原文区段并存且应用解析失败", "Changed high-entropy regions coexist with preserved plaintext and application parsing fails")],
    B("按设备与进程在可调的 15 分钟窗口聚合；区域比较只对候选文件及受控诱饵执行。", "Aggregate by device and process over a tunable 15-minute window; perform regional comparison only on candidate files and controlled canaries."),
    ["device.id", "initiating.process.unique.id", "file.id", "folder.path", "timestamp"],
    [B("批准的备份还原、同步、数据库整理、构建或合法重密钥会改变许多文件", "Approved backup restore, sync, database compaction, build, or rekeying changes many files")],
    [B("没有前版本或内容传感器、文件共享未受管及原文件已加密时，无法判定区域布局", "Absent prior versions or content sensors, unmanaged shares, and already encrypted source files prevent regional classification")],
    P("按主机角色和业务目录维护获批批量写入程序、签名、账户及维护窗口；严重度要求异常写入广度与内容或业务读失败证据结合。若只有文件事件，保留较低置信输出而不以提高整文件熵阈值来掩盖稀疏路径。", "Baseline approved bulk writers, signatures, accounts, and maintenance windows by host role and business directory. Severity requires unusual write breadth plus content or business-read evidence. With file events alone, keep a lower-confidence result rather than raising a whole-file entropy threshold that hides the sparse path."),
    ["REF-000659", "REF-000475", "REF-000662", "REF-000658"])

strategy(176, B("S3 客户密钥对象重加密异常关联", "S3 Customer-Key Object Re-encryption Anomaly Correlation"),
    B("发现同一主体以客户密钥异常覆写已有对象，并连接桶配置、版本和合法读取结果。", "Detect abnormal same-principal customer-key overwrites of existing objects and join bucket configuration, versions, and legitimate reads."),
    PP(("此策略直接覆盖客户密钥服务端重加密。分析先核对每桶 SSE-C 阻止状态与可能的解除阻止事件，再在 S3 对象数据事件中寻找带客户密钥参数的 CopyObject 覆写；按主体和对象范围识别异常批量操作，并核查当前版本和组织密钥归属。它不从单一 SSE-C 请求推断恶意，也不会用主机文件日志替代云数据面。", "This strategy directly covers Customer-Key Service-Side Re-encryption. The analytic first checks each bucket's SSE-C block state and any event removing it, then finds CopyObject overwrites carrying customer-key parameters in S3 object data events. It identifies abnormal batches by principal and object scope and checks current versions and organizational key custody. One SSE-C request does not prove malice, and host file logs do not replace the cloud data plane.")),
    ["NJT-0157", "NJS-0157-002"], "NJA-000192", ["REF-000658", "REF-000660", "REF-000661", "REF-000663", "REF-000654", "REF-000513"])
analytic(192, "DET-000176", B("S3 SSE-C CopyObject 覆写与桶许可分析", "S3 SSE-C CopyObject Overwrite and Bucket-Permission Analytic"),
    B("输出未经批准的客户密钥重加密作业及其对象版本、主体和配置前驱。", "Emit unapproved customer-key re-encryption jobs with object versions, principal, and configuration precursor."),
    ["IaaS"],
    PP(("为关键桶开启 CloudTrail S3 对象数据事件，筛选 s3.amazonaws.com 的 CopyObject，并把请求中的客户密钥算法头规范为 request.sse.customer.algorithm；PutObject 和分段上传作为相关写入另行审查。按用户 ARN 或 access key、源地址、桶及可调 10 至 30 分钟窗口计数被覆写的已有对象键，比较批准 SSE-C 作业和历史身份范围；首次使用或异常批量作为候选。不得收集客户密钥内容。", "Enable CloudTrail S3 object data events for critical buckets. Filter s3.amazonaws.com CopyObject and normalize its customer-key algorithm header as request.sse.customer.algorithm; inspect PutObject and multipart upload as related writes separately. Count previously existing keys overwritten by user ARN or access key, source address, bucket, and a tunable 10 to 30 minute window. Compare approved SSE-C jobs and historical identity scope; first use or an anomalous batch creates a candidate. Do not collect customer key material."),
       ("把桶的 BlockedEncryptionTypes 清单与 PutBucketEncryption 管理事件接入，识别先解除 SSE-C 阻止再发生覆写的链；解除配置本身不是加密结果。对候选对象核查新版本标识、组织是否持有所需密钥、合法读取失败及旧版本是否可恢复。若数据事件缺失或获批身份被盗，只凭加密参数无法断定恶意。", "Join bucket BlockedEncryptionTypes inventory and PutBucketEncryption management events to identify a block-removal precursor followed by overwrites; configuration removal alone is not encryption. Check new version IDs, whether the organization holds the needed key, legitimate read failures, and recovery of prior versions. Missing data events or compromise of an approved principal means an encryption parameter alone cannot prove malice.")),
    [requirement("s3-object-data-event", B("S3 对象数据事件", "S3 object data events"), "CloudTrail S3 data events", ["event.time", "event.source", "event.name", "user.identity.arn", "source.ip", "bucket.name", "object.key", "request.sse.customer.algorithm"]),
     requirement("s3-encryption-configuration", B("桶加密配置与变更", "Bucket encryption configuration and changes"), "S3 configuration inventory and CloudTrail management events", ["bucket.name", "blocked.encryption.types", "configuration.event.name", "configuration.actor", "configuration.time"]),
     requirement("object-version-read-check", B("对象版本与授权读取验证", "Object version and authorized read verification"), None, ["bucket.name", "object.key", "version.id", "read.result", "key.custodian"])],
    [B("同一主体短时将许多已有对象覆写为 SSE-C 当前版本", "One principal rapidly overwrites many existing objects as SSE-C current versions"), B("SSE-C 阻止被移除后出现未经批准的对象重加密", "Unapproved object re-encryption follows removal of an SSE-C block")],
    B("按身份和桶使用可调 10 至 30 分钟覆写窗口，并回看配置变更及旧版本。", "Use a tunable 10 to 30 minute overwrite window by identity and bucket and look back to configuration changes and prior versions."),
    ["user.identity.arn", "source.ip", "bucket.name", "object.key", "event.time", "version.id"],
    [B("批准的 SSE-C 重密钥、迁移、恢复或批量复制可能形成相似对象序列", "Approved SSE-C rekeying, migration, restore, or bulk copy can create similar object sequences")],
    [B("对象数据事件未启用、延迟送达、合法 SSE-C 应用被盗或客户端预先加密上传会避开或混淆该逻辑", "Disabled or delayed object data events, compromise of an approved SSE-C app, or client-side encrypted uploads bypass or confuse this logic")],
    P("以桶和应用维护批准的 SSE-C 例外、身份、源网络、任务标识和对象范围，按受保护资产的重要性调阈值。保留首次使用及跨范围异常，不按合法身份全局放行；对缺少密钥归属或安全读取验证的结果标记为可疑重加密而非已证实勒索。", "Maintain approved SSE-C exceptions, principals, source networks, job IDs, and object scope by bucket and application; tune thresholds to protected asset importance. Keep first-use and cross-scope anomalies rather than globally allowing a valid identity. Where key custody or safe read verification is absent, label suspicious re-encryption rather than confirmed ransom impact."),
    ["REF-000660", "REF-000661", "REF-000663", "REF-000654", "REF-000513"])

def measure(key, name, description, control_type):
    return {"key": key, "name": name, "description": description, "control_type": control_type}


def application(target, use, effect, limits):
    return {"target_ref": target, "use": use, "expected_effect": effect, "limitations": limits}

write("mitigations/MIT-000158-data-retention-authority-and-recovery.yaml", {
    "schema_version": "2.0.0", "type": "mitigation", "id": "MIT-000158",
    "name": B("数据保留权限与独立恢复保护", "Data-Retention Authority and Independent Recovery Protection"),
    "summary": B("限制单一身份改变删除规则或批量毁坏数据，并以受保护版本和独立副本保留恢复路径。", "Limit one identity's ability to change deletion rules or destroy data in bulk while preserving recovery through protected versions and independent copies."),
    "description": PP(("此控制同时缩小破坏权限和损失后果。关键文件与对象的可恢复版本应与生产写入身份隔离并定期演练；对生命周期规则则单独治理配置权限和规则差分，因为禁止用户对象删除并不会阻止服务按已启用的生命周期规则执行。", "This control reduces destructive authority and the consequences of loss. Recoverable versions of critical files and objects should be isolated from production writers and periodically tested. Lifecycle rules require separate governance of configuration authority and rule diffs, because denying user object deletion does not stop a service executing an enabled lifecycle rule.")),
    "domains": ["enterprise"],
    "measures": [
        measure("protected-independent-copies", B("受保护独立副本与恢复演练", "Protected Independent Copies and Restore Exercises"), P("为关键文件和对象保留受版本控制、不可变保留或独立管理域保护的副本，定期验证能从已删除、覆写或隐藏的当前视图恢复业务。", "Keep versioned, immutable, or separately administered copies of critical files and objects, and regularly verify business restoration after deletion, overwrite, or disappearance from the current view."), "containment"),
        measure("lifecycle-rule-authority", B("生命周期规则权限与审批", "Lifecycle Rule Authority and Approval"), P("只向少数管理身份授予生命周期配置写权限，对关键桶的前缀、标签和保留期变更施加审批、配置快照与实时告警；普通工作负载身份不得任意缩短保留。", "Grant lifecycle-configuration write authority only to a small set of management identities. Apply approval, configuration snapshots, and real-time alerting to critical-bucket filter and retention changes; ordinary workload identities must not shorten retention arbitrarily."), "preventive")],
    "applications": [
        application("NJT-0156", P("对受影响业务文件和对象保留独立恢复副本、记录批准清理者和破坏权限，并演练从大规模删除或覆写中恢复真实业务读取。", "For affected business files and objects, retain independent recovery copies, record authorized cleanup actors and destructive rights, and exercise restoration of real business reads after mass deletion or overwrite."), P("降低永久损失并使已受损对象可被清点和恢复，同时限制一个被盗生产身份可破坏的范围。", "Reduce permanent loss, make damaged objects enumerable and recoverable, and limit the scope one stolen production identity can destroy."), P("备份不自动维持当前业务可用性；未覆盖的本地路径仍可被擦除，若备份处于同一权限域也可能被一并删除。", "Backups do not automatically preserve current availability. Uncovered local paths may still be wiped, and backups in the same authority domain may be deleted together.")),
        application("NJS-0156-001", P("在关键 S3 桶保护旧对象版本，对 PutBucketLifecycleConfiguration 对应权限实行最小授权和变更审批，并保存规则前后快照以支持撤销与追溯。", "Protect prior versions in critical S3 buckets, apply least privilege and change approval to lifecycle-configuration writes, and preserve before-and-after rule snapshots for rollback and attribution."), P("攻击者难以悄然扩大服务删除范围；受保护版本在保留期内不随恶意生命周期规则被永久移除，控制面变更更易早期发现。", "It becomes harder to broaden service deletion silently. Protected versions resist permanent removal by a malicious lifecycle rule during retention, and control-plane changes are easier to detect early."), P("删除标记仍可能隐藏当前视图；治理模式绕过权限、保留期不足和未覆盖前缀会降低保护，合法生命周期清理也需要运维审批。", "Delete markers can still hide the current view. Governance-mode bypass rights, insufficient retention, and uncovered prefixes weaken protection; legitimate lifecycle cleanup also needs operational approval."))],
    "evidence_refs": ["REF-000647", "REF-000648", "REF-000652", "REF-000653", "REF-000654", "REF-000655", "REF-000657"],
    "lifecycle": life()})

write("mitigations/MIT-000159-sse-c-permission-and-version-protection.yaml", {
    "schema_version": "2.0.0", "type": "mitigation", "id": "MIT-000159",
    "name": B("客户密钥写入许可与对象版本保护", "Customer-Key Write Permission and Object-Version Protection"),
    "summary": B("保持无需使用 SSE-C 的桶处于阻止状态，收窄例外和配置权限，并保护旧版本以降低恶意重加密影响。", "Keep buckets without an SSE-C need blocked, narrow exceptions and configuration rights, and protect prior versions to reduce malicious re-encryption impact."),
    "description": PP(("此控制针对攻击者借有效凭据把现有对象覆写成只受其客户密钥保护的当前版本。先维持 S3 已提供的 SSE-C 默认阻止状态，对确需 SSE-C 的应用单独管理许可和身份；再用受保护旧版本与恢复测试降低当前版本被改写后的损失。阻止 SSE-C 不是通用加密禁令，也不能替代对象写权限治理。", "This control addresses an actor using valid credentials to overwrite existing objects with a current version protected only by the actor's customer key. Preserve S3's existing default SSE-C block, govern permission and identity separately for applications that truly need SSE-C, and use protected prior versions and restore tests to reduce damage after current-version overwrite. Blocking SSE-C is not a general encryption ban and does not replace object-write governance.")),
    "domains": ["enterprise"],
    "measures": [
        measure("preserve-sse-c-block", B("保持客户密钥写入阻止", "Preserve Customer-Key Write Block"), P("清点各桶 BlockedEncryptionTypes；对无业务需要的桶维持 SSE-C 阻止，并限制可以通过 PutBucketEncryption 移除该阻止的身份。对既有例外配置附加审批与定期复核。", "Inventory BlockedEncryptionTypes by bucket. Keep SSE-C blocked where there is no business need and restrict identities that can remove the block through PutBucketEncryption. Approve and periodically review existing exceptions."), "preventive"),
        measure("scope-sse-c-exceptions", B("收窄客户密钥应用例外", "Narrow Customer-Key Application Exceptions"), P("确需 SSE-C 的应用应使用短期身份、最小对象复制与写入范围，以及针对客户密钥算法条件的桶或组织拒绝策略例外。", "Applications that truly require SSE-C should use short-lived identities, minimal copy and write scope, and narrowly governed exceptions to bucket or organization deny policies conditioned on customer-key algorithms."), "preventive"),
        measure("protected-prior-object-versions", B("保护先前对象版本", "Protect Prior Object Versions"), P("对重要对象启用版本控制和适当的对象锁或独立备份，并演练从攻击者密钥覆写后的旧版本恢复业务读取。", "Use versioning with appropriate Object Lock or independent backup for critical objects and exercise restoration of business reads from prior versions after attacker-key overwrite."), "containment")],
    "applications": [
        application("NJT-0157", P("对关键对象存储实行客户密钥使用清单和最小对象写入权限，并与端点业务数据的独立恢复策略配合；只有确需该加密模式的应用才获得例外。", "For critical object stores, maintain a customer-key use inventory and least object-write rights alongside independent recovery for endpoint business data; grant exceptions only to applications that need this encryption mode."), P("限制对象当前版本被攻击者密钥覆写的机会，并在已覆写时提供旧版本恢复路径。", "Reduce opportunities for attacker-key overwrites of current object versions and preserve a prior-version recovery path if overwrite occurs."), P("此控制不阻止攻击者先在客户端加密再上传内容，也不覆盖文件服务器上的局部加密；旧版本可恢复不代表当前读请求没有中断。", "This control does not stop an attacker encrypting content client-side before upload or cover sparse encryption on file servers. Recoverable prior versions do not mean current reads were uninterrupted.")),
        application("NJS-0157-002", P("在目标桶确认 SSE-C 默认阻止状态并限制移除阻止的配置权限；对获批 SSE-C 应用限定身份、源和键前缀，再用对象锁保护先前版本。", "Verify the target bucket's default SSE-C block and restrict authority to remove it. Scope approved SSE-C apps by identity, source, and key prefix, then protect prior object versions with Object Lock."), P("带攻击者客户密钥的 CopyObject 覆写在阻止或拒绝策略处失败；受保护旧版本仍可用于恢复，同时配置例外留下审计前驱。", "CopyObject overwrites under an attacker-provided customer key fail at the block or deny policy; protected prior versions remain recoverable, and configuration exceptions leave an audit precursor."), P("2026 年后的新桶常已默认阻止，不能把此控制当作额外新增覆盖；获批例外被盗用、配置权被攻破或客户先加密内容后上传仍可造成损失。", "Many new buckets already block SSE-C by default after 2026, so this measure is not extra coverage there. Compromised approved exceptions, stolen configuration authority, or client-side encrypted uploads can still cause loss."))],
    "evidence_refs": ["REF-000660", "REF-000663", "REF-000654"], "lifecycle": life()})

# Extend an existing canonical control only where its measures really apply.
mit115_path = next((ROOT / "mitigations").glob("MIT-000115-*.yaml"))
mit115 = yaml.safe_load(mit115_path.read_text(encoding="utf-8"))
mit115_new = [
    application("NJT-0157", P("对可写业务目录限制未知加密载荷和过宽写权限，在支持的平台启用受控文件夹访问，并把不可变恢复副本与生产账户分离。多文件可读性丧失时隔离写入进程，即使单文件改写量不大。", "Restrict unknown encryptors and excessive write authority over writable business directories, enable controlled folder access where supported, and separate immutable recovery copies from production accounts. Isolate the writer on multi-file readability loss even when per-file writes are modest."), P("提高未批准加密写入的执行成本并保留恢复路径，使攻击者无法单靠降低单文件 I/O 绕过写入授权。", "Raise the cost of unauthorized encryption writes and preserve restoration, so lowering per-file I/O does not bypass writer authorization alone."), P("受信任应用或被盗有权身份仍可能写入，受控文件夹仅保护配置范围，恢复副本也不能消除当前数据短时不可用。", "Trusted applications or stolen authorized identities may still write. Controlled folder access protects only configured scope, and recovery copies do not remove temporary current-data unavailability.")),
    application("NJS-0157-001", P("对稀疏文件加密，保护业务目录不受未知写入者修改，并保留可安全比较的前版本或诱饵；响应条件以跨文件同进程异常和解析失败为准，不要求整文件高熵。", "For sparse file encryption, protect business directories against unknown writers and retain safely comparable prior versions or canaries. Trigger response on cross-file same-process anomaly and parse failure rather than requiring high whole-file entropy."), P("在稀疏区段积累为大范围不可读前限制写入，并保留恢复及区域差分证据。", "Constrain writes before sparse regions accumulate into widespread unreadability and preserve recovery and regional-difference evidence."), P("被批准的写入者遭劫持仍可越过应用控制，缺少受保护前版本时只能发现可疑改写，不能自动恢复文件。", "A hijacked approved writer can still pass application control. Without a protected prior version, suspicious rewriting may be found but the file cannot automatically be restored."))]
existing = {a["target_ref"] for a in mit115["applications"]}
mit115["applications"].extend(a for a in mit115_new if a["target_ref"] not in existing)
mit115["evidence_refs"] = list(dict.fromkeys(mit115["evidence_refs"] + ["REF-000659", "REF-000662"]))
mit115["lifecycle"]["modified"] = TODAY
mit115["lifecycle"]["version"] = "0.3.0"
mit115_path.write_text(yaml.safe_dump(mit115, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
