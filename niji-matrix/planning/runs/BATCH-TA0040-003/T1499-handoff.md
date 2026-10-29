# T1499 research handoff — BATCH-TA0040-003

Research staging only. All proposed new objects use temporary prefix `TA0040-T1499-`. No formal IDs are allocated, and no canonical matrix, decision, shared library, tactic plan, batch brief, reservation, or integration summary is modified.

## Admission recommendation

**Candidate:** ATT&CK Enterprise 19.1 T1499 Endpoint Denial of Service / 端点拒绝服务. **Recommendation:** `adapt`. **Parent confidence:** `high`. **Fixed ATT&CK children:** T1499.001 OS Exhaustion Flood, T1499.002 Service Exhaustion Flood, T1499.003 Application Exhaustion Flood, T1499.004 Application or System Exploitation. `original_attack_subtechniques_imported: false`.

**准入理由（中文）：** T1499 直接描述攻击者耗尽端点、操作系统、服务或应用内部资源，或触发软件缺陷造成持续崩溃，使合法用户无法取得预期功能，同时明确排除提供网络被饱和的 T1498。该可用性结果属于 Impact，且系统连接池、工作线程、事件循环、内存、CPU、句柄和崩溃状态提供可验证对象。Niji 应保留直接结果，但把正式匿迹问题改写为攻击者如何用低流量长期保持状态，或用少量输入放大内部工作，使端点失效前缺少传统高流量或高请求数特征。服务最终不可用本身通常显著；匿迹发生在原因和前兆，而不是中断结果不可见。

**Admission rationale (English):** T1499 directly covers adversary exhaustion of internal endpoint, operating-system, service, or application resources, or triggering of a software flaw for a persistent crash so legitimate users lose expected function, while explicitly excluding saturation of the providing network under T1498. The availability result belongs to Impact and exposes verifiable objects in connection pools, workers, event loops, memory, CPU, handles, and crash state. Niji should retain that result while adapting the formal stealth question to low-traffic state holding or small-input internal-work amplification that removes traditional high-volume or high-request-count precursors before endpoint failure. The unavailable service is usually conspicuous; stealth concerns cause and precursor rather than invisibility of the outage.

## Mandatory adjacent boundaries

- **NJT-0185 Business Service Stop / 业务服务停用:** NJT-0185 requires an accepted management stop/disable path and an orderly administrative terminal state. T1499 covers involuntary resource saturation, hang, crash, panic, OOM termination, watchdog restart, or exploit-induced unavailability. The same service being unavailable does not merge the causes. A `stopped` state with authorized control lineage belongs to NJT-0185; abnormal depletion or failure without a stop control belongs here.
- **T1498 Network Denial of Service:** T1498 impairs the network link, protocol path, or boundary capacity used to reach services. T1499 leaves the providing network unsaturated and exhausts or crashes the endpoint stack behind it. A distributed HTTP campaign can generate both only when evidence separately establishes path/boundary saturation and endpoint-resource failure. Request source count or the word DDoS does not decide the boundary.
- **NJT-0189 Resource Hijacking / 资源劫持:** NJT-0189 consumes victim resources to complete attacker work such as mining, proxy resale, messaging, or model inference, with availability degradation secondary. T1499 makes endpoint unavailability the direct result. A miner that produces attacker revenue while reducing performance is NJT-0189; if it also drives a critical endpoint into proven outage, both may be recorded with different direct objects. Resource use without failed service is not T1499.
- **Exploit execution:** Vulnerability probing, malformed input, code execution, privilege gain, or a crash in a noncritical test process does not complete T1499 without a proven endpoint/OS/service/application availability result. T1499.004 is planning breadth only; Niji's proposed amplification child is defined by input-to-work asymmetry and availability, not by the word exploit.
- **T1529 System Shutdown/Reboot:** An explicit attacker-controlled transition to shutdown/reboot belongs to T1529. A kernel panic or watchdog restart caused by exhaustion/exploit first establishes T1499; record T1529 only if evidence supports an intended lifecycle transition rather than a recovery side effect.

## ATT&CK-child breadth review and coverage resolutions

ATT&CK's four children partition target stack layer and exploitation form. Those dimensions cannot be imported. Open-ended Niji research examined: low-rate state holding; input-to-work cost amplification; distributed source dilution; maintenance-like crash/restart appearance; source spoofing; and scheduled/legitimate-traffic alignment. Two variables pass current stability, trace, evidence, and defense gates.

| ATT&CK 19.1 child | Represented dimension | Planning-only resolution | Niji reasoning |
|---|---|---|---|
| T1499.001 OS Exhaustion Flood | Kernel/OS connection, process, memory, file, or scheduling resources | `parent-core`; contributes to both Niji candidates where evidenced | OS is a resource layer, not a stealth variable. Slow held sockets can exhaust OS state; crafted input can amplify kernel work, but only the trace variable defines a child. |
| T1499.002 Service Exhaustion Flood | Service daemon connection/worker/queue resources | `niji-variable-candidate` plus `parent-core` | Slow incomplete sessions directly support state-holding exhaustion. Ordinary high-rate service floods remain parent-core. |
| T1499.003 Application Exhaustion Flood | Application request/session/work resources | `niji-variable-candidate` plus `parent-core` | Both held-request state and asymmetric request cost can exhaust applications; application layer itself is not imported. |
| T1499.004 Application or System Exploitation | Vulnerability-triggered crash or exhaustion | `niji-variable-candidate` for asymmetric cost; otherwise `adjacent-technique`/`parent-core` | ReDoS and algorithmic complexity support small-input/high-work traces. Exploit execution without availability stays adjacent, and crash trigger type is not a child key. |

