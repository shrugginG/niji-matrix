"""Serialize implementable screen/video detection and target-specific mitigation."""

from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
H={t:yaml.safe_load((RUN/f'{t}-handoff.yaml').read_text(encoding='utf-8')) for t in ('T1113','T1125')}
LIFE={'status':'draft','version':'1.0.0','created':'2026-09-22','modified':'2026-09-09','contributors':['Niji Matrix Research'],'reviewers':[]}
LIFE['modified']='2026-09-22'
REF={'REF-000484':'REF-000484','REF-000506':'REF-000506','REF-000512':'REF-000512','REF-000583':'REF-000583','REF-000584':'REF-000584','REF-000586':'REF-000586','REF-000587':'REF-000587','REF-000366':'REF-000366',
     'T1113_REF_ATTACK':'REF-000666','T1113_REF_ATTOR_PDF':'REF-000583','T1113_REF_FUNNYDREAM':'REF-000512',
     'T1113_REF_VOLEXITY':'REF-000667','T1113_REF_MITRE_DET':'REF-000668','T1113_REF_SYSMON':'REF-000669',
     'T1113_REF_MS_WGC':'REF-000670','T1113_REF_APPLE_SCREEN':'REF-000671','REF-000484':'REF-000484',
     'T1125_REF_ATTACK':'REF-000672','T1125_REF_T9000':'REF-000584','T1125_REF_INV':'REF-000506',
     'T1125_REF_ZOOM':'REF-000673','T1125_REF_WARDLE':'REF-000674','T1125_REF_MS_CAM':'REF-000675',
     'T1125_REF_APPLE_CAM':'REF-000676','T1125_REF_APPLE_IND':'REF-000677',
     'T1125_REF_MS_PRIVACY':'REF-000586','T1125_REF_MS_CSP':'REF-000587'}

def pair(zh,en):return {'zh':zh,'en':en}
def para(zh,en):return {'paragraphs':[pair(zh,en)]}
def refs(keys):return list(dict.fromkeys(REF[x] for x in keys))
def save(folder,name,obj):
    p=ROOT/folder/name
    p.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120),encoding='utf-8')
def research(tid,kind,key):return next(x for x in H[tid]['defense_candidates'][kind] if x['temporary_key']==key)

NAMES={'camera-device-session':pair('摄像头设备会话','Camera-device session'),
       'process-and-module-provenance':pair('进程与模块来源','Process and module provenance'),
       'endpoint-file-and-media-type':pair('端点文件与媒体类型','Endpoint file and media type'),
       'call-media-interface-audit':pair('通话媒体接口授权审计','Call-media interface grant audit'),
       'video-call-session':pair('视频通话会话事件','Video-call session events'),
       'endpoint-visual-artifact':pair('端点视觉媒体产物','Endpoint visual-media artifact')}
def requirements(items):
    result=[]
    for x in items:
        name=x.get('name') or NAMES[x['source_type']]
        result.append({'source_type':x['source_type'],'name':name,'channel':x.get('channel'),'required_fields':x['required_fields']})
    return result

