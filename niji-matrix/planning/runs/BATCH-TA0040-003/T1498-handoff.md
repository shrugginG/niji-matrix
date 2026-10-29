# T1498 Network Denial of Service research handoff

`batch_ref: BATCH-TA0040-003`  
`work_item_ref: WORK-TA0040-T1498`  
`temporary_key_prefix: TA0040-T1498-`  
`status: research-only; integration pending`  
`baseline: Enterprise ATT&CK 19.1`  
`formal IDs allocated: none`

## Recommendation

**Adapt; high confidence; two formal Niji children proposed.** Proposed bilingual admission rationale:

> 网络拒绝服务以攻击流量耗尽网络链路、路径或边界设备为合法通信提供容量，使用户即使面对仍在运行的端点也无法稳定到达服务，直接属于 TA0040。Niji 应把正式范围适配为两类有独立证据的低可归因容量耗尽设计：攻击者让大量来源各自只贡献较小流量、迫使防守从目的端聚合后才能看见完整洪泛；或伪造受害者源地址驱动第三方响应者回包，使受害侧看到响应者而非真实发起者。两者分别改变局部阈值和源因果观察，且要求不可互换的检测与缓解。[E1][E4][E5][E6]
>
> Network Denial of Service uses attack traffic to exhaust the capacity that links, paths, or boundary devices provide to legitimate communications, making a service unreachable even when its endpoint remains running and directly serving TA0040. Niji should adapt the formal scope to two independently evidenced low-attribution capacity-exhaustion designs: the adversary divides the flood among many sources so each contributes little and defenders must aggregate at the destination to see the operation, or spoofs the victim's source address so third-party responders send the visible traffic and the victim observes responders rather than the true initiator. These designs respectively change local-threshold and source-causality observation and require noninterchangeable detection and mitigation.[E1][E4][E5][E6]

The parent behavior, source dispersion, and reflection causality are high-confidence. No ATT&CK child is imported: the proposed children use defender-observation variables rather than direct-versus-reflected delivery labels, and reflection amplification's volume multiplier remains parent-level attack economics rather than an NJS boundary.

## Required boundary convergence

- **T1498 versus T1499 Endpoint Denial of Service:** T1498 requires exhaustion or obstruction of network capacity, a transit/boundary queue, or the providing link. T1499 owns CPU, memory, connection tables, application workers, parser/exploit crash, or other endpoint/application exhaustion when the providing network remains below saturation. The same packet stream may exercise both; classification must state which resource crossed capacity and which availability probe failed.[E1][E13]
- **T1498 versus T1496/NJT-0189 bandwidth use:** T1496 consumes a victim's bandwidth or provider quota to complete an attacker task such as proxying, resale, spam, or another workload, with cost/capacity impact left to the owner. T1498 directs traffic to deny a target's legitimate network availability. Incidental slowdown from proxyjacking remains T1496 unless denial is the direct objective/result; a hijacked host used as a flood source can map to T1496 for unauthorized resource use and T1498 for the target-facing flood, with separate evidence.[E14][L1]
- **Botnet and C2:** malware installation, enrollment, rental, command distribution, and operator control are prerequisites or adjacent C2/resource-development behaviors. T1498 begins with actual flood traffic and network-capacity result. A list of source IPs does not prove those systems are bots, compromised, or controlled through one C2.[E4][E6]
- **Source and reflection attribution:** visible flow source identifies the immediate sender of packets, not necessarily the adversary. In direct botnet floods it may be a compromised device using its normal IP; in reflection it is a third-party responder that received a request carrying the victim's spoofed address. Reflectors need not be compromised, and blocking them does not identify the initiator.[E4][E6][E7]
- **Flash crowd and operational congestion:** a legitimate demand surge can produce high aggregate bandwidth and many sources. Capacity, source topology, protocol success, authorization/business context, and external availability must be joined; traffic volume or source count alone cannot prove malicious intent.[E6][E11]

## ATT&CK child coverage and native-axis review

Fixed ATT&CK 19.1 child count: **2**. Breadth trigger: ordinary, with explicit planning-only coverage for both. Proposed Niji child count: **2**. `lineage.attck_subtechnique_inherited: false` for both future NJS objects.

| ATT&CK child | Planning-only resolution | Niji coverage conclusion |
| --- | --- | --- |
| T1498.001 Direct Network Flood | `niji-variable-candidate` plus `parent-core` remainder | Botnet evidence that numerous sources can each contribute little supports **Multi-Source Low-Contribution Flooding**. One-source or few-source direct volume remains parent core and does not itself establish stealth.[E2][E4][E5] |
| T1498.002 Reflection Amplification | `niji-variable-candidate` plus `parent-core` remainder | Spoofed-victim requests causing third-party responses support **Response-Origin Attribution Displacement**. Amplification factor, reflector protocol, and server type affect volume/cost but do not define the child.[E3][E6][E8] |

Open-ended axes examined:

| Candidate Niji axis | Trace change and defender effect | Resolution |
| --- | --- | --- |
| Many true/immediate sources with low per-source contribution | Local source monitors see small fractions and single-source filters explain little; destination/prefix aggregation exposes the flood | **Formal child 1**; stable source-distribution variable with distinct aggregation defense.[E2][E4][E5] |
| Third-party responses replace the initiating source in victim-visible traffic | Victim sees legitimate responder addresses and no corresponding outbound request; traceback by visible source stops at reflectors | **Formal child 2**; stable causal-source displacement with request/response and source-validation defense.[E3][E6][E7][E8] |
| Spoofed direct flood without reflection | Source values can be fabricated and filters weakened | `evidence-deferred`; attributable-source uncertainty is real, but current evidence does not establish a sibling boundary and detection distinct from the parent plus reflection child. |
| Pulsing or low-rate temporal bursts | Short windows may alternate between congestion and recovery | `evidence-deferred`; no conclusion-level T1498 source reviewed establishes an intentional timing pattern and useful independent control set. |
| Destination-prefix or “carpet” dispersion | Per-address thresholds may remain low while one access link/prefix saturates | `evidence-deferred`; plausible prefix-aggregation variable, but this research lacks primary attack evidence sufficient for a formal child. |
| Protocol, port, packet size, or amplification ratio | These change efficiency and filter signatures | `not-stealth-distinct`; protocol and volume multiplier are implementations/attack economics, not stable defender-observation siblings.[E3][E6] |
| Multi-vector campaign | Several floods or application attacks occur together | `parent-core / relationship`; campaign composition does not create a child, and application-resource outcomes may additionally map to T1499. |
| Botnet family, rental market, or C2 topology | Changes attacker control and supply chain | `adjacent-technique`; not part of flood outcome taxonomy. |

