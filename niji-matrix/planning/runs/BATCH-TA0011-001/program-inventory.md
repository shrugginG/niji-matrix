# TA0011 Command and Control — ATT&CK Enterprise 19.1 fixed inventory

Source: https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-19.1.json

This inventory contains all 18 parent techniques assigned to TA0011 in the fixed STIX bundle. Its 27 ATT&CK children are planning-only breadth context; none is a Niji child.

| Parent | Name | ATT&CK children | Planned batch |
|---|---|---|---|
| T1001 | Data Obfuscation | T1001.001 Junk Data, T1001.002 Steganography, T1001.003 Protocol or Service Impersonation | BATCH-TA0011-001 |
| T1008 | Fallback Channels | None | BATCH-TA0011-001 |
| T1071 | Application Layer Protocol | T1071.001 Web Protocols, T1071.002 File Transfer Protocols, T1071.003 Mail Protocols, T1071.004 DNS, T1071.005 Publish/Subscribe Protocols | BATCH-TA0011-002 |
| T1090 | Proxy | T1090.001 Internal Proxy, T1090.002 External Proxy, T1090.003 Multi-hop Proxy, T1090.004 Domain Fronting | BATCH-TA0011-003 |
| T1092 | Communication Through Removable Media | None | BATCH-TA0011-003 |
| T1095 | Non-Application Layer Protocol | None | BATCH-TA0011-004 |
| T1102 | Web Service | T1102.001 Dead Drop Resolver, T1102.002 Bidirectional Communication, T1102.003 One-Way Communication | BATCH-TA0011-004 |
| T1104 | Multi-Stage Channels | None | BATCH-TA0011-005 |
| T1105 | Ingress Tool Transfer | None | BATCH-TA0011-005 |
| T1132 | Data Encoding | T1132.001 Standard Encoding, T1132.002 Non-Standard Encoding | BATCH-TA0011-006 |
| T1205 | Traffic Signaling | T1205.001 Port Knocking, T1205.002 Socket Filters | BATCH-TA0011-006 |
| T1219 | Remote Access Tools | T1219.001 IDE Tunneling, T1219.002 Remote Desktop Software, T1219.003 Remote Access Hardware | BATCH-TA0011-007 |
| T1568 | Dynamic Resolution | T1568.001 Fast Flux DNS, T1568.002 Domain Generation Algorithms, T1568.003 DNS Calculation | BATCH-TA0011-008 |
| T1571 | Non-Standard Port | None | BATCH-TA0011-008 |
| T1572 | Protocol Tunneling | None | BATCH-TA0011-009 |
| T1573 | Encrypted Channel | T1573.001 Symmetric Cryptography, T1573.002 Asymmetric Cryptography | BATCH-TA0011-009 |
| T1659 | Content Injection | None | BATCH-TA0011-010 |
| T1665 | Hide Infrastructure | None | BATCH-TA0011-010 |

Inventory extraction: active, non-revoked `attack-pattern` objects with a `command-and-control` kill-chain phase; parent rows have `x_mitre_is_subtechnique` false. Parent and child counts are confined to TA0011.
