# T1657 research handoff — BATCH-TA0040-004

Research staging only. Every proposed new object uses temporary prefix `TA0040-T1657-`. No formal ID is allocated and no canonical matrix, decision, shared library, tactic plan, batch brief, reservation, gap analysis, or integration summary is modified.

## Admission recommendation

**Candidate:** ATT&CK Enterprise 19.1 T1657 Financial Theft / 金融盗窃. **Recommendation:** `adapt`, not exclude. **Parent confidence:** `high` for completed transfer; **stealth confidence:** `high` for beneficiary/account substitution and `medium-high` for linked post-receipt dispersion. **ATT&CK children:** zero. `original_attack_subtechniques_imported: false`.

**准入理由（中文）：** ATT&CK T1657 把勒索、BEC、银行攻击、加密资产盗窃及其他牟利活动放在一个很宽的目标概念下，其中许多 procedure 只证明凭据/钱包资料收集、勒索要求或“以盗窃为目标”，没有证明价值实际转移。Niji 不能保留这种泛化。建议把父级收敛为：受害方控制的资金、数字资产或等价可结算价值，经未授权支付/账本交易完成扣账并由攻击者或其受益账户取得控制。FinCEN、FBI、Mandiant 和联邦支付资料既证明这种完成结果，也支持两个独立匿迹变量：保留熟悉业务受益人外观但替换结算账户，以及到账后快速跨账户/机构拆分转移。因而准入 `adapt` 有足够证据；若主审不接受“实际结算”这一缩窄，则应 `exclude`，不应退回通用牟利父级。

**Admission rationale (English):** ATT&CK T1657 places ransomware, BEC, bank attacks, digital-asset theft, and other profit-seeking activity under a broad objective, while many procedures establish only credential or wallet-data collection, extortion demands, or intent to steal rather than actual value movement. Niji should not retain that generality. Adapt the parent to victim-controlled funds, digital assets, or equivalent settleable value that is debited through an unauthorized payment or ledger transaction and placed under adversary or beneficiary control. FinCEN, FBI, Mandiant, and Federal Reserve payment sources establish that completed outcome and two independent stealth variables: retaining a familiar business-beneficiary appearance while substituting the settlement account, and rapidly splitting value across accounts or institutions after receipt. The evidence supports `adapt`; if primary review rejects the completed-settlement narrowing, use `exclude` rather than a generic profit parent.

## Completion rule and adjacent boundaries

- **Completion / 完成标准:** T1657 is complete only when a payment/ledger record shows victim value debited and an adversary-controlled or fraud-beneficiary account/wallet credited or otherwise able to spend/control it. For the Fedwire implementation, `ACSC` (Accepted Settlement Completed), successful IMAD/OMAD, and receiving-side credit are stronger than instruction submission. `PDNG`, rejected, blocked, or merely approved transactions remain attempts. A later legitimate return/recovery changes recovery/net-loss state but does not erase the original completed unauthorized transfer.
- **NJT-0189 Resource Hijacking / 资源劫持:** NJT-0189 makes the victim bear compute, bandwidth, message, model-token, quota, or service cost while the attacker consumes a service. T1657 moves existing monetary/digital value to an adversary beneficiary through settlement. A cloud bill increase without value credited to the attacker is Resource Hijacking; a wire/asset transfer to an attacker account is Financial Theft.
- **T1565 Data Manipulation:** changing invoice data, transaction instructions, beneficiary fields, balances, or runtime values without completed value transfer is Data Manipulation. Once the altered instruction produces settled debit and fraud-beneficiary credit, T1657 also applies. Do not infer theft from a modified payment record that was blocked or corrected before settlement.
- **Credentials/account compromise:** credential theft, session hijacking, valid-account use, wallet-key collection, and privilege escalation are authority precursors. T1657 starts at actual transaction execution/settlement. RedLine collecting wallet credentials, for example, does not establish stolen assets without an on-chain transfer or equivalent ledger effect.
- **BEC/social engineering:** NJT-0118 Human-Trust Action Brokerage owns impersonation and induced legitimate user approval; phishing/BEC mail techniques own their communication traces. Financial Theft owns the later settled asset result. The proposed beneficiary/account child is not “BEC”: it can be produced by BEC, compromised ERP, direct bank account takeover, or malicious insider, and requires settlement-account mismatch plus completion.
- **Extortion:** a ransom or coercive demand without payment is not completed T1657. A victim payment that settles to the adversary is. Data encryption, exfiltration, leak threat, and negotiation retain their own objects.
- **Authorized fraud-response reversal / 获批欺诈响应冲正:** a bank hold, recall request, camt.056, pacs.004 return, chargeback, freeze, or ledger reversal executed by authorized responders to return stolen value is remediation, not another theft. Link it to the original UETR/IMAD/transaction, approval and responder identity. A rejected return request or unsuccessful recall does not reverse the original completed theft.

## Open-ended taxonomy review

T1657 has no ATT&CK children. Research examined beneficiary identity/account decoupling, post-receipt value dispersion, threshold-shaped structuring, established-session transaction camouflage, business-hour/holiday settlement timing, cross-rail conversion, human-authorized payment brokerage, and transaction-history alteration.

**Proposed Niji children:** `TA0040-T1657-CHILD-BENEFICIARY` Business-Beneficiary Settlement-Account Substitution / 业务受益人结算账户替换; `TA0040-T1657-CHILD-DISPERSION` Rapid Multi-Hop Value Dispersion / 快速多跳价值分散.

