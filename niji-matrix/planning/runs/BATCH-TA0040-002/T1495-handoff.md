# T1495 Firmware Corruption research handoff

`batch_ref: BATCH-TA0040-002`  
`work_item_ref: WORK-TA0040-T1495`  
`temporary_key_prefix: TA0040-T1495-`  
`status: research-only; integration pending`  
`baseline: Enterprise ATT&CK 19.1`  
`formal IDs allocated: none`

## Recommendation

**Adapt; medium confidence; zero formal Niji children.** Proposed bilingual admission rationale:

> 固件破坏通过未授权覆写或损坏平台及组件的非易失固件，使设备不能初始化、启动或继续提供功能，直接属于 TA0040 的可用性影响。Niji 应把正式范围适配为“观察链坍塌型固件破坏”：被破坏的固件同时支撑操作系统、设备管理代理或主机内传感器启动，故破坏结果不仅使设备不可用，也使同一设备无法报告变更后的固件状态和因果链。Win95/CIH 实际具有以随机数据覆写 Flash BIOS、使设备无法重启并可能需要更换 BIOS 或主板的能力；NIST SP 800-193 则把破坏性固件攻击后的保护、检测和独立恢复作为同一韧性问题。[E1][E2][E3]
>
> Firmware Corruption overwrites or damages nonvolatile platform or component firmware without authorization so a device cannot initialize, boot, or continue functioning, directly producing TA0040 availability impact. Niji should adapt the formal scope to Observation-Collapsing Firmware Corruption: the damaged firmware also supports startup of the operating system, device-management agent, or in-band sensor, so the outcome both removes device availability and prevents the same device from reporting post-change firmware state and causal lineage. Win95/CIH had the actual capability to overwrite Flash BIOS with random data, prevent reboot, and potentially require BIOS or motherboard replacement. NIST SP 800-193 treats protection, detection, and independent recovery after destructive firmware attack as one resiliency problem.[E1][E2][E3]

Parent behavior and destructive outcome are high-confidence. The Niji claim that the dual availability-and-observation collapse is a stealth-relevant design is **medium** because sources establish the causal effect but do not state that CIH selected firmware destruction specifically to conceal attribution. The outage is conspicuous; what becomes difficult is proving the firmware object, writer, and exact destructive change from the failed device's own telemetry.

## Required boundary convergence

- **Versus NJT-0097 Pre-OS Boot Persistence Control:** NJT-0097 owns firmware or boot state that still executes adversary code before the OS and restores access or hides activity beyond host measurement. T1495 owns corruption whose direct result is failure to initialize, boot, or operate. An unauthorized flash write can be an exposure for both, but the observed outcome decides the technique: functioning implant and restored access map to NJT-0097; destructive nonfunction maps to T1495. NJT-0097 explicitly excludes destructive firmware corruption causing only unavailability.[L1]
- **Versus NJT-0167 Network-Device System-Image Integrity Impairment:** NJT-0167 requires a network device to run or boot a modified image and show a security, observation, or recovery function difference while retaining its trusted device identity and service. T1495 applies when firmware or low-level image corruption prevents normal boot or service. A network-device image that runs maliciously is NJT-0167; an erased or invalid firmware image that bricks the device is T1495. Partial boot must be classified by the proven direct result rather than product label.[L2]
- **Versus NJT-0172 Restricted-Boot Defensive-Coverage Omission:** NJT-0172 requires a completed Safe Mode or equivalent restricted boot session in which expected defense components are absent and the attacker uses the window. T1495 has no valid restricted session: firmware initialization or normal boot fails. Safe Mode, recovery mode, and boot diagnostics are counterexamples unless an unauthorized firmware change is independently proven.[L3]
- **Versus T1561 Disk Wipe:** T1561 owns raw disk content, partitions, MBR, filesystem structures, and network-device data/configuration erase. T1495 owns code or critical data stored in firmware nonvolatile memory and consumed to initialize/manage hardware. A malicious firmware component that remains functional but issues disk erase commands supports T1561/T1485 for the data result; it supports T1495 only if the firmware itself is corrupted and the device becomes unusable.[E10]
- **Versus legitimate recoverable firmware update failure:** power loss, incompatible OEM packages, sticky flash bits, hardware failure, or other update errors can produce the same boot failure. A completed T1495 classification requires an attacker-controlled unauthorized write or package plus destructive consumption. A signed approved update that fails, records a nonzero status, rolls back to the last known good firmware, and boots normally is a strong counterexample; a rejected or rolled-back malicious attempt is exposure, not completed corruption.[E5][E7]
- **ATT&CK procedure examples:** Bad Rabbit's modified bootloader and other disk-resident boot code do not expand the Niji firmware object into MBR/EFI files; those remain disk/boot owners. TrickBoot demonstrates hardware identification, a signed raw-access driver, SPI writeability discovery, and the feasibility of erasing the BIOS region, but the analyzed module only checked writeability and did not itself perform a destructive flash write. It supports attacker prerequisites and detection design, not a completed corruption case.[E4]

