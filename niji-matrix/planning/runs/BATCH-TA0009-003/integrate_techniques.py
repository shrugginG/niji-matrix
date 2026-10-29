"""Assemble reviewed screen/video parent prose and one native video child."""

from copy import deepcopy
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
H={t:yaml.safe_load((RUN/f'{t}-handoff.yaml').read_text(encoding='utf-8')) for t in ('T1113','T1125')}
BASE=ROOT/'matrix/tactics/TA0009-collection/techniques'
LIFE={'status':'draft','version':'1.0.0','created':'2026-09-22','modified':'2026-09-22','contributors':['Niji Matrix Research'],'reviewers':[]}
REF={'T1113_REF_ATTACK':'REF-000666','T1113_REF_ATTOR_PDF':'REF-000583','T1113_REF_FUNNYDREAM':'REF-000512',
     'T1113_REF_VOLEXITY':'REF-000667','T1113_REF_MITRE_DET':'REF-000668','T1113_REF_SYSMON':'REF-000669',
     'T1113_REF_MS_WGC':'REF-000670','T1113_REF_APPLE_SCREEN':'REF-000671','REF-000484':'REF-000484',
     'T1125_REF_ATTACK':'REF-000672','T1125_REF_T9000':'REF-000584','T1125_REF_INV':'REF-000506',
     'T1125_REF_ZOOM':'REF-000673','T1125_REF_WARDLE':'REF-000674','T1125_REF_MS_CAM':'REF-000675',
     'T1125_REF_APPLE_CAM':'REF-000676','T1125_REF_APPLE_IND':'REF-000677',
     'T1125_REF_MS_PRIVACY':'REF-000586','T1125_REF_MS_CSP':'REF-000587'}

def block(zh,en):return {'paragraphs':[{'zh':zh,'en':en}]}
def refs(keys):return list(dict.fromkeys(REF[x] for x in keys))
def mechanisms(items):
    out=[]
    for source in items:
        value={k:deepcopy(source[k]) for k in ('mechanism_ref','role','summary','analysis','confidence')}
        value['evidence_refs']=refs(source['evidence_keys'])
        out.append(value)
    return out
def defense(strategies,mitigations):return {'detections':{'coverage':'available','strategy_refs':strategies},'mitigations':{'coverage':'available','mitigation_refs':mitigations}}
def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False,width=120),encoding='utf-8')

TAXONOMY={
    'T1113':block('屏幕捕获已有可证的条件性取像与连续取像对照，但“窗口状态决定后继截图何时出现”的可控变量及非命中时段缺席的痕迹差，已由 NJS-0132-001 规范拥有。T1113 父技术要求实际取得显示像素，其 DET/NJA 再核实条件命中后取像结果；增加这一结果条件不会创造第二项 Niji 子技术。截图节奏、API 与文件格式也没有独立且足证的匿迹边界，因此当前不设子项。',
        'Evidence shows both conditional and continuous screen acquisition, but NJS-0132-001 already owns the controlled variable in which window state decides when later screenshots appear and their absence during nonmatches. The T1113 parent requires actual display pixels, while its DET/NJA verifies capture after a match; adding that outcome condition does not create another Niji variable. Cadence, API, and file format lack separate sufficiently supported stealth boundaries, so the current taxonomy has no children.'),
    'T1125':block('通话接口语境取帧是当前唯一成立的原生子项：第三方视觉采集借真实通话应用的媒体授权和会话承载，防守需联查请求者、授予、视频会话及帧产物。独立打开摄像头是父级对照；既有摄像头会话寄生与受信会议进程权限继承目前只有研究演示，不能当作野外子项。OS、摄像头品牌、接口名称、图片后缀或视频文件格式都不是稳定分类基础。',
        'Call-Interface-Context Frame Capture is the sole established native child: third-party visual acquisition rides a real call app media grant and session, requiring a join across requester, grant, video session, and frame output. Direct camera opening is a parent comparator. Piggybacking on an existing camera session and inheriting a trusted meeting process grant remain research demonstrations rather than field children. OS, camera brand, interface name, image extension, and movie-file format are not stable partitions.')}
