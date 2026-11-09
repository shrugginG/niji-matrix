"""Record independently observed gates and promote one reviewed delivery batch."""
from pathlib import Path
import sys,json,yaml
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from library_common import load_objects
batch=sys.argv[1];run=ROOT/'planning/runs'/batch
receipt=json.loads((run/'gate-receipt.json').read_text())
assert receipt['make_quality']=='passed' and receipt['python_tests']==12 and receipt['web_tests']==140
report=json.loads((run/'web-qa/report.json').read_text());assert report['status']=='passed' and not report['api_issues'] and not report['browser_errors']
objects,paths=load_objects(ROOT);mapping=yaml.safe_load((run/'id-map.yaml').read_text());written=yaml.safe_load((run/'written-paths.yaml').read_text());proposal=yaml.safe_load((run/'approved-proposal.yaml').read_text())
source=proposal['decision']['candidate']['source_attack_id'];parent=mapping[proposal['parent']['id']];children=[mapping[c['id']] for c in proposal['children']]
registry=yaml.safe_load((ROOT/'planning/id-reservations.yaml').read_text());owned={r['id'] for r in registry['reservations'] if r['owner']==batch};assert all(r['status']=='consumed' for r in registry['reservations'] if r['owner']==batch)
for id_,path in written.items():
 o=objects[id_]
 if 'lifecycle' in o:o['lifecycle']['status']='review'
 elif o.get('type') in {'claim','case'}:o['status']='review'
 elif o.get('type')=='technique-decision':
  o['review']['status']='review';o['review']['review_notes_zh']='准入、独立原生分类、证据深度、防御、共享库、完整质量、Bundle及实际双语Web门禁通过；人工领域评审未完成。';o['review']['review_notes_en']='Admission, independent native taxonomy, evidence depth, defense, shared libraries, full quality, bundle, and actual bilingual Web gates pass; human domain review remains pending.'
 paths[id_].write_text(yaml.safe_dump(o,allow_unicode=True,sort_keys=False,width=135))
notes={
'T1558':('adapt 为 Kerberos 票据材料取得与构造，三项原生轴分别控制请求密度、本机缓存落点及真实签发模板承袭；成功取得、离线验证、呈现与接受分开。完整候选门禁通过，等待人工领域评审。','Adapted as Kerberos ticket-material acquisition and construction with native axes for request density, local-cache destination, and genuine issuance-template inheritance. Acquisition, offline verification, presentation, and acceptance stay separate. All candidate gates pass; human domain review is pending.'),
'T1552':('adapt 为未保护的认证秘密取得；八项覆盖与七轴第二轮后，仅可证次生记录角色建立一项原生子技术，8→1差距已主审。完整候选门禁通过，等待人工领域评审。','Adapted as unprotected authentication-secret acquisition. After eight-item coverage and seven second-pass axes, one native child uses provable secondary-record role, with the breadth gap reviewed. All candidate gates pass; human domain review is pending.'),
'T1539':('adapt 为 Web 会话 Cookie 取得，一项原生子技术按可信客户端处理材料与受控接收者划分；浏览器控制不替代Cookie返回。完整候选门禁通过，等待人工领域评审。','Adapted as web session-cookie acquisition with one native child distinguished by trusted-client handling and a controlled recipient. Browser control does not replace cookie return. All candidate gates pass; human domain review is pending.')}
f=ROOT/'planning/tactics/TA0006.yaml';p=yaml.safe_load(f.read_text())
for b in p['batches']:
 if b['id']==batch:b['status']='review'
for w in p['work_items']:
 if w.get('source_attack_id')==source:w.update(stage='review',notes_zh=notes[source][0],notes_en=notes[source][1])
complete=sum(w['stage']=='review' or w['stage']=='excluded' for w in p['work_items']);remaining=[w['source_attack_id'] for w in p['work_items'] if w['stage'] not in ['review','excluded','published']]
parents=[o for o in objects.values() if o.get('type')=='technique' and 'TA0006' in o.get('classification',{}).get('tactic_refs',[])];child_count=sum(len(o['subtechnique_taxonomy']['subtechnique_refs']) for o in parents)
p['gap_analysis']['notes_zh']=f'固定19.1清单17项，已完成候选门禁{complete}项，关联{child_count}项Niji原生子技术；剩余'+('、'.join(remaining) if remaining else'0项')+'。全量战术收敛与人工领域评审分别记录。'
p['gap_analysis']['notes_en']=f'The fixed 19.1 inventory has 17 candidates; {complete} passed candidate gates with {child_count} associated native children. Remaining: '+(', '.join(remaining) if remaining else'none')+'. Tactic-wide convergence and human domain review are recorded separately.'
f.write_text(yaml.safe_dump(p,allow_unicode=True,sort_keys=False,width=135))
counts={}
for id_ in owned:counts[objects[id_]['type']]=counts.get(objects[id_]['type'],0)+1
summary=yaml.safe_load((ROOT/'planning/templates/batch-integration-summary.yaml').read_text());summary.update(batch_ref=batch,status='review')
summary['delivery_control']=dict(overall_candidate_count=17,batch_candidate_count=1,batch_size_rationale={'zh':'复杂候选单项交付，完整研究并行但正式编写与验收顺序执行。','en':'Deliver a complex candidate alone; complete research runs in parallel while canonical writing and acceptance remain sequential.'},previous_batch_gate_passed=True)
summary['candidate_results']=[dict(source_attack_id=source,decision='adapt',technique_ref=parent,subtechnique_refs=children)]
res=yaml.safe_load((run/'shared-resolutions.yaml').read_text());summary['shared_library_resolutions']=dict(reuse=sorted(set(res.get('temporary_to_existing',{}).values())),extend=[x['id'] for x in res.get('extensions',[])],create_ranges=counts)
summary['deferred_hypotheses']=proposal.get('integration_notes',{}).get('confidence_calibration',[]) if isinstance(proposal.get('integration_notes',{}).get('confidence_calibration'),list) else []
summary['duplicate_resolution_refs']=[]
summary['semantic_validation']={k:True for k in ['candidate_level_gates_passed','conclusion_level_evidence_passed','njt_0001_field_responsibility_reviewed','bilingual_argument_depth_passed','boilerplate_review_passed','taxonomy_breadth_reviewed','attack_breadth_gap_explained']};summary['semantic_validation']['canonical_prose_bulk_generated']=False
summary['validation']=dict(matrix_objects=len(objects),schema_errors=0,schema_warnings=0,unresolved_duplicate_candidates=0,reviewed_similarity_resolutions=receipt['reviewed_similarity_resolutions'],infrastructure_tests=f'Python 12/12; Review Web 140/140; isolated Chrome bilingual {len(report["pages"])}/{len(report["pages"])} pages',web_api_issues=0,bundles_built=[parent])
summary['review_notes_zh']=notes[source][0]+f' 本批新增{counts}；TA0006候选{complete}/17，关联NJS {child_count}。'
summary['review_notes_en']=notes[source][1]+f' Added object counts: {counts}; TA0006 candidates {complete}/17 with {child_count} associated children.'
(run/'integration-summary.yaml').write_text(yaml.safe_dump(summary,allow_unicode=True,sort_keys=False,width=135));(run/'acceptance.json').write_text(json.dumps(dict(status='passed',parent=parent,children=children,counts=counts,gate_receipt=receipt,browser_pages=len(report['pages']),human_domain_review='pending'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(batch=batch,parent=parent,children=children,counts=counts,completed=complete,remaining=remaining,associated_children=child_count),ensure_ascii=False))