## Taxonomy breadth review and zero-child justification

Fixed ATT&CK 19.1 child count: **0**. Represented dimensions: none. Breadth trigger: ordinary open-ended search. Proposed Niji child count: **0**; `subtechnique_taxonomy.coverage: none-justified`.

| Candidate stealth axis examined | Trace and defender-observation effect | Resolution |
| --- | --- | --- |
| Corruption collapses the same in-band boot and telemetry path needed to report it | Pre-impact write/package traces may exist, but after destructive consumption the OS, agent, and local readback disappear; defenders see heartbeat/POST failure and must use remote or hardware evidence | **Parent-core admission variable.** This defines the adapted parent and would be redundant as its sole child.[E2][E3][E8] |
| Direct flash/SPI write versus standard capsule or vendor update path | Direct access can expose a driver, flash tool, and raw operation; a staged capsule can resemble servicing and execute before OS takeover after reboot | **Evidence-deferred.** Platform docs establish both trace models, but no reviewed destructive incident proves attacker use of a legitimate capsule path for corruption or a distinct evasion intent.[E4][E6][E7] |
| Immediate erase versus staged write consumed on next reboot | Staging separates initial actor/process from later boot failure and changes the correlation window | **Evidence-deferred / adjacent execution timing.** CIH used a date trigger, but trigger gating is owned by execution-guardrail taxonomy and does not justify a firmware-specific child without separate defense value.[E2] |
| Platform firmware versus peripheral/component firmware | System firmware loss can suppress the whole host; peripheral firmware loss may leave host telemetry available | **Not-stealth-distinct by target type.** Component category changes blast radius and evidence coverage, not a stable NJS boundary. Component-only failures without observation collapse fall outside the adapted formal parent.[E1][E3] |
| Total erase versus partial corruption | Different amounts of damage can cause no boot, intermittent failure, or component loss | **Impact severity, not taxonomy.** Byte count and corruption pattern do not independently establish a stealth mechanism. |
| Corrupt active firmware versus corrupt recovery copy first | Destroying recovery material can delay trustworthy restoration | **Adjacent/deferred.** Direct recovery-copy impairment belongs to T1490; no conclusion-level T1495 source reviewed proves a stable two-stage firmware recovery-blinding pattern. |
| Host, network appliance, storage controller, GPU, or other device | Telemetry, update, and recovery channels vary by platform | **Implementation surface.** Device class and vendor cannot define NJS without a common attacker-controlled trace variable and sibling defense difference. |

Zero children are justified because the supported observation-collapse variable is the parent's admission boundary. The other axes are target classes, damage extent, transport mechanisms, timing controls, or adjacent recovery behavior. A future NJS requires an independently evidenced attacker variable, trace shift, prerequisites, defensive observation difference, and target-specific controls.

## Proposed parent content (`TA0040-T1495-PARENT`)

Name: **观察链坍塌型固件破坏 / Observation-Collapsing Firmware Corruption**  
Aliases: `Firmware Corruption`, `T1495`  
Summary:

> 攻击者破坏启动或组件初始化所依赖的非易失固件，使设备不可用，并同时切断设备自身对破坏后状态的观测与报告。
>
> Adversaries corrupt nonvolatile firmware required for boot or component initialization, making the device unavailable while severing its own observation and reporting of the post-corruption state.

### `definition_and_concept`

> 观察链坍塌型固件破坏是攻击者未授权覆写、擦除或损坏平台或组件非易失存储中的固件代码及启动关键数据，使硬件无法完成初始化、操作系统无法接管，或组件不能提供预期功能。直接对象是被硬件在上电或初始化阶段消费的固件状态及其可用性结果，不是固件文件名、更新工具、设备品牌或普通磁盘内容。[E1][E3]
>
> Observation-Collapsing Firmware Corruption is unauthorized adversary overwrite, erase, or damage to firmware code or boot-critical data in platform or component nonvolatile storage so hardware cannot initialize, the operating system cannot take control, or a component cannot provide its expected function. The direct object is firmware state consumed by hardware during power-on or initialization and the resulting availability loss, rather than a firmware filename, update tool, device brand, or ordinary disk content.[E1][E3]

> Niji 的附加概念条件是破坏同时移除同一设备的有效观察面：主机日志、EDR、管理代理或正常固件读回不能在变更后启动或响应，因而防守方只能从变更前远程日志、外部管理控制器、启动证明失败或离线硬件取证重建原因。明显停机不等于行为不可见；匿迹效果位于根因、写入者和固件差分难以由受损设备自证。[E2][E3][E8]
>
> Niji adds the condition that the corruption also removes an effective observation plane on the same device: host logs, EDR, management agents, or normal firmware readback cannot start or respond after the change, forcing defenders to reconstruct cause from pre-change remote logs, an external management controller, failed attestation, or offline hardware forensics. The outage is conspicuous; the stealth effect lies in the damaged device's inability to establish the root cause, writer, and firmware differential itself.[E2][E3][E8]