| Axis | Resolution | Reason |
|---|---|---|
| Familiar beneficiary identity with changed/new settlement account | `niji-variable-candidate` | FinCEN directly identifies known beneficiary/name with changed account information and unfamiliar account-history mismatches; it changes transaction features and preventive control. |
| Rapid splitting after receipt across accounts/institutions/countries | `niji-variable-candidate` | FBI documents victim funds entering one account then splitting to four banks; Mandiant documents APT38 transfers through multiple transactions to accounts at other banks/countries. Graph/time evidence and recovery differ. |
| Multiple small transfers below thresholds | `evidence-deferred` | Structuring is well established in AML, but reviewed sources do not sufficiently bind deliberate threshold shaping to one cyber-enabled victim theft and a distinct sibling beyond multi-hop dispersion. |
| Existing authenticated session/device | `adjacent-technique` | Session/account hijacking owns the observation variable; Financial Theft records settlement. A session alone cannot define a new child. |
| Human legitimate approval | `adjacent-technique` | NJT-0118 owns the user-brokered action; completed settlement remains parent/beneficiary child depending on account mismatch. |
| Transaction/history record alteration | `adjacent-technique` | T1565 owns data integrity change; T1657 requires the ledger value result. |
| Holiday/end-of-day timing | `evidence-deferred` | FinCEN notes limited verification time in fraudulent instructions, but current evidence does not establish a stable settlement-timing child independent of the instruction/BEC stage. |
| Currency/rail/crypto conversion | `not-stealth-distinct` | Rail and asset type are implementations. Conversion can be a hop in the dispersion child only when linked to the stolen value graph. |

The two children can combine but are non-interchangeable. The first keeps a stable business counterparty description while redirecting the initial settlement endpoint. The second changes the topology and time of value after or across completed transfers. One fraudulent payment to a substituted account need not be dispersed; a direct account takeover can disperse stolen funds without impersonating a vendor.

## Proposed parent field content

**Name / 名称:** 金融盗窃 / Financial Theft.

**Summary / 摘要:** 攻击者完成受害资金或数字资产向其受益方的未授权结算，并以受益人外观替换或快速多跳分散削弱交易识别、追踪和追回。 / Adversaries complete unauthorized settlement of victim funds or digital assets to their beneficiaries and use beneficiary-appearance substitution or rapid multi-hop dispersion to weaken recognition, tracing, and recovery.

### Definition and concept / 定义与概念

中文：金融盗窃是受害方控制的货币、证券、加密资产、礼品/储值或其他可结算价值，经未授权支付、提款、账本交易或智能合约转移，被攻击者、钱骡或其指定受益方实际取得控制。直接对象是所有权/可支配权与结算状态；盗窃完成需要受害方扣账和受益方可用 credit/control，而非攻击动机、勒索要求、凭据或支付指令本身。

English: Financial Theft is unauthorized payment, withdrawal, ledger transaction, or smart-contract transfer of victim-controlled money, securities, digital assets, gift or stored value, or other settleable value into actual adversary, mule, or designated-beneficiary control. The direct object is ownership or spend authority and settlement state. Completion requires victim debit and usable beneficiary credit or control, not profit motive, extortion demand, credentials, or payment instruction alone.

中文：概念锚连接原始资产/账户、发起主体和渠道、支付/账本唯一标识、受益账户/钱包、金额/资产、授权与业务依据、处理状态、结算/确认及后继返回。不同支付轨道的“完成”不同，必须使用该轨道的权威状态；在 Fedwire 中，成功消息的 IMAD/OMAD 和 `ACSC` 可证明处理/结算，return request 不是已返还资金。

English: The concept joins source asset or account, initiating principal and channel, payment or ledger unique identifier, beneficiary account or wallet, amount or asset, authorization and business basis, processing state, settlement or confirmation, and any later return. Completion differs by rail and requires its authoritative status. In Fedwire, successful-message IMAD/OMAD and `ACSC` establish processing or settlement, while a return request does not establish returned funds.

### Stealth characteristics / 匿迹特性

中文：金融盗窃可把异常隐藏在业务上熟悉的付款外观中。攻击者保留供应商/债权人名称、发票、金额和审批链，只替换账户号、银行/agent 或钱包，使只按显示名称与金额基线的检测把交易视为正常；FinCEN 明确把“已知 beneficiary、不同账户信息”和“beneficiary 名称与账户 holder 不符”列为 BEC red flags。真实异常集中在业务身份与结算标识的差分。

English: Financial Theft can hide anomaly inside a familiar business-payment appearance. The adversary preserves vendor or creditor name, invoice, amount, and approval chain while changing the account number, bank or agent, or wallet, causing name-and-amount baselines to treat the payment as ordinary. FinCEN explicitly lists a known beneficiary with different account information and mismatch between beneficiary name and account holder as BEC red flags. The anomaly resides in the differential between business identity and settlement identifier.

中文：到账后快速拆分会把一笔明显损失变成多个账户、机构、国家、币种或链上地址中的较小后继事件，使单机构和短窗口只能看到局部。FBI 的真实案例记录首个收款账户再分到四家银行，APT38 则经多笔交易把资金转至其他银行和国家。UETR/IMAD、账户、金额守恒、时间和 return/freeze 状态仍可恢复图谱，但跨机构可见性与隐私限制会断链。

English: Rapid splitting after receipt changes one conspicuous loss into smaller successor events across accounts, institutions, countries, currencies, or on-chain addresses, leaving one institution and short window with only a fragment. An FBI case records funds entering one account and then splitting to four banks, while APT38 transferred funds through multiple transactions to accounts at other banks and countries. UETR or IMAD, accounts, value conservation, time, and return or freeze state can recover the graph, but cross-institution visibility and privacy limits break links.

### Scope boundary definition / 范围边界界定

中文：纳入未授权交易已达到支付轨道的完成状态并把受害价值置于攻击者/受益方控制，同时至少一个正式匿迹变量有结论级证据。被拒、待定、冻结且未记入受益方、仅有恶意指令、仅修改数据、仅收集钱包/卡片/凭据或仅提出勒索要求都不完成父级。正常付款错误、重复支付、退款、内部资金归集和获批账户迁移是反例。

