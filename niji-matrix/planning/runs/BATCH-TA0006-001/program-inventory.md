# TA0006 fixed ATT&CK Enterprise 19.1 parent inventory

Source: `data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx`, sheet `techniques`; the parent set is reconciled with `planning/tactics/TA0006.yaml`. ATT&CK children below are planning-only implementation breadth and are never imported as Niji children.

| Order | Parent | Child count | Fixed ATT&CK child IDs and labels |
|---:|---|---:|---|
| 1 | T1557 Adversary-in-the-Middle | 4 | T1557.002 ARP Cache Poisoning; T1557.003 DHCP Spoofing; T1557.004 Evil Twin; T1557.001 Name Resolution Poisoning and SMB Relay |
| 2 | T1110 Brute Force | 4 | T1110.004 Credential Stuffing; T1110.002 Password Cracking; T1110.001 Password Guessing; T1110.003 Password Spraying |
| 3 | T1555 Credentials from Password Stores | 6 | T1555.006 Cloud Secrets Management Stores; T1555.003 Credentials from Web Browsers; T1555.001 Keychain; T1555.005 Password Managers; T1555.002 Securityd Memory; T1555.004 Windows Credential Manager |
| 4 | T1212 Exploitation for Credential Access | 0 | None; open Niji taxonomy search still required |
| 5 | T1187 Forced Authentication | 0 | None; open Niji taxonomy search still required |
| 6 | T1606 Forge Web Credentials | 2 | T1606.002 SAML Tokens; T1606.001 Web Cookies |
| 7 | T1056 Input Capture | 4 | T1056.004 Credential API Hooking; T1056.002 GUI Input Capture; T1056.001 Keylogging; T1056.003 Web Portal Capture |
| 8 | T1556 Modify Authentication Process | 9 | T1556.009 Conditional Access Policies; T1556.001 Domain Controller Authentication; T1556.007 Hybrid Identity; T1556.006 Multi-Factor Authentication; T1556.004 Network Device Authentication; T1556.008 Network Provider DLL; T1556.002 Password Filter DLL; T1556.003 Pluggable Authentication Modules; T1556.005 Reversible Encryption |
| 9 | T1111 Multi-Factor Authentication Interception | 0 | None; open Niji taxonomy search still required |
| 10 | T1621 Multi-Factor Authentication Request Generation | 0 | None; open Niji taxonomy search still required |
| 11 | T1040 Network Sniffing | 0 | None; open Niji taxonomy search still required |
| 12 | T1003 OS Credential Dumping | 8 | T1003.008 /etc/passwd and /etc/shadow; T1003.005 Cached Domain Credentials; T1003.006 DCSync; T1003.004 LSA Secrets; T1003.001 LSASS Memory; T1003.003 NTDS; T1003.007 Proc Filesystem; T1003.002 Security Account Manager |
| 13 | T1528 Steal Application Access Token | 0 | None; open Niji taxonomy search still required |
| 14 | T1539 Steal Web Session Cookie | 0 | None; open Niji taxonomy search still required |
| 15 | T1649 Steal or Forge Authentication Certificates | 0 | None; open Niji taxonomy search still required |
| 16 | T1558 Steal or Forge Kerberos Tickets | 5 | T1558.004 AS-REP Roasting; T1558.005 Ccache Files; T1558.001 Golden Ticket; T1558.003 Kerberoasting; T1558.002 Silver Ticket |
| 17 | T1552 Unsecured Credentials | 8 | T1552.008 Chat Messages; T1552.005 Cloud Instance Metadata API; T1552.007 Container API; T1552.001 Credentials In Files; T1552.002 Credentials in Registry; T1552.006 Group Policy Preferences; T1552.004 Private Keys; T1552.003 Shell History |

All 17 fixed parent IDs occur exactly once in the TA0006 plan. The formal TA0006 matrix contains zero techniques at preflight. The current delivery subset is T1557 and T1110; subsequent batches are sequential and do not imply admission or formal NJS counts.