## Proposed parent content (`TA0040-T1498-PARENT`)

Name: **低可归因网络容量拒绝服务 / Low-Attribution Network Capacity Denial of Service**  
Aliases: `Network Denial of Service`, `T1498`  
Summary:

> 攻击者以分散来源或第三方响应来源汇聚攻击流量，耗尽目标网络容量，同时削弱单源检测和真实发起者归因。
>
> Adversaries converge attack traffic through dispersed sources or third-party responders to exhaust target network capacity while weakening single-source detection and attribution of the true initiator.

### `definition_and_concept`

> 低可归因网络容量拒绝服务是攻击者向受保护地址、服务前缀、接入链路或其依赖的网络设备汇聚足量流量，使合法通信因带宽、转发队列或边界处理容量耗尽而丢包、超时或无法建立连接。直接对象是提供访问的网络容量和路径结果；协议、端口、工具、僵尸网络家族及政治或勒索动机不是概念边界。[E1][E6][E12]
>
> Low-Attribution Network Capacity Denial of Service is adversary convergence of enough traffic on a protected address, service prefix, access link, or dependent network device that legitimate communications drop, time out, or fail to connect because bandwidth, forwarding queues, or boundary-processing capacity is exhausted. The direct object is the network capacity providing access and its path outcome; protocol, port, tool, botnet family, and political or extortion motive do not define the concept.[E1][E6][E12]

> Niji 的正式范围要求攻击者控制来源拓扑或因果来源呈现，以降低识别、过滤或归因。多源低贡献设计把完整操作拆成许多局部弱信号；响应源置换则让第三方服务器以自身地址发送由伪造请求触发的回包。单一高带宽发送者、明显测试流量或没有观察变化的容量攻击可属于 ATT&CK 父行为，但不进入本适配后的正式匿迹范围。[E2][E3][E4][E6]
>
> Formal Niji scope requires attacker control over source topology or presentation of causal origin that weakens identification, filtering, or attribution. Multi-source low-contribution design decomposes the operation into many locally weak signals. Response-origin displacement makes third-party servers send responses under their own addresses after spoofed requests. A single high-bandwidth sender, conspicuous stress test, or capacity attack without an observation change can satisfy the ATT&CK parent behavior but remains outside this adapted formal stealth scope.[E2][E3][E4][E6]

### `stealth_characteristics`

> 低可归因网络容量拒绝服务改变“在哪里能看到完整洪泛”和“可见源是否等于发起者”。多源洪泛在每个发送网络或来源上只留下较小贡献，目的端聚合才显示总量；反射路径中，受害方直接看到的是正常协议响应者，真实请求发送者不在返回路径。基于单源速率、源名单或最近会话的局部检测因此失去区分力。[E4][E5][E6]
>
> Low-Attribution Network Capacity Denial of Service changes where the complete flood is visible and whether visible source equals initiator. A multi-source flood leaves only a small contribution at each sending network or source and becomes complete only after destination aggregation. In reflection, the victim directly sees ordinary protocol responders while the true request sender is absent from the return path. Local detection based on one-source rate, source lists, or recent sessions therefore loses discrimination.[E4][E5][E6]

> 残余包括目的前缀和入口接口的总 bps/pps、源/ASN 多样性、top-k 来源占比、流量方向、请求—响应不对称、接口丢弃、队列或链路利用率、外部可达性、上游清洗事件及反射服务特征。跨入口 flow、接口计数、外部探针和上游提供方视角能恢复完整图像；采样、非对称路由、NAT、Anycast 和合法突发会削弱或混淆结论。[E9][E10][E11]
>
> Residual evidence includes aggregate bps and pps at the destination prefix and ingress interface, source and ASN diversity, top-k source share, flow direction, request-response asymmetry, interface discards, queue or link utilization, external reachability, upstream scrubbing events, and reflector-service features. Cross-ingress flow, interface counters, external probes, and upstream-provider views recover the full picture. Sampling, asymmetric routing, NAT, Anycast, and legitimate bursts weaken or confound conclusions.[E9][E10][E11]

### `scope_boundary_definition`

> 纳入要求攻击者导向的聚合流量实际使网络链路、路径、边界转发或协议容量跨越正常承载能力，并造成合法用户的丢包、超时或不可达，同时有证据证明多源低贡献或响应源置换这一观察变量。流量峰值、单个大流、源地址多或一次健康检查失败均不足；须连接容量基线、接口结果、外部可达性和来源拓扑。[E1][E5][E9][E10]
>
> Inclusion requires adversary-directed aggregate traffic to exceed the normal carrying capacity of a network link, path, boundary forwarding plane, or protocol surface and cause packet loss, timeout, or unreachability for legitimate users, with evidence of multi-source low contribution or response-origin displacement. A traffic spike, one large flow, many source addresses, or one failed health check is insufficient. Capacity baseline, interface result, external reachability, and source topology must be joined.[E1][E5][E9][E10]

> 端点 CPU、内存、连接状态、服务线程或应用解析器被耗尽而网络未饱和归 T1499；受害带宽被用于代理、转发或其他攻击者任务而拒绝服务不是直接目标归 T1496/NJT-0189。Botnet/C2 只描述来源取得与协调。获批压力测试、流量迁移、备份/复制、Flash Crowd、路由故障、链路故障和监控错误是反例；反射流量的可见服务器不能未经证据标记为攻击者基础设施。[E13][E14][L1]
>
> Exhaustion of endpoint CPU, memory, connection state, service threads, or an application parser while the network is not saturated belongs to T1499. Victim bandwidth used for proxying, forwarding, or another adversary task when denial is not the direct objective belongs to T1496/NJT-0189. Botnet and C2 describe acquisition and coordination of sources. Approved stress tests, traffic migration, backup or replication, flash crowds, routing failure, link failure, and monitoring error are counterexamples. Visible servers in reflected traffic cannot be labeled adversary infrastructure without evidence.[E13][E14][L1]

### `application_scenarios_and_threat_model`

Application scenarios:

> 攻击者可租用或控制分布于多个网络的设备，让每个节点以不显著的本地速率向同一服务前缀发送 UDP、ICMP、TCP 或其他流量，最终压满目标接入链路。另一场景中，攻击者从允许源地址伪造的网络向开放 DNS、NTP 或其他响应服务发送带受害地址的小请求，由响应者把大量回包汇聚到受害网络。两种场景均可与应用攻击并发，但本父级只判断网络容量结果。[E2][E3][E4][E6]
>
> An adversary can rent or control devices spread across many networks and have each node send UDP, ICMP, TCP, or other traffic at a locally unremarkable rate toward one service prefix until the target access link fills. In another scenario, an adversary in a network permitting source-address spoofing sends small requests carrying the victim address to open DNS, NTP, or other response services, causing responders to converge large replies on the victim network. Either scenario can coincide with application attacks, but this parent assesses only the network-capacity result.[E2][E3][E4][E6]

