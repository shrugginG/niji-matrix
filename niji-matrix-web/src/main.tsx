import React, { useEffect, useRef, useState, lazy, Suspense } from "react";
import { createRoot } from "react-dom/client";
import {
  BrowserRouter,
  HashRouter,
  Link,
  NavLink,
  useLocation,
  useNavigate,
  useParams,
  useSearchParams,
} from "react-router-dom";
import {
  Search,
  ArrowUpRight,
  ArrowLeft,
  ChevronRight,
  ChevronDown,
  Layers,
  Grid2X2,
  List,
  SlidersHorizontal,
  BookOpen,
  RefreshCw,
} from "lucide-react";
import {
  json,
  title,
  labels,
  statuses,
  type RecordData,
  type IndexData,
  type Value,
} from "./data";
import "./styles.css";
import SectionLink from "./components/SectionLink";
import SimulationErrorBoundary from "./components/SimulationErrorBoundary";
import { MechanismIcon } from "./components/MechanismIcon";
import { TacticIcon } from "./components/TacticIcon";
import { RecordSourceLinks, SourceLink, sourceUrl } from "./components/SourceLinks";
const Simulation = lazy(() => import("./features/simulation/Simulation"));
const Context = React.createContext<{ data: IndexData; lang: string }>({
  data: null!,
  lang: "zh",
});
const useData = () => React.useContext(Context);
function ObjectLink({ id }: { id: string }) {
  const { data, lang } = useData();
  const o = data.objects[id];
  return o ? (
    <span className="object-link-group">
    <Link className="object-link" to={`/objects/${encodeURIComponent(id)}`}>
      <span className="object-link-name">{o.type === "mechanism" && <MechanismIcon id={id} size={16} />}{o.type === "tactic" && <TacticIcon id={id} size={16} />}{title(o, lang)}</span>
      <code>{id}</code>
      <ArrowUpRight size={13} />
    </Link>
    <RecordSourceLinks record={o} lang={lang} />
    </span>
  ) : (
    <span>{id}</span>
  );
}
function Content({
  value,
  depth = 0,
}: {
  value: Value | unknown;
  depth?: number;
}) {
  const { data, lang } = useData();
  if (value == null) return null;
  if (typeof value === "string") {
    if (data.objects[value]) return <ObjectLink id={value} />;
    if (sourceUrl(value)) return <SourceLink href={value} showLabel />;
    return <span>{statuses[value] || value}</span>;
  }
  if (typeof value !== "object") return <span>{String(value)}</span>;
  if (Array.isArray(value))
    return (
      <div className="content-array">
        {value.map((v, i) => (
          <div className={typeof v === "object" ? "content-item" : ""} key={i}>
            <Content value={v} depth={depth + 1} />
          </div>
        ))}
      </div>
    );
  const obj = value as Record<string, Value>;
  if ("zh" in obj || "en" in obj)
    return <Content value={obj[lang] ?? obj.zh ?? obj.en} depth={depth} />;
  if ("paragraphs" in obj)
    return (
      <>
        {(obj.paragraphs as Value[]).map((p, i) => (
          <p key={i}>
            <Content value={p} depth={depth + 1} />
          </p>
        ))}
      </>
    );
  return (
    <div className="structured">
      {Object.entries(obj)
        .filter(
          ([k]) =>
            !k.startsWith("_") && !k.endsWith(lang === "zh" ? "_en" : "_zh"),
        )
        .map(([k, v]) => (
          <div className="field" key={k}>
            <div className="field-label">
              {labels[k.replace(/_(zh|en)$/, "")] || k.replaceAll("_", " ")}
            </div>
            <div>
              <Content value={v} depth={depth + 1} />
            </div>
          </div>
        ))}
    </div>
  );
}
interface MechanismAnalysis {
  mechanism_ref: string;
  role: string;
  summary?: unknown;
  analysis?: unknown;
  evidence_refs?: string[];
  confidence?: string;
  [key: string]: unknown;
}
function MechanismCards({ value }: { value: unknown }) {
  const { data, lang } = useData();
  if (!Array.isArray(value)) return <Content value={value} />;
  const mechanisms = value as MechanismAnalysis[];
  const primaryCount = mechanisms.filter(m => m.role === "primary").length;
  const secondaryCount = mechanisms.filter(m => m.role === "secondary").length;
  return (
    <div className="mechanism-section">
      <div className="mechanism-overview" aria-label="匿迹机理概况">
        <p className="mechanism-count">共 {mechanisms.length} 项机理 · 主要 {primaryCount} 项 · 次要 {secondaryCount} 项</p>
        <div className="mechanism-jumps">
          {mechanisms.map(m => (
            <SectionLink key={m.mechanism_ref} id={`mechanism-${m.mechanism_ref}`} className={`mechanism-jump ${m.role === "primary" ? "is-primary" : ""}`}>
              <MechanismIcon id={m.mechanism_ref} size={16} />
              {data.objects[m.mechanism_ref] ? title(data.objects[m.mechanism_ref], lang) : m.mechanism_ref}
              <span>{statuses[m.role] || m.role}</span>
            </SectionLink>
          ))}
        </div>
      </div>
      <div className="mechanism-cards">
        {mechanisms.map(m => {
          const name = data.objects[m.mechanism_ref] ? title(data.objects[m.mechanism_ref], lang) : m.mechanism_ref;
          const extra = Object.fromEntries(Object.entries(m).filter(([key]) => !["mechanism_ref", "role", "summary", "analysis", "evidence_refs", "confidence"].includes(key)));
          return (
            <section key={m.mechanism_ref} id={`mechanism-${m.mechanism_ref}`} aria-label={`${name}机理分析`} className={`mechanism-card ${m.role === "primary" ? "mechanism-primary" : "mechanism-secondary"}`}>
              <div className="mechanism-card-header">
                <div className="mechanism-title"><h3><Link to={`/objects/${m.mechanism_ref}`}><MechanismIcon id={m.mechanism_ref} size={21} />{name}<ArrowUpRight size={15} aria-hidden="true" /></Link></h3><code>{m.mechanism_ref}</code></div>
                <div className="mechanism-meta"><span className="mechanism-role">{statuses[m.role] || m.role}机理</span>{m.confidence && <span className="mechanism-confidence">置信度：<strong>{statuses[m.confidence] || m.confidence}</strong></span>}</div>
              </div>
              <div className="mechanism-card-body">
                {m.summary != null && <div className="mechanism-summary"><h4>机理摘要</h4><p><Content value={m.summary} /></p></div>}
                {m.analysis != null && <div className="mechanism-analysis"><h4>机理分析</h4><Content value={m.analysis} /></div>}
                {Object.keys(extra).length > 0 && <Content value={extra} />}
                <details className="mechanism-evidence">
                  <summary>证据来源 <span>{m.evidence_refs?.length || 0}</span></summary>
                  {m.evidence_refs?.length ? <div className="mechanism-references">{m.evidence_refs.map(id => <ObjectLink id={id} key={id} />)}</div> : <p className="muted">未提供证据来源</p>}
                </details>
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}

function SubtechniqueTaxonomy({ value }: { value: unknown }) {
  const { data, lang } = useData();
  if (!value || typeof value !== "object" || Array.isArray(value)) return <Content value={value} />;
  const fields = value as Record<string, unknown>;
  const refs = Array.isArray(fields.subtechnique_refs) ? fields.subtechnique_refs as string[] : [];
  const coverage = String(fields.coverage || "");
  const coverageLabels: Record<string, string> = {
    established: "分类已建立",
    "none-justified": "暂无合理细分",
    deferred: "分类暂缓",
  };
  const extras = Object.fromEntries(Object.entries(fields).filter(([key]) => !["narrative", "coverage", "subtechnique_refs"].includes(key)));
  return (
    <div className="taxonomy">
      <section className="taxonomy-explanation" aria-label="分类说明">
        <div className="taxonomy-heading"><h3>分类说明</h3>{coverage && <span className="taxonomy-status">{coverageLabels[coverage] || coverage}</span>}</div>
        <Content value={fields.narrative} />
      </section>
      <section className="taxonomy-list" aria-label="子技术一览">
        <div className="taxonomy-heading"><h3>子技术一览</h3><span className="taxonomy-count">{refs.length} 项子技术</span></div>
        {refs.length ? <div className="taxonomy-rows">{refs.map(id => {
          const child = data.objects[id];
          if (!child) return <div className="taxonomy-empty" key={id}>未能解析子技术：{id}</div>;
          return <article className="taxonomy-row" key={id}>
            <div className="taxonomy-identity"><h4><Link to={`/objects/${id}`}>{title(child, lang)}<ArrowUpRight size={14} aria-hidden="true" /></Link></h4><code>{id}</code></div>
            <div className="taxonomy-content">
              {child.summary && <p>{child.summary[lang as "zh" | "en"] || child.summary.zh}</p>}
              {!!child.mechanism_refs?.length && <div className="taxonomy-mechanisms" aria-label="关联匿迹机理">{child.mechanism_refs.map(ref => <Link to={`/objects/${ref}`} key={ref}><MechanismIcon id={ref} size={15} />{data.objects[ref] ? title(data.objects[ref], lang) : ref}</Link>)}</div>}
            </div>
          </article>;
        })}</div> : <p className="taxonomy-empty">{coverage === "deferred" ? "当前尚未建立子技术分类，暂缓原因见上方分类说明。" : coverage === "none-justified" ? "当前未划分子技术，分类依据见上方说明。" : "当前未关联子技术。"}</p>}
      </section>
      {Object.keys(extras).length > 0 && <Content value={extras} />}
    </div>
  );
}

function objectFields(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : {};
}
function ExtraFields({ fields, known }: { fields: Record<string, unknown>; known: string[] }) {
  const extra = Object.fromEntries(Object.entries(fields).filter(([key]) => !known.includes(key)));
  return Object.keys(extra).length ? <Content value={extra} /> : null;
}
function RelatedRows({ ids, analytics = false, compact = false }: { ids: string[]; analytics?: boolean; compact?: boolean }) {
  const { data, lang } = useData();
  if (!ids.length) return <p className="section-empty">当前未关联对象</p>;
  return <div className={`related-rows ${compact ? "related-rows-compact" : ""}`}>{ids.map(id => {
    const record = data.objects[id];
    if (!record) return <div className="related-row" key={id}><span>未能解析引用：{id}</span></div>;
    const name = title(record, lang);
    const description = record.summary?.[lang as "zh" | "en"] || record.summary?.zh || record[`statement_${lang}`] || record[`description_${lang}`];
    const analyticIds = Array.isArray(record.analytic_refs) ? record.analytic_refs as string[] : [];
    return <div className="related-row" key={id}>
      <div className="related-row-heading"><Link to={`/objects/${id}`} className="related-row-name">{record.type === "mechanism" && <MechanismIcon id={id} size={16} />}{record.type === "tactic" && <TacticIcon id={id} size={16} />}{name === id ? labels[record.type] || id : name}<ArrowUpRight size={13} aria-hidden="true" /></Link><code>{id}</code><RecordSourceLinks record={record} lang={lang} /></div>
      {!compact && typeof description === "string" && <p>{description}</p>}
      {record.type === "reference" && Boolean(record.publisher || record.published) && <div className="reference-meta">{[record.publisher, record.published].filter(Boolean).map(String).join(" · ")}</div>}
      {analytics && analyticIds.length > 0 && <div className="analytic-shortcuts"><span>检测分析</span>{analyticIds.map(ref => <ObjectLink key={ref} id={ref} />)}</div>}
    </div>;
  })}</div>;
}
function DefenseSection({ value }: { value: unknown }) {
  const fields = objectFields(value);
  const groups = [
    { key: "detections", title: "检测策略", refs: "strategy_refs", icon: <ModelPersonIcon equipment="magnifier" /> },
    { key: "mitigations", title: "缓解措施", refs: "mitigation_refs", icon: <ModelPersonIcon equipment="wrench" /> },
  ];
  const coverageLabels: Record<string, string> = { available: "已关联", "not-applicable": "不适用", deferred: "暂缓" };
  return <><div className="defense-groups">{groups.filter(g => fields[g.key] != null).map(g => {
    const group = objectFields(fields[g.key]);
    const ids = Array.isArray(group[g.refs]) ? group[g.refs] as string[] : [];
    return <section className="defense-group" key={g.key} aria-label={g.title}>
      <div className="section-group-heading"><h3><span className="section-icon">{g.icon}</span>{g.title}</h3><span className="section-count">{ids.length} 项</span>{group.coverage != null && <span className="section-state">{coverageLabels[String(group.coverage)] || String(group.coverage)}</span>}</div>
      {group.rationale != null && <div className="coverage-rationale"><Content value={group.rationale} /></div>}
      <RelatedRows ids={ids} analytics={g.key === "detections"} />
      <ExtraFields fields={group} known={[g.refs, "coverage", "rationale"]} />
    </section>;
  })}</div><ExtraFields fields={fields} known={["detections", "mitigations"]} /></>;
}
function EvidenceSection({ value }: { value: unknown }) {
  const fields = objectFields(value);
  const groups = [{ key: "claim_refs", title: "研究主张" }, { key: "case_refs", title: "案例证据" }, { key: "reference_refs", title: "参考资料" }];
  return <div className="evidence-groups">{groups.map(g => {
    const ids = Array.isArray(fields[g.key]) ? fields[g.key] as string[] : [];
    return <section className="evidence-group" aria-label={g.title} key={g.key}><div className="section-group-heading"><h3>{g.title}</h3><span className="section-count">{ids.length} 项</span></div><RelatedRows ids={ids} /></section>;
  })}<ExtraFields fields={fields} known={groups.map(g => g.key)} /></div>;
}
function ResearchSection({ value }: { value: unknown }) {
  const fields = objectFields(value);
  return <div className="research-groups">{Object.entries(fields).map(([key, item]) => <section key={key} className="research-group" aria-label={labels[key] || key}><h3>{labels[key] || key}</h3><div className="research-prose"><Content value={item} /></div></section>)}</div>;
}
function MetadataItem({ label, children }: { label: string; children: React.ReactNode }) {
  return <div className="metadata-item"><dt>{label}</dt><dd>{children}</dd></div>;
}
function ClassificationSection({ value }: { value: unknown }) {
  const fields = objectFields(value), origin = objectFields(fields.origin);
  const kinds: Record<string, string> = { "attack-retained": "保留 ATT&CK 技术", "attack-adapted": "基于 ATT&CK 调整", "niji-added": "匿迹矩阵新增" };
  return <><dl className="metadata-grid classification-grid">
    {fields.tactic_refs != null && <MetadataItem label="所属战术"><Content value={fields.tactic_refs} /></MetadataItem>}
    {origin.kind != null && <MetadataItem label="来源类型">{kinds[String(origin.kind)] || String(origin.kind)}</MetadataItem>}
    {origin.source_attack_id != null && <MetadataItem label="ATT&CK 来源技术"><code>{String(origin.source_attack_id)}</code></MetadataItem>}
    {origin.source_attack_version != null && <MetadataItem label="ATT&CK 基线版本">{String(origin.source_attack_version)}</MetadataItem>}
    {fields.decision_ref != null && <MetadataItem label="准入决策"><Link className="object-link" to={`/objects/${String(fields.decision_ref)}`}><span>查看准入决策</span><code>{String(fields.decision_ref)}</code><ArrowUpRight size={13} aria-hidden="true" /></Link></MetadataItem>}
  </dl><ExtraFields fields={origin} known={["kind", "source_attack_id", "source_attack_version"]} /><ExtraFields fields={fields} known={["tactic_refs", "origin", "decision_ref"]} /></>;
}
function LifecycleSection({ value }: { value: unknown }) {
  const fields = objectFields(value);
  const names: Record<string, string> = { status: "当前状态", version: "内容版本", created: "创建日期", modified: "最近修改", contributors: "贡献者", reviewers: "审阅者" };
  return <><dl className="metadata-grid lifecycle-grid">{Object.entries(names).filter(([key]) => key in fields).map(([key, label]) => <MetadataItem key={key} label={label}>{key === "status" ? <span className="badge">{statuses[String(fields[key])] || String(fields[key])}</span> : Array.isArray(fields[key]) && !(fields[key] as unknown[]).length ? <span className="muted">未记录</span> : <Content value={fields[key]} />}</MetadataItem>)}</dl><ExtraFields fields={fields} known={Object.keys(names)} /></>;
}
function ReverseReferences({ ids }: { ids: string[] }) {
  const { data } = useData();
  const groups: Record<string, string[]> = {};
  ids.forEach(id => { const type = data.objects[id]?.type || "unknown"; (groups[type] ||= []).push(id); });
  const order = ["technique", "evasion-subtechnique", "detection-strategy", "detection-analytic", "mitigation", "claim", "case", "reference"];
  return <div className="reverse-groups">{Object.entries(groups).sort(([a], [b]) => (order.indexOf(a) < 0 ? 99 : order.indexOf(a)) - (order.indexOf(b) < 0 ? 99 : order.indexOf(b))).map(([type, refs]) => <details key={type} className="reverse-group" open={type === "technique" || type === "evasion-subtechnique"}><summary><span>{labels[type] || type}</span><span className="section-count">{refs.length} 项</span></summary><RelatedRows ids={refs} compact /></details>)}</div>;
}

function ModelPersonIcon({ equipment }: { equipment: "sword" | "shield" | "magnifier" | "wrench" }) {
  return (
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none"
      stroke="currentColor" strokeWidth="1.65" strokeLinecap="round"
      strokeLinejoin="round" aria-hidden="true" focusable="false">
      <circle cx="10" cy="6" r="3" />
      <path d="M4 20v-5a3 3 0 0 1 3-3h6a3 3 0 0 1 3 3M7 16v6h6v-6M8 22v7M12 22v7" />
      {equipment === "sword" ? (
        <>
          <path d="M16 15l4 2M18 21l4-4M19 14l6 6M21 16l5-11 3-2v4l-6 11" />
        </>
      ) : equipment === "shield" ? (
        <path d="M16 15l3 2M23 12l6 3v5c0 4-3 7-6 9-3-2-6-5-6-9v-5z" />
      ) : equipment === "magnifier" ? (
        <>
          <circle cx="24" cy="9" r="5" />
          <path d="m20.5 12.5-4 4M16 15l2 2" />
        </>
      ) : (
        <>
          <path d="M22 3a5 5 0 0 0-2 8l-4 11a2 2 0 0 0 4 1l4-11a5 5 0 0 0 5-7l-3 3-4-2zM16 15l3 2" />
        </>
      )}
    </svg>
  );
}

function ScenarioAndThreatModel({ value }: { value: unknown }) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return <Content value={value} />;
  }
  const fields = value as Record<string, unknown>;
  const threat = fields.threat_model;
  const models = threat && typeof threat === "object" && !Array.isArray(threat)
    ? threat as Record<string, unknown>
    : undefined;
  const extraFields = Object.fromEntries(Object.entries(fields).filter(([key]) =>
    !["application_scenarios", "threat_model"].includes(key)));
  const extraModels = models ? Object.fromEntries(Object.entries(models).filter(([key]) =>
    !["attacker_model", "defender_model"].includes(key))) : {};
  return (
    <div className="scenario-threat">
      {fields.application_scenarios != null && (
        <section className="application-scenarios" aria-label="应用场景">
          <h3>应用场景</h3>
          <Content value={fields.application_scenarios} />
        </section>
      )}
      {threat != null && (
        <section className="threat-model" aria-label="威胁模型">
          <h3>威胁模型</h3>
          {models ? <>
            <div className="model-columns">
              {models.attacker_model != null && (
                <section className="model-panel attacker-model" aria-label="攻击者模型">
                  <h4><span className="model-icon"><ModelPersonIcon equipment="sword" /></span>攻击者模型</h4>
                  <Content value={models.attacker_model} />
                </section>
              )}
              {models.defender_model != null && (
                <section className="model-panel defender-model" aria-label="防守方模型">
                  <h4><span className="model-icon"><ModelPersonIcon equipment="shield" /></span>防守方模型</h4>
                  <Content value={models.defender_model} />
                </section>
              )}
            </div>
            {Object.keys(extraModels).length > 0 && <Content value={extraModels} />}
          </> : <Content value={threat} />}
        </section>
      )}
      {Object.keys(extraFields).length > 0 && <Content value={extraFields} />}
    </div>
  );
}

function App() {
  const [data, setData] = useState<IndexData>();
  const [error, setError] = useState("");
  const [checking, setChecking] = useState(true);
  const [lang, setLang] = useState("zh");
  const revision = useRef("");
  const busy = useRef(false);
  const location = useLocation();
  const navigate = useNavigate();
  const [globalQuery, setGlobalQuery] = useState("");
  const [update, setUpdate] = useState(false);
  async function sync() {
    if (busy.current) return;
    busy.current = true;
    try {
      const status = await json<{
        ok: boolean;
        revision: string;
        message?: string;
      }>("/data/status.json");
      if (!status.ok) throw new Error(status.message || "内容校验失败");
      if (revision.current !== status.revision) {
        const next = await json<IndexData>(
          `/data/${status.revision}/index.json`,
        );
        revision.current = status.revision;
        setData(next);
      }
      setError("");
    } catch (e) {
      setError(String(e));
    } finally {
      setChecking(false);
      busy.current = false;
    }
  }
  useEffect(() => {
    sync();
    const timer = import.meta.env.DEV ? setInterval(sync, 4000) : undefined;
    const onFocus = () => { if (!document.hidden) void sync(); };
    window.addEventListener("focus", onFocus);
    return () => { if (timer) clearInterval(timer); window.removeEventListener("focus", onFocus); };
  }, []);
  useEffect(() => {
    const listener = () => {
      setUpdate(true);
      sync().finally(() => setUpdate(false));
    };
    const hot = (
      import.meta as unknown as {
        hot?: {
          on: (s: string, f: () => void) => void;
          off: (s: string, f: () => void) => void;
        };
      }
    ).hot;
    hot?.on("niji-content", listener);
    return () => hot?.off("niji-content", listener);
  }, []);
  useEffect(() => {
    if (!location.pathname.startsWith("/matrix")) window.scrollTo(0, 0);
  }, [location.pathname]);
  return (
    <>
      <header className="header">
        <Link to="/matrix" className="brand">
          <span className="brand-mark">
            <Layers size={23} />
          </span>
          <span className="brand-text">
            <strong>匿迹技战术矩阵</strong>
            <span className="brand-english">Niji Tactics and Techniques Matrix</span>
          </span>
        </Link>
        <nav aria-label="主导航">
          <NavLink to="/matrix">矩阵</NavLink>
          <NavLink to="/library/mechanism">匿迹机理</NavLink>
          <NavLink to="/library/defense">检测与缓解</NavLink>
          <NavLink to="/library/reference">参考资料</NavLink>
          <NavLink to="/simulation">公害仿真</NavLink>
        </nav>
        <form
          className="global-search"
          onSubmit={(e) => {
            e.preventDefault();
            navigate(`/search?q=${encodeURIComponent(globalQuery)}`);
          }}
        >
          <Search size={16} />
          <input
            aria-label="全局搜索"
            placeholder="搜索名称或编号…"
            value={globalQuery}
            onChange={(e) => setGlobalQuery(e.target.value)}
          />
          <button aria-label="提交搜索">
            <ArrowUpRight size={15} />
          </button>
        </form>
        <button
          className="language"
          onClick={() => setLang(lang === "zh" ? "en" : "zh")}
        >
          {lang === "zh" ? "EN" : "中文"}
        </button>
      </header>
      {error && (
        <div className="error" role="alert">
          <strong>
            内容同步失败 ·{" "}
            {data ? "正在显示上次成功校验的版本" : "暂时无法加载矩阵"}
          </strong>
          <details>
            <summary>查看错误详情</summary>
            <pre>{error}</pre>
          </details>
          <button onClick={sync}>重新校验状态</button>
        </div>
      )}
      {data ? (
        <Context.Provider value={{ data, lang }}>
          <main>
            {location.pathname === "/simulation" || location.pathname.startsWith("/simulation/") ? (
              <SimulationErrorBoundary><Suspense fallback={<div className="empty">正在加载画布…</div>}><Simulation data={data} lang={lang} /></Suspense></SimulationErrorBoundary>
            ) : location.pathname.startsWith("/objects/") ? (
              <Detail key={location.pathname + data.revision} />
            ) : location.pathname.startsWith("/library/") ||
              location.pathname === "/search" ? (
              <Library />
            ) : location.pathname === "/" || location.pathname === "/matrix" ? (
              <Matrix />
            ) : (
              <div className="empty">
                <h1>页面不存在</h1>
                <Link to="/matrix">返回矩阵</Link>
              </div>
            )}
          </main>
          {!location.pathname.startsWith("/simulation") && <footer>
            <span>
              <i className={error ? "dot error-dot" : "dot"} />
              {error ? "内容同步异常" : update ? "正在同步" : "本地内容已同步"}
            </span>
            <span>
              NIJI MATRIX · {String(data.matrix.lifecycle?.version || "")} ·{" "}
              {data.revision.slice(0, 8)}
            </span>
            <span>以证据理解匿迹</span>
          </footer>}
        </Context.Provider>
      ) : (
        <div className="empty" role="status">
          {checking
            ? "正在校验并载入矩阵内容…"
            : "内容尚不可用，请查看上方错误信息。"}
        </div>
      )}
    </>
  );
}
function readExpanded(): string[] {
  try {
    const value = JSON.parse(sessionStorage.getItem("niji-expanded") || "[]");
    return Array.isArray(value)
      ? value.filter((x) => typeof x === "string")
      : [];
  } catch {
    return [];
  }
}
function Matrix() {
  const { data, lang } = useData();
  const [params, setParams] = useSearchParams();
  const q = params.get("q") || "";
  const mechanism = params.get("mechanism") || "";
  const view = params.get("view") || "matrix";
  const [expanded, setExpanded] = useState<Set<string>>(
    () => new Set(readExpanded()),
  );
  const board = useRef<HTMLDivElement>(null);
  const tactics = data.matrix.tactic_refs
    .map((id) => data.objects[id])
    .filter(Boolean);
  const objects = Object.values(data.objects);
  const techniques = objects
    .filter((o) => o.type === "technique")
    .sort((a, b) => a.id.localeCompare(b.id));
  const query = q.trim().toLowerCase();
  const [searchAutoExpand, setSearchAutoExpand] = useState(true);
  useEffect(() => setSearchAutoExpand(true), [query]);
  const isExpanded = (id: string) => expanded.has(id) || (!!query && searchAutoExpand);
  const matches = (o: RecordData) =>
    !query ||
    `${o.id} ${title(o, "zh")} ${title(o, "en")} ${JSON.stringify(o.aliases || "")}`
      .toLowerCase()
      .includes(query);
  const visible = techniques.filter(
    (o) =>
      (!mechanism || o.mechanism_refs?.includes(mechanism)) &&
      (matches(o) ||
        (o.children || []).some((id) => matches(data.objects[id]))),
  );
  const visibleIDs = new Set(visible.map((o) => o.id));
  const update = (key: string, value: string) => {
    const p = new URLSearchParams(params);
    if (value) p.set(key, value);
    else p.delete(key);
    setParams(p, { replace: true });
  };
  useEffect(() => {
    if (board.current)
      board.current.scrollLeft = Number(
        sessionStorage.getItem("niji-scroll") || 0,
      );
  }, [view]);
  const expandable = techniques.filter(o => o.children?.length).map(o => o.id);
  const visibleExpandable = visible.filter(o => o.children?.length).map(o => o.id);
  const allExpanded = visibleExpandable.length > 0 && visibleExpandable.every(isExpanded);
  const saveExpanded = (next: Set<string>) => {
    setExpanded(next);
    sessionStorage.setItem("niji-expanded", JSON.stringify([...next]));
    setSearchAutoExpand(false);
  };
  const toggle = (id: string) => {
    const next = new Set([...expanded, ...(query && searchAutoExpand ? visibleExpandable : [])]);
    next.has(id) ? next.delete(id) : next.add(id);
    saveExpanded(next);
  };
  const toggleAll = () => saveExpanded(allExpanded ? new Set<string>() : new Set(expandable));
  return (
    <div className="matrix-page">
      <div className="page-heading">
        <div>
          <div className="eyebrow">THE NIJI KNOWLEDGE BASE</div>
          <h1>匿迹技战术矩阵</h1>
          <p>从攻击行为到匿迹机理，探索技术、证据与防御之间的联系。</p>
        </div>
        <div className="matrix-count">
          <strong>{techniques.length}</strong> 技术 <span>/</span>{" "}
          <strong>
            {objects.filter((o) => o.type === "evasion-subtechnique").length}
          </strong>{" "}
          子技术 <span>/</span> {tactics.length} 战术
        </div>
      </div>
      <div className="toolbar">
        <label className="search-field">
          <Search size={17} />
          <input
            aria-label="搜索矩阵"
            placeholder="搜索技术名称、编号或子技术…"
            value={q}
            onChange={(e) => update("q", e.target.value)}
          />
          {q && (
            <button aria-label="清空搜索" onClick={() => update("q", "")}>
              ×
            </button>
          )}
        </label>
        <label className="select-field">
          {mechanism ? <MechanismIcon id={mechanism} size={18} /> : <SlidersHorizontal size={15} />}
          <select
            aria-label="匿迹机理筛选"
            value={mechanism}
            onChange={(e) => update("mechanism", e.target.value)}
          >
            <option value="">全部匿迹机理</option>
            {objects
              .filter((o) => o.type === "mechanism")
              .map((o) => (
                <option key={o.id} value={o.id}>
                  {title(o, lang)}
                </option>
              ))}
          </select>
        </label>
        <div className="toolbar-spacer" />
        <span className="result-count">{visible.length} 项技术</span>
        <div className="segmented">
          <button
            className={view === "matrix" ? "active" : ""}
            aria-pressed={view === "matrix"}
            onClick={() => update("view", "matrix")}
          >
            <Grid2X2 size={15} />
            矩阵
          </button>
          <button
            className={view === "list" ? "active" : ""}
            aria-pressed={view === "list"}
            onClick={() => update("view", "list")}
          >
            <List size={16} />
            列表
          </button>
        </div>
        {view === "matrix" && <button className="matrix-toggle-all" disabled={!visibleExpandable.length} aria-expanded={allExpanded} onClick={toggleAll}>{allExpanded ? "全部收起" : "全部展开"}</button>}
      </div>
      {!visible.length ? (
        <div className="empty">
          <Search size={30} />
          <h2>未找到匹配的技术</h2>
          <p>尝试更短的关键词，或清除机理筛选。</p>
          <button onClick={() => setParams({})}>清除筛选</button>
        </div>
      ) : view === "list" ? (
        <ObjectTable records={visible} />
      ) : (
        <>
          <div
            className="matrix-board"
            ref={board}
            onScroll={(e) =>
              sessionStorage.setItem(
                "niji-scroll",
                String(e.currentTarget.scrollLeft),
              )
            }
          >
            {tactics.map((tactic) => {
              const items = techniques.filter(
                (o) =>
                  o.classification?.tactic_refs?.includes(tactic.id) &&
                  visibleIDs.has(o.id),
              );
              return (
                <section className="tactic-column" key={tactic.id}>
                  <div className="tactic-heading">
                    <div>
                      <Link to={`/objects/${tactic.id}`}>
                        <TacticIcon id={tactic.id} size={18} />
                        {title(tactic, lang)}
                      </Link>
                      <span className="column-count">{items.length}</span>
                    </div>
                    <code>{tactic.id}</code>
                  </div>
                  <div className="techniques" role="region" aria-label={`${title(tactic, lang)}技术列表`} tabIndex={0}>
                    {items.map((o) => (
                      <div
                        className={
                          "technique-group " +
                          (isExpanded(o.id) ? "expanded" : "")
                        }
                        key={o.id}
                      >
                        <div className="technique-card">
                          <Link to={`/objects/${o.id}`}>
                            <span>{title(o, lang)}</span>
                            <code>{o.id}</code>
                          </Link>
                          {!!o.children?.length && (
                            <button
                              aria-label={`展开 ${title(o, lang)} 的子技术`}
                              aria-expanded={isExpanded(o.id)}
                              onClick={() => toggle(o.id)}
                            >
                              {isExpanded(o.id) ? (
                                <ChevronDown size={14} />
                              ) : (
                                <ChevronRight size={14} />
                              )}
                              <span>{o.children.length}</span>
                            </button>
                          )}
                        </div>
                        {isExpanded(o.id) && (
                          <div className="children">
                            {o.children
                              ?.filter(
                                (id) =>
                                  !query ||
                                  matches(o) ||
                                  matches(data.objects[id]),
                              )
                              .map((id) => (
                                <Link key={id} to={`/objects/${id}`}>
                                  <span>{title(data.objects[id], lang)}</span>
                                  <code>{id}</code>
                                </Link>
                              ))}
                          </div>
                        )}
                      </div>
                    ))}
                    {!items.length && (
                      <p className="column-empty">当前筛选无匹配项</p>
                    )}
                  </div>
                </section>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}
function ObjectTable({ records }: { records: RecordData[] }) {
  const { lang } = useData();
  return (
    <div className="object-table">
      {records.map((o) => (
        <div className="object-table-entry" key={o.id}>
        <Link to={`/objects/${o.id}`} className="object-row">
          <code>{o.id}</code>
          <div>
            <strong className="object-row-title">{o.type === "mechanism" && <MechanismIcon id={o.id} size={21} />}{o.type === "tactic" && <TacticIcon id={o.id} size={21} />}{title(o, lang)}</strong>
            {o.summary && (
              <p>{o.summary[lang as "zh" | "en"] || o.summary.zh}</p>
            )}
          </div>
          <span className="type-label">{labels[o.type] || o.type}</span>
          <ChevronRight size={16} />
        </Link>
        <RecordSourceLinks record={o} lang={lang} />
        </div>
      ))}
    </div>
  );
}
function Library() {
  const { data } = useData();
  const location = useLocation();
  const [params, setParams] = useSearchParams();
  const category = location.pathname.split("/")[2] || "search";
  const query = params.get("q") || "";
  const [limit, setLimit] = useState(50);
  const isSearch = location.pathname === "/search";
  const heading = isSearch
    ? "搜索知识库"
    : category === "defense"
      ? "检测与缓解"
      : labels[category] || category;
  const records = Object.values(data.objects)
    .filter((o) =>
      isSearch
        ? !["matrix", "technique-decision", "relationship"].includes(o.type)
        : category === "defense"
          ? ["detection-strategy", "detection-analytic", "mitigation"].includes(
              o.type,
            )
          : o.type === category,
    )
    .filter((o) =>
      `${o.id} ${title(o, "zh")} ${title(o, "en")} ${JSON.stringify(o.summary || "")}`
        .toLowerCase()
        .includes(query.trim().toLowerCase()),
    );
  useEffect(() => setLimit(50), [query, category]);
  return (
    <div className="library-page">
      <div className="eyebrow">EXPLORE THE KNOWLEDGE</div>
      <h1>{heading}</h1>
      <p className="subtitle">
        {isSearch
          ? "通过名称、编号或摘要查找关联知识。"
          : "从结构化知识出发，追溯技术、观测与证据。"}
      </p>
      <div className="toolbar">
        <label className="search-field">
          <Search size={17} />
          <input
            aria-label="搜索当前知识库"
            value={query}
            onChange={(e) =>
              setParams({ q: e.target.value }, { replace: true })
            }
            placeholder="搜索名称、编号或摘要…"
          />
        </label>
        <span className="result-count">{records.length} 个结果</span>
      </div>
      <ObjectTable records={records.slice(0, limit)} />
      {!records.length && <div className="empty">没有匹配的内容</div>}
      {records.length > limit && (
        <button className="load-more" onClick={() => setLimit(limit + 50)}>
          加载更多（已显示 {limit} / {records.length}）
        </button>
      )}
    </div>
  );
}
const sectionKeys = [
  "definition_and_concept",
  "stealth_characteristics",
  "scope_boundary_definition",
  "application_scenarios_and_threat_model",
  "stealth_mechanisms",
  "subtechnique_taxonomy",
  "defense",
  "evidence",
  "research",
];
function Detail() {
  const { data, lang } = useData();
  const location = useLocation();
  const id = decodeURIComponent(location.pathname.split("/")[2] || "");
  const [obj, setObj] = useState<RecordData>();
  const [error, setError] = useState("");
  const [activeSection, setActiveSection] = useState("");
  useEffect(() => {
    let live = true;
    json<RecordData>(
      `/data/${data.revision}/objects/${encodeURIComponent(id)}.json`,
    )
      .then((o) => {
        if (live) setObj(o);
      })
      .catch((e) => {
        if (live) setError(String(e));
      });
    return () => {
      live = false;
    };
  }, [id, data.revision]);
  useEffect(() => {
    if (obj) {
      document.title = `${title(obj, lang)} · 匿迹技战术矩阵`;
      if (location.hash)
        document.getElementById(location.hash.slice(1))?.scrollIntoView();
    }
    return () => {
      document.title = "匿迹技战术矩阵 · Niji Matrix";
    };
  }, [obj, lang, location.hash]);
  useEffect(() => {
    if (!obj) return;
    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries.find((e) => e.isIntersecting);
        if (entry) setActiveSection(entry.target.id);
      },
      { rootMargin: "-110px 0px -65% 0px" },
    );
    document
      .querySelectorAll(".reading-section")
      .forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, [obj]);
  if (!data.objects[id])
    return (
      <div className="empty">
        <h1>未找到该对象</h1>
        <code>{id}</code>
        <Link to="/matrix">返回矩阵</Link>
      </div>
    );
  if (error)
    return (
      <div className="empty" role="alert">
        {error}
      </div>
    );
  if (!obj) return <div className="empty">正在加载详情…</div>;
  const isTechnique = ["technique", "evasion-subtechnique"].includes(obj.type);
  const hide = new Set([
    "id",
    "type",
    "schema_version",
    "name",
    "name_zh",
    "name_en",
    "title_zh",
    "title_en",
    "summary",
    "_source",
    "_reverse",
  ]);
  const fields = isTechnique
    ? [
        ...sectionKeys,
        ...Object.keys(obj).filter(
          (k) => !sectionKeys.includes(k) && !hide.has(k),
        ),
      ]
    : Object.keys(obj).filter(
        (k) => !hide.has(k) && !k.endsWith(lang === "zh" ? "_en" : "_zh"),
      );
  const sections = fields.filter(
    (k) =>
      obj[k] != null &&
      (!Array.isArray(obj[k]) || (obj[k] as unknown[]).length > 0),
  );
  const back = (obj._reverse || []) as string[];
  const parentTechnique = obj.type === "evasion-subtechnique" && obj.parent_ref
    ? data.objects[obj.parent_ref]
    : undefined;
  return (
    <div className="detail-page">
      <div className="breadcrumb" role="navigation" aria-label="面包屑导航">
        <Link to="/matrix">
          <ArrowLeft size={14} aria-hidden="true" />
          匿迹技战术矩阵
        </Link>
        <ChevronRight size={12} aria-hidden="true" />
        <span>{labels[parentTechnique ? parentTechnique.type : obj.type]}</span>
        <ChevronRight size={12} aria-hidden="true" />
        {parentTechnique && (
          <>
            <Link to={`/objects/${parentTechnique.id}`}>{title(parentTechnique, lang)}</Link>
            <ChevronRight size={12} aria-hidden="true" />
          </>
        )}
        <span className="breadcrumb-current" aria-current="page">{obj.type === "mechanism" && <MechanismIcon id={obj.id} size={15} />}{obj.type === "tactic" && <TacticIcon id={obj.id} size={15} />}{title(obj, lang)}</span>
      </div>
      <div className="detail-layout">
        <aside className="outline">
          <span className="eyebrow">本页目录</span>
          {sections.map((k) => (
            <SectionLink
              className={activeSection === k ? "current" : ""}
              id={k}
              key={k}
            >
              {labels[k.replace(/_(zh|en)$/, "")] || k}
            </SectionLink>
          ))}
          {!!back.length && <SectionLink id="reverse">反向引用</SectionLink>}
        </aside>
        <article>
          <div className="detail-title">
            <span className="type-label">{labels[obj.type]}</span>
            <h1 className={["mechanism", "tactic"].includes(obj.type) ? "mechanism-page-title" : undefined}>{obj.type === "mechanism" && <MechanismIcon id={obj.id} size={32} />}{obj.type === "tactic" && <TacticIcon id={obj.id} size={32} />}{title(obj, lang)}</h1>
            <div className="detail-subtitle">
              <code>{id}</code>
              <RecordSourceLinks record={obj} lang={lang} showLabel />
              <span>{title(obj, lang === "zh" ? "en" : "zh")}</span>
              {obj.lifecycle?.status && (
                <span className="badge">
                  {statuses[obj.lifecycle.status] || obj.lifecycle.status}
                </span>
              )}
            </div>
            {obj.summary && (
              <p className="lead">
                {obj.summary[lang as "zh" | "en"] || obj.summary.zh}
              </p>
            )}
          </div>
          {sections.map((k) => (
            <section className="reading-section" id={k} key={k}>
              <h2>{labels[k.replace(/_(zh|en)$/, "")] || k}</h2>
              {k === "application_scenarios_and_threat_model" ? (
                <ScenarioAndThreatModel value={obj[k]} />
               ) : k === "stealth_mechanisms" ? (
                <MechanismCards value={obj[k]} />
              ) : k === "subtechnique_taxonomy" ? (
                <SubtechniqueTaxonomy value={obj[k]} />
              ) : k === "defense" ? <DefenseSection value={obj[k]} />
                : k === "evidence" ? <EvidenceSection value={obj[k]} />
                : k === "research" ? <ResearchSection value={obj[k]} />
                : k === "classification" ? <ClassificationSection value={obj[k]} />
                : k === "lifecycle" ? <LifecycleSection value={obj[k]} />
                : <Content value={obj[k]} />}
            </section>
          ))}
          {!!back.length && (
            <section className="reading-section" id="reverse">
              <h2>
                反向引用 <span className="muted">{back.length}</span>
              </h2>
              <ReverseReferences ids={back} />
            </section>
          )}
        </article>
        <aside className="related">
          <h3>关联导航</h3>
          {obj.parent_ref && (
            <>
              <span className="field-label">父技术</span>
              <ObjectLink id={obj.parent_ref} />
            </>
          )}
          {obj.classification?.tactic_refs?.map((id) => (
            <ObjectLink key={id} id={id} />
          ))}
          {data.objects[id].mechanism_refs?.map((id) => (
            <ObjectLink key={id} id={id} />
          ))}
          <hr />
          <h3>内容来源</h3>
          <p className="source-path">{String(obj._source)}</p>
          <p className="muted">与本地匿迹矩阵内容同步</p>
          <hr />
          <Link to="/library/reference">
            <BookOpen size={15} /> 浏览参考资料
          </Link>
        </aside>
      </div>
    </div>
  );
}
const SiteRouter = import.meta.env.VITE_ROUTER_MODE === "hash" ? HashRouter : BrowserRouter;
createRoot(document.getElementById("root")!).render(
  <SiteRouter>
    <App />
  </SiteRouter>,
);
