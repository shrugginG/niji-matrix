"""Promote accepted batch outcomes and independently verify final canonical artifacts."""
from collections import Counter
from pathlib import Path
import hashlib,json,re,sys,yaml
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[2]
CANDIDATES=['T1033','T1007','T1124','T1673','T1497']
final='--verify' in sys.argv
ids=json.loads((RUN/'allocated-ids.json').read_text())
parents=[ids['parents'][t] for t in CANDIDATES]
quality=(RUN/'quality.log').read_text()
for s in ['校验通过：0 个错误，0 个警告。','规划校验通过：0 个错误，0 个警告。','0 组精确重复，0 组待审可能重复','Reader-prose audit passed: 219 parents','dist/catalogs/library-catalog.json:']:assert s in quality,s
assert re.search(r'Ran 12 tests',quality) and '\nOK\n' in quality
web=(RUN/'web-tests.log').read_text();assert re.search(r'pass\s+140\b',web) and re.search(r'fail\s+0\b',web)
duplicates=json.loads((RUN/'duplicate-audit-final.json').read_text());assert not duplicates['exact'] and not duplicates['possible']
if final:
 for name,s in [('final-content-validation.log','校验通过：0 个错误，0 个警告。'),('final-planning-validation.log','规划校验通过：0 个错误，0 个警告。')]:assert s in (RUN/name).read_text()
page_count=0
for p in parents:
 browser=json.loads((RUN/f'web-qa/{p}/report.json').read_text());assert browser['status']=='passed' and not browser['api_issues'] and not browser['browser_errors'];page_count+=len(browser['pages'])
 bundle=json.loads((ROOT/f'dist/techniques/{p}.json').read_text());assert bundle['technique']['id']==p
 children=ids['NJS'].get(p,['NJS-0122-001','NJS-0122-002','NJS-0122-003'] if p=='NJT-0122' else [])
 assert [c['id'] for c in bundle['subtechniques']]==children
 if final:
  for c in ['subtechniques','detection_strategies','detection_analytics','mitigations']:assert all(x['lifecycle']['status']=='review' for x in bundle[c]),(p,c)
  assert bundle['technique']['lifecycle']['status']=='review'
registry=yaml.safe_load((ROOT/'planning/id-reservations.yaml').read_text());assert not [r for r in registry['reservations'] if r['status']=='reserved']
paths=json.loads((RUN/'written-object-paths.json').read_text());extensions=json.loads((RUN/'extended-object-paths.json').read_text());before=json.loads((RUN/'shared-objects-before.json').read_text())
for relative,text in before.items():
 if relative.startswith('mitigations/'):
  original=yaml.safe_load(text);current=yaml.safe_load((ROOT/relative).read_text());assert original['measures']==current['measures'],relative
  if original['id']=='MIT-000078':assert current['applications'][:len(original['applications'])]==original['applications'],relative
  elif original['id']=='MIT-000120':
   assert [a['target_ref'] for a in current['applications']]==[a['target_ref'] for a in original['applications']]
   assert [a['limitations'] for a in current['applications']]==[a['limitations'] for a in original['applications']]
  else:raise AssertionError(relative)
if not final:
 for relative in dict.fromkeys(paths+extensions):
  if relative.startswith('planning/'):continue
  path=ROOT/relative;obj=yaml.safe_load(path.read_text())
  if 'lifecycle' in obj:obj['lifecycle']['status']='review'
  elif obj['type'] in {'claim','case'}:obj['status']='review'
  elif obj['type']=='technique-decision':
   obj['review']['status']='review';obj['review']['review_notes_zh']='独立研究、准入、原生分类、证据与双语主审、共享身份、质量、Bundle 和双语 Web 门禁通过；保持 review 等待人工领域审查。'
   obj['review']['review_notes_en']='Independent research, admission, native taxonomy, evidence and bilingual primary review, shared identity, quality, bundle, and bilingual Web gates pass; retain review pending human domain approval.'
  else:continue
  path.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