Attacker model:

> 多源路径要求足够多可控或可租发送者、统一目标和时间协调以及对目标容量的粗略估计，但不必伪造地址。响应源置换要求出站网络允许伪造受害者地址，并存在会向该地址回包的第三方服务；放大提高效率却不是归因置换的必要定义。上游源地址验证、反射器访问控制、限速、Anycast/清洗容量和攻击成本会限制效果。[E4][E6][E7][E8]
>
> The multi-source path needs enough controlled or rented senders, common target and timing coordination, and a rough estimate of target capacity, but does not require address spoofing. Response-origin displacement requires an egress network that permits spoofing of the victim address and third-party services that respond to it. Amplification improves efficiency but is not necessary to define attribution displacement. Upstream source-address validation, reflector access control, rate limiting, Anycast or scrubbing capacity, and attack cost constrain the effect.[E4][E6][E7][E8]

Defender model:

> 防守方在多个入口采集 IPFIX/NetFlow、接口高容量计数、路由和清洗事件，并从目标网络外运行可达性探针；其维护按前缀、服务、时段和事件的合法容量/来源基线。为区分 T1499，还需端点 CPU、内存、连接表与应用队列。若只看单一边界、采样过粗、缺少出站请求视角或上游先丢弃流量，来源分布和反射因果会不完整。[E9][E10][E11]
>
> Defenders collect IPFIX or NetFlow, high-capacity interface counters, routing and scrubbing events across multiple ingress points and run reachability probes outside the target network. They maintain legitimate capacity and source baselines by prefix, service, time, and event. Endpoint CPU, memory, connection tables, and application queues are also needed to distinguish T1499. A single boundary, coarse sampling, absent outbound-request view, or upstream packet loss leaves source distribution and reflection causality incomplete.[E9][E10][E11]

### `stealth_mechanisms`

1. `NM-ST`, role `primary`, confidence `high`. Summary: **来源分布把完整洪泛拆成局部低贡献流量 / Source distribution decomposes the full flood into locally low-contribution traffic**

> 攻击者让大量来源共同指向一个网络容量对象，每个来源只产生完整攻击的一小部分。源侧和按源阈值看到的是分散弱信号，目的前缀或入口链路聚合后才跨越容量；跨来源关联不足会使防守无法重建完整洪泛，形成时空释痕。目的聚合、top-k 占比、源/ASN 多样性和接口丢弃仍可揭示操作。[E2][E4][E5]
>
> The adversary directs many sources at one network-capacity object while each source generates only a small fraction of the complete attack. Source-side and per-source thresholds see dispersed weak signals, and capacity is crossed only after aggregation at the destination prefix or ingress link. Inadequate cross-source correlation prevents reconstruction of the full flood, producing Spatiotemporal Trace Dilution. Destination aggregation, top-k share, source and ASN diversity, and interface discards still expose the operation.[E2][E4][E5]

2. `NM-FD`, role `secondary`, confidence `high`. Summary: **第三方响应者地址取代真实请求发起者成为可见来源 / Third-party responder addresses replace the true request initiator as visible sources**

> 攻击者把受害者地址写入发往第三方服务的请求，响应者随后以自身合法地址把回包送到受害者。受害侧流量特征显示正常协议服务器，真实发起者不在返回路径，按可见源封禁既可能误伤也只到达反射器，形成来源特征伪装。缺少对应出站请求、响应/请求字节不对称、反射器集合和源地址验证证据可揭示置换。[E3][E6][E7][E8]
>
> The adversary places the victim address in requests to third-party services, which then send responses from their own legitimate addresses to the victim. Victim-side traffic features show ordinary protocol servers while the true initiator is absent from the return path. Blocking visible sources can cause collateral damage and reaches only reflectors, producing source Feature Disguise. Missing corresponding outbound requests, response-to-request byte asymmetry, reflector sets, and source-address-validation evidence expose the displacement.[E3][E6][E7][E8]

### `subtechnique_taxonomy`

> 子技术按攻击者如何改变来源观察划分。多源低贡献洪泛改变真实/即时发送源的分布，使单源贡献低而目的聚合跨越容量；响应源归因置换改变流量因果，让第三方响应者成为受害侧可见源、真实请求发起者位于另一条路径。前者不要求伪造或反射，后者不要求大量反射器，二者可同时映射但互不蕴含。
>
> Children are divided by how the adversary changes source observation. Multi-Source Low-Contribution Flooding changes distribution of true or immediate sending sources so each contribution is low while destination aggregation crosses capacity. Response-Origin Attribution Displacement changes traffic causality so third-party responders become victim-visible sources and the true request initiator lies on another path. The first does not require spoofing or reflection, while the second does not require many reflectors; both can map to one operation without implying each other.

> ATT&CK 的 Direct Network Flood 与 Reflection Amplification 只用于覆盖审查且不导入。直接流量的一源/少源实现留在父级；反射中的放大倍数、协议和服务类型留在父级。Botnet/C2、平台、工具、数据包大小、端口和攻击动机不形成 NJS。
>
> ATT&CK Direct Network Flood and Reflection Amplification are used only for coverage review and are not imported. Single-source or few-source direct traffic remains at the parent, while amplification ratio, protocol, and service type in reflection remain parent-level. Botnet or C2, platform, tool, packet size, port, and motive do not form NJS.

### `research.limitations`

> 标准和研究直接支持分布式来源、每源低占比、伪造源、反射响应及聚合检测需要，但公开资料通常不能从受害侧流量单独证明操作者身份、Botnet 控制或每个反射器配置。IP 地址可能经 NAT、Anycast、采样或伪造改变，Flash Crowd 与合法热点也可能形成相似来源熵。正式结论必须把流量拓扑与容量/丢弃及外部可用性连接，子项二还需请求—响应不对称或上游证据。[E4][E5][E6][E9][E11]
>
> Standards and research directly support distributed sources, low per-source share, source spoofing, reflected responses, and the need for aggregate detection, but public material usually cannot prove operator identity, botnet control, or each reflector's configuration from victim-side traffic alone. NAT, Anycast, sampling, and spoofing can change IP observations, while flash crowds and legitimate hot spots can produce similar source entropy. Formal conclusions must join traffic topology to capacity or discards and external availability, and child two additionally needs request-response asymmetry or upstream evidence.[E4][E5][E6][E9][E11]