**Proposed Niji children:** `TA0040-T1499-CHILD-STATE` State-Holding Low-Rate Exhaustion / 状态保持式低速耗尽; `TA0040-T1499-CHILD-AMPLIFICATION` Input-to-Work Cost Amplification / 输入到工作量成本放大. The first controls *progress rate and holding duration* so many low-bandwidth sessions accumulate state. The second controls *input complexity relative to internal work* so a small number of requests consumes disproportionate CPU/memory or triggers a crash. A slow upload can be the first without expensive computation; a ReDoS request can be the second without holding many connections.

**Breadth-gap explanation:** four ATT&CK stack/behavior categories converge to two Niji trace variables because OS, service, application, and exploit are ownership or implementation layers. High-volume exhaustion remains parent core and has no independent stealth partition. Source distribution and crash appearance remain deferred. This satisfies the required examination of at least two materially distinct axes without creating resource-layer children.

## Proposed parent field content

**Name / 名称:** 端点拒绝服务 / Endpoint Denial of Service.

**Summary / 摘要:** 攻击者使端点、操作系统、服务或应用因内部资源耗尽或触发性故障而失去功能，并通过低速状态保持或输入成本放大削弱失效前兆。 / Adversaries make an endpoint, OS, service, or application unavailable through internal resource exhaustion or triggered failure while low-rate state holding or input-cost amplification weakens the precursor signal.

### Definition and concept / 定义与概念

中文：端点拒绝服务是攻击者使承载功能的主机、操作系统、服务进程或应用因连接/会话状态、线程、队列、句柄、CPU、内存、事件循环或缺陷触发而无法继续为合法用户提供预期功能。直接对象是端点内部可用性；网络仍可到达地址并不否定服务失败，进程仍存活也不否定挂起或无可用工作槽位。

English: Endpoint Denial of Service is adversary-caused loss of expected function when the hosting machine, OS, service process, or application can no longer serve legitimate users because connection or session state, workers, queues, handles, CPU, memory, event loop, or a triggered flaw is exhausted or blocked. The direct object is internal endpoint availability. A reachable network address does not negate service failure, and a surviving process does not negate a hang or absence of usable worker slots.

中文：概念锚连接攻击输入、端点内资源或故障状态、合法请求/健康结果以及恢复过程。包数、请求数、平台、进程名和漏洞编号只是实现。Niji 关注攻击者怎样降低“外部输入量—内部损失”之间的可见比例，而不是把所有明显洪泛重新命名为匿迹技术。

English: The concept joins adversary input, internal resource or fault state, legitimate request or health outcome, and recovery process. Packet count, request count, platform, process name, and vulnerability ID are implementations. Niji focuses on how the adversary lowers the visible ratio between external input and internal loss rather than relabeling every conspicuous flood as a stealth technique.

### Stealth characteristics / 匿迹特性

中文：常规高速洪泛会同步抬高流量、请求率和资源使用。状态保持式攻击以极低数据率让连接、请求头、请求体或会话长期未完成，局部带宽和单源速率较低但并发状态不断积累；输入成本放大则用少量、外形接近正常的内容触发指数回溯、昂贵解析或故障，使内部 CPU/事件循环/内存远高于输入量。二者都使只看请求量的防守方低估风险。

English: Conventional high-rate floods raise traffic, request rate, and resource use together. State-holding attacks send data very slowly so connections, headers, bodies, or sessions remain incomplete while local bandwidth and per-source rate stay low and concurrent state accumulates. Input-cost amplification uses a small amount of ordinary-looking content to trigger exponential backtracking, expensive parsing, or a fault, making internal CPU, event-loop, or memory cost far exceed input volume. Both cause request-count-only defenders to underestimate risk.

中文：残余痕迹包括活动连接与完成请求的比例、连接存续和字节进度、408/503/504、工作线程和句柄、队列深度、每请求时延与长度、路由、错误类型、进程 CPU/内存、OOM/崩溃/重启及外部健康探针。攻击结果本身显著，但如果入口层、端点资源和业务健康不按请求 ID/时间关联，防守方可能把故障归因于容量规划、代码缺陷或偶发客户端。

English: Residual traces include active-to-completed connection ratio, connection age and byte progress, 408/503/504 status, workers and handles, queue depth, per-request duration and length, route, error type, process CPU or memory, OOM/crash/restart, and external health probes. The result is conspicuous, but without request-ID/time joins across ingress, endpoint resource, and business health, defenders can attribute it to capacity planning, software defects, or accidental clients.

### Scope boundary definition / 范围边界界定

中文：纳入攻击者输入与端点内部耗尽/故障之间有可验证因果，且合法用户功能实际降级或不可用的行为。资源升高但健康正常、被限流且未影响服务、失败的漏洞探测和单个非关键进程崩溃是企图或相邻行为。正常流量峰值、慢移动网络、大文件上传、缓存冷启动、垃圾回收、配置错误和容量不足是强反例。

English: Include behavior with verified causality from adversary input to internal endpoint exhaustion or fault and actual degradation or unavailability for legitimate users. Raised resource use with healthy service, successfully rate-limited traffic without impact, failed exploit probing, and a noncritical process crash are attempts or adjacent behavior. Legitimate traffic peaks, slow mobile networks, large uploads, cold cache, garbage collection, misconfiguration, and inadequate capacity are strong counterexamples.

中文：有序控制停止归 NJT-0185；链路或网络边界容量饱和归 T1498；为攻击者任务消耗资源归 NJT-0189。漏洞利用可与本技术共同记录，但必须分别证明执行/权限结果和可用性结果。自动恢复、进程重启或故障转移不会否定短暂 T1499，但必须记录影响持续时间和用户范围。