### `stealth_characteristics`

> 观察链坍塌型固件破坏把可观察链截断在固件消费边界。写入可能由运行中的高权进程、驱动、闪存工具或已暂存更新发起，但一旦损坏内容在重启或组件重新初始化时被消费，系统可在 OS、日志转发和端点传感器启动前停止。防守方看到的是电源存在但 POST/启动/心跳缺失、组件消失或固件更新失败，而不是一条由本机持续记录的“攻击者写入—固件差—不可用”完整链。[E1][E2][E5][E8]
>
> Observation-Collapsing Firmware Corruption truncates the observable chain at firmware consumption. A privileged process, driver, flash utility, or staged update can initiate the write while the system is running, but once corrupted content is consumed during reboot or component reinitialization, the platform can stop before the OS, log forwarder, and endpoint sensor start. Defenders see power without POST, boot, or heartbeat, a missing component, or firmware-update failure rather than one continuously recorded local chain from adversary write through firmware difference to unavailability.[E1][E2][E5][E8]

> 残余痕迹包括异常刷写进程、内核驱动加载及签名/hash、固件资源 GUID 和更新状态、变更批准、重启、TPM PCR 与 TCG 日志、外部 BMC/串口 POST 结果、资产心跳断点、已知良好映像和恢复时离线读回。硬件信任根、不同权远程证明和不可变变更日志会缩小盲区；只保留设备自报版本或本地 agent 会在破坏成功后失去独立证据。[E3][E6][E7][E8][E9]
>
> Residual traces include anomalous flashing processes, kernel-driver load with signature and hash, firmware-resource GUID and update status, change approval, reboot, TPM PCR and TCG logs, external BMC or serial POST results, asset-heartbeat discontinuity, known-good images, and offline readback during recovery. Hardware roots of trust, differently authorized remote attestation, and immutable change logs reduce the blind spot. Device self-reported version or a local agent alone loses independent evidence after successful corruption.[E3][E6][E7][E8][E9]

### `scope_boundary_definition`

> 纳入要求四项闭合：攻击者控制的未授权固件或启动关键数据变化；目标确属硬件消费的非易失固件对象；变化被上电、重启或组件初始化实际消费；设备或组件随之不可用且同一设备的正常观察或读回路径失效。只有刷写工具、可写 SPI、固件 hash 异常、更新包暂存或一次启动失败最多证明 exposure/anomaly，不能单独确认本技术。[E1][E3][E4]
>
> Inclusion requires four closed elements: an adversary-controlled unauthorized change to firmware or boot-critical data, a target that is truly a hardware-consumed nonvolatile firmware object, actual consumption of the change at power-on, reboot, or component initialization, and resulting device or component unavailability together with failure of the same device's ordinary observation or readback path. A flashing tool, writable SPI region, firmware-hash anomaly, staged update package, or one boot failure establishes exposure or anomaly at most and cannot alone confirm the technique.[E1][E3][E4]

> 能启动并在 OS 前执行恶意代码以恢复访问归 NJT-0097；网络设备实际运行被修改映像并继续提供服务归 NJT-0167；完成 Safe Mode/受限启动且防御组件缺席归 NJT-0172。磁盘扇区、MBR、分区、文件系统或设备配置数据擦除归 T1561。合法签名更新因电源、兼容性或硬件故障失败并由回滚恢复、厂商诊断模式、硬件自然失效和批准主板更换是反例；必须以 actor、package、签名、状态、证明和恢复结果排除。[E5][E7][E10][L1][L2][L3]
>
> Malicious code that boots before the OS and restores access belongs to NJT-0097. A network device that actually runs a modified image while continuing service belongs to NJT-0167. A completed Safe Mode or restricted boot with missing defenses belongs to NJT-0172. Erasure of disk sectors, MBR, partitions, filesystems, or device configuration data belongs to T1561. A legitimately signed update that fails through power, compatibility, or hardware error and recovers through rollback, vendor diagnostics, natural hardware failure, and approved motherboard replacement are counterexamples separated by actor, package, signature, status, attestation, and recovery result.[E5][E7][E10][L1][L2][L3]

### `application_scenarios_and_threat_model`

Application scenarios:

> 攻击者在已控制 Windows 主机并取得内核或硬件接口访问后，可加载具有 SPI/物理内存写能力的驱动，识别芯片组与 BIOS 写保护状态，再擦除或以无效内容覆写可启动固件区域；也可能滥用厂商更新权限暂存一个在重启时由固件消费的破坏性映像。Win95/CIH 证明随机内容覆写 Flash BIOS 能导致无法重启；TrickBoot 证明现代恶意模块可自动识别平台和 BIOS 区可写性，但其公开样本没有完成破坏写入。[E2][E4]
>
> After controlling a Windows host and obtaining kernel or hardware-interface access, an adversary can load a driver capable of SPI or physical-memory writes, identify the chipset and BIOS write-protection state, and erase or overwrite a bootable firmware region with invalid content. An adversary may also abuse vendor-update authority to stage a destructive image consumed by firmware at reboot. Win95/CIH establishes that random overwrite of Flash BIOS can prevent reboot. TrickBoot establishes modern malicious automation for platform identification and BIOS-region writeability, although its public sample did not complete the destructive write.[E2][E4]