## Proposed child 1 (`TA0040-T1498-CHILD-MULTI-SOURCE-LOW-CONTRIBUTION`)

Name: **多源低贡献洪泛 / Multi-Source Low-Contribution Flooding**  
Summary:

> 攻击者让大量来源各自贡献较小流量，只有在目标链路或前缀聚合后才形成容量拒绝服务。
>
> Adversaries make many sources contribute small amounts of traffic so capacity denial emerges only after aggregation at the target link or prefix.

### Definition and concept

> 多源低贡献洪泛以来源分布为稳定变量：攻击者协调大量即时发送源同时指向同一网络容量对象，使每个来源的 bps、pps 或连接贡献接近本地常态，而总和超过目标链路或边界承载能力。直接目的仍是阻断合法网络访问；节点是否属于特定 Botnet、使用何种协议及单包大小只是实现。[E2][E4][E5]
>
> Multi-Source Low-Contribution Flooding uses source distribution as its stable variable: the adversary coordinates many immediate senders toward one network-capacity object so each source's bps, pps, or connection contribution approaches a local norm while the sum exceeds the target link or boundary capacity. The direct purpose remains denial of legitimate network access. Membership in a named botnet, protocol choice, and packet size are implementations.[E2][E4][E5]

### Stealth characteristics

> 多源低贡献洪泛让完整攻击只在靠近目的端的聚合视角成立。源侧网络、单一来源告警和 top-talker 列表可能看不到强异常，且真实来源可来自普通消费网络，与合法客户共享地址和协议。目的前缀总量、源/ASN 多样性、top-k 份额下降、接口丢弃及外部探针失败仍保留可观察差分。[E4][E5]
>
> Multi-Source Low-Contribution Flooding becomes complete only in an aggregate view near the destination. Source-side networks, one-source alerts, and top-talker lists may show no strong anomaly, while real senders can come from ordinary consumer networks and share addresses and protocols with legitimate clients. Destination-prefix totals, source and ASN diversity, reduced top-k share, interface discards, and external-probe failures remain observable differentials.[E4][E5]

### Scope boundary

> 纳入要求多个独立即时来源、低单源贡献、共同目标、聚合容量跨越及合法可达性损失同时成立。单源高速洪泛、只有许多伪造地址而无独立来源证据、合法 Flash Crowd、内容分发热点和获批压力测试不属于本项。Botnet 感染或 C2 指令是相邻证据，不能替代实际洪泛与网络容量结果。
>
> Inclusion requires multiple independent immediate sources, low per-source contribution, a common target, aggregate capacity crossing, and loss of legitimate reachability. A high-rate single-source flood, many spoofed addresses without evidence of independent senders, a legitimate flash crowd, content-distribution hot spot, or approved stress test is outside this child. Botnet infection or C2 instruction is adjacent evidence and cannot replace the actual flood and network-capacity result.

### Application scenario

> 攻击者使用租用或自有的分布式设备群，在多个接入网络同步向目标前缀发送流量；每台设备只需产生有限速率，目标边界却承受总和。该设计适用于攻击者希望降低单源速率异常、提高按源封禁成本并利用合法客户端来源背景的容量攻击。[E2][E4]
>
> An adversary uses a rented or self-controlled distributed device population across many access networks to send traffic concurrently at a target prefix. Each device needs only a limited rate while the target boundary receives the sum. The design fits capacity attacks seeking to weaken per-source rate anomalies, raise the cost of source blocking, and exploit the background of legitimate client networks.[E2][E4]

### Threat model

Attacker:

> 攻击者需要足够多可同时发包的节点、目标地址/前缀和粗略容量信息，以及下发目标、开始/停止和速率的协调能力。节点地理、ASN 和接入多样性提高过滤难度；清洗容量、Anycast、源侧限速、节点下线和 C2 中断提高成本。
>
> The adversary needs enough concurrent senders, the target address or prefix and a rough capacity estimate, plus coordination of target, start and stop, and rate. Diversity of geography, ASN, and access network raises filtering difficulty. Scrubbing capacity, Anycast, source-side rate limiting, node takedown, and C2 disruption raise cost.

Defender:

> 防守方需要按目的前缀和入口聚合 flow，而不是只按 source 排序，并把源贡献分布、接口容量/丢弃及外部探针关联。NAT、Anycast、采样和合法高热事件会改变来源统计；若只在目标链路饱和后采集，流量出口器本身也可能丢失证据。
>
> Defenders need flow aggregation by destination prefix and ingress rather than only source ranking, joined to source-contribution distribution, interface capacity or discards, and external probes. NAT, Anycast, sampling, and legitimate high-interest events alter source statistics. If collection begins only after target-link saturation, the flow exporter itself can also lose evidence.

### Mechanism

`NM-ST`, primary, high confidence. Summary: **局部低贡献在目的聚合前隐藏完整容量攻击 / Locally low contributions conceal the full capacity attack until destination aggregation**.

> 攻击者把总流量预算分配给大量来源，使任何单一来源只留下较低 bps/pps 或连接贡献；源侧和单源阈值难以区分这些片段，完整攻击直到目的前缀或入口聚合才跨越容量，形成时空释痕。按受保护目标连接源分布、top-k 占比、总量、接口丢弃和外部失败可以恢复因果。[E2][E4][E5]
>
> The adversary allocates the total traffic budget across many sources so any one source leaves only low bps, pps, or connection contribution. Source-side and one-source thresholds have difficulty distinguishing the fragments, and the operation crosses capacity only after aggregation at the destination prefix or ingress, producing Spatiotemporal Trace Dilution. Joining source distribution and top-k share to protected target, aggregate volume, interface discards, and external failure recovers causality.[E2][E4][E5]

### Defense, evidence, and limits

Detection coverage is `available` through the parent Strategy and `TA0040-T1498-NJA-MULTI-SOURCE-AGGREGATE-SATURATION`; mitigation coverage is `available` through the shared Mitigation and its child-one application. Temporary claims: `TA0040-T1498-CLM-MULTI-SOURCE-CHILD` and `TA0040-T1498-CLM-MULTI-SOURCE-DETECTION`. Case refs `[]`.

