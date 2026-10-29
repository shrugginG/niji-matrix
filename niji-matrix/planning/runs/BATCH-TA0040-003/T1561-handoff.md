# T1561 research handoff — BATCH-TA0040-003

Research staging only. All proposed new objects use temporary prefix `TA0040-T1561-`. No formal ID is allocated, and no canonical matrix, decision, shared library, tactic plan, batch brief, reservation, or integration summary is modified.

## Admission recommendation

**Candidate:** ATT&CK Enterprise 19.1 T1561 Disk Wipe / 磁盘擦除. **Recommendation:** `adapt`. **Parent confidence:** `high`. **Fixed ATT&CK children:** T1561.001 Disk Content Wipe and T1561.002 Disk Structure Wipe. `original_attack_subtechniques_imported: false`. Existing `REF-000898` is the exact canonical fixed-baseline parent reference and should be reused.

**准入理由（中文）：** T1561 的直接行为是攻击者在块设备、物理磁盘或卷层覆写内容或破坏引导、分区和文件系统结构，使系统、卷或数据集整体不可用。HermeticWiper、ExPetr 和 GigaWiper 等在野分析直接证明这种行为及不可启动、不可恢复结果。Niji 应保留块/介质级直接对象，但将正式匿迹问题改写为攻击者如何用极少关键元数据写入产生远大于写入量的损失，或如何把不可恢复擦除呈现为可支付、可解密的勒索事件，从而削弱文件级监控、写量阈值和事件响应分类。

**Admission rationale (English):** T1561 directly covers adversary overwrite of block-device, physical-disk, or volume content or destruction of boot, partition, and file-system structures so a system, volume, or data set becomes broadly unavailable. Field analyses of HermeticWiper, ExPetr, and GigaWiper directly establish the behavior and unbootable or unrecoverable outcome. Niji should retain the block/media direct object while adapting the formal stealth question to minimal writes against critical metadata that cause loss disproportionate to write volume, and presentation of irreversible wiping as payable, decryptable ransomware, weakening file-level monitoring, write-volume thresholds, and incident classification.

## Mandatory adjacent boundaries

- **NJT-0156 Data Destruction / 数据销毁:** NJT-0156 owns deletion or overwrite of identifiable files, objects, or useful content through filesystem/object semantics. T1561 requires block/volume/physical-disk mutation or destruction of metadata governing a medium as a whole. A wiper may do both: HermeticWiper overwrote MBR/MFT and also recursively wiped files. Record each direct object separately rather than deciding from the malware family name.
- **NJT-0188 Firmware Corruption / 固件破坏:** NJT-0188 changes firmware or low-level component code/configuration so the hardware cannot initialize or operate. T1561 changes storage content/structure while the device firmware can remain intact. A signed partition driver or NVMe sanitize command does not imply firmware corruption; malicious firmware that falsifies or destroys media state requires separate firmware evidence.
- **NJT-0186 Inhibit System Recovery / 抑制系统恢复:** destruction of backups, snapshots, recovery partitions, or recovery keys in their recovery role belongs to NJT-0186. Wiping the primary production disk/volume belongs to T1561. If one action wipes both primary and recovery media, map object role and record both outcomes. Disabling VSS before a disk wipe is an adjacent recovery-inhibition step, not part of the Disk Wipe child boundary.
- **NJT-0108 Raw Storage View Access / 原始存储视图访问:** NJT-0108 ends at reading or viewing data through a raw/alternate storage path and may produce no mutation. T1561 requires destructive write/discard/initialization and availability outcome. A raw handle, `DeviceIoControl`, block-device open, or signed storage driver is a precursor/implementation until destructive sectors and result are proven.
- **NJT-0157 Data Encrypted for Impact:** reversible or attacker-key-controlled ciphertext denying current reading belongs to NJT-0157. Raw disk/metadata destruction or encryption with no recoverable key can belong to T1561 when the disk/volume is the direct object. The ransom label does not decide.
- **Ordinary formatting/decommission / 正常格式化与退役:** approved imaging, partition conversion, filesystem creation, secure decommission, repair, and test wipes produce the same raw writes. Classification requires asset owner, change record, device identity, approved tool/identity, expected replacement state, and absence or presence of malicious successor impact. A format command alone is not evidence.

## ATT&CK-child breadth review and coverage resolutions

ATT&CK's two children divide whether content or disk structure is wiped. Niji uses them only as breadth context. Open-ended research examined critical-metadata write concentration, recovery-pretext camouflage, trusted-driver I/O delegation, overwrite-pattern distortion, delayed sanitize/delegated device execution, and cross-disk selective preservation.

| ATT&CK 19.1 child | Represented dimension | Planning-only resolution | Niji reasoning |
|---|---|---|---|
| T1561.001 Disk Content Wipe | Broad block/content overwrite | `parent-core`; contributes to camouflage candidate | Content is an object layer, not a stealth variable. Full/multi-pass overwrite remains parent core. A destructive disk operation presented as recoverable ransomware can contribute to the pretext child. |
| T1561.002 Disk Structure Wipe | MBR/GPT/partition/file-system metadata destruction | `niji-variable-candidate` plus `parent-core` | HermeticWiper shows that corrupting the first 512-byte MBR can already make a device unbootable. The Niji variable is low write coverage relative to whole-volume impact, not the ATT&CK structure label. Full structure reinitialization remains parent core. |

**Proposed Niji children:** `TA0040-T1561-CHILD-METADATA` Critical-Metadata Minimal-Write Destruction / 关键元数据最小写入式毁坏; `TA0040-T1561-CHILD-PRETEXT` Recoverability-Pretext Wipe Camouflage / 可恢复性话术伪装式擦除. They remain separable: the first changes *where and how much is written*; the second changes *how irreversible impact is presented*. A minimal MBR overwrite can occur without a ransom story, and a ransomware-pretext wipe can overwrite the full disk.