English: Orderly controlled stop belongs to NJT-0185, link or boundary saturation to T1498, and resource use for adversary work to NJT-0189. Exploitation can co-occur, but execution or privilege result and availability result require separate proof. Automatic recovery, process restart, or failover does not negate a transient T1499 outcome, but impact duration and affected user scope must be recorded.

### Application scenarios / 应用场景

中文：面向 Web 的端点可被大量低进度 HTTP 连接占用，使工作进程/连接池等待未完成头部或请求体，而接入带宽仍未饱和。另一个场景是攻击者向存在低效正则或高复杂度解析路径的路由提交精心构造的短输入，使单个事件循环或少数工作线程长时间计算，其他客户端得不到调度。系统服务和内核解析器也可能出现相同的“低输入、高内部代价”关系。

English: A web endpoint can have its worker or connection pool occupied by many low-progress HTTP connections waiting for incomplete headers or bodies while ingress bandwidth remains unsaturated. In another scenario, an adversary sends crafted short input to a route with an inefficient regular expression or high-complexity parser, leaving one event loop or a few workers computing for long periods so other clients do not get scheduled. System services and kernel parsers can exhibit the same low-input, high-internal-cost relation.

### Attacker model / 攻击方模型

中文：状态保持攻击者需要建立并维持足够多的会话、按低于超时/最小速率门限的节奏发送进度，并容忍连接重置；可以用多个来源降低每源速率。成本放大攻击者需要识别高复杂度或故障输入路径并反复触发，输入量可以很小。代理/CDN 超时、连接与请求限额、无回溯算法、输入长度/复杂度界限、隔离工作池和快速故障转移会限制效果。

English: A state-holding adversary needs to establish and maintain enough sessions, send progress around timeout or minimum-rate boundaries, and tolerate resets, possibly distributing sources to lower per-source rate. A cost-amplification adversary needs to identify a high-complexity or faulting input path and retrigger it, potentially with little input volume. Proxy/CDN timeouts, connection and request limits, nonbacktracking algorithms, input length or complexity bounds, isolated worker pools, and rapid failover constrain the effect.

### Defender model / 防守方模型

中文：防守方可观察负载均衡器连接/请求/字节和拒绝计数、Web 接入日志、超时日志、端点连接与工作池状态、OpenTelemetry 路由/时延/错误、进程 CPU/内存、崩溃/重启及不同权健康探针。判断需要同时保留未完成连接和已完成请求；只写请求完成日志会漏掉仍在占槽的攻击。仅用源 IP 速率会漏掉分布式低速攻击，只有主机资源而无请求 lineage 则无法区分代码回归。

English: Defenders can observe load-balancer connection, request, byte, and rejection counts, web access and timeout logs, endpoint connection and worker-pool state, OpenTelemetry route/duration/error, process CPU or memory, crash/restart, and a differently authorized health probe. Assessment retains incomplete connections as well as completed requests; completion-only logs miss attacks still occupying slots. Source-IP rates miss distributed low-rate activity, while host resource without request lineage cannot separate a code regression.

### Supported parent mechanisms

`TA0040-T1499-MECH-STATE` — `NM-ST`, primary. **Summary zh:** 低进度连接跨时间累积并发状态. **Summary en:** Low-progress connections accumulate concurrent state over time. **Analysis zh:** 攻击者把本应快速完成的请求拆成低速片段并维持大量未完成状态，流量痕迹在时间和来源上被稀释，而连接/工作槽位持续占用；短窗流量阈值难以还原累计耗尽，形成时空释痕。连接年龄、字节进度和全局并发仍能恢复。 **Analysis en:** The adversary fragments requests into low-rate progress and maintains many incomplete states, diluting traffic across time and sources while connection or worker slots remain occupied. Short-window volume thresholds cannot reconstruct accumulated exhaustion, producing Spatiotemporal Trace Dilution. Connection age, byte progress, and global concurrency still recover the chain. **Evidence:** E2–E4. **Confidence:** `high` for HTTP state holding, `medium` across protocols.

`TA0040-T1499-MECH-AMPLIFICATION` — `NM-FD`, secondary. **Summary zh:** 小型请求外观掩盖不成比例的内部工作. **Summary en:** Small request appearance disguises disproportionate internal work. **Analysis zh:** 攻击者选择能触发回溯或高复杂度路径的短输入，外部请求数量和长度与正常请求相近，但应用内部工作呈指数或异常增长并阻塞共享执行资源；入口特征难以表明恶意代价，形成特征伪装。每请求工作/时延、输入结构和健康结果可揭示不对称。 **Analysis en:** The adversary selects short input that triggers backtracking or another high-complexity path. External request count and length resemble normal requests while application work grows exponentially or anomalously and blocks shared execution resources. Ingress features do not reveal the malicious cost, producing Feature Disguise. Per-request work or duration, input structure, and health outcome reveal the asymmetry. **Evidence:** E5–E7. **Confidence:** `high` for ReDoS, `medium` across arbitrary crash triggers.

### Parent taxonomy narrative / 父级分类叙述

中文：原生子项按“外部输入如何与内部损失脱钩”划分。状态保持式低速耗尽通过长连接/未完成事务积累并发状态，需连接进度和池容量防御；输入到工作量成本放大通过少量完成输入触发不成比例计算或故障，需路由/输入与内部工作/崩溃关联。前者通常单事务工作低而持有时间长，后者单事务内部代价高而输入量小。

