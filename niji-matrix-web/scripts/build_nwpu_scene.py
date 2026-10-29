"""Rebuild the attributed NWPU report reconstruction; never modifies matrix YAML."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
status=json.loads((ROOT/'public/data/status.json').read_text())
index=json.loads((ROOT/'public/data'/status['revision']/'index.json').read_text())
BLACK='#354b40'; RED='#cf443b'; CYAN='#159ebb'; GREEN='#39814a'; BLUE='#6479a0'
scene=dict(schemaVersion='1.0.0',id='nwpu-nsa-report',name='NSA 入侵西北工业大学',category='case',author='拓扑依据：ABC_123 / 希潭实验室；画布整理：Niji Matrix',description='本案例展示针对西北工业大学的网络入侵过程，涵盖匿名基础设施准备、境外跳板中转、边界设备入侵、浏览器攻击、内网渗透及信息回传，并标注各阶段涉及的匿迹技术与子技术。',createdAt='2026-10-22T00:00:00Z',updatedAt='2026-10-22T00:00:00Z',matrix=dict(id='niji-matrix',version=index['matrix']['lifecycle']['version'],revision=status['revision']),nodes=[],edges=[],bindings=[],viewport=dict(x=20,y=20,zoom=.14),sources=[],views=[],legend=[dict(label='黑线：组织、资源、部署与控制关系（以标签为准）',color=BLACK,lineStyle='solid'),dict(label='红线：原图重点关系及 A1—A3 路径',color=RED,lineStyle='solid'),dict(label='青线：办公终端 B1—B3 路径',color=CYAN,lineStyle='solid'),dict(label='绿虚线：邮件钓鱼投递',color=GREEN,lineStyle='dashed'),dict(label='蓝虚框：平台或网络范围；浅灰框：排版分区',color=BLUE,lineStyle='dashed')],reviewNotes=[
'所有“报道陈述”均表示上传材料如此记载，不表示本系统独立核实。作者明确声明其分析来自公开资料及个人经验。',
'原图的 49 台跳板机集合仅展开七个代表节点；不补画其余 42 台。两个日本节点的脱敏地址相同但时间标签不同，按原图分别保留。',
'办公网用户1—用户6为原图表示，不推断六人的真实身份；“多台服务器／终端”保持集合表达。',
'Foxacid 的四种载荷递送方式属于原图的平台能力展示，不把它们全部认定为本案已观测攻击步骤。',
'边界设备上的 NOPEN、二次约会按文字和图中标注表达；逻辑工具节点不是独立物理主机。原图中并列但无箭头的设备不自动补连。',
'Register 匿名保护服务与利用工具之间的线忠实保留原图编排，不表示该服务商是发动攻击的主体。',
'“首尔国立江原大学”、工具译名、“suctionchar”等文字按原图保留，未作外部校订。20xx 日期与脱敏地址也不补全。',
'CDR 为报道原称，保留原文不推定其完整协议或密码实现。Foxsearch 属于汇总检索用途，不推断具体运行位置。',
'“狡诈异端犯”在正文中使用“可能会安装”的表述，相关关系标记为作者分析，不作为确定部署事实。',
'矩阵关联均为对报道行为的分析映射，未仅凭工具名称断言具体子技术；反调试能力未进一步映射到某个实现子技术。',
'灰色组织／准备／工具区框与局部视图为展示处理；蓝色 Foxacid、跳板网络、西工大及办公网范围对应原图。'
])
figures={'overview':'总拓扑图','organization':'NSA / TAO 组织职责','preparation':'资源准备与平台','relays-boundary':'跳板与边界概览','boundary':'边界入侵与工具部署','foxacid-office':'Foxacid 与办公网','platform-boundary':'平台与边界关系','internal':'跳板与内网横向','paths':'A / B / 邮件路径','tools':'内网与驻留工具'}
scene['sources']=[dict(id='nwpu-report',title='第58篇：美国安全局NSA入侵西北工业大学流程图梳理和分析（正式篇）',author='ABC_123 / 希潭实验室',publishedAt='2023-04-22',assetPath='/case-assets/nwpu/report.txt')]+[dict(id='fig-'+key,title='原图：'+name,author='ABC_123 / 希潭实验室',publishedAt='2023-04-22',assetPath=f'/case-assets/nwpu/{key}.png') for key,name in figures.items()]
lookup={}; inventory=[]
def evidence(fig,loc,basis='reported',note=''):
 return [dict(sourceRef='fig-'+fig,locator=loc,basis=basis,**({'note':note} if note else {}))]
def node(id,name,kind,x,y,*,category='endpoint',parent=None,w=210,h=120,subtitle='',notes='',fig='overview',loc='',attrs=None,logical=None,container=False,color='#ffffff',basis='reported'):
 n=dict(id=id,kind=kind,category=category,name=name,position=dict(x=x,y=y),size=dict(width=w,height=h),color=color,notes=notes,container=container,provenance=evidence(fig,loc or name,basis))
 if parent:n['parentId']=parent
 if subtitle:n['subtitle']=subtitle
 if attrs:n['attributes']=attrs
 if logical:n['entityClass']=logical
 scene['nodes'].append(n);lookup[id]=n;inventory.append(dict(id=id,element='node',label=name,source=fig,locator=loc or name,interpretation=basis));return n
def zone(id,name,x,y,w,h,fig='overview',parent=None,original=True):
 n=node(id,name,'networkZone',x,y,category='auxiliary',parent=parent,w=w,h=h,container=True,fig=fig,notes='原图虚线分区' if original else '用于阅读的展示分区，不增加事件事实',basis='reported' if original else 'layout');n['borderColor']=BLUE if original else '#cad5ce';return n
def absolute(id):
 n=lookup[id];p=dict(n['position']);parent=n.get('parentId')
 while parent:
  n=lookup[parent];p['x']+=n['position']['x'];p['y']+=n['position']['y'];parent=n.get('parentId')
 return p
def edge(id,src,dst,name,relation='control',*,fig='overview',loc='',color=BLACK,style='solid',sp=None,tp=None,points=None,label=None,basis='reported',note='',pathGroup=None):
 a,b=absolute(src),absolute(dst);na,nb=lookup[src],lookup[dst];dx=b['x']+nb['size']['width']/2-a['x']-na['size']['width']/2;dy=b['y']+nb['size']['height']/2-a['y']-na['size']['height']/2
 if abs(dx)>abs(dy):default=('right','left') if dx>=0 else ('left','right')
 else:default=('bottom','top') if dy>=0 else ('top','bottom')
 e=dict(id=id,source=src,target=dst,sourcePort=sp or default[0],targetPort=tp or default[1],name=name,relation=relation,direction='forward',lineStyle=style,routing='straight' if not points else 'step',color=color,notes=note,waypoints=[dict(x=x,y=y) for x,y in (points or [])],anchorMode='manual',provenance=evidence(fig,loc or name,basis))
 if label:e['labelPosition']=dict(x=label[0],y=label[1])
 if pathGroup:e['pathGroup']=pathGroup
 scene['edges'].append(e);inventory.append(dict(id=id,element='edge',source=src,target=dst,label=name,figure=fig,locator=loc or name,interpretation=basis));return e
# Organization: source's ten responsibility units around TAO, not ten independent attackers.
zone('zone-org','组织与职责',630,0,1800,820,'organization',original=False)
node('nsa','美国 NSA','organization',790,55,category='human',parent='zone-org',subtitle='报道中的攻击组织',fig='organization')
node('tao','TAO 特定入侵行动办公室','department',770,340,category='human',parent='zone-org',w=260,h=145,fig='organization')
units=[('roc','ROC (S321)','远程操作中心',390,620,'操作武器库／控制目标网络'),('ant','ANT (S322)','先进 / 接入网络技术处',50,245,'硬件技术／武器装备'),('dnt','DNT (S323)','数据网络技术处',50,440,'研发复杂软件'),('tnt','TNT (S324)','电信网络技术处',50,630,'研究电信技术／隐蔽渗透'),('mit','MIT (S325)','任务基础设施技术处',1110,620,'侦查监控／构建匿名网络'),('ao','AO (S326)','接入行动处',1500,240,'供应链／后门安装'),('rt','R&T (S327)','需求与定位处',390,60,'行动战略／评估情报价值'),('ato','ATO (S328)','接入技术行动处',1500,440,'研发接触式窃密装置'),('ppi','PPI (S32P)','项目计划整合处',1190,60,'总体规划／项目管理'),('nwt','NWT','网络战小组',1500,630,'联络网络作战小组')]
edge('nsa-tao','nsa','tao','下属部门','affiliation',fig='organization')
for id,name,sub,x,y,duty in units:
 node(id,name,'department',x,y,category='human',parent='zone-org',subtitle=sub,fig='organization',attrs={'职责（原图）':duty})
 edge('tao-'+id,'tao',id,duty,'support',fig='organization',color=RED if id=='mit' else BLACK)
# Anonymous access resources; address resources are not invented individual machines.
for j,ip in enumerate(['207.195.240.*','209.59.36.*','69.165.54.*','209.118.143.*']):
 node('us-ip-'+str(j+1),ip,'ipAddress',70+j*265,950,category='cloud',subtitle='美国运营商接入 IP',fig='relays-boundary',logical='artifact')
 edge('tao-ip-'+str(j+1),'tao','us-ip-'+str(j+1),'TAO 接入来源','control',fig='relays-boundary',color=RED if j==0 else BLACK)
node('register','Register 匿名保护服务','privacyService',500,1260,category='cloud',w=260,fig='preparation',attrs={'保护对象':'域名、证书与注册人信息'})
for j in range(4):edge('ip-register-'+str(j+1),'us-ip-'+str(j+1),'register','匿名保护','registration',fig='relays-boundary')
node('razor','“剃须刀”工具','softwareTool',420,1580,logical='software',fig='relays-boundary',subtitle='Solaris / RPC 远程溢出',attrs={'原图集合规模':'49 台跳板机'},notes='表现报道中的工具与用途，不包含实现或操作参数。')
node('island','“孤岛”工具','softwareTool',1370,1580,logical='software',fig='boundary',subtitle='Solaris 远程溢出',notes='正文强调该工具不具备自主探测开放服务能力；不补入扫描步骤。')
edge('register-razor','register','razor','构建匿名化跳板网络','custom',fig='relays-boundary',note='原图编排；不表示 Register 服务商直接实施漏洞攻击。')
edge('register-island','register','island','边界入侵准备（原图关系）','custom',fig='boundary',note='原图编排关系，不将 Register 认定为攻击执行者。')
# Commercial resources and a named false identity.
zone('zone-prep','匿名化基础设施准备',2480,0,1220,900,'preparation',original=False)
node('cover-one','杰克·史密斯咨询公司','company',40,80,category='human',parent='zone-prep',subtitle='报道中的掩护公司',fig='preparation')
node('cover-two','穆勒多元系统公司','company',350,80,category='human',parent='zone-prep',subtitle='报道中的掩护公司',fig='preparation')
node('terremark','泰瑞马克公司','company',790,80,category='human',parent='zone-prep',fig='preparation')
node('leased','租赁服务器与地址资源','rentalService',790,340,category='cloud',parent='zone-prep',w=280,subtitle='埃及 / 荷兰 / 哥伦比亚',fig='preparation')
node('identity','Amanda Ramirez','identity',40,355,category='human',parent='zone-prep',subtitle='阿曼达·拉米雷斯（假名）',fig='preparation')
node('domain','www.xxx.com','domain',70,640,category='cloud',parent='zone-prep',subtitle='原图占位域名',logical='artifact',fig='preparation')
node('cert','通用 SSL 证书','certificate',430,640,category='cloud',parent='zone-prep',subtitle='ID：e42d***（原图脱敏）',logical='artifact',fig='preparation')
for id in ['cover-one','cover-two']:edge('mit-'+id,'mit',id,'成立掩护公司','procurement',fig='preparation',color=RED);edge(id+'-terremark',id,'terremark','购买 / 租赁','procurement',fig='preparation')
edge('terremark-leased','terremark','leased','服务器与地址资源','procurement',fig='preparation')
edge('mit-identity','mit','identity','假名身份','affiliation',fig='preparation',color=RED)
edge('identity-domain','identity','domain','用假名购买域名','registration',fig='preparation')
edge('identity-cert','identity','cert','用假名购买证书','registration',fig='preparation')
# Relay set: preserve seven explicitly drawn nodes, including repeated masked addresses.
zone('zone-relays','境外跳板网络｜原图称 49 台，展开 7 个节点',50,1920,1120,1370,'internal')
relays=[('jp-one','日本跳板机 1','210.135.x.x','20xx年3月2日3时41分',40,130,''),('jp-two','日本跳板机 2','210.135.x.x','20xx年5月30日0时28分',390,130,''),('jp-three','日本跳板机 3','130.54.x.x','20xx年12月11日6时52分',740,130,'日本京都大学'),('de','德国跳板机','141.57.x.x','20xx年7月4日1时12分',40,510,'莱比锡技术经济和文化学院'),('kr-one','韩国跳板机 1','143.248.x.x','20xx年10月19日2时46分',390,510,'高等科学技术研究学院'),('kr-two','韩国跳板机 2','210.115.x.x','20xx年10月11日10时35分',740,510,'首尔国立江原大学（原图文字）'),('kr-three','韩国跳板机 3','222.122.x.x','20xx年6月6日1时27分',390,920,'')]
for id,name,ip,time,x,y,org in relays:
 node(id,name,'relay',x,y,parent='zone-relays',subtitle=ip,fig='internal',attrs={'地址（脱敏）':ip,'原图时间标记':time,'软件标注':'NOPEN','机构标注':org or '原图未标注'})
 edge('razor-'+id,'razor',id,'获取权限 / 安装 NOPEN','intrusion',fig='internal')
# Platform contains capabilities, marker backdoors and exfiltration infrastructure.
zone('zone-fox','“酸狐狸”中间人劫持平台',2320,1140,1400,1550,'foxacid-office')
node('foxacid','酸狐狸 Foxacid','hostedPlatform',545,440,category='cloud',parent='zone-fox',w=280,h=160,subtitle='哥伦比亚 190.242.xx.xx',fig='foxacid-office',attrs={'报道用途':'浏览器级 0day 平台','兼容平台（报道）':'IE / Firefox / Safari / Android Webkit'})
for id in ['leased','domain','cert']:edge('build-'+id,id,'foxacid','搭建平台','build',fig='preparation')
methods=[('mots','MotS 链路劫持',70,110),('mim','MiM 中间人攻击',420,110),('mail-method','Email 邮件钓鱼',770,110),('xss','XSS 跨站脚本攻击',1100,110)]
for k,(id,name,x,y) in enumerate(methods,1):
 node(id,name,'deliveryMethod',x,y,category='auxiliary',parent='zone-fox',logical='annotation',fig='foxacid-office',attrs={'性质':'原图平台能力展示，不等于本案逐项观测'})
 edge('capability-'+id,'foxacid',id,'载荷递送 '+str(k),'capability',fig='foxacid-office')
for id,name,y in [('validator','“验证器” Validator',420),('misty','MistyVeal',650)]:
 node(id,name,'softwareTool',1120,y,parent='zone-fox',logical='software',fig='foxacid-office',subtitle='标配后门' if id=='validator' else 'Validator 增强版（原图）')
 edge('fox-'+id,'foxacid',id,'标配后门','capability',fig='foxacid-office')
callbacks=[('egypt','埃及跳板机','80.77.xx.xx',50),('denmark','丹麦跳板机','82.103.xx.xx',390),('netherlands','荷兰跳板机','83.98.xx.xx',730),('czech','捷克跳板机','81.31.xx.xx',1070)]
for id,name,ip,x in callbacks:node(id,name,'relay',x,1100,parent='zone-fox',subtitle=ip,fig='foxacid-office',attrs={'用途（原图）':'木马信息回传平台'})
node('return-bus','回传汇合','junction',655,1350,category='auxiliary',parent='zone-fox',w=70,h=60,logical='annotation',fig='foxacid-office',basis='layout',notes='原图公共连线的汇合点；不是新设备。')
node('cdr','CDR 加密传输','dataAsset',535,830,parent='zone-fox',w=260,h=100,logical='artifact',fig='foxacid-office',notes='将原图公共回传线文字转为可选择逻辑对象；保留 CDR 原称。',basis='layout')
for id,_,_,_ in callbacks:
 edge('return-'+id,'return-bus',id,'数据回传','exfiltration',fig='foxacid-office',sp='top',tp='bottom')
 edge(id+'-cdr',id,'cdr','汇总','exfiltration',fig='foxacid-office')
edge('cdr-fox','cdr','foxacid','信息回传 / 加密传输','exfiltration',fig='foxacid-office')
node('foxsearch','Foxsearch 情报检索','softwareTool',45,720,parent='zone-fox',logical='software',fig='foxacid-office',notes='原图回传线旁的检索工具文字展开为逻辑对象；不推定独立部署主机。',basis='layout')
edge('fox-foxsearch','foxacid','foxsearch','汇总信息检索','collection',fig='foxacid-office',basis='analysis')
# Campus: preserve original parallel devices and actual depicted internal branches.
zone('zone-campus','西北工业大学网络',1280,2960,2440,1700,'tools')
for id,name,kind,x in [('gateway','网关服务器','gateway',60),('border-router','边界路由器','router',450),('border-other','其他边界设备','gateway',840)]:
 node(id,name,kind,x,100,parent='zone-campus',subtitle='西北工业大学',fig='boundary',attrs={'软件（报道）':'NOPEN；二次约会'})
 edge('island-'+id,'island',id,'入侵边界 / 安装 NOPEN','intrusion',fig='boundary',note='依据原图文字；不提供漏洞参数。')
 tool='second-'+id
 node(tool,'“二次约会”','softwareTool',x,360,parent='zone-campus',logical='software',fig='boundary',subtitle='中间人劫持工具实例',attrs={'工具族':'二次约会','承载设备':name})
 edge('deploy-'+tool,id,tool,'安装','deployment',fig='boundary')
edge('hijack-one','second-gateway','second-border-router','劫持流量','hijack',fig='boundary')
edge('hijack-two','second-border-router','second-border-other','劫持流量','hijack',fig='boundary')
node('endpoints','多台上网终端','pc',1260,590,parent='zone-campus',fig='paths',notes='原图集合节点，不扩展为未知主机。')
node('multi-servers','多台服务器','server',840,680,parent='zone-campus',fig='tools')
node('inside-router','内部路由器','router',50,680,parent='zone-campus',fig='tools')
node('inside-switch','内部交换机','switch',430,680,parent='zone-campus',fig='tools')
node('inside-server','内网服务器','server',60,980,parent='zone-campus',fig='internal')
node('telnet','telnet 运维管理服务器','opsServer',420,980,parent='zone-campus',w=250,fig='internal')
node('ops-monitor','运维网络监控管理服务器','opsServer',840,980,parent='zone-campus',w=270,fig='internal')
for j,(id,*_) in enumerate(relays):
 dst='inside-server' if id=='kr-three' else 'telnet'
 edge('relay-'+id,id,dst,'指令中转 / 渗透','control',fig='internal',sp='bottom',tp='left',points=[(150+j*80,3500+j*35),(1160,3500+j*35)],label=(600+j*70,3500+j*35))
edge('telnet-ops','telnet','ops-monitor','运维网进一步控制','lateral',fig='internal')
internal=[('network-monitor','内网监控管理服务器','opsServer',60),('auth','认证服务器','authServer',330),('backup','内网备份服务器','backupServer',600),('server-one','服务器1','server',870),('server-two','服务器2','server',1140)]
for id,name,kind,x in internal:
 node(id,name,kind,x,1390,parent='zone-campus',w=220,fig='tools')
 edge('lateral-'+id,'telnet' if id=='network-monitor' else 'ops-monitor',id,'横向','lateral',fig='tools')
node('mailserver','邮件服务器','mailServer',1540,600,parent='zone-campus',fig='paths')
zone('zone-office','西工大办公内网',1460,950,920,650,'paths',parent='zone-campus')
for j in range(6):node('user-'+str(j+1),'用户'+str(j+1),'userTerminal',40+(j%3)*295,100+(j//3)*270,parent='zone-office',subtitle='办公内网',fig='paths',notes='复刻原图用户终端组合符号，不推断真实身份。')
for src,dst in [('user-2','user-1'),('user-2','user-3'),('user-2','user-5'),('user-5','user-4'),('user-5','user-6')]:edge(src+'-'+dst,src,dst,'办公网传播（原图箭头）','lateral',fig='paths')
# Red A route and cyan B route retain named stages and distinct returns.
edge('a-visit','endpoints','second-border-other','访问 / 通信流经','internet',fig='paths',color=RED,style='dashed')
edge('a1','second-border-other','foxacid','A1 访问“酸狐狸”／劫持至恶意域名','redirection',fig='paths',color=RED,sp='right',tp='left',points=[(2450,3375),(2450,1730)],label=(2450,2800),pathGroup='A')
edge('a2','foxacid','endpoints','A2 识别浏览器／投递攻击载荷','payload',fig='paths',color=RED,sp='left',tp='top',points=[(2510,1690),(2510,3410)],label=(2510,3060),pathGroup='A')
edge('a3','endpoints','return-bus','A3 数据回传','exfiltration',fig='paths',color=RED,sp='top',tp='left',points=[(2600,3470),(2600,2520)],label=(2600,3210),pathGroup='A')
edge('b1','user-2','foxacid','B1 访问恶意域名','redirection',fig='paths',color=CYAN,sp='right',tp='right',points=[(3840,4030),(3840,1700)],label=(3840,3060),pathGroup='B')
edge('b2','foxacid','user-2','B2 下发“怒火喷射”木马','payload',fig='paths',color=CYAN,sp='right',tp='right',points=[(3920,1740),(3920,4140)],label=(3920,3300),pathGroup='B')
edge('b3','user-2','return-bus','B3 数据回传','exfiltration',fig='paths',color=CYAN,sp='top',tp='right',points=[(3770,3910),(3770,2550)],label=(3770,2900),pathGroup='B')
node('phishing-mail','科研评审／答辩邀请／出国通知','mailPayload',2980,2780,w=290,h=115,logical='artifact',fig='paths',attrs={'时间（报道）':'20xx年4月','性质':'邮件主题与投递过程'},notes='正文描述邮件数据窃取风险及主机受攻击痕迹；不补造具体收件人。')
edge('phish-origin','foxacid','phishing-mail','邮件钓鱼路径（原图）','payload',fig='paths',color=GREEN,style='dashed',sp='bottom',tp='top',points=[(2910,1940),(2910,2710)],pathGroup='mail',note='原图将邮件路径与 Foxacid 联系；该关联保留为原图叙述，不额外证明投递基础设施归属。')
edge('mail-server-deliver','phishing-mail','mailserver','送达邮件服务器','delivery',fig='paths',color=GREEN,style='dashed',pathGroup='mail')
edge('mail-user-deliver','phishing-mail','user-2','邮件投递 / 送达','payload',fig='paths',color=GREEN,style='dashed',sp='bottom',tp='top',points=[(3200,3200),(3200,3900)],pathGroup='mail')
# Post-compromise tools: descriptions and tool-family relationships, not runnable instructions.
zone('zone-tools','驻留、隐藏与资料获取工具',1260,4810,2460,800,'tools',original=False)
tools=[('nopen','NOPEN','跨平台远控木马',80,110),('surgeon','“精准外科医生”','文件与进程隐藏',470,110),('sniffer','“饮茶” suctionchar','嗅探与日志收集（原图拼写）',920,110),('toast','“吐司面包”','入侵痕迹清理',1440,110),('heretic','“狡诈异端犯”','自启动后门（正文：可能安装）',1900,110),('rage','“怒火喷射”','Windows；抗分析／反调试（报道能力）',1900,410)]
for id,name,sub,x,y in tools:node(id,name,'softwareTool',x,y,parent='zone-tools',w=260,subtitle=sub,logical='software',fig='tools',basis='analysis' if id=='heretic' else 'reported')
node('data','资料与认证材料','dataAsset',850,490,parent='zone-tools',w=550,h=200,logical='artifact',fig='overview',notes='将原图底部资料清单合并为一个逻辑集合。',attrs={'原图资料清单':'边界设备账号口令；运维人员账号口令；路由器配置；用户密钥；原图第5项文字待核对；网络设备日志；FTP 服务器资料'},basis='layout')
for id in ['network-monitor','backup','server-two']:edge('install-sniffer-'+id,id,'sniffer','安装嗅探工具','deployment',fig='tools',style='dotted')
edge('surgeon-nopen','surgeon','nopen','隐藏文件与进程','concealment',fig='tools',basis='analysis',note='正文明确隐藏关系；具体实现接口未给出。')
edge('sniffer-data','sniffer','data','获取资料','collection',fig='tools')
edge('toast-data','toast','data','清理日志痕迹','cleanup',fig='tools',basis='analysis',note='指向逻辑资料集合中的日志部分，不表示删除全部认证材料。')
edge('heretic-nopen','heretic','nopen','为再次上传 NOPEN 提供驻留条件','persistence',fig='tools',basis='analysis',note='正文为“可能会安装”，不作确定部署结论。')
edge('b2-tool-note','user-2','rage','B2 载荷名称对应','capability',fig='paths',style='dotted',basis='layout',note='工具说明关联，不是新增感染路径。')
lookup['surgeon']['attributes']={'系统标注':'Linux、Solaris、JunOS、FreeBSD 等','原图说明':'通过替换 3 个原系统文件隐藏 NOPEN 文件和进程'}
lookup['toast']['attributes']={'原图日志文件':'utmp、wtmp、lastlog','原图用途':'入侵痕迹清理'}
lookup['heretic']['attributes']={'报道能力':'自删除、权限提升、随操作系统启动','部署确定性':'正文使用“可能会安装”，不可视为确定部署'}
lookup['nopen']['attributes']={'报道能力':'跨平台远控；文件、进程及系统操作；加密隧道','表现方式':'工具族说明，不是额外物理主机'}
lookup['sniffer']['attributes']={'原图工具名':'饮茶 / suctionchar','报道采集对象':'认证材料、Linux 日志、命令操作记录等'}
# Matrix mappings are explicit analytical assessments of the supplied report, not source assertions.
def bind(target,ref,note,fig='overview',kind='edge'):
 assert ref in index['objects'],ref
 assert not any(b['target']==dict(kind=kind,id=target) and b['matrixRef']==ref for b in scene['bindings']), (target,ref)
 scene['bindings'].append(dict(id='binding-'+str(len(scene['bindings'])+1),target=dict(kind=kind,id=target),matrixRef=ref,applicationNote=note,basis='inference',evidenceRefs=['nwpu-report','fig-'+fig]))
bind('identity-domain','NJT-0051','报道描述假名购买域名及基础设施匿名化。映射父级获取隐蔽型基础设施；不据此推断信誉老化、共享租户或预置资源切换。','preparation')
bind('cover-one-terremark','NJT-0051','掩护公司租赁资源的目的在报道中为隐藏关联，属于取得阶段的分析映射。','preparation')
bind('razor-jp-one','NJT-0044','报道描述攻陷第三方服务器用作后续跳板；该边代表被展开的一个来源，不把国家或 IP 数量当作子技术。','internal')
bind('relay-jp-one','NJS-0206-001','实际转发行为：报道明确被攻陷的第三方跳板转发控制指令，使目标看到第三方网络归属。细化到被攻陷网络出口归属借用，不另重复记录父级 NJT-0206。','internal')
bind('a1','NJT-0052','正文描述在线流量劫持与响应注入，映射内容注入；具体注入实现及持久 C2 结论仍需独立证据。','paths')
bind('surgeon-nopen','NJS-0111-001','隐藏作用：报道描述 NOPEN 文件和进程继续可用但在常用观察中被隐藏，分析映射默认视图枚举遗漏；不推定具体 API 或内核拦截实现。','tools')
bind('sniffer-data','NJT-0176','正文描述对既有 ssh、telnet、rlogin 等通信相关认证材料的嗅探；映射父级，不假定加密流被如何解密。','tools')
bind('toast-data','NJS-0112-001','清理作用：报道描述清理日志、消除入侵痕迹，原图列出 utmp、wtmp、lastlog。映射相关证据记录的擦除，不表示删除整个资料集合，也不推定时间戳伪造。','tools')
bind('heretic-nopen','NJT-0084','按工具描述映射启动生命周期恢复执行；正文仅称可能安装，保留分析推断状态。','tools')
# Expand only the explicit, user-approved mappings; topology is unchanged.
for relay_id,relay_name,*_ in relays:
 if relay_id != 'jp-one':
  bind('razor-'+relay_id,'NJT-0044',f'资源取得行为：原图将{relay_name}列在被攻陷跳板集合，并标注 NOPEN 安装。映射第三方基础设施攻陷；不推定其出口轮换或原业务是否持续。','internal')
  bind('relay-'+relay_id,'NJS-0206-001',f'实际中转行为：原图从{relay_name}连接校内目标，正文说明跳板转发指令并掩盖真实来源。按被攻陷网络出口归属借用解释，不推定多跳日志分舱。','internal')
 bind(relay_id,'NJS-0206-001',f'节点角色：{relay_name}是报道中被攻陷并承担控制中转的第三方出口载体。此处是对应中转连线的节点视角，不是额外一次攻击，也不表示该节点主动攻陷自身。','internal',kind='node')
for device in ['gateway','border-router','border-other']:
 bind('island-'+device,'NJT-0054','入口阶段：报道描述利用 Solaris / 边界服务漏洞直接获得首个立足点，并指出边界后方防护难以覆盖该入口。映射父技术；不据此断言该设备必然没有 EDR 或长期日志，也不推定具体利用子技术。','boundary')
 bind('island-'+device,'NJT-0130','与入口相邻的到达阶段：这条复合连线还标注取得控制后的 NOPEN 安装；仅将后续工具到达已受控设备的部分映射到本技术，不把初次漏洞输入算作入侵后的文件传输。','boundary')
 bind('deploy-second-'+device,'NJT-0130','工具到达阶段：图示在已经受控的边界设备安装“二次约会”。映射工具到达，不把后继流量劫持与文件到达混为一个动作，也不推定传输协议。','boundary')
bind('phishing-mail','NJT-0057','载体角色：科研评审、答辩邀请和出国通知是报道中的业务主题诱饵，目的是诱导点击并获得邮箱或主机入口。节点表达投递内容的用途，不宣称具体收件人身份，也不推定线程寄生、云协作等子技术。','paths',kind='node')
bind('mail-user-deliver','NJT-0057','投递行为：正文称定向主题邮件引诱师生点击并取得邮箱登录权限；原图用户2是办公用户的示意节点，不代表唯一被攻击者。映射钓鱼入口父级。','paths')
bind('foxacid','NJS-0053-002','平台能力：报道与 A2 标注说明识别浏览器版本并智能适配攻击载荷，分析映射漏洞适配客户端选择性交付。此节点描述报道中的能力，不宣称平台每一次访问均执行了该能力。','paths',kind='node')
bind('a2','NJS-0053-002','入口交付动作：A2 明确标注识别浏览器版本和适配投递，分析映射选择性交付。保留报道层面的依据，不补造对非目标客户端的实际响应样本。','paths')
bind('a2','NJT-0069','执行阶段：结合正文中正常浏览被引向浏览器级漏洞并获得主机权限的描述，将本连线的漏洞执行结果映射到情境门控客户端利用执行；与同线的入口交付是不同动作。证据不足以确认兼容性门控子项的全部差分条件，故保留父级。','paths')
bind('b2','NJT-0069','执行阶段：正文将办公网浏览器漏洞利用、取得个人主机权限与随后安装“怒火喷射”联系起来。本关联指向前置客户端漏洞执行，不把普通木马下载本身当作漏洞执行证据。','paths')
bind('surgeon','NJS-0111-001','工具能力：报道说明“精准外科医生”通过替换系统文件隐藏仍在使用的 NOPEN 文件和进程，分析映射默认视图枚举遗漏。此处是隐藏作用连线的工具能力视角，不增加独立执行次数。','tools',kind='node')
bind('toast','NJS-0112-001','工具能力：报道明确其清理入侵日志的用途，原图给出 utmp、wtmp、lastlog。映射消除相关证据记录的能力；并不表示在所有设备上都已执行，亦不额外推定时间元数据伪造。','tools',kind='node')
for host in ['network-monitor','backup','server-two']:
 bind('install-sniffer-'+host,'NJT-0130','部署动作：原图在已受控内网服务器上标注“安装”饮茶工具，分析映射工具到达。嗅探凭据是另外的后继行为，仍由工具到资料的关联说明。','tools')
scene['views']=[dict(id='organization',name='01 组织与职责',nodeIds=['zone-org']),dict(id='preparation',name='02 匿名资源准备',nodeIds=['zone-prep','register','us-ip-1','us-ip-4']),dict(id='relays',name='03 境外跳板网络',nodeIds=['zone-relays','razor']),dict(id='foxacid',name='04 Foxacid 平台',nodeIds=['zone-fox']),dict(id='boundary',name='05 校园边界',nodeIds=['gateway','border-router','border-other','second-gateway','second-border-router','second-border-other','island']),dict(id='operations',name='06 运维网横向',nodeIds=['telnet','ops-monitor','inside-server','network-monitor','auth','backup','server-one','server-two']),dict(id='office',name='07 办公网与邮件',nodeIds=['zone-office','phishing-mail','mailserver']),dict(id='tools',name='08 驻留与取证对象',nodeIds=['zone-tools'])]
# Node ledger makes additions originating from textual labels distinguishable from the original icon topology.
output=ROOT/'scenes/cases/nwpu-nsa-report.niji-scene.json';output.write_text(json.dumps(scene,ensure_ascii=False,indent=2)+'\n')
manifest=dict(caseId=scene['id'],sourceTitle=scene['sources'][0]['title'],sourceDate='2023-04-22',counts=dict(nodes=len(scene['nodes']),edges=len(scene['edges']),bindings=len(scene['bindings'])),items=inventory,reviewNotes=scene['reviewNotes'])
(ROOT/'scenes/sources/nwpu/topology-inventory.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
catalogPath=ROOT/'scenes/catalog.json';catalog=json.loads(catalogPath.read_text());catalog=[item for item in catalog if item['id']!='nwpu-nsa-report'];catalog.insert(0,dict(id='nwpu-nsa-report',name='NSA 入侵西北工业大学',category='case',file='cases/nwpu-nsa-report.niji-scene.json',description='希潭实验室报道复刻 · 可追溯拓扑'))
catalogPath.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n');print(manifest['counts'])