### Other axes

| Axis | Resolution | Reason |
|---|---|---|
| Signed/benign storage-driver delegation | `implementation` / adjacent raw-storage control | HermeticWiper proves observation is deferred into driver/IOCTL paths, but driver choice is not a stable sibling; it implements raw destructive writes and overlaps driver trust/governance. |
| Overwrite-pattern signature distortion | `evidence-deferred` | Microsoft assesses GigaWiper's randomized first byte in otherwise zero-filled buffers may avoid full-zeroing detection. One observed implementation and inferred intent are insufficient for a stable child, but defense should avoid zero-pattern-only rules. |
| Device-internal sanitize/secure erase | `evidence-deferred` | Asynchronous device execution could separate one command from media loss, but reviewed sources do not establish a malicious field case and distinct Niji boundary. |
| Selective preservation of boot/system drives | `adjacent-technique` | Attacker-controlled preservation predicates belong to NJT-0117; disk wipe records the disks actually destroyed. |
| Slow or staggered block overwrite | `evidence-deferred` | No conclusion-level source establishes intentional write pacing for stealth and a distinct detection method. |

## Proposed parent field content

**Name / 名称:** 磁盘擦除 / Disk Wipe.

**Summary / 摘要:** 攻击者在块或磁盘层破坏内容和关键结构，并通过少量关键写入或可恢复性伪装降低早期识别和正确响应。 / Adversaries destroy block-level content and critical disk structures while minimal critical writes or recoverability pretext reduce early recognition and correct response.

### Definition and concept / 定义与概念

中文：磁盘擦除是攻击者直接写入、丢弃、重新初始化或不可恢复地变换物理磁盘、块设备或卷，使其内容、引导状态、分区关系或文件系统元数据不能再支持原有系统与数据用途。直接对象是介质级可用性和结构，而非单个路径对象；文件名仍存在于缓存、设备仍被枚举或硬件仍通电，都不否定磁盘状态已失效。

English: Disk Wipe is adversary writing, discarding, reinitializing, or irreversibly transforming a physical disk, block device, or volume so its content, boot state, partition relationships, or file-system metadata can no longer support the original system and data purpose. The direct object is media-level availability and structure rather than one path object. Cached filenames, continued device enumeration, or powered hardware do not negate invalid disk state.

中文：概念锚连接写入主体/控制路径、设备与块范围、写入/丢弃结果、分区/文件系统 before/after 状态、挂载或启动失败及资产用途。写零、写随机数、加密、格式化、IOCTL、驱动和重启只是实现。只有块/结构状态与合法可用性结果共同存在时，才能区别真实擦除、企图和普通维护。

English: The concept joins writer or control path, device and block range, write or discard outcome, before/after partition or file-system state, mount or boot failure, and asset purpose. Zero fill, random fill, encryption, format, IOCTL, driver, and reboot are implementations. Block or structure state and legitimate availability outcome together distinguish a completed wipe, attempt, and ordinary maintenance.

### Stealth characteristics / 匿迹特性

中文：关键引导、分区和文件系统元数据占介质比例很小，但决定整个卷能否定位和解释。攻击者集中写入这些区间时，文件级删除/修改遥测和全盘写量阈值可能没有与结果相称的信号；原始设备句柄、驱动/IOCTL、扇区偏移与元数据校验才保留因果。HermeticWiper 对首个 512 字节 MBR 的破坏即足以造成启动失败，随后更广泛写入并不改变这一不对称。

English: Critical boot, partition, and file-system metadata occupies a small fraction of media but determines whether the whole volume can be located and interpreted. When an adversary concentrates writes on those extents, file-level delete or modify telemetry and full-disk write-volume thresholds need not produce signal proportional to the result. Raw-device handle, driver or IOCTL, sector offset, and metadata validation retain causality. HermeticWiper corruption of the first 512-byte MBR was already sufficient for boot failure even though broader writes followed.

中文：攻击者还可借勒索画面、安装 ID、扩展名、加密流程或解密承诺，把不可恢复擦除呈现为普通密钥控制事件。防守方可能先追踪支付/解密而延迟隔离、保全介质和裸机重建。原始块写入、关键元数据损伤、密钥/ID生成逻辑和恢复函数可达性仍能揭示话术与真实状态的矛盾。

English: The adversary can also use a ransom screen, installation ID, extension, encryption workflow, or decryption promise to present irreversible wiping as an ordinary key-custody incident. Defenders can pursue payment or decryption first and delay isolation, media preservation, and bare-metal rebuild. Raw block writes, critical metadata damage, key or ID generation logic, and reachability of recovery functions expose the conflict between presentation and actual state.

### Scope boundary definition / 范围边界界定

中文：纳入针对物理盘、块设备或卷的未授权写入/丢弃/初始化，并有分区表、引导记录、文件系统结构、块内容、挂载/启动或业务数据集失效证据。只加载磁盘驱动、枚举盘、打开原始设备、读取块或发出失败 IOCTL 是前置/企图。合法格式化与退役必须有匹配 owner、范围、工单、工具、时间和预期新状态。

English: Include unauthorized write, discard, or initialization of a physical disk, block device, or volume with evidence of partition-table, boot-record, file-system structure, block-content, mount or boot, or business-data-set failure. Driver load, disk enumeration, raw-device open, block read, or failed IOCTL is precursor or attempt. Legitimate format and decommission require matching owner, scope, work record, tool, time, and expected new state.

