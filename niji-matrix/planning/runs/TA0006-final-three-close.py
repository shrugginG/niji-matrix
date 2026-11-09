"""Serialize the primary agent's reviewed tactic convergence and fixed-inventory closure."""
from pathlib import Path
from collections import Counter
import json,sys,yaml
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from library_common import load_objects
runs=ROOT/'planning/runs';acceptances=[]
for suffix in ['011','012','013']:
 a=json.loads((runs/f'BATCH-TA0006-{suffix}/acceptance.json').read_text());assert a['status']=='passed';acceptances.append(a)
inventory=yaml.safe_load((runs/'TA0006-final-three-inventory.yaml').read_text());pfile=ROOT/'planning/tactics/TA0006.yaml';p=yaml.safe_load(pfile.read_text());objects,paths=load_objects(ROOT)
assert p['attack_baseline']=={'domain':'enterprise-attack','version':'19.1'}
assert len(p['work_items'])==17 and {w['source_attack_id'] for w in p['work_items']}==set(inventory['parent_ids'])
parents=[];rows=[]
for w in p['work_items']:
 assert w['stage']=='review',w['id']
 d=objects[w['decision_ref']];assert d['candidate']['source_attack_id']==w['source_attack_id'] and d['candidate']['source_attack_version']=='19.1'
 t=objects[w['resulting_technique_ref']];assert d['resulting_technique_ref']==t['id'] and 'TA0006' in t['classification']['tactic_refs'] and t['lifecycle']['status']=='review'
 for child in t['subtechnique_taxonomy']['subtechnique_refs']:
  c=objects[child];assert c['parent_ref']==t['id'] and not c['lineage']['attck_subtechnique_inherited'] and c['lifecycle']['status']=='review'
 parents.append(t);rows.append(f"| {w['source_attack_id']} | {d['decision']} | {t['id']} {t['name']['zh']} | {len(t['subtechnique_taxonomy']['subtechnique_refs'])} | review |")
assert {t['id'] for t in parents}=={o['id'] for o in objects.values() if o.get('type')=='technique' and 'TA0006' in o.get('classification',{}).get('tactic_refs',[])}
children=sum(len(t['subtechnique_taxonomy']['subtechnique_refs']) for t in parents)
p['status']='review';p['candidate_inventory']['last_synced']='2026-11-05';p['gap_analysis'].update(status='complete',notes_zh=f'固定 ATT&CK Enterprise 19.1 的17个父候选全部完成准入与独立交付门禁，17个关联父技术、{children}项Niji原生子技术处于review，剩余0项。原生缺口、全量跨技术边界与共享库收敛见planning/runs/TA0006-credential-access-closure-review.md；证据不足轴已登记暂缓，人工领域评审未完成。',notes_en=f'All 17 fixed ATT&CK Enterprise 19.1 parent candidates passed admission and independent delivery gates. Seventeen associated parents and {children} native children are in review, with none remaining. Native gaps, tactic-wide boundaries, and shared-library convergence are recorded in planning/runs/TA0006-credential-access-closure-review.md. Unsupported axes are explicitly deferred and human domain review is pending.')
p['review'].update(taxonomy='passed',evidence='passed',bilingual='passed',reviewers=[])
# Remove stale authoring-progress statements from already reviewed historical work items.
for w in p['work_items']:
 if w['source_attack_id'] in {'T1111','T1621','T1040','T1003','T1528'}:
  t=objects[w['resulting_technique_ref']];n=len(t['subtechnique_taxonomy']['subtechnique_refs'])
  w['notes_zh']=f"对应{t['id']}，关联{n}项Niji原生子技术；准入、分类、证据、双语、防御、Bundle及Web候选门禁已通过，等待人工领域评审。固定ATT&CK实现库存与原生分类记录保留在{w['batch_ref']}目录，原子子项不导入。"
  w['notes_en']=f"Mapped to {t['id']} with {n} associated native children. Admission, taxonomy, evidence, bilingual content, defense, bundle, and Web candidate gates pass; human domain review is pending. Fixed ATT&CK implementation inventory and independent taxonomy records remain under {w['batch_ref']}; ATT&CK children are not imported."
