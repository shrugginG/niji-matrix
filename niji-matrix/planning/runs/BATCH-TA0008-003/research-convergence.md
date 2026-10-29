# BATCH-TA0008-003 T1021 主 Agent 收敛

- 准入：adapt；新建 T1021 对应父项。NJT-0055/T1133 的直接对象是外部首次/持续重入及 token/session replay、用户风险情境；T1021 的直接对象是已有内网立足点后的 source asset→destination→service→accepted fresh session→target action。SMB/DCOM/WinRM 等并不依赖外部网关风险面，因此父项 split。
- 固定 8 个 ATT&CK 子项已逐项覆盖并完成第二 taxonomy pass。协议和云控制面不导入 NJS；Cloud Services 的有效身份和云命令由 NJT-0061/NJT-0064 等既有对象承担，Direct Cloud VM 仅在真实新建 guest RDP/SSH 会话时进入父项。
- 正式 Niji 子项 2 项：
  1. 角色贴合的远程管理路径：攻击者选择与批准的 source role、destination role、principal、service、time 关系贴合的连接，使恶意会话落入日常管理图。与 NJS-0055-002 的外部用户 geography/ASN/device/time 风险情境不同。
  2. 中继来源远程会话间接化：original controller 经受控 relay/jump/bastion 建立 fresh destination session，目标只见 relay/localhost。与 NJS-0168-002 的禁止域对桥接不同：此处即使路径获批，未授权操作者仍可借用；与 NJS-0151-001 不同：目标是新认证连接而非旧 transport 增 channel。
- 延期：攻击者自有会话长寿化、低交互、时序稀释和 service broker 子轴缺结论级意图、兄弟边界或独立防御差异。
- 防御：新建 1 DET + 2 NJA。扩展 MIT-000052 到父项/角色路径，扩展 MIT-000172 到中继路径；不复制 DET-000053/094/191。
- 来源：7 个正式新 REF；Ubuntu SSH 生命周期仅支撑延期轴，不进入正式库。复用 REF-000278/289/377/598/604/614。三个 Case 分别按真实入侵、授权评估、跨报告模式限制结论。
- 正式对象先保持 draft；通过证据、Schema、查重、Bundle、Web/API 后提升 review。T1550 不在本批分配 ID。