English: Native children divide by how external input is decoupled from internal loss. State-Holding Low-Rate Exhaustion accumulates concurrency through long-lived connections or incomplete transactions and requires connection-progress and pool-capacity defense. Input-to-Work Cost Amplification uses a few completed inputs to trigger disproportionate computation or fault and requires route/input-to-work/crash correlation. The former generally has low work per transaction and long holding time; the latter has high internal cost per transaction and small input.

中文：T1499.001–.004 的 OS、服务、应用与利用分类全部保留为 planning-only 实现。分布式来源可增强两项，但来源拓扑本身与 T1498/C2/botnet交叉且证据不足；正常故障外观和合法流量对齐也保持 deferred。高流量洪泛留在父级，不为数量建立 NJS。

English: T1499.001–.004 OS, service, application, and exploitation partitions remain planning-only implementations. Distributed sources can strengthen both children, but source topology intersects T1498, C2, and botnets and lacks enough evidence as a separate axis. Ordinary-fault appearance and legitimate-traffic alignment also remain deferred. High-volume floods stay parent core and do not receive a child merely for count.

## Proposed child `TA0040-T1499-CHILD-STATE`

**Name / 名称:** 状态保持式低速耗尽 / State-Holding Low-Rate Exhaustion. **Confidence:** `high` for HTTP, `medium` cross-protocol.

### Definition and concept / 定义与概念

中文：状态保持式低速耗尽是攻击者建立大量连接、会话或事务，以极慢但持续的进度保持其未完成状态，使端点为每个状态保留套接字、缓冲区、工作线程、句柄或队列项，最终没有容量服务合法请求。稳定变量是每个攻击事务的持有时间与进度速率，而不是 HTTP、连接数或源数量本身。

English: State-Holding Low-Rate Exhaustion establishes many connections, sessions, or transactions and keeps them incomplete with extremely slow but continuing progress, causing the endpoint to retain sockets, buffers, workers, handles, or queue entries until no capacity remains for legitimate requests. The stable variable is holding duration and progress rate per adversary transaction, not HTTP, connection count, or source count itself.

### Stealth characteristics / 匿迹特性

中文：状态保持式低速耗尽使单源带宽、每秒完成请求和单连接字节数保持很低，看起来像慢客户端或不稳定网络；真正异常在全局未完成状态、长连接年龄和池占用累积。请求完成后才写日志的系统可能在最关键阶段缺少访问日志，只有连接计量、超时/最小速率日志和端点池状态显示原因。

English: State-Holding Low-Rate Exhaustion keeps per-source bandwidth, completed requests per second, and bytes per connection low, resembling slow clients or unstable networks. The anomaly is the aggregate incomplete state, connection age, and pool occupancy. Systems that log only after request completion can lack access records at the critical stage, leaving connection meters, timeout or minimum-rate logs, and endpoint pool state to expose the cause.

### Scope boundary definition / 范围边界界定

中文：纳入攻击者有意让事务长期不完成且内部状态持续保留，最终造成端点功能损失的行为。合法大文件上传、WebSocket、SSE、长轮询、慢移动连接、TLS 证书检查延迟和获批持久会话是反例。若高带宽本身饱和链路归 T1498；若连接都快速完成但处理成本高，归成本放大子项或父级洪泛。

English: Include deliberate noncompletion of transactions while internal state remains allocated and endpoint function is eventually lost. Legitimate large uploads, WebSockets, server-sent events, long polling, slow mobile connections, TLS certificate-check delay, and approved persistent sessions are counterexamples. Saturation of the link by bandwidth belongs to T1498. Rapidly completed connections with expensive processing belong to the cost-amplification child or parent flood behavior.

### Application scenarios and threat model / 应用场景与威胁模型

中文场景：攻击者并行建立 HTTP 连接，只间歇发送部分头部或请求体，使 Web 服务器继续等待。OWASP 说明慢速碎片请求可占满并发连接池而所需攻击资源很小；Apache `mod_reqtimeout` 为握手、头部和正文定义超时与最小数据率，说明可观测变量和控制点。

English scenario: The adversary opens HTTP connections in parallel and intermittently sends only partial headers or bodies so the web server continues waiting. OWASP describes slow fragmented requests filling the concurrent connection pool at low attacker cost, while Apache `mod_reqtimeout` defines handshake, header, and body timeouts and minimum data rates, establishing the observable variable and control point.

中文攻击方：攻击者需要维持足够多会话并根据服务超时调整发送节奏；分布式来源可避免每源连接限制。代理重置、最大连接寿命、请求读取超时、最小速率和独立池会提高成本。协议多路复用、NAT 和 CDN 可能改变“一连接一状态”的关系。

English attacker: The adversary needs to maintain enough sessions and tune progress against service timeouts, potentially distributing sources to avoid per-source caps. Proxy resets, maximum connection life, request-read timeout, minimum rate, and isolated pools raise cost. Protocol multiplexing, NAT, and CDN termination can change the one-connection-to-one-state relation.

中文防守方：防守方需要连接创建/关闭与年龄、接收字节进度、未完成请求阶段、活动与拒绝连接数、工作/文件描述符池、超时日志和外部健康。只保留完成请求或按源 IP 聚合会漏掉未完成及分布式状态；必须按目标 listener/虚拟主机和全局池关联。

English defender: The defender needs connection create/close and age, received-byte progress, incomplete request stage, active and rejected connection counts, worker or descriptor pool, timeout logs, and external health. Completion-only or per-source-IP aggregation misses incomplete and distributed state; correlation must operate by target listener or virtual host and global pool.

### Supported mechanism and limitations

