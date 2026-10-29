# BATCH-TA0002-015 T1569 / T1047 整改约束

- 总体任务范围是 Execution 剩余 NJT-0074～NJT-0082；本批处理 T1569/NJT-0079 与 T1047/NJT-0082。上一批 T1129/T1127 已通过证据、taxonomy、专用防御、质量、Bundle 与 42 项 Web 门禁。
- T1569 的直接对象是 Windows SCM、launchd 或 systemd 等服务管理器响应 create/start/control 而启动程序；T1047 的直接对象是 WMI client 调用 namespace/class/method，经 WMI service/provider 产生进程或动作。服务持久定义归父级相邻 Persistence 对象，WMI Event Subscription 归其专用持久化技术，远程 DCOM/WinRM 只是传输边界。
- 固定 `enterprise-attack 19.1`。T1569 有 T1569.001 Launchctl、.002 Service Execution、.003 Systemctl，必须作多轴覆盖而不导入；T1047 无子项，执行开放检索。候选轴分别检查既有服务上下文借用、短驻服务事务、定义替换边界，以及 provider 托管来源、远程会话分离、日常管理语义合形和查询/执行方法差异。
- 为两项分别创建专用 DET/NJA/MIT。服务分析关联 control request、service definition、manager event、process 与 create-start-delete；WMI 分析关联 client/session、namespace/class/method、provider operation、wmiprvse child 与远程来源。旧 DET-000063/MIT-000060 只保留 NJT-0089 服务持久化覆盖，WMI 专用旧 NJA-000042 在迁移后归档。
- 当前批次未通过结论级证据、字段深度、共享库、Schema、Bundle 与 Web QA 前，不进入最后 T1204 批次。
