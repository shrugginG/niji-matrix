# T1531 Account Access Removal research handoff

`batch_ref: BATCH-TA0040-003`  
`work_item_ref: WORK-TA0040-T1531`  
`temporary_key_prefix: TA0040-T1531-`  
`status: research-only; integration pending`  
`baseline: Enterprise ATT&CK 19.1`  
`formal IDs allocated: none`

## Recommendation

**Adapt; high confidence; two formal Niji children proposed.** Proposed bilingual admission rationale:

> 账户访问移除通过删除、禁用、锁定或操纵合法主体的认证与授权状态，使用户、管理员或租户 owner 无法继续进入系统或资源，直接造成 TA0040 的访问可用性影响。Niji 应把正式范围适配为借用正常身份管理、恢复或权限变更接口并形成实际 lockout 的行为，按两个独立观察变量划分：账户身份仍存在但原认证器被替换/移除，或账户和认证器仍有效但关键角色、组、委托或策略边被撤除。Storm-2949 直接证明攻击者重置密码、移除原 MFA、注册自身方法并阻止合法用户登录；DEV-0537/LAPSUS$ 直接证明攻击者创建自身全局管理员后移除其他全局管理员，使组织失去访问。[E1][E2][E3]
>
> Account Access Removal deletes, disables, locks, or manipulates authentication and authorization state of a legitimate principal so a user, administrator, or tenant owner can no longer enter systems or resources, directly producing TA0040 access-availability impact. Niji should adapt the formal scope to actions that use ordinary identity administration, recovery, or entitlement-change interfaces and cause actual lockout, divided by two independent observation variables: the identity remains while original authenticators are replaced or removed, or the account and authenticator remain valid while critical role, group, delegation, or policy edges are removed. Storm-2949 directly establishes password reset, removal of original MFA, enrollment of an attacker method, and prevention of legitimate sign-in. DEV-0537/LAPSUS$ directly establishes creation of an actor global administrator followed by removal of all other global administrators, locking the organization out.[E1][E2][E3]

Parent and child existence are high-confidence. Legitimate administrative interfaces create feature similarity with offboarding, recovery, and fraud response, but actual victim lockout and adversary control remain mandatory. No ATT&CK child exists or is imported.

## Required boundary convergence

- **Versus NJT-0083 Existing-Identity Access-State Manipulation:** NJT-0083 owns durable additions or changes that preserve or expand attacker access: parallel authenticators, added authorization edges, or device trust. T1531 owns the negative effect on a legitimate principal: all usable victim authenticators are displaced, the account is disabled/deleted, or required authorization edges are removed and access actually fails. Storm-2949 can dual-map because the actor added its method while displacing the victim's methods; DEV-0537 can dual-map creation/grant of actor admins and removal of legitimate admins, but each conclusion needs separate edges and outcomes.[E2][E3][L1]
- **Credential/access-material change without actual lockout:** password reset, authentication-method deletion, key rotation, device removal, or contact change is exposure/state mutation until the legitimate owner is shown unable to authenticate or recover through an approved remaining path. A changed credential string, control-plane success, or help-desk request alone does not complete T1531.[E4][E5]
- **Privilege escalation:** adding an attacker role, group membership, application grant, or higher-authority authenticator belongs to NJT-0083/TA0004 when it yields new attacker authority. Removing a victim's role establishes Impact only when the victim loses required access; it does not prove the changer gained privilege. Compute pre/post authority separately for attacker and victim.[L1]
- **Identity defense impairment:** targeted lockout of incident responders or security administrators is still T1531 for the identity availability result and can also impair defense if a concrete response capability is lost. A central policy mutation that broadly lowers identity/security controls belongs to NJT-0125; a modified authentication mechanism that accepts attacker proofs belongs to NJT-0093. Do not create a T1531 child based only on the victim's job title.[L2][L3]
- **Session revocation:** revoking a refresh token, terminating a session, or logging a user off is not durable account access removal if the legitimate principal can immediately authenticate again with unchanged approved state. Session revocation becomes an activation or consequence when paired with disabled account, displaced authenticators, or removed authorization that blocks subsequent access.[E7]
- **Normal offboarding, account recovery, and fraud response:** legitimate responders intentionally disable users, reset passwords, remove authentication methods, revoke sessions, and deprovision application access. The same local events are strong counterexamples distinguished through HR/fraud case, owner, initiator, ticket, scope, timing, remaining recovery path, emergency-account status, and expected post-state.[E6][E7]

## Taxonomy breadth review and open-ended axes

Fixed ATT&CK 19.1 child count: **0**. Breadth trigger: ordinary open search. Proposed Niji child count: **2**. Future children must set `lineage.attck_subtechnique_inherited: false`.

| Candidate stealth axis | Trace and defender-observation effect | Resolution |
| --- | --- | --- |
| Identity-preserving authenticator displacement | Account remains present/enabled while password and victim authentication methods are replaced or removed; account-state checks look healthy and sign-in evidence carries the later failure | **Formal child 1**; exact method/password-state lineage and owner sign-in outcome differ from role analysis.[E3][E4][E5] |
| Authorization-graph edge eviction | Authentication can succeed while a role, group, delegation, or resource-policy edge is removed; effective access fails only at authorization evaluation | **Formal child 2**; requires old/new graph, evaluation path, and resource denial.[E2][E4] |
| Whole-account deletion or disablement | Account object disappears or `accountEnabled` becomes false | `parent-core`; highly visible state result, still within parent when adversary-controlled and actual lockout occurs, but no independent stealth variable beyond normal administrative interface. |
| Mass/burst removal | One actor disables/removes many users or administrators | `parent-core / detection severity`; count and speed help detection but current sources do not establish a stable Niji mechanism separate from the state paths. |
| Delayed token/cache propagation | Existing tokens continue briefly or denial appears after synchronization | `evidence-deferred`; propagation affects correlation window and recovery but is platform timing, not yet an evidenced attacker-controlled child. |
| Session-only invalidation | Active tokens/sessions end while credentials and authorization remain | `not-completed`; no durable victim lockout if reauthentication succeeds.[E7] |
| Parallel attacker credential added while victim path is removed | Attacker persists and victim is excluded | `dual-owner`; added path maps to NJT-0083, displaced victim path maps to child 1. Do not merge into a third T1531 child.[E3][L1] |
| Targeting responders/admins | Defense response may degrade | `relationship / adjacent result`; identity role is not a taxonomy variable. |
| Maintenance-like actor/time/ticket alignment | Malicious mutation may resemble offboarding or incident response | `parent-core camouflage`; relevant to NM-FD and detection, but no stable child without distinct state/defense logic. |