中文：文件/对象路径级损失归 NJT-0156；固件代码或初始化组件损坏归 NJT-0188；恢复角色对象损失归 NJT-0186；只读原始视图归 NJT-0108。密文可由攻击者/组织掌握的密钥恢复时归 NJT-0157；未保存密钥且直接破坏磁盘状态时可归本技术，但必须验证介质对象和不可恢复性。

English: File or object path loss belongs to NJT-0156, firmware code or initialization-component damage to NJT-0188, loss of recovery-role objects to NJT-0186, and read-only raw views to NJT-0108. Ciphertext recoverable under an adversary or organizational key belongs to NJT-0157. Encryption with no retained key can belong here when it directly destroys disk state, but media object and irrecoverability require validation.

### Application scenarios / 应用场景

中文：攻击者取得本地管理员、内核/驱动加载或原始设备写权限后，可枚举物理盘并覆写 MBR、GPT、MFT、文件系统位图/日志或完整块内容，使主机无法启动或卷无法挂载。HermeticWiper 通过合法 EaseUS 驱动和 `DeviceIoControl` 操作低层磁盘；GigaWiper 重新初始化分区元数据并按大块覆写物理盘。另一个场景是 ExPetr 用勒索屏幕和安装 ID 表示可解密，但 ID 为随机数据，攻击者无法恢复磁盘。

English: After obtaining local administrator, kernel or driver-load, or raw-device write authority, an adversary can enumerate physical disks and overwrite MBR, GPT, MFT, file-system bitmap or log, or broad block content, making the host unbootable or volume unmountable. HermeticWiper used legitimate EaseUS drivers and `DeviceIoControl` for low-level disk operations, while GigaWiper reinitialized partition metadata and overwrote physical disks in large chunks. In another scenario, ExPetr presented a ransom screen and installation ID as if decryption were possible, while the ID was random data and could not restore the disk.

### Attacker model / 攻击方模型

中文：攻击者需要原始设备写入、存储管理 IOCTL、驱动加载、root/管理员或等价存储控制权限，并了解目标盘及关键元数据位置；预text伪装还需要构造可信的勒索/恢复叙事。错误设备选择会破坏攻击者控制路径，GPT 备份头、冗余元数据、只读/受保护设备、应用控制、内核遥测和独立镜像会限制效果。

English: The adversary needs raw-device write, storage-management IOCTL, driver-load, root or administrator, or equivalent storage-control authority and knowledge of target disks and critical metadata locations. Pretext camouflage additionally needs a credible ransom or recovery narrative. Wrong-device selection can destroy the adversary's control path, while backup GPT headers, redundant metadata, read-only or protected devices, application control, kernel telemetry, and independent images constrain the effect.

### Defender model / 防守方模型

中文：防守方可观察进程/账户、原始设备打开、驱动加载与签名、IOCTL、块 I/O 的设备/扇区/长度/方向、分区和文件系统清单、关键元数据 hash/CRC、挂载/启动/健康结果、文件/勒索工件及重启。完整块追踪成本高且主机可能随盘失效，因此关键区间优先、外部日志汇聚和不同权健康/镜像验证是核心。只看文件事件或写入总量形成主要盲区。

English: Defenders can observe process and account, raw-device open, driver load and signature, IOCTL, block-I/O device, sector, length and direction, partition and file-system inventory, critical-metadata hash or CRC, mount/boot/health outcome, file or ransom artifacts, and reboot. Complete block tracing is expensive and host telemetry can die with the disk, making critical-extent priority, external log collection, and differently authorized health or image validation central. File events or total write volume alone create the main blind spot.

### Supported parent mechanisms

`TA0040-T1561-MECH-METADATA` — `NM-BT`, primary. **Summary zh:** 关键块破坏发生在文件级观察之外. **Summary en:** Critical-block destruction occurs outside file-level observation. **Analysis zh:** 攻击者对 MBR、GPT、MFT 或同类关键区间执行少量原始写入，痕迹从大量文件修改变为块设备句柄、驱动/IOCTL 与有限扇区变化；文件级传感器无法看到决定卷可用性的因果，形成行为透明。块偏移、元数据校验和启动/挂载结果可恢复。 **Analysis en:** The adversary performs a small number of raw writes to MBR, GPT, MFT, or similar critical extents, changing traces from many file modifications to a block-device handle, driver or IOCTL, and limited sector mutation. File-level sensors cannot observe the cause deciding volume availability, producing Behavioral Transparency. Block offsets, metadata validation, and boot or mount outcome recover it. **Evidence:** E2–E4. **Confidence:** `high` for Windows disk metadata, `medium` cross-filesystem.

`TA0040-T1561-MECH-PRETEXT` — `NM-FD`, secondary. **Summary zh:** 勒索可恢复外观掩盖不可恢复磁盘毁坏. **Summary en:** A recoverable-ransomware appearance disguises irreversible disk destruction. **Analysis zh:** 攻击者显示勒索信息、安装 ID 或加密状态，使事件特征类似可通过密钥恢复的 ransomware；真实实现不保留恢复信息或并行擦除关键磁盘结构，守方难以从呈现判断正确响应，形成特征伪装。块状态、密钥/ID来源和恢复代码语义揭示矛盾。 **Analysis en:** The adversary displays ransom information, an installation ID, or encryption state so the event resembles ransomware recoverable through a key, while the implementation retains no recovery material or wipes critical disk structures in parallel. Presentation no longer supports correct defensive classification, producing Feature Disguise. Block state, key or ID provenance, and recovery-code semantics reveal the conflict. **Evidence:** E3–E5. **Confidence:** `high` for ExPetr/PartyTicket, `medium` across wipers.

### Parent taxonomy narrative / 父级分类叙述