Attacker model:

> 攻击者需要固件更新、SPI/flash、BMC/管理面或等价低层写权限，准确识别硬件型号、区域布局和写保护，并在目标内容被验证或回滚前提交变化。其可能借有效签名驱动取得硬件访问或利用错误更新权限；约束包括硬件写保护、签名 capsule、最低版本策略、独立恢复根和错误写入过早 brick 设备而失去控制与横向能力。[E3][E4][E5]
>
> The adversary needs firmware-update, SPI or flash, BMC or management-plane, or equivalent low-level write authority, accurate hardware model and region-layout identification, and the ability to commit the change before validation or rollback rejects it. A validly signed driver can provide hardware access, or weak update authority can be abused. Constraints include hardware write protection, signed capsules, lowest-version policy, an independent recovery root, and the risk that an incorrect write bricks the device prematurely and removes command or lateral capability.[E3][E4][E5]

Defender model:

> 防守方在破坏前能观察更新主体、包来源/hash/签名、进程与驱动、重启意图及固件资源状态；在启动边界能取得 TPM/TCG 度量；在设备失联后仍有不同权的 BMC、串口、网络、电源和集中日志，并保存按硬件 GUID/型号匹配的已知良好映像及离线读回能力。缺少硬件信任根、组件不在度量集合、BMC 同时失陷或固件不可读回时，只能把恶意破坏与合法更新/硬件故障作为竞争解释。[E3][E6][E7][E8]
>
> Before corruption, defenders can observe update principal, package source, hash and signature, processes and drivers, reboot intent, and firmware-resource status. At the boot boundary they can obtain TPM or TCG measurements. After the device disappears, they still have a differently authorized BMC, serial, network, power, and centralized logs, plus known-good images matched by hardware GUID or model and offline readback capability. Without a hardware root of trust, when a component is absent from measurements, the BMC is also compromised, or firmware cannot be read back, malicious corruption and legitimate update or hardware failure remain competing explanations.[E3][E6][E7][E8]

### `stealth_mechanisms`

- `mechanism_ref: NM-DO`; role `primary`; confidence `medium`.
- Summary: **破坏固件同时终止设备自身的启动后观察与读回 / Firmware corruption also terminates the device's own post-boot observation and readback**
- Analysis:

> 攻击者破坏硬件启动或初始化必须消费的固件；变化生效后，OS、管理代理、日志转发和本地固件查询无法启动或响应，原本可能连续记录写入与结果的观察链被固件消费边界切断。防守方虽然立即看到不可用，却难以从设备自身区分恶意写入、失败更新和硬件故障，也难以获得破坏后的完整固件差分，形成观测干扰。不同权远程日志、硬件证明、BMC/串口以及离线 flash 读回仍可恢复因果。公开案例证明结果链而未明确证明攻击者以毁坏观察为独立动机，故置信度为 medium。[E2][E3][E5][E8]
>
> The adversary corrupts firmware that hardware must consume to boot or initialize. Once the change takes effect, the OS, management agent, log forwarding, and local firmware query cannot start or respond, breaking an observation chain that could otherwise record the write and result across the firmware-consumption boundary. Defenders see unavailability immediately but have difficulty using the device itself to distinguish a malicious write from failed update or hardware fault and to acquire a complete post-corruption firmware differential, producing Disruption of Observation. Differently authorized remote logs, hardware attestation, BMC or serial output, and offline flash readback can still recover causality. Public evidence establishes the result chain without explicitly proving destruction of observation as a separate actor motive, so confidence is medium.[E2][E3][E5][E8]

Rejected mechanisms: `NM-BT` is not assigned merely because firmware sits below the OS; NJT-0097 owns functioning below-OS persistence outside host observation, while T1495 produces conspicuous nonfunction. `NM-FD` is deferred because no reviewed destructive incident proves a malicious corrupt image was made to resemble an approved update package. `NM-ST` is deferred because date triggers or delayed reboot separate time but are execution gating or operations scheduling without a firmware-specific dilution conclusion.

### `subtechnique_taxonomy`

> 当前 taxonomy 为 `none-justified`。观察链坍塌是本父技术的准入变量，不能复制成与父级同义的唯一子技术。系统/组件固件、主机/网络设备、SPI/厂商 capsule、全擦除/局部损坏和立即/重启生效分别是目标、平台、传输、严重度或消费时机，不自动形成独立匿迹兄弟项。
>
> The current taxonomy is `none-justified`. Observation collapse is the parent's admission variable and cannot be duplicated as a sole child synonymous with the parent. System versus component firmware, host versus network device, SPI versus vendor capsule, total erase versus partial damage, and immediate versus reboot-time effect are target, platform, transport, severity, or consumption-time distinctions and do not automatically form independent stealth siblings.

