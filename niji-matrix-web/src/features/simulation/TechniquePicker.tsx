import { useEffect, useRef, useState } from "react";
import { Search, X, ChevronDown, ChevronRight, ArrowLeft } from "lucide-react";
import { title, type IndexData } from "../../data";
import { TacticIcon } from "../../components/TacticIcon";
export default function TechniquePicker({ data, lang, existing, targetName, onApply, onClose }: {
  data: IndexData; lang: string; existing: string[]; targetName: string;
  onApply: (ids: string[]) => void; onClose: () => void;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  const body = useRef<HTMLDivElement>(null);
  const heading = useRef<HTMLHeadingElement>(null);
  const [q, setQ] = useState("");
  const [tactic, setTactic] = useState("");
  const [selected, setSelected] = useState(new Set(existing));
  const [expanded, setExpanded] = useState(new Set<string>());
  const query = q.trim().toLowerCase();
  useEffect(() => { ref.current?.showModal(); return () => ref.current?.close(); }, []);
  useEffect(() => { if (body.current) body.current.scrollTop = 0; }, [tactic, query]);
  const matches = (id: string) => {
    const o = data.objects[id];
    return o && `${id} ${title(o, "zh")} ${title(o, "en")}`.toLowerCase().includes(query);
  };
  const techniques = Object.values(data.objects).filter(o => o.type === "technique").sort((a, b) => a.id.localeCompare(b.id));
  const tactics = data.matrix.tactic_refs.map(id => data.objects[id]).filter(Boolean);
  const parents = techniques.filter(o => (!tactic || o.classification?.tactic_refs?.includes(tactic)) && (matches(o.id) || o.children?.some(matches)));
  const home = !tactic && !query;
  function goToTactic(id: string) { setTactic(id); setQ(""); setTimeout(() => heading.current?.focus(), 0); }
  function checkbox(id: string, child = false) {
    return <label className={`sim-tech-option ${child ? "is-child" : ""}`}>
      <input type="checkbox" checked={selected.has(id)} onChange={e => setSelected(old => { const next = new Set(old); e.target.checked ? next.add(id) : next.delete(id); return next; })}/>
      <span>{title(data.objects[id], lang)}<code>{id}</code></span>
    </label>;
  }
  return <dialog className="sim-picker sim-picker-hierarchical" ref={ref} onCancel={onClose} aria-labelledby="sim-picker-title">
    <div className="sim-picker-heading"><div><h2 id="sim-picker-title">关联匿迹技战术</h2><p>添加到：{targetName}</p></div><button aria-label="关闭技术选择器" onClick={onClose}><X size={18}/></button></div>
    <div className="sim-picker-filters"><label><Search size={16}/><input autoFocus aria-label="搜索技术或子技术" value={q} onChange={e => setQ(e.target.value)} placeholder={tactic ? "在当前战术中搜索技术或子技术…" : "搜索全部技术或子技术名称、编号…"}/>{q && <button aria-label="清空技术搜索" onClick={() => setQ("")}><X size={14}/></button>}</label></div>
    <div className="sim-picker-breadcrumb">
      {!home && <><button onClick={() => goToTactic("")}><ArrowLeft size={14}/>全部战术</button><ChevronRight size={12}/></>}
      <h3 ref={heading} tabIndex={-1}>{home ? "选择匿迹战术" : tactic ? <><TacticIcon id={tactic} size={19}/>{title(data.objects[tactic], lang)}</> : "全局搜索结果"}</h3>
      <span>{home ? `${tactics.length} 个战术` : `${parents.length} 项技术`}</span>
    </div>
    <div className="sim-picker-body" ref={body}>
      {home ? <div className="sim-tactic-grid">{tactics.map(t => {
        const items = techniques.filter(o => o.classification?.tactic_refs?.includes(t.id));
        const relatedIds = new Set(items.flatMap(o => [o.id, ...(o.children || [])]));
        const count = [...selected].filter(id => relatedIds.has(id)).length;
        return <button key={t.id} className={`sim-tactic-card ${count ? "has-selections" : ""}`} aria-label={`选择战术 ${title(t, lang)}`} onClick={() => goToTactic(t.id)}>
          <TacticIcon id={t.id} size={24}/><span className="sim-tactic-card-copy"><strong>{title(t, lang)}</strong><span><code>{t.id}</code><span>{items.length} 项技术</span></span></span>
          {count ? <span className="sim-tactic-selected">已选 {count}</span> : <ChevronRight size={14}/>} 
        </button>;
      })}</div> : <>
        <p className="sim-picker-hint">勾选技术，或展开选择子技术；返回战术首页会保留已选内容。</p>
        <div className="sim-tech-tree">{parents.map(o => <div key={o.id} className="sim-tech-group">
          <div className="sim-tech-parent">{!!o.children?.length && <button aria-label={`展开 ${title(o, lang)} 的子技术`} aria-expanded={expanded.has(o.id) || !!query} onClick={() => setExpanded(old => { const next = new Set(old); next.has(o.id) ? next.delete(o.id) : next.add(o.id); return next; })}>{expanded.has(o.id) || query ? <ChevronDown size={15}/> : <ChevronRight size={15}/>}</button>}{checkbox(o.id)}{!!o.children?.length && <span className="sim-child-count">{o.children.length} 子技术</span>}</div>
          {(expanded.has(o.id) || query) && o.children?.filter(id => !query || matches(o.id) || matches(id)).map(id => <div key={id}>{checkbox(id, true)}</div>)}
        </div>)}{!parents.length && <p className="sim-no-results">没有匹配的技术</p>}</div>
      </>}
    </div>
    <div className="sim-picker-footer"><span aria-live="polite">已选择 {selected.size} 项</span><button onClick={onClose}>取消</button><button className="sim-primary" onClick={() => onApply([...selected])}>应用所选</button></div>
  </dialog>;
}