中文：原生分类按防守观察被改变的变量划分。关键元数据最小写入式毁坏用很小块覆盖产生整个卷/启动失败，需要原始 I/O 与结构完整性观察；可恢复性话术伪装式擦除用勒索/解密呈现改变事件语义，需要破坏状态与密钥/恢复路径验证。前者改变写入覆盖，后者改变解释框架，可在同一事件共现但不互相蕴含。

English: Native classification separates the defender-observation variable changed. Critical-Metadata Minimal-Write Destruction produces whole-volume or boot failure from small block coverage and requires raw I/O and structural-integrity observation. Recoverability-Pretext Wipe Camouflage changes incident meaning through ransom or decryptability presentation and requires validation of destruction state and key or recovery path. The first changes write coverage and the second interpretive framing; they can co-occur without implying each other.

中文：T1561.001/.002 的内容/结构二分不导入。全盘内容覆写和无特殊变量的结构初始化留在父级；签名驱动只是路径，擦除值模式暂待更多样本，恢复对象与固件由相邻技术负责。子项不能按 HDD/SSD、Windows/Linux、MBR/GPT、工具或写入值划分。

English: T1561.001/.002 content/structure partition is not imported. Full-disk content overwrite and structure initialization without a stealth variable remain parent core. Signed driver is a path, overwrite-value pattern awaits broader evidence, and recovery objects and firmware have adjacent owners. Children cannot be divided by HDD or SSD, Windows or Linux, MBR or GPT, tool, or overwrite value.

## Proposed child `TA0040-T1561-CHILD-METADATA`

**Name / 名称:** 关键元数据最小写入式毁坏 / Critical-Metadata Minimal-Write Destruction. **Confidence:** `high` for MBR/MFT cases, `medium` cross-storage.

### Definition and concept / 定义与概念

中文：关键元数据最小写入式毁坏是攻击者把破坏写入集中到占介质比例很小、却决定启动、分区解析、文件系统定位或卷一致性的块区间，使整个盘/卷在很少字节被改变后失去原用途。稳定变量是破坏覆盖率与可用性损失之间的不对称，而不是“结构擦除”、MBR、GPT 或某个文件系统名称。

English: Critical-Metadata Minimal-Write Destruction concentrates destructive writes on block extents that occupy a small fraction of media but govern boot, partition interpretation, file-system location, or volume consistency, causing the disk or volume to lose its purpose after few bytes change. The stable variable is asymmetry between destructive coverage and availability loss, not “structure wipe,” MBR, GPT, or a file-system name.

### Stealth characteristics / 匿迹特性

中文：关键元数据最小写入式毁坏不会产生与受影响文件数或磁盘容量相称的写带宽，也可能绕过文件路径审计。异常集中在低 LBA、分区/文件系统关键区间、原始设备句柄或驱动 IOCTL；随后才出现卷消失、CRC/结构校验失败、挂载或启动失败。只看累计写量的规则可能在损失完成前不报警。

English: Critical-Metadata Minimal-Write Destruction does not generate write bandwidth proportional to affected file count or disk size and can bypass file-path audit. The anomaly concentrates in low LBA, partition or file-system critical extents, raw-device handles, or driver IOCTL, followed by volume disappearance, CRC or structural validation failure, mount failure, or boot failure. Rules based only on cumulative write volume can remain quiet until loss is complete.

### Scope boundary definition / 范围边界界定

中文：纳入低覆盖原始写入/初始化直接破坏磁盘/卷关键结构并造成整体不可用。完整盘覆写、文件逐一覆盖和获批分区/格式化不属于本子项；它们分别留在父级、NJT-0156 或正常运维。需要设备总大小、实际写区间、结构角色、before/after 完整性和影响结果，不能只凭 sector 0 写入定性。

English: Include low-coverage raw write or initialization directly destroying critical disk or volume structures with broad unavailability. Full-disk overwrite, file-by-file overwrite, and approved partitioning or format do not belong to this child; they remain parent core, NJT-0156, or normal operations. Device size, actual extents, structural role, before/after integrity, and impact are required; a sector-zero write alone is insufficient.

### Application scenarios and threat model / 应用场景与威胁模型

中文场景：HermeticWiper 通过合法 EaseUS 驱动访问物理盘并腐坏每个盘的首个 512 字节 MBR，SentinelOne 指出此时已足以使设备无法启动，随后再处理分区/MFT。GigaWiper 用 `IOCTL_DISK_CREATE_DISK` 重新初始化非系统盘的分区元数据，再进行大块覆盖；前一个动作证明关键元数据损失本身已经改变可用性。

English scenario: HermeticWiper accessed physical disks through legitimate EaseUS drivers and corrupted the first 512-byte MBR on each disk; SentinelOne notes that this was already sufficient to prevent boot before later partition and MFT handling. GigaWiper used `IOCTL_DISK_CREATE_DISK` to reinitialize partition metadata on non-system disks before broad overwrite, showing that critical-metadata loss independently changes availability.

中文攻击方：攻击者需要原始设备写权限或可代理该写入的存储驱动/IOCTL，并准确识别目标盘和关键区间。GPT 备份、冗余超级块或自动修复可能降低效果；错误定位可能只破坏非关键数据或暴露行动。写入范围越小，攻击者越依赖结构知识。

English attacker: The adversary needs raw-device write authority or a storage driver or IOCTL that brokers it and accurate identification of target disk and critical extents. GPT backup, redundant superblocks, or automated repair can reduce effect. Wrong offsets can damage only noncritical data or expose the operation. Smaller write scope increases dependence on structural knowledge.

