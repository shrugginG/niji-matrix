"""Apply candidate-specific reader-prose refinements found by the full audit."""

from pathlib import Path
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
BASE = ROOT / "matrix/tactics"

def update(path, fn):
    data = yaml.safe_load(path.read_text())
    fn(data)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120))

child_path = BASE / "TA0001-initial-access/techniques/NJT-0052-content-injection/subtechniques/NJS-0052-002-racing-forged-response-injection/subtechnique.yaml"
def racing(child):
    child["definition_and_concept"]["paragraphs"][1] = {
        "zh": "Fox-IT 对 QUANTUM INSERT 的技术复现证明旁路选择器、有效序列状态及先到伪造响应如何改变客户端接收内容，并提出相同 TCP 序号异载荷的证据。公开来源足以支持首次入口中的匿迹变量；已植入主机持续通过竞速回复取得任务的事件仍缺直接证据，不能由父级的双战术范围自动推出。",
        "en": "Fox-IT's technical reproduction of QUANTUM INSERT shows how off-path selectors, valid TCP sequence state, and an earlier forged response alter client receipt and identifies duplicate sequence numbers with different payloads as evidence. Public sources support the evasion variable during first entry. A continuing task loop through racing replies on an implanted host still lacks direct incident evidence and cannot be inferred from the parent's dual-tactic scope.",
    }
    child["scope_boundary_definition"]["paragraphs"][1] = {
        "zh": "已记录的首次入口情形可正式归类；持续控制只有在已受控端经竞速回复取得任务并产生结果时才纳入，目前作为研究假设。合法重传、CDN 多路径、缓存不一致和网络故障可能生成相近包序列，需凭攻击者响应内容和源站对照排除。",
        "en": "Documented first-entry cases qualify. Continuing control requires an already compromised endpoint obtaining tasking through a racing reply and producing a result; that remains a research hypothesis. Legitimate retransmission, CDN paths, cache inconsistency, and faults can create similar packet sequences and require exclusion through actor response content and origin comparison.",
    }
    child["research"]["limitations"]["paragraphs"][0] = {
        "zh": "Fox-IT 给出可复现技术链与检测残迹，但没有持续命令交换的直接事件记录。当前子项对首次入口行为的置信度高；对持续控制用途仅保留假设，不能用父级一般陈述替代子项级证据。",
        "en": "Fox-IT provides a reproducible technical chain and residual signal but no direct incident of continuing command exchange. Confidence is high for first-entry behavior; continuing-control use remains a hypothesis and cannot be inferred from the parent's general description.",
    }
update(child_path, racing)

parent1 = BASE / "TA0011-command-and-control/techniques/NJT-0221-port-expectation-semantic-mismatch/technique.yaml"
def port(parent):
    p = parent["subtechnique_taxonomy"]["narrative"]["paragraphs"][1]
    p["zh"] = p["zh"].replace("故正式数量为零", "因此没有独立子技术")
    p["en"] = p["en"].replace("so the formal child count is zero", "so no independent child is established")
update(parent1, port)

parent3 = BASE / "TA0011-command-and-control/techniques/NJT-0223-adversary-keyed-c2-protection/technique.yaml"
def encryption(parent):
    parent["subtechnique_taxonomy"]["narrative"]["paragraphs"][0]["zh"] = parent["subtechnique_taxonomy"]["narrative"]["paragraphs"][0]["zh"].replace("三项候选", "三项子技术")
    parent["subtechnique_taxonomy"]["narrative"]["paragraphs"][0]["en"] = parent["subtechnique_taxonomy"]["narrative"]["paragraphs"][0]["en"].replace("Three candidates", "Three children")
    parent["subtechnique_taxonomy"]["narrative"]["paragraphs"][1] = {
        "zh": "对称或非对称算法、密钥长度、TLS、密码库和产品名称都不改变本分类的密钥恢复范围或检查边界，因而不单独成项。只有密文外观而无法恢复密钥材料路径、接收端解密和后继命令结果时，应停留在不透明通道候选层级。",
        "en": "Symmetric or asymmetric algorithms, key length, TLS, cryptographic libraries, and product names do not change the key-recovery scope or inspection boundary and therefore do not form children. Ciphertext appearance without a recoverable key-material path, receiver decryption, and successor command outcome remains an opaque-channel candidate.",
    }
update(parent3, encryption)

parent4 = BASE / "TA0011-command-and-control/techniques/NJT-0224-selective-c2-infrastructure-exposure/technique.yaml"
def infrastructure(parent):
    p = parent["scope_boundary_definition"]["paragraphs"][3]
    p["zh"] = p["zh"].replace("DET-000032/NJA-000006 识别 Web host profiling 与选择性内容，主体是被画像 visitor/page；本技术检测基础设施是否对不同 vantages 隐藏 C2，并要求 victim C2 outcome，因此不能直接复用。", "Web 主机画像与选择性内容的直接对象是被画像的访问者或页面；这里的直接对象是基础设施是否对不同观察者隐藏真实 C2，并要求受害端控制结果。")
    p["en"] = p["en"].replace("DET-000032 and NJA-000006 identify Web host profiling and selective content with the visitor or page as subject. This technique detects infrastructure hiding C2 across vantages and requires a victim C2 outcome, so those objects cannot be directly reused.", "Web host profiling and selective content concern the profiled visitor or page. The direct object here is infrastructure hiding real C2 from different observers, with a victim control outcome required.")
update(parent4, infrastructure)

print("Refined four parent or child prose packages for reader audit")