English: Include an unauthorized transaction that reaches the rail's completion state and places victim value under adversary or beneficiary control, with conclusion-level evidence for at least one formal stealth variable. Rejected, pending, or blocked transfers not credited to the beneficiary, malicious instructions alone, data modification alone, wallet/card/credential collection alone, and extortion demands alone do not complete the parent. Ordinary payment error, duplicate, refund, internal treasury sweep, and approved account migration are counterexamples.

中文：资源/云服务使用成本归 NJT-0189；未完成价值转移的数据操纵归 T1565；账户/会话控制、社交工程和 BEC 邮件归其前置对象。获批追回、冲正、chargeback、hold/freeze 和返还支付是响应状态，必须反向连接原交易，不因资金方向相反而被误记为第二次盗窃。

English: Resource or cloud-service usage cost belongs to NJT-0189, data manipulation without completed value transfer to T1565, and account or session control, social engineering, and BEC mail to their precursor objects. Authorized recovery, reversal, chargeback, hold or freeze, and return payment are response states that must link to the original transaction and cannot be mislabeled as a second theft merely because value direction reverses.

### Application scenarios / 应用场景

中文：BEC 行动可控制真实邮箱或伪造供应商，沿既有发票线程提供新的 beneficiary account，使财务人员发起看似符合金额与供应商历史的 wire；当支付到 `ACSC`/受益方 credit 后，T1657 成立。银行入侵行动可直接在 SWIFT/核心支付系统插入多笔欺诈交易并修改历史。加密资产场景中，用户被诱导批准恶意智能合约后，钱包资产链上转至攻击者地址；钓鱼与签名批准仍是前置。

English: A BEC operation can control a real mailbox or impersonate a supplier and provide a new beneficiary account in an existing invoice thread, causing finance staff to initiate a wire whose amount and vendor history appear ordinary. T1657 begins when payment reaches `ACSC` or beneficiary credit. A bank intrusion can directly insert multiple fraudulent transactions in SWIFT or core payment systems and alter history. In digital assets, a user can be induced to approve a malicious smart contract and wallet assets transfer on-chain to an adversary address; phishing and signature approval remain precursors.

### Attacker model / 攻击方模型

中文：攻击者需要能直接发起/批准交易，或影响可发起者，以及一个可接收并快速控制价值的银行账户、钱骡、wallet 或受益网络。账户替换要求了解供应商、金额、发票和付款周期；快速分散要求预置多个账户/机构/rail 并能在冻结前转出。双人审批、已验证 beneficiary 目录、实时 pre-validation、独立回呼、交易限额/hold 和跨机构快速冻结会限制效果。

English: The adversary needs direct transaction or approval authority, or influence over an authorized initiator, plus a bank account, mule, wallet, or beneficiary network able to receive and rapidly control value. Account substitution requires vendor, amount, invoice, and payment-cycle knowledge. Rapid dispersion requires staged accounts, institutions, or rails and outbound capability before freeze. Dual approval, validated beneficiary registry, real-time pre-validation, independent callback, transaction limit or hold, and rapid cross-institution freeze constrain the effect.

### Defender model / 防守方模型

中文：防守方可观察供应商主数据版本、账户变更与审批、发票/PO/付款请求、用户/会话、pacs.008 交易字段、IMAD/OMAD/UETR、`PDNG`/`ACSC`/`RJCT`、受益方 credit、内部账本、后继转出、camt.056/camt.029/pacs.004 和冻结状态。高质量判断需将业务 counterparty 身份与不可变结算账户标识分开，并跨至少到账后 24 小时构建价值图。邮件或银行单面可见、共享账户、correspondent 链、现金/crypto 转换及跨境隐私形成盲区。

English: Defenders can observe vendor-master versions, account changes and approval, invoice or PO or payment request, user or session, pacs.008 transaction fields, IMAD or OMAD or UETR, `PDNG`, `ACSC`, or `RJCT`, beneficiary credit, internal ledger, successor outflows, camt.056 or camt.029 or pacs.004, and freeze state. High-quality assessment separates business-counterparty identity from immutable settlement-account identifier and builds a value graph across at least the first 24 hours after receipt. Mail-only or bank-only visibility, shared accounts, correspondent chains, cash or crypto conversion, and cross-border privacy create blind spots.

### Supported parent mechanisms

`TA0040-T1657-MECH-BENEFICIARY` — `NM-FD`, primary. **Summary zh:** 熟悉受益人外观掩盖结算账户替换. **Summary en:** Familiar beneficiary appearance disguises settlement-account substitution. **Analysis zh:** 攻击者保留交易中的供应商名称、发票、金额或对话情境，只把 creditor account/agent 改为其控制标识；技术事件由合法人员/系统发起且外观匹配历史，按名称/金额分类的守方难以区分，形成特征伪装。主数据版本、账户历史和接收行 account-holder 可揭示差分。 **Analysis en:** The adversary preserves vendor name, invoice, amount, or conversation context and changes only the creditor account or agent to an attacker-controlled identifier. A legitimate person or system initiates the technical event and visible features match history, defeating name or amount classification and producing Feature Disguise. Vendor-master version, account history, and receiving-bank account holder reveal the differential. **Evidence:** E2–E4. **Confidence:** `high`.

`TA0040-T1657-MECH-DISPERSION` — `NM-ST`, secondary. **Summary zh:** 到账价值跨账户机构快速拆分使追踪与追回碎片化. **Summary en:** Rapid splitting across accounts and institutions fragments tracing and recovery. **Analysis zh:** 攻击者在首个受益账户到账后迅速把价值拆为多个后继转账/兑换，痕迹在账户、机构、地区和时间上分散，单机构只看到一段且召回窗口缩短，形成时空释痕。金额守恒、账户图、时间和 UETR/return 链可重建。 **Analysis en:** After first beneficiary credit, the adversary rapidly splits value into multiple successor transfers or conversions, dispersing traces across accounts, institutions, regions, and time. One institution sees one segment and the recovery window contracts, producing Spatiotemporal Trace Dilution. Value conservation, account graph, time, and UETR or return lineage can reconstruct it. **Evidence:** E5/E6. **Confidence:** `high` for observed BEC/APT38 cases, `medium` across rails.

