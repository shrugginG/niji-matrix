#!/usr/bin/env python3
"""Serialize eight candidate-specific, reviewed Detection Analytics."""
from pathlib import Path
import re
import yaml
ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
research={n:yaml.safe_load((RUN/f"{n}-handoff.yaml").read_text()) for n in ["T1080","T1091","T1210","T1534","T1563"]}
CANDIDATES={a["key"]:a for d in research.values() for a in d["defense_candidates"]["detection_analytics"]}
SPECS=[
("B8B-T1080-NJA-OBJECT-VERSION","NJA-000178","DET-000166",["Windows","SaaS"],
"把共享对象旧新版本的主动内容差异与另一主机的真实打开和首次执行连成链。","Join active-content differences between old and new shared-object versions to another host's real open and first execution.",
{"zh":"对同一对象版本从异常改写到异机消费追踪最长七天；预览、同步及离线设备延迟按存储服务实际日志调整。","en":"Track one object version from anomalous modification to cross-host consumption for up to seven days, adjusting for preview, synchronization, and offline-device delay."},
[{"zh":"经批准的宏更新、模板迁移或内部软件发布也可能产生相同版本—消费链。","en":"Approved macro updates, template migrations, and internal software releases may produce the same version-to-consumption chain."}],
[{"zh":"没有改写前版本、内容加密或未采集目标进程时，无法确认恶意语义差分或执行结果。","en":"Without a prior version, inspectable content, or destination process telemetry, the malicious semantic difference or execution result cannot be confirmed."}],
["REF-000590","REF-000591","REF-000379","REF-000593","REF-000594","REF-000190"]),
("B8B-T1080-NJA-NAV-ENTRY","NJA-000179","DET-000166",["Windows"],
"发现共享目录导航项指向替代命令后，关联另一主机点击时的原目录显示与恶意进程链。","Find a shared navigation entry redirected to a substitute command and join another host's click to both expected-directory display and malicious processes.",
{"zh":"共享目录改写到受害者导航默认观察七天；同一次点击到命令、文件及原目录打开默认五分钟。","en":"Observe up to seven days from share-directory mutation to victim navigation, then default to five minutes from one click to command, file, and original-directory activity."},
[{"zh":"合法快捷方式发布、DFS 调整和管理员重命名目录可能出现同名导航项。","en":"Authorized shortcuts, DFS changes, and administrator directory renames can create similar-looking navigation entries."}],
[{"zh":"只有文件服务器审计而缺少目标端 Explorer 和子进程谱系时，不能证明替身被用户实际触发。","en":"File-server audit without destination Explorer and child-process lineage cannot prove that a user triggered the substitute."}],
["REF-000592","REF-000474","REF-000379","REF-000595"]),
("B8B-T1091-NJA-MEDIA-CROSS-HOST","NJA-000180","DET-000167",["Windows"],
"以同一受控介质和载荷摘要连接 A 主机播种、B 主机接入与 B 上首次执行。","Join host A seeding, host B insertion, and B's first execution by the same controlled medium and payload digest.",
{"zh":"A 写入到 B 执行依合法介质轮转周期设窗，可从同日延至数周；B 接入到进程启动以分钟至一个工作班次为本地窗。","en":"Set the A-write-to-B-execution window from legitimate media rotation, ranging from the same day to weeks; use minutes to one work shift for B insertion to process launch."},
[{"zh":"获批准的离线补丁、取证拷贝及备份还原也会使同一介质在多机携带可执行文件。","en":"Approved offline patching, forensic copies, and backup restoration also carry executables on the same medium between hosts."}],
[{"zh":"隔离 B 无端点遥测、介质 ID 不稳定或载荷先复制到本地再运行，会使 A—介质—B 链失去确定性。","en":"No endpoint telemetry on isolated B, unstable media IDs, or a payload copied locally before launch can break deterministic A-to-media-to-B lineage."}],
["REF-000596","REF-000597","REF-000475","REF-000598","REF-000301"]),
("B8B-T1210-NJA-EXPLOIT-RESULT","NJA-000181","DET-000168",["Windows"],
"把内网源到脆弱服务的请求、目标异常状态和另一主机首个受控结果分层关联。","Correlate an internal source's request to a vulnerable service, abnormal target state, and first controlled result on another host in graded stages.",
{"zh":"以入站服务请求前后十分钟连接异常响应与首个目标结果；若服务恢复或载荷延迟，延长调查窗并明确降级置信度。","en":"Join abnormal response and first target outcome within ten minutes around an inbound service request; extend the investigation window for restarts or delayed payloads and mark lower confidence."},
[{"zh":"漏洞扫描、故障重试与正常服务重启可形成请求后错误或进程变化，需同时审查业务解释。","en":"Vulnerability scans, fault retries, and normal service restarts can create request-to-error or process changes that require a business explanation check."}],
[{"zh":"加密协议、无服务内部事件、旧补丁台账或利用后内存运行可遮住关键转折；SMB 会话并不单独证明 EternalBlue 成功。","en":"Encrypted protocols, absent service events, stale patch inventory, or in-memory post-exploit activity obscure the transition; an SMB session alone does not prove EternalBlue success."}],
["REF-000591","REF-000602","REF-000603","REF-000604","REF-000605","REF-000598","REF-000377"]),
("B8B-T1534-NJA-SEND-OUTCOME","NJA-000182","DET-000169",["SaaS","Windows"],
"重建受陷内部发件账户到另一收件者动作与第二账户失陷的有向消息谱系。","Reconstruct a directed message lineage from a compromised internal sender through another recipient's action to second-account compromise.",
{"zh":"默认二十四小时连接消息投递、点击或附件打开与第二账户异常；针对延迟动作按事件调查延长，保留先前已失陷的替代解释。","en":"Default to twenty-four hours joining delivery, click or attachment open, and second-account anomaly; extend for delayed action while retaining prior compromise as an alternative explanation."},
[{"zh":"获批安全演练、帮助台通知和真实内部共享也会出现带链接或附件的内网消息。","en":"Approved security simulations, help-desk notices, and genuine internal sharing also produce intra-organization messages with links or attachments."}],
[{"zh":"没有邮件安全许可、协作消息不入日志或收件者身份调查未完成时，无法确认完整跨主体结果。","en":"Missing mail-security licensing, unlogged collaboration messages, or an unfinished recipient identity investigation prevent a complete cross-principal outcome conclusion."}],
["REF-000607","REF-000608","REF-000609","REF-000610","REF-000611","REF-000612"]),
("B8B-T1563-NJA-SSH-CHANNEL","NJA-000183","DET-000170",["Linux","macOS"],
"将旧 SSH 认证传输上的新逻辑通道与本地套接字或客户端进程接触者关联。","Join a new logical channel on an old authenticated SSH transport to the local process touching its control socket or client.",
{"zh":"本地控制套接字访问到新通道默认两分钟；原连接到后继通道按真实传输寿命追踪，最长二十四小时并按跳板任务调优。","en":"Default to two minutes from local control-socket access to new channel; follow the original connection through its actual lifetime, up to twenty-four hours with jump-host tuning."},
[{"zh":"批准的 ControlMaster 多终端复用、备份、部署和合法调试也会在同一认证连接上增加通道。","en":"Approved multi-terminal ControlMaster use, backup, deployment, and legitimate debugging also add channels on one authenticated connection."}],
[{"zh":"标准 sshd 未必提供稳定通道 ID；缺少跳板 socket 或 ptrace 遥测时不能断言通道由另一控制者打开。","en":"Stock sshd may lack stable channel IDs; without jump-host socket or ptrace telemetry, a different controller cannot be attributed reliably."}],
["REF-000614","REF-000615","REF-000616","REF-000370"]),
("B8B-T1563-NJA-RDP-ATTACH","NJA-000184","DET-000170",["Windows"],
"把既有 RDS LogonID 的断开—重连与 tscon 进程、控制端变化及后继动作相连。","Join disconnect and reconnect of an existing RDS LogonID to tscon execution, controller change, and follow-on actions.",
{"zh":"同一 LogonID 的 4779 到 4778 默认五分钟，tscon 进程前后两分钟；目标结果按具体操作再观察十分钟。","en":"Default to five minutes from 4779 to 4778 for one LogonID, two minutes around tscon, and ten more minutes for a target action."},
[{"zh":"帮助台移交、断线重连或管理员按批准流程切换会话可产生同形事件。","en":"Help-desk handoff, reconnection after network loss, and approved administrator session switching can produce the same event shape."}],
[{"zh":"4778/4779 缺失、命令行未记录或会话 ID 在重启后复用时，无法单靠时间邻接确认劫持。","en":"Missing 4778 or 4779, absent command lines, or session-ID reuse after reboot prevents confirmation from temporal adjacency alone."}],
["REF-000617","REF-000621","REF-000622","REF-000623","REF-000624","REF-000618"]),
("B8B-T1563-NJA-RDP-SHADOW","NJA-000185","DET-000170",["Windows"],
"连接影子控制策略变化、shadow 请求、原会话活动及未经批准的共同控制结果。","Join shadow-control policy changes, shadow requests, original session activity, and unapproved co-control outcomes.",
{"zh":"策略改变到影子请求可观察二十四小时；请求到同一会话控制默认两分钟，再追踪目标动作十分钟。","en":"Observe up to twenty-four hours from policy change to shadow request, default to two minutes from request to control of the same session, and follow target actions for ten minutes."},
[{"zh":"获批准的远程支持、培训和无障碍协助会使用 shadow 或共享会话。","en":"Approved remote support, training, and accessibility assistance may use shadow or shared sessions."}],
[{"zh":"缺少 shadow 操作日志或原用户在场证明时，只能把进程与策略变化判为风险信号，不能断言实际共同控制。","en":"Without shadow-operation logs or proof of the original user's presence, process and policy changes remain risk signals rather than confirmed co-control."}],
["REF-000618","REF-000619","REF-000620","REF-000621","REF-000622","REF-000623"]),
]
assert len(SPECS)==8
DATA_NAMES={
"shared-object-version-history":("共享对象版本历史","Shared-object version history"),
"windows-security-file-access":("Windows 文件对象访问审计","Windows file-object access audit"),
"endpoint-object-consumption":("目标端对象读取或打开","Destination object read or open"),
"endpoint-process-and-network":("目标端进程与网络结果","Destination process and network outcomes"),
"approved-content-change":("批准内容变更记录","Approved content-change records"),
"shared-directory-change":("共享目录变更历史","Shared-directory change history"),
"navigation-entry-metadata":("导航入口目标与外观元数据","Navigation entry target and appearance metadata"),
"windows-security-detailed-file-share":("Windows 详细共享访问审计","Windows detailed share-access audit"),
"endpoint-process-tree":("目标端进程树","Destination process tree"),
"media-device-endpoint":("介质接入与设备控制事件","Media insertion and device-control events"),
"endpoint-file-activity":("端点文件活动","Endpoint file activity"),
"endpoint-process-activity":("端点进程活动","Endpoint process activity"),
"media-transfer-ledger":("批准介质流转台账","Approved media-transfer ledger"),
"internal-network-ndr":("内网协议与利用告警","Internal protocol and exploit alerts"),
"target-service-health":("目标服务响应与状态","Target service response and state"),
"target-process":("目标进程创建","Destination process creation"),
"target-successor-network":("目标后继网络连接","Destination successor connections"),
"time-valid-vulnerability-state":("事件时软件和漏洞状态","Event-time software and vulnerability state"),
"m365-email-processing":("内部邮件投递事件","Internal email-processing events"),
"m365-url-click":("邮件 URL 点击事件","Email URL click events"),
"identity-and-investigation":("身份登录与事件调查","Identity sign-in and investigation"),
"optional-attachment-endpoint-join":("附件与目标端文件关联","Attachment and destination-file join"),
"instrumented-openssh-connection-channel":("经验证的 SSH 连接和通道遥测","Validated SSH connection and channel telemetry"),
"jump-host-unix-socket-and-debug-access":("跳板主机套接字和调试访问","Jump-host socket and debug access"),
"destination-process-lineage":("目标 SSH 进程谱系","Destination SSH process lineage"),
"approved-ssh-sharing-inventory":("批准 SSH 复用关系","Approved SSH-sharing relationships"),
"windows-rds-session-transition":("Windows RDS 会话转换事件","Windows RDS session transition"),
"windows-remote-interactive-logon":("Windows 远程交互登录","Windows remote interactive logon"),
"windows-process-creation":("Windows 进程创建与命令行","Windows process creation and command line"),
"rds-approval-and-asset-context":("RDS 支持审批与资产情境","RDS support approval and asset context"),
"rds-session-control-operation":("RDS 会话影子控制操作","RDS session shadow-control operation"),
"rds-shadow-policy-state":("RDS 影子控制策略状态","RDS shadow-control policy state"),
}
CHANNELS={
"windows-security-file-access":"Security/4663",
"windows-security-detailed-file-share":"Security/5145",
"media-device-endpoint":"Microsoft Defender XDR/DeviceEvents",
"endpoint-file-activity":"Microsoft Defender XDR/DeviceFileEvents",
"endpoint-process-activity":"Microsoft Defender XDR/DeviceProcessEvents",
"target-process":"Microsoft Defender XDR/DeviceProcessEvents",
"target-successor-network":"Microsoft Defender XDR/DeviceNetworkEvents",
"time-valid-vulnerability-state":"Microsoft Defender XDR/DeviceTvmSoftwareVulnerabilities",
"m365-email-processing":"Microsoft Defender XDR/EmailEvents",
"m365-url-click":"Microsoft Defender XDR/UrlClickEvents",
"optional-attachment-endpoint-join":"Microsoft Defender XDR/EmailAttachmentInfo",
"windows-rds-session-transition":"Security/4778,4779",
"windows-remote-interactive-logon":"Security/4624",
"windows-process-creation":"Security/4688",
}
def norm(value):
    value=str(value).replace(" ", "_").replace("/", "_").replace(":", "_")
    value=re.sub(r"(?<=[a-z0-9])(?=[A-Z])","_",value)
    value=re.sub(r"[^A-Za-z0-9_.-]+","_",value).lower()
    return value.strip("_")
