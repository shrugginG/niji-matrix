"""Serialize reviewed visual-capture admission, claims, cases, and exact reuse."""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
H = {t: yaml.safe_load((RUN / f"{t}-handoff.yaml").read_text(encoding="utf-8")) for t in ("T1113", "T1125")}
REF = {"REF-000484":"REF-000484", "T1113_REF_ATTACK":"REF-000666", "T1113_REF_ATTOR_PDF":"REF-000583",
       "T1113_REF_FUNNYDREAM":"REF-000512", "T1113_REF_VOLEXITY":"REF-000667", "T1113_REF_MITRE_DET":"REF-000668",
       "T1113_REF_SYSMON":"REF-000669", "T1113_REF_MS_WGC":"REF-000670", "T1113_REF_APPLE_SCREEN":"REF-000671",
       "T1125_REF_ATTACK":"REF-000672", "T1125_REF_T9000":"REF-000584", "T1125_REF_INV":"REF-000506",
       "T1125_REF_ZOOM":"REF-000673", "T1125_REF_WARDLE":"REF-000674", "T1125_REF_MS_CAM":"REF-000675",
       "T1125_REF_APPLE_CAM":"REF-000676", "T1125_REF_APPLE_IND":"REF-000677",
       "T1125_REF_MS_PRIVACY":"REF-000586", "T1125_REF_MS_CSP":"REF-000587"}

def refs(keys):return list(dict.fromkeys(REF[x] for x in keys))

def save(folder,filename,record):
    p=ROOT/folder/filename
    p.write_text(yaml.safe_dump(record,allow_unicode=True,sort_keys=False,width=120),encoding='utf-8')

def source_claim(tactic,key):
    return next(x for x in H[tactic]['library_candidates']['claims'] if x.get('key')==key or x.get('temporary_key')==key)

for cid,tid,key,slug,kind,subjects,mode,confidence in [
    ('CLM-000784','T1113','T1113_CLM_PARENT','screen-pixel-acquisition-boundary','technique-relevance',['NJT-0158'],'strongly-inferred','high'),
    ('CLM-000785','T1113','T1113_CLM_GATE','attor-targeted-screen-output','mechanism-mapping',['NJT-0158'],'strongly-inferred','low'),
    ('CLM-000786','T1113','T1113_CLM_CADENCE_LIMIT','bluelight-cadence-stealth-limit','other',['NJT-0158'],'directly-observed','high'),
    ('CLM-000787','T1125','T1125_CLM_PARENT','video-input-frame-boundary','technique-relevance',['NJT-0159'],'strongly-inferred','high'),
    ('CLM-000788','T1125','T1125_CLM_T9000_VIDEO','t9000-call-video-frame-acquisition','subtechnique-existence',['NJT-0159','NJS-0159-001'],'directly-observed','high'),
    ('CLM-000789','T1125','T1125_CLM_CAMERA_SOURCE','invisimole-webcam-screen-difference','technique-boundary',['NJT-0159'],'directly-observed','high'),
]:
    source=source_claim(tid,key)
    statement=source['statement']
    save('claims',f'{cid}-{slug}.yaml',{'schema_version':'1.0.0','type':'claim','id':cid,'claim_type':kind,
        'statement_zh':statement['zh'],'statement_en':statement['en'],'subject_refs':subjects,
        'evidence_refs':refs(source['evidence_keys']),'evidence_mode':mode,'confidence':confidence,'status':'draft'})

def case(cid,slug,name,actor,event,subjects,evidence):
    save('cases',f'{cid}-{slug}.yaml',{'schema_version':'1.0.0','type':'case','id':cid,
        'name_zh':name['zh'],'name_en':name['en'],'actor_or_campaign':actor,'subject_refs':subjects,
        'description_zh':event['zh'],'description_en':event['en'],'time_range':None,
        'target_sectors_zh':[],'target_sectors_en':[],'evidence_refs':refs(evidence),
        'confidence':'high','status':'draft'})

for cid,key,slug,actor in [
    ('CASE-000217','T1113_CASE_ATTOR','attor-target-window-screenshot','Attor'),
    ('CASE-000218','T1113_CASE_FUNNYDREAM','funnydream-continuous-screen-grab','FunnyDream')]:
    x=next(x for x in H['T1113']['library_candidates']['cases'] if x['temporary_key']==key)
    case(cid,slug,x['name'],actor,x['event'],['NJT-0158'],x['evidence_keys'])