pfile.write_text(yaml.safe_dump(p,allow_unicode=True,sort_keys=False,width=135))
new=Counter()
for a in acceptances:new.update(a['counts'])
summary=dict(schema_version='1.0.0',type='tactic-development-closure',tactic_ref='TA0006',attack_baseline=p['attack_baseline'],status='review',fixed_parent_candidates=17,decisions=17,formal_parents=len(parents),formal_children=children,remaining_candidates=[],completed_batches=['BATCH-TA0006-011','BATCH-TA0006-012','BATCH-TA0006-013'],new_object_counts=dict(new),human_domain_review='pending',reviewers=[],machine_and_content_review_record='TA0006-credential-access-closure-review.md',final_machine_receipt='TA0006-final-verification.json')
(runs/'TA0006-final-three-summary.yaml').write_text(yaml.safe_dump(summary,allow_unicode=True,sort_keys=False,width=135))
page_count=sum(a['browser_pages'] for a in acceptances)
text='''# TA0006 凭据获取研发收尾审查

2026-11-05。范围固定为 ATT&CK Enterprise 19.1，当前状态为 review。本记录表示候选研发、内容与机器门禁已收敛，不构成人工领域批准，也不标记 published。

## 固定清单逐项核对

官方19.1工作簿的17个父候选与计划完整一致。按 classification.tactic_refs 计数，包含跨战术复用的 NJT-0093；未只按目录归属漏计。

| ATT&CK | 准入 | 正式父技术 | NJS数 | 状态 |
|---|---|---|---:|---|
'''+ '\n'.join(rows)+f'''

合计17项准入、17项父技术、{children}项原生子技术，未处理候选0项。

## 本轮交付与顺序控制

三个sub-agent各提交一个候选的完整研究，未分配正式ID或修改正式矩阵/共享库。主Agent等待全部结果后统一裁决，正式写入依次执行BATCH-011、012、013，每批完成独立证据、分类、内容、防御、质量、Bundle与双语Web门禁后才写入下一批。各批详细收据与集成摘要保留在其目录。

本轮新增{dict(new)}，另有三项准入决议；这些是新对象数量，既有共享对象扩展另计。旧T1649交付及其他战术保留。

## 跨技术边界收敛

Kerberos票据材料、AS-REP客户端加密部分及构造结果与离线候选验证分别建模；AS-REP取得不意味着获得口令或可用TGT。票据呈现和资源接受不补写取得路径。缓存旁路指不填充本机常规缓存，仍有KDC请求，不等于OS认证库读取旁路。

T1552按普通内容暴露路径界定，与T1555受管理保管、T1003 OS权威材料和具体token/票据/Cookie/证书对象可在独立证据下并列。次生记录角色须有交互、共享、版本或复制链支持，不能把所有文件或老记录均视为副本。正常自动交付、API名称与base64不能自动证明未保护暴露。

Cookie取得要求完整既有会话材料返回控制面；浏览器代理、页面读取或同设备资源使用归NJT-0145及后继身份对象，不自动证明Cookie返回。可信客户端代取按处理身份与输出边界划分，不复刻token位置三分。Cookie属性、ABE与设备持钥续期各自承担不同保护边界，不声称统一阻止复制或MFA绕过。

原有输入捕获、路径介入、被动嗅探、认证过程修改、MFA证明与挑战生成、漏洞边界、保管库及证书构造均保持其直接行为和结果。新来源/案例不替相邻对象补证，材料对象与路径的双标注需要两个完成点。

## 原生分类广度与缺口审查

T1552八项覆盖和七轴第二轮已由主Agent逐行审核。八种承载/平台/材料不等于八种匿迹变量；现行残留是父核心，材料类型归邻接，自动交付归属及频率轴证据不足，只有可证次生记录角色通过全部门，8→1差距接受。T1558五项实现被时间密度、缓存落点与模板来源的三条独立轴覆盖或保留父级；T1539无ATT&CK子项仍比较四类路径，仅客户端处理身份轴成立。未复制ATT&CK原子分类。

原有高广度T1555、T1556、T1003的第二轮与覆盖记录继续保留在前批目录，新分类未取代其边界。未分项行为仍在父级，不以子项数声称穷尽所有实现。

目前没有结论层级证据支持另增一个直接行为不同的TA0006父技术。不可导出密钥调用仍只有平台能力/控制原理，跨平台等价遥测与具体匿迹效能需要后续独立证据；这些已登记暂缓。新材料类型、产品、储存介质、后处理加密与低量外观不能独自建立新父子项。ATT&CK20.0的T1697属于另行基线迁移，未并入此次固定清单。

## 共享库与证据校准

来源按规范URL及身份集中查重；REF-000435复用同报告但CHP票据Case与制造业LazyWiper中心事件分开，微软Cookie取得Case与后继财务历史选择Case分开。REF-000942的Git事件字段被复用，未新造重复来源。MIT-000187与MIT-000147保留原控制措施，只添加目标专用应用；CLM-000886保留命题并扩展适用主体。策略目标、数据与结果实质不同则新建，未以名称替换通用分析。

真实事件只证明公开记录的中心事实。CHP报告不证明精确票据字段或规避成功，MSRC共享秘密不证明Slack、具体秘密类型或全部值有效，Cookie作者实验不冒充受害者案例。构造能力、实际使用与实测匿迹收益分别校准。

## 门禁与实际页面

三批各自make quality通过，内容/规划0错误0警告，共享库0精确重复、0待审重复，Python12/12，Review Web140/140；三份Bundle已构建并在review状态复核。实际独立Chrome检查累计{page_count}个双语页面（包含最终战术页），覆盖正文、机理、Strategy到Analytic详情、数据字段/误报/盲区/调优、Mitigation应用、原始YAML与API。API和浏览器异常均为0。

初次集成映射错误已用原预留ID补齐共享对象并重新通过全部门禁，未复用或重分配ID。Chrome临时目录清理竞争已加入限定重试并复验。最终收尾机器复核见TA0006-final-verification.json；这些检查不代表已部署生产检测器或完成人工领域审查。

## 人工领域评审状态

所有父子保持review，reviewers为空。后续人工评审应重点核对条件性观察模型、原始实现到真实事件的外推边界，以及目标部署数据源和参数；本记录不为这些未知条件编造通过结论。
'''
(runs/'TA0006-credential-access-closure-review.md').write_text(text)
work=runs/'TA0006-final-convergence-work.md'
if work.exists():work.write_text('# TA0006 收尾工作台账\n\n研发收敛已记录于 [TA0006-credential-access-closure-review.md](TA0006-credential-access-closure-review.md)。固定17项全部进入review，人工领域评审pending。\n')
print(json.dumps(dict(tactic='TA0006',parents=len(parents),children=children,remaining=0,new=dict(new),browser_pages=page_count),ensure_ascii=False))