## Proposed parent content (`TA0040-T1531-PARENT`)

Name: **管理合形式账户访问移除 / Administration-Conforming Account Access Removal**  
Aliases: `Account Access Removal`, `T1531`  
Summary:

> 攻击者通过正常身份管理或恢复接口移除合法主体的认证或授权能力，使受害者失去访问，同时让局部痕迹类似离职、恢复或欺诈响应。
>
> Adversaries use ordinary identity administration or recovery interfaces to remove a legitimate principal's authentication or authorization capability, denying victim access while local traces resemble offboarding, recovery, or fraud response.

### `definition_and_concept`

> 管理合形式账户访问移除是攻击者对已经存在且属于合法用户、管理员、服务 owner 或租户管理者的身份执行删除、禁用、密码/认证器置换或授权边撤除，使该主体无法继续通过原本批准的路径认证或访问所需资源。直接对象是合法主体的有效访问能力及失败结果；命令、API、门户、目录产品、账户类型和后继勒索行为只是实现或相邻事件。[E1]
>
> Administration-Conforming Account Access Removal is adversary deletion, disablement, password or authenticator displacement, or authorization-edge removal on an existing identity belonging to a legitimate user, administrator, service owner, or tenant operator, preventing that principal from authenticating or reaching required resources through previously approved paths. The direct object is the legitimate principal's effective access capability and failure outcome. Commands, APIs, portals, directory products, account type, and later extortion are implementations or adjacent events.[E1]

> Niji 的正式条件要求移除借用平台原生管理、恢复或权限工作流并改变防守观察。账户可以仍显示为启用，认证也可以成功，实际 lockout 却分别隐藏在认证方法集合或有效授权图中；控制面变更和受害者后续失败还可能位于不同日志与时间。只有把发起者、目标状态 old/new、审批和 post-state 认证/授权结果连接起来，才能把恶意移除与正常身份生命周期区分。[E2][E3][E4][E5]
>
> Niji formal scope requires removal through native administration, recovery, or entitlement workflows with a changed defensive observation. The account can still appear enabled, or authentication can succeed, while actual lockout lies respectively in the authentication-method set or effective authorization graph. Control-plane mutation and later victim failure can also occur in different logs and times. Only a join among initiator, target old and new state, approval, and post-state authentication or authorization result distinguishes malicious removal from normal identity lifecycle.[E2][E3][E4][E5]

### `stealth_characteristics`

> 管理合形式账户访问移除保留身份系统熟悉的操作与状态：管理员重置密码、删除 MFA、撤销角色或停用账户都是合法离职、欺诈处置和恢复流程也会使用的动作。恶意行为因此没有专用破坏接口，单条审计记录中的操作名、成功结果或高权限发起者不足以区分；攻击者若先取得全局管理员或社会工程化恢复流程，局部来源更可能符合正常管理外观。[E2][E3][E7]
>
> Administration-Conforming Account Access Removal preserves familiar identity operations and states: administrators reset passwords, delete MFA methods, revoke roles, or disable accounts during legitimate offboarding, fraud containment, and recovery. The malicious behavior therefore has no dedicated destructive interface, and an operation name, successful result, or privileged initiator in one audit record is insufficient to distinguish it. When an adversary first obtains global administration or social engineers a recovery workflow, local provenance can more closely match ordinary administration.[E2][E3][E7]

> 残余包括 directory audit 的发起用户/应用、targetResources、modifiedProperties old/new、认证方法或角色/组 ID、correlationId、批准/HR/fraud case、账户快照、登录失败、条件访问状态、资源拒绝、owner 报告和紧急账户使用。身份变更、后继失败与恢复动作按 tenant、principal、edge/method、session、resource 和时间关联后，能够证明实际 lockout 并排除单纯会话撤销或正常处置。[E4][E5][E6]
>
> Residual evidence includes directory-audit initiating user or app, target resources, modified-property old and new values, authentication-method or role and group IDs, correlation ID, approval or HR or fraud case, account snapshots, sign-in failure, Conditional Access status, resource denial, owner report, and emergency-account use. Correlating identity mutation, later failure, and recovery by tenant, principal, edge or method, session, resource, and time can establish actual lockout and exclude session-only revocation or normal response.[E4][E5][E6]

### `scope_boundary_definition`

> 纳入要求目标身份在变更前存在并属于合法主体，变更由攻击者或被其控制的管理主体发起，认证器/账户/授权状态成功改变，并且 post-state 证据证明合法主体无法重新认证、激活必要角色或访问所需资源。没有实际失败结果时保留为访问移除 exposure；删除后立即重建同名攻击者账户还需分别评估新身份创建和伪装。[E1][E4][E5]
>
> Inclusion requires a target identity that existed before mutation and belonged to a legitimate principal, a mutation initiated by the adversary or a controlled administrator, successful change to authenticator, account, or authorization state, and post-state evidence that the legitimate principal cannot reauthenticate, activate a necessary role, or reach a required resource. Without an actual failure outcome, retain access-removal exposure. Deletion followed by recreation of an attacker-controlled same-name account also requires separate new-identity and masquerading assessment.[E1][E4][E5]

> 向既有身份增加并行凭据、角色或设备信任以保存攻击者访问归 NJT-0083；只有凭据/材料变化但 victim 仍有批准路径不属于 T1531。攻击者新获高权限归 TA0004；改变全局认证过程归 NJT-0093，发布削弱身份防御的中心策略归 NJT-0125。仅撤销 session/token 且可重新登录不成立。合法离职、用户请求恢复、欺诈响应、合规去权限和应急隔离是强反例，须按完整工作流而非操作名称排除。[E7][L1][L2][L3]
>
> Adding a parallel credential, role, or device trust to an existing identity to preserve adversary access belongs to NJT-0083. Credential or material change without loss of every approved victim path is outside T1531. New attacker privilege belongs to TA0004. Global authentication-process change belongs to NJT-0093, and central policy that weakens identity defense belongs to NJT-0125. Session or token revocation alone does not qualify when reauthentication remains possible. Legitimate offboarding, user-requested recovery, fraud response, compliant deprovisioning, and emergency containment are strong counterexamples excluded by the complete workflow rather than operation name.[E7][L1][L2][L3]

### `application_scenarios_and_threat_model`

Application scenarios:

