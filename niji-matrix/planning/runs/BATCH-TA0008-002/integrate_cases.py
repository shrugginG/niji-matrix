#!/usr/bin/env python3
"""Serialize ten independently reviewed incident or sample-procedure cases."""
from pathlib import Path
import re
import yaml
ROOT=Path(__file__).resolve().parents[3]
# ID, slug, zh/en title, actor, zh/en explanation, period, zh/en sectors,
# source refs and calibrated confidence. Each description is candidate-specific.
CASES=[
("CASE-000203","gamaredon-existing-doc-injection","Gamaredon 改写原有文档中的宏与模板","Gamaredon Injects Macros and Templates into Existing Documents","Gamaredon",
" ESET 分析 Gamaredon 的 CodeBuilder 与 VBScript 模块：它们寻找可访问的 Word/Excel 文档，移动至暂存位置，加入恶意宏或远程模板引用，再放回原路径。报告说明这些文档可在组织内共享并由后来打开者触发；没有逐个公开异机打开和失陷结果，也明确称该组织偏重快速扩散。",
"ESET analyzed Gamaredon CodeBuilder and VBScript modules that find reachable Word or Excel documents, move them temporarily, insert malicious macros or remote-template references, and return them to their paths. The report explains how colleagues can share and later open those documents, but does not publish each cross-host open or compromise outcome and explicitly describes an actor focused on rapid spread.",
"2019-2020",["乌克兰机构"],["Ukrainian organizations"],["REF-000590"],"medium"),
("CASE-000204","invisimole-trojanized-internal-files","InvisiMole 替换组织内部原有软件和文档","InvisiMole Replaces Existing Organizational Software and Documents","InvisiMole",
"ESET 白皮书第 5.2 节记录行动者取得组织内部文档和软件安装包，将原件改为携带 InvisiMole 的自解压包，保留名称、图标和元数据，再放回内部使用路径，依赖其他用户分享与执行。该证据支持原有对象身份延续与恶意内容变化；报告未给每台消费者的完整执行遥测。",
"ESET's white paper section 5.2 records actors obtaining internal documents and software installers, replacing originals with self-extracting packages carrying InvisiMole while preserving names, icons, and metadata, and relying on others to share and execute them. This supports continuity of apparent object identity despite changed content, but the report does not give complete execution telemetry for every consumer.",
"late 2019-2020",["军事与外交目标"],["Military and diplomatic targets"],["REF-000591"],"high"),
("CASE-000205","dirsharepivot-navigation-substitute","共享盘目录替身导致用户点击后本地执行","Directory Substitute on a Share Leads to Local Execution","Unknown ransomware intrusion investigated by David Routin",
"原作者记录一处客户共享盘中真实目录被隐藏，同名并带目录图标的快捷方式替代可见入口。员工点击后仍看到预期目录，同时快捷方式把恶意内容复制到本地并运行；作者还给出受控复现与共享审计建议。此案例支持导航绑定变化与受害者动作，但客户身份、逐台遥测和真实传播规模未公开。",
"The investigator reports a customer share where real directories were hidden and same-named shortcuts with directory icons replaced visible entries. Users who clicked still saw the expected directory while the shortcut copied malicious content locally and ran it; the author also provides a controlled reproduction and share-audit guidance. The account supports changed navigation binding and recipient action, but client identity, per-host telemetry, and full spread were not disclosed.",
"reported 2017",["未披露企业环境"],["Undisclosed enterprise"],["REF-000592"],"medium"),
("CASE-000206","sednit-usbstealer-a-media-b","Sednit USBStealer 的 A—介质—B 传播模型","Sednit USBStealer A-to-Media-to-B Propagation Model","Sednit USBStealer sample",
"ESET 对 Win32/USBStealer 样本逆向重建：已受控主机 A 写入可移动介质上的隐藏组件与诱导入口，介质接到隔离主机 B 后，用户或自动运行触发本地组件。隐藏属性、仿冒安全工具与时间属性可改变可见外观。该结论是样本能力及传播模型，不是某次企业事件已公开完整 A/B 时间线。",
"ESET reverse engineered Win32/USBStealer and reconstructed an already controlled host A writing hidden components and a lure to removable media, followed by local activation when that medium is connected to isolated host B. Hidden attributes, security-tool disguise, and time attributes change visible appearance. The conclusion is a sample capability and propagation model, not a complete published A/B timeline from one enterprise incident.",
"analyzed 2014",["隔离网络目标，具体行业未披露"],["Air-gapped targets; sector undisclosed"],["REF-000596"],"medium"),
("CASE-000207","invisimole-internal-service-exploit","InvisiMole 内网远程服务利用传播","InvisiMole Internal Remote-Service Exploitation","InvisiMole",
"ESET 白皮书第 5.1 节记录 BlueKeep 插件包含目标探测、漏洞利用与下载器执行阶段；在另一 SMB 路径上，研究者在多个目标发现 DoublePulsar，并从 Windows Security Logs 看到 SMB 会话后数秒运行 InvisiMole loader。研究者明确未获得 EternalBlue 利用代码，因此 SMB 路径的具体利用步骤仍是有限重建，不能声称每个目标的完整链已观测。",
"ESET's white paper section 5.1 documents a BlueKeep plugin with target probing, exploitation, and downloader launch. On a separate SMB route, investigators found DoublePulsar on several targets and Windows Security Logs showing an InvisiMole loader starting seconds after an SMB session. They explicitly did not obtain the EternalBlue exploit code, so the precise SMB exploitation step is a limited reconstruction rather than a fully observed chain on every target.",
"late 2019-2020",["军事与外交目标"],["Military and diplomatic targets"],["REF-000591"],"medium"),
("CASE-000208","notpetya-mixed-internal-propagation","NotPetya 混合内部传播路径","NotPetya Mixed Internal Propagation Paths","NotPetya",
"Microsoft 对 NotPetya 的样本和网络分析显示，传播组合了获取的凭据、系统管理工具与在部分条件下尝试的 SMB 漏洞路径。它证明同一活动中的主机间到达和远程运行可有不同因果入口；没有每个目标的 exploit 成功证据时，不应把所有横向结果归为 T1210。",
"Microsoft sample and network analyses show NotPetya combining acquired credentials, system administration tools, and an SMB exploit path attempted under some conditions. This establishes that arrival and remote execution within one campaign can have different causal entries. Without exploit-success evidence for each destination, not every lateral outcome can be attributed to T1210.",
"2017-06",["跨行业"],["Multiple sectors"],["REF-000600","REF-000601"],"high"),
("CASE-000209","microsoft-internal-aitm-propagation","受陷内部身份发信后第二账户失陷","Compromised Internal Sender Followed by Further Account Compromise","Microsoft-observed AiTM and BEC campaign",
"Microsoft 记录能源部门活动中受陷账户被用于向内外联系人发送超过六百封带新诱导链接的邮件，部分组织内收件者点击后又出现新的账户失陷。该案例支持内部发件主体、消息触达、收件者动作和后继账户结果，不证明每一封邮件都造成失陷，也不把邮件数量当作低可见性。",
"Microsoft records compromised accounts in an energy-sector campaign sending more than six hundred messages with a new lure link to internal and external contacts; some recipients inside organizations clicked and further accounts were compromised. The case supports the internal sending principal, delivery, recipient action, and subsequent account outcome, not compromise by every message or low visibility merely because of message volume.",
"reported 2026",["能源部门"],["Energy sector"],["REF-000607"],"high"),
("CASE-000210","proofpoint-accounting-internal-lure","受陷会计邮箱内部诱导与警示回复归档","Compromised Accounting Mailbox Internal Lure and Warning-Reply Archive","Proofpoint-observed cloud account takeover",
"Proofpoint 记录攻击者控制会计邮箱后先建立按活动主题自动归档回复的规则，再以同一主题向四十五名同事发恶意附件；高管助理打开后其账户也被攻陷。规则让原邮箱日常 Inbox 不显示警示回复，但服务端规则和归档消息仍可查。案例支持内部钓鱼结果及共现的视图遗漏，不产生一个与 NJS-0111-001 同义的新子项。",
"Proofpoint records an attacker controlling an accounting mailbox, first creating a rule to archive replies matching the campaign subject, then sending malicious attachments with that subject to forty-five colleagues. An executive assistant opened one and their account was also compromised. The rule removed warning replies from the original user's ordinary Inbox while server-side rule and archived messages remained. This supports internal-phishing outcome and co-occurring default-view omission, not a new child synonymous with NJS-0111-001.",
"reported 2026",["未披露组织"],["Undisclosed organization"],["REF-000608"],"high"),
("CASE-000211","crowdstrike-rds-shadow-success","受阻 tscon 后成功的 RDS shadow 接管","Successful RDS Shadow Control After a Blocked tscon Attempt","Unidentified eCrime intrusion investigated by CrowdStrike",
"CrowdStrike 2020 OverWatch 报告记录攻击者在亚太物流环境枚举 RDP 会话，尝试以 tscon 改接会话但遭 Falcon 阻断；随后更改影子控制策略并用 mstsc 的 shadow/control 选项成功控制活动会话。只能把后一分支算作成功的控制端重绑定，不能把受阻 tscon 写成成功。",
"CrowdStrike's 2020 OverWatch report records an actor in an Asia-Pacific logistics intrusion enumerating RDP sessions and attempting tscon reattachment, which Falcon blocked. The actor then changed shadow-control policy and successfully controlled an active session with mstsc shadow and control options. Only the latter branch is a successful controller rebind; the blocked tscon attempt is not.",
"2020",["运输与物流"],["Transport and logistics"],["REF-000618"],"high"),
("CASE-000212","maze-tscon-rdp-hijack","MAZE 入侵中的合法 RDP 会话劫持","Legitimate RDP Session Hijacking in MAZE Intrusions","MAZE ransomware incidents",
"Mandiant 对多起 MAZE 入侵的调查综述明确记录攻击者使用 tscon 接管合法 RDP 会话，并用于横向移动与权限提升。报告未给逐个会话 ID、4778/4779 前后态或每次命令的资源结果，因此案例只能支持此行为在现场出现，不能当作具体 Analytic 字段链的原始遥测。",
"Mandiant's synthesis of multiple MAZE investigations directly states that actors used tscon to commandeer legitimate RDP sessions for lateral movement and privilege escalation. The report does not provide per-session IDs, before-and-after 4778 or 4779 state, or resource outcomes for each command. It supports field occurrence of the behavior, not the raw telemetry chain of a particular analytic.",
"2019-2020",["未披露多行业"],["Multiple undisclosed sectors"],["REF-000624"],"medium"),
]
assert len(CASES)==10
targets={
"CASE-000203":["NJT-0148","NJS-0148-001"],
"CASE-000204":["NJT-0148","NJS-0148-001"],
"CASE-000205":["NJT-0148","NJS-0148-002"],
"CASE-000206":["NJT-0058","NJS-0058-001","NJS-0058-002"],
"CASE-000207":["NJT-0149"],
"CASE-000208":["NJT-0149"],
"CASE-000209":["NJT-0150"],
"CASE-000210":["NJT-0150","NJS-0111-001"],
"CASE-000211":["NJT-0151","NJS-0151-002"],
"CASE-000212":["NJT-0151","NJS-0151-002"],
}
for cid,slug,zh,en,actor,desc_zh,desc_en,period,sectors_zh,sectors_en,refs,confidence in CASES:
    obj={"schema_version":"1.0.0","type":"case","id":cid,"name_zh":zh,"name_en":en,
         "actor_or_campaign":actor,"subject_refs":targets[cid],
         "description_zh":desc_zh.strip(),"description_en":desc_en.strip(),
         "time_range":period,"target_sectors_zh":sectors_zh,"target_sectors_en":sectors_en,
         "evidence_refs":refs,"confidence":confidence,"status":"draft"}
    path=ROOT/"cases"/f"{cid}-{slug}.yaml"
    if path.exists():raise RuntimeError(path)
    path.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
print("serialized",len(CASES),"reviewed cases")
