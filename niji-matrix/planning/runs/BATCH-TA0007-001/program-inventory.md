# TA0007 fixed ATT&CK Enterprise 19.1 parent inventory

Source: `data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx`, `techniques` sheet. Include every parent whose `tactics` contains `Discovery`, including T1622 and T1497 which also map to Stealth. The ATT&CK children below are planning-only breadth context and are never imported as Niji children.

| Order | Parent | ATT&CK child count | Fixed child IDs and names | Planned batch |
|---:|---|---:|---|---|
| 1 | T1087 Account Discovery / 账户发现 | 4 | T1087.004 Cloud Account; T1087.002 Domain Account; T1087.003 Email Account; T1087.001 Local Account | BATCH-TA0007-001 |
| 2 | T1010 Application Window Discovery / 应用窗口发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-001 |
| 3 | T1217 Browser Information Discovery / 浏览器信息发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-002 |
| 4 | T1580 Cloud Infrastructure Discovery / 云基础设施发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-002 |
| 5 | T1538 Cloud Service Dashboard / 云服务控制台 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-002 |
| 6 | T1526 Cloud Service Discovery / 云服务发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-003 |
| 7 | T1619 Cloud Storage Object Discovery / 云存储对象发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-003 |
| 8 | T1613 Container and Resource Discovery / 容器与资源发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-003 |
| 9 | T1622 Debugger Evasion / 调试器规避 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-004 |
| 10 | T1652 Device Driver Discovery / 设备驱动程序发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-005 |
| 11 | T1482 Domain Trust Discovery / 域信任发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-005 |
| 12 | T1083 File and Directory Discovery / 文件与目录发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-005 |
| 13 | T1615 Group Policy Discovery / 组策略发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-006 |
| 14 | T1680 Local Storage Discovery / 本地存储发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-006 |
| 15 | T1654 Log Enumeration / 日志枚举 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-006 |
| 16 | T1046 Network Service Discovery / 网络服务发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-007 |
| 17 | T1135 Network Share Discovery / 网络共享发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-007 |
| 18 | T1040 Network Sniffing / 网络嗅探 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-008 |
| 19 | T1201 Password Policy Discovery / 密码策略发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-009 |
| 20 | T1120 Peripheral Device Discovery / 外围设备发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-009 |
| 21 | T1069 Permission Groups Discovery / 权限组发现 | 3 | T1069.003 Cloud Groups; T1069.002 Domain Groups; T1069.001 Local Groups | BATCH-TA0007-009 |
| 22 | T1057 Process Discovery / 进程发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-010 |
| 23 | T1012 Query Registry / 注册表查询 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-010 |
| 24 | T1018 Remote System Discovery / 远程系统发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-010 |
| 25 | T1518 Software Discovery / 软件发现 | 2 | T1518.002 Backup Software Discovery; T1518.001 Security Software Discovery | BATCH-TA0007-011 |
| 26 | T1082 System Information Discovery / 系统信息发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-011 |
| 27 | T1614 System Location Discovery / 系统位置发现 | 1 | T1614.001 System Language Discovery | BATCH-TA0007-011 |
| 28 | T1016 System Network Configuration Discovery / 系统网络配置发现 | 2 | T1016.001 Internet Connection Discovery; T1016.002 Wi-Fi Discovery | BATCH-TA0007-012 |
| 29 | T1049 System Network Connections Discovery / 系统网络连接发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-012 |
| 30 | T1033 System Owner/User Discovery / 系统所有者与用户发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-012 |
| 31 | T1007 System Service Discovery / 系统服务发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-013 |
| 32 | T1124 System Time Discovery / 系统时间发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-013 |
| 33 | T1673 Virtual Machine Discovery / 虚拟机发现 | 0 | None; open Niji taxonomy search required | BATCH-TA0007-013 |
| 34 | T1497 Virtualization/Sandbox Evasion / 虚拟化与沙箱规避 | 3 | T1497.001 System Checks; T1497.003 Time Based Checks; T1497.002 User Activity Based Checks | BATCH-TA0007-014 |

All 34 fixed parent IDs occur exactly once in the TA0007 plan. The formal TA0007 matrix contains zero techniques at preflight. The current delivery subset is T1087 and T1010; planned later batches do not imply admission or formal NJS counts.