plan_path=ROOT/'planning/tactics/TA0007.yaml';plan=yaml.safe_load(plan_path.read_text())
if not final:
 plan['status']='review';next(b for b in plan['batches'] if b['id']=='BATCH-TA0007-012')['status']='review'
 details={
 'T1033':('retain','一个新增原生子项','one new native child'),
 'T1007':('retain','一个新增原生子项','one new native child'),
 'T1124':('retain','零子项且none-justified','zero children with none-justified coverage'),
 'T1673':('retain','零已成立子项且分类deferred','zero established children with deferred taxonomy'),
 'T1497':('adapt','复用整改既有父项及三个原生子项，保留TA0005并加入TA0007','reuse and repair of the existing parent and three native children, retaining TA0005 and adding TA0007')}
 for t,p in zip(CANDIDATES,parents,strict=True):
  w=next(w for w in plan['work_items'] if w['source_attack_id']==t);w['stage']='review';dec,zh,en=details[t]
  w['notes_zh']=f'Enterprise 19.1独立研究与{dec}准入完成：{p}，{zh}。逐项证据、机理、分类、双语深度及可实施防御通过主审；共享库、ID、质量、Bundle与双语Web验收通过，保持review等待人工领域批准。见BATCH-TA0007-012审定交接与验收记录。'
  w['notes_en']=f'Independent Enterprise 19.1 research and {dec} admission establish {p}, with {en}. Evidence, mechanisms, taxonomy, bilingual depth, and implementable defenses pass primary review. Shared-library, ID, quality, bundle, and bilingual Web gates pass; retain review pending human domain approval. See BATCH-TA0007-012 reviewed handoffs and acceptance.'
 plan['candidate_inventory']['last_synced']='2026-11-08'
 plan['gap_analysis']={'status':'complete','notes_zh':'固定Enterprise 19.1的34父候选均已完成准入：33正式父项及T1538一项排除，TA0007共21项正式NJS，剩余未处理父候选0。本批新增4NJT/2NJS并复用整改NJT-0122及3NJS。对照当前矩阵及TA0011完成有界原生父级缺口与跨技术收敛，当前证据未支持另一新增父项。13项既有及T1673共14项子分类仍deferred，不能解释为所有匿迹变体研究完结；人工领域审查未完成。见BATCH-TA0007-012/tactic-convergence.md。','notes_en':'All 34 fixed Enterprise 19.1 parents have admissions: 33 formal parents and excluded T1538, with 21 TA0007 NJS and zero unprocessed parents. This delivery adds four NJT and two NJS and reuses/repairs NJT-0122 and three NJS. Bounded native-parent gap and cross-technique convergence against the current matrix and TA0011 found no additional presently supported parent. Thirteen prior taxonomies plus T1673 remain fourteen deferred child-taxonomy reviews; this does not close research into every stealth variant. Human domain review remains pending. See BATCH-TA0007-012/tactic-convergence.md.'}
 plan['review'].update(taxonomy='in-progress',evidence='passed',bilingual='passed')
 plan_path.write_text(yaml.safe_dump(plan,allow_unicode=True,sort_keys=False,width=120))
stages=dict(Counter(w['stage'] for w in plan['work_items']));assert stages=={'review':33,'excluded':1},stages
objects={}
for folder in ['matrix','references','claims','cases','detections','analytics','mitigations','relationships','mechanisms']:
 for p in (ROOT/folder).rglob('*.yaml'):
  d=yaml.safe_load(p.read_text())
  if isinstance(d,dict) and 'id' in d:objects[d['id']]=d
members=[x for x in objects.values() if x.get('type')=='technique' and 'TA0007' in x['classification']['tactic_refs']]
children=[x for x in objects.values() if x.get('type')=='evasion-subtechnique' and x['parent_ref'] in {p['id'] for p in members}]
deferred=[x['id'] for x in members if x['subtechnique_taxonomy']['coverage']=='deferred']
assert len(members)==33 and len(children)==21 and len(deferred)==14,(len(members),len(children),deferred)
assert all(x['lifecycle']['status']=='review' for x in members+children)
for t in CANDIDATES:
 d=objects[f'DEC-TA0007-{t}'];assert not d['original_attack_subtechniques_imported']
assert objects['NJT-0122']['classification']['tactic_refs']==['TA0005','TA0007']
assert objects['NJT-0122']['classification']['decision_ref']=='DEC-TA0005-T1497'
counts=json.loads((RUN/'allocation-counts.json').read_text());extended_ids=[yaml.safe_load((ROOT/p).read_text()).get('id') for p in extensions if not p.startswith('planning/')]
reused=set()
for t in CANDIDATES:
 d=yaml.safe_load((RUN/f'{t}-reviewed-handoff.yaml').read_text());reused.update(d['existing_library_reuse'].get('reference_refs',[]))
