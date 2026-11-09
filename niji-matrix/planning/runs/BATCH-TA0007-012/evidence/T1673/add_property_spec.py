# Archived one-shot authoring script; do not rerun against the frozen handoff.
from pathlib import Path
import json,yaml,requests,hashlib
from html.parser import HTMLParser
E=Path(__file__).resolve().parent;B=E.parents[1];R=E.parents[4]
u='https://developer.broadcom.com/xapis/vsphere-web-services-api/latest/vmodl.query.PropertyCollector.PropertySpec.html'
r=requests.get(u,timeout=30);r.raise_for_status();raw=E/'property-spec.html';raw.write_bytes(r.content)
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.parts.append(d.strip())
p=Parser();p.feed(raw.read_bytes().decode('utf-8'));text=E/'property-spec.txt';text.write_text('\n'.join(p.parts))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
facts={'reference_key':'B012-T1673-REF-PROPERTYSPEC','locator':'PropertySpec type/all/pathSet; description of union across applicable specs','facts':{'zh':'PropertySpec按对象类型选择属性，适用spec的属性集合取并集；all=true忽略pathSet，pathSet为空可仅返回对象引用。','en':'PropertySpec selects properties by object type and applicable specs contribute a union. all=true ignores pathSet, while an empty pathSet can retrieve references without properties.'},'limits':{'zh':'请求范围不证明值已返回；all=true或不能展开的集合不可被空pathSet误判为全部属性完成。','en':'Requested scope does not establish returned values. all=true or an unexpandable scope cannot be mistaken for complete property acquisition from an empty pathSet.'},'evidence_level':'official-property-selection-contract'}
m=json.loads((E/'download-manifest.json').read_text());item={'key':'property-spec','requested_url':u,'resolved_url':r.url,'status_code':r.status_code,'sha256':sha(raw),'bytes':raw.stat().st_size,'raw_path':str(raw.relative_to(R)),'text_path':str(text.relative_to(R)),'text_encoding':'utf-8','text_bytes':text.stat().st_size,'text_sha256':sha(text)};m.append(item);(E/'download-manifest.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
hp=B/'T1673-research-handoff.yaml';h=yaml.safe_load(hp.read_text());key=facts['reference_key']
h['library_candidates']['references'].append({'temporary_key':key,'schema_version':'1.0.0','type':'reference','title_zh':'vSphere Web Services API：PropertySpec','title_en':'vSphere Web Services API — PropertySpec','source_type':'official-documentation','authors':[],'publisher':'Broadcom','published':None,'url':u,'accessed':'2026-11-08','locator':facts['locator'],'archive_url':None,'credibility':'high','notes_zh':facts['facts']['zh']+facts['limits']['zh'],'notes_en':facts['facts']['en']+' '+facts['limits']['en']})
h['proposed_content']['evidence']['reference_keys'].append(key)
h['defense_candidates']['detection_strategies'][0]['evidence_keys'].append(key)
a=h['defense_candidates']['detection_analytics'][1];a['evidence_keys'].append(key)
a['data_requirements'][0]['required_fields'].append('requested_property_all')
a['logic']['paragraphs'][0]['zh']=a['logic']['paragraphs'][0]['zh'].replace('type及pathSet','type、all及pathSet，并按对象类型合并适用PropertySpec的属性路径集合且保留原过滤关联')
a['logic']['paragraphs'][0]['en']=a['logic']['paragraphs'][0]['en'].replace('type, and pathSet.','type, all, and pathSet, retaining filter associations and combining applicable PropertySpec paths by object type.')
a['logic']['paragraphs'][1]['zh']+='PropertySpec的all为true时忽略pathSet；明确仅请求对象引用而不请求属性时，property_state置为not_requested，不能用空路径集合宣称全部属性取得。'
a['logic']['paragraphs'][1]['en']+=' PropertySpec all=true ignores pathSet. For an explicit reference-only request, set property_state to not_requested rather than interpreting an empty path set as acquisition of every property.'
for c in h['library_candidates']['claims']:
 if c['temporary_key']=='B012-T1673-CLM-API-TELEMETRY':c['evidence_keys'].append(key)
hp.write_text(yaml.safe_dump(h,allow_unicode=True,sort_keys=False,width=110))
vp=B/'T1673-evidence-verification.yaml';v=yaml.safe_load(vp.read_text());v['examined_sources'].append(dict(artifact_key='property-spec',**facts,requested_url=u,resolved_url=r.url,http_status=r.status_code,raw_path=item['raw_path'],raw_sha256=item['sha256'],raw_bytes=item['bytes'],text_path=item['text_path'],text_encoding='utf-8',text_sha256=item['text_sha256'],text_bytes=item['text_bytes'],quotations=[]))
v['claim_verification']=[{'claim_key':c['temporary_key'],'evidence_mode':c['evidence_mode'],'confidence':c['confidence'],'evidence_keys':c['evidence_keys']} for c in h['library_candidates']['claims']]
v['native_contract_review']['api_mapping']['zh']+='PropertySpec.all和pathSet保留原生语义，按对象类型合并适用集合；只取引用时属性状态为not_requested。'
v['native_contract_review']['api_mapping']['en']+=' Preserve PropertySpec.all/pathSet semantics, union applicable sets by object type, and use not_requested for reference-only property state.'
vp.write_text(yaml.safe_dump(v,allow_unicode=True,sort_keys=False,width=110))
# Keep the repeatable serializer consistent with this independently authored supplementary fact.
f=E/'finalize_and_verify.py';s=f.read_text();s=s.replace('examined=[]',"facts['property-spec']="+repr(facts)+'\nexamined=[]');f.write_text(s)
f=E/'validate_handoff.py';s=f.read_text().replace("len(idx)==25,'expected 25 complete temporary objects'","len(idx)==26,'expected 26 complete temporary objects'");f.write_text(s)
print(json.dumps(item,indent=2))
