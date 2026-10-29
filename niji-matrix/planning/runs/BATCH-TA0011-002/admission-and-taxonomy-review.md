# T1071 主 Agent 准入与原生分类收敛

固定基线为 ATT&CK Enterprise 19.1。sub-agent 独立提交 `T1071-research-handoff.yaml` 后，主 Agent 对五个 ATT&CK 子项、两条 Niji 变量、相邻技术和共享库逐项复核。准入结论为 **adapt**：保留持续应用层命令/结果交换的父行为，只把有可说明观察差的会话方向、协议中介或地址路由纳入匿迹分析。普通 HTTP、DNS、邮件、FTP、MQTT 流量、端口或 TLS 本身不够；单次工具下载及纯外传不成立 C2。

## 两项正式分类变量

1. **协议中介分离控制端**：受害端与解析器、broker 或消息路由节点完成协议事务，实际下令者在另一侧。WailingCrab 与 MQsTTang 的公共 broker 样本直接支持控制端与受害端目的地分离；Wekby 的 DNS TXT 请求/回复只在使用递归解析器的观察模型下支持类似路径，不能据样本断言每个受害端五元组都不指向权威端。残余包括完整 DNS 问题名、broker 主题、客户端 ID 和端点结果。区别于 T1102 的服务资源/信誉、T1090 的代理转发与 T1572 的内层协议封装。
2. **按接收者分区控制地址**：攻击者把共享控制主题改为每植入独立的逻辑接收地址，使仅监控旧共享主题或按单主题聚合的防守方失去整体覆盖。IBM 对 WailingCrab 两版有直接可见性比较，ESET 对 MQsTTang 的唯一客户端主题提供独立实现。该变量在 broker 已知时仍成立，区别于第一项的控制端目的地分离；但公开证据主要来自 MQTT，不能自动推广到邮箱或其他队列。全量 broker 日志、授权设备目录与跨主题图谱可消除这一匿迹效果。

两项子技术均以稳定的观察关系和防守差异命名，不按 ATT&CK 的协议类别、产品或 topic 字符串建项。父技术保留普通应用会话承载的行为面；不存在“必须为五项 ATT&CK 子项各建 NJS”的配额。

## 五个 ATT&CK 子项的规划覆盖

| 固定基线子项 | 主 Agent 覆盖决议 | 理由 |
|---|---|---|
| T1071.001 Web Protocols | parent-core；相邻 NJT-0152/T1102 | Web 请求回复是父级承载；服务契约伪装、公共服务资源有其他直接对象。 |
| T1071.002 File Transfer Protocols | evidence-deferred | 已知清单支持协议类别，但本轮没有独立原始材料证明可重复文件任务队列与独立匿迹观察差；一次下载或外传不入子项。 |
| T1071.003 Mail Protocols | parent-core；相邻 NJT-0152 | Turla Outlook MAPI 展示邮件控制能力；实际入站命令 PDF 未被研究者取得，PDF 内容遮蔽另归 NJT-0152。 |
| T1071.004 DNS | niji-variable-candidate | Wekby TXT 事务与标准递归解析路径提供协议中介研究线索；问题名和回复仍可见，演示命令由模拟 DNS 服务器生成。 |
| T1071.005 Publish/Subscribe Protocols | niji-variable-candidate | 两个独立 MQTT 原始案例支持 broker 分离控制端；WailingCrab 版本对比支持接收者分区后的共享主题可见性变化。 |

另审查了“受害端先发起会话”轴，正常应用过于普遍，未形成独立子项；消息表示、编码、加密、失败换路和公共服务信誉分别与 NJT-0152、T1132、T1573、NJT-0153、T1102 划界。

## 证据与防御限制

Wekby 报告中的 drive/open 命令回合由模拟 DNS 服务器产生，不能写成现场操作者任务；ESET 对 Turla Outlook 未取得真实入站命令 PDF；ESET 2025 年修订了 MQsTTang 的行为归属，案例不得无条件写作 Mustang Panda。原始报告没有测量组织级漏报率。Zeek/Sysmon/EMQX/AWS 文档只支持可配置的数据或控制功能，需注明 Sysmon Event 3 默认关闭、公共 broker 不提供完整服务端日志、递归缓存和加密 DNS 改变观察面。

防御按对象分工：父级与第一子项需要 DNS 事务/进程/结果和 broker 发布—订阅—端点结果的双侧关联；第二子项需要跨主题、客户端、注册标识的图谱与授权。正式 broker Analytic 应以 EMQX Cloud Data Integration 的发布、投递、订阅事件持续导出为数据前提，订阅清单 API 用于对照；Log Trace 仅作为受限部署和时长内的定向取证辅助，不能替代全量历史。两个 MIT 分别管理应用协议出口及中介映射、broker topic 身份授权与审计。公共 broker 无日志共享时只得低置信端点候选，不能声称识别发布者。

共享库初步决议：复用并扩展 REF-000625 的固定基线 locator，复用 REF-000230、REF-000632/634/635 与 REF-000636；新增有唯一原始 URL 的 Wekby、WailingCrab、MQsTTang、Turla、RFC 1034、MQTT 5.0 和 EMQX Cloud 文档；DET/NJA/MIT 按上述不同目标、关联键和控制动作新建。相似标题不构成复用。正式 ID 在本文件记录准入和分类后由主 Agent 统一分配。