LIMITS={
    'T1113':{'paragraphs':[
        {'zh':'ESET 的 Attor 逆向分析证明条件匹配及其后的截图，但没有量化检出率；Bitdefender 的 FunnyDream 是持续抓屏与文件痕迹对照，Volexity 的 BLUELIGHT 只证明频率改变而非规避目的。条件门控造成非命中时段缺少截图，是根据代码和结果作出的低置信度观察推断，不得将其升级为实测告警下降。相同窗口变量已经由 NJS-0132-001 记录，屏幕像素结果则由本父级承担。',
         'en':'ESET reverse engineering proves Attor’s condition and later screenshots but does not measure detection rates. Bitdefender’s FunnyDream supplies a continuous capture and file-trace comparator; Volexity’s BLUELIGHT proves cadence change, not evasion intent. Absence of screenshots while a condition is false is a low-confidence observation inference from code and result, not a measured alert reduction. NJS-0132-001 already records the window variable, while this parent owns the acquired display pixels.'},
        {'zh':'实际检测依赖经试点验证的图形与窗口传感器及可确认的像素产物。Sysmon 进程、模块和文件事件只提供谱系与产物线索，不能冒充截图 API 日志；Windows.Graphics.Capture 的选择器和边框也不能外推到 GDI 或全部截图路径。macOS 屏幕授权界面不保证集中可导出逐次事件。合法远程支持、会议共享、无障碍和用户主动截图需按任务授权排除。',
         'en':'Detection depends on pilot-validated graphics and window sensors plus verifiable pixel output. Sysmon process, module, and file events supply lineage and artifact leads, not screenshot-API logs. The Windows.Graphics.Capture picker and border do not generalize to GDI or every capture path. A macOS screen grant UI does not guarantee centrally exported per-capture events. Authorized remote support, meeting sharing, accessibility, and user screenshots require task-level exclusion.'}
    ]},
    'T1125':{'paragraphs':[
        {'zh':'Unit 42 对 T9000 的视频事实来自逆向与解密产物观察，旧 Skype API 不能代表现行会议客户端。用户必须批准接口请求；报告只说正常进程提示可能误导，不证明无提示绕过或告警下降。InvisiMole 的类型表区分 webcam 照片与屏幕截图，但不证明每次执行均有视频结果。既有摄像头会话寄生和 Zoom 权限继承是实验演示，应留在待证范围。',
         'en':'Unit 42’s T9000 video facts come from reverse engineering and decrypted output, but the old Skype API does not represent current meeting clients. The user had to approve interface access; the report describes possible prompt confusion, not silent bypass or fewer alerts. InvisiMole’s type table separates webcam photos from screen screenshots without proving a video result on every execution. Existing-camera-session piggybacking and Zoom grant inheritance are research demonstrations and remain unadmitted.'},
        {'zh':'Windows 与 Apple 文档说明用户可见的相机许可、指示与控制能力，不保证端点或会议产品能导出设备会话、接口请求者、视频模态和帧内容键。缺失这些数据时只能形成设备访问或授权暴露线索。合法会议录制、远程支持、质检和用户拍照也可产生相同外观，不能由摄像头灯、文件扩展名或批准点击单独断言恶意采集。',
         'en':'Windows and Apple documents describe user-visible camera grants, indicators, and controls, not guaranteed exports of device session, interface requester, video modality, or frame-content keys. Without those data, only device-access or grant-exposure leads are justified. Authorized meeting recording, remote support, quality assurance, and user photography can look alike; a camera light, file extension, or approval click alone cannot establish malicious capture.'}
    ]}}

PARENTS=[
    ('T1113','NJT-0158','stealth-oriented-screen-capture',[], 'none-justified', ['DET-000177'],['MIT-000160'],
     ['CLM-000784','CLM-000785','CLM-000786'],['CASE-000217','CASE-000218'],
     ['REF-000666','REF-000583','REF-000484','REF-000512','REF-000667','REF-000668','REF-000669','REF-000670','REF-000671']),
    ('T1125','NJT-0159','stealth-oriented-video-capture',['NJS-0159-001'],'established',['DET-000178','DET-000179'],['MIT-000161','MIT-000149'],
     ['CLM-000787','CLM-000788','CLM-000789'],['CASE-000198'],
     ['REF-000672','REF-000584','REF-000506','REF-000673','REF-000674','REF-000675','REF-000676','REF-000677','REF-000586','REF-000587'])]

