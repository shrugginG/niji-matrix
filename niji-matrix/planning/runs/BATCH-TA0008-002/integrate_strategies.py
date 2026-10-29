#!/usr/bin/env python3
"""Serialize the five reviewed Detection Strategies and their analytic links."""
from pathlib import Path
import re
import yaml
ROOT=Path(__file__).resolve().parents[3]
SPECS=[
("DET-000166","shared-object-consumer-lineage",
{"zh":"共享对象改写—异机消费结果关联","en":"Shared-Object Mutation to Cross-Host Consumer Outcome Lineage"},
{"zh":"跨旧新版本、导航绑定与目标端执行结果识别恶意共享内容消费。","en":"Identify malicious shared-content consumption by joining old and new versions or navigation bindings to destination execution outcomes."},
[
{"zh":"本策略把共享对象的写入者、旧新版本或导航入口解析关系，与另一内部主机消费后的首次攻击者动作连接为同一事务。NJA-000178 处理原有对象内容或执行语义改变，要求版本差分、真实消费与结果三段；NJA-000179 处理目录入口被替身绑定，要求共享侧隐藏原件/创建替身与消费者点击后命令链相互验证。","en":"This strategy joins the writer of a shared object, its old and new version or navigation-entry resolution, and the first attacker action after another internal host consumes it. NJA-000178 handles changed content or execution semantics within an established object and requires version difference, real consumption, and outcome. NJA-000179 handles a substituted directory entry and requires share-side changes to the original and substitute plus the consumer's post-click command chain."},
{"zh":"共享文件被写入或读取不自动证明横向成功；预览、同步和正常编辑都需作为替代解释。输出需分别标记污染候选与已确认异机结果，并保留写者、版本、内容摘要、导航目标、消费者设备和进程的联接证据。","en":"A write or read on a share does not automatically prove lateral success; previews, synchronization, and authorized editing remain alternative explanations. Output distinguishes a taint candidate from a confirmed cross-host outcome and preserves joins among writer, version, digest, navigation target, consumer device, and process."}],
["NJT-0148","NJS-0148-001","NJS-0148-002"],["NJA-000178","NJA-000179"],"REF-000589"),
("DET-000167","removable-media-cross-host-lineage",
{"zh":"可移动介质跨主机传播谱系","en":"Removable-Media Cross-Host Propagation Lineage"},
{"zh":"以同一介质与载荷连接已控 A 的播种、不同 B 的接入和 B 上首次恶意动作。","en":"Join seeding on controlled host A, insertion on distinct host B, and B's first malicious action by the same medium and payload."},
[
{"zh":"本策略面向 T1091 的 TA0008 结果门。NJA-000180 以介质身份、A 端写入进程与内容摘要、B 端挂载和真实执行构建 A—介质—B 三门链；同时分别比较伪装入口的可见外观与命令目标，以及自动播种的卷枚举和批量写入。它不把一台主机的 USB 插入或用户点击单独升级为内部横向传播。","en":"This strategy targets T1091's TA0008 outcome gate. NJA-000180 uses medium identity, A-side writer and content digest, B-side mount, and actual execution to build a three-gate A-to-media-to-B chain. It also compares a disguised entry's appearance with its command target and automatic seeding's volume enumeration and bulk writes. A USB insertion or user click on one host alone is not promoted to internal propagation."},
{"zh":"输出保留介质序列号可伪造、隔离区日志可能缺失和合法离线更新的限制。TA0001 的首个入口与 TA0008 的后续异机结果可以共用 NJT-0058，但必须给每次映射独立的源主机、介质及目标证据。","en":"Output preserves the limits of spoofable media serials, missing isolated-zone logs, and legitimate offline updates. Initial Access and later cross-host results can share NJT-0058, but each mapping requires its own source host, medium, and destination evidence."}],
["NJT-0058","NJS-0058-001","NJS-0058-002"],["NJA-000180"],"REF-000091"),
("DET-000168","internal-service-exploit-result",
{"zh":"内网服务利用请求—异机结果关联","en":"Internal Service Exploit Request to Remote Outcome Correlation"},
{"zh":"从内部服务利用输入连接目标异常状态与首个可控结果，并区分尝试、可能与确认。","en":"Join internal service exploit input to abnormal target state and first controlled outcome, separating attempt, probable result, and confirmation."},
[
{"zh":"本策略以服务漏洞因果入口为界：NJA-000181 连接源主机对脆弱内部服务的入站请求、协议异常或服务状态变化，以及目标上首次非基线进程、模块或后继连接。它同时核对事件时补丁和资产角色，不以开放端口、CVE 标签或一个 SMB 登录事件直接宣称利用成功。","en":"This strategy is bounded by the service-vulnerability causal entry. NJA-000181 joins an internal source's inbound request to a vulnerable service, protocol anomaly or service-state change, and the destination's first off-baseline process, module, or successor connection. It checks patch state and asset role at event time rather than treating an open port, CVE tag, or one SMB logon as exploit success."},
{"zh":"结果分为利用尝试、带一致后继信号的可能利用、以及具有独立目标效果的确认横向控制。ESET InvisiMole 对 EternalBlue 未见实际 exploit code 的限制要保留；NotPetya 的凭据与管理工具路径不能混入此策略的漏洞成功数。","en":"Outcomes are graded as exploit attempt, probable exploitation with consistent successor signals, and confirmed lateral control with an independent target effect. Preserve ESET InvisiMole's missing EternalBlue exploit-code limitation, and do not count NotPetya's credential or administration-tool routes as successful exploitation."}],
["NJT-0149"],["NJA-000181"],"REF-000599"),
("DET-000169","internal-lure-second-principal-outcome",
{"zh":"内部诱导消息—第二主体结果关联","en":"Internal Lure Message to Second-Principal Outcome Correlation"},
{"zh":"把受陷内部发件、另一员工动作及第二账户失陷连接成有向结果链。","en":"Join a compromised internal sender, another employee's action, and second-account compromise into a directed outcome chain."},
[
{"zh":"本策略针对内部可信身份被用作横向诱导的因果链。NJA-000182 从已确认受陷的发件身份和会话建立有向收件边，以 NetworkMessageId 连接邮件交付、URL 点击或可靠的附件打开，再以收件者对象 ID 连接调查确认的新异常登录或会话接管。仅发送或点击时分别保留 sent 与 acted 阶段，不声称已完成横向控制。","en":"This strategy targets the causal chain in which a trusted internal identity becomes a lateral lure. NJA-000182 builds directed recipient edges from a confirmed compromised sender and session, joins message delivery to URL clicks or reliably established attachment opens by NetworkMessageId, then joins the recipient object ID to investigator-confirmed abnormal sign-in or session takeover. Sending or clicking alone remains a sent or acted stage rather than completed lateral control."},
{"zh":"按主题归档警示回复可压低原邮箱所有者看到的反馈，但这是现有 NJS-0111-001 的默认视图遗漏变量。本策略仍在消息服务端连接规则变化、回复路由与受害者结果，帮助解释发现延迟；正常内部公告和安全演练须按批准计划排除。","en":"Subject-matched archiving of warning replies can suppress what the original mailbox owner sees, but that is the existing NJS-0111-001 default-view omission variable. This strategy still joins server-side rule changes, reply routing, and recipient outcomes to explain delayed discovery, while approved announcements and security simulations remain counterexamples."}],
["NJT-0150"],["NJA-000182"],"REF-000606"),
("DET-000170","existing-session-controller-lineage",
{"zh":"既有会话控制者—目标动作谱系","en":"Existing Session Controller to Target Action Lineage"},
{"zh":"比较旧认证传输或会话的原所有者与新控制者，并联接目标动作。","en":"Compare the original owner of an authenticated transport or session with a new controller and join the target action."},
[
{"zh":"本策略以“没有建立新的同等会话，却改变了谁能操纵旧连接”为检测目标。NJA-000183 在已认证 SSH transport 上检测新增 channel 与跳板本地控制套接字或客户端进程接触者的差异；NJA-000184 在既有 RDS LogonID 上连接 tscon、断开/重连与控制端变化；NJA-000185 对 shadow 并存控制检查策略、请求、原用户状态与后继资源动作。三者各自需要不同遥测，不把 SSH/RDP 协议名称当作 Niji 子项边界。","en":"The detection target is a change in who can operate an old connection without a comparable new session. NJA-000183 compares new channels on an authenticated SSH transport with processes touching the control socket or client on the jump host. NJA-000184 joins tscon, disconnect and reconnect, and controller change for an existing RDS LogonID. NJA-000185 tests shadow co-control through policy, request, original-user state, and successor resource action. Each needs distinct telemetry, and SSH versus RDP protocol names do not define Niji children."},
{"zh":"仅没有新认证事件不是劫持证明：授权复用、远程支持或日志缺失也会同形。告警需展示旧连接或会话 ID、新本地操作者、目标动作和批准记录；缺少 SSH 通道埋点或 RDS 控制操作日志时必须降低置信度。","en":"An absent new authentication event is not proof of hijacking: authorized reuse, remote support, and missing logs can look the same. Alerts should display the old connection or session ID, new local operator, target action, and approval record. Without SSH channel instrumentation or RDS control-operation logs, confidence must be lowered."}],
["NJT-0151","NJS-0151-001","NJS-0151-002"],["NJA-000183","NJA-000184","NJA-000185"],"REF-000613"),
]
assert len(SPECS)==5
for det,slug,name,summary,paragraphs,targets,analytic_ids,parent_ref in SPECS:
    refs=[parent_ref]
    for aid in analytic_ids:
        path=next((ROOT/"analytics").glob(aid+"-*.yaml"))
        a=yaml.safe_load(path.read_text())
        for ref in a["evidence_refs"]:
            if ref not in refs:refs.append(ref)
    obj={"schema_version":"2.0.0","type":"detection-strategy","id":det,
        "name":name,"summary":summary,"description":{"paragraphs":paragraphs},
        "detects_refs":targets,"domains":["enterprise"],"analytic_refs":analytic_ids,
        "evidence_refs":refs,
        "lifecycle":{"status":"draft","version":"0.1.0","created":"2026-09-22","modified":"2026-09-22",
                     "contributors":["Niji Matrix Research"],"reviewers":[]}}
    path=ROOT/"detections"/f"{det}-{slug}.yaml"
    if path.exists():raise RuntimeError(path)
    path.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
print("serialized",len(SPECS),"reviewed strategies")