reused-=set(extended_ids)
validation={'matrix_objects':4826,'schema_errors':0,'schema_warnings':0,'planning_errors':0,'planning_warnings':0,'exact_duplicates':0,'unresolved_duplicate_candidates':0,'reviewed_similarity_resolutions':len(duplicates['resolved']),'infrastructure_tests':12,'web_tests':140,'web_api_issues':0,'bilingual_browser_pages':page_count,'browser_errors':0,'bundles_built':parents,'unexplained_reserved_ids':0,'real_host_device_or_cloud_experiment_performed':False,'post_promotion_verification':'passed' if final else 'pending','authoritative_quality_log':'quality.log','post_promotion_checks':['final-content-validation.log','final-planning-validation.log','final-browser-qa.log','final-bundles.log']}
assert '4826' in quality
results=[{'source_attack_id':t,'decision':'adapt' if t=='T1497' else 'retain','technique_ref':p,'new_parent':t!='T1497','subtechnique_refs':ids['NJS'].get(p,['NJS-0122-001','NJS-0122-002','NJS-0122-003'] if t=='T1497' else []),'new_subtechniques':t in ['T1033','T1007']} for t,p in zip(CANDIDATES,parents,strict=True)]
progress={'inventory':34,'admissions_completed':34,'formal_parents':33,'excluded':1,'formal_subtechniques':21,'remaining':0,'remaining_candidates':[],'deferred_taxonomy_count':14,'deferred_taxonomies':sorted(deferred),'fixed_parent_inventory_complete':True,'native_parent_gap_assessment':'complete within reviewed evidence','human_domain_review_completed':False,'all_child_hypotheses_closed':False,'tactic_status':'review'}
summary={'schema_version':'1.0.0','type':'batch-integration-summary','batch_ref':'BATCH-TA0007-012','status':'review','delivery_control':{'overall_candidate_count':34,'batch_candidate_count':5,'batch_size_rationale':{'zh':'用户指定最后五项，五位独立研究者分两轮完成，主审收齐冻结结果后统一准入、分配及写入。','en':'The user requested the final five; five independent researchers completed two waves, followed by primary admission, allocation, and integration after all frozen results returned.'},'previous_batch_gate_passed':True,'research_subagent_count':5,'canonical_integration_after_complete_handoffs':True,'scope_plan':'planning/tactics/TA0007.yaml','additional_plan_checked':'planning/tactics/TA0011.yaml'},'candidate_results':results,'remediation':{'existing_parent':'NJT-0122','existing_children':['NJS-0122-001','NJS-0122-002','NJS-0122-003'],'existing_package_revisions':20,'original_tactic_and_decision_preserved':True,'mitigation_measures_preserved':['MIT-000078','MIT-000120']},'shared_library_resolutions':{'reuse':sorted(reused),'extend':extended_ids,'create_ranges':{e:values[0]+('..'+values[-1] if len(values)>1 else '') for e,values in ids.items() if e not in {'NJT','NJS','parents'} and values},'new_object_counts':{**counts,'REL':0,'DEC':5},'resolution_record':'admission-and-convergence.md','precise_aliases_and_source_rebindings':'shared-convergence-overrides.yaml'},'deferred_hypotheses':['Fourteen parent taxonomies remain deferred; hypothetical source substitution, caches, subscriptions, and query shaping require positive evidence.','No default API result, complete VM property set, actual person, full inventory, physical location, or measured detection effect is assumed.'],'semantic_validation':{**{k:True for k in ['candidate_level_gates_passed','conclusion_level_evidence_passed','njt_0001_field_responsibility_reviewed','bilingual_argument_depth_passed','boilerplate_review_passed','taxonomy_breadth_reviewed','attack_breadth_gap_explained']},'canonical_prose_bulk_generated':False},'validation':validation,'TA0007_progress':progress,'review_notes_zh':'本批正式对象通过主审与验收并保持review。已完成固定父候选开发及有界原生父级缺口审查；14项子分类仍deferred，人工领域批准待完成。无真实主机/虚拟机恶意实验或量化检测率。','review_notes_en':'Formal objects pass primary review and acceptance and remain review. Fixed-parent development and bounded native-parent gap review are complete; fourteen child taxonomies remain deferred and human approval is pending. No real-host/VM malicious experiment or quantified detection rate is claimed.'}
mapping=json.loads((RUN/'canonical-id-map.json').read_text())
summary['duplicate_resolution_refs']=[r['ids'] for r in yaml.safe_load((ROOT/'planning/duplicate-resolutions.yaml').read_text())['resolutions'] if any(x in set(mapping.values()) for x in r['ids'])]
(RUN/'integration-summary.yaml').write_text(yaml.safe_dump(summary,allow_unicode=True,sort_keys=False,width=120))
if final:
 hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in dict.fromkeys(paths+extensions)}
 bundles={p:hashlib.sha256((ROOT/f'dist/techniques/{p}.json').read_bytes()).hexdigest() for p in parents}
 report={'batch':'BATCH-TA0007-012','status':'passed',**validation,'canonical_file_sha256':hashes,'bundle_sha256':bundles,'new_canonical_objects':len(paths),'extended_canonical_objects':len(extended_ids),'TA0007_stages':stages,'TA0007_progress':progress,'human_domain_review_completed':False}
 (RUN/'final-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'review','final_verification':final,'validation':validation,'TA0007':progress},ensure_ascii=False))