> 在云租户接管中，攻击者可先取得或创建高权管理身份，再移除其他全局管理员角色，使组织缺少可管理租户的合法主体；DEV-0537 直接展示该路径。在定向用户接管中，攻击者可滥用 SSPR/MFA 恢复，重置密码、删除原认证方法并注册自身方法，让用户对象仍存在但 owner 无法登录；Storm-2949 直接展示该路径。两类行为都可发生在数据窃取、勒索或破坏前后，但账户 lockout 需独立证据。[E2][E3]
>
> In cloud-tenant takeover, an adversary can first obtain or create a privileged administrator and then remove other Global Administrator roles, leaving the organization without a legitimate tenant-management principal; DEV-0537 directly demonstrates this path. In targeted user takeover, an adversary can abuse SSPR or MFA recovery, reset the password, delete original methods, and enroll an attacker method, leaving the user object present while its owner cannot sign in; Storm-2949 directly demonstrates this path. Either can accompany theft, extortion, or destruction, but account lockout needs independent evidence.[E2][E3]

Attacker model:

> 攻击者需要用户/角色/组/认证方法变更权限或能社会工程化自助恢复，了解目标的剩余认证路径、嵌套授权、token 传播和紧急账户，并能在恢复团队反应前完成移除。PIM/JIT、抗钓鱼管理员认证、职责分离、owner/双人确认、受保护紧急账户和不可变审计提高成本；遗漏一个有效路径会使 victim 保持访问，过度移除则产生显著告警。[E3][E6]
>
> The adversary needs authority to change users, roles, groups, or authentication methods, or the ability to socially engineer self-service recovery; knowledge of remaining authentication paths, nested authorization, token propagation, and emergency accounts; and enough time to complete removal before responders recover. PIM or JIT, phishing-resistant administrator authentication, separation of duties, owner or two-person confirmation, protected emergency accounts, and immutable audit raise cost. Missing one valid path leaves victim access, while excessive removal creates conspicuous alerts.[E3][E6]

Defender model:

> 防守方能取得目录/IdP 控制面审计、认证方法和角色/组快照、登录和 token、资源访问决策、PIM/审批、HR/欺诈工单、owner 报告及紧急账户日志，并解析每个主体的全部认证器和有效授权图。只检查 `accountEnabled` 会漏掉两项子技术；只看失败登录无法证明恶意变更；只看控制面又不能证明 lockout 已兑现。攻击者控制审批、同步源或日志租户时形成主要盲区。[E4][E5][E6]
>
> Defenders can obtain directory or IdP control-plane audit, authentication-method and role or group snapshots, sign-in and token records, resource access decisions, PIM or approval, HR or fraud cases, owner reports, and emergency-account logs, and resolve every principal's complete authenticator set and effective authorization graph. Checking only `accountEnabled` misses both children. Failed sign-in alone cannot prove malicious mutation, while control-plane data alone cannot prove lockout materialized. Adversary control of approval, synchronization source, or logging tenant creates the principal blind spots.[E4][E5][E6]

### `stealth_mechanisms`

1. `NM-FD`, role `primary`, confidence `high`. Summary: **正常身份管理动作承载恶意访问剥夺 / Ordinary identity-administration actions carry malicious access deprivation**

> 攻击者使用密码恢复、认证方法管理、角色/组撤除或账户停用等合法控制，把恶意剥夺编码成与 offboarding、欺诈响应或 owner 恢复相同的操作和对象状态；只按事件名称、管理员身份或成功结果分类时难以区分，形成特征伪装。审批/HR/fraud case、管理来源、old/new 状态和 victim 后继失败揭示用途差异。[E2][E3][E7]
>
> The adversary uses legitimate controls for password recovery, authentication-method management, role or group removal, or account disablement, encoding malicious deprivation in the same operations and object states used for offboarding, fraud response, or owner recovery. Classification by event name, administrator identity, or successful result alone has difficulty distinguishing intent, producing Feature Disguise. Approval or HR or fraud case, administrative origin, old and new state, and later victim failure expose the usage difference.[E2][E3][E7]

2. `NM-BT`, role `secondary`, confidence `medium`. Summary: **控制面状态变更与受害者访问失败分离在不同日志和时间 / Control-plane state mutation and victim access failure separate across logs and time**

> 身份控制面记录谁改变了认证器或授权边，登录/资源面随后只记录目标主体的失败或拒绝；两侧常使用不同 ID、保留期和传播时间。缺少 method/edge 到 post-state decision 的关联时，管理事件看似常规、失败看似用户错误，关键因果落在分析理解之外，形成行为透明。correlationId、target principal、method/edge ID、snapshot 和 denied result 能恢复。[E4][E5]
>
> The identity control plane records who changed an authenticator or authorization edge, while sign-in or resource planes later record only target-principal failure or denial. The sides commonly use different IDs, retention, and propagation time. Without joining method or edge to post-state decision, the administration looks routine and the failure looks like user error, leaving causality outside analytic understanding and producing Behavioral Transparency. Correlation ID, target principal, method or edge ID, snapshot, and denied result recover it.[E4][E5]

### `subtechnique_taxonomy`

> 子技术按访问失败发生在认证还是授权求值划分。身份保留式认证器置换锁定保留 user/principal 对象，却替换或移除 owner 的密码、MFA 或恢复认证器，检测以 method/password state 和后继 sign-in 为核心；授权图边撤除锁定保留身份和认证器，却删除角色、组、委托或策略边，检测以 effective graph、evaluation path 和 resource denial 为核心。两者可共现但状态键、失败阶段和恢复动作不同。
>
> Children are divided by whether access fails during authentication or authorization evaluation. Identity-Preserving Authenticator Displacement Lockout keeps the user or principal object while replacing or removing the owner's password, MFA, or recovery authenticators, so detection centers method or password state and later sign-in. Authorization-Graph Edge Eviction Lockout keeps identity and authenticators while deleting a role, group, delegation, or policy edge, so detection centers effective graph, evaluation path, and resource denial. They can co-occur but use different state keys, failure stages, and recovery actions.

> 账户整体删除/禁用由父级表达；平台、账户类型、CLI/API、批量数量和 victim 职位不形成 NJS。新增攻击者 access edge 属于 NJT-0083；session-only revocation 不完成本技术；中心身份防御策略和全局认证机制保留各自 owner。
>
> Whole-account deletion or disablement remains at the parent. Platform, account type, CLI or API, batch count, and victim job role do not form NJS. Added adversary access edges belong to NJT-0083. Session-only revocation does not complete this technique, and central identity-defense policy and global authentication mechanisms retain their own owners.

### `research.limitations`

