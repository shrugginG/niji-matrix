# Independent primary boundary review during research

No formal decisions, semantic IDs or canonical packages have been allocated for this delivery. The primary is reviewing adjacent ownership and source identities while the five independent candidate handoffs are produced.

## Existing canonical boundaries

NJT-0241 explicitly assigns dedicated information objects such as software inventory to their corresponding discovery technique. A Registry API does not require a second copy of the same information fact under general Registry exploration. NJT-0240 distinguishes current process instances from installed software, and its resident-query child requires positive evidence of both the actual query and task carrier. NJT-0180 covers driver identity and state; security-software discovery additionally requires an evidenced mapping from that driver to a security product.

NJT-0109 already owns target-condition comparisons and environment-derived decryption that control core malicious results. NJT-0122 owns analysis-environment classification followed by exit, withholding or a behavioral differential. Acquiring software, hardware, region or language facts alone does not establish those outcomes; neither may an existing guardrail be copied as a child of a new Discovery parent.

NJT-0242 separates remote-system candidates from current reachability, local configuration, current socket relationships and remote service facts. Reading preexisting local knowledge can avoid fresh target probes at that stage, but local interfaces and socket tables are not new versions of its host-candidate child merely because they are read locally. The five new parents need their own direct-result and trace-variable boundaries.

## Independently checked network contracts

GetAdaptersAddresses retrieves local adapter-associated addresses. Requested address family and flags select the returned view; unavailable addresses, an insufficient buffer or unsupported flags are not evidence of hidden configuration. The all-compartments flag is documented as reserved rather than a guarantee of cross-compartment visibility. Adapter facts do not establish a remote-host inventory, Internet reachability or a network's actual protection state.

https://learn.microsoft.com/en-us/windows/win32/api/iphlpapi/nf-iphlpapi-getadaptersaddresses

GetExtendedTcpTable returns endpoint tables selected by address family and table class. A size-query or insufficient-buffer result is not a returned endpoint list. Owner PID is the process associated with the socket, not necessarily the actor reading the table. LISTEN entries have no meaningful remote address/port; ports are stored in network byte order. The tuple, state, address family, interface scope and observation time must be preserved rather than labeling every row an active peer.

https://learn.microsoft.com/en-us/windows/win32/api/iphlpapi/nf-iphlpapi-getextendedtcptable

https://learn.microsoft.com/en-us/windows/win32/api/tcpmib/ns-tcpmib-mib_tcprow_owner_pid

The kernel's proc_net_tcp documentation includes listeners, connection state, uid and socket inode, not an automatic reader-to-owner identity mapping. TIME_WAIT can omit fields, and the interface is deprecated in favor of tcp_diag. Namespace-scoped views, cross-process permissions, asynchronous table changes and later inode/PID joins need explicit limits in any Linux analytic.

https://docs.kernel.org/networking/proc_net_tcp.html

## Provisional primary review questions

T1518 and T1082 researchers currently recommend retaining the parents with no independently evidenced native child. That outcome requires complete search and source-specific explanations rather than a copied zero-child template. Software inventory queries can trigger effects such as MSI consistency processing; local read-only intent does not establish absence of side effects. T1082's IaaS platform is present in the fixed workbook, but provider-declared image or architecture attributes must not be upgraded into observed guest kernel or patch state.

T1614 research has found original reporting of controller-side GeoIP queries after bot registration. Before admission, verify the registration-to-source-IP-to-service-result chain and distinguish post-compromise acquisition from pre-compromise targeting. A proxy, VPN or NAT egress location is not the victim device's physical location. Moving a query outside enterprise endpoint visibility may support NM-BT; NM-ST additionally requires actual spatiotemporal distribution and a defensible association-cost chain, not the existence of two computers alone. Enterprise-side absence of GeoIP traffic cannot prove controller-side lookup.

## Shared mitigation identity checks

MIT-000078's existing interpreter entry/capability/audit measures can be extended for a specific interpreted system-property query without changing those measures or prior applications. Its effect is on a controllable execution path, not a promise to prevent ordinary native getters. MIT-000139's IaaS inventory authority and read-audit measures can cover a new property-read application if provider/API scope and returned-fact limits are explicit. CloudTrail requests do not contain complete response inventories. Neither extension is approved merely by a similar title; each application will be read after the full handoff.

Both existing-control extensions must preserve all old measures and applications. Shared source publications such as REF-000626, REF-000639, REF-000230, REF-000525 and REF-000200 are to be reused or extended by their exact identity, with case reuse decided separately from publication reuse.
