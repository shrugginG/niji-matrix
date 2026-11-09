"""Serialize already reviewed prose and centrally resolved identities; no prose generation."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import re
import runpy
import sys
import yaml

RUN = Path(__file__).resolve().parent
_helpers = runpy.run_path(str(RUN/'prepare-reviewed.py'))
CANDIDATES, read, key, append_unique, strict_bilingual = [_helpers[k] for k in ['CANDIDATES','read','key','append_unique','strict_bilingual']]
ROOT = RUN.parents[2]
TODAY = '2026-11-08'
ENTITY = {'references':'REF', 'claims':'CLM', 'cases':'CASE',
          'detection_strategies':'DET', 'detection_analytics':'NJA', 'mitigations':'MIT'}
DIRECTORY = {'REF':'references', 'CLM':'claims', 'CASE':'cases',
             'DET':'detections', 'NJA':'analytics', 'MIT':'mitigations'}
FIELDS = {
 'REF':['title_zh','title_en','source_type','identifiers','authors','publisher','published','url','accessed','locator','archive_url','credibility','notes_zh','notes_en'],
 'CLM':['claim_type','statement_zh','statement_en','subject_refs','evidence_refs','evidence_mode','confidence','status'],
 'CASE':['name_zh','name_en','actor_or_campaign','subject_refs','description_zh','description_en','time_range','target_sectors_zh','target_sectors_en','evidence_refs','confidence','status'],
 'DET':['name','summary','description','detects_refs','domains','analytic_refs','evidence_refs','lifecycle'],
 'NJA':['strategy_ref','name','summary','domains','platforms','logic','data_requirements','observables','correlation','false_positives','blind_spots','tuning_guidance','evidence_refs','lifecycle'],
 'MIT':['name','summary','description','domains','measures','applications','evidence_refs','lifecycle']}
TYPE = {'REF':'reference','CLM':'claim','CASE':'case','DET':'detection-strategy','NJA':'detection-analytic','MIT':'mitigation'}
READER = ['definition_and_concept','stealth_characteristics','scope_boundary_definition',
          'application_scenarios_and_threat_model','stealth_mechanisms']

def lifecycle():
    return {'status':'draft','version':'0.1.0','created':TODAY,'modified':TODAY,
            'contributors':['Niji Matrix Research'],'reviewers':[]}

def resolve_groups():
    handoffs = {t:read(f'{t}-reviewed-handoff.yaml') for t in CANDIDATES}
    manifest = json.loads((RUN/'review-input-manifest.json').read_text())
    for t in CANDIDATES:
        assert hashlib.sha256((RUN/f'{t}-reviewed-handoff.yaml').read_bytes()).hexdigest() == manifest[t]['reviewed_sha256']
    convergence = read('shared-convergence-overrides.yaml')
    aliases = convergence.get('aliases', {})
    groups = {e:[] for e in DIRECTORY}
    extensions = []
    for t,d in handoffs.items():
        for category,e in ENTITY.items():
            section = d.get('library_candidates', {}) if category in ['references','claims','cases'] else d.get('defense_candidates', {})
            for source in section.get(category, []):
                item = deepcopy(source)
                if e=='MIT' and any(k in item for k in ['existing_ref','existing_key','existing_temporary_key']):
                    extensions.append(item)
                else:
                    item['temporary_key'] = key(item)
                    assert item['temporary_key']
                    if item['temporary_key'] not in aliases:groups[e].append(item)
    for merge in convergence.get('reference_merges', []):
        keep = next(x for x in groups['REF'] if key(x)==merge['keep_key'])
        for other in merge['merge_keys']:
            source = next(x for d in handoffs.values() for x in d.get('library_candidates',{}).get('references',[]) if key(x)==other)
            for field in ['locator','notes_zh','notes_en']:
                if source.get(field):keep[field]=(keep.get(field) or '')+' '+source[field]
    for ext in convergence.get('shared_subject_extensions', []):
        obj=next(x for xs in groups.values() for x in xs if key(x)==ext['temporary_key'])
        append_unique(obj['subject_keys'], ext['add_subject_keys'])
    for edit in convergence.get('shared_object_edits', []):
        obj=next(x for xs in groups.values() for x in xs if key(x)==edit['temporary_key'])
        obj.update(edit['fields'])
    extensions.extend(convergence.get('mitigation_extensions', []))
    all_keys=[key(x) for xs in groups.values() for x in xs]
    assert len(all_keys)==len(set(all_keys))
    return handoffs,groups,aliases,extensions

def translate(value, mapping):
    if isinstance(value,str):
        return mapping.get(value,value)
    if isinstance(value,list):
        values=[translate(v,mapping) for v in value]
        return list(dict.fromkeys(values)) if all(isinstance(v,str) for v in values) else values
    if isinstance(value,dict):
        renamed={'subject_keys':'subject_refs','evidence_keys':'evidence_refs','detects_keys':'detects_refs',
                 'analytic_keys':'analytic_refs','strategy_key':'strategy_ref','target_key':'target_ref',
                 'claim_keys':'claim_refs','case_keys':'case_refs','reference_keys':'reference_refs',
                 'strategy_keys':'strategy_refs','mitigation_keys':'mitigation_refs'}
        return {renamed.get(k,k):translate(v,mapping) for k,v in value.items()}
    return value

def main():
    dry_run = '--dry-run' in sys.argv
    assert (RUN/'admission-and-convergence.md').is_file()
    handoffs,groups,aliases,extensions=resolve_groups()
    ids=json.loads((RUN/'allocated-ids.json').read_text())
    mapping={}
    for t,p in ids['parents'].items():
        mapping[f'B012-{t}-PARENT']=p
        if handoffs[t].get('existing_technique_ref'):continue
        for child,c in zip(handoffs[t]['proposed_subtechniques'],ids['NJS'].get(p,[]),strict=True):
            mapping[key(child)]=c
    for e,items in groups.items():
        for item,ident in zip(items,ids[e],strict=True):mapping[key(item)]=ident
    pending=dict(aliases)
    while pending:
        resolved=[(alias,dest) for alias,dest in pending.items() if dest in mapping or not dest.startswith('B012-')]
        assert resolved,pending
        for alias,dest in resolved:
            mapping[alias]=mapping.get(dest,dest)
            del pending[alias]
    (RUN/'canonical-id-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
    written=[];before={};extended=[];parent_paths={}
    def write(relative,obj):
        path=ROOT/relative
        assert not path.exists(),relative
        obj=translate(obj,mapping);strict_bilingual(obj)
        assert not re.search(r'B012-T\d+-',yaml.safe_dump(obj)),relative
        if not dry_run:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
        written.append(relative)
    def update(path,obj):
        rel=str(path.relative_to(ROOT));before.setdefault(rel,path.read_text())
        obj=translate(obj,mapping)
        strict_bilingual(obj)
        assert not re.search(r'B012-T\d+-',yaml.safe_dump(obj)),rel
        if not dry_run:path.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
        if rel not in extended:extended.append(rel)
    for e,items in groups.items():
        for source in items:
            item=translate(deepcopy(source),mapping)
            item['lifecycle']=lifecycle()
            if e=='REF':
                item.setdefault('identifiers',{'doi':None,'rfc':None,'arxiv':None,'attack_id':None,'other':[]})
                for field in ['publisher','published','archive_url']:item.setdefault(field,None)
                item.setdefault('authors',[]);item['accessed']=TODAY
                for field in ['notes_zh','notes_en']:item.setdefault(field,'')
            if e in {'CLM','CASE'}:
                item['status']='draft'
                for pair,flat in [('statement','statement'),('name','name'),('description','description')]:
                    if pair in item:
                        value=item[pair]
                        for lang in ['zh','en']:
                            item[f'{flat}_{lang}']='\n\n'.join(p[lang] for p in value['paragraphs']) if 'paragraphs' in value else value[lang]
            if e=='DET':
                for analytic in groups['NJA']:
                    if key(analytic) in source['analytic_keys']:
                        append_unique(item['evidence_refs'],translate(analytic['evidence_keys'],mapping))
            if e=='MIT':
                for ext in extensions:
                    if ext.get('existing_key',ext.get('existing_ref',ext.get('existing_temporary_key')))==key(source):
                        apps=ext.get('applications',ext.get('additional_applications',ext.get('proposed_applications',[])))
                        item['applications'].extend(translate(apps,mapping))
                        append_unique(item['evidence_refs'],translate(ext.get('evidence_keys',[]),mapping))
            obj={'schema_version':'1.0.0' if e in {'REF','CLM','CASE'} else '2.0.0',
                 'type':TYPE[e],'id':mapping[key(source)]}
            for field in FIELDS[e]:obj[field]=item[field]
            slug=key(source).removeprefix('B012-').lower()
            write(f'{DIRECTORY[e]}/{obj["id"]}-{slug}.yaml',obj)
    # Add only reviewed applications to existing mitigations, retaining every measure and old application.
    for ident in sorted({x.get('existing_ref') for x in extensions if x.get('existing_ref','').startswith('MIT-')}):
        path=next((ROOT/'mitigations').glob(ident+'-*.yaml'));obj=yaml.safe_load(path.read_text())
        for ext in extensions:
            if ext.get('existing_ref')!=ident:continue
            apps=ext.get('applications',ext.get('additional_applications'))
            if apps is None:apps=[ext['proposed_application']]
            obj['applications'].extend(translate(apps,mapping))
            append_unique(obj['evidence_refs'],translate(ext.get('evidence_keys',[]),mapping))
        targets=[a['target_ref'] for a in obj['applications']];assert len(targets)==len(set(targets)),ident
        obj['lifecycle']['modified']=TODAY
        version=obj['lifecycle']['version'].split('.');version[1]=str(int(version[1])+1);version[2]='0';obj['lifecycle']['version']='.'.join(version)
        update(path,obj)
    for ext in read('existing-reference-extensions.yaml').get('extensions', []):
        path=next((ROOT/'references').glob(ext['id']+'-*.yaml'));obj=yaml.safe_load(path.read_text())
        obj['accessed']=TODAY
        for field in ['locator','notes_zh','notes_en']:obj[field]=(obj.get(field) or '')+' '+ext[field]
        for field in ['title_zh','title_en','url','published']:
            if field in ext:obj[field]=ext[field]
        update(path,obj)
    existing_revisions=read('existing-object-revisions.yaml')['revisions']
    for revision in existing_revisions:
        ident=revision['object_ref']
        if ident.startswith(('NJT-', 'NJS-')):
            filename='subtechnique.yaml' if ident.startswith('NJS-') else 'technique.yaml'
            path=next(p for p in (ROOT/'matrix').rglob(filename) if p.parent.name.startswith(ident+'-'))
        elif ident.startswith('DEC-'):
            path=next((ROOT/'matrix').rglob(ident+'.yaml'))
        else:
            directory=DIRECTORY[ident.split('-')[0]]
            path=next((ROOT/directory).glob(ident+'-*.yaml'))
        obj=deepcopy(revision['replacement']) if 'replacement' in revision else yaml.safe_load(path.read_text())
        assert obj['id']==ident
        for change in revision.get('content_edits', []):
            parts=change['pointer'].strip('/').split('/')
            node=obj
            for part in parts[:-1]:node=node[int(part)] if isinstance(node,list) else node[part]
            last=int(parts[-1]) if isinstance(node,list) else parts[-1]
            if change.get('append'):
                assert last==len(node)
                node.append(deepcopy(change['value']))
            else:node[last]=deepcopy(change['value'])
        if 'lifecycle' in obj:
            obj['lifecycle']['status']='draft';obj['lifecycle']['modified']=TODAY
            old=yaml.safe_load(path.read_text())['lifecycle']['version'].split('.')
            obj['lifecycle']['version']=f'{old[0]}.{int(old[1])+1}.0'
        elif obj['type'] in {'claim','case'}:obj['status']='draft'
        elif obj['type']=='technique-decision':obj['review']['status']='draft'
        elif obj['type']=='reference':obj['accessed']=TODAY
        update(path,obj)
    for t,d in handoffs.items():
        parent=mapping[f'B012-{t}-PARENT'];rec=d['recommendation'];pc=d.get('proposed_content',{})
        decision={'schema_version':'1.1.0','type':'technique-decision','id':f'DEC-TA0007-{t}','tactic_ref':'TA0007',
            'candidate':{'source_type':'attack','source_attack_id':t,'source_attack_version':'19.1',
                         'name_zh':d['candidate']['name']['zh'],'name_en':d['candidate']['name']['en']},
            'decision':rec['decision'],'gap_statement_zh':None,'gap_statement_en':None,
            'original_attack_subtechniques_imported':False,'resulting_technique_ref':parent,
            'evidence_refs':rec.get('evidence_keys', {'T1033':['REF-000625','REF-001341','REF-000639','REF-001305','REF-001303'], 'T1007':['REF-000625','B012-T1007-REF-GOSAR','REF-001305','REF-001303','B012-T1007-REF-ENUM','B012-T1007-REF-QUERYSTATUS']}.get(t, [])),'confidence':rec['confidence'],
            'review':{'status':'draft','authors':['Niji Matrix Research'],'reviewers':[],
                'review_notes_zh':'独立研究、准入及跨技术主审收敛完成，进入机器质量、Bundle 与双语 Web 验收。',
                'review_notes_en':'Independent research, admission, and cross-technique primary convergence are complete; machine quality, bundle, and bilingual Web acceptance follow.'}}
        for field in ['rationale','scope_notes']:
            for lang in ['zh','en']:decision[field+'_'+lang]='\n\n'.join(p[lang] for p in rec[field]['paragraphs'])
        write(f'matrix/tactics/TA0007-discovery/decisions/{decision["id"]}.yaml',decision)
        if rec['decision']=='exclude':continue
        if d.get('existing_technique_ref'):
            path=next(p for p in (ROOT/'matrix').rglob('technique.yaml') if p.parent.name.startswith(parent+'-'))
            # The primary-reviewed replacement explicitly supplies cross-tactic membership.
            replacement=next(r['replacement'] for r in existing_revisions if r['object_ref']==parent)
            assert 'TA0007' in replacement['classification']['tactic_refs']
            parent_paths[parent]=str(path.relative_to(ROOT))
            continue
        obj={'schema_version':'2.0.0','type':'technique','id':parent,'name':pc.get('name',d['candidate']['name']),
             'summary':pc['summary'],'aliases':pc.get('aliases',[]),
             'classification':{'tactic_refs':['TA0007'],'origin':{'kind':'attack-retained' if rec['decision']=='retain' else 'attack-adapted',
                 'source_attack_id':t,'source_attack_version':'19.1'},'decision_ref':decision['id']}}
        obj.update({field:pc[field] for field in READER})
        tax=pc['subtechnique_taxonomy'];obj['subtechnique_taxonomy']={'coverage':tax['coverage'],
             'subtechnique_refs':[key(c) for c in d['proposed_subtechniques']],'narrative':tax['narrative']}
        obj.update({'defense':pc['defense'],'evidence':pc['evidence'],
                    'research':{'limitations':pc.get('research',d['research'])['limitations']},'lifecycle':lifecycle()})
        slug=d['candidate']['name']['en'].lower().replace('/','-').replace(' ','-')
        folder=f'matrix/tactics/TA0007-discovery/techniques/{parent}-{slug}'
        write(folder+'/technique.yaml',obj);parent_paths[parent]=folder+'/technique.yaml'
        for c in d['proposed_subtechniques']:
            child=mapping[key(c)]
            obj={'schema_version':'2.0.0','type':'evasion-subtechnique','id':child,'name':c['name'],
                 'summary':c['summary'],'aliases':c.get('aliases',[]),'parent_ref':parent,
                 'lineage':{'attck_subtechnique_inherited':False}}
            obj.update({field:c[field] for field in READER})
            obj.update({field:c[field] for field in ['defense','evidence','research']});obj['lifecycle']=lifecycle()
            childslug=c['name']['en'].lower().replace('/','-').replace(' ','-')
            write(folder+f'/subtechniques/{child}-{childslug}/subtechnique.yaml',obj)
    path=ROOT/'planning/tactics/TA0007.yaml';plan=yaml.safe_load(path.read_text())
    for t in CANDIDATES:
        work=next(w for w in plan['work_items'] if w['source_attack_id']==t)
        assert work['stage']=='researching';work['stage']='excluded' if handoffs[t]['recommendation']['decision']=='exclude' else 'authoring';work['decision_ref']=f'DEC-TA0007-{t}'
        work['resulting_technique_ref']=mapping[f'B012-{t}-PARENT']
    update(path,plan)
    if dry_run:
        print(json.dumps({'dry_run':True,'written':len(written),'extended':len(extended),'parents':parent_paths},ensure_ascii=False))
        return
    for name,value in [('written-object-paths.json',written),('extended-object-paths.json',extended),
                       ('shared-objects-before.json',before),('canonical-parent-paths.json',parent_paths)]:
        (RUN/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'written':len(written),'extended':len(extended),'parents':parent_paths},ensure_ascii=False))

if __name__=='__main__':main()