Mechanism is `TA0040-T1499-MECH-STATE` / `NM-ST`. **Limitation zh:** OWASP 和 Apache 直接支持 HTTP 慢速状态保持及其控制，但不证明每个长连接恶意，也不提供所有服务器通用阈值。ALB 活动连接包括客户端到负载均衡器和负载均衡器到目标两段，需结合请求、字节与目标健康解释。 **Limitation en:** OWASP and Apache directly support slow HTTP state holding and its controls but do not make every long connection malicious or provide a universal server threshold. ALB ActiveConnectionCount covers both client-to-load-balancer and load-balancer-to-target legs and requires request, byte, and target-health context.

## Proposed child `TA0040-T1499-CHILD-AMPLIFICATION`

**Name / 名称:** 输入到工作量成本放大 / Input-to-Work Cost Amplification. **Confidence:** `high` for ReDoS, `medium` across parsers/exploit crashes.

### Definition and concept / 定义与概念

中文：输入到工作量成本放大是攻击者选择能触发算法最坏路径、递归/回溯、解压/解析扩张或故障的输入，使少量外部字节或请求在端点内部产生不成比例的 CPU、内存、线程占用或崩溃。稳定变量是输入成本与内部工作/损失之间的放大比，而不是漏洞编号、编程语言或应用层名称。

English: Input-to-Work Cost Amplification selects input that triggers an algorithmic worst case, recursion or backtracking, decompression or parsing expansion, or a fault so a small amount of external bytes or requests causes disproportionate endpoint CPU, memory, worker use, or crash. The stable variable is the amplification ratio between input cost and internal work or loss, not vulnerability ID, programming language, or application-layer label.

### Stealth characteristics / 匿迹特性

中文：输入到工作量成本放大使请求率和请求长度保持在常规范围，入口限流器或网络容量检测可能没有显著异常；端点却在单个路由/处理器内出现长时延、事件循环阻塞、CPU 峰值、内存扩张或崩溃。残余痕迹是相同输入形态、请求 ID、路由、每请求时延/工作、错误和健康下降之间的不对称。

English: Input-to-Work Cost Amplification keeps request rate and request length within ordinary ranges so ingress rate limits or network-capacity monitoring may show little anomaly, while one endpoint route or handler develops long latency, event-loop blocking, CPU spikes, memory expansion, or crash. Residual evidence is the asymmetry among repeated input shape, request ID, route, per-request duration or work, error, and degraded health.

### Scope boundary definition / 范围边界界定

中文：纳入攻击者可控输入触发不成比例内部工作/故障，并实际影响合法功能。ReDoS 是实例，不限定本项；昂贵查询、解析器、压缩、模板和内核处理均可能实现。正常复杂报表、合法大输入、缓存未命中、下游延迟和偶发代码缺陷是反例。只证明漏洞可利用或代码执行而无可用性结果不属于本项。

English: Include adversary-controlled input that triggers disproportionate internal work or fault and actually affects legitimate function. ReDoS is an instance rather than the boundary; expensive queries, parsers, compression, templates, and kernel processing can implement it. Legitimate complex reports, large approved input, cache misses, downstream latency, and accidental defects are counterexamples. Exploitability or code execution without an availability result does not qualify.

### Application scenarios and threat model / 应用场景与威胁模型

中文场景：Node.js 官方说明恶意客户端可提交使事件循环长时间运行的输入，阻止其他客户端获得执行；嵌套量词等脆弱正则可能随输入长度呈指数回溯。OWASP 和 CWE-1333 同样描述攻击者用精心构造输入触发异常 CPU 消耗。该证据支持成本放大变量，不等于所有解析器都有指数复杂度。

English scenario: Node.js documentation explains that a malicious client can submit input that occupies the event loop for a long time and prevents other clients from running; vulnerable regular expressions such as nested quantifiers can backtrack exponentially with input length. OWASP and CWE-1333 likewise describe crafted input causing excessive CPU use. This establishes the cost-amplification variable without claiming every parser is exponential.

中文攻击方：攻击者需要找到对未信任输入开放的高复杂度或故障路径，并构造触发最坏情况的内容；源代码、错误时延或试探可帮助识别。输入长度界限、无回溯实现、执行/回溯预算、隔离线程池、熔断和补丁会限制效果。

English attacker: The adversary needs an exposed high-complexity or fault path accepting untrusted input and crafted content that reaches its worst case, aided by source access, error timing, or probing. Input-length limits, nonbacktracking implementations, execution or backtracking budgets, isolated worker pools, circuit breakers, and patches constrain the effect.

中文防守方：防守方需要入口请求 ID、路由/模板、长度和状态，应用时延/错误，进程 CPU/内存或事件循环状态，崩溃/重启和健康探针。缺少每请求成本时只能用请求时间与主机资源近似；请求体被隐私脱敏、崩溃前日志未刷盘或共享进程承载多路由时形成盲区。

English defender: The defender needs ingress request ID, route or template, length and status, application duration and error, process CPU/memory or event-loop state, crash/restart, and health probe. Without per-request cost, duration and host resource are proxies. Privacy-redacted bodies, unflushed logs before crash, and one shared process serving many routes create blind spots.

### Supported mechanism and limitations

Mechanism is `TA0040-T1499-MECH-AMPLIFICATION` / `NM-FD`. **Limitation zh:** ReDoS 文档证明算法不对称和可用性结果，却不是命名攻击活动；不得制造 CASE 或把所有高时延解释为攻击。跨正则、解析、压缩和内核路径的通用化为中等置信，正式对象应保留具体实现证据。 **Limitation en:** ReDoS documentation establishes algorithmic asymmetry and availability impact but is not a named attack campaign; no CASE should be invented and high latency cannot automatically be treated as attack. Generalization across regex, parser, compression, and kernel paths is medium confidence and formal content should retain implementation evidence.