# Same T9000 Skype event already has CASE-000198 for audio. Add the observed
# video facts and new target references without manufacturing a second case.
case_path=next((ROOT/'cases').glob('CASE-000198-*.yaml'))
existing=yaml.safe_load(case_path.read_text(encoding='utf-8'))
existing['name_zh']='T9000 经 Skype 接口录制通话媒体'
existing['name_en']='T9000 Skype-Interface Call-Media Recording'
existing['description_zh']='Unit 42 分析 T9000 经已登录 Skype 接口、在用户批准后同时取得通话音频与视频。临时音频及视频分别位于应用数据的子目录；解密产物直接显示周期性视频通话图像，音频为 WAV，均在会后压缩加密。该事件可支持音频与视频的不同直接对象，但不证明现代通话产品具有相同接口，也不证明无提示权限绕过。'
existing['description_en']='Unit 42 analyzed T9000 acquiring call audio and video through a signed-in Skype interface after user approval. Temporary audio and video occupied separate application-data subdirectories; decrypted output directly showed periodic video-call images and WAV audio, followed by post-call compression and encryption. The same event supports distinct audio and video objects but does not prove identical interfaces in current call products or promptless permission bypass.'
for target in ('NJT-0159','NJS-0159-001'):
    if target not in existing['subject_refs']:existing['subject_refs'].append(target)
case_path.write_text(yaml.safe_dump(existing,allow_unicode=True,sort_keys=False,width=120),encoding='utf-8')

# Preserve reference URL identity while widening locators to the exact new
# screenshot, webcam, or video passage. Earlier evidence remains in scope.
updates={
    'REF-000583':('ESET Attor 音频与选定窗口截图插件白皮书','Audio recorder §4.3.3 and Screengrabber §4.3.2, plus collection architecture §§3.2–3.3','同时支持会议进程音频录制及目标进程/前台窗口条件后每十秒截图；两种输入和产物须分别判断。','Supports meeting-process audio and target-process/foreground-window-conditioned ten-second screenshots; input and artifacts require separate judgments.'),
    'REF-000512':('FunnyDream FilePakMonitor 与 ScreenCap 分析','FilePak and FilePakMonitor pp. 14–18; ScreenCap pp. 15–16 GDI+ capture, ws.tmp, and five-second interval','同时支持状态化文件收集与持续五秒抓屏样本；截图节奏未被测为匿迹收益。','Supports stateful file collection and observed continuous five-second screen capture; cadence was not measured as an evasion benefit.'),
    'REF-000584':('Unit 42 对 T9000 Skype 通话媒体录制的分析','Skype API plugin: explicit user approval, audio and video subdirectories, periodic decrypted video-call images and WAV audio','支持旧 Skype 接口下音频和视频通话采集；正常进程提示可能误导但不是无提示绕过。','Supports audio and video call capture through the older Skype interface; a normal-looking prompt may mislead but is not a silent bypass.'),
    'REF-000506':('InvisiMole 内置封装与采集路径','Integrated Zlib and WinRAR paths; internal storage table distinguishes webcam photos from screenshots and audio; command 220 webcam API','同时支持内置压缩路径及摄像头照片与屏幕截图的来源区别；不证明摄像头指示被隐藏。','Supports integrated compression and the source distinction between webcam photos and screen captures; does not show camera-indicator suppression.'),
}
for rid,(zh,locator,note_zh,note_en) in updates.items():
    p=next((ROOT/'references').glob(f'{rid}-*.yaml'))
    d=yaml.safe_load(p.read_text(encoding='utf-8'))
    d['title_zh']=zh;d['locator']=locator;d['notes_zh']=note_zh;d['notes_en']=note_en
    p.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False,width=120),encoding='utf-8')

for tid,nid,zh,en,evidence in [
    ('T1113','NJT-0158','屏幕捕获','Screen Capture',['REF-000666','REF-000583','REF-000512']),
    ('T1125','NJT-0159','视频捕获','Video Capture',['REF-000672','REF-000584','REF-000506'])]:
    recommendation=H[tid]['recommendation'];rationale=recommendation['rationale']['paragraphs'];scope=recommendation['scope_notes']
    save('matrix/tactics/TA0009-collection/decisions',f'DEC-TA0009-{tid}.yaml',{
        'schema_version':'1.1.0','type':'technique-decision','id':f'DEC-TA0009-{tid}','tactic_ref':'TA0009',
        'candidate':{'source_type':'attack','source_attack_id':tid,'source_attack_version':'19.1','name_en':en,'name_zh':zh},
        'decision':'adapt','rationale_zh':'\n\n'.join(x['zh'] for x in rationale),'rationale_en':'\n\n'.join(x['en'] for x in rationale),
        'scope_notes_zh':scope['zh'],'scope_notes_en':scope['en'],'gap_statement_zh':None,'gap_statement_en':None,
        'original_attack_subtechniques_imported':False,'resulting_technique_ref':nid,'evidence_refs':evidence,
        'confidence':recommendation.get('confidence','medium'),
        'review':{'status':'draft','authors':['Niji Matrix Research'],'reviewers':[],
                  'review_notes_zh':'第三批准入与跨技术边界已完成，正式内容及质量门禁待验。',
                  'review_notes_en':'Batch-three admission and cross-technique boundaries are complete; canonical content and quality gates remain.'}})

print('Serialized two decisions, six claims, two new cases; extended CASE-000198 and four exact shared references')