### Parent taxonomy narrative / 父级分类叙述

中文：原生子项按结算链中被攻击者控制的观察差分划分。业务受益人结算账户替换保持业务身份/金额而改变 creditor account/agent，需要主数据—指令—结算三方差分；快速多跳价值分散在首笔完成后改变资金图拓扑与时间，需要到账—后继出账—return/freeze 图。前者发生在初始去向选择，后者发生在已到账价值的后继路径。

English: Native children divide the adversary-controlled observation differential in the settlement chain. Business-Beneficiary Settlement-Account Substitution preserves business identity and amount while changing creditor account or agent and requires a vendor-master-to-instruction-to-settlement differential. Rapid Multi-Hop Value Dispersion changes graph topology and timing after initial completion and requires a credit-to-successor-debit-to-return-or-freeze graph. The first acts on initial destination selection, while the second acts on the later path of credited value.

中文：BEC、被攻陷会话、账户 takeover、恶意 invoice 和交易历史修改是实现/前置，不构成子项。金额大小、支付 rail、币种、国内/跨境、银行/crypto 和收益用途均不是边界。若没有完成结算，taxonomy 不进入正式 T1657。

English: BEC, compromised session, account takeover, malicious invoice, and transaction-history modification are implementations or precursors rather than children. Amount, payment rail, currency, domestic or cross-border, bank or crypto, and profit use are not boundaries. Without completed settlement, the taxonomy does not enter formal T1657.

## Proposed child `TA0040-T1657-CHILD-BENEFICIARY`

**Name / 名称:** 业务受益人结算账户替换 / Business-Beneficiary Settlement-Account Substitution. **Confidence:** `high`.

### Definition and concept / 定义与概念

中文：业务受益人结算账户替换是攻击者保持付款方认知中的供应商、债权人、发票、金额或付款用途，却把支付消息中实际接收价值的 creditor account、wallet、agent 或 routing identifier 改为攻击者/钱骡控制标识，并使该交易完成结算。稳定变量是业务身份连续性与结算账户连续性之间的差分，而不是邮件、BEC 或账户 takeover。

English: Business-Beneficiary Settlement-Account Substitution preserves the payer's perceived vendor, creditor, invoice, amount, or payment purpose while changing the creditor account, wallet, agent, or routing identifier that actually receives value to an adversary or mule identifier and carrying the transaction through settlement. The stable variable is a differential between business-identity continuity and settlement-account continuity rather than email, BEC, or account takeover.

### Stealth characteristics / 匿迹特性

中文：业务受益人结算账户替换让名称、金额、发票和审批者仍与历史吻合，异常只落在 account/agent 与受益人历史、账户持有人或已验证目录不一致。只按显示 beneficiary 或金额阈值的检测可能放行；主数据修改、首次账户使用、receiving account holder、银行国家与独立确认仍可暴露。

English: Business-Beneficiary Settlement-Account Substitution leaves name, amount, invoice, and approver consistent with history and confines anomaly to account or agent mismatch against beneficiary history, account holder, or validated registry. Detection based only on displayed beneficiary or amount can allow it. Vendor-master change, first account use, receiving account holder, bank country, and independent confirmation remain revealing.

### Scope boundary definition / 范围边界界定

中文：纳入熟悉业务 beneficiary 与新的/不匹配结算标识共同存在，并有 `ACSC`/受益 credit 或等价完成证据的未授权交易。单纯伪造邮件归 NJT-0118，单纯修改 invoice/主数据归 T1565，未结算/被拒支付是企图。供应商真实换行、factor/escrow/“for further credit”、并购和获批 payout provider 是反例，须查 owner/证明材料。

English: Include unauthorized transactions where a familiar business beneficiary and new or mismatched settlement identifier coexist and `ACSC`, beneficiary credit, or equivalent completion is proven. Forged mail alone belongs to NJT-0118, invoice or master-data change alone to T1565, and unsettled or rejected payment is an attempt. Genuine vendor bank migration, factoring, escrow, “for further credit,” merger, and approved payout provider are counterexamples requiring owner and documentation.

### Application scenarios and threat model / 应用场景与威胁模型

中文场景：攻击者进入供应商或客户邮箱，沿真实 invoice thread 发送新的账户号，财务人员按正常 PO/金额完成 wire。FinCEN 还指出交易可命名已知 beneficiary 但账户 holder 并非该受益人，或已知 beneficiary 使用此前未用账户。FBI 案例记录骗子把 trusted account number 只改一个数字以降低怀疑。

English scenario: An adversary enters a vendor or customer mailbox and sends a new account number in a real invoice thread, after which finance staff completes a wire under the ordinary PO and amount. FinCEN also notes transactions naming a known beneficiary while the account holder differs, or using an account never used for that beneficiary. An FBI case records criminals changing a trusted account number by a single digit to reduce suspicion.

中文攻击方：攻击者需要业务关系/付款周期情报、能改变 instruction 或影响发起者，以及已准备的受益账户。账户名称核验、已验证 beneficiary directory、独立回呼和账户变更冷却会提高成本。若付款系统只检查 routing/account 格式而不核对 business identity，效果更强。

English attacker: The adversary needs business-relationship and payment-cycle intelligence, ability to change an instruction or influence the initiator, and a staged beneficiary account. Account-name verification, validated beneficiary directory, independent callback, and cooling-off after account change raise cost. The technique is stronger when payment systems validate only routing and account syntax without business-identity comparison.

中文防守方：防守方需要不可变 vendor/beneficiary 主数据历史、账户 owner/验证来源、instruction/approval、pacs.008 creditor/agent/account、UETR/IMAD/OMAD、状态和 receiving credit。共享/汇总账户、代理收款和 correspondent 链会产生合法差分；没有接收行 account-holder 数据时置信度下降。