> 标准更新路径伪装、先毁恢复副本和跨设备渐进提交是开放研究轴，但当前缺少实际破坏案例、稳定 trace boundary 或独立防御差异。延迟触发还与执行护栏重叠，恢复副本破坏与 T1490 重叠。零子项保留这些证据限制，避免按设备类型或 ATT&CK 例子强制拆分。
>
> Standard-update-path camouflage, prior destruction of recovery copies, and gradual cross-device commit remain open research axes, but current evidence lacks an actual destructive case, stable trace boundary, or independent defensive difference. Delayed triggering also overlaps execution guardrails, while recovery-copy destruction overlaps T1490. Zero children preserve these evidence limits and avoid forced partitions by device type or ATT&CK example.

### `research.limitations`

> Win95/CIH 直接支持 Flash BIOS 随机覆写和设备无法重启，NIST 直接支持破坏性固件攻击可造成永久不可用或需要原厂重编程以及保护—检测—恢复模型。TrickBoot 的公开分析只证明平台识别、SPI BIOS 可写性测试和把模块改造成实际擦除器的可行性，不能作为已完成 T1495 案例。Windows UEFI、ESRT、PCR 和 Sysmon 字段只适用于相应配置；许多外围设备、旧平台和网络设备没有可导出 readback、测量或更新状态。没有攻击者控制证据时，恶意固件破坏不能从一次 no-boot 结论性地区分于电源、硬件或更新故障。[E2][E3][E4][E5]
>
> Win95/CIH directly supports random Flash BIOS overwrite and inability to reboot. NIST directly supports destructive firmware attack causing permanent inoperability or manufacturer reprogramming and the protect-detect-recover model. Public TrickBoot analysis establishes only platform identification, SPI BIOS writeability testing, and feasibility of converting the module into an eraser, not a completed T1495 case. Windows UEFI, ESRT, PCR, and Sysmon fields apply only where configured, and many peripherals, legacy platforms, and network devices expose no readback, measurement, or update status. Without evidence of adversary control, one no-boot event cannot conclusively distinguish malicious firmware corruption from power, hardware, or update failure.[E2][E3][E4][E5]

## Evidence and shared-library candidates

Suggested temporary claims:

- `TA0040-T1495-CLM-ADAPT`: T1495 is adapted to firmware corruption that causes availability loss and collapse of the same device's in-band observation/readback.
- `TA0040-T1495-CLM-OBSERVATION-COLLAPSE`: consumption of corrupted boot/initialization firmware prevents OS and sensor startup, breaking causal telemetry at the firmware boundary.
- `TA0040-T1495-CLM-BOUNDARY`: functioning pre-OS implants, running modified network images, restricted boot, raw disk wipe, and recoverable approved update failures have separate owners or remain counterexamples.
- `TA0040-T1495-CLM-ZERO-CHILD`: target class, write transport, corruption extent, and commit timing do not pass the Niji child gates on current evidence.

Suggested cases: **none**. Microsoft Win95/CIH is a software-family behavior reference rather than a sufficiently scoped victim/campaign event for the canonical Case identity. TrickBoot is a capability/precondition report and must not be upgraded to an observed destructive case.

### Evidence ledger