> Microsoft 对 DEV-0537 和 Storm-2949 的现场观察直接支持两项子技术存在，但日志字段、authentication method ID、角色传播和资源拒绝因租户许可、应用和保留设置不同。合法 offboarding/欺诈响应在局部可与攻击完全相同，owner 无法登录的报告也可能来自密码错误、服务故障或设备问题。正式结论必须连接攻击者控制、状态差和具体 post-state 失败；缺少精确 method/edge 时降低为 principal-level 推断。[E2][E3][E4][E5][E7]
>
> Microsoft's field observations of DEV-0537 and Storm-2949 directly support both children, but log fields, authentication-method IDs, role propagation, and resource denial vary by tenant license, application, and retention. Legitimate offboarding or fraud response can be locally identical to attack, while an owner's inability to sign in can also result from password error, service failure, or device problems. Formal conclusions must join adversary control, state differential, and a specific post-state failure. Missing exact method or edge reduces the result to principal-level inference.[E2][E3][E4][E5][E7]

## Proposed child 1 (`TA0040-T1531-CHILD-AUTHENTICATOR-DISPLACEMENT`)

Name: **身份保留式认证器置换锁定 / Identity-Preserving Authenticator Displacement Lockout**  
Summary:

> 攻击者保留身份对象，却替换或移除合法 owner 的可用认证器，使账户看似存在而受害者无法重新登录。
>
> Adversaries retain the identity object while replacing or removing the legitimate owner's usable authenticators, leaving the account present but the victim unable to sign in again.

### Definition and concept

> 身份保留式认证器置换锁定以主体对象持续存在而 owner 的认证路径集合发生排他变化为变量。攻击者重置密码、删除原 MFA/恢复方法，并可注册自身方法；完成条件是合法 owner 的批准认证器不再能产生成功认证，而不是某个方法发生变化。[E3]
>
> Identity-Preserving Authenticator Displacement Lockout varies an identity object that continues to exist while the owner's authentication-path set changes exclusively. The adversary resets the password, deletes original MFA or recovery methods, and can enroll an attacker method. Completion requires that the legitimate owner's approved authenticators can no longer produce successful authentication, not merely that one method changed.[E3]

### Stealth characteristics

> 身份保留式认证器置换锁定使 user ID、UPN、账户年龄和 `accountEnabled` 保持正常，粗粒度“用户存在/启用”健康检查继续通过；身份审计只显示可由恢复流程产生的密码/MFA 变化，实际影响在稍后的 owner 登录失败中显现。method old/new、恢复发起者、新方法设备、sign-in source 和 owner 报告仍可恢复链条。[E3][E4][E5]
>
> Identity-Preserving Authenticator Displacement Lockout preserves user ID, UPN, account age, and `accountEnabled`, so coarse user-present or user-enabled health checks continue to pass. Identity audit shows password or MFA changes also produced by recovery, while the impact appears in later owner sign-in failure. Method old and new state, recovery initiator, new-method device, sign-in source, and owner report still recover the chain.[E3][E4][E5]

### Scope boundary

> 纳入要求既有身份仍存在，攻击者控制的恢复/认证变更移除所有可用 owner 路径，且 post-state sign-in 或经验证 owner 报告证明无法认证。合法密码轮换、MFA 迁移、丢失设备恢复、只删一个备用方法及 victim 仍能用另一批准方法登录是反例。攻击者新增方法另记 NJT-0083，但不替代本项的 victim failure。[E7][L1]
>
> Inclusion requires an existing identity to remain present, an adversary-controlled recovery or authentication change to remove every usable owner path, and post-state sign-in or verified owner report proving authentication failure. Legitimate password rotation, MFA migration, lost-device recovery, deletion of only one backup method, and a victim who can still sign in with another approved method are counterexamples. An attacker-added method is additionally mapped to NJT-0083 but does not replace this child's victim failure.[E7][L1]

### Application scenario

> 攻击者社会工程化 SSPR/MFA 提示或取得 Authentication Administrator 等权限，重置目标密码、清除电话/邮箱/Authenticator，并把新方法绑定到自己设备；用户对象仍正常显示，合法用户在下一次登录或 session 失效后被排除。Storm-2949 在多个高价值用户上重复了该链。[E3]
>
> An adversary social engineers SSPR or MFA prompts or obtains Authentication Administrator-equivalent authority, resets the target password, clears phone, email, or Authenticator methods, and binds a new method to an attacker device. The user object remains normal while the legitimate user is excluded at the next sign-in or session expiry. Storm-2949 repeated this chain across multiple high-value users.[E3]

### Attacker model

> 攻击者需要恢复或认证方法管理权限，或能说服用户完成强认证步骤；还需知道或枚举全部剩余方法，并在 owner/帮助台反应前注册自身路径。抗钓鱼恢复证明、owner 回拨、独立审批、方法数量/设备约束和短期高权会限制效果。
>
> The adversary needs recovery or authentication-method management authority or the ability to persuade the user to complete strong-authentication steps. The adversary must also know or enumerate every remaining method and enroll its own path before the owner or help desk responds. Phishing-resistant recovery proof, owner callback, independent approval, method-count or device constraints, and short-lived privilege limit the effect.

### Defender model

> 防守方保留 method ID、绑定设备、initiator、correlationId、old/new snapshot、后继登录和经验证 owner case，并区分 active token 尚未到期与真正可重新认证。平台不公开具体使用方法时，关联只能降为 principal-level。
>
> Defenders retain method ID, bound device, initiator, correlation ID, old and new snapshots, later sign-in, and a verified owner case, and distinguish an unexpired active token from the ability to reauthenticate. When the platform does not expose the method actually used, correlation falls back to principal level.

### Mechanism, defense, and limitations

`NM-FD`, primary, high confidence. Summary: **保留账户身份外观并把恶意置换包装为恢复流程 / Preserve account identity appearance and package malicious displacement as recovery**.

> 攻击者通过正常恢复接口移除 owner 方法并注册新认证器，账户实体和启用状态不变，变更事件与合法 SSPR/MFA 恢复共享名称和对象；防守若只看账户存在或恢复成功会误判正常，形成特征伪装。认证方法集合差分、恢复来源和 owner 后继失败揭示排他置换。[E3][E4]
>
> The adversary removes owner methods and enrolls a new authenticator through normal recovery interfaces. Account entity and enabled state remain unchanged, while change events share names and objects with legitimate SSPR or MFA recovery. Defenders checking only account presence or recovery success can misclassify the result as normal, producing Feature Disguise. Authentication-method-set differential, recovery origin, and later owner failure expose exclusive displacement.[E3][E4]

Detection coverage: proposed parent Strategy plus `TA0040-T1531-NJA-AUTHENTICATOR-DISPLACEMENT-LOCKOUT`. Mitigation coverage: extend MIT-000063 with this child application. Temporary claims: `TA0040-T1531-CLM-AUTHENTICATOR-DISPLACEMENT` and `TA0040-T1531-CLM-AUTHENTICATOR-DETECTION`; case candidate `TA0040-T1531-CASE-STORM2949-SSPR-LOCKOUT`.