English defender: The defender needs immutable vendor or beneficiary master history, account owner and verification source, instruction and approval, pacs.008 creditor, agent, and account, UETR or IMAD or OMAD, status, and receiving credit. Shared or collection accounts, payment agents, and correspondent chains create legitimate differentials. Confidence falls without receiving-bank account-holder data.

### Supported mechanism and limitations

Mechanism is `TA0040-T1657-MECH-BENEFICIARY` / `NM-FD`. **Limitation zh:** FinCEN red flags 高质量支持差分，却明确指出单一 red flag 不等于欺诈；正式结论仍需未经授权和完成结算。FBI 案例证明真实损失，但早期报道字段不等于每个支付 rail 的全部消息。 **Limitation en:** FinCEN strongly supports the differential while explicitly warning that no single red flag proves fraud; formal conclusions still require unauthorized context and completed settlement. FBI cases establish real loss, but reported fields do not substitute for every rail's message semantics.

## Proposed child `TA0040-T1657-CHILD-DISPERSION`

**Name / 名称:** 快速多跳价值分散 / Rapid Multi-Hop Value Dispersion. **Confidence:** `high` for bank-transfer cases, `medium` cross-rail.

### Definition and concept / 定义与概念

中文：快速多跳价值分散是攻击者在受害价值首次结算至受益账户后，在追回或冻结前把该价值全部或部分拆分到多个后继账户、机构、国家、币种或链上地址，使原始交易与最终控制点之间形成短时扩张的价值图。稳定变量是到账后的分支数、hop、时间和价值守恒，不是银行、crypto 或钱骡名称。

English: Rapid Multi-Hop Value Dispersion splits all or part of victim value after first beneficiary settlement across successor accounts, institutions, countries, currencies, or on-chain addresses before recovery or freeze, creating a rapidly expanding value graph between original transaction and final control points. The stable variable is post-credit branching, hops, time, and value conservation rather than bank, crypto, or mule naming.

### Stealth characteristics / 匿迹特性

中文：快速多跳价值分散把单笔异常变成不同账本上的多个局部事件，金额可与普通出账混合，原始银行只看到出境，后继银行只看到来源账户。资金图的空间碎片化与极短时间压缩降低关联和冻结成功率；账户年龄、到账后出账比例、受益数量、共享 UETR/金额/时间和跨机构 intelligence 仍可揭示。

English: Rapid Multi-Hop Value Dispersion turns one anomaly into local events on different ledgers, where amounts can blend with ordinary outflows; the originating bank sees departure and later institutions see only the preceding account. Spatial fragmentation and short timing reduce correlation and successful freeze. Account age, post-credit outflow fraction, beneficiary count, linked UETR, value and time, and cross-institution intelligence remain revealing.

### Scope boundary definition / 范围边界界定

中文：纳入可与已完成受害转账建立价值/时间/账户关联的快速后继拆分。没有原始未授权受害交易的普通洗钱图不进入 T1657；正常 treasury sweep、payroll、merchant acquiring、broker settlement、escrow disbursement、correspondent pass-through 和获批现金归集是反例。单次换汇或单一转出没有多跳/分支证据时留在父级。

English: Include rapid successor splitting that can be linked by value, time, and account to a completed unauthorized victim transfer. An ordinary laundering graph without the originating victim theft does not enter T1657. Treasury sweeps, payroll, merchant acquiring, broker settlement, escrow disbursement, correspondent pass-through, and approved cash concentration are counterexamples. One conversion or one onward transfer without branch or multi-hop evidence remains parent-level.

### Application scenarios and threat model / 应用场景与威胁模型

中文场景：FBI 记录房地产 BEC 受害者首付款进入犯罪账户后被拆分并转往四家银行，数日内准备出境。Mandiant 记录 APT38 在银行环境插入欺诈 SWIFT 交易，经多笔交易转至其他银行、通常在不同国家以支持洗钱。两例都证明跨账户拓扑和追回窗口差异。

English scenario: The FBI records a real-estate BEC down payment entering a criminal account, then being split and sent to four banks with onward movement abroad expected within days. Mandiant records APT38 inserting fraudulent SWIFT transactions and transferring funds through multiple transactions to accounts at other banks, usually in different countries, to enable laundering. Both establish the cross-account topology and recovery-window difference.

中文攻击方：攻击者需要预置钱骡/账户/wallet、足够出账权限、跨机构路径和在冻结前完成 hop 的自动化或协调。新账户 hold、到账后 velocity 限制、cross-bank intelligence 和快速法律/支付响应会降低成功率。拆分增加账户与手续费暴露，也可能产生 value-conservation graph。

English attacker: The adversary needs staged mules, accounts, or wallets, sufficient outbound authority, cross-institution paths, and automation or coordination to complete hops before freeze. New-account holds, post-credit velocity limits, cross-bank intelligence, and rapid legal or payment response reduce success. Splitting also exposes more accounts and fees and can produce a value-conservation graph.

中文防守方：防守方需要入账/出账 ledger、booking/value/settlement 时间、账户年龄/owner、counterparty/agent、金额/币种、UETR/IMAD/OMAD、channel/device、hold/freeze/return 及跨机构 intelligence。在单机构视图、现金提取、privacy coin/mixer、预付卡、nested account 和境外不可见 rail 中形成盲区。

English defender: The defender needs inbound and outbound ledger, booking, value and settlement time, account age and owner, counterparty and agent, amount and currency, UETR or IMAD or OMAD, channel or device, hold, freeze or return, and cross-institution intelligence. Blind spots arise under single-institution views, cash withdrawal, privacy coins or mixers, prepaid cards, nested accounts, and opaque foreign rails.

### Supported mechanism and limitations

