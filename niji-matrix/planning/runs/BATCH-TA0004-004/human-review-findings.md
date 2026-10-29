# BATCH-TA0004-004 人工可读审阅记录

## 候选与对象决议

- T1547 在 TA0004 下独立决议为 retain。ATT&CK 19.1 直接说明部分启动/登录自启动以更高权限运行；正式门槛是 writer/pre-state → descriptor → lifecycle consumer security context → positive authority delta → first newly-authorized outcome。
- 同权限用户级恢复只承担 Persistence。HKLM、SYSTEM/root、系统父体、LSA、Winlogon、spooler、kernel 或高权限路径都不能单独证明提权。
- 直接对象仍是 NJT-0084 的生命周期激活映射，因此跨战术扩展复用 NJT-0084 与三个 NJS，不新建 NJT/NJS；TA0003 decision 保持 canonical，TA0004 独立由 DEC-TA0004-T1547 表达。

## Taxonomy breadth

- 十四项固定子技术已显式覆盖：T1547.007 支持会话恢复队列，T1547.009 支持既有描述符目标替换，其余实现留在父级；没有导入 ATT&CK 子技术。
- 第二轮检查 update theme、writer-consumer 权限分离、system/user scope、broker provenance、early-boot sensor gap 与 trusted-component loading。更新主题是第三个既有正式轴；权限分离/scope/broker 为 parent-core，early boot deferred，load hijacking adjacent，平台/组件/介质 rejected。
- 最终正式数仍为 3，新增 0。不能增加：没有第四个同时改变 stable trace、观察结果与独立防御的轴。不能减少：theme、old/new descriptor、restoration item/prior session 使用不同关联键、反例和恢复动作。

## 内容、证据与防御

- NJT-0084 及三个 NJS 均新增候选特定的 TA0004 定义、范围、场景、攻防模型、机制或限制，特别保留用户级案例不证明提权、恢复队列大多同用户执行等限制。
- REF-000148 扩展 TA0004 与 higher-authority 条件；既有九项 Reference、两项 Case 和十项 Claim 复用。新建 CLM-000542（TA0004 relevance）与 CLM-000543（dual-output detection）。
- DET-000065 输出未批准状态、Persistence 恢复与 proven Privilege Escalation；NJA-000044 新增第七类数据，保存 writer/pre-state、consumer token/security context、authority delta 和首个新获准结果。MIT-000064 新增第六项 writer-consumer boundary measure，并覆盖高权限进程/module、session/token 与结果回滚。

## 门禁与状态

- make quality：1367 个对象，0 errors、0 warnings；planning 0/0；重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础测试通过。
- dist/techniques/NJT-0084.json 已重建；pipeline 为 TA0004 inventory 13、decision 4、technique 4、subtechnique 11、gap pending；无 reserved ID。
- Review Web npm test 58/58；Headless Chrome 实际渲染父、3 个子项、DET/NJA/MIT 的 zh/en 共 14 页，标题、核心字段、语言状态、交叉链接和 raw YAML 均无缺失。
- 本批保持 review，没有人工领域 reviewer。前五进度 4/5；下一批处理 T1037。TA0004 未关闭。

