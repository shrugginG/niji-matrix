import Ajv from "ajv";
import schema from "../../../schemas/niji-scene.schema.json";
import type { IndexData } from "../../data";
export type Point = { x: number; y: number };
export type Provenance = { sourceRef:string; locator:string; basis:"reported"|"analysis"|"layout"; note?:string };
export type SceneSource = { id:string; title:string; url?:string; matrixRef?:string; assetPath?:string; author?:string; publishedAt?:string };
export type SceneNode = {
  id: string;
  kind: string;
  category: "human" | "cloud" | "endpoint" | "auxiliary";
  name: string;
  position: Point;
  size: { width: number; height: number };
  parentId?: string;
  color: string;
  notes: string;
  container: boolean;
  subtitle?: string;
  entityClass?: "software"|"artifact"|"service"|"annotation";
  provenance?: Provenance[];
  attributes?: Record<string,string>;
  borderColor?: string;
};
export type SceneEdge = {
  id: string;
  source: string;
  target: string;
  sourcePort: "left" | "right" | "top" | "bottom";
  targetPort: "left" | "right" | "top" | "bottom";
  name: string;
  relation: string;
  direction: "forward" | "both" | "none";
  lineStyle: "solid" | "dashed" | "dotted";
  routing: "bezier" | "step" | "straight";
  color: string;
  notes: string;
  waypoints: Point[];
  anchorMode?: "auto" | "manual";
  provenance?: Provenance[];
  pathGroup?: string;
  labelPosition?: Point;
};
export type Binding = {
  id: string;
  target: { kind: "node" | "edge"; id: string };
  matrixRef: string;
  applicationNote: string;
  basis: "fact" | "inference" | "hypothesis";
  evidenceRefs: string[];
};
export type Scene = {
  schemaVersion: "1.0.0";
  id: string;
  name: string;
  description: string;
  category: "custom" | "threat" | "case";
  author: string;
  createdAt: string;
  updatedAt: string;
  matrix: { id: string; version: string; revision: string };
  nodes: SceneNode[];
  edges: SceneEdge[];
  bindings: Binding[];
  viewport: { x: number; y: number; zoom: number };
  sources: SceneSource[];
  views?: {id:string;name:string;nodeIds:string[]}[];
  legend?: {label:string;color:string;lineStyle:"solid"|"dashed"|"dotted"}[];
  reviewNotes?: string[];
  presetId?: string;
};
export function newId(prefix: string): string {
  // randomUUID is secure-context-only; getRandomValues also works on LAN HTTP.
  if (typeof globalThis.crypto.randomUUID === "function") {
    return `${prefix}-${globalThis.crypto.randomUUID()}`;
  }
  const bytes = globalThis.crypto.getRandomValues(new Uint8Array(16));
  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  const hex = Array.from(bytes, byte => byte.toString(16).padStart(2, "0")).join("");
  return `${prefix}-${hex.slice(0,8)}-${hex.slice(8,12)}-${hex.slice(12,16)}-${hex.slice(16,20)}-${hex.slice(20)}`;
}
export function blankScene(data: IndexData): Scene {
  const time = new Date().toISOString();
  return {
    schemaVersion: "1.0.0",
    id: newId("scene"),
    name: "未命名场景",
    description: "",
    category: "custom",
    author: "",
    createdAt: time,
    updatedAt: time,
    matrix: {
      id: "niji-matrix",
      version: data.matrix.lifecycle?.version || "",
      revision: data.revision,
    },
    nodes: [],
    edges: [],
    bindings: [],
    viewport: { x: 0, y: 0, zoom: 1 },
    sources: [],
  };
}
const validate = new Ajv({ allErrors: true }).compile<Scene>(schema);
export function parseScene(value: unknown): Scene {
  if (!validate(value))
    throw new Error(
      "场景格式无效：" +
        (validate.errors || [])
          .slice(0, 4)
          .map((e) => `${e.instancePath || "/"} ${e.message}`)
          .join("；"),
    );
  const scene = structuredClone(value);
  const ids = new Set<string>();
  for (const item of [
    ...scene.nodes,
    ...scene.edges,
    ...scene.bindings,
    ...scene.sources,
  ]) {
    if (ids.has(item.id)) throw new Error(`重复 ID：${item.id}`);
    ids.add(item.id);
  }
  const nodes = new Map(scene.nodes.map((n) => [n.id, n]));
  const edges = new Set(scene.edges.map((e) => e.id));
  for (const n of scene.nodes) {
    const seen = new Set([n.id]);
    let parent = n.parentId;
    while (parent) {
      if (seen.has(parent)) throw new Error("容器层级存在循环");
      seen.add(parent);
      const p = nodes.get(parent);
      if (!p || !p.container) throw new Error(`无效容器：${parent}`);
      parent = p.parentId;
    }
  }
  for (const e of scene.edges)
    if (!nodes.has(e.source) || !nodes.has(e.target))
      throw new Error(`连线端点不存在：${e.id}`);
  for (const b of scene.bindings)
    if (
      !(b.target.kind === "node"
        ? nodes.has(b.target.id)
        : edges.has(b.target.id))
    )
      throw new Error(`技术关联的目标不存在：${b.id}`);
  const sourceIds=new Set(scene.sources.map(s=>s.id));
  for(const item of [...scene.nodes,...scene.edges])for(const evidence of item.provenance||[])if(!sourceIds.has(evidence.sourceRef))throw new Error(`来源不存在：${evidence.sourceRef}`);
  for(const view of scene.views||[])for(const id of view.nodeIds)if(!nodes.has(id))throw new Error(`视图引用节点不存在：${id}`);
  return scene;
}
export function warnings(scene: Scene, data: IndexData): string[] {
  const out: string[] = [];
  if (scene.matrix.revision && scene.matrix.revision !== data.revision)
    out.push("场景使用的矩阵快照与当前版本不同，请复核知识关联。");
  for (const b of scene.bindings) {
    const o = data.objects[b.matrixRef];
    if (!o || !["technique", "evasion-subtechnique"].includes(o.type))
      out.push(`无法解析技术引用 ${b.matrixRef}，已保留原关联。`);
    else if (o.lifecycle?.status === "deprecated")
      out.push(`${b.matrixRef} 已弃用，原关联仍保留。`);
    for (const ref of b.evidenceRefs)
      if (!scene.sources.some((s) => s.id === ref) && !data.objects[ref])
        out.push(`证据引用 ${ref} 尚未解析。`);
  }
  return [...new Set(out)];
}
export function removeObjects(
  scene: Scene,
  selection: { kind: "node" | "edge"; id: string },
): Scene {
  const next = structuredClone(scene);
  const removed = new Set([selection.id]);
  if (selection.kind === "node") {
    let changed = true;
    while (changed) {
      changed = false;
      for (const n of next.nodes)
        if (n.parentId && removed.has(n.parentId) && !removed.has(n.id)) {
          removed.add(n.id);
          changed = true;
        }
    }
    next.nodes = next.nodes.filter((n) => !removed.has(n.id));
    for (const e of next.edges)
      if (removed.has(e.source) || removed.has(e.target)) removed.add(e.id);
  }
  next.edges = next.edges.filter((e) => !removed.has(e.id));
  next.bindings = next.bindings.filter((b) => !removed.has(b.target.id));
  next.views = next.views?.map(view=>({...view,nodeIds:view.nodeIds.filter(id=>!removed.has(id))}));
  return next;
}
export function orderedNodes(nodes: SceneNode[]): SceneNode[] {
  const out: SceneNode[] = [];
  const visited = new Set<string>();
  const byId = new Map(nodes.map((n) => [n.id, n]));
  const visit = (n: SceneNode) => {
    if (visited.has(n.id)) return;
    visited.add(n.id);
    if (n.parentId && byId.has(n.parentId)) visit(byId.get(n.parentId)!);
    out.push(n);
  };
  nodes.forEach(visit);
  return out;
}
export function absolutePosition(node: SceneNode, nodes: SceneNode[]): Point {
  let point = { ...node.position };
  let parent = node.parentId;
  while (parent) {
    const n = nodes.find((n) => n.id === parent);
    if (!n) break;
    point = { x: point.x + n.position.x, y: point.y + n.position.y };
    parent = n.parentId;
  }
  return point;
}