> 公开标准和研究证明多源聚合、源侧低占比及目的/中转关联价值，但不能从 IP 数量单独证明每个地址是独立设备或同一攻击者控制。伪造、NAT、Anycast、采样和 Flash Crowd 会改变来源分布；若无法同时证明网络容量跨越及合法可达性损失，本项只能保持 hypothesis。
>
> Public standards and research establish multi-source aggregation, low source-side share, and the value of destination or transit correlation, but IP count alone cannot prove that every address is an independent device or under one adversary. Spoofing, NAT, Anycast, sampling, and flash crowds change source distribution. Without simultaneous proof of network-capacity crossing and loss of legitimate reachability, this child remains a hypothesis.

## Proposed child 2 (`TA0040-T1498-CHILD-RESPONSE-ORIGIN-DISPLACEMENT`)

Name: **响应源归因置换 / Response-Origin Attribution Displacement**  
Summary:

> 攻击者伪造受害者源地址触发第三方响应，使合法响应者成为受害侧可见来源并遮蔽真实请求发起者。
>
> Adversaries spoof the victim source address to trigger third-party responses, making legitimate responders the victim-visible sources and obscuring the true request initiator.

### Definition and concept

> 响应源归因置换以请求发起者与受害侧包来源分离为稳定变量。攻击者向第三方服务发送携带受害地址的请求，服务按协议把响应发给受害者；受害网络观察到的 source 是响应者，发起伪造请求的系统位于另一条路径。响应大于请求可提高破坏效率，但放大比、DNS/NTP 等协议名称和反射器数量不定义本项。[E3][E6][E8]
>
> Response-Origin Attribution Displacement uses separation of request initiator from victim-side packet source as its stable variable. The adversary sends third-party services requests carrying the victim address, and the services respond to the victim according to protocol. The victim network observes responders as sources while the system initiating spoofed requests lies on another path. Responses larger than requests can improve destructive efficiency, but amplification ratio, protocol names such as DNS or NTP, and reflector count do not define the child.[E3][E6][E8]

### Stealth characteristics

> 响应源归因置换使攻击流量携带真实且常见的服务器地址和正常响应格式，防守按可见源调查会到达未必失陷的开放服务；真实攻击源不接收返回流量，也不出现在受害侧会话前史。没有对应出站请求、响应方向标志、字节不对称、重复响应服务和上游伪造流量仍可揭示因果断点。[E6][E7][E8]
>
> Response-Origin Attribution Displacement gives attack traffic real, common server addresses and ordinary response formats. Investigation by visible source reaches open services that need not be compromised, while the true attack source receives no return traffic and does not appear in victim-side session history. Absence of corresponding outbound requests, response-direction indicators, byte asymmetry, repeated responder services, and upstream spoofed traffic still expose the causal break.[E6][E7][E8]

### Scope boundary

> 纳入要求第三方确因带受害者伪造源地址的请求而生成回包，回包汇聚导致网络容量影响，并能证明受害侧没有相应请求或有上游/反射器证据。直接伪造源洪泛、代理转发、合法异步通知、DNS resolver 正常响应、Anycast 迁移及只有“常见 UDP 源端口”不属于本项。反射器不能仅凭参与回包被标记为 Botnet 或攻击者资产。
>
> Inclusion requires a third party to generate replies because of a request carrying the spoofed victim source, convergence of replies causing network-capacity impact, and evidence that the victim made no corresponding request or that upstream or reflector evidence establishes the chain. Direct spoofed-source flooding, proxy forwarding, legitimate asynchronous notification, ordinary DNS resolver responses, Anycast movement, and a common UDP source port alone are outside this child. A reflector cannot be labeled a bot or adversary asset merely because it sent a response.

### Application scenario

> 攻击者从缺少出站源地址验证的网络向开放递归 DNS、NTP 或其他可产生响应的 UDP 服务发送小请求，并把目标地址放在 source 字段。响应者随后向目标返回更大或重复的数据，使真实攻击者只承担请求流量，受害侧面对来自许多正常服务器的回包。[E6][E7][E8]
>
> From a network lacking egress source-address validation, an adversary sends small requests to open recursive DNS, NTP, or other responsive UDP services with the target address in the source field. Responders then return larger or repeated data to the target, leaving the true attacker responsible only for request traffic while the victim faces replies from many ordinary servers.[E6][E7][E8]

### Threat model

Attacker:

> 攻击者需要能够发送带任意源地址的报文、可达第三方响应服务并选择能向受害者回包的请求。放大服务和多反射器提高容量，但源地址验证、关闭开放递归/服务、响应限速和提供方反欺骗会破坏路径。
>
> The adversary needs the ability to send packets with an arbitrary source address, reachable third-party response services, and requests that cause replies to the victim. Amplifying services and many reflectors increase capacity, while source-address validation, closure of open recursion or services, response-rate limiting, and provider anti-spoofing break the path.

Defender:

> 防守方需要同时观察受保护网络的出站请求与入站响应，保留 flow direction、五元组、字节/包计数和足够的协议元数据，并与上游网络和反射器 owner 协作。非对称路由、采样、NAT、外部 resolver 和缺少事务字段会让“无请求响应”判断降为推断。
>
> Defenders need both outbound-request and inbound-response views for the protected network, retaining flow direction, five-tuple, byte and packet counts, and sufficient protocol metadata, plus cooperation from upstream networks and reflector owners. Asymmetric routing, sampling, NAT, external resolvers, and absent transaction fields reduce an unsolicited-response conclusion to inference.

### Mechanism

`NM-FD`, primary, high confidence. Summary: **合法响应者来源特征遮蔽真实请求发起者 / Legitimate responder source features conceal the true request initiator**.

> 攻击者以受害者地址向第三方服务发起请求，第三方按正常协议从自身地址回包；痕迹因而把合法响应者呈现为攻击流量来源，防守沿 visible source 追查或封禁只到达反射器且可能伤及正常服务，真实发起者不在返回路径，形成特征伪装。请求—响应不对称、上游源验证与反射器侧请求日志可以恢复置换。[E3][E6][E7][E8]
>
> The adversary sends third-party services requests using the victim address, and those services reply normally from their own addresses. The trace therefore presents legitimate responders as attack-traffic sources. Investigation or blocking along the visible source reaches only reflectors and can harm legitimate service, while the true initiator is absent from the return path, producing Feature Disguise. Request-response asymmetry, upstream source validation, and reflector-side request logs recover the displacement.[E3][E6][E7][E8]

### Defense, evidence, and limits

Detection coverage is `available` through the parent Strategy and `TA0040-T1498-NJA-UNSOLICITED-REFLECTED-RESPONSE-CORRELATION`; mitigation coverage is `available` through the shared Mitigation and its child-two application. Temporary claims: `TA0040-T1498-CLM-RESPONSE-ORIGIN-CHILD` and `TA0040-T1498-CLM-REFLECTION-DETECTION`. Case refs `[]`.

