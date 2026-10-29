#!/usr/bin/env python3
"""Serialize individually reviewed BATCH-TA0008-002 source decisions."""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
selected = yaml.safe_load((RUN / "source-resolutions.yaml").read_text())["selected_new_sources"]
handoffs = {
    name: yaml.safe_load((RUN / f"{name}-handoff.yaml").read_text())
    for name in ["T1080", "T1091", "T1210", "T1534", "T1563"]
}
source = {
    x["key"]: x
    for handoff in handoffs.values()
    for x in handoff["library_candidates"]["references"]
    if isinstance(x, dict) and x.get("key")
}
# Each tuple is a reviewed title, publisher, source type, publication date and
# conclusion limit. This data is authored per source; this script only serializes.
META = {
"T1080-ATTACK": ("共享内容污染，技术 T1080", "Taint Shared Content, Technique T1080", "MITRE ATT&CK", "official-documentation", None, "仅锚定 Enterprise 19.1 父行为与战术，不能单独证明 Niji 子项、恶意意图或防御字段。"),
"T1080-ESET-GAMAREDON": ("Gamaredon 组织的后入侵工具与横向扩散", "Gamaredon Group Grows Its Game", "ESET Research", "incident-report", "2020-06-11", "直接证明原有文档的宏/模板注入及内部邮箱发信；报告称该组织重快速扩散，不能用作匿迹动机证据。"),
"T1080-ESET-INVISIMOLE": ("InvisiMole 幕后行动白皮书", "InvisiMole: The Hidden Part of the Story", "ESET Research", "incident-report", "2020-06-18", "同一白皮书的第 5.2 节支持原有文件木马化，第 5.1 节支持远程服务利用；网页摘要不作为第二条独立来源。"),
"T1080-DIRSHARE": ("共享目录替身的现场取证与 DirSharePivot 复现", "Abusing Network Shares for Efficient Lateral Movements and Privesc", "David Routin", "incident-report", "2017-11-13", "作者报告客户共享盘现场并展示可重现实验；可支持导航替身与正常目录继续显示，不推定未公开的受害者遥测。"),
"T1080-MS-AUDIT": ("Microsoft Purview 审计活动索引", "Microsoft Purview Audit Log Activities", "Microsoft", "official-documentation", None, "支持共享对象和协作活动可记录字段；实际启用、保留与旧新版本可得性需按租户核验。"),
"T1080-MS-MACROS": ("阻止来自互联网的 Office 宏", "Macros from the Internet Are Blocked by Default in Office", "Microsoft", "official-documentation", None, "支持宏信任与策略防御的实现限制；内部共享文件不一定具有互联网来源标记。"),
"T1080-MS-APPLOCKER": ("AppLocker 规则使用", "Working with AppLocker Rules", "Microsoft", "official-documentation", None, "支持脚本和可执行内容策略控制；规则批准不证明共享对象当前内容无恶意。"),
"T1091-ESET-USBSTEALER": ("Sednit 对隔离网络的 USBStealer 攻击分析", "Sednit Espionage Group Attacking Air-Gapped Networks", "ESET Research", "sample-analysis", "2014-11-11", "样本逆向给出已控 A 主机播种介质及 B 主机触发执行模型，不等于一宗已公布完整 A/B 遥测的事件。"),
"T1091-MDE-DEVICE-CONTROL": ("Microsoft Defender 设备控制报告", "View Device Control Events and Information in Microsoft Defender for Endpoint", "Microsoft", "official-documentation", None, "支持介质接入和设备身份日志字段；设备 ID 映射与事件上报时延需本地验证。"),
"T1091-MDE-PROCESS-EVENTS": ("Microsoft Defender XDR 设备进程事件表", "DeviceProcessEvents Table in the Advanced Hunting Schema", "Microsoft", "official-documentation", None, "支持目标端进程、父进程与命令行字段；单独的进程事件不能证明同一介质跨主机来源。"),
"T1210-ATTACK19": ("利用远程服务，技术 T1210", "Exploitation of Remote Services, Technique T1210", "MITRE ATT&CK", "official-documentation", None, "仅锚定固定 19.1 父行为与 TA0008 映射；滚动页面在 19.1 之后更新，不能替代冻结基线。"),
"T1210-MS-PETYA-NET": ("NotPetya 网络传播技术分析", "Advanced Threat Analytics Network Technical Analysis of NotPetya", "Microsoft Security", "incident-report", "2017-10-03", "记录内部传播与服务/主机痕迹，不能把每次接入或失败利用都升格为确认的远程漏洞执行。"),
"T1210-MS-PETYA-SAMPLE": ("Petya 勒索软件的蠕虫传播能力", "New Ransomware, Old Techniques: Petya Adds Worm Capabilities", "Microsoft Security", "sample-analysis", "2017-06-27", "支持样本使用 SMB 利用与其他传播路径；具体目标成功与否仍须结果日志确认。"),
"T1210-CISA-RVA": ("医疗与公共卫生部门风险漏洞评估", "Risk and Vulnerability Assessment for the Healthcare and Public Health Sector", "CISA", "official-documentation", "2023-12", "受控评估能证明漏洞可利用和防守观察条件，不应被表述为真实恶意入侵或匿迹意图。"),
"T1210-MS17-010": ("Microsoft 安全公告 MS17-010", "Microsoft Security Bulletin MS17-010", "Microsoft", "official-documentation", "2017-03-14", "支持受影响 SMB 实现与补丁控制；漏洞存在不证明已被利用或产生横向结果。"),
"T1210-MDE-NET": ("Microsoft Defender XDR 设备网络事件表", "DeviceNetworkEvents Table in the Advanced Hunting Schema", "Microsoft", "official-documentation", None, "支持设备网络连接与目标字段；不单独证明漏洞利用成功。"),
"T1210-MDE-VULN": ("Microsoft Defender XDR 设备软件漏洞表", "DeviceTvmSoftwareVulnerabilities Table in the Advanced Hunting Schema", "Microsoft", "official-documentation", None, "支持按设备/软件版本核对已知漏洞暴露；扫描结果可能滞后，不能当作真实 exploit 结果。"),
"T1534-ATTACK": ("内部定向钓鱼，技术 T1534", "Internal Spearphishing, Technique T1534", "MITRE ATT&CK", "official-documentation", None, "仅锚定 19.1 父行为与战术；发送内部消息不自动证明收件者失陷或新 Niji 子项。"),
"T1534-MS-2026": ("滥用 SharePoint 的多阶段 AiTM 与 BEC 活动", "Resurgence of a Multi-Stage AiTM Phishing and BEC Campaign Abusing SharePoint", "Microsoft Security", "incident-report", "2026-01-21", "直接记录受陷身份的内部投递及后续账户失陷；邮件数量不能替代逐收件者触发证据。"),
"T1534-PROOFPOINT-2026": ("云账户接管后邮箱规则与内部钓鱼", "Mailbox Rules in O365: A Post-Exploitation Tactic in Cloud ATO", "Proofpoint", "incident-report", "2026-04-13", "直接记录按主题归档警示回复、45 名内部收件者和第二账户失陷；归档变量已由 NJS-0111-001 覆盖。"),
"T1534-MS-EMAILEVENTS": ("Microsoft Defender XDR 邮件事件表", "EmailEvents Table in the Advanced Hunting Schema", "Microsoft", "official-documentation", None, "支持发件身份、收件者与邮件投递字段；仅有投递不能证明点击或账户结果。"),
"T1534-MS-URLCLICKS": ("Microsoft Defender XDR URL 点击事件表", "UrlClickEvents Table in the Advanced Hunting Schema", "Microsoft", "official-documentation", None, "支持部分邮件链接点击遥测；附件打开和其他客户端动作需额外数据。"),
"T1534-MS-ATTACHMENTINFO": ("Microsoft Defender XDR 邮件附件表", "EmailAttachmentInfo Table in the Advanced Hunting Schema", "Microsoft", "official-documentation", None, "支持附件摘要、文件名与邮件关联，不能单独证明收件者执行。"),
"T1534-MS-RULE-AUDIT": ("通过审计日志识别邮箱规则", "Identify Mailbox Rules with Audit Logs", "Microsoft", "official-documentation", None, "支持规则创建和修改审计；规则存在需与相应主题消息和反馈路由结合判断。"),
"T1563-ATTACK": ("远程服务会话劫持，技术 T1563", "Remote Service Session Hijacking, Technique T1563", "MITRE ATT&CK", "official-documentation", None, "仅锚定 19.1 父行为和两项 ATT&CK 实现宽度，不直接生成 Niji SSH/RDP 子项。"),
"T1563-OPENSSH-CONFIG": ("OpenBSD ssh_config 控制主连接文档", "OpenBSD ssh_config ControlMaster Manual", "OpenBSD", "official-documentation", None, "证明 ControlMaster 与 ControlPath 能复用既有认证连接；不证明野外攻击使用。"),
"T1563-OPENSSH-MUX": ("OpenSSH 多路复用协议", "OpenSSH Multiplexing Protocol", "OpenSSH", "official-documentation", None, "证明 MUX_C_NEW_SESSION 可在同一连接中增设逻辑会话；这是协议能力而非攻击现场证据。"),
"T1563-ISSHD": ("借 SSHD 埋点研究会话劫持与通道可见性", "Local System Security via SSHD Instrumentation", "USENIX LISA", "academic-paper", "2011", "研究演示 SSH-Jack 向运行中客户端注入并增设通道；非野外事件，iSSHD 埋点也不等于通用 sshd 日志。"),
"T1563-TSCON": ("tscon 会话连接命令", "tscon Command", "Microsoft", "official-documentation", None, "证明会话连接命令与参数；真实攻击需结合事件和控制权变化。"),
"T1563-CROWDSTRIKE-OVERWATCH": ("CrowdStrike 2020 OverWatch 威胁狩猎报告", "2020 OverWatch Threat Hunting Report", "CrowdStrike", "incident-report", "2020-09-15", "记录 tscon 尝试受阻及随后 RDS shadow 成功；不可把前一尝试写作成功会话接管。"),
"T1563-SHADOW": ("shadow 远程桌面会话命令", "shadow Command", "Microsoft", "official-documentation", None, "证明影子查看/控制功能与会话目标；是否需要用户同意取决于策略。"),
"T1563-SHADOW-POLICY": ("远程桌面影子控制策略", "Remote Desktop Services Shadow-Control Policy", "Microsoft", "official-documentation", None, "支持会话控制同意设置，不能证明某次攻击者无提示成功。"),
"T1563-4778": ("Windows 事件 4778：会话重新连接", "Windows Event 4778 A Session Was Reconnected", "Microsoft", "official-documentation", None, "提供会话重新连接的客户端和会话字段；事件不自动标记恶意接管。"),
"T1563-4779": ("Windows 事件 4779：会话断开", "Windows Event 4779 A Session Was Disconnected", "Microsoft", "official-documentation", None, "提供会话断开的客户端和会话字段；需与重新连接及控制进程联合解释。"),
"T1563-4688": ("Windows 命令行进程审计", "Windows Command-Line Process Auditing", "Microsoft", "official-documentation", None, "支持创建进程及可选命令行记录前提；需启用相应审核策略。"),
"T1563-MAZE": ("Mandiant MAZE 勒索事件技战术", "Navigating the MAZE Ransomware Incidents", "Mandiant", "incident-report", "2020-07-05", "直接称攻击者以 tscon 劫持合法 RDP 会话；未公开逐会话 ID 与完整旧新客户端链。"),
}
assert len(META)==36,len(META)
valid_types={"official-documentation","academic-paper","incident-report","threat-report","vendor-report","news","dataset","sample-analysis","web-page","other"}
for row in selected:
    key=row["temporary_key"]
    short=key.removeprefix("B8B-").replace("-REF-", "-", 1)
    zh,en,publisher,source_type,published,notes_zh=META[short]
    assert source_type in valid_types
    item=source[key]
    notes_en=item.get("limit") or item.get("limits") or item.get("note") or item.get("strength") or item.get("locator") or "Evidence is limited to the documented behavior and data fields."
    locator=item.get("locator") or row.get("research_locator") or "Documented behavior, telemetry, and limitations"
    authors=item.get("authors") or item.get("author") or []
    if isinstance(authors,str):authors=[authors]
    attack_id=short.split("-")[0] if "ATTACK" in short else None
    obj={
        "schema_version":"1.0.0","type":"reference","id":row["canonical_ref"],
        "title_zh":zh,"title_en":en,"source_type":source_type,
        "identifiers":{"doi":None,"rfc":None,"arxiv":None,"attack_id":attack_id,"other":[]},
        "authors":authors,"publisher":publisher,"published":published,
        "url":row["url"],"accessed":"2026-09-22","locator":str(locator),
        "archive_url":None,"credibility":"high" if source_type in {"official-documentation","incident-report","sample-analysis"} else "medium",
        "notes_zh":notes_zh,"notes_en":str(notes_en)}
    slug=re.sub(r"[^a-z0-9]+","-",short.lower()).strip("-")
    path=ROOT/"references"/f"{row['canonical_ref']}-{slug}.yaml"
    if path.exists():raise RuntimeError(f"already exists: {path}")
    path.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
print(f"serialized {len(selected)} reviewed references")
