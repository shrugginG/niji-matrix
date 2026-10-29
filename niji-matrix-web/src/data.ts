import { publicAssetUrl } from "./paths";
export type Value =
  string | number | boolean | null | Value[] | { [key: string]: Value };
export interface RecordData {
  id: string;
  type: string;
  name?: { zh?: string; en?: string };
  name_zh?: string;
  name_en?: string;
  title_zh?: string;
  title_en?: string;
  url?: string | null;
  archive_url?: string | null;
  source?: { url?: string; [key: string]: unknown };
  summary?: { zh?: string; en?: string };
  classification?: { tactic_refs?: string[] };
  parent_ref?: string;
  mechanism_refs?: string[];
  children?: string[];
  lifecycle?: { status?: string; version?: string };
  [key: string]: unknown;
}
export interface IndexData {
  revision: string;
  generated_at: string;
  matrix: RecordData & { tactic_refs: string[] };
  objects: Record<string, RecordData>;
}
export const labels: Record<string, string> = {
  matrix: "矩阵",
  tactic: "战术",
  technique: "匿迹技术",
  "evasion-subtechnique": "匿迹子技术",
  mechanism: "匿迹机理",
  "detection-strategy": "检测策略",
  "detection-analytic": "检测分析",
  mitigation: "缓解措施",
  reference: "参考资料",
  claim: "研究主张",
  case: "案例",
  relationship: "对象关系",
  "technique-decision": "准入决策",
  definition_and_concept: "定义与概念",
  stealth_characteristics: "匿迹特性",
  scope_boundary_definition: "范围边界",
  application_scenarios_and_threat_model: "应用场景与威胁模型",
  application_scenarios: "应用场景",
  threat_model: "威胁模型",
  attacker_model: "攻击者模型",
  defender_model: "防守方模型",
  stealth_mechanisms: "匿迹机理",
  subtechnique_taxonomy: "子技术分类",
  defense: "检测与缓解",
  evidence: "证据与参考",
  research: "研究限制与治理",
  lifecycle: "生命周期",
  classification: "分类与来源",
  origin: "来源",
  kind: "类型",
  tactic_refs: "所属战术",
  source_attack_version: "ATT&CK 版本",
  source_attack_technique_ref: "ATT&CK 技术",
  decision_ref: "准入决策",
  narrative: "分类说明",
  coverage: "覆盖程度",
  subtechnique_refs: "匿迹子技术",
  mechanism_ref: "机理",
  role: "角色",
  analysis: "分析",
  evidence_refs: "证据来源",
  confidence: "置信度",
  summary: "摘要",
  description: "说明",
  definition: "定义",
  core_question: "核心问题",
  defender_effect: "对防守方的影响",
  detections: "检测策略",
  strategy_refs: "检测策略",
  mitigations: "缓解措施",
  mitigation_refs: "缓解措施",
  claim_refs: "研究主张",
  case_refs: "案例",
  reference_refs: "参考资料",
  limitations: "研究限制",
  review_notes: "审阅说明",
  status: "状态",
  version: "版本",
  created: "创建日期",
  modified: "修改日期",
  name: "名称",
  logic: "检测逻辑",
  data_requirements: "数据要求",
  observables: "可观测信号",
  correlation: "关联分析",
  false_positives: "误报",
  blind_spots: "盲区",
  tuning_guidance: "调优建议",
  analytic_refs: "检测分析",
  detects_refs: "检测对象",
  strategy_ref: "所属策略",
  domains: "领域",
  platforms: "平台",
  measures: "措施",
  applications: "逐目标应用",
  target_ref: "应用对象",
  subject_refs: "关联对象",
  statement: "研究主张",
  claim_type: "主张类型",
  evidence_mode: "证据模式",
  source_type: "来源类型",
  authors: "作者",
  publisher: "发布机构",
  published: "发布日期",
  accessed: "访问日期",
  url: "原文链接",
  archive_url: "存档链接",
  locator: "定位信息",
  credibility: "可信度",
  notes: "说明",
  parent_ref: "父技术",
  lineage: "继承关系",
  aliases: "别名",
  actor_or_campaign: "活动主体",
  time_range: "时间范围",
  target_sectors: "目标行业",
  shortname: "缩写",
  title: "标题",
};
export const statuses: Record<string, string> = {
  draft: "草稿",
  review: "审阅中",
  published: "已发布",
  deprecated: "已弃用",
  high: "高",
  medium: "中",
  low: "低",
  primary: "主要",
  secondary: "次要",
  established: "已建立",
};
export function title(o: RecordData, lang = "zh"): string {
  return (
    o.name?.[lang as "zh" | "en"] ||
    String(
      o[lang === "zh" ? "name_zh" : "name_en"] ||
        o[lang === "zh" ? "title_zh" : "title_en"] ||
        o.name?.zh ||
        o.name_zh ||
        o.title_zh ||
        o.id,
    )
  );
}
export async function json<T>(url: string): Promise<T> {
  const r = await fetch(publicAssetUrl(url), { cache: import.meta.env.DEV ? "no-store" : "no-cache" });
  if (!r.ok) throw new Error(`加载失败（${r.status}）：${url}`);
  return r.json();
}