> 受害侧单向流量通常只能证明大量第三方响应到达，不能独立证明初始请求由哪台设备发出、源地址在哪里伪造或反射器是否开放配置错误。非对称路由、外部 resolver、事务字段缺失和上游清洗会产生相似的“无请求响应”；没有上游、反射器或协议事务证据时，应降低归因置信度而不把响应者标记为攻击者。
>
> Victim-side one-way traffic usually proves only that many third-party responses arrived; it cannot independently prove which device sent the initial requests, where the source was spoofed, or whether a reflector was openly misconfigured. Asymmetric routing, external resolvers, missing transaction fields, and upstream scrubbing can create similar unmatched responses. Without upstream, reflector, or protocol-transaction evidence, attribution confidence must be lowered and responders must not be labeled adversaries.

## Evidence and shared-library candidates

Suggested parent Claims: `TA0040-T1498-CLM-ADAPT`, `TA0040-T1498-CLM-BOUNDARY`, `TA0040-T1498-CLM-SOURCE-TOPOLOGY`, and `TA0040-T1498-CLM-DEFENSE`. Child Claims are named above. Suggested Cases: **none**; standards and measurement research support the causal taxonomy, while this research did not obtain a sufficiently scoped incident source tying actor, time, target, exact network-capacity result, and source topology.

### Evidence ledger

