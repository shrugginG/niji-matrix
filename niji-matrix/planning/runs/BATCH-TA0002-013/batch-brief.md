# BATCH-TA0002-013 T1204 单候选整改约束

- 总体任务范围是 Execution 剩余 NJT-0074～NJT-0082；本批只处理最后的 T1204/NJT-0081。上一批 T1569/T1047 已通过独立证据、taxonomy、专用防御、质量、Bundle 与 45 项 Web 门禁。
- 固定 `enterprise-attack 19.1` 的 T1204 有 T1204.001 Malicious Link、.002 Malicious File、.003 Malicious Image、.004 Malicious Copy and Paste、.005 Malicious Library。它们按媒介和用户动作划分，只作为宽度先验，不导入 Niji 子项。
- 直接对象是攻击者诱导或依赖用户完成导致代码、脚本、镜像、库或远程工具实际执行的动作。Phishing/Initial Access 负责投递，T1203 负责漏洞触发，T1059/容器/库/远程工具负责执行实现；T1204 固定人类授权动作到首个恶意结果的因果边。
- 检验两个既有 Niji 轴：让恶意操作贴合用户真实工作/支持/开发流程，以及把一次执行拆成浏览器、clipboard、Run/terminal、paste/enter 等多步交互。ClearFake/TA571、Contagious Interview、Raspberry Robin 与 LAPSUS$/Scattered Spider 只能支持各自观察到的结论。
- 重写既有 DET-000060/NJA-000038/MIT-000059 为 T1204 专用对象，关联 user-facing app/event、下载/clipboard/file/repository、user action、helper/interpreter/runtime、首个恶意进程/网络结果和身份/支持上下文。当前批次通过全部门禁后，九项整改项目才整体完成；正式对象仍停留 `review`。
