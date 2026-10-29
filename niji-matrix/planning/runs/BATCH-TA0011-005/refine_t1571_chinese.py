"""Polish the T1571 parent Chinese prose while retaining its reviewed evidence gates."""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "matrix/tactics/TA0011-command-and-control/techniques/NJT-0221-port-expectation-semantic-mismatch/technique.yaml"
parent = yaml.safe_load(P.read_text())

def replace(section, texts):
    paragraphs = section["paragraphs"]
    if len(paragraphs) != len(texts):
        raise ValueError((len(paragraphs), len(texts)))
    for item, text in zip(paragraphs, texts):
        item["zh"] = text

replace(parent["definition_and_concept"], [
    "端口预期语义错配是攻击者配置控制端与植入体，使线上实际运行的协议或应用，与目标环境为该来源、目的地和端口组合登记的服务不一致。实际通信可以是完整的 HTTP、SSH 等应用事务，也可以是自定义二进制会话；攻击者借用按端口放行的策略、解析器选择或服务标签，以降低阻断和语义可见性。技术边界由当地预期与真实语义之间的差确定，不由端口号高低、IANA 默认表或协议名称决定。",
    "认定时需要连接四层证据：实际连接及端口；通过载荷感知解析、协议仿真或端点实现证明的真实语义；资产目录、策略和解析器配置所给出的预期服务与处理结果；以及同一会话或端点进程产生的任务、响应、命令结果或持续信标。缺少策略和解析差异时只能记录端口配置，缺少后继控制时只能记录协议异常，两者都不足以完成本技术。",
])
replace(parent["stealth_characteristics"], [
    "只按端口放行的防火墙可能把 TCP/443 或 UDP/53 视作必需的 Web 或 DNS 出口，即使实际载荷并非 TLS 或 DNS。按端口启动解析器的传感器也可能选错协议、解析失败，或在日志中留下“未知服务”而没有任务和结果字段。只看目的端口和表面服务标签的分析者因此会把自定义控制通信误作被允许的业务。公开流量研究与 Zeek 的解析示例说明端口名称不能代替内容确认。",
    "这种错配不会消除首包、握手和响应、解析器确认或失败、应用识别结果、策略规则与动作、端点进程和命令结果等残余痕迹。端口无关的动态协议检测、协议仿真和应用感知策略可以恢复真实语义；加密、未知专有协议、采样或只保存流量摘要会限制这一能力，但“未知”本身不能证明恶意。",
])
replace(parent["scope_boundary_definition"], [
    "纳入范围要求控制通信的真实语义与当地服务预期不一致，并由此产生过滤、解析或记录差异。HTTP 使用非预期高位端口、自定义二进制协议使用 443、专有消息使用 53 都可能满足条件，但必须逐一证明本地映射、具体防守效果和后继控制结果。已登记且正确解析的内部自定义服务、测试服务、厂商管理端口、端口共享、TLS 卸载和迁移例外是反例；偏离 IANA 默认端口并不自动构成攻击。",
    "非应用层协议技术拥有自定义 TCP、UDP 或 ICMP 通信本身；本项只拥有该通信与端口预期的错配，因此同一 FlawedGrace、Winnti 或 PseudoManuscrypt 会话可以并列归类，却不会因为使用 443 就成为 HTTPS。应用层协议技术则拥有真实 HTTP、SSH 或其他应用事务，不受端口号限制；当这些事务使用当地未预期的端口时才另外成立本项。",
    "代理技术拥有中继路径，协议隧道技术要求可识别的内层会话被外层承载，流量信令技术要求特殊输入激活隐藏功能；任何一个端口号都不能替代这些行为证据。动态求得的端口归运行时端点求取，伪造 TLS 握手或服务外观归消息与服务伪装，附加密码层归加密通道。只有各自变量与后继控制分别成立时才并列归类。",
])
replace(parent["application_scenarios_and_threat_model"]["application_scenarios"], [
    "在仅按 TCP/443 放行 Web 出口的环境，植入体可直接以自定义二进制协议连接控制端。DFIR Report 在真实入侵中观察到 FlawedGrace 从被注入的 svchost.exe 连接多个 443 控制端，却没有 SSL 证书或 JA3；VMware 的 Winnti 4.0 协议仿真也在 443 发出自定义加密请求并得到可验证响应。这些案例证明真实语义与 HTTPS 标签不同，并存在后继控制；具体企业是否因此误放行仍须核对当地策略。",
    "PseudoManuscrypt 在 UDP/53 和 TCP/443 上使用自有的分层消息协议。BitSight 实现该协议后，通过接管的控制端收到约五万台感染设备的通信；53 和 443 在此都不能直接等同 DNS 或 TLS。若某组织将同样端口正式分配给专有设备并能正确识别协议，就没有本项要求的当地预期差；预期必须来自该组织的策略和资产登记。",
])
replace(parent["application_scenarios_and_threat_model"]["threat_model"]["attacker_model"], [
    "攻击者需要控制植入体和监听器的端口配置、选取目标可达且较易放行的端口，并实现能够交换任务与结果的实际协议。匿迹收益还取决于对目标防火墙、解析器和日志按端口作何假设的了解；动态协议检测与应用识别会削弱这种收益。无效握手、未知载荷、异常进程和长连接也可能让错配更显眼，自定义协议还增加开发与运维成本。",
])
replace(parent["application_scenarios_and_threat_model"]["threat_model"]["defender_model"], [
    "防守方至少掌握连接流量和一种能够识别载荷的解析器或防火墙，并可把它们与端点进程或协议仿真的控制结果相连。资产目录及策略提供来源角色、目的服务、允许应用、规则版本和所有者；传感器提供实际识别的协议、解析失败和策略动作。缺少真实语义或当地预期映射时，只能标记为未知或未登记，不能断言端口预期错配。",
    "合法自定义服务应按来源、目的地、端口、协议、解析规则、用途和期限登记，避免把一切非默认通信告警。TLS、QUIC、VPN、代理、NAT、采样及不受支持的专有协议会降低解析能力；解析失败也可能来自短流、丢包或正常应用。端点任务结果可以提高置信，却不能倒推出未被记录的过滤或日志差异。",
])
replace(parent["stealth_mechanisms"][0]["analysis"], [
    "攻击者把自定义协议或另一种应用协议放到环境标为 Web、DNS 或其他允许服务的端口，令连接记录中的端口标签与真实语义分离。依赖端口类别的规则和分析者把预期服务误当作实际服务，恶意会话借用正常服务外观，形成特征伪装。FlawedGrace、Winnti、PseudoManuscrypt 和流量研究支持这种错配；载荷感知解析与握手验证可以恢复真实协议。",
])
replace(parent["stealth_mechanisms"][1]["analysis"], [
    "如果传感器按端口启用错误解析器，或不支持自定义协议，任务与结果可能只留下连接记录、未知服务或解析失败，而没有进入预期的 TLS、HTTP 或 DNS 事务日志。只查询该事务日志的检测因此看不到关键控制动作，形成有条件的行为透明。Zeek 与 Suricata 的解析状态字段可记录这一断点；启用端口无关检测后，效果会明显减弱。",
])
replace(parent["subtechnique_taxonomy"]["narrative"], [
    "端口策略借用与按端口选定解析器的错位，分别影响放行决策和语义日志，但攻击者控制的共同变量都是“真实协议与预期服务不一致”。两种结果由防守部署决定，不能稳定分成兄弟子技术；父级机理和检测分析保留这两类影响。",
    "真实通信是已知应用还是专有协议，属于应用层协议与非应用层协议的直接对象；端口范围、传输层、方向和工具名称也只是实现条件。运行时端口计算、伪造服务握手和信号激活分别由相邻技术拥有。现有证据没有给出另一项独立攻击者变量及其专属防御，因此本技术不再拆分子项。",
])
replace(parent["research"]["limitations"], [
    "FlawedGrace、Winnti 与 PseudoManuscrypt 直接证明真实协议、所用端口及后继控制，却没有公开各受害组织的防火墙策略、代理预期或解析器输出。它们不能单独证明具体现场已发生过滤绕过或日志错分。正式认定须补充当地规则、动作与解析结果；缺少部署证据时，只能记录协议—端口错配候选。",
    "Zeek、Suricata 与 PAN-OS 文档证明字段和控制措施可以实施，并不证明检测率或恶意意图。解析失败可由协议升级、错误配置、短流与单向流引起；应用识别也可能在会话中变化，并受解密和签名覆盖限制。十五分钟与二十四小时窗口只是工程起点，应以当地测试流量、报文重放和合法自定义服务校准。",
    "较早的流量研究说明按端口推断 TLS 容易错分及内容验证的价值，但其样本和网络环境不能代表当前流行度或阈值。专有加密可能阻止真实语义恢复；协议仿真可以验证已知家族响应，却不能假定总能对活跃控制端合法探测。解析器没有得出语义，既不能证明本技术存在，也不能证明其不存在。",
])
P.write_text(yaml.safe_dump(parent, allow_unicode=True, sort_keys=False, width=120))
print("Refined all T1571 parent Chinese reader-prose responsibilities")