| Key | Primary source and locator | Supported conclusion and limit |
| --- | --- | --- |
| E1 | MITRE ATT&CK 19.1 [T1498](https://attack.mitre.org/versions/v19/techniques/T1498/), description and boundary | Network bandwidth/path capacity, source spoofing and botnet context, T1499 boundary; not sufficient alone for Niji children. |
| E2 | MITRE ATT&CK 19.1 [T1498.001](https://attack.mitre.org/versions/v19/techniques/T1498/001/), botnet distribution discussion | Direct-flood coverage and per-node low contribution; planning reference, not imported taxonomy. |
| E3 | MITRE ATT&CK 19.1 [T1498.002](https://attack.mitre.org/versions/v19/techniques/T1498/002/), reflection causal chain | Reflector behavior and amplification coverage; planning reference, not imported taxonomy. |
| E4 | [NIST SP 800-189](https://doi.org/10.6028/NIST.SP.800-189), Section 3 | Many distributed sources, normal source IPs in Mirai, spoofing and reflection; supports source-topology contrast. |
| E5 | NIST research, [Monitoring the Macroscopic Effect of DDoS Flooding Attacks](https://www.nist.gov/system/files/documents/itl/antd/Monitoring-the-Macroscopic-Effect-of-DDoS-Flooding-Attacks.pdf), introduction/related work | Attack fraction can be small near each source; destination/transit aggregation and correlation are needed; legitimate/attack distinction remains hard. |
| E6 | IETF [RFC 4732](https://www.rfc-editor.org/rfc/rfc4732.html), Sections 1, 3.1 and 4 | Distributed DoS, DNS reflection with spoofed victim source, flash-crowd ambiguity, monitoring/baselines. |
| E7 | IETF [RFC 2827 / BCP 38](https://www.rfc-editor.org/rfc/rfc2827.html), abstract and filtering method | Source-address spoofing and ingress/egress validation mitigation; global deployment limits remain. |
| E8 | IETF [RFC 5358](https://www.rfc-editor.org/rfc/rfc5358.html), recursive nameserver reflector guidance | DNS reflector/amplifier causal path and resolver access-control mitigation; DNS-specific, not a universal protocol schema. |
| E9 | Existing `REF-000664`, [IANA IPFIX Information Elements](https://www.iana.org/assignments/ipfix), plus [RFC 7013](https://www.rfc-editor.org/rfc/rfc7013.html) Figure 1 | Exact reuse for flow fields and primary template definitions. |
| E10 | IETF [RFC 2863](https://www.rfc-editor.org/rfc/rfc2863.html), IF-MIB high-capacity/interface groups | `ifHCInOctets`, packet counters, discards, errors, `ifHighSpeed`, names and counter discontinuity. |
| E11 | IETF [RFC 9244](https://www.rfc-editor.org/rfc/rfc9244.html), introduction and telemetry model | Network-layer DDoS categories, botnets/reflectors, and domain-specific telemetry/baseline requirement. |
| E12 | CERT-EU, [DDoS Overview and Response Guide](https://cert.europa.eu/publications/security-guidance/CERT-EU_Security_Whitepaper_DDoS_17-003/), identification/containment | Volumetric categories, upstream mitigation, scrubbing/CDN and response planning; high-level guidance, not a fixed threshold source. |
| E13 | MITRE ATT&CK 19.1 [T1499 Endpoint Denial of Service](https://attack.mitre.org/versions/v19/techniques/T1499/), parent definition | Endpoint/application resource boundary without network saturation. |
| E14 | MITRE ATT&CK 19.1 [T1496 Resource Hijacking](https://attack.mitre.org/versions/v19/techniques/T1496/), parent definition | Attacker-task resource consumption boundary. |
| L1 | Existing `NJT-0189 Resource Hijacking` | Formal local owner for attacker-task resource consumption, including bandwidth; boundary object, not T1498 evidence. |

## Exact shared-library lookup and resolution advice

Required `library_lookup.py` searches were run for `network denial of service`, `DDoS`, `reflection amplification`, `source address validation`, `BCP 38`, `IPFIX flow`, `upstream traffic filtering`, `NIST SP 800 189`, `RFC 4732`, `RFC 2827`, `RFC 5358`, `RFC 2863`, `RFC 9244`, and `DDoS Overview Response Guide`.

- **Reuse `REF-000664`** exactly for the IANA IPFIX registry and field identities.[E9]
- No exact canonical match was returned for T1498 fixed pages, NIST SP 800-189, the NIST macroscopic DDoS paper, RFC 4732, RFC 2827, RFC 5358, RFC 2863, RFC 9244, or CERT-EU DDoS guidance. Recommend `create` after URL-level lookup against the refreshed catalog.
- Existing `CASE-000155`/`REF-000433` concern XorDdos rootkit hiding of processes and ports. They may describe malware later capable of DDoS, but their semantic identity is host artifact hiding, not a target-facing flood or source topology. Do not reuse for T1498.
- `MIT-000131 Network-Path Authority Enforcement` protects path-authority manipulation and interception; it does not provide source validation, reflector hardening, upstream absorption, or DDoS response. Do not extend by title similarity.
- No DET/NJA/MIT matched destination-capacity/source-topology correlation or the proposed network-capacity controls. Recommend `create` one Strategy, two Analytics, and one Mitigation; no Case; create Claims. Existing REF reuse is limited to `REF-000664`.

## Defense design

### Detection Strategy `TA0040-T1498-DET-DESTINATION-CAPACITY-SOURCE-TOPOLOGY`

Name: **目的容量—来源拓扑—可达性关联 / Destination Capacity–Source Topology–Reachability Correlation**. The Strategy establishes actual network-capacity impact first, then uses two Analytics to distinguish multi-source contribution dilution from reflected-response origin displacement. Domain `enterprise`; platforms are network-flow and edge infrastructure rather than endpoint OS labels.

### Shared data requirements

1. `ipfix-flow`, channel IPFIX/NetFlow: `flowStartMilliseconds`, `flowEndMilliseconds`, `sourceIPv4Address`/`sourceIPv6Address`, `destinationIPv4Address`/`destinationIPv6Address`, `sourceTransportPort`, `destinationTransportPort`, `protocolIdentifier`, `packetDeltaCount`, `octetDeltaCount`, `tcpControlBits`, `ingressInterface`, `egressInterface`, `flowDirection`, `bgpSourceAsNumber`, `samplingInterval`, `observationDomainId`. Reuse `REF-000664`; validate exporter support and sampling.[E9]
2. `interface-capacity`, channel SNMP IF-MIB/streaming telemetry: `timestamp`, `device_id`, `ifIndex`, `ifName`, `ifHighSpeed`, `ifHCInOctets`, `ifHCOutOctets`, `ifHCInUcastPkts`, `ifHCInMulticastPkts`, `ifHCInBroadcastPkts`, `ifInDiscards`, `ifInErrors`, `ifCounterDiscontinuityTime`.[E10]
3. `protected-prefix-capacity`, channel CMDB/network intent: `prefix_or_vip`, `service_id`, `ingress_set`, `provider`, `contracted_capacity_bps`, `normal_peak_bps`, `normal_peak_pps`, `criticality`, `owner`, `anycast_site`, `approved_test_id`, `event_calendar`.
4. `external-reachability`, channel independent probes: `timestamp`, `vantage_id`, `target_ip_or_name`, `resolved_ip`, `success`, `connect_latency_ms`, `packet_loss_pct`, `http_or_protocol_status`, `route_or_as_path`.
5. `endpoint-resource-boundary`, channel endpoint/load balancer/application metrics: `timestamp`, `service_id`, `cpu_pct`, `memory_pct`, `connection_table_pct`, `application_queue_depth`, `healthy_instance_count`, `request_success_rate`. These fields distinguish network saturation from T1499.
6. `packet-or-protocol-sample`, optional channel packet/NSM: `timestamp`, `sensor_id`, `source_ip`, `destination_ip`, `source_port`, `destination_port`, `protocol`, `packet_length`, `direction`, `response_indicator`, `transaction_id`, `query_or_request_type`. Do not require DNS fields for non-DNS protocols.
7. `upstream-mitigation`, channel ISP/CDN/scrubbing/DOTS: `timestamp`, `protected_prefix`, `provider_event_id`, `attack_vector`, `observed_bps`, `observed_pps`, `source_count`, `mitigation_action`, `route_action`, `start_time`, `end_time`, `dropped_bytes`, `passed_bytes`.

### Analytic 1 `TA0040-T1498-NJA-MULTI-SOURCE-AGGREGATE-SATURATION`

Logic:

1. Build rolling **10-second, 60-second, and 5-minute** aggregates by destination prefix/VIP, ingress interface, protocol, and service. Compute bps/pps, link-capacity fraction, interface discards/errors, external reachability, unique source IPs/ASNs, source entropy, and top-1/top-10 share. Windows are starting points validated against local exporter cadence and link buffering.
2. Establish parent impact only when aggregate traffic exceeds the service/link adaptive baseline or available capacity **and** interface discards/queue symptoms or independent reachability degradation confirms legitimate-user impact. A high flow count without capacity/result remains anomaly.
3. Establish child 1 when the aggregate result coincides with source diversity materially above the same service/event baseline and no small source set explains most traffic. Use top-k share and per-source contribution distribution rather than a universal source-count threshold. Source IP count alone is insufficient where spoofing, NAT, or sampling dominates.
4. Compare endpoint resource metrics. If access-link utilization and discards remain normal while CPU, connection tables, or application queues saturate, route the conclusion to T1499. If endpoint health remains normal but external probes fail as ingress fills, confidence in T1498 rises.
5. Aggregate correlated events across Anycast sites and upstream providers for **15 minutes** using protected prefix, service ID, source ASN distribution, and provider attack ID; keep per-site views so traffic engineering changes do not masquerade as source dispersion.

Observables: a destination prefix crosses capacity with increased discards and external failures while thousands of source networks have low individual shares; top talkers change rapidly while aggregate pps remains stable; multiple ingress sites see portions of one source distribution.

False positives: flash crowds; product launches/elections/news events; software/game distribution; backup/replication; traffic-engineering or Anycast shift; approved load test; broken routing causing retries; flow-exporter duplicate records.

Blind spots: unsampled/missing flows; source spoofing inflating diversity; carrier-grade NAT collapsing users; Anycast routing changes; exporter loss during saturation; upstream scrubbing hiding original topology; link capacity or counters stale; legitimate and malicious traffic inseparable.

Tuning: baseline by protected prefix, service, interface, time, event calendar, Anycast site, and provider; bind load-test exclusions to source ranges, target, time, expected bps/pps, and test ID; model top-k share/entropy distributions per service; never globally allow consumer ASNs or all CDN traffic; retain low-confidence saturation even when attribution is unresolved.

### Analytic 2 `TA0040-T1498-NJA-UNSOLICITED-REFLECTED-RESPONSE-CORRELATION`

Logic:

1. From packet metadata where available, classify inbound response-bearing packets and seek a reversed outbound request with matching protocol/addresses/ports and transaction ID in the preceding **30 seconds**. With flow-only data, use bidirectional five-tuple reversal over **60 seconds** and mark the result inferred rather than exact.
2. Aggregate unmatched inbound response bytes/packets by protected destination and responder service over **10 seconds, 60 seconds, and 5 minutes**. Compute inbound-response to outbound-request octet ratio, distinct responder IP/ASN counts, repeated source-service patterns, link-capacity fraction, interface discards, and external probe outcome.
3. Establish child 2 when unmatched responses from third-party responders converge with actual capacity/reachability impact, and upstream/reflector or packet evidence supports spoofed-victim requests. A common UDP source port or large ratio alone remains hypothesis.
4. Correlate provider mitigation records and any source-address-validation evidence. Do not mark reflectors compromised; record immediate responder, suspected protocol role, and attribution status separately from initiating source.
5. Keep a **15-minute** pre/post window for routing, resolver, or Anycast changes that can explain missing outbound requests. If egress is observed elsewhere due asymmetric routing, downgrade rather than suppress.

Observables: large inbound response volume from many third-party servers with no corresponding victim requests; packet responses carrying DNS/NTP or equivalent response semantics toward one protected prefix; provider identifies reflection vector while ingress fills and probes fail.

False positives: legitimate recursive-resolver traffic observed at only one direction; asynchronous UDP notifications; anycast/path change; telemetry sampling; state expiration shorter than application latency; monitoring/measurement services; delayed/retransmitted responses.

Blind spots: asymmetric routing; no egress view; encrypted or proprietary response semantics; sampling drops small outbound requests; NAT obscures requester; upstream scrubbing removes original packet features; spoofed direct flood looks diverse without reflection; provider vector labels too coarse.

Tuning: inventory authorized resolvers and asynchronous UDP services; validate transaction matching per protocol; baseline unmatched-response ratios by protected role; bind exceptions to responder/service and expiry rather than port alone; preserve an `attribution_unresolved` state when only victim-side flow exists.

### Mitigation `TA0040-T1498-MIT-SOURCE-VALIDATED-UPSTREAM-ABSORPTION`

Name: **源地址验证、反射面约束与上游容量吸收 / Source Validation, Reflector-Surface Constraint, and Upstream Capacity Absorption**.

Measures:

1. `source-address-validation` (`preventive`): deploy BCP 38/84-style ingress and egress validation or appropriate uRPF/ACL policy so customer and workload networks cannot emit source addresses they do not legitimately use. Test asymmetric and multihomed routes before strict enforcement.[E7]
2. `reflector-service-hardening` (`exposure-reduction`): restrict recursive/response services to authorized clients, disable unneeded UDP services, patch known amplifiers, and apply protocol-aware response rate limiting. Preserve authoritative DNS availability and validate each service rather than blocking UDP broadly.[E8]
3. `upstream-capacity-and-scrubbing` (`containment`): prearrange ISP/CDN/Anycast/scrubbing capacity, authenticated escalation, protected prefixes, telemetry exchange, and emergency route actions such as FlowSpec or RTBH with explicit owner approval and rollback. Filtering must occur before the saturated link.[E11][E12]
4. `prefix-capacity-observability` (`detective-support`): export multi-ingress IPFIX and IF-MIB counters to a separately provisioned collector, maintain external probes and capacity baselines, and exercise DDoS playbooks with provider event IDs and immutable timing.

Parent application:

> 对低可归因网络容量拒绝服务，在关键前缀和入口预置上游清洗、容量、Anycast/路由应急及多入口 flow/接口计数，触发条件同时使用容量、丢弃和外部可达性。攻击开始后在饱和链路上游执行经审批的过滤或引流，保留原始来源拓扑和提供方事件，避免本地防火墙成为新的瓶颈。
>
> For Low-Attribution Network Capacity Denial of Service, prearrange upstream scrubbing, capacity, Anycast or emergency routing, and multi-ingress flow and interface counters for critical prefixes, with triggers combining capacity, discards, and external reachability. During attack, apply approved filtering or diversion upstream of the saturated link while preserving original source topology and provider events, avoiding creation of a new bottleneck at the local firewall.

Child 1 application:

> 对多源低贡献洪泛，按目的前缀/服务在上游聚合并吸收流量，不依赖单源封禁或固定 top-talker 阈值；利用行为、会话完成度和容量信号区分合法来源，并在多个 Anycast/清洗点共享同一攻击 ID 与来源分布。
>
> For Multi-Source Low-Contribution Flooding, aggregate and absorb traffic upstream by destination prefix or service rather than relying on source blocking or a fixed top-talker threshold. Use behavior, session completion, and capacity signals to distinguish legitimate sources and share one attack ID and source distribution across Anycast or scrubbing sites.

Expected effect: per-source dilution no longer prevents detection because control is applied to the destination aggregate before the constrained link. Limits: scrubbing capacity can be exceeded, encrypted/legitimate-looking traffic remains difficult, provider diversion changes routes/latency, and broad rate limits harm flash crowds and real users.

Child 2 application:

> 对响应源归因置换，在自身和客户出口实施源地址验证，限制组织拥有的开放递归/响应服务，并与上游共享未配对响应、反射器列表和受保护前缀；受害侧过滤应按协议语义、请求状态和容量执行，而不是永久封禁所有响应者。
>
> For Response-Origin Attribution Displacement, enforce source-address validation at organizational and customer egress, restrict organization-owned open recursive or response services, and share unmatched responses, reflector sets, and protected prefixes with upstream providers. Victim-side filtering should use protocol semantics, request state, and capacity rather than permanently blocking every responder.

Expected effect: source validation prevents participating networks from originating spoofed requests, reflector hardening reduces available third parties, and upstream state-aware filtering removes unsolicited responses before the constrained link. Limits: the victim cannot compel global BCP 38 or reflector remediation, asymmetric routing weakens request state, responder blocking causes collateral damage, and RTBH restores network stability by making the target intentionally unreachable.

Resolution: `create`. Existing Niji mitigations do not combine anti-spoofing, reflector hardening, upstream absorption, and destination-capacity observability with per-target applications.

## Content-depth and integration checks

- Parent and both child drafts cover definition, trace change, residual observations, included/excluded behavior, scenarios, attacker prerequisites, defender visibility, mechanism, evidence, limits, and defense at NJT-0001 field responsibility depth.
- Child-one and child-two first stealth paragraphs begin with their exact names; formal YAML must preserve this.
- Do not write ATT&CK child IDs/names or coverage rows into formal Technique/Sub-technique YAML. The planning table above is the only provenance record.
- Parent and children can share the Strategy and Mitigation, but each child needs the Analytic/application that directly fits it. Strategy↔Analytic links remain bidirectional.
- Keep volume thresholds adaptive. The 10s/60s/5m and 30s/60s request windows are implementable starting values requiring local validation, not source-proven universal constants.
- Reuse only `REF-000664` from current lookup; create the remaining exact References after refreshed URL lookup. Do not manufacture Cases.
- Keep lifecycle `review` after schema, quality, bundle, duplicate, bilingual Web/API, and human-content gates. This handoff allocates no canonical IDs and changes no formal/shared/plan object.
