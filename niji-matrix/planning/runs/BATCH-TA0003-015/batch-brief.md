# BATCH-TA0003-015 T1137 研究约束

- 固定 `enterprise-attack 19.1`；本批只处理 T1137，前序 T1112 全部门禁通过。
- 直接对象是 Office/Outlook 在应用启动或其持久配置生命周期中自动加载的模板、宏、add-in、form、rule 或 homepage 状态。一般事件订阅归 T1546，加载路径劫持归 T1574，Registry 仅是介质。
- 六项 ATT&CK 子项触发覆盖表和第二轮 taxonomy；平台/功能名称不得导入。正式变量只在稳定改变 Office 信任/启动观察且有独立防御时成立。
- 本批未过全部门禁前不得进入 T1653。

