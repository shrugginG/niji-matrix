import {useLayoutEffect,useRef,useState} from 'react';
import {createPortal} from 'react-dom';
import {title,type IndexData} from '../../data';
import {MechanismIcon} from '../../components/MechanismIcon';
import type {Binding} from './model';
export type TechniqueHoverTarget={kind:'node'|'edge';id:string;name:string;x:number;y:number};
const basisLabels={fact:'有证据事实',inference:'分析推断',hypothesis:'场景假设'};
export default function TechniqueHover({target,bindings,data,lang}:{target:TechniqueHoverTarget;bindings:Binding[];data:IndexData;lang:string}){
 const ref=useRef<HTMLDivElement>(null);const[position,setPosition]=useState({left:target.x+16,top:target.y+16});
 useLayoutEffect(()=>{const el=ref.current;if(!el)return;const width=el.offsetWidth,height=el.offsetHeight;const left=target.x+16+width>window.innerWidth-10?target.x-width-16:target.x+16;const top=target.y+16+height>window.innerHeight-10?target.y-height-16:target.y+16;setPosition({left:Math.max(10,Math.min(left,window.innerWidth-width-10)),top:Math.max(10,Math.min(top,window.innerHeight-height-10))});},[target,bindings,data,lang]);
 const visible=bindings;
 return createPortal(<div ref={ref} className={`sim-tech-hover ${bindings.length>3?"is-compact":""}`} role="tooltip" aria-label={`${target.name}的关联匿迹技战术`} style={position}>
   <div className="sim-tech-hover-heading"><strong>{target.name||'未命名对象'}</strong><span>{target.kind==='node'?'实体':'连线'} · {bindings.length} 项关联</span></div>
   <div className="sim-tech-hover-cards">{visible.map(binding=>{const record=data.objects[binding.matrixRef];const parent=record?.parent_ref?data.objects[record.parent_ref]:undefined;const summary=record?.summary?.[lang as 'zh'|'en']||record?.summary?.zh;return <article className="sim-tech-hover-card" key={binding.id}>
     <div className="sim-tech-hover-title"><strong>{record?title(record,lang):'未解析的矩阵引用'}</strong><span>{record?.type==='evasion-subtechnique'?'子技术':'技术'}</span></div>
     <code>{binding.matrixRef}</code>{parent&&<div className="sim-tech-hover-parent">所属技术：{title(parent,lang)}</div>}
     {summary&&<p className="sim-tech-hover-summary">{summary}</p>}
     {binding.applicationNote&&<p className="sim-tech-hover-application"><span>场景应用</span>{binding.applicationNote}</p>}
     <div className="sim-tech-hover-meta"><span>{basisLabels[binding.basis]}</span><div>{record?.mechanism_refs?.map(id=><span key={id} title={data.objects[id]?title(data.objects[id],lang):id}><MechanismIcon id={id} size={13}/>{data.objects[id]?title(data.objects[id],lang):id}</span>)}</div></div>
   </article>})}</div>
   <div className="sim-tech-hover-footer">点击对象，可在右侧查看完整关联信息</div>
 </div>,document.body);
}