def section(value):
    assert isinstance(value,dict) and isinstance(value.get("zh"),str) and isinstance(value.get("en"),str)
    return {"paragraphs":[{"zh":value["zh"],"en":value["en"]}]}
for key,nja,strategy,platforms,summary_zh,summary_en,window,fp,blind,evidence in SPECS:
    a=CANDIDATES[key]
    raw=a.get("data_requirements") or a.get("required_data")
    data=[]
    for item in raw:
        source_type=norm(item["source_type"]).replace("_","-")
        name=item.get("name") or DATA_NAMES[source_type]
        if isinstance(name,tuple):name={"zh":name[0],"en":name[1]}
        fields=item.get("required_fields") or item.get("fields")
        normalized=list(dict.fromkeys(norm(x) for x in fields))
        data.append({"source_type":source_type,"name":name,"channel":CHANNELS.get(source_type),
                     "required_fields":normalized})
    observable=a.get("observables")
    if not observable:
        observable=[
          {"zh":"同一介质在 A 主机新增诱导入口后于不同的 B 主机接入，B 随后运行与该介质内容相同的脚本或安装器。","en":"The same medium gains a lure on host A, appears on distinct host B, and B then runs a script or installer matching content on that medium."},
          {"zh":"A 端接入后的自动卷枚举与批量写入先于 B 端第一次执行，且该流转不在批准离线发布台账中。","en":"Automatic volume enumeration and bulk writes after insertion on A precede first execution on B, outside an approved offline release ledger."}]
    for item in observable:
        assert isinstance(item,dict) and set(item)=={"zh","en"},(key,item)
    dimensions=a.get("dimensions") or a.get("correlation",{}).get("dimensions")
    dimensions=list(dict.fromkeys(norm(x) for x in dimensions))
    logic=a["logic"]
    tuning=a["tuning"]
    assert set(logic)=={"zh","en"} and set(tuning)=={"zh","en"},key
    obj={"schema_version":"2.0.0","type":"detection-analytic","id":nja,"strategy_ref":strategy,
        "name":a.get("name") or {"zh":nja,"en":summary_en},
        "summary":{"zh":summary_zh,"en":summary_en},"domains":["enterprise"],"platforms":platforms,
        "logic":section(logic),"data_requirements":data,"observables":observable,
        "correlation":{"window":window,"dimensions":dimensions},"false_positives":fp,
        "blind_spots":blind,"tuning_guidance":section(tuning),"evidence_refs":evidence,
        "lifecycle":{"status":"draft","version":"0.1.0","created":"2026-09-22","modified":"2026-09-22",
                     "contributors":["Niji Matrix Research"],"reviewers":[]}}
    # T1091 research expresses a natural name in its strategy; give its analytic
    # the distinct A-media-B identity rather than using an ID as a visible title.
    if key=="B8B-T1091-NJA-MEDIA-CROSS-HOST":
        obj["name"]={"zh":"介质 A—B 主机传播链分析","en":"Media A-to-B Host Propagation Lineage Analytic"}
    slug=re.sub(r"[^a-z0-9]+","-",key.removeprefix("B8B-").lower()).strip("-")
    path=ROOT/"analytics"/f"{nja}-{slug}.yaml"
    if path.exists():raise RuntimeError(path)
    path.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
print("serialized",len(SPECS),"reviewed analytics")
