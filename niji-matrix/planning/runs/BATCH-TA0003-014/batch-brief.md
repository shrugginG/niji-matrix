# BATCH-TA0003-014 T1112 研究约束

- 固定 `enterprise-attack 19.1`；本批只处理 T1112，前序 T1556 全部门禁通过。
- 直接对象限于 Windows Registry 中由系统/应用以后消费、能够维持访问或激活其他持久化的状态。Run key、服务、Office、认证策略等具体语义仍归各自技术；T1112 只保留跨语义的 registry 状态与观察差。
- ATT&CK 无子技术，开放搜索覆盖命名、API 可见性、数据遮蔽、远程修改和 per-user overlay；只有 null-prefixed pseudo-hidden key 具直接稳定证据和独立枚举差分。
- 本批未过全部门禁前不得进入 T1137。

