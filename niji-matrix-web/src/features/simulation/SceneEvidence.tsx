import { publicAssetUrl } from "../../paths";
import { Link } from 'react-router-dom';
import type { IndexData } from '../../data';
import { RecordSourceLinks, SourceLink, sourceUrl } from '../../components/SourceLinks';
import type {Provenance,Scene,SceneNode,SceneSource} from './model';
const basisLabels={reported:'报道陈述',analysis:'分析推断',layout:'展示处理'};

export function SceneSourceLink({ source, data, lang }: { source: SceneSource; data: IndexData; lang: string }) {
 const original = sourceUrl(source.url);
 const asset = source.assetPath?.startsWith('/') && !source.assetPath.startsWith('//')
   ? publicAssetUrl(source.assetPath) : sourceUrl(source.assetPath);
 const href = asset || original;
 return <span className="sim-source-link">
   {source.matrixRef ? <Link to={`/objects/${encodeURIComponent(source.matrixRef)}`} target="_blank" rel="noopener noreferrer">{source.title}</Link>
     : href ? <a href={href} target="_blank" rel="noopener noreferrer">{source.title}</a> : <span>{source.title}</span>}
   {original ? <SourceLink href={original} name={source.title} />
     : <RecordSourceLinks record={source.matrixRef ? data.objects[source.matrixRef] : undefined} lang={lang} />}
   {asset && asset !== original && <SourceLink href={asset} name={source.title} label="查看材料" />}
 </span>;
}

export function SceneEvidence({scene,provenance,attributes,data,lang}:{scene:Scene;provenance?:Provenance[];attributes?:SceneNode['attributes'];data:IndexData;lang:string}){
 if(!provenance?.length&&!attributes)return null;
 return <section className="sim-inspector-section sim-provenance"><h3>来源与原图信息</h3>{attributes&&<dl>{Object.entries(attributes).map(([key,value])=><div key={key}><dt>{key}</dt><dd>{value}</dd></div>)}</dl>}{provenance?.map((item,i)=>{const source=scene.sources.find(s=>s.id===item.sourceRef);return <div className="sim-evidence-record" key={i}><span className="sim-evidence-basis">{basisLabels[item.basis]}</span><strong>{item.locator}</strong>{source?<SceneSourceLink source={source} data={data} lang={lang}/>:<span>{item.sourceRef}</span>}{item.note&&<p>{item.note}</p>}</div>})}</section>;
}
export function SceneLegend({scene}:{scene:Scene}){if(!scene.legend?.length)return null;return <details className="sim-scene-legend"><summary>线路图例</summary><div>{scene.legend.map((item,i)=><span key={i}><i style={{borderColor:item.color,borderTopStyle:item.lineStyle}}/>{item.label}</span>)}</div></details>;}