Mechanism is `TA0040-T1657-MECH-DISPERSION` / `NM-ST`. **Limitation zh:** FBI 案例直接证明一入四行，APT38 报告直接证明多笔跨银行/国家，但公开资料没有完整 transaction IDs 与金额守恒表。正式 CASE 只能保留来源明确事实；精确图阈值需机构数据验证。 **Limitation en:** The FBI case directly establishes one receipt followed by four banks, and APT38 reporting directly establishes multiple transactions across banks and countries, but public sources do not publish complete transaction IDs and value-conservation tables. Formal CASE objects must retain only sourced facts; exact graph thresholds require institutional data.

## Detection Strategy and Analytics

### `TA0040-T1657-DET-SETTLEMENT` — Business Instruction to Settlement and Successor Value Graph / 业务指令到结算与后继价值图

**Objective:** identify unauthorized value transfers through business-identity/account mismatch before settlement where possible, prove completion from rail status, and trace/freeze post-credit dispersion. Initial implementation is Fedwire ISO 20022 plus internal ERP/ledger; do not copy field names to ACH, card, or blockchain rails without schema and finality validation.

#### `TA0040-T1657-NJA-BENEFICIARY-SETTLEMENT`

**Logic:** Ingest immutable vendor/beneficiary master revisions (`vendor_id`, business name, tax/legal ID, creditor account and type, routing/BIC, bank country, verification method, verified contact, revision time, changed by, approval/change ID) and ERP payment context (`invoice_id`, PO/contract, amount, currency, due date, requester, approvers, approval timestamps, device/session, instruction source). Parse Fedwire pacs.008 and status/advice fields: Message Identification, creation time, Instruction Identification, End-to-End Identification, Transaction Identification, UETR, debtor/debtor account/agent, creditor/creditor account/agent, ultimate debtor/creditor where present, interbank settlement amount/currency/date, purpose/remittance, IMAD, OMAD, and pacs.002 status (`PDNG`, `ACSC`, `RJCT`).

At message creation, compare creditor business identity and invoice to the last independently verified account/agent and account-holder result. Score first-use account, recently changed master, name/account-holder mismatch, foreign/new agent, familiar amount with new account, missing out-of-band confirmation, new initiator/device, and urgency/instruction-source context. Alert before release and place a risk hold where authorized. If sent, join the same UETR/IMAD/OMAD to `ACSC` and receiving credit. Emit attempt/prevented for rejection/hold, and completed T1657 only on settlement plus unauthorized/fraud-beneficiary evidence.

**Windows:** master/instruction lookback should cover at least the organization's vendor-change and invoice cycle; use 90 days as an initial local baseline, not a universal standard. Join instruction/change to transaction for up to that cycle. Settlement status is real-time/event-driven; `PDNG` must resolve to `ACSC` or `RJCT` by Fedwire close of business. On `ACSC`, open a 24-hour priority recovery window because FinCEN reports greater BEC recovery success when reported within 24 hours.

**Correlation dimensions:** vendor/business counterparty, verified account/agent, invoice/PO, UETR, IMAD/OMAD, debtor account, creditor account/agent, amount/currency, initiator/approver/session, master revision, time.

**False positives:** genuine vendor bank change, factoring, escrow or collection account, merger/acquisition, one-time supplier, correspondent/intermediary routing, pay-on-behalf/ultimate creditor, tax/payment provider, emergency refund, legitimate new country.

**Blind spots:** third-party ERP or bank portal lacks export, free-text account instructions, beneficiary-owner data unavailable, shared/omnibus account, tokenized account ID, compromised authorized approver, correspondent chain, payment outside monitored rail, fraudulent party controls callback channel.

**Tuning:** require dual approval and known-channel verification for new account, register factoring/collection relationships and expiry, retain first-use risk after approval rather than permanent allow, and never classify `ACSC` alone as theft. **Evidence:** E2–E4, E7–E10.

#### `TA0040-T1657-NJA-VALUE-DISPERSION`

**Logic:** Starting from the confirmed or high-risk inbound beneficiary credit, ingest receiving-bank/internal ledger with transaction ID, account ID and owner, debit/credit indicator, amount/currency, booking/value/settlement time, balance, channel/device/session, counterparty account and agent/BIC/routing, country, and hold/freeze/return state. Preserve Fedwire UETR/IMAD/OMAD for the original payment and the distinct identifiers of successor payments; new onward transfers do not inherit one UETR, so link by credited account, amount conservation, time and counterparty graph rather than fabricating UETR continuity.

Over the first 24 hours after credit, compute outbound fraction of the suspicious inbound amount, branch count, distinct accounts/agents/institutions/countries, account age, dwell time, currency/rail conversions, cash/crypto exits, and remaining balance. Extend graph review to 72 hours for slower rails, documented as a local investigative horizon. Raise severity on rapid near-total pass-through, split across new recipients, or network-level intelligence linking the same beneficiary to same-amount/currency payments from other institutions. Join camt.056 return request, camt.029 response, freeze/hold, and actual pacs.004 return; a request without return is not recovery.

**Settlement semantics:** Fedwire credits are final at the rail level; a return requires beneficiary/receiving participant action. The service imposes no date restriction on return requests or payment returns, but FinCEN's observed 24-hour reporting advantage justifies priority monitoring, not a claim that recovery is impossible after 24 hours.

**Correlation dimensions:** original UETR/IMAD/OMAD, receiving account and owner, ledger transaction IDs, amount/currency, successor accounts/agents, booking/value time, account age, channel/device, return/freeze status.

**False positives:** corporate treasury/cash concentration, payroll, merchant acquiring, marketplace settlement, securities/broker clearing, escrow disbursement, correspondent/pass-through bank, remittance business, loan syndication, approved crypto exchange, disaster liquidity sweep.

**Blind spots:** no cross-bank data, cash withdrawal, prepaid/gift cards, nested/omnibus accounts, correspondent opacity, privacy coins/mixers, foreign legal delay, amount altered by fees/FX, internal ledger latency, recipient identity unavailable.

**Tuning:** baseline account role and expected sweep destinations, compare value fraction rather than one fixed amount, require source-theft context before labeling laundering activity as T1657, and preserve legitimate return transactions through original-reference linkage. **Evidence:** E5/E6, E9/E11.