> 登录日志可能不公开实际使用的 method ID，合法 owner 也可能直到 token 到期或设备重新认证才发现失败。SSPR/MFA 恢复、帮助台迁移和丢失设备处置具有相同局部痕迹；缺少精确方法集合和 post-state owner 失败时，子项只能维持中等置信的 principal-level 推断。
>
> Sign-in logs may not expose the method ID actually used, and the legitimate owner may not discover failure until token expiry or device reauthentication. SSPR or MFA recovery, help-desk migration, and lost-device response have the same local traces. Without an exact method set and post-state owner failure, the child remains a medium-confidence principal-level inference.

## Proposed child 2 (`TA0040-T1531-CHILD-AUTHORIZATION-EDGE-EVICTION`)

Name: **授权图边撤除锁定 / Authorization-Graph Edge Eviction Lockout**  
Summary:

> 攻击者保留账户和认证器，却撤除关键角色、组、委托或策略边，使合法主体在授权阶段失去所需资源访问。
>
> Adversaries retain the account and authenticator while removing critical role, group, delegation, or policy edges so the legitimate principal loses required resource access during authorization.

### Definition and concept

> 授权图边撤除锁定以认证状态保持有效、effective access 因负向 graph delta 消失为变量。攻击者删除直接或嵌套角色、组成员、委托、tenant ownership 或资源策略边；完成条件是该 edge 位于实际求值路径，且 post-state 对同一资源/动作从 allow 变为 deny 或无法激活必要角色。[E2][E4]
>
> Authorization-Graph Edge Eviction Lockout varies valid authentication with loss of effective access through a negative graph delta. The adversary removes a direct or nested role, group membership, delegation, tenant ownership, or resource-policy edge. Completion requires that the edge was in the actual evaluation path and that post-state changes the same resource and action from allow to deny or prevents activation of a necessary role.[E2][E4]

### Stealth characteristics

> 授权图边撤除锁定使用户对象、密码、MFA 和成功登录保持正常，账户健康与认证告警可能全绿；异常隐藏在角色/组传递关系和资源求值中。DEV-0537 通过新建全局管理员移除其他管理员角色，局部事件仍是标准 role removal。graph old/new、移除发起者、newly-created admin、effective privilege、资源拒绝和紧急账户状态仍可揭示。[E2][E4]
>
> Authorization-Graph Edge Eviction Lockout leaves user object, password, MFA, and successful sign-in normal, so account health and authentication alerts can remain green. The anomaly lies in role or group transitivity and resource evaluation. DEV-0537 used a newly created Global Administrator to remove other administrator roles, while each local event remained a standard role removal. Graph old and new state, removing initiator, newly created administrator, effective privilege, resource denial, and emergency-account state remain revealing.[E2][E4]

### Scope boundary

> 纳入要求既有合法主体仍能认证，攻击者成功撤除其所需授权边，并证明资源访问、管理动作或角色激活实际失败。正常岗位调整、least privilege review、离职去权限、临时角色到期、PIM eligibility 变化和 fraud containment 是反例。攻击者同时给自己新增角色另记 NJT-0083/TA0004；不能以“其他管理员减少”推断攻击者权限提升。[L1]
>
> Inclusion requires an existing legitimate principal that can still authenticate, successful adversary removal of a required authorization edge, and actual failure of resource access, administrative action, or role activation. Normal role change, least-privilege review, offboarding, temporary-role expiry, PIM eligibility change, and fraud containment are counterexamples. Roles added to the attacker are separately mapped to NJT-0083 or TA0004, and fewer other administrators does not itself prove adversary privilege gain.[L1]

### Application scenario

> 攻击者取得 Role Management 或 tenant owner 权限后，可批量移除现有全局管理员、owner 或响应角色，让自身账户成为唯一控制者。DEV-0537 创建自身全局管理员并移除其他全局管理员，直接展示组织级管理访问被排除的场景。[E2]
>
> After obtaining Role Management or tenant-owner authority, an adversary can remove existing Global Administrators, owners, or response roles in bulk and leave an attacker account as sole controller. DEV-0537 created its own Global Administrator and removed the other Global Administrators, directly demonstrating organization-wide management exclusion.[E2]

### Attacker model

> 攻击者需要 role/group/owner removal 权限，理解嵌套组、PIM eligibility/activation、token 传播和紧急账户，并在被撤角色者恢复前完成关键动作。职责分离、移除 quorum、JIT/PIM、受保护 break-glass 与 owner 确认会阻止单一被盗管理员完成全局驱逐。
>
> The adversary needs role, group, or owner-removal authority, knowledge of nested groups, PIM eligibility or activation, token propagation, and emergency accounts, and time to complete critical actions before removed-role holders recover. Separation of duties, removal quorum, JIT or PIM, protected break-glass identities, and owner confirmation prevent one stolen administrator from completing global eviction.

### Defender model

> 防守方展开 effective graph，保存 assignment ID 与 old/new、关联新管理员来源、30 分钟移除 burst、紧急账户状态和 post-state resource decision。缓存 token、外部 SaaS 授权和未解析嵌套会让控制面 removal 与实际 deny 不一致。
>
> Defenders resolve the effective graph, retain assignment ID and old and new state, and correlate newly created administrator provenance, a 30-minute removal burst, emergency-account state, and post-state resource decision. Cached tokens, external SaaS authorization, and unresolved nesting can make control-plane removal differ from actual denial.

### Mechanism, defense, and limitations

`NM-BT`, primary, high confidence. Summary: **正常认证掩盖授权图中导致访问失败的撤边 / Successful authentication conceals the removed authorization edge causing access failure**.

> 攻击者只撤除授权关系，账户和认证器继续成功；身份登录面因此显示健康主体，资源面才出现 deny，管理面则记录角色/组删除。若防守不解析 graph 和 evaluation path，三处单独都像合法角色调整或普通授权失败，关键因果不可见，形成行为透明。assignment/edge ID、pre/post effective access 和具体 denied action 恢复链条。[E2][E4][E5]
>
> The adversary removes only authorization relationships while account and authenticator continue to succeed. The identity sign-in plane therefore shows a healthy principal, denial appears only at the resource plane, and the management plane records role or group deletion. Without resolving graph and evaluation path, each plane separately resembles legitimate role adjustment or ordinary authorization failure, leaving causality invisible and producing Behavioral Transparency. Assignment or edge ID, pre/post effective access, and the specific denied action recover the chain.[E2][E4][E5]