中文防守方：防守方需要盘/分区拓扑、关键元数据区间、块写设备/扇区/长度/进程、驱动加载与签名、结构 hash/CRC、挂载和启动状态。完整块追踪并非必需，但必须对低 LBA、GPT 头/备份、引导区及已识别文件系统元数据设置优先级，并把维护窗口加入基线。

English defender: The defender needs disk and partition topology, critical metadata extents, block-write device, sector, length and process, driver load and signing, structure hash or CRC, and mount and boot state. Full block tracing is not always required, but low LBA, GPT primary/backup, boot extents, and identified file-system metadata must be prioritized and maintenance windows included in baseline.

### Supported mechanism and limitations

Mechanism is `TA0040-T1561-MECH-METADATA` / `NM-BT`. **Limitation zh:** HermeticWiper 同时进行更广泛 MFT/文件擦除，不能把全部最终损失只归于 512 字节；证据只证明 MBR 破坏足以造成启动失败。不同文件系统有冗余和修复语义，关键区间必须按资产生成，不能硬编码一组跨环境偏移。 **Limitation en:** HermeticWiper also performed broader MFT and file wiping, so final loss cannot all be attributed to 512 bytes; evidence establishes only that MBR corruption was sufficient for boot failure. File systems differ in redundancy and repair, so critical extents must be generated per asset rather than hardcoded globally.

## Proposed child `TA0040-T1561-CHILD-PRETEXT`

**Name / 名称:** 可恢复性话术伪装式擦除 / Recoverability-Pretext Wipe Camouflage. **Confidence:** `high` for ExPetr, `medium` across decoy implementations.

### Definition and concept / 定义与概念

中文：可恢复性话术伪装式擦除是攻击者在实施不可恢复的磁盘/卷毁坏时，同时显示勒索、安装 ID、支付、扩展名、加密或“解密”流程，使受害方合理误以为当前状态由仍存在的密钥或攻击者服务可逆。稳定变量是真实恢复语义与对外呈现之间的故意差分，不是有无 ransom note 或是否调用加密 API。

English: Recoverability-Pretext Wipe Camouflage pairs irreversible disk or volume destruction with a ransom, installation ID, payment path, extension, encryption, or “decryption” workflow that causes the victim to reasonably believe the state is reversible through a retained key or adversary service. The stable variable is deliberate divergence between actual recovery semantics and external presentation, not the mere presence of a ransom note or cryptographic API.

### Stealth characteristics / 匿迹特性

中文：可恢复性话术伪装式擦除保留 ransomware 常见特征，使初始分类聚焦密钥、支付、谈判与解密工具，而忽略关键磁盘结构和裸机重建。ExPetr 的勒索屏幕显示安装 ID，但 Kaspersky 证明其只是随机数据，攻击者无法据此提取解密信息。伪装不隐藏中断，却隐藏了“是否可逆”这一决定响应路径的属性。

English: Recoverability-Pretext Wipe Camouflage retains familiar ransomware features so initial classification focuses on key recovery, payment, negotiation, and decryptors rather than critical disk structures and bare-metal rebuild. ExPetr displayed an installation ID on a ransom screen, but Kaspersky established it was random data from which the actor could not recover decryption information. The disguise does not hide outage; it hides reversibility, the attribute that selects the response path.

### Scope boundary definition / 范围边界界定

中文：纳入真实块/磁盘毁坏不可恢复且攻击者提供可恢复性呈现的行为。真正保留密钥并能恢复磁盘的勒索归 NJT-0157；只在文件级破坏并伪装归 NJT-0156 的相应研究，而非本项。付款无保证本身不足以判为伪装，必须通过 key/ID生成、恢复代码、块状态或独立分析证明话术与能力矛盾。

English: Include actual unrecoverable block or disk destruction accompanied by adversary presentation of recoverability. Ransomware that retains a key and can restore the disk belongs to NJT-0157. File-only destruction with a pretext belongs to the corresponding NJT-0156 research rather than this child. The general uncertainty of paying is insufficient; key or ID generation, recovery code, block state, or independent analysis must prove conflict between claim and capability.

### Application scenarios and threat model / 应用场景与威胁模型

中文场景：ExPetr 替换磁盘引导路径并显示支付/安装 ID 流程，看似 Petya 类勒索；分析显示 ID 由随机数据生成且不包含恢复密钥所需信息，支付不能使磁盘解密。HermeticWiper 行动还伴随 PartyTicket decoy ransomware；Microsoft 观察到 GigaWiper 中基于 Crucio 的“加密”命令生成随机 key/IV 后不保存，行为者无法解密。

English scenario: ExPetr replaced the disk boot path and displayed payment and installation-ID workflow resembling Petya ransomware, while analysis found the ID was random data containing no recovery information, making payment unable to decrypt the disk. HermeticWiper operations also used PartyTicket decoy ransomware. Microsoft observed a GigaWiper Crucio-derived “encryption” command generate random key and IV and never save them, leaving the actor unable to decrypt.

中文攻击方：攻击者需要实施真实毁坏并控制受害者可见的启动画面、note、扩展名或恢复标识；可信伪装还依赖公众熟悉的勒索叙事。防守方若保留离线块证据、样本和 key/ID生成逻辑，伪装会在技术验证中失效。攻击者也承担伪装组件提前触发告警的风险。

English attacker: The adversary needs actual destructive capability and control over victim-visible boot screen, note, extension, or recovery identifier, with credible disguise relying on a familiar ransomware narrative. If defenders preserve offline block evidence, samples, and key or ID generation logic, technical validation defeats the pretext. The disguise component can also trigger alerts before wiping completes.

中文防守方：防守方需要同时保全原始盘镜像/关键扇区、勒索工件、进程/驱动 lineage、安装 ID/密钥材料、样本反向分析及恢复尝试结果。不能在生产盘上试验所谓 decryptor；先镜像并比较 MBR/GPT/MFT/卷状态。只有话术证据而无不可恢复验证时，结论保持 hypothesis。

