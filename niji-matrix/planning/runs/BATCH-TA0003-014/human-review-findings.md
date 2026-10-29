# BATCH-TA0003-014 人工审查整改记录

## 发现

2026-09-12 的 Persistence 横向审计发现，NJT-0094、NJS-0094-001 以及 DET-000074、NJA-000053、MIT-000074 全部只引用 ATT&CK T1112 页面。原父/子攻防模型和限制过短，无法区分等价权限 API 差、ACL 拒绝、WOW64/virtualization、未装载 hive、parser 错误和在线扫描竞争；检测对象虽有字段，但没有来源证明 Sysmon 事件、kernel/Win32 字符串语义、raw hive 差分和专用清除。

## 整改决议

- 保留 `adapt` 与单一 NJS-0094-001；不因 ATT&CK 无子项而停止开放 taxonomy 搜索，也不为数量新增证据不足轴。
- 使用 FIN7 CARBANAK 证明父级 writer—state—consumer 链，使用 Sysinternals 与 Kovter 证明 embedded-null API 差分、实际消费和恢复限制。
- 扩展 REF-000230 的同一 Sysmon URL 身份，使 Registry 12/13/14 与原进程/管道字段共同可引用，不创建重复 Reference。
- 重写父/子全部核心字段，显式要求同一快照、等价权限、原始名称字节和 consumer 结果。
- DET/NJA 分离未批准写入、持久状态异常、API 视图异常和确认伪隐藏 consumer 链；MIT 增加版本/事务保留、跨视图盘点和 consumer 感知恢复。
- 增加候选级 Review Web 回归测试；全套门禁通过后恢复 `review`。

## 共享库决议

- `REF-000230`：extend，同一官方 URL，增加 Registry Event 12/13/14 覆盖。
- `REF-000308..REF-000311`：create，覆盖 RegDelNull、RootkitRevealer、Kovter 与 FIN7。
- `CASE-000113..CASE-000114`：create，分别支撑伪隐藏子项与父级 consumer 链。
- `CLM-000380..CLM-000381`：extend，语义身份不变并补充结论级来源。
- `DET-000074`、`NJA-000053`、`MIT-000074`：extend，身份不变并扩展可实施性。