Detection coverage: proposed parent Strategy plus `TA0040-T1531-NJA-AUTHORIZATION-EDGE-EVICTION`. Mitigation coverage: extend MIT-000063 with this child application. Temporary claims: `TA0040-T1531-CLM-AUTHORIZATION-EVICTION` and `TA0040-T1531-CLM-AUTHORIZATION-DETECTION`; case candidate `TA0040-T1531-CASE-DEV0537-GLOBAL-ADMIN-EVICTION`.

> 目录日志能直接证明角色或成员边被移除，却不一定证明每个下游资源已拒绝访问；缓存 token、传播延迟、外部 SaaS 本地授权和不完整嵌套图都会造成差异。没有实际 evaluation path 或 verified denied action 时，应输出 eviction-risk 而非完成的 Impact。
>
> Directory logs directly prove removal of a role or membership edge but do not necessarily prove that every downstream resource denied access. Cached tokens, propagation delay, external SaaS-local authorization, and an incomplete nested graph all create differences. Without an actual evaluation path or verified denied action, output eviction risk rather than completed Impact.

## Evidence and shared-library candidates

Suggested parent Claims: `TA0040-T1531-CLM-ADAPT`, `TA0040-T1531-CLM-LOCKOUT-COMPLETION`, `TA0040-T1531-CLM-BOUNDARY`, and `TA0040-T1531-CLM-DEFENSE`. Child Claims and Cases are named above.

### Evidence ledger