English defender: The defender needs preserved raw disk images or critical sectors, ransom artifacts, process and driver lineage, installation ID or key material, sample reverse analysis, and recovery-attempt outcome. A claimed decryptor must not be tested first on production media; image and compare MBR, GPT, MFT, and volume state. Presentation without irrecoverability validation remains hypothesis.

### Supported mechanism and limitations

Mechanism is `TA0040-T1561-MECH-PRETEXT` / `NM-FD`. **Limitation zh:** ExPetr 高置信证明随机安装 ID 与不可恢复，PartyTicket 是并行 decoy 而非 HermeticWiper 本体的解密承诺，GigaWiper 的不可恢复“加密”没有 ransom note。三者共同支持范围，但正式案例必须分别写明呈现形态，不能合并成一条虚构事件。 **Limitation en:** ExPetr strongly establishes a random installation ID and irrecoverability; PartyTicket is a parallel decoy rather than a decryption promise from HermeticWiper itself, and GigaWiper's irreversible “encryption” lacks a ransom note. Together they support the scope, but formal cases must preserve each presentation form rather than merge them into a fabricated event.

## Detection Strategy and Analytic candidates

### `DET-000105` candidate `extend` — Raw Storage–Object–Outcome Lineage

The existing strategy already defines mapping volume/device-level reads or writes to objects and successor outcomes. Extend its future `detects_refs` to the T1561 parent and metadata child and add a distinct write/outcome analytic; do not reuse NJA-000090 because its logic and observables are sensitive-object reads and output use.

#### `TA0040-T1561-NJA-BLOCK-MUTATION`

**Name:** Critical Block Mutation to Disk/Volume Availability / 关键块变更到磁盘卷可用性.

**Logic:** For Linux, use auditd rules on approved block-device nodes to record `timestamp`, host, `auid`, `euid`, `pid`, `exe`, syscall, success/exit, path, file type `block`, major/minor device, open flags, and change key. Collect block I/O via `blktrace`/`blkparse` or an equivalent eBPF sensor with timestamp, device major/minor, PID, command, action (`Q/I/D/C` as available), RWBS (`W`, `D`, flush), starting sector, block/byte count, completion/error, and cgroup. Preserve explicit `lsblk --json --output` inventory with device path/name, major/minor, type, size, parent, start, partition table style/UUID, partition type/UUID, filesystem type/UUID, and mountpoints; columns must be pinned rather than default output.

Generate a per-device critical-extent map from actual partition/file-system metadata, including MBR/GPT primary and backup structures, partition starts/boot areas, and file-system-specific metadata. On each unapproved raw write/discard/initialize, calculate written-sector union, coverage ratio to device size, overlap with critical extents, writer identity, and result. Correlate within five minutes to partition/UUID disappearance, GPT/CRC or signature change, mount failure, device health, and protected workload loss. Flag a high-impact low-coverage mutation even when total bytes are small; retain broad overwrite as parent-level T1561.

For Windows, join process/driver lineage and Sysmon Event 6 (`UtcTime`, driver image, hashes, signature/status) to a validated raw-I/O sensor exposing device/volume ID, process start key, IOCTL or access mask, offset, length, operation and result. DeviceFileEvents is file-level and cannot be claimed to provide block offsets. Preserve before/after MBR/GPT/volume hashes through an independent storage-integrity collector.

**Correlation:** raw open to I/O seconds; write to structure state and health five minutes; write to reboot/boot failure 30 minutes. Dimensions: host, asset/device ID, major/minor or PhysicalDrive ID, process start key/PID, driver hash/service, sector interval, partition/volume ID, maintenance approval, time.

**False positives:** authorized format, OS deployment/imaging, disk conversion, partition resize, filesystem creation/repair, LVM/RAID administration, backup restore, database raw devices, secure decommission, vendor diagnostics.

**Blind spots:** no block-level sensor, driver/kernel/firmware execution without process attribution, controller/device-internal sanitize with no per-sector trace, multipath/device-mapper remapping, volatile logs lost on reboot, encrypted/proprietary metadata, stale asset inventory.

**Tuning:** bind approved writer to exact account, executable/driver signature and hash, device class, operation/IOCTL, sector scope and ticket window; do not globally allow signed partition tools. Prioritize system/critical disks and critical extents, externally stream events, and distinguish attempt, metadata damage, broad wipe, and availability result. **Evidence:** E2–E4, E6–E10; extend DET-000105, create this NJA.

### `TA0040-T1561-DET-PRETEXT` — Presented Recoverability versus Disk Reality / 呈现可恢复性与磁盘真实状态差分

#### `TA0040-T1561-NJA-PRETEXT-DIFFERENTIAL`

**Logic:** Begin with confirmed or suspected raw disk mutation from the block analytic. Join within 30 minutes to process/file evidence for ransom notes, boot-screen replacement, encryption extensions, installation IDs, payment contacts, claimed decryptors, and forced reboot. On Windows use `DeviceProcessEvents` and `DeviceFileEvents` fields `Timestamp`, `DeviceId`, `ActionType`, `FileName`, `FolderPath`, `SHA1`, `FileSize`, `InitiatingProcessUniqueId`, initiating process/account/command line, `PreviousFileName`, and `ReportId`; add Sysmon driver load and preserved boot-sector/media hashes.