ANALYTICS=[
    ('NJA-000193','T1113','T1113_NJA_CAPTURE_GATE','DET-000177','foreground-match-screen-pixel-chain',
     pair('前台目标命中后截图链验证','Verify Capture Chain After Foreground-Target Match'),
     pair('把经验证的目标窗口状态、成功取像与屏幕像素产物连接。','Join validated target-window state, successful capture, and screen-pixel output.'),
     ['Windows'],[pair('目标窗口命中后同进程出现截图成功与有间隔的产物','The same process has successful capture and interval-spaced output after a target-window match'),
                  pair('未命中时缺少相应截图结果而驻留模块仍在','The matching capture outcome is absent while the resident module remains before a match')],None),
    ('NJA-000194','T1113','T1113_NJA_CAPTURE_ARTIFACT','DET-000177','screen-artifact-caller-lineage',
     pair('异常截图产物与调用者谱系关联','Correlate Unusual Screenshot Artifacts With Caller Lineage'),
     pair('用文件和进程证据确认截图产物及其调用者，区分普通业务序列。','Confirm a screen-image artifact and its caller from file and process evidence, distinguishing approved capture sequences.'),
     ['Windows'],[pair('非批准进程形成经图像头或解码确认的屏幕像素产物','An unapproved process writes an artifact confirmed by image header or decode to contain screen pixels'),
                  pair('连续产物与同一会话和写入进程相连','A sequence of artifacts links to the same session and writer process')],None),
    ('NJA-000195','T1125','T1125_NJA_CAMERA','DET-000178','camera-session-visual-output',
     pair('非批准摄像头会话后的视觉产物','Visual Output Following an Unapproved Camera Session'),
     pair('将实际摄像头设备会话与调用进程、可信图像或视频产物相连。','Join an actual camera-device session to its caller and a confirmed image or video artifact.'),
     ['Windows'],[pair('非批准进程打开摄像头并形成经内容确认的画面文件','An unapproved process opens the camera and produces content-confirmed imagery'),
                  pair('摄像头会话时间与媒体文件写入时间闭合','Camera-session time aligns with media-file creation')],
     pair('从设备激活前五分钟到会话结束后十五分钟关联，按产品实测时间漂移调整。','Join from five minutes before device activation through fifteen minutes after the session ends, adjusting for measured clock drift.')),
    ('NJA-000196','T1125','T1125_NJA_CALL','DET-000179','call-interface-grant-video-frame-output',
     pair('视频会话接口附着后的周期性画面文件','Periodic Call Frames After Media-Interface Attachment'),
     pair('连接第三方接口授权、视频会话及经内容确认的通话帧结果。','Join third-party interface grant, video-call session, and content-confirmed call-frame output.'),
     ['Windows'],[pair('未经批准的请求者在通话附近取得媒体接口权限','An unapproved requester gains media-interface access near a call'),
                  pair('同一视频会话随后出现周期性通话帧产物','Periodic call-frame artifacts then appear for the same video session')],
     pair('从通话开始前十五分钟到结束后三十分钟关联；缺少产品接口日志时不输出确认结论。','Join fifteen minutes before call start through thirty minutes after call end; without product interface audit, do not emit a confirmed result.'))]

for aid,tid,key,strategy,slug,name,summary,platforms,observables,manual_window in ANALYTICS:
    x=research(tid,'detection_analytics',key)
    if 'paragraphs' in x['logic']:logic=x['logic']
    else:logic=para(x['logic']['zh'],x['logic']['en'])
    if isinstance(x['correlation']['window'],dict):window=x['correlation']['window']
    else:window=manual_window
    assert window is not None
    fp=x['false_positives'] if isinstance(x['false_positives'],list) else [x['false_positives']]
    blind=x['blind_spots'] if isinstance(x['blind_spots'],list) else [x['blind_spots']]
    guide=x['tuning_guidance']
    if 'paragraphs' not in guide:guide=para(guide['zh'],guide['en'])
    obj={'schema_version':'2.0.0','type':'detection-analytic','id':aid,'strategy_ref':strategy,
         'name':name,'summary':summary,'domains':['enterprise'],'platforms':platforms,'logic':logic,
         'data_requirements':requirements(x['data_requirements']),'observables':observables,
         'correlation':{'window':window,'dimensions':x['correlation']['dimensions']},
         'false_positives':fp,'blind_spots':blind,'tuning_guidance':guide,
         'evidence_refs':refs(x['evidence_keys']),'lifecycle':LIFE.copy()}
    save('analytics',f'{aid}-{slug}.yaml',obj)