## Detection Strategy and Analytics

### `TA0040-T1499-DET-ENDPOINT-COST` — External Input to Endpoint Capacity and Availability / 外部输入到端点容量与可用性

**Objective:** detect low-visible input causing internal state exhaustion, disproportionate work, or crash and prove a legitimate-user availability result. Cover parent and both proposed children with two non-interchangeable analytics.

#### `TA0040-T1499-NJA-STATE-HOLDING`

**Logic:** On an AWS ALB or equivalent edge, collect 60-second `ActiveConnectionCount`, `NewConnectionCount`, `RejectedConnectionCount`, `RequestCount`, `ProcessedBytes`, `HTTPCode_ELB_4XX_Count`, `HTTPCode_ELB_5XX_Count`, target 5XX, target response time, and healthy target count by `LoadBalancer`, `TargetGroup`, and Availability Zone. Preserve ALB access fields `client:port`, `target:port`, `request_processing_time`, `target_processing_time`, `response_processing_time`, `elb_status_code`, `target_status_code`, `received_bytes`, `sent_bytes`, `request_line`, `user_agent`, `trace_id`, `target_group_arn`, `request_creation_time`, and `error_reason`.

At the endpoint, configure NGINX/Apache connection/request logging with `remote_addr`, `connection`, `connection_requests`, `request_id`, `request_length`, `request_time`, `status`, request method/URI/protocol, plus `mod_reqtimeout` stage/min-rate timeout events and worker/file-descriptor or connection-pool telemetry. In rolling one-minute bins, compare active connections and pool occupancy against completed requests and received bytes. Alert over a tunable five-minute window when active/incomplete state grows toward the configured capacity while bytes and completed request rate remain below that service's ordinary proportional range, then require rising rejection/timeouts or independent health failure for T1499 confirmation. Aggregate both per source and globally so distributed low-rate sources cannot evade.

**Correlation:** raw connection progress seconds to one minute; exhaustion window five minutes; baseline by listener/route/hour over 30 days. Dimensions: load balancer, target group, endpoint/listener, virtual host, connection ID, source/NAT group, request ID/trace ID, protocol/stage, time.

**False positives:** WebSocket/SSE/long polling, large or slow uploads, mobile/satellite networks, legitimate streaming, TLS/CRL delays, deployment drain, dependency slowness, and capacity undersizing.

**Blind spots:** CDN terminates slow connections before monitored ALB, completion-only access logs, HTTP/2 or HTTP/3 multiplexing, source NAT, encrypted protocol stage unavailable, missing configured pool capacity, and local telemetry lost during exhaustion.

**Tuning:** inventory legitimate long-lived routes/protocols and their expected progress, derive ratios per endpoint rather than global constants, preserve global pool alarms even when source allowlists exist, and alert on blocked attempts separately from confirmed availability. Apache example minimum rates are implementation examples, not universal detection thresholds. **Evidence:** E2–E4, E8–E10.

#### `TA0040-T1499-NJA-INPUT-COST`

**Logic:** Collect NGINX/ALB request fields above and OpenTelemetry HTTP server metrics/spans including `http.server.request.duration`, `http.request.method`, `http.response.status_code`, `url.template` or normalized route where configured, `server.address`, `server.port`, `error.type`, trace/span ID, and protocol version. Add application telemetry for `request_id`, normalized input-shape digest or validated feature flags, `request_bytes`, handler, worker/process ID, exception/crash type, and per-request CPU time or allocated bytes when instrumentation supports it; these application cost fields are custom and must not be mislabeled as standard OpenTelemetry fields. Join process CPU/memory, event-loop lag or worker-queue state, supervisor restart/OOM/crash, and external health.

Compute route/method/content-class baselines. In a five-minute window, identify a small request count/byte total whose p99 duration, process CPU/memory, queue depth, or crash rate is disproportionate to baseline; connect repeated input shape to the same high-cost handler and legitimate health failure. For sparse trigger crashes, join the last request/trace to crash/restart and failed health within 60 seconds. Report high-cost attempt, confirmed capacity degradation, and crash outcome separately.

**Correlation:** ingress-to-span by trace/request ID; request-to-crash 60 seconds; cost aggregation five minutes; route baseline 30 days. Dimensions: endpoint, route template, method, content type/length bucket, input-shape digest, request/trace ID, process/worker, exception type, time.

**False positives:** legitimate analytical query/report, cache warmup, large approved upload, database/downstream slowdown, GC, JIT compilation, deployment cold start, load test, and organically pathological input.

**Blind spots:** request body or route redacted, sampling omits rare trigger, crash before log flush, no per-request CPU attribution, shared worker handles many routes, edge rewrites request IDs, or exploit occurs below application instrumentation.

**Tuning:** set route-specific input/complexity limits and owner-approved expensive workflows, use ratio and outcome rather than raw duration alone, retain unsampled crash-adjacent edge logs, and never globally suppress health failures after deployment. Static/SAST findings for vulnerable regex raise context but do not establish an attack without request and availability evidence. **Evidence:** E5–E7, E8, E11–E13.

## Mitigation candidate

### `TA0040-T1499-MIT-WORK-ADMISSION` — Endpoint Work Admission, Cost Bounds, and Graceful Degradation / 端点工作准入、成本界限与优雅降级

**Measures:** (1) enforce handshake/header/body and maximum connection lifetime, minimum ingress progress, per-principal and global connection/queue limits, and separate pools for long-lived traffic; (2) normalize and bound untrusted input length, recursion, decompression, query complexity, regex backtracking/execution time, memory allocation, and per-request CPU/deadline; use nonbacktracking algorithms where feasible; (3) partition critical worker capacity, apply load shedding/circuit breakers and upstream filtering, maintain independent health probes and tested failover/restart; (4) patch known crash/exhaustion flaws and preserve last-request/crash telemetry outside the target process.