| Key | Primary source and locator | Supported conclusion and limit |
| --- | --- | --- |
| E1 | MITRE ATT&CK 19.1 [T1531 Account Access Removal](https://attack.mitre.org/versions/v19/techniques/T1531/), definition, platforms, no-child inventory | Parent behavior, actual access-removal outcome, normal tools, Impact mapping; not sufficient alone for Niji children. |
| E2 | Existing `REF-000103`, Microsoft [DEV-0537/LAPSUS$](https://www.microsoft.com/en-us/security/blog/2022/03/22/dev-0537-criminal-actor-targeting-organizations-for-data-exfiltration-and-destruction/), “Exfiltration, destruction, and extortion” and hunting queries | Exact reuse. Actor-created admins removed all other Global Administrators, locking organization out; supports child 2 and its fields. |
| E3 | Microsoft Threat Intelligence, [Storm-2949 cloud-wide breach](https://www.microsoft.com/en-us/security/blog/2026/05/18/storm-2949-turned-compromised-identity-into-cloud-wide-breach/), SSPR section | Password reset, original-method removal, attacker method enrollment, and legitimate-user sign-in prevention; supports child 1. |
| E4 | Microsoft Graph, [directoryAudit resource](https://learn.microsoft.com/en-us/graph/api/resources/directoryaudit?view=graph-rest-1.0), properties/JSON | Real control-plane fields including initiator, targets, category, operation, result, correlation ID, and modified properties. |
| E5 | Microsoft Graph, [signIn resource](https://learn.microsoft.com/en-us/graph/api/resources/signin?view=graph-rest-1.0), properties/JSON | Real sign-in, resource, device, risk, Conditional Access, and failure-status fields; exact method ID may be absent. |
| E6 | Microsoft Entra, [Manage emergency access accounts](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access), guardrails | Two or more cloud-only emergency accounts, distinct phishing-resistant authentication, monitoring, and testing; tenant-lockout mitigation. |
| E7 | Existing `REF-000790`, Microsoft Entra [Revoke user access in an emergency](https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access), disable/revoke behavior | Exact reuse. Legitimate incident-response counterexample, session/token timing, and distinction between session revocation and durable state. |
| E8 | Existing `REF-000376`, Microsoft Entra [Sign-in logs](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins) | Exact reuse for sign-in categories/retention context; Graph schema E5 supplies exact fields. |
| E9 | Existing `REF-000143`, ATT&CK 19.1 [T1098 Account Manipulation](https://attack.mitre.org/versions/v19/techniques/T1098/) | Exact reuse for persistent added access-state boundary; no ATT&CK child is imported into T1531. |
| L1 | Existing `NJT-0083 Existing-Identity Access-State Manipulation` | Formal local owner for added parallel authenticators, authorization edges, and device trust preserving/raising attacker access. |
| L2 | Existing `NJT-0125 Central Defensive-Policy Impairment` | Formal local owner when central policy consumption broadly reduces identity/security defensive outcomes. |
| L3 | Existing `NJT-0093 Authentication-Decision Subversion` | Formal local owner for global authentication mechanism changes accepting attacker proofs. |

## Exact shared-library lookup and resolution advice

Required `library_lookup.py` searches were run for `identity defense impairment`, `identity account disable`, `account lockout`, `authentication policy impairment`, `session revocation`, `Account Access Removal`, `DEV 0537 LAPSUS global admin removal`, `Storm 2949 authenticator lockout`, `directoryAudit resource type`, `signIn resource type`, `emergency access accounts`, `revoke user access emergency`, and `DEV-0537 criminal actor targeting organizations`.

- **Reuse `REF-000103`, `REF-000790`, `REF-000376`, and `REF-000143`** at their exact stored meanings.[E2][E7][E8][E9]
- `CASE-000120` uses REF-000103 for DEV-0537 geography-proximate VPN/device-context alignment. Its central facts differ from global-admin eviction; recommend `create` a new child-2 Case rather than extend that case.
- `CASE-000061` records Storm-2949 VMAccess local-admin creation, a different later behavior. Create a new Storm SSPR/authenticator-displacement Case.
- No exact canonical source was returned for Storm-2949, Graph directoryAudit, Graph signIn schema, or emergency-access guidance. Recommend `create` References after URL lookup.
- `DET-000064`/`NJA-000043` detect **added** access edges and successful later use for persistence/privilege escalation. T1531 requires removed/replaced edges and failed victim access, so logic, outputs, windows, and tuning differ. Recommend `create` a new Strategy and two Analytics.
- **Extend `MIT-000063`** rather than create a duplicate. Its identity-state change authority, access-edge inventory, recoverable old values, and all-path recovery measures remain unchanged; add parent and two child Applications for negative access-state mutation and lockout recovery.

## Defense design

### Detection Strategy `TA0040-T1531-DET-IDENTITY-REMOVAL-TO-VICTIM-DENIAL`

Name: **身份负向变更—受害者访问失败谱系 / Negative Identity Mutation–Victim Access-Failure Lineage**. The Strategy confirms an existing legitimate principal, adversary-controlled negative state mutation, and concrete authentication or authorization failure. It holds state anomalies separately when no victim outcome exists and uses two Analytics for authenticator displacement and authorization-edge eviction.

### Shared data requirements

1. `entra-directory-audit`, channel Microsoft Graph `directoryAudits`: `id`, `activityDateTime`, `activityDisplayName`, `category`, `correlationId`, `initiatedBy.user.id/userPrincipalName/ipAddress`, `initiatedBy.app.appId/displayName`, `loggedByService`, `operationType`, `result`, `resultReason`, `targetResources[].id/displayName/type/userPrincipalName/modifiedProperties[].displayName/oldValue/newValue`, `additionalDetails`.[E4]
2. `identity-state-snapshot`, channel directory/IdP inventory: `snapshot_time`, `tenant_id`, `principal_id`, `user_principal_name`, `account_enabled`, `authenticator_id`, `authenticator_type`, `authenticator_owner_or_device`, `password_last_changed`, `role_assignment_id`, `role_definition_id`, `group_membership_id`, `delegation_id`, `policy_edge_id`, `resource_scope`, `valid_from`, `valid_until`, `parent_edge_id`.
3. `entra-signin`, channel Microsoft Graph `auditLogs/signIns`: `id`, `createdDateTime`, `userId`, `userPrincipalName`, `ipAddress`, `appId`, `appDisplayName`, `resourceId`, `resourceDisplayName`, `clientAppUsed`, `correlationId`, `conditionalAccessStatus`, `appliedConditionalAccessPolicies`, `isInteractive`, `deviceDetail.deviceId/operatingSystem/browser`, `location`, `riskLevelAggregated`, `riskState`, `status.errorCode/failureReason/additionalDetails`.[E5]
4. `resource-authorization-result`, channel target SaaS/IaaS/application audit: `timestamp`, `tenant_id`, `principal_id`, `session_or_token_id`, `resource_id`, `action`, `authorization_result`, `decision_reason`, `evaluation_path`, `role_assignment_or_edge_id`, `request_id`, `correlation_id`. Product mappings must be validated before formal platform expansion.
5. `identity-change-approval`, channel PIM/change/HR/fraud workflow: `case_or_change_id`, `case_type`, `requested_at`, `requester_id`, `target_principal_id`, `approved_operation`, `expected_old_state`, `expected_new_state`, `approver_id`, `owner_confirmation`, `window_start`, `window_end`, `status`.
6. `owner-access-report`, channel help desk/fraud/IR case: `case_id`, `reported_at`, `target_principal_id`, `verified_owner`, `reported_failure_stage`, `last_successful_access`, `usual_device_id`, `usual_ip_or_location`, `recovery_result`, `closed_at`.
7. `emergency-access-inventory`, channel protected tenant inventory: `principal_id`, `cloud_only`, `role_assignment_id`, `authenticator_type`, `credential_expiry`, `last_tested_at`, `last_used_at`, `account_enabled`, `monitoring_status`.[E6]

### Analytic 1 `TA0040-T1531-NJA-AUTHENTICATOR-DISPLACEMENT-LOCKOUT`

Logic:

1. Confirm target user existed in a trusted pre-state snapshot. Normalize successful password reset/change, authentication-method delete/add, recovery contact change, and account-enabled state from directoryAudit. Preserve exact method IDs and old/new where exposed; otherwise label principal-level.
2. Within **15 minutes**, group a recovery/reset sequence by tenant, target principal, initiator, correlation ID, and admin session. Flag removal of owner methods, password replacement, and enrollment of a method/device not in owner inventory, especially when one initiator repeats across users or lacks an approved recovery case.
3. Over **24 hours** or until verified recovery, join post-state sign-ins and owner reports. High-confidence child completion requires failure from a prior known owner device/location or verified owner report **and** no remaining approved authenticator path. A successful attacker sign-in from the new method strengthens attribution but is not required for victim Impact.
4. If only sessions/tokens were revoked and the same owner reauthenticates successfully with unchanged authenticators, classify legitimate/session-only response and close T1531. If account is disabled/deleted, route to parent-core branch rather than force child 1.
5. Use at least **90 days** for normal recovery initiator, device, location, method-type, and target-peer baselines. Exact method joins can span method lifetime; principal-only joins default to 24 hours and medium confidence.

Observables: SSPR/password reset followed by deletion of all prior phone/email/Authenticator methods and a new device-bound method; owner sign-in failures after a successful control-plane change; repeated recovery sequences across IT/leadership users from one unusual initiator.

False positives: legitimate owner-requested recovery; lost-phone/MFA migration; help-desk fraud containment; password rotation; user offboarding; break-glass exercise; synchronization delay causing temporary failures.

Blind spots: no authentication-method IDs; sign-in logs omit method used; owner does not report; active access token delays failure; federation/on-prem sync overwrites cloud state; attacker controls help desk/approval; legitimate user changes location/device simultaneously.

Tuning: baseline by user risk, peer role, normal help-desk initiators, method inventory, recovery source, and token lifetime; exceptions bind case ID, owner confirmation, target, exact method diff, operator, and expiry; never globally allow Authentication Administrators or self-service recovery.

### Analytic 2 `TA0040-T1531-NJA-AUTHORIZATION-EDGE-EVICTION`

Logic:

1. Normalize successful role/group/delegation/policy removal and preserve assignment/edge IDs, initiator, target, scope, old/new, and approval. Reconstruct pre/post effective graph including nested groups and PIM eligible/active state.
2. Use a **30-minute** burst window to identify one actor removing multiple Global Administrators, owners, responders, or one critical target's complete management paths. Raise provenance risk for a newly created/elevated initiator, unusual app, unmanaged IP/device, or missing change/HR/fraud record, following Microsoft's DEV-0537 hunting logic.[E2]
3. Over **24 hours** or propagation completion, join target sign-in and resource authorization. Child completion requires that authentication remains possible while the same resource/action or role activation becomes deny/unreachable because the removed edge was in the evaluation path. A directory role removal without a post-state result remains `eviction-risk`.
4. Independently evaluate attacker additions/privilege gains and map them to NJT-0083/TA0004. Never infer escalation merely because other admins lost access.
5. Check emergency access inventory immediately. Removal, disablement, expiry, or untested state of every independent recovery admin raises tenant-lockout severity; any emergency-account use is separately high priority.[E6]

Observables: a newly created Global Administrator removes all other Global Administrators; role/group removal followed by successful sign-in but denied admin action; multiple privileged edge removals with no offboarding case; emergency access paths disabled or unavailable.

False positives: approved least-privilege campaign; reorganization/offboarding; PIM eligibility expiry; role migration; compromised-account containment; tenant merger; automated entitlement review; mistaken emergency-account test.

Blind spots: incomplete nested graph; resource logs omit edge/evaluation path; cached tokens retain old roles; SaaS has local authorization outside Entra; propagation delay; external/B2B ownership; attacker controls approval or emergency inventory.

Tuning: baseline normal role-removal volume, initiator, scopes, and HR events; bind exceptions to assignment IDs, target list, owner, reason, approval, and window; use controlled before/after authorization tests for critical admin functions; preserve `authorization_unresolved` rather than assuming deny cause.

### Mitigation reuse: extend `MIT-000063 Durable Identity Access-State Governance and Recovery`

Existing measures remain unchanged: least identity-state change authority/strong approval, complete access-edge inventory and expiry, all-path recovery/evidence preservation, device-trust governance, and before/after effective-authority gating.

Parent application:

> 对管理合形式账户访问移除，把密码/认证方法删除、账户禁用/删除、角色/组/委托撤除列为负向高风险身份变更，要求隔离管理身份、抗钓鱼认证、JIT 权限、owner 或双人确认、精确 old/new 和可恢复前态。维护至少两个不同依赖的 cloud-only 紧急管理员并独立监控/定期测试。发现未批准移除时先保全变更与 post-state 失败，再通过受保护恢复主体还原 victim 的可信认证器和最小必要授权，同时撤销攻击者会话与新增路径。[E6]
>
> For Administration-Conforming Account Access Removal, treat password or authentication-method deletion, account disable or deletion, and role, group, or delegation removal as negative high-risk identity changes requiring isolated administrators, phishing-resistant authentication, JIT authority, owner or two-person confirmation, exact old and new state, and a recoverable pre-state. Maintain at least two cloud-only emergency administrators with different dependencies, independent monitoring, and regular tests. On unapproved removal, preserve mutation and post-state failure first, then use a protected recovery principal to restore trusted victim authenticators and minimum necessary authorization while revoking attacker sessions and added paths.[E6]

Expected effect:

> 破坏性身份变更需要通过更受保护的工作流，紧急管理员保留租户恢复入口，状态快照使负向 edge 可逆；攻击者必须同时攻陷多个独立控制。
>
> Destructive identity mutations require a more protected workflow, emergency administrators preserve tenant recovery entry, and state snapshots make negative edges reversible; the adversary must compromise multiple independent controls.

Limitations:

> 紧急账户本身是高权目标，排除 Conditional Access 需要严密 guardrail；缓存 token 与 SaaS 本地状态延迟恢复，错误回滚还可能恢复本应移除或已经失陷的用户。
>
> Emergency accounts are themselves privileged targets, and Conditional Access exclusions require strict guardrails. Cached tokens and SaaS-local state delay recovery, while erroneous rollback can restore a legitimately removed or compromised user.

Child 1 application:

> 对身份保留式认证器置换锁定，阻止单一管理员或 SSPR 流程在没有 owner/独立审批时删除最后一个批准认证器并绑定未知设备方法；保留 method ID 与前态，恢复时验证 owner 身份后重建至少一个可信路径并删除攻击者方法、token、session 和 device trust。
>
> For Identity-Preserving Authenticator Displacement Lockout, prevent one administrator or SSPR workflow from deleting the last approved authenticator and binding an unknown-device method without owner or independent approval. Preserve method IDs and prior state. During recovery, reverify owner identity, rebuild at least one trusted path, and remove attacker methods, tokens, sessions, and device trust.

Expected effect:

> 排他认证器置换更难完成，并能依据保存的 method state 快速恢复可信 owner 路径。
>
> Exclusive authenticator displacement becomes harder to complete and the saved method state enables rapid restoration of a trusted owner path.

Limitations:

> 真实丢失设备恢复有时必须移除最后一个旧方法；失陷的 owner proof 或帮助台仍可能满足工作流，部分平台不能恢复旧秘密而必须重新注册。
>
> Genuine lost-device recovery sometimes must remove the last old method. Compromised owner proof or help desk can still satisfy the workflow, and some platforms cannot restore old secrets and require fresh enrollment.

Child 2 application:

> 对授权图边撤除锁定，要求高价值 role/group/owner 的 removal 进行 before/after effective-access 模拟、职责分离和独立批准，禁止发起者同时成为唯一剩余管理员；保护并测试紧急管理员，保存 assignment edge，恢复时重建完整最小授权路径并刷新 token，而不是只重新添加显示角色。
>
> For Authorization-Graph Edge Eviction Lockout, require before-and-after effective-access simulation, separation of duties, and independent approval for removal of high-value roles, groups, or owners, and prevent the initiator from becoming the sole remaining administrator. Protect and test emergency administrators, preserve assignment edges, and during recovery rebuild the complete minimum authorization path and refresh tokens rather than only readding a displayed role.

Expected effect:

> 批量或唯一控制者驱逐会被阻断，或留下可立即恢复的授权图差分和独立管理入口。
>
> Bulk or sole-controller eviction is blocked or leaves an immediately recoverable authorization-graph differential and independent administrative entry.

Limitations:

> 有效权限模型可能遗漏外部 SaaS 和 deny 优先级，紧急账户仍可被针对；未经失陷调查就恢复角色可能把攻击者控制的身份重新送回高权位置。
>
> Effective-access models can miss external SaaS and deny precedence, and emergency accounts can still be targeted. Restoring roles without investigating compromise can return attacker-controlled identities to privilege.

Resolution: **extend**, not create. MIT-000063 already governs both addition and deletion of durable identity state and preserves recoverable old values. Add one parent and two child Applications after formal allocation; do not create a name-substituted duplicate.

## Content-depth and integration checks

- Parent and both children cover definition, trace change, residual observations, included/excluded behavior, scenarios, attacker prerequisites, defender visibility, mechanisms, evidence, limitations, and defense at NJT-0001 field responsibility depth.
- ATT&CK T1531 has no children; both proposed NJS objects arise from authentication-stage versus authorization-stage observation, not platform or operation names.
- Preserve actual victim failure as a hard completion gate. State mutation without lockout stays risk/exposure.
- Dual-map attacker additions to NJT-0083/TA0004 with separate edge/outcome evidence. Session revocation alone is not T1531.
- Reuse only confirmed shared objects and extend MIT-000063 only after target allocation. Strategy/Analytics remain new because their terminal outcome is failed victim access rather than added-edge use.
- Keep the first formal child `stealth_characteristics` paragraph beginning with its exact bilingual name, and do the same for child two.
- Keep lifecycle `review` after schema, quality, bundle, duplicate, bilingual Web/API, and human-content gates. This handoff allocates no IDs and modifies no canonical/shared/plan object.