/** Select facing ports using absolute geometry, including nested containers. */
export function naturalAnchors(edge: SceneEdge, nodes: SceneNode[]): Pick<SceneEdge, 'sourcePort' | 'targetPort'> {
  const source = nodes.find(n => n.id === edge.source), target = nodes.find(n => n.id === edge.target);
  if (!source || !target || source === target) return { sourcePort: edge.sourcePort, targetPort: edge.targetPort };
  const ports = (node: SceneNode) => {
    const p = absolutePosition(node, nodes), w = node.size.width, h = node.size.height;
    return [
      {id:'left' as const,x:p.x,y:p.y+h/2,nx:-1,ny:0},
      {id:'right' as const,x:p.x+w,y:p.y+h/2,nx:1,ny:0},
      {id:'top' as const,x:p.x+w/2,y:p.y,nx:0,ny:-1},
      {id:'bottom' as const,x:p.x+w/2,y:p.y+h,nx:0,ny:1},
    ];
  };
  let best = Infinity, result = { sourcePort: edge.sourcePort, targetPort: edge.targetPort };
  for (const a of ports(source)) for (const b of ports(target)) {
    const dx=b.x-a.x, dy=b.y-a.y, distance=Math.hypot(dx,dy)||1;
    const facingA=(a.nx*dx+a.ny*dy)/distance, facingB=-(b.nx*dx+b.ny*dy)/distance;
    const score=distance+100*(2-facingA-facingB)+1000*(Math.max(0,-facingA)+Math.max(0,-facingB));
    if(score<best){best=score;result={sourcePort:a.id,targetPort:b.id};}
  }
  return result;
}
export function updateAutomaticAnchors(scene: Scene, upgradeLegacy=false): void {
  for(const edge of scene.edges){
    if(upgradeLegacy && !edge.anchorMode){
      edge.anchorMode=edge.sourcePort==='right'&&edge.targetPort==='left'&&!edge.waypoints.length?'auto':'manual';
    }
    if(edge.anchorMode==='auto'&&!edge.waypoints.length)Object.assign(edge,naturalAnchors(edge,scene.nodes));
  }
}
