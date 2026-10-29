# TA0009 fixed ATT&CK Enterprise 19.1 parent inventory

Source: `data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx`; tactic membership from the `tactics` column. Parent and child identifiers below are research metadata, never Niji child IDs.

| No. | Parent | Name | ATT&CK children | Planned batch |
|---:|---|---|---|---|
| 1 | T1557 | Adversary-in-the-Middle | T1557.002, T1557.003, T1557.004, T1557.001 | BATCH-TA0009-002 |
| 2 | T1560 | Archive Collected Data | T1560.003, T1560.002, T1560.001 | BATCH-TA0009-001 |
| 3 | T1123 | Audio Capture | none | BATCH-TA0009-005 |
| 4 | T1119 | Automated Collection | none | BATCH-TA0009-001 |
| 5 | T1185 | Browser Session Hijacking | none | BATCH-TA0009-004 |
| 6 | T1115 | Clipboard Data | none | BATCH-TA0009-006 |
| 7 | T1074 | Data Staged | T1074.001, T1074.002 | BATCH-TA0009-001 |
| 8 | T1530 | Data from Cloud Storage | none | BATCH-TA0009-007 |
| 9 | T1602 | Data from Configuration Repository | T1602.002, T1602.001 | BATCH-TA0009-007 |
| 10 | T1213 | Data from Information Repositories | T1213.003, T1213.001, T1213.004, T1213.006, T1213.005, T1213.002 | BATCH-TA0009-003 |
| 11 | T1005 | Data from Local System | none | BATCH-TA0009-006 |
| 12 | T1039 | Data from Network Shared Drive | none | BATCH-TA0009-006 |
| 13 | T1025 | Data from Removable Media | none | BATCH-TA0009-008 |
| 14 | T1114 | Email Collection | T1114.003, T1114.001, T1114.002 | BATCH-TA0009-004 |
| 15 | T1056 | Input Capture | T1056.004, T1056.002, T1056.001, T1056.003 | BATCH-TA0009-008 |
| 16 | T1113 | Screen Capture | none | BATCH-TA0009-005 |
| 17 | T1125 | Video Capture | none | BATCH-TA0009-005 |

All 17 parent rows are included, including T1557 and T1056 with additional Credential Access mapping. No TA0005 list or external candidate inventory is counted. ATT&CK children provide a taxonomy breadth prior only.