| Key | Primary source and locator | Supported conclusion and limit |
| --- | --- | --- |
| E1 | MITRE ATT&CK 19.1 [T1495 Firmware Corruption](https://attack.mitre.org/versions/v19/techniques/T1495/), description and no-subtechnique inventory | Parent firmware object, inoperable/unable-to-boot outcome, Impact mapping; does not prove Niji mechanism. |
| E2 | Microsoft Security Intelligence, [Win95/CIH](https://www.microsoft.com/security/portal/Threat/Encyclopedia/Entry.aspx?Name=Win95%2FCIH), payload and symptoms | Random Flash BIOS overwrite, inability to restart, and possible BIOS/motherboard replacement; no specific victim case or explicit stealth intent. |
| E3 | Existing `REF-000194`, [NIST SP 800-193](https://doi.org/10.6028/NIST.SP.800-193), abstract and Sections 3–4 | Exact reuse. Destructive firmware impact plus protection, detection, and recovery principles. |
| E4 | Eclypsium/Advanced Intelligence, [TrickBoot](https://eclypsium.com/threat-reports/trickboot/), technical analysis | Signed raw-access driver, platform/SPI writeability discovery, and destructive feasibility; explicitly not actual corruption by analyzed module. |
| E5 | Microsoft Learn, [Seamless crisis prevention and recovery](https://learn.microsoft.com/en-us/windows-hardware/drivers/bringup/seamless-crisis-prevention-and-recovery), post-install validation and rollback | Legitimate update-failure counterexamples, integrity validation, rollback, and possible unusable crisis. |
| E6 | Microsoft Learn, [Windows UEFI Firmware Update Platform](https://learn.microsoft.com/en-us/windows-hardware/drivers/bringup/windows-uefi-firmware-update-platform), capsule/ESRT flow | Firmware resource GUID, package/capsule delivery and reboot-time consumption path; not adversary evidence. |
| E7 | Microsoft Learn, [QueryVersionAndStatus.ps1](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/query-version-and-status-ps1-script?view=windows-11), registry constants | `FirmwareResources\{GUID}`, `LastAttemptVersion`, and `LastAttemptStatus` fields for an implementable Analytic. |
| E8 | Microsoft Learn, [Control the health of Windows devices](https://learn.microsoft.com/en-us/windows/security/operating-system-security/system-security/protect-high-value-assets-by-controlling-the-health-of-windows-10-based-devices), measured boot | PCR/TCG measurements of firmware and boot components plus remote health attestation. |
| E9 | Microsoft Learn, [Sysmon events](https://learn.microsoft.com/en-us/windows/security/operating-system-security/sysmon/sysmon-events), Event 6 | Driver-load event with signature and hash information; does not prove driver hardware capability. |
| E10 | MITRE ATT&CK 19.1 [T1561 Disk Wipe](https://attack.mitre.org/versions/v19/techniques/T1561/), object and child descriptions | Raw disk, MBR/structure, and device data/configuration boundary. |
| L1 | Existing `NJT-0097 Pre-OS Boot Persistence Control` | Formal local owner for functioning malicious boot/firmware state that restores access or lies outside measurement. |
| L2 | Existing `NJT-0167 Network-Device System-Image Integrity Impairment` | Formal local owner for modified network-device code that actually runs while the trusted device continues service. |
| L3 | Existing `NJT-0172 Restricted-Boot Defensive-Coverage Omission` | Formal local owner for completed restricted boot and missing defensive components. |

## Exact shared-library lookup and resolution advice

Required `library_lookup.py` searches were run for `firmware corruption`, `firmware resiliency`, `boot integrity recovery`, `firmware attestation`, `firmware update status`, `raw firmware write`, `Win95 CIH`, `TrickBoot`, `Seamless crisis prevention and recovery`, `Measured Boot PCR firmware`, `Sysmon driver load`, `T1495 Firmware Corruption`, and `pre OS boot control lineage`.

- **Reuse `REF-000194` exactly.** Its DOI, NIST identity, and firmware-resiliency conclusions are unchanged.[E3]
- **Extend `MIT-000077`** with one T1495 application if admitted. Its control concept and measures already cover firmware write protection, complete measurement/readback, trusted sources, and an independent recovery root. T1495 needs target-specific use/effect/limitations, not a duplicate mitigation.
- `DET-000077` and `NJA-000056` are close but detect pre-OS persistence by joining changes to a booted malicious runtime or external image. T1495 requires a different terminal branch: firmware change followed by absent attestation, failed POST/boot, lost heartbeat, and hardware/offline recovery. Recommend **create** a new DET/NJA rather than extend an Analytic whose logic, required outcome, windows, and tuning differ.
- `MIT-000107 Raw Storage Access Governance` is a disk/raw-storage control and does not replace firmware recovery-root measures. Do not reuse it solely because a driver exposes low-level writes.
- No exact match was returned for the fixed T1495 page, Win95/CIH, TrickBoot, Microsoft crisis-recovery, UEFI/ESRT status, measured-boot, or Sysmon Event 6 sources. Recommend **create** new References after main-agent URL lookup against the refreshed catalog.
- No existing Claim, Case, DET, NJA, or Relationship has the same semantic identity as observation-collapsing destructive firmware outcome. Claims and DET/NJA: `create`; Cases: `defer`; MIT: `extend MIT-000077`.

## Defense design

### Detection Strategy `TA0040-T1495-DET-FIRMWARE-WRITE-BOOT-FAILURE-LINEAGE`

Name: **固件写入—启动失败—观察中断谱系 / Firmware Write–Boot Failure–Observation Loss Lineage**. Objective: join a firmware-capable writer or staged update with firmware version/status and measured-boot evidence, then distinguish a destructive no-boot/observation-loss result from an approved failed update or natural hardware failure. Domain `enterprise`; first Analytic is Windows platform firmware only. Network appliances and peripheral firmware require separate vendor field evidence.

### Detection Analytic `TA0040-T1495-NJA-WINDOWS-FIRMWARE-CORRUPTION-OUTCOME`

**Data requirements and real fields**

1. `firmware-asset-baseline`, channel asset/firmware inventory: `device_id`, `hardware_id`, `manufacturer`, `model`, `component_or_resource_guid`, `firmware_type`, `current_version`, `known_good_hash`, `approved_signer`, `measurement_coverage`, `write_protection_state`, `recovery_image_id`, `owner`.
2. `firmware-change-approval`, channel change/package management: `change_id`, `device_id`, `resource_guid`, `package_id`, `package_hash`, `signer`, `source`, `operator_id`, `window_start`, `window_end`, `expected_version`, `expected_reboot_count`, `rollback_image_id`, `status`.
3. `process-and-driver-lineage`, channels Microsoft Defender XDR `DeviceProcessEvents` plus Sysmon Event 6: process fields `Timestamp`, `DeviceId`, `DeviceName`, `FileName`, `FolderPath`, `ProcessCommandLine`, `ProcessId`, `ProcessUniqueId`, `AccountSid`, `AccountName`, `InitiatingProcessUniqueId`, `SHA1`, `ReportId`; driver fields `UtcTime`, `ImageLoaded`, `Hashes`, `Signed`, `Signature`, `SignatureStatus`. Event 6 proves a driver loaded, not that it wrote firmware.[E9]
4. `windows-firmware-resource-status`, channel `HKLM\SYSTEM\CurrentControlSet\Control\FirmwareResources\{RESOURCE_GUID}`/ESRT: `timestamp`, `device_id`, `resource_guid`, `FirmwareVersion`, `LastAttemptVersion`, `LastAttemptStatus`, `Policy`. Preserve before and after state centrally.[E7]
5. `measured-boot-attestation`, channel TPM/TCG and remote health attestation: `timestamp`, `device_id`, `boot_id`, `pcr_index`, `pcr_value`, `tcg_event_type`, `component_identifier`, `measurement_hash`, `attestation_result`, `quote_nonce`. PCR 0/firmware interpretation depends on platform measurement policy; never treat a generic pass as coverage of every component.[E8]
6. `out-of-band-boot-health`, channel BMC/serial/power/network monitoring: `timestamp`, `device_id`, `management_controller_id`, `power_state`, `post_code`, `boot_phase`, `console_status`, `hardware_health`, `network_link`, `host_heartbeat`, `last_successful_boot_id`. Channel and fields require vendor validation; BMC must have different authority from the host.
7. `offline-firmware-readback`, channel incident recovery: `timestamp`, `device_id`, `component_or_resource_guid`, `acquisition_method`, `reader_id`, `image_hash`, `signature_result`, `comparison_baseline`, `validation_result`, `chain_of_custody_id`.

**Logic**

1. Create an approved update transaction keyed by device, resource GUID, package hash, signer, operator, window, expected version, and reboot count. Flag a firmware flasher/capsule staging or hardware-access driver outside that exact transaction. A known flash utility or valid driver signature is context, never an allowlist.
2. Within **fifteen minutes**, correlate a suspicious process/driver sequence with firmware package staging, raw firmware audit if available, or a change to `LastAttemptVersion/Status`. Direct `DeviceIoControl`/SPI operations may require product-specific API telemetry; when absent, record the chain as exposure rather than inventing a write field.
3. From staging or suspected write through the **next two boots or twenty-four hours**, join reboot, ESRT current/last-attempt state, PCR/TCG measurements, attestation result, and external boot health. Escalate to high confidence when the prior chain is followed within **fifteen minutes of reboot** by power present plus failed POST/boot or absent attestation/host heartbeat, with no approved recovery state.
4. Treat `LastAttemptStatus != 0` as an update failure signal, not malicious proof. If the transaction is approved, package/signature match, firmware rolls back to the known-good version or measurement, and the device successfully boots, classify as legitimate recoverable failure. If the device remains unusable, preserve the ambiguity until offline readback or writer evidence distinguishes malicious corruption from hardware/power crisis.[E5][E7]
5. On recovery, compare offline image hash/signature and damaged region with the model/GUID-specific known-good image. Do not power-cycle or reflash before preserving accessible remote and hardware evidence unless life/safety or service-restoration priority requires it.
6. Aggregate multiple devices sharing writer hash, package ID, signer anomaly, operator, management source, or failed measurement over **one hour** for campaign severity. Thresholds must be derived by hardware fleet and update process; one critical out-of-window firmware write plus boot collapse can be sufficient.

**Observables**

- An unusual or revoked hardware-access driver loads, a privileged process stages or invokes firmware tooling outside change control, then the next boot lacks attestation and host heartbeat while BMC power remains present.
- `LastAttemptVersion` changes to an unapproved version/package, PCR or offline readback differs from the known-good resource, and the device fails before OS telemetry starts.
- Several identical hardware models lose POST/boot after the same package, operator, source, or writer hash, inconsistent with independent hardware failure.

**Correlation dimensions:** `device_id`, `hardware_id/model`, `component_or_resource_guid`, `package_id/hash/signer`, `operator/account`, `process_unique_id`, `driver_hash/signature`, `change_id`, `boot_id`, `pcr_index/value`, `management_controller_id`, `post_code`, `offline_image_hash`, `time`.

**False positives:** approved OEM/enterprise firmware rollout; power loss during flash; hardware replacement; incompatible but signed firmware; lab recovery/reflash; BIOS reset; natural flash wear or motherboard failure; TPM clearing or legitimate boot-chain changes; an update rejected and automatically rolled back.

**Blind spots:** external hardware programmer with no host trace; firmware/flash region absent from TPM measurements; unavailable or attacker-controlled BMC; direct SPI writes invisible to endpoint sensors; signed vulnerable driver allowed by policy; device self-report forged before failure; no model-specific known-good image; destroyed device cannot be read back; component firmware failure that leaves no whole-host heartbeat change; clocks and boot IDs lost across reset.

**Tuning:** baseline by hardware ID, resource GUID, firmware version, signer, expected PCR/TCG measurements, update method, and reboot count. Bind exceptions to package hash, operator, source, device scope, window, and rollback plan. Test a successful update, a rejected capsule, automatic rollback, power-loss recovery, and offline readback on each supported model. Maintain an explicit measurement-coverage map and keep the ambiguous hardware-failure branch instead of suppressing all approved-window failures.

### Mitigation reuse: extend `MIT-000077 Boot Integrity Component Attestation and Trusted Recovery`

The existing measures remain semantically unchanged: `boot-write-protection`, `complete-measurement-map`, `trusted-boot-source`, and `independent-firmware-recovery`. Proposed T1495 application:

Use:

> 对观察链坍塌型固件破坏，以硬件写保护和只允许 JIT 更新身份、签名且型号/GUID 匹配的厂商包限制平台及组件 firmware；把每个组件是否进入 measured boot/attestation、是否可 readback 和恢复根位置登记在独立清单。固件异常或 no-boot 后不信任受损 OS 自报，从 BMC/硬件根保全状态，以离线已知良好映像重刷并在恢复业务前验证多次启动度量、组件功能和设备凭据轮换。
>
> For Observation-Collapsing Firmware Corruption, use hardware write protection and allow only JIT update identities and signed vendor packages matched to model and resource GUID for platform and component firmware. Record independently whether each component enters measured boot or attestation, supports readback, and has a recovery root. After a firmware anomaly or no-boot outcome, do not trust the damaged OS self-report; preserve state from BMC or a hardware root, reflash from an offline known-good image, and verify multiple boot measurements, component function, and device-credential rotation before restoring business service.

Expected effect:

> 未授权固件写入更可能在提交前被硬件或签名策略拒绝；破坏发生时，不同权度量、远程状态和离线恢复根保留设备自身失联后仍可使用的证据与恢复路径，缩短不可用并提高恶意写入与失败更新的可区分性。
>
> Unauthorized firmware writes are more likely to be rejected by hardware or signing policy before commit. If corruption occurs, differently authorized measurements, remote state, and an offline recovery root preserve evidence and a recovery path after the device loses in-band visibility, shortening outage and improving distinction between malicious write and failed update.

Limitations:

> 旧设备可能没有写保护、Secure/Measured Boot、可信 readback、双镜像或 BMC；供应商签名链、更新服务器或硬件根失陷仍可让恶意映像通过。错误重刷会永久 brick 或丢失配置，恢复前取证与业务复原存在时间冲突；没有攻击者控制证据时，缓解无法把所有固件危机归因为攻击。
>
> Legacy devices may lack write protection, Secure or Measured Boot, trusted readback, dual images, or BMC. Compromise of a vendor signing chain, update server, or hardware root can still admit a malicious image. Incorrect reflashing can permanently brick the device or lose configuration, creating tension between evidence preservation and service restoration. Without evidence of adversary control, the mitigation cannot attribute every firmware crisis to attack.

Resolution: **extend**, not create. MIT-000077 already has the identical overall control purpose and measures; only the T1495 target application, expected destructive-impact effect, and limits are new. The primary Agent should add one unique `applications[].target_ref` after formal NJT allocation.

## Content-depth and integration checks

- Parent draft covers definition, direct purpose, observation collapse, residual traces, inclusion, exclusions, normal update/hardware counterexamples, application, attacker requirements, defender visibility, supported mechanism, zero-child taxonomy, evidence, limitations, and defense at NJT-0001 field responsibility depth.
- No NJS is proposed. Record fixed child count zero and the open-axis table in planning metadata only.
- Preserve the `medium` mechanism confidence and the overt-outage limitation. Do not claim that obvious unavailability is itself hidden.
- Use Win95/CIH as a Reference/Claim source, not a fabricated victim Case. Keep TrickBoot limited to capability and prerequisite evidence.
- Canonical references should reuse `REF-000194`; create exact-source objects only after refreshed URL lookup. Extend MIT-000077 only after target allocation; DET/NJA remain new because terminal logic differs from pre-OS persistence.
- Keep Windows/UEFI data fields platform-scoped. Network device, Linux, macOS, BMC, storage controller, and peripheral firmware need vendor-specific schemas before formal Analytic expansion.
- If primary review rejects observation collapse as an intentional stealth-relevant effect, fallback is **exclude** rather than generic retention of all firmware failures.
- If integrated, lifecycle remains `review` after schema, quality, bundle, bilingual Web/API, duplicate, and human-content gates. This handoff allocates no canonical IDs and changes no formal or shared object.
