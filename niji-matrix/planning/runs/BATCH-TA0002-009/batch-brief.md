# BATCH-TA0002-009 T1609 / T1610 整改约束

- 固定 `enterprise-attack 19.1`；前序 BATCH-TA0002-008 全部门禁通过后，本批处理 NJT-0066（既有容器内命令）与 NJT-0067（新容器/工作负载部署）。一个对象必须以 exec/attach 等进入已运行容器，另一个必须产生新的容器实例，不能因都使用 Kubernetes/Docker 而合并。
- T1609 检索 Kubernetes audit、RBAC/subresource、kubelet、Docker exec events、运行时进程以及 TeamTNT/外部攻击案例。既有工作负载借用要求直接证据；自动化身份一致性若缺少现场攻击者意图证据必须保持 medium 并说明局限。
- T1610 检索 create/admission/image resolution、workload spec、容器事件、Pod Security、签名/证明和 TeamTNT/Portainer 伪装案例。良性镜像后置载荷与规范上下文伪装必须按不同可观测变量划分。
- 每项创建独立 DET/NJA/MIT；检测分别以 exec request—runtime result 和 create/admission—resolved image—first action 为核心。不得以 shell 名称、镜像名称、privileged 标志或单一告警直接定性。