STRATEGIES=[
    ('DET-000177','T1113','screen-window-condition-to-pixel-outcome',
     pair('窗口条件与屏幕像素结果关联','Correlate Window Conditions With Acquired Screen Pixels'),
     pair('验证目标情境后的实际取像和产物，而非只发现窗口条件或截图工具。','Verify actual capture and output after target context, not only a window condition or screenshot tool.'),
     para('NJA-000193 在已验证 GUI/图形传感器的端点上连接目标窗口状态、取像成功和结果间隔；NJA-000194 在可审计输出面以文件内容识别和进程谱系确认屏幕像素产物。策略区分窗口发现、图形调用、产物已证三层；合法远程支持、RPA、会议共享和用户截图按任务与会话排除。','NJA-000193 joins target-window state, successful capture, and result intervals on endpoints with validated GUI and graphics sensors. NJA-000194 confirms screen-pixel artifacts through content inspection and process lineage in auditable outputs. The strategy separates window discovery, graphics call, and proven artifact, excluding approved remote support, RPA, meeting sharing, and user screenshots by task and session.'),
     ['NJT-0158'],['NJA-000193','NJA-000194'],['REF-000666','REF-000583','REF-000512']),
    ('DET-000178','T1125','camera-session-visual-source-lineage',
     pair('摄像头会话与画面产物来源关联','Camera-Session to Visual-Artifact Provenance Correlation'),
     pair('以设备会话和实际媒体内容确认未批准摄像头取像。','Confirm unapproved camera acquisition through device sessions and real media content.'),
     para('NJA-000195 要求部署环境已验证摄像头设备会话能与进程、模块及文件结果联接。摄像头使用或图片后缀本身只形成调查线索；必须有来源于相机的可信帧产物、缺少业务批准及正常会议或拍照基线差异，才升级为采集候选。通话应用接口取得的远端参与者画面由另一个策略处理。','NJA-000195 requires locally verified joins from camera-device sessions to process, module, and file outcomes. Camera use or an image extension alone is an investigation lead. A confirmed camera-derived frame, absent business approval, and a difference from normal meetings or photography are needed to raise an acquisition candidate. The other strategy covers remote-party imagery obtained through a call-app interface.'),
     ['NJT-0159'],['NJA-000195'],['REF-000672','REF-000506','REF-000675','REF-000676']),
    ('DET-000179','T1125','video-call-grant-to-frame-output',
     pair('视频通话第三方授权与帧产物关联','Video-Call Third-Party Grant to Frame-Output Correlation'),
     pair('证明非批准接口请求者在视频通话中取得帧，而非只有授权提示。','Prove an unapproved interface requester obtained video-call frames rather than only a grant prompt.'),
     para('NJA-000196 仅用于实际导出第三方接口与视频模态审计的通话产品，联查请求者授权、会话、临时帧与后继产物。T9000 的旧 Skype 路径支持历史实例，不是现代统一字段；只有授权没有帧结果时保留为暴露或企图。合法录制机器人、质检和会议纪要集成按批准组件与期限排除。','NJA-000196 applies only where a call product exports third-party interface and video-modality audit, joining requester grants, session, temporary frames, and later output. T9000’s older Skype path is historical evidence rather than a universal modern field. A grant without frames remains exposure or attempt. Approved recording bots, quality assurance, and meeting-note integrations are excluded by requester and expiry.'),
     ['NJT-0159','NJS-0159-001'],['NJA-000196'],['REF-000672','REF-000584'])]
for sid,tid,slug,name,summary,description,subjects,analytics,extra in STRATEGIES:
    evidence=list(extra)
    for aid in analytics:
        a=yaml.safe_load(next((ROOT/'analytics').glob(f'{aid}-*.yaml')).read_text())
        evidence.extend(a['evidence_refs'])
    evidence=list(dict.fromkeys(evidence))
    save('detections',f'{sid}-{slug}.yaml',{'schema_version':'2.0.0','type':'detection-strategy','id':sid,
         'name':name,'summary':summary,'description':description,'detects_refs':subjects,
         'domains':['enterprise'],'analytic_refs':analytics,'evidence_refs':evidence,'lifecycle':LIFE.copy()})

