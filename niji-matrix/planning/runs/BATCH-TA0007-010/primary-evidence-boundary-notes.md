# Independent primary review — before complete research handoff

No admission decision, semantic ID reservation, or canonical content has been written. These notes are an independent check while the assigned researcher completes the candidate handoff.

## Fixed inventory and adjacent objects

The versioned 19.1 techniques workbook contains T1018 v3.6, modified 2026-05-12, with Discovery as its tactic and zero child rows. The mechanical extraction is preserved in `fixed-baseline-T1018.json`. The user's TA0011 plan reference concerns the already-reviewed Command and Control inventory; TA0007 determines this delivery. The current BATCH-TA0007-010 work item was already registered and has been activated rather than duplicated.

Reading the current canonical neighbor scopes confirms a useful direct-object boundary. NJT-0234 explicitly excludes mere host-presence confirmation from network-service discovery. NJT-0235 distinguishes `net view` domain/computer output from server share lists. NJT-0181 reserves trust relationships and excludes host/domain-controller lists. NJT-0236 requires an actual packet-observation relationship; local files or API inventories do not become sniffing because their contents mention a network. NJT-0233 covers obtaining log sources or records; extracting host facts from already available knowledge must not silently be presented as a new log-enumeration transaction. Cloud and container infrastructure retain their dedicated resource-object boundaries.

NJS-0131-001 already uses a preexisting identity-view variable, and NJS-0234-001 uses service-advertisement lookup substitution. Similar abstract trace logic does not establish semantic duplication: the obtained identity, host, or service fact, replacement path, and directly applicable defense must be checked separately. A child for T1018 cannot simply copy those paragraphs or their mechanisms.

## Independently read source semantics

Microsoft GetIpNetTable documentation describes enumerating the local IPv4-to-physical-address table. ERROR_NO_DATA can be successful with no entries. The `arp` command distinguishes display operations from addition/deletion; verbose output can include invalid and loopback entries. A returned row is a candidate observation, not contemporary reachability or service availability.

https://learn.microsoft.com/en-us/windows/win32/api/iphlpapi/nf-iphlpapi-getipnettable

https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/arp

The ESET original publication behind existing REF-000988 is available on WeLiveSecurity, dated 2022-03-01. Its HermeticWizard section separates known-IP gathering from subsequent TCP connection attempts and optional /24 expansion. Its list mixes cache, enumeration, connection, and adapter APIs: it must not be described as an entirely local, entirely passive chain. Its subsequent port-order randomization concerns fingerprinting of connection traffic and does not by itself justify a host-knowledge child. The same original publication still contains the existing REF-000988 low-level disk-write facts, so upgrading source identity and extending its locator can preserve prior applicability.

https://www.welivesecurity.com/2022/03/01/isaacwiper-hermeticwizard-wiper-worm-targeting-ukraine/

Microsoft Sysmon distinguishes process creation, optional network-connection collection, and DNS-query events. DNS queries may produce Event 22 even when a cache supplies the answer. The absence of new target traffic cannot establish the absence of endpoint telemetry, and a command or API-entry record cannot establish a nonempty returned host list. Sysmon is not an assumed general file-read or cache-API-result provider.

https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon

Microsoft Event 4663 records exercised object rights subject to a matching SACL; it is stronger than a handle request, but a read-access event alone does not show which host identifiers an application parsed. Preserve host/process-lifetime mapping, hexadecimal PID normalization, and missing-telemetry states if the final analytic uses it.

https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4663

Microsoft's 1644 documentation states that events are generated for expensive, inefficient, or slow LDAP searches under configured diagnostic and threshold conditions. It is not a complete default directory-query audit. A directory analytic must declare validated instrumentation or its actual threshold-limited coverage; do not infer all query filters, returned names, or requester identity from an unrelated logon event.

https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/event1644reader-analyze-ldap-query-performance

Nmap's official list-scan description explicitly separates no packets to target hosts from default reverse-DNS traffic and discusses a stealth rationale. It is a valuable negative control: merely expanding a supplied range without responses is not evidence that remote hosts were discovered, and DNS-mediated host information cannot be labeled universally traffic-free. Keep it as a taxonomy comparison unless the final evidence establishes a defensible additional axis.

https://nmap.org/book/host-discovery-controls.html

## Primary acceptance questions for the returned handoff

Confirm evidence at the level of any proposed child, preserve attempt versus nonempty candidate result versus validation, and keep stale/invalid/hash limitations. Identify which branch consumes stock events, optional captured output, or a custom sensor that requires implementation and validation. Every consumed field must belong to a declared source. Do not require optional result material to recognize an attempt or manufacture names that the source never supplies. Review all confidence language in both languages, and preserve normal diagnostics, inventory, backup, and incident-response comparators. Human domain review and deployment validation remain separate from machine and browser acceptance.