**Parent application:** map each critical endpoint to network path, listener, connection/worker/resource caps, external health and failover. Apply layered limits before internal work and reserve capacity for health/control traffic. **Expected effect:** constrains both floods and sparse triggers, reduces outage scope/duration, and preserves causal telemetry. **Limitations:** controls can reject slow or complex legitimate clients, autoscaling can increase cost without removing a bottleneck, and a shared dependency may remain a single failure point.

**State-child application:** configure Apache `RequestReadTimeout` or equivalent handshake/header/body timeouts and minimum rate, maximum lifetime, NGINX/proxy connection limits, and isolated pools for WebSocket/SSE/upload routes. **Expected effect:** incomplete sessions must make progress or are released before exhausting global capacity. **Limitations:** values that are too strict harm mobile/slow users; per-IP limits fail behind NAT or distributed sources; connection limits applied after TLS do not protect handshake resources.

**Amplification-child application:** replace vulnerable backtracking regex or enforce backtracking/execution limits; validate and cap input before expensive work; bound decompression/parser depth, query plans and per-request memory/CPU; isolate expensive handlers and trip a circuit breaker before shared event loop/pool failure. **Expected effect:** limits the input-to-work amplification ratio and contains a failing handler. **Limitations:** worst-case inputs are hard to enumerate, timeouts can leave downstream work running, static analysis has false negatives, and a kernel-level fault requires patching or upstream filtering.

**Reuse decision:** MIT-000194 contains independent health and tested restart/failover measures, but its semantic identity is control of orderly service-stop authority and includes a least-stop-authority measure irrelevant to exhaustion. Do not extend it directly; primary review may split a reusable availability-resilience control if measures remain semantically identical. MIT-000197/198 govern resource ownership for attacker work under NJT-0189, not work admission for unavailability.

## Evidence and conclusion-level sources