## Mitigation candidates

### `MIT-000116` candidate `extend` — High-Risk Request Provenance and Independent Confirmation

The existing `independent-action-confirmation` measure explicitly covers payment. Add a T1657 parent/beneficiary-child application: verify bank-account changes through previously known supplier contacts and authoritative vendor directory, require dual approval outside the compromised mail thread, and bind confirmation evidence to the payment UETR/instruction. **Expected effect:** control of one email/session or forged instruction cannot redirect settlement alone. **Limitations:** compromise of vendor, directory and callback together can bypass; alert fatigue and emergencies need audited exceptions; confirmation without checking the exact account/agent is insufficient.

### `TA0040-T1657-MIT-SETTLEMENT` candidate `create`

**Name:** Beneficiary Master, Settlement Hold, and Rapid Recovery Governance / 受益人主数据、结算暂缓与快速追回治理.

**Measures:** (1) immutable beneficiary/account master history, independent account-holder/pre-validation, dual approval and cooling-off for new/changed accounts; (2) risk-based pre-settlement hold, per-transaction/beneficiary limits, positive beneficiary allowlist and first-use review; (3) real-time owner and fraud operations coverage for `PDNG`/`ACSC`, beneficiary credit, unusual post-credit outflows and cross-institution intelligence; (4) tested recovery playbook linking original UETR/IMAD/OMAD to camt.056, camt.029, freeze/hold and pacs.004, plus IC3/law-enforcement escalation within the first 24 hours; (5) require explicit approval and original-transaction linkage for legitimate reversal/return so response is not blocked as fraud.

**Parent application:** apply owner/account verification and hold to high-risk transfers, then maintain settlement/return state until value is recovered or investigation closes. **Expected effect:** prevents unverified destination change, reduces completed theft, and shortens freeze/return delay. **Limitations:** Fedwire finality means return is not guaranteed; holds delay legitimate urgent payments; not all receiving institutions share owner/graph data; legal jurisdiction and weekend coverage matter.

**Beneficiary-child application:** lock vendor account edits to independent workflow, compare displayed beneficiary with receiving account holder, and require exact account/agent confirmation. **Expected effect:** familiar invoice/name cannot carry a substituted settlement account through approval. **Limitations:** factoring/escrow/omnibus accounts create valid name differences; receiving-bank owner data may be unavailable.

**Dispersion-child application:** place enhanced monitoring/temporary holds on newly opened or mule-risk accounts, detect rapid pass-through, coordinate cross-bank freeze, and link actual return to original theft. **Expected effect:** reduces hop count before intervention and preserves a reconstructable value graph. **Limitations:** cash/crypto exits and foreign institutions can outrun holds; overbroad controls harm legitimate treasury/payment businesses.

## Evidence and conclusion-level sources

