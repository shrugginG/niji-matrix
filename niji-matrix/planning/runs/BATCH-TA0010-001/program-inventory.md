# TA0010 fixed ATT&CK Enterprise 19.1 parent inventory

Source: [MITRE ATT&CK Enterprise v19 Exfiltration tactic](https://attack.mitre.org/versions/v19/tactics/TA0010/) and [Enterprise ATT&CK v19.1 STIX bundle](https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-19.1.json). The tactic has nine parent rows. ATT&CK children below are planning-only research breadth context, never Niji child IDs.

| No. | Parent | Name | ATT&CK children | Represented ATT&CK dimension | Planned batch |
|---:|---|---|---|---|---|
| 1 | T1020 | Automated Exfiltration | T1020.001 | Traffic mirroring as an automated collection and forwarding implementation | BATCH-TA0010-002 |
| 2 | T1030 | Data Transfer Size Limits | none | No ATT&CK child partition | BATCH-TA0010-001 |
| 3 | T1048 | Exfiltration Over Alternative Protocol | T1048.001, T1048.002, T1048.003 | Symmetric encryption, asymmetric encryption, or no encryption on a non-C2 protocol | BATCH-TA0010-002 |
| 4 | T1041 | Exfiltration Over C2 Channel | none | No ATT&CK child partition | BATCH-TA0010-002 |
| 5 | T1011 | Exfiltration Over Other Network Medium | T1011.001 | Bluetooth as a medium implementation | BATCH-TA0010-002 |
| 6 | T1052 | Exfiltration Over Physical Medium | T1052.001 | USB as a physical-medium implementation | BATCH-TA0010-002 |
| 7 | T1567 | Exfiltration Over Web Service | T1567.001, T1567.002, T1567.003, T1567.004 | Code repository, cloud storage, text storage, or webhook service form | BATCH-TA0010-003 |
| 8 | T1029 | Scheduled Transfer | none | No ATT&CK child partition | BATCH-TA0010-001 |
| 9 | T1537 | Transfer Data to Cloud Account | none | No ATT&CK child partition | BATCH-TA0010-003 |

Only formal techniques under `matrix/tactics/TA0010-exfiltration/techniques/` count toward TA0010 completion. Neither TA0005 nor any external list contributes to that count. No candidate decision or Niji child is implied by this inventory.