| Key | Primary source and locator | Support and limit |
|---|---|---|
| E1 `TA0040-T1499-REF-ATTACK` | [MITRE ATT&CK Enterprise v19 T1499](https://attack.mitre.org/versions/v19/techniques/T1499/) and fixed 19.1 inventory | Parent behavior, T1498 boundary, and four-child breadth only; new REF. |
| E1a–d `TA0040-T1499-REF-ATTACK-CHILD-*` | Versioned T1499 [.001](https://attack.mitre.org/versions/v19/techniques/T1499/001/), [.002](https://attack.mitre.org/versions/v19/techniques/T1499/002/), [.003](https://attack.mitre.org/versions/v19/techniques/T1499/003/), [.004](https://attack.mitre.org/versions/v19/techniques/T1499/004/) | Planning-only stack/exploit clusters; never imported as NJS. |
| E2 `TA0040-T1499-REF-OWASP-DOS` | [OWASP Denial of Service Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html), application and slow HTTP sections | Slow fragmented requests retain server resources with low attacker cost; mitigation concepts; new REF. |
| E3 `TA0040-T1499-REF-APACHE-REQTIMEOUT` | [Apache 2.4 mod_reqtimeout](https://httpd.apache.org/docs/2.4/mod/mod_reqtimeout.html), summary, examples, directive | Request stages, timeouts, minimum data rate, info logging and limits; new REF. |
| E4 `TA0040-T1499-REF-NGINX-TIMEOUT` | [NGINX core module](https://nginx.org/en/docs/http/ngx_http_core_module.html), client header/body and keepalive timeout | Request-state controls and protocol limits; new REF. |
| E5 `TA0040-T1499-REF-NODE-EVENTLOOP` | [Node.js: Don't Block the Event Loop](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop), event-loop security and REDOS sections | Malicious input blocks shared event loop; exponential regex example and input bounds; new REF. |
| E6 `TA0040-T1499-REF-OWASP-REDOS` | [OWASP ReDoS](https://community.owasp.org/attacks/Regular_expression_Denial_of_Service_-_ReDoS), description and attacks | Crafted small input causes exponential work/hang; not a named campaign; new REF. |
| E7 `TA0040-T1499-REF-CWE-1333` | [MITRE CWE-1333](https://cwe.mitre.org/data/definitions/1333.html), consequence and mitigations | CPU availability impact, nonbacktracking/input/execution bounds; new REF. |
| E8 `TA0040-T1499-REF-NGINX-LOG` | [NGINX log module](https://nginx.org/en/docs/http/ngx_http_log_module.html) and [core variables](https://nginx.org/en/docs/http/ngx_http_core_module.html) | Exact connection/request/time/length/status fields; logs generally materialize on request completion; new REF. |
| E9 `TA0040-T1499-REF-ALB-METRICS` | [AWS ALB CloudWatch metrics](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-cloudwatch-metrics.html), Active/New/Rejected connections, RequestCount, ProcessedBytes, HTTP codes | Real one-minute capacity metrics and their dimensional limits; new REF. |
| E10 `TA0040-T1499-REF-ALB-ACCESS` | [AWS ALB access logs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html), field table | Real processing-time, byte, request, target, status, trace and error fields; new REF. |
| E11 `TA0040-T1499-REF-OTEL-HTTP` | [OpenTelemetry HTTP metrics semantics](https://opentelemetry.io/docs/specs/semconv/http/http-metrics/) | Standard server request duration/method/status/route/error fields; per-request CPU is not standard; new REF. |
| E12 `TA0040-T1499-REF-WAF-FIELDS` | [AWS WAF logging fields](https://docs.aws.amazon.com/waf/latest/developerguide/logging-fields.html) | Client IP, country, headers, URI, args, method and request ID where WAF is used; new REF. |
| E13 `TA0040-T1499-REF-ATTACK-DET0208` | [ATT&CK DET0208](https://attack.mitre.org/detectionstrategies/DET0208/) | Parent resource/crash detection ideas; does not establish Niji children; new REF. |

## Shared-library lookup and resolution record

Executed `library_lookup.py` with: `endpoint denial service`; `slow HTTP denial service RequestReadTimeout`; `regular expression denial service ReDoS`; `nginx request_time request_length connection_requests`; `Application Load Balancer ActiveConnectionCount`; `OpenTelemetry http server request duration`; `input work amplification exhaustion`; and `state holding low rate exhaustion`. No exact REF/DET/NJA/MIT match exists for E1–E13 or the two proposed analytic identities.

- **References:** all source URLs above are new candidates. Existing REF-000866/REF-000867 describe orderly Windows service stopping and state transition for NJT-0185; use them as a boundary only, not evidence of exhaustion. Existing generic process/network schemas may supplement a host-specific implementation but do not replace request/resource sources.
- **Cases:** no qualified named CASE is proposed. OWASP, Apache, Node.js, NGINX, AWS, and CWE establish attack/control semantics but do not document one named victim chain with all availability facts. Do not manufacture a Slowloris or ReDoS CASE.
- **Claims:** propose `TA0040-T1499-CLM-PARENT` (endpoint internal exhaustion/crash with unsaturated path; E1); `TA0040-T1499-CLM-STATE` (slow fragmented requests retain concurrent state at low traffic; E2/E3); `TA0040-T1499-CLM-AMPLIFICATION` (crafted input produces exponential CPU/event-loop blockage; E5–E7); `TA0040-T1499-CLM-STATE-FIELDS` (E8–E10); `TA0040-T1499-CLM-COST-FIELDS` (E10–E12); `TA0040-T1499-CLM-MITIGATION` (timeouts/min-rate/input/algorithm bounds; E2–E7).
- **Detection objects:** DET-000213 is orderly stop-controller lineage and is semantically different. DET-000217/218 detect resource use for attacker work, not endpoint unavailability. DET-000168/185 connect exploitation to remote control or credential outcome, not availability. Recommendation: create `TA0040-T1499-DET-ENDPOINT-COST` and its two NJAs.
- **Mitigations:** MIT-000194 partly overlaps health/failover but its measure set and identity are malicious management stop control. MIT-000197/198 own resource use budgets/transaction admission for NJT-0189. MIT-000113 normalizes obscured content for stealth, not algorithmic work bounds. Recommendation: create the work-admission/cost-bound mitigation or split an exact availability-resilience measure after primary review.
- **Relationships:** no existing relation is reusable before formal IDs. T1499 may co-occur with exploit, T1498, T1529, or NJT-0189, but co-occurrence requires separate direct-object evidence.

## Rejected or deferred axes

| Axis | Resolution | Reason |
|---|---|---|
| Distributed-source per-node/request dilution | `evidence-deferred` | ATT&CK establishes botnet dilution, but a separate Niji child would cross T1498/source topology and lacks a defense distinct from global aggregation already required by state holding. |
| Source IP spoofing/reflection | `adjacent-technique` | Attribution/delivery variable belongs network DoS or source validation; endpoint internal state/work remains the T1499 object. |
| Crash/restart resembling ordinary software fault | `evidence-deferred` | Plausible Feature Disguise, but current sources do not prove attacker-controlled fault shaping separate from sparse amplification. |
| Maintenance-window or legitimate-traffic alignment | `evidence-deferred` | No conclusion-level T1499 evidence of deliberate alignment and trace change. |
| OS/service/application target tier | `not-stealth-distinct` | ATT&CK breadth context; resource layer is not an attacker-controlled observation variable. |
| Exploit versus flood | `not-stealth-distinct` | Exploit is a behavior form. Only state-holding or cost-asymmetry evidence produces a Niji child, and availability outcome remains mandatory. |

## Content-depth and research limitations

中文：当前证据高置信支持 HTTP 慢速状态保持和 ReDoS 输入放大，但跨协议、解析器、内核及非 Web 服务的泛化只能中等置信。两项主要来源是权威技术文档与安全指南，不是命名在野事件，因此正式子项可以建立机制和防御差异，但 CASE 保持空。可用性故障的正常原因极多；没有入口、内部资源及外部健康三面关联时，只能报告未解释的饱和或崩溃，不能推断攻击者意图。

English: Current evidence strongly supports slow HTTP state holding and ReDoS input amplification, while generalization across protocols, parsers, kernels, and non-web services is medium confidence. The main sources are authoritative technical documentation and security guidance rather than named field incidents, so mechanisms and defensive differences can support children while CASE remains empty. Availability failures have many benign causes; without joins across ingress, internal resource, and external health, only unexplained saturation or crash can be reported, not adversary intent.

Compared with NJT-0001 by field responsibility, the parent and both children separately cover direct behavior, stable variable, changed trace, observation difference, residual evidence, inclusion/exclusion, scenario, attacker prerequisites, defender visibility, mechanism, evidence strength, and limitation. The analytics use real fields and separate connection-state from request-cost logic. Canonical integration must retain paired bilingual prose and keep lifecycle at `review` pending human review.

**Integration status:** pending all five candidate handoffs, primary boundary convergence with T1498/T1529/NJT-0185/NJT-0189, shared-library resolution, formal allocation, YAML authoring, quality, Bundle, Web/API QA, and human review. Only this staging file was written.