# Screen capture needs its own output control, even though MIT-000130 already
# owns window-state governance. Do not add an application for a duplicate NJS.
screen=research('T1113','mitigations','T1113_MIT_CAPTURE')
save('mitigations','MIT-000160-screen-capture-actor-output-governance.yaml',{
    'schema_version':'2.0.0','type':'mitigation','id':'MIT-000160','name':screen['name'],
    'summary':screen['summary'],'description':screen['description'],'domains':['enterprise'],
    'measures':screen['measures'],
    'applications':[{'target_ref':'NJT-0158',
       'use':para(screen['applications'][0]['use']['zh'],screen['applications'][0]['use']['en']),
       'expected_effect':para(screen['applications'][0]['expected_effect']['zh'],screen['applications'][0]['expected_effect']['en']),
       'limitations':para(screen['applications'][0]['limitations']['zh'],screen['applications'][0]['limitations']['en'])}],
    'evidence_refs':refs(screen['evidence_keys']),'lifecycle':LIFE.copy()})

camera=research('T1125','mitigations','T1125_MIT_CAMERA')
camera_names=[pair('按业务限制摄像头授权','Business-Scoped Camera Grants'),pair('会议与相机应用完整性','Meeting and Camera App Integrity')]
measures=[{'key':x['key'],'name':camera_names[i],
           'description':para(x['description']['zh'],x['description']['en']),'control_type':x['control_type']}
          for i,x in enumerate(camera['measures'])]
app=camera['applications'][0]
save('mitigations','MIT-000161-camera-access-app-integrity.yaml',{
    'schema_version':'2.0.0','type':'mitigation','id':'MIT-000161','name':camera['name'],
    'summary':pair('限制未经批准的摄像头取像并保留相机应用与模块来源。','Constrain unauthorized camera acquisition and retain provenance of camera apps and modules.'),
    'description':para(camera['description']['zh'],camera['description']['en']),'domains':['enterprise'],
    'measures':measures,'applications':[{'target_ref':'NJT-0159',
       'use':para(app['use']['zh'],app['use']['en']),
       'expected_effect':para(app['expected_effect']['zh'],app['expected_effect']['en']),
       'limitations':para(app['limitations']['zh'],app['limitations']['en'])}],
    'evidence_refs':refs(camera['evidence_keys']),'lifecycle':LIFE.copy()})

# MIT-000149 already governs third-party call-media grants for T1123. Its
# measures are unchanged. Add exact video applications and broaden the scope
# wording to audio/video without duplicating its ID.
path=next((ROOT/'mitigations').glob('MIT-000149-*.yaml'))
shared=yaml.safe_load(path.read_text(encoding='utf-8'))
shared['summary']=pair('审批第三方通话音视频媒体接口，并把授权与录制结果连接。','Approve third-party call audio/video media interfaces and join grants to recording outcomes.')
shared['description']=para('对提供音频或视频媒体接口的受管通话应用，按请求组件、用户、会话、模态和有效期限制第三方授权，并保存授予及撤销记录。通话时段、音频和视频产物均与授权链比较；不提供接口审计的产品须退回端点应用控制，旧 Skype API 名称不能当作现行通用字段。',
    'For managed call apps with audio or video media interfaces, constrain third-party grants by requester, user, session, modality, and duration, retaining grant and revocation records. Compare call intervals and audio or video output to the grant chain. Products without interface audit require endpoint application control, and old Skype API names are not universal modern fields.')
video=research('T1125','mitigations','T1125_MIT_CALL')
shared['applications']=[x for x in shared['applications'] if x['target_ref'] not in {'NJT-0159','NJS-0159-001'}]
for target,x in zip(['NJT-0159','NJS-0159-001'],video['applications']):
    shared['applications'].append({'target_ref':target,
        'use':para(x['use']['zh'],x['use']['en']),
        'expected_effect':para(x['expected_effect']['zh'],x['expected_effect']['en']),
        'limitations':para(x['limitations']['zh'],x['limitations']['en'])})
shared['evidence_refs']=list(dict.fromkeys(shared['evidence_refs']+['REF-000672','REF-000584']))
shared['lifecycle']['version']='1.1.0';shared['lifecycle']['modified']='2026-09-22'
path.write_text(yaml.safe_dump(shared,allow_unicode=True,sort_keys=False,width=120),encoding='utf-8')

print('Serialized 3 Strategies, 4 Analytics, 2 new Mitigations; extended MIT-000149')