ROOTS={}
for tid,nid,slug,children,coverage,strategies,mitigations,claims,cases,evidence in PARENTS:
    content=H[tid]['proposed_content']
    formal_mechanisms=mechanisms(content['stealth_mechanisms'])
    if tid=='T1113':
        formal_mechanisms=[{'mechanism_ref':'NM-BT','role':'primary',
            'summary':{'zh':'目标窗口未命中时不产生截图结果，延迟可见采集链','en':'Withhold screenshot results before a target-window match, delaying the visible capture chain'},
            'analysis':block('攻击者将实际取像绑定到目标进程与前台窗口条件。Attor 的加密截图在命中后按十秒间隔出现，非命中时缺少这条结果链；只看截图文件的防守方难以把等待期与之后的采集连成同一行为。命中后的取像和产物仍可观察，检测率变化没有实测。此条件缺席机理与 NJS-0132-001 属于同一窗口门控轴；本父级只补充证明显示像素已取得，不据此增加第二个子技术。',
                             'The adversary binds actual pixel acquisition to a target-process and foreground-window condition. Attor produced encrypted screenshots at ten-second intervals after matches, leaving no corresponding outcome chain during nonmatches. A defender watching only image files may fail to connect the waiting period to later capture. Post-match capture and artifacts remain visible, and a change in detection rate was not measured. This absence-on-nonmatch mechanism is the same window-gating axis already owned by NJS-0132-001; this parent adds proof that display pixels were obtained, not another child.'),
            'evidence_refs':['REF-000583','REF-000484'],'confidence':'low'}]
    record={'schema_version':'2.0.0','type':'technique','id':nid,'name':deepcopy(content['name']),
            'summary':deepcopy(content['summary']),'aliases':[],
            'classification':{'tactic_refs':['TA0009'],'origin':{'kind':'attack-adapted','source_attack_id':tid,'source_attack_version':'19.1'},'decision_ref':f'DEC-TA0009-{tid}'},
            'definition_and_concept':deepcopy(content['definition_and_concept']),
            'stealth_characteristics':deepcopy(content['stealth_characteristics']),
            'scope_boundary_definition':deepcopy(content['scope_boundary_definition']),
            'application_scenarios_and_threat_model':deepcopy(content['application_scenarios_and_threat_model']),
            'stealth_mechanisms':formal_mechanisms,
            'subtechnique_taxonomy':{'narrative':TAXONOMY[tid],'coverage':coverage,'subtechnique_refs':children},
            'defense':defense(strategies,mitigations),
            'evidence':{'claim_refs':claims,'case_refs':cases,'reference_refs':evidence},
            'research':{'limitations':LIMITS[tid]},'lifecycle':deepcopy(LIFE)}
    for m in record['stealth_mechanisms']:assert set(m['evidence_refs']).issubset(evidence)
    folder=BASE/f'{nid}-{slug}';save(folder/'technique.yaml',record);ROOTS[tid]=folder

child=next(x for x in H['T1125']['proposed_subtechniques'] if x['temporary_key']=='T1125_CHILD_CALL')
record={'schema_version':'2.0.0','type':'evasion-subtechnique','id':'NJS-0159-001','parent_ref':'NJT-0159',
        'name':deepcopy(child['name']),'summary':deepcopy(child['summary']),'aliases':[],
        'lineage':{'attck_subtechnique_inherited':False},
        'definition_and_concept':deepcopy(child['definition_and_concept']),
        'stealth_characteristics':deepcopy(child['stealth_characteristics']),
        'scope_boundary_definition':deepcopy(child['scope_boundary_definition']),
        'application_scenarios_and_threat_model':deepcopy(child['application_scenarios_and_threat_model']),
        'stealth_mechanisms':mechanisms(child['stealth_mechanisms']),
        'defense':defense(['DET-000179'],['MIT-000149']),
        'evidence':{'claim_refs':['CLM-000788'],'case_refs':['CASE-000198'],
                    'reference_refs':['REF-000672','REF-000584','REF-000675','REF-000676','REF-000677']},
        'research':{'limitations':deepcopy(child['limitations'])},'lifecycle':deepcopy(LIFE)}
assert record['stealth_characteristics']['paragraphs'][0]['zh'].startswith(record['name']['zh'])
assert record['stealth_characteristics']['paragraphs'][0]['en'].startswith(record['name']['en'])
for m in record['stealth_mechanisms']:assert set(m['evidence_refs']).issubset(record['evidence']['reference_refs'])
save(ROOTS['T1125']/'subtechniques/NJS-0159-001-call-interface-context-frame-capture/subtechnique.yaml',record)

print('Serialized two bilingual parent techniques and one native video child in draft')