Create incident-analysis fields rather than pretending they are native EDR: `presentation.type`, `artifact.path/hash`, `claimed_recovery_id`, `claimed_key_or_decryptor`, `key_material_present`, `recovery_path_reachable`, `disk_structure_state`, `offline_image_id`, `analysis.confidence`. Reverse engineering or trusted vendor analysis validates whether the ID/key can derive recovery and whether recovery code exists. Emit `recoverability_pretext_conflict` only when a recovery presentation and irreversible block/structure evidence conflict; otherwise remain suspected ransomware or unknown destructive impact.

**Correlation:** block mutation to presentation/reboot 30 minutes; offline recoverability validation up to 24 hours or documented incident-analysis horizon. Dimensions: device/host, sample/process hash, process start key, driver hash, disk/image ID, artifact hash, installation ID, event time.

**False positives:** legitimate ransomware with a functioning key path, destructive recovery drill with banner, disk encryption migration, OEM recovery environment, authorized imaging with user warning, broken but nonmalicious encryption software.

**Blind spots:** disk cannot be imaged, note delivered off-host, sample unavailable, hybrid wiper/encryptor partly recoverable, key retained only by attacker, TPM/HSM state unavailable, production reboot destroys volatile evidence.

**Tuning:** treat visible ransom semantics as a hypothesis, image before remediation, preserve key/ID derivation and block offsets, and never infer irrecoverability merely because payment is uncertain. Escalate faster when critical metadata writes precede the presentation. **Evidence:** E3–E5, E10–E12.

## Mitigation resolutions

### `MIT-000107` candidate `extend` — Raw Storage Access Governance

The existing `raw-device-least-authority` and `block-object-lineage` measures are exact reusable concepts. Add parent/metadata-child applications: restrict raw write, discard, format and storage IOCTL authority to registered storage/deployment identities; govern driver installation and signed partition utilities; capture process-level sector ranges and critical-metadata outcomes. **Expected effect:** blocks ordinary scripts and low-privilege actors from destructive media access and makes successful writes attributable. **Limitations:** legitimate storage agents remain highly privileged, kernel/firmware actors can bypass host audit, signed drivers can be abused, and full block tracing has performance cost.

### `MIT-000158` candidate `extend` — Data-Retention Authority and Independent Recovery Protection

Reuse `protected-independent-copies` for the parent: retain bare-metal images, partition maps, boot/config state and business data outside production disk writer authority, then exercise full disk/volume restoration. **Expected effect:** disk wipe does not eliminate every recovery route and restoration validates structure as well as files. **Limitations:** a snapshot in the same account/controller is not independent, stale images lose RPO, and backups do not prevent current outage. Do not reuse the lifecycle-rule measure as T1561-specific.

### `TA0040-T1561-MIT-IMPACT-VALIDATION` candidate `create`

**Name:** Destructive-Impact Validation and Clean Rebuild Routing / 破坏性影响验证与清洁重建路由. **Measures:** preserve read-only/offline disk images and volatile evidence before using attacker tools; validate MBR/GPT/file-system state and key/installation-ID derivation in an isolated lab; predefine a decision tree for decryptable encryption versus irreversible wipe; revoke compromised raw-storage/driver authority and rebuild from known-good media when wipe is confirmed.

**Pretext-child application:** treat ransom/decryption claims as untrusted until key path and disk structure are validated; route confirmed wipe to containment and bare-metal rebuild rather than payment-driven delay. **Expected effect:** reduces response misclassification and prevents claimed decryptors from further altering original evidence. **Limitations:** reverse engineering takes time, partial recoverability can vary by volume, imaging large media delays restoration, and unavailable keys cannot prove the actor never retained one.

## Evidence and conclusion-level sources

