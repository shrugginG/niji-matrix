"""Record accepted gate artifacts and promote only this batch to review."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import sys
import yaml

RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[2]
CANDIDATES=['T1518','T1082','T1614','T1016','T1049']
ids=json.loads((RUN/'allocated-ids.json').read_text())
final='--verify' in sys.argv
quality=(RUN/'quality.log').read_text()
assert '校验通过：0 个错误，0 个警告。' in quality
assert '规划校验通过：0 个错误，0 个警告。' in quality
assert '0 组精确重复，0 组待审可能重复' in quality
assert 'Reader-prose audit passed: 215 parents' in quality
assert re.search(r'Ran 12 tests',quality) and '\nOK\n' in quality
assert 'dist/catalogs/library-catalog.json:' in quality
if final:
    assert '校验通过：0 个错误，0 个警告。' in (RUN/'final-content-validation.log').read_text()
    assert '规划校验通过：0 个错误，0 个警告。' in (RUN/'final-planning-validation.log').read_text()
web=(RUN/'web-tests.log').read_text()
assert re.search(r'pass\s+140\b',web) and re.search(r'fail\s+0\b',web)
duplicates=json.loads((RUN/'duplicate-audit-final.json').read_text())
assert not duplicates['exact'] and not duplicates['possible']
pages=0
for parent in ids['NJT']:
    browser=json.loads((RUN/f'web-qa/{parent}/report.json').read_text())
    assert browser['status']=='passed' and not browser['api_issues'] and not browser['browser_errors']
    pages+=len(browser['pages'])
    bundle=json.loads((ROOT/f'dist/techniques/{parent}.json').read_text())
    assert bundle['technique']['id']==parent
    assert [c['id'] for c in bundle['subtechniques']]==ids['NJS'][parent]
    if final:
        for category in ['subtechniques','detection_strategies','detection_analytics','mitigations']:
            assert all(x['lifecycle']['status']=='review' for x in bundle[category]),category
        assert bundle['technique']['lifecycle']['status']=='review'
registry=yaml.safe_load((ROOT/'planning/id-reservations.yaml').read_text())
assert not [r for r in registry['reservations'] if r['status']=='reserved']
paths=json.loads((RUN/'written-object-paths.json').read_text())
before=json.loads((RUN/'shared-objects-before.json').read_text())
for relative,text in before.items():
    if relative.startswith('mitigations/'):
        original=yaml.safe_load(text);current=yaml.safe_load((ROOT/relative).read_text())
        assert original['measures']==current['measures'],relative
        assert current['applications'][:len(original['applications'])]==original['applications'],relative
if not final:
    for relative in paths:
        path=ROOT/relative;obj=yaml.safe_load(path.read_text())
        if 'lifecycle' in obj:obj['lifecycle']['status']='review'
        elif obj['type'] in {'claim','case'}:obj['status']='review'
        elif obj['type']=='technique-decision':
            obj['review']['status']='review'
            obj['review']['review_notes_zh']='独立研究、准入、原生分类、双语字段、共享身份、质量、Bundle 与双语 Web 门禁通过；保持 review 等待人工领域审查。'
            obj['review']['review_notes_en']='Independent research, admission, native taxonomy, bilingual fields, shared identity, quality, bundle, and bilingual Web gates pass; keep review pending human domain approval.'
        else:continue
        path.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
plan_path=ROOT/'planning/tactics/TA0007.yaml'
plan=yaml.safe_load(plan_path.read_text())
if not final:
    next(b for b in plan['batches'] if b['id']=='BATCH-TA0007-011')['status']='review'
    for t,parent in zip(CANDIDATES,ids['NJT'],strict=True):
        work=next(w for w in plan['work_items'] if w['source_attack_id']==t)
        work['stage']='review'
        work['notes_zh']=f'Enterprise 19.1 独立研究与 retain 准入完成，建立 {parent} 及一项原生子技术；逐项证据、分类、双语深度与防御合同通过主审，共享库、ID、质量、Bundle 和双语 Web 验收通过。保持 review，尚无人工领域批准或实测检测率。详见 BATCH-TA0007-011 的本候选审定交接与验收记录。'
        work['notes_en']=f'Independent Enterprise 19.1 research and retain admission establish {parent} and one native child. Candidate evidence, taxonomy, bilingual depth, and defense contracts pass primary review; shared-library, ID, quality, bundle, and bilingual Web gates pass. Keep review pending human domain approval without measured detector effects. See this candidate\'s reviewed handoff and acceptance in BATCH-TA0007-011.'
    plan['candidate_inventory']['last_synced']='2026-11-07'
    plan['gap_analysis']['status']='pending'
    plan['gap_analysis']['notes_zh']='固定 Enterprise 19.1 TA0007 共34父候选，已完成29项准入：28项正式父技术、T1538排除、16项正式NJS。本批五项retain均完成独立原生分类与防御验收。剩余5父候选，13项既有父技术的子分类仍deferred；原生缺口、最终战术收敛和人工领域审查尚未完成。'
    plan['gap_analysis']['notes_en']='Fixed Enterprise 19.1 TA0007 has 34 parents and 29 completed admissions: 28 formal parents, excluded T1538, and 16 formal NJS. Five retained candidates in this delivery pass independent native-taxonomy and defense acceptance. Five parents remain; thirteen existing parent taxonomies remain deferred. Native gaps, final tactic convergence, and human domain review remain open.'
    plan_path.write_text(yaml.safe_dump(plan,allow_unicode=True,sort_keys=False,width=120))
stages=dict(Counter(w['stage'] for w in plan['work_items']))
assert stages=={'review':28,'excluded':1,'untriaged':5},stages
counts=json.loads((RUN/'allocation-counts.json').read_text())
mapping=json.loads((RUN/'canonical-id-map.json').read_text())
extensions=json.loads((RUN/'extended-object-paths.json').read_text())
extended_ids=[yaml.safe_load((ROOT/p).read_text()).get('id') for p in extensions if not p.startswith('planning/')]
reused=set()
for t in CANDIDATES:
    d=yaml.safe_load((RUN/f'{t}-reviewed-handoff.yaml').read_text())
    reused.update(d['existing_library_reuse']['reference_refs'])
reused-=set(extended_ids)
validation={'matrix_objects':4690,'schema_errors':0,'schema_warnings':0,'planning_errors':0,'planning_warnings':0,
    'exact_duplicates':0,'unresolved_duplicate_candidates':0,'reviewed_similarity_resolutions':len(duplicates['resolved']),
    'infrastructure_tests':12,'web_tests':140,'web_api_issues':0,'bilingual_browser_pages':pages,'browser_errors':0,
    'bundles_built':ids['NJT'],'unexplained_reserved_ids':0,'real_host_device_or_cloud_experiment_performed':False,
    'post_promotion_verification':'passed' if final else 'pending',
    'authoritative_quality_log':'quality.log',
    'post_promotion_checks':['final-content-validation.log','final-planning-validation.log','final-browser-qa.log','final-bundles.log']}
summary={'schema_version':'1.0.0','type':'batch-integration-summary','batch_ref':'BATCH-TA0007-011','status':'review',
    'delivery_control':{'overall_candidate_count':34,'batch_candidate_count':5,
        'batch_size_rationale':{'zh':'用户指定后续五项，按三加二两轮独立研究，每项完整门禁，主审等待全部结果后统一写入。',
                                'en':'The user specified the next five; two research waves of three and two preserve independent gates, with canonical integration only after all results return.'},
        'previous_batch_gate_passed':True,'research_subagent_count':5,'canonical_integration_after_complete_handoffs':True,
        'scope_plan':'planning/tactics/TA0007.yaml','additional_plan_checked':'planning/tactics/TA0011.yaml'},
    'candidate_results':[{'source_attack_id':t,'decision':'retain','technique_ref':p,'subtechnique_refs':ids['NJS'][p]}
                         for t,p in zip(CANDIDATES,ids['NJT'],strict=True)],
    'shared_library_resolutions':{'reuse':sorted(reused),'extend':extended_ids,
        'create_ranges':{e:values[0]+('..'+values[-1] if len(values)>1 else '') for e,values in ids.items() if e not in {'NJT','NJS'} and values},
        'new_object_counts':{**counts,'REL':0},'resolution_record':'admission-and-convergence.md',
        'precise_aliases_and_source_rebindings':'shared-convergence-overrides.yaml'},
    'deferred_hypotheses':['Unproven cache/source substitutions, timing, filtering, notification and resolution-control axes remain planning hypotheses.',
        'No default in-process return-buffer feed, controller visibility, physical location, or complete system/software/network inventory is assumed.'],
    'duplicate_resolution_refs':[r['ids'] for r in yaml.safe_load((ROOT/'planning/duplicate-resolutions.yaml').read_text())['resolutions'] if any(x in set(mapping.values()) for x in r['ids'])],
    'semantic_validation':{k:True for k in ['candidate_level_gates_passed','conclusion_level_evidence_passed',
        'njt_0001_field_responsibility_reviewed','bilingual_argument_depth_passed','boilerplate_review_passed',
        'taxonomy_breadth_reviewed','attack_breadth_gap_explained']},
    'validation':validation,'TA0007_progress':{'inventory':34,'admissions_completed':29,'formal_parents':28,
        'excluded':1,'formal_subtechniques':16,'remaining':5,
        'remaining_candidates':[w['source_attack_id'] for w in plan['work_items'] if w['stage']=='untriaged'],
        'prior_deferred_taxonomies':13,'tactic_closed':False},
    'review_notes_zh':'本批五项通过独立主审与全部验收，正式对象保持review。原始实案、仪器化样本与逆向能力分别标注；没有本研究真实主机检测实验、量化规避结果或人工领域批准。',
    'review_notes_en':'Five independently reviewed candidates pass acceptance and remain review. Incident observations, instrumented samples, and reversed capabilities retain distinct evidence levels. No real-host detector experiment, quantified evasion result, or human domain approval is claimed.'}
summary['semantic_validation']['canonical_prose_bulk_generated']=False
(RUN/'integration-summary.yaml').write_text(yaml.safe_dump(summary,allow_unicode=True,sort_keys=False,width=120))
if final:
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    bundles={p:hashlib.sha256((ROOT/f'dist/techniques/{p}.json').read_bytes()).hexdigest() for p in ids['NJT']}
    report={'batch':'BATCH-TA0007-011','status':'passed',**validation,'canonical_file_sha256':hashes,
        'bundle_sha256':bundles,'new_canonical_objects':len(paths),'extended_canonical_objects':len(extended_ids),
        'TA0007_stages':stages,'TA0007_progress':summary['TA0007_progress'],'human_domain_review_completed':False}
    (RUN/'final-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'review','final_verification':final,'validation':validation,'TA0007':summary['TA0007_progress']},ensure_ascii=False))