| Key | Primary source and locator | Support and limit |
|---|---|---|
| E1 `TA0040-T1657-REF-ATTACK` | [MITRE ATT&CK Enterprise v19 T1657](https://attack.mitre.org/versions/v19/techniques/T1657/) and fixed 19.1 inventory | Parent tactic and breadth; too broad to prove completed settlement or Niji children; new REF. |
| E2 `TA0040-T1657-REF-FINCEN-BEC` | [FinCEN FIN-2016-A003](https://www.fincen.gov/resources/statutes-regulations/guidance/advisory-financial-institutions-e-mail-compromise-fraud), stages, red flags, recovery guidance | Executed unauthorized wires, known beneficiary/different account, holder mismatch, independent verification, often-irrevocable transfers and 24-hour recovery advantage; new REF. |
| E3 `TA0040-T1657-REF-FBI-BEC-STORY` | [FBI: Business E-Mail Compromise](https://www.fbi.gov/news/stories/business-e-mail-compromise), case and account-number discussion | Real $737k wire, familiar workflow, single-digit account substitution, extremely short recovery window; new REF/CASE. |
| E4 `TA0040-T1657-REF-FBI-BEC-GUIDE` | [FBI: Business Email Compromise](https://www.fbi.gov/how-we-can-help-you/common-frauds-and-scams/business-email-compromise) | Real beneficiary-instruction scenarios and immediate institution contact; new REF. |
| E5 `TA0040-T1657-REF-FBI-MULE` | [FBI: Your Bank Account Could Be Fueling Crime](https://www.fbi.gov/news/stories/money-muling-is-illegal-120419), Cole case | Completed down-payment theft into one account, split to four banks and expected onward movement abroad; new REF/CASE. |
| E6 `TA0040-T1657-REF-MANDIANT-APT38` | [Mandiant: APT38](https://cloud.google.com/blog/topics/threat-intelligence/apt38-details-on-new-north-korean-regime-backed-threat-group/), lifecycle “Transfer funds” | Inserted fraudulent SWIFT transactions and multiple transfers to accounts at other banks/countries; transaction history alteration is adjacent T1565; new REF/CASE. |
| E7 `TA0040-T1657-REF-FEDWIRE` | [Fedwire Funds Service](https://www.frbservices.org/financial-services/wires/fedwire-funds-service/), service/finality/FAQ | Same-day settlement, master-account finality, IMAD/OMAD success, camt.110/camt.056 functions; new REF. |
| E8 `TA0040-T1657-REF-FEDWIRE-ISO` | [Fedwire ISO 20022 Format FAQ](https://www.frbservices.org/resources/financial-services/wires/fedwire-services-frequently-asked-questions/fedwire-service-iso-20022-faq/format-faq/), value status, UETR, return messages | `PDNG`, `ACSC`, `RJCT`; UETR/EndToEndId; camt.056/camt.029/pacs.004 and no date restriction. New REF. |
| E9 `TA0040-T1657-REF-FEDWIRE-FIELDS` | [Fedwire International Wires](https://www.frbservices.org/binaries/content/assets/crsocms/resources/resource-centers/fedwire-funds-service-international-wire.pdf) | Creditor name/address/account and agent information; new REF. |
| E10 `TA0040-T1657-REF-SWIFT-PREVALIDATION` | [Swift Payment Pre-validation](https://www.swift.com/myswift/ordering/changereplace-upgrade/payment-pre-validation) | Real-time beneficiary account verification with ultimate receiving bank; new REF. |
| E11 `TA0040-T1657-REF-SWIFT-CONTROLS` | [Swift fraud targeting banks' customers](https://www.swift.com/risk-and-compliance/fraud/fraud-targeting-banks-customers) | Network-level same amount/currency/beneficiary insight and transaction fraud monitoring; new REF. |
| E12 `TA0040-T1657-REF-MANDIANT-CLINKSINK` | [Mandiant: CLINKSINK Solana drainers](https://cloud.google.com/blog/topics/threat-intelligence/solana-cryptocurrency-stolen-clinksink-drainer-campaigns/) | Completed digital-asset theft after malicious approval, estimated observed campaign value; parent scenario only. New REF/CASE candidate. |
| E13 `REF-000570` | [Microsoft: Behind the Scenes of BEC](https://www.microsoft.com/en-us/security/blog/2021/06/14/behind-the-scenes-of-business-email-compromise-using-cross-domain-threat-data-to-disrupt-a-large-bec-infrastructure) | Existing reference for BEC mailbox/rule precursor; boundary/context only, not settlement proof. Reuse if cited. |
| E14 `REF-000404` | [ATT&CK Social Engineering T1684](https://attack.mitre.org/versions/v19/techniques/T1684) | Existing NJT-0118 boundary and independent-confirmation mitigation context; not T1657 evidence. Reuse only for boundary. |

## Shared-library lookup and resolution record

Executed `library_lookup.py` with: `Financial Theft T1657`; `FinCEN email compromise beneficiary account information`; `BEC wire transfer fraudulent beneficiary`; `APT38 SWIFT multiple transactions`; `Fedwire UETR IMAD OMAD beneficiary`; `rapid dispersion mule funds multiple banks`; `financial fraud settlement transaction`; and `payment controls beneficiary account`.

- **References:** no exact T1657, FinCEN, FBI settlement, APT38 transfer, Fedwire or Swift payment-control REF matched. Create E1–E12. Reuse `REF-000570` and `REF-000404` only for precursor/boundary if canonical prose mentions them.
- **Cases:** create `TA0040-T1657-CASE-FBI-BEC-ACCOUNT-SUBSTITUTION` from E3; `TA0040-T1657-CASE-COLE-MULTIBANK-DISPERSION` from E5; `TA0040-T1657-CASE-APT38-SWIFT` from E6. Optionally create CLINKSINK parent case from E12, but do not infer the two proposed children without account/dispersion evidence.
- **Claims:** `TA0040-T1657-CLM-COMPLETION` (settled debit/credit versus attempt; E2/E7/E8); `TA0040-T1657-CLM-BENEFICIARY` (known identity/different account mismatch; E2/E3); `TA0040-T1657-CLM-DISPERSION` (post-credit split and cross-bank path; E5/E6); `TA0040-T1657-CLM-FEDWIRE-FIELDS` (E7–E9); `TA0040-T1657-CLM-RECOVERY-WINDOW` (24-hour advantage and return semantics; E2/E8); `TA0040-T1657-CLM-DIGITAL-ASSET` (E12).
- **Detection:** DET-000115/NJA-000103 detect trust request to user action but do not prove payment settlement; T1565 detection will own instruction/data modification; NJT-0189 analytics own metered service cost. No exact settlement/value-graph object exists. Create `TA0040-T1657-DET-SETTLEMENT` and its two NJAs.
- **Mitigation:** extend MIT-000116 for independent payment confirmation. Create transaction-master/hold/recovery governance for destination integrity and rail response. Do not reuse MIT-000197/198: their control identity is resource usage/transaction admission for metered services, not value ownership transfer.
- **Relationships:** future links to NJT-0118, T1565, credential/account compromise, and return actions require formal IDs and evidence; co-occurrence is not identity.

## Rejected/deferred conclusions and limitations

中文：ATT&CK 的许多 procedure 只描述钱包凭据、信用卡资料、勒索或财务动机；正式父级不得复用这些作为已完成盗窃证据。受益人替换资料高质量但多数来自 BEC，主审必须保持变量可由 direct takeover/insider/ERP manipulation 实现，而不是把 BEC 变成 T1657 子项。多跳来源公开了账户数量和跨行事实，却缺完整 IDs/amounts；检测阈值必须在机构数据验证。Fedwire 状态与字段不能照搬 ACH、card、SEPA、crypto；每条 rail 需独立 finality/return 语义。

English: Many ATT&CK procedures establish wallet credentials, card details, extortion, or financial motive only; the formal parent cannot reuse them as completed-theft evidence. Beneficiary-substitution evidence is strong but often comes from BEC, so primary review must preserve a variable implementable through direct takeover, insider, or ERP manipulation rather than make BEC a T1657 child. Public multi-hop sources disclose account count and cross-bank movement but not complete IDs or values; analytic thresholds require institutional validation. Fedwire status and fields cannot be copied to ACH, card, SEPA, or crypto rails; each rail needs independent finality and return semantics.

Compared with NJT-0001 by field responsibility, parent and both children define direct behavior, stable variable, trace change, defender-observation effect, residual evidence, inclusion/exclusion, scenarios, attacker prerequisites, defender model, mechanisms, defense differences, primary evidence, and calibrated limitations. If canonical integration cannot preserve completed settlement as the parent gate, recommendation changes to `exclude`.

**Integration status:** pending all three final-batch handoffs, primary cross-technique convergence, shared-library resolution, formal allocation, canonical YAML, tactic closure, quality, Bundles, Web/API QA, and human review. Only this staging file was written.
