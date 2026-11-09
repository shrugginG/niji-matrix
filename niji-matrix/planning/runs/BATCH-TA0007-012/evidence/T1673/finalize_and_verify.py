# Archived one-shot authoring script; do not rerun against the frozen handoff.
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, re, yaml, copy

ROOT = Path(__file__).resolve().parents[5]
# ROOT is canonical niji-matrix: planning/runs/batch/evidence/T1673/file -> five parents.
BATCH = Path(__file__).resolve().parents[2]
EVIDENCE = Path(__file__).resolve().parent
HANDOFF = BATCH / 'T1673-research-handoff.yaml'
VERIFY = BATCH / 'T1673-evidence-verification.yaml'
OVERRIDES = BATCH / 'T1673-primary-overrides.yaml'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

class StrictLoader(yaml.SafeLoader):
    pass

def strict_mapping(loader, node, deep=False):
    out = {}
    for k, v in node.value:
        key = loader.construct_object(k, deep=deep)
        if key in out:
            raise ValueError('Duplicate YAML key: ' + str(key))
        out[key] = loader.construct_object(v, deep=deep)
    return out
StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, strict_mapping)

class Extractor(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip = max(0,self.skip-1)
    def handle_data(self, data):
        if not self.skip and data.strip(): self.parts.append(data.strip())

handoff = yaml.load(HANDOFF.read_text(), Loader=StrictLoader)
override_hash = sha(OVERRIDES)
for edit in json.loads(OVERRIDES.read_text())['content_edits']:
    parts=edit['pointer'].strip('/').split('/')
    obj=handoff
    for p in parts[:-1]: obj=obj[int(p)] if isinstance(obj,list) else obj[p]
    p=parts[-1]
    if isinstance(obj,list): obj[int(p)]=edit['value']
    else: obj[p]=edit['value']
assert sha(OVERRIDES)==override_hash
# Primary overrides are applied mechanically; their source file is preserved byte-for-byte.
HANDOFF.write_text(yaml.safe_dump(handoff, allow_unicode=True, sort_keys=False, width=110))

manifest=json.loads((EVIDENCE/'download-manifest.json').read_text())
for item in manifest:
    raw=ROOT/item['raw_path']; text_path=ROOT/item['text_path']
    assert sha(raw)==item['sha256'], ('Raw evidence changed',raw)
    parser=Extractor(); parser.feed(raw.read_bytes().decode('utf-8',errors='strict'))
    text_path.write_text('\n'.join(parser.parts),encoding='utf-8')
    item['text_encoding']='utf-8'
    item['text_bytes']=text_path.stat().st_size
    item['text_sha256']=sha(text_path)
(EVIDENCE/'download-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')

# These facts and limits were independently authored from the sources; only their serialization is automated.
facts={
'crowdstrike-hypervisor-part2': {
 'reference_key':'B012-T1673-REF-CROWDSTRIKE',
 'locator':'PINCHY SPIDER and REvix Table 2; VIKING SPIDER and Ragnar Locker Table 3; How to Protect Your Cluster',
 'facts':{'zh':'2021年8月30日Michael Dawson的原始报告分别记录REvix选WorldID/DisplayName的CSV枚举管线，以及VIKING SPIDER列运行VM、按World ID处理并再次查询的命令序列。后者为本交接VIKING案例的唯一中心；正常用途对照来自官方故障排查资料。','en':'Michael Dawson’s original 30 August 2021 report separately records the REvix CSV pipeline selecting WorldID/DisplayName and the VIKING SPIDER sequence listing running VMs, acting by World ID, and querying again. Only the latter centers the proposed VIKING case; the legitimate-use contrast comes from official troubleshooting.'},
 'limits':{'zh':'正文since June2021是部署背景，本枚举具体日期及行业未知，命令表不是所有运行时原始返回。没有伪装动机证明、对照检测率或漏检测量。','en':'The text’s since-June-2021 statement is deployment background; exact enumeration dates and sectors are unknown. Command tables are not all runtime raw returns. No camouflage motive, comparative detection rate, or miss measurement is established.'},
 'evidence_level':'reported-malicious-command-sequence'},
'play-trendai': {
 'reference_key':'B012-T1673-REF-TREND',
 'locator':'Publication metadata; Infection Routine of the Linux Variant of Play Ransomware; command preceding Figure 6',
 'facts':{'zh':'已取得迁移后的完整原始出版，日期为2024年7月19日，列七名作者。正文getallvms首列送入逐VMID循环，支持样本查询及标识使用设计。','en':'The complete migrated original publication was obtained, dated 19 July 2024 with seven authors. Its getallvms first column feeds a per-VMID loop, supporting sample query and identifier-use design.'},
 'limits':{'zh':'旧TrendMicro URL在浏览时只给导航，现用验证过的TrendAI同出版别名，非另一份REF。图6文字提esxcli而命令为vim-cmd，以具体代码为准。样本操作日期null、行业空，不导入全组统计或VT零检出为机理效果。','en':'The old TrendMicro URL returned navigation during browsing; the verified TrendAI alias is the same publication, not a second REF. Figure 6 mentions esxcli while the command uses vim-cmd; use the concrete code. Sample operation time is null and sectors empty; neither group-wide statistics nor zero VirusTotal detections establish this mechanism’s effect.'},
 'evidence_level':'original-sample-analysis'},
'esxcli-vm': {
 'reference_key':'B012-T1673-REF-ESXCLI',
 'locator':'vm process list; vm process kill --world-id',
 'facts':{'zh':'命令参考明确list当前仅列运行VM，World ID可用于独立kill命令。','en':'The command reference explicitly limits list to running VMs and makes World ID an input to a separate kill command.'},
 'limits':{'zh':'这是功能及对象合同，不证明恶意意图、单次返回或kill成功。','en':'This is a capability and object contract rather than proof of malicious intent, an individual return, or successful kill.'},
 'evidence_level':'official-capability-contract'},
'poweroff-kb': {
 'reference_key':'B012-T1673-REF-KB-VIEWS',
 'locator':'Article 308457 / legacy 1004340; Using vim-cmd steps 1–4; Using esxcli steps 1–3',
 'facts':{'zh':'正文区分getallvms的注册VM/VMID和esxcli的运行VM/World ID，另以power.getstate读取状态；它也提供合法故障排查使用的正面对照。','en':'The body distinguishes getallvms registered VMs/VMIDs from esxcli running VMs/World IDs and separately reads state through power.getstate; it supplies a positive legitimate troubleshooting contrast.'},
 'limits':{'zh':'使用root是示例前提，不是所有管理读取的统一权限下界。输出图像未逐图检查，完整列、空格与CSV解析必须经部署样例验收；不把图示作为本地实验。','en':'Root is an example prerequisite rather than a universal minimum for management reads. Output images were not individually inspected; full columns, spaces, and CSV parsing require deployed-example acceptance and are not local experiments.'},
 'evidence_level':'official-operational-contract'},
'esxi-audit': {
 'reference_key':'REF-001223',
 'locator':'Article 321910; auth.log examples; Session opened; shell[64386] join',
 'facts':{'zh':'Accepted消息包含账号及客户端，Session opened消息给出shell World ID及终端，shell消息按对应World ID连接；不能将sshd监听父PID直接等于shell World ID。','en':'Accepted messages contain account and client, Session opened supplies shell World ID and terminal, and shell messages join on the corresponding World ID. The listening sshd parent PID is not directly the shell World ID.'},
 'limits':{'zh':'命令审计并不承诺stdout、退出码、所有非交互程序内部子命令或人类操作者身份；身份映射需实际消息链。','en':'Command auditing does not promise stdout, exit codes, every internal noninteractive subcommand, or a human operator’s identity; attribution requires the actual message chain.'},
 'evidence_level':'official-audit-contract'},
'esxi-logs': {
 'reference_key':'B012-T1673-REF-LOGS',
 'locator':'Article 306962; Location and Contents; auth.log/shell.log/hostd.log',
 'facts':{'zh':'日志目录与职责分别涵盖认证、shell命令和hostd管理任务、事件及SDK连接。','en':'Log locations and responsibilities separately cover authentication, shell commands, and hostd management tasks, events, and SDK connections.'},
 'limits':{'zh':'一般职责说明未保证每次只读API完整参数或VM返回，也不保证shell保存标准输出。','en':'General responsibilities do not guarantee full parameters or VM returns for every read-only API, nor stdout in shell records.'},
 'evidence_level':'official-logging-capability'},
'propertycollector': {
 'reference_key':'B012-T1673-REF-PROPERTYCOLLECTOR',
 'locator':'RetrievePropertiesEx; ContinueRetrievePropertiesEx; access evaluation',
 'facts':{'zh':'RetrievePropertiesEx按filter取得属性，方法入口System.Anonymous与对象可见权限评估并存；Continue要求同session、同collector，文档列System.View。','en':'RetrievePropertiesEx retrieves filtered properties; method-entry System.Anonymous coexists with object-visibility evaluation. Continue requires the same session and collector and is documented with System.View.'},
 'limits':{'zh':'入口权限不证明匿名全库可读或数据返回；API定义不保证默认审计，也不证明本案例实际恶意调用该API。','en':'Entry privilege establishes neither anonymous whole-inventory reads nor returned data. API definitions guarantee neither default audit nor this case’s malicious use of that API.'},
 'evidence_level':'official-api-contract'},
'retrieve-result': {
 'reference_key':'B012-T1673-REF-RETRIEVERESULT',
 'locator':'RetrieveResult.objects; RetrieveResult.token',
 'facts':{'zh':'objects承载ObjectContent，token设置需同session同collector一次性续页；unset表示该响应检索无更多结果。','en':'objects carries ObjectContent. A set token requires once-only continuation in the same session/collector; unset means no further results in that retrieval.'},
 'limits':{'zh':'token耗尽只是页链边界，不证明全库、采集完整或请求属性全部取得，需与capture及missingSet分别解释。','en':'Token exhaustion is a page boundary rather than proof of whole inventory, complete capture, or all requested properties; interpret capture and missingSet separately.'},
 'evidence_level':'official-result-contract'},
'object-content': {
 'reference_key':'B012-T1673-REF-OBJECTCONTENT',
 'locator':'ObjectContent.obj; propSet; missingSet',
 'facts':{'zh':'obj提供managed object reference，propSet提供属性名值，missingSet提供无法取得属性及fault。','en':'obj supplies a managed-object reference, propSet supplies property pairs, and missingSet supplies unacquired properties and faults.'},
 'limits':{'zh':'缺失、null、fault与成功值不同；完整分页不清除属性fault，引用取得也不等于未返回名称、路径或状态取得。','en':'Missing, null, fault, and successful values differ. Complete pagination does not remove property faults, and reference acquisition does not establish unreturned names, paths, or states.'},
 'evidence_level':'official-object-contract'},
'user-session': {
 'reference_key':'B012-T1673-REF-USERSESSION',
 'locator':'UserSession.key; userName; ipAddress; userAgent; loginTime; lastActiveTime',
 'facts':{'zh':'key是会话标识，用户名与客户端另列，ipAddress可以是pipe而非IP。','en':'key identifies the session, with separate user and client fields; ipAddress can be a pipe rather than an IP.'},
 'limits':{'zh':'对象包含字段不代表默认日志采集，更不能从共享账号或代理客户端确定人类操作者。','en':'Object fields do not imply default logging or identify a human behind a shared account or proxied client.'},
 'evidence_level':'official-session-contract'},
'host-access': {
 'reference_key':'B012-T1673-REF-HOSTACCESS',
 'locator':'Managed object description; ChangeLockdownMode; UpdateLockdownExceptions',
 'facts':{'zh':'直接host权限与vCenter权限不同，lockdown移除一般host权限但保留例外及dcui/vpxuser。','en':'Direct-host permissions differ from vCenter permissions; lockdown removes general host permissions while retaining exceptions and dcui/vpxuser.'},
 'limits':{'zh':'这不撤销已授权vCenter可见清单，也不能保证阻止持有root或例外会话者读取。','en':'This does not revoke authorized vCenter inventory visibility or guarantee prevention against root or exception sessions.'},
 'evidence_level':'official-access-control-contract'},
'virtualmachine': {
 'reference_key':None,
 'locator':'VirtualMachine properties config; guest; runtime; summary',
 'facts':{'zh':'补充官方材料说明VM配置可能不可用，guest信息可为最后已知状态。','en':'Supplemental official material states that VM configuration can be unavailable and guest data can reflect the last known state.'},
 'limits':{'zh':'已下载用于边界核验，最终候选不新增此REF，也不以下载数量要求建立共享对象。','en':'Downloaded for boundary verification; the final proposal does not create a REF solely to match download counts.'},
 'evidence_level':'supplemental-official-material'},
'cisa-play': {
 'reference_key':None,
 'locator':'HTTP 403 error response at AA23-352A',
 'facts':{'zh':'本次只能取得403错误响应，没有取得CISA原始正文。','en':'Only an HTTP 403 response was obtained, not the CISA advisory body.'},
 'limits':{'zh':'不作为事实来源，不新增REF，不扩展CASE-000284。其现有出版年/平台型时间和行业元数据需要独立审查。','en':'Not factual evidence, not a new REF, and not a basis for extending CASE-000284. Its existing publication-year/platform time and sector metadata require independent review.'},
 'evidence_level':'access-failure-only'}
}
facts['property-spec']={'reference_key': 'B012-T1673-REF-PROPERTYSPEC', 'locator': 'PropertySpec type/all/pathSet; description of union across applicable specs', 'facts': {'zh': 'PropertySpec按对象类型选择属性，适用spec的属性集合取并集；all=true忽略pathSet，pathSet为空可仅返回对象引用。', 'en': 'PropertySpec selects properties by object type and applicable specs contribute a union. all=true ignores pathSet, while an empty pathSet can retrieve references without properties.'}, 'limits': {'zh': '请求范围不证明值已返回；all=true或不能展开的集合不可被空pathSet误判为全部属性完成。', 'en': 'Requested scope does not establish returned values. all=true or an unexpandable scope cannot be mistaken for complete property acquisition from an empty pathSet.'}, 'evidence_level': 'official-property-selection-contract'}
examined=[]
for m in manifest:
    f=facts[m['key']]
    examined.append(dict(artifact_key=m['key'], **f, requested_url=m['requested_url'], resolved_url=m['resolved_url'], http_status=m['status_code'], raw_path=m['raw_path'], raw_sha256=m['sha256'], raw_bytes=m['bytes'], text_path=m['text_path'], text_encoding='utf-8', text_sha256=m['text_sha256'], text_bytes=m['text_bytes'], quotations=[]))
verification={
 'verification_schema_version':'2.0.0',
 'type':'evidence-verification',
 'batch_ref':'BATCH-TA0007-012',
 'candidate':'T1673',
 'source_attack_version':'19.1',
 'subject_key':'B012-T1673-PARENT',
 'local_experiments_performed':False,
 'verified_scope':'primary-research-and-official-contracts',
 'fixed_baseline':{'reference_ref':'REF-000625','path':str((BATCH/'fixed-baseline-T1673.json').relative_to(ROOT)),'sha256':sha(BATCH/'fixed-baseline-T1673.json'),'attack_subtechnique_count':0},
 'primary_overrides':{'path':str(OVERRIDES.relative_to(ROOT)),'sha256':override_hash,'preserved_unmodified':True,'applied':True},
 'examined_sources':examined,
 'claim_verification':[{'claim_key':c['temporary_key'],'evidence_mode':c['evidence_mode'],'confidence':c['confidence'],'evidence_keys':c['evidence_keys']} for c in handoff['library_candidates']['claims']],
 'native_contract_review':{
  'shell_join':{'zh':'沿Accepted→Session opened→shell[world]明确链，独立保留host启动代际；sshd PID、shell World ID和VM World ID不可混同。','en':'Join the explicit Accepted-to-Session-opened-to-shell[world] chain with host boot generation; sshd PID, shell World ID, and VM World ID are distinct.'},
  'views_and_paths':{'zh':'运行World ID与注册VMID分离；CSV用表头，名称含空格需版本解析，datastore方括号定位不是臆造绝对路径。可选stdout字段映射需实际部署样例验收。','en':'Separate running World IDs and registered VMIDs. Use CSV headers and version-aware spaced-name parsing; bracketed datastore locators are not invented absolute paths. Optional stdout mappings require actual deployment examples.'},
  'api_mapping':{'zh':'_this→collector_object_ref，specSet/type/pathSet→请求范围，ObjectContent.obj→类型与引用，propSet→名值，missingSet→属性fault，UserSession.key/userName/ipAddress→独立会话字段。','en':'Map _this to collector_object_ref, specSet/type/pathSet to request scope, ObjectContent.obj to type/reference, propSet to pairs, missingSet to property faults, and UserSession.key/userName/ipAddress to distinct session fields.'},
  'completeness':{'zh':'capture_state、page_state和property_state分别计算；token耗尽不清除missingSet。all=true属性集合无法展开时不宣称全部属性完成；空结果只说明当次权限可见过滤范围。','en':'Compute capture_state, page_state, and property_state separately. Token exhaustion does not remove missingSet. Do not declare all properties complete when an all=true scope cannot be expanded; empty results apply only to that permission-visible filtered request.'},
  'input_contracts':{'zh':'NJA声明了原始日志、会话映射、批准登记、可选返回、采集支持与健康。API事务为自定义已验收输入，不是默认EDR或hostd结果流；缺失或截断须降级。','en':'Analytics declare raw logs, session mappings, approval registers, optional results, capabilities, and health. API transactions are custom accepted inputs rather than a default EDR/hostd result stream; missing or truncated data reduces conclusions.'}
 },
 'taxonomy_resolution':{'coverage':'deferred','established_child_count':0,'reason':{'zh':'旧清单、会话借用和事件订阅仍待结论层证据；零已成立项不等于所有变量已被排除。','en':'Existing inventories, session borrowing, and subscriptions lack conclusion-level evidence; zero established children does not exclude every variable.'}},
 'mechanism_resolution':{'retained':'NM-FD','confidence':'medium','rejected':['NM-BT','NM-ST','NM-DO'],'reason':{'zh':'正常管理与恶意采用重合只支持条件化特征推断；guest观察位置是父级固有性质，不能单独作为BT。','en':'Overlap between normal management and malicious adoption supports only conditional feature inference; guest observation position is inherent to the parent and cannot alone establish BT.'}},
 'machine_checks':{'status':'pending'},
 'freeze':{'status':'pending'}
}
VERIFY.write_text(yaml.safe_dump(verification,allow_unicode=True,sort_keys=False,width=110))
print(json.dumps({'handoff_bytes':HANDOFF.stat().st_size,'verification_bytes':VERIFY.stat().st_size,'raw_sources_preserved':len(manifest),'utf8_texts_reextracted':len(manifest),'overrides_sha256':override_hash},indent=2))