| Key | Primary source and locator | Support and limit |
|---|---|---|
| E1 `REF-000898` | [MITRE ATT&CK Enterprise v19 T1561](https://attack.mitre.org/versions/v19/techniques/T1561/) | Exact existing parent behavior/tactic and two-child breadth anchor; reuse. |
| E2 `TA0040-T1561-REF-ESET-HERMETIC` | [ESET: IsaacWiper and HermeticWizard](https://www.esetngblog.com/post/isaacwiper-and-hermeticwizard-new-wiper-and-worm-targeting-ukraine), HermeticWiper analysis | Signed EaseUS drivers, DeviceIoControl, MBR/MFT/$Bitmap/$LogFile writes and boot failure; new REF/CASE. |
| E3 `TA0040-T1561-REF-SENTINEL-HERMETIC` | [SentinelOne: HermeticWiper](https://www.sentinelone.com/labs/hermetic-wiper-ukraine-under-attack/), MBR and Partition Corruption; PartyTicket | First 512 bytes sufficient for boot failure; driver indirection; ransomware decoy; new REF/CASE. |
| E4 `TA0040-T1561-REF-MS-GIGAWIPER` | [Microsoft: GigaWiper](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/), standalone wiper and RanMain | Physical disk enumeration, partition reinitialization, broad raw overwrite, unsaved key/IV ransomware-like wipe and patterned writes; new REF/CASE. |
| E5 `TA0040-T1561-REF-KASPERSKY-EXPETR` | [Securelist: ExPetr is a Wiper, Not Ransomware](https://securelist.com/expetrpetyanotpetya-is-a-wiper-not-ransomware/78902/), installation ID analysis | Ransom presentation, random ID and inability to derive disk decryption; new REF/CASE. |
| E6 `TA0040-T1561-REF-BLKPARSE` | [Linux blkparse manual](https://man7.org/linux/man-pages/man1/blkparse.1.html), output fields and actions | Device, PID, command, RWBS, sector, block/byte count, time and error; new REF. |
| E7 `TA0040-T1561-REF-BLOCK-STATS` | [Linux block statistics](https://kernel.org/doc/html/latest/block/stat.html), sector/write/discard counters | Completed read/write/discard sectors and timing; aggregate only, no process attribution; new REF. |
| E8 `TA0040-T1561-REF-LSBLK` | [lsblk manual](https://man7.org/linux/man-pages/man8/lsblk.8.html), JSON/explicit columns/filesystem/topology | Stable explicit inventory and udev timing limits; new REF. |
| E9 `TA0040-T1561-REF-AUDITCTL` | [auditctl manual](https://man7.org/linux/man-pages/man8/auditctl.8.html), syscall/path/identity/device fields | Raw block node access attribution; audit does not provide all block offsets; new REF. |
| E10 `REF-000366` | [Microsoft Sysmon events](https://learn.microsoft.com/en-us/windows/security/operating-system-security/sysmon/sysmon-events), Event 6 | Existing driver-load hash/signature reference; reuse. |
| E11 `REF-000475` | [MDE DeviceFileEvents](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicefileevents-table) | Existing file/pretext artifact and process lineage fields; not block offsets; reuse. |
| E12 `TA0040-T1561-REF-MS-CREATE-DISK` | [Microsoft CREATE_DISK / IOCTL_DISK_CREATE_DISK](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ns-winioctl-create_disk) | Partition table/raw disk initialization semantics used by GigaWiper; new REF. |
| E13 `TA0040-T1561-REF-MS-GPT` | [Microsoft Basic and Dynamic Disks](https://learn.microsoft.com/en-us/windows/win32/fileio/basic-and-dynamic-disks), GPT layout | GPT header/CRC/backup semantics for integrity inventory; new REF. |

## Shared-library lookup and resolution record

Executed `library_lookup.py` with: `Disk Wipe T1561`; `HermeticWiper MBR EaseUS driver`; `GigaWiper physical disk partition metadata`; `NotPetya wiper ransomware installation ID`; `raw block write sector blkparse`; `ransomware decoy wiper`; `critical metadata overwrite disk`; and `IOCTL_DISK_CREATE_DISK`.

- **References:** exact reuse `REF-000898` for T1561, `REF-000366` for Sysmon driver loads, and `REF-000475` for DeviceFileEvents. No exact canonical URL matched E2–E9 or E12–E13. `REF-000601` covers Petya propagation rather than ExPetr recoverability semantics and cannot replace E5.
- **Cases:** create `TA0040-T1561-CASE-HERMETIC` using E2/E3 with exact driver, MBR/MFT and outcome facts; `TA0040-T1561-CASE-GIGAWIPER` using E4; `TA0040-T1561-CASE-EXPETR-PRETEXT` using E5. Do not merge PartyTicket, GigaWiper and ExPetr into one case.
- **Claims:** `TA0040-T1561-CLM-PARENT` (block/structure destruction and availability; E1/E2/E4); `TA0040-T1561-CLM-MINIMAL` (small critical metadata writes can prevent boot; E3); `TA0040-T1561-CLM-PRETEXT` (random/nonretained recovery material conflicts with ransomware presentation; E4/E5); `TA0040-T1561-CLM-BLOCK-FIELDS` (E6–E9); `TA0040-T1561-CLM-WINDOWS-FIELDS` (E10–E13); `TA0040-T1561-CLM-MITIGATION` (raw authority and independent images; E2–E4 plus existing MIT evidence).
- **Detection:** recommend **extend** DET-000105 with the new destructive-write NJA because strategy identity already covers raw reads or writes mapped to outcome. Do not reuse NJA-000090 because it is sensitive-object read/use logic. Create a separate presentation-versus-reality DET/NJA for the pretext child.
- **Mitigation:** recommend **extend** MIT-000107 with T1561 raw-write applications and MIT-000158 with protected disk-image restore application. Create the impact-validation control only for pretext response. Existing raw-storage objects do not prove destructive intent by themselves.
- **Adjacent library:** REF-000898 is currently used by NJT-0188 only as a boundary; extending subjects does not change its identity. NJT-0108/DET-000105/MIT-000107 remain the raw-view owner for read behavior, while T1561 adds write/outcome facts.

## Content-depth and research limitations

中文：HermeticWiper 高质量证明驱动代理、关键结构和启动失败，但同时实施更广泛擦除，因此只能断言 MBR 破坏足以失去启动，不应把全部损失归于最少写入。ExPetr 高质量证明可恢复性话术与真实 key/ID 语义冲突；GigaWiper 和 PartyTicket 的呈现不同，不能模板化合并。Linux 块字段是可实施遥测示例，Windows 缺少默认逐扇区 EDR 字段，正式 NJA 必须明确依赖自建/内核传感器而不能伪称 DeviceFileEvents 提供偏移。

English: HermeticWiper strongly establishes driver brokerage, critical structures, and boot failure, but it also performs broader wiping, so only sufficiency of MBR damage for boot loss can be claimed rather than attributing all damage to minimal writes. ExPetr strongly establishes conflict between recoverability presentation and real key or ID semantics; GigaWiper and PartyTicket use different presentation forms and cannot be merged through boilerplate. Linux block fields are an implementable telemetry example. Windows lacks default per-sector EDR fields, so a formal NJA must declare its custom or kernel sensor rather than claim DeviceFileEvents supplies offsets.

Compared with NJT-0001 by field responsibility, parent and both children define direct behavior, stable variable, changed trace, defender observation, residual evidence, boundary/counterexamples, scenarios, attacker prerequisites, defender visibility, mechanisms, defense differences, source strength, and limitations. No child is copied from ATT&CK content/structure names.

**Integration status:** pending all five candidate handoffs, primary convergence with NJT-0156/NJT-0188/NJT-0186/NJT-0108, shared-library resolution, formal ID allocation, canonical YAML, quality, Bundle, Web/API QA, and human review. Only this staging file was written.
