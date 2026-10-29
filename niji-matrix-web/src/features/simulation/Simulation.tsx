import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import {
  ReactFlow,
  ReactFlowProvider,
  Background,
  BackgroundVariant,
  Controls,
  MiniMap,
  Handle,
  Position,
  NodeResizer,
  ConnectionMode,
  MarkerType,
  BaseEdge,
  EdgeLabelRenderer,
  getBezierPath,
  getSmoothStepPath,
  getStraightPath,
  type NodeProps,
  type EdgeProps,
  type ReactFlowInstance,
  type Node,
  type Edge,
  type Connection,
  type NodeChange,
} from "@xyflow/react";
import {
  Plus,
  Save,
  Upload,
  Download,
  Undo2,
  Redo2,
  Trash2,
  MousePointer2,
  Hand,
  Link2,
  Search,
  X,
  ChevronDown,
  FilePlus2,
  FolderOpen,
  Layers,
  LocateFixed,
} from "lucide-react";
import "@xyflow/react/dist/style.css";
import "./simulation.css";
import { title, type IndexData } from "../../data";
import { palette, relations, categoryNames, swatches } from "./palette";
import {
  blankScene,
  newId,
  parseScene,
  warnings,
  removeObjects,
  orderedNodes,
  absolutePosition,
  updateAutomaticAnchors,
  type Scene,
  type SceneNode,
  type SceneEdge,
  type Binding,
} from "./model";
import { saveDraft, drafts, activeDraft } from "./storage";
import TechniquePicker from "./TechniquePicker";
import TechniqueHover, {type TechniqueHoverTarget} from "./TechniqueHover";
import { SceneEvidence, SceneLegend, SceneSourceLink } from "./SceneEvidence";
import catalog from "../../../scenes/catalog.json";
const sceneFiles = import.meta.glob("../../../scenes/**/*.niji-scene.json", {
  import: "default",
});
type Selection = { kind: "node" | "edge"; id: string } | null;
type EntityData = {
  name: string;
  kind: string;
  color: string;
  container: boolean;
  count: number;
  onResizeStart: () => void;
  subtitle?:string;
  entityClass?:SceneNode["entityClass"];
  borderColor?:string;
};
type FlowNode = Node<EntityData>;
type FlowEdge = Edge<{ edge: SceneEdge; count: number }>;
function EntityNode({ data, selected }: NodeProps<FlowNode>) {
  const Icon = palette.find((p) => p.kind === data.kind)?.icon || Layers;
  return (
    <div
      className={`sim-entity ${data.count > 0 ? "has-techniques" : ""} ${data.entityClass ? "sim-logical" : ""} ${data.kind === "junction" ? "sim-junction" : ""} ${data.container ? "sim-container" : ""} ${selected ? "is-selected" : ""}`}
      style={{ background: data.count > 0 ? `linear-gradient(rgba(18,116,93,.065),rgba(18,116,93,.065)), ${data.container ? `${data.color}80` : data.color}` : data.container ? `${data.color}80` : data.color, borderColor: selected ? "#12745d" : data.borderColor || (data.count > 0 ? "#72a88c" : undefined) }}
    >
      <NodeResizer
        color="#12745d"
        isVisible={selected}
        minWidth={data.container ? 260 : data.kind === "junction" ? 40 : 120}
        minHeight={data.container ? 180 : data.kind === "junction" ? 40 : 80}
        onResizeStart={data.onResizeStart}
      />
      <div className="sim-entity-title">
        <Icon size={data.container ? 20 : 30} />
        <strong>{data.name || "未命名实体"}</strong>
        {data.subtitle && <span className="sim-entity-subtitle">{data.subtitle}</span>}
      </div>
      {data.count > 0 && (
        <span className="sim-binding-badge"><Layers size={11} aria-hidden="true"/>匿迹技术 {data.count}</span>
      )}
      {(["left", "right", "top", "bottom"] as const).map((port) => (
        <Handle
          key={port}
          id={port}
          type="source"
          position={
            {
              left: Position.Left,
              right: Position.Right,
              top: Position.Top,
              bottom: Position.Bottom,
            }[port]
          }
          aria-label={`${data.name} ${port} 连接点`}
        />
      ))}
    </div>
  );
}
function RelationEdge(props: EdgeProps<FlowEdge>) {
  const edge = props.data!.edge;
  const args = {
    sourceX: props.sourceX,
    sourceY: props.sourceY,
    targetX: props.targetX,
    targetY: props.targetY,
    sourcePosition: props.sourcePosition,
    targetPosition: props.targetPosition,
  };
  let [path, x, y] =
    edge.routing === "step"
      ? getSmoothStepPath(args)
      : edge.routing === "straight"
        ? getStraightPath(args)
        : getBezierPath(args);
  if (edge.waypoints.length) {
    const points = [
      { x: props.sourceX, y: props.sourceY },
      ...edge.waypoints,
      { x: props.targetX, y: props.targetY },
    ];
    path = points.map((p, i) => `${i ? "L" : "M"} ${p.x} ${p.y}`).join(" ");
    const middle = points[Math.floor(points.length / 2)];
    x = middle.x;
    y = middle.y;
  }
  if(edge.labelPosition){x=edge.labelPosition.x;y=edge.labelPosition.y;}
  return (
    <>
      {props.data!.count > 0 && <path className="sim-edge-technique-halo" d={path} fill="none" stroke="#279469" strokeWidth={props.selected ? 10 : 7} strokeOpacity={0.2} strokeLinecap="round" strokeLinejoin="round" pointerEvents="none" aria-hidden="true" />}
      <BaseEdge
        id={props.id}
        path={path}
        markerEnd={props.markerEnd}
        markerStart={props.markerStart}
        interactionWidth={24}
        style={{
          stroke: edge.color,
          strokeWidth: props.selected ? 2.8 : props.data!.count > 0 ? 2.1 : 1.6,
          strokeDasharray:
            edge.lineStyle === "dashed"
              ? "7 5"
              : edge.lineStyle === "dotted"
                ? "2 5"
                : undefined,
        }}
      />
      <EdgeLabelRenderer>
        <div
          className={`sim-edge-label nodrag nopan ${props.data!.count > 0 ? "has-techniques" : ""} ${props.selected ? "is-selected" : ""}`}
          style={{
            transform: `translate(-50%, -50%) translate(${x}px,${y}px)`,
          }}
        >
          {edge.name || relations[edge.relation]}
          {props.data!.count > 0 && <span>匿迹技术 {props.data!.count}</span>}
        </div>
      </EdgeLabelRenderer>
    </>
  );
}
const nodeTypes = { entity: EntityNode };
const edgeTypes = { relation: RelationEdge };
export default function Simulation(props: { data: IndexData; lang: string }) {
  return (
    <ReactFlowProvider>
      <Editor {...props} />
    </ReactFlowProvider>
  );
}
function sceneDisplayName(scene:Scene){
  if(scene.presetId==='nwpu-nsa-report' && /^NSA 入侵西北工业大学(?:｜报道拓扑复刻)?(?: · (?:副本|导入))*$/.test(scene.name))return 'NSA 入侵西北工业大学';
  if(scene.presetId==='remote-access-trojan' && /^远控木马(?:传播场景（教学示意）)?(?: · (?:副本|导入))*$/.test(scene.name))return '远控木马';
  return scene.name;
}
function sceneIntroduction(scene:Scene){
  if(scene.presetId==='nwpu-nsa-report' && scene.description.startsWith('依据用户上传的希潭实验室'))return '本案例展示针对西北工业大学的网络入侵过程，涵盖匿名基础设施准备、境外跳板中转、边界设备入侵、浏览器攻击、内网渗透及信息回传，并标注各阶段涉及的匿迹技术与子技术。';
  return scene.description;
}
function Editor({ data, lang }: { data: IndexData; lang: string }) {
  const location = useLocation(),
    navigate = useNavigate();
  const [scene, setScene] = useState(() => blankScene(data));
  const sceneRef = useRef(scene);
  sceneRef.current = scene;
  const [hovered,setHovered]=useState<TechniqueHoverTarget|null>(null);
  const [ready, setReady] = useState(false),
    [selection, setSelection] = useState<Selection>(null),
    [picker, setPicker] = useState(false),
    [message, setMessage] = useState(""),
    [error, setError] = useState(""),
    [saveState, setSaveState] = useState("正在加载草稿…");
  const [paletteQuery, setPaletteQuery] = useState(""),
    [tab, setTab] = useState<"elements" | "layers">("elements"),
    [tool, setTool] = useState<"select" | "hand" | "connect">("select"),
    [relation, setRelation] = useState("control"),
    [draftList, setDraftList] = useState<Scene[] | null>(null);
  const history = useRef<Scene[]>([]),
    future = useRef<Scene[]>([]);
  const [historyVersion, bumpHistory] = useState(0);
  const flow = useRef<ReactFlowInstance<FlowNode, FlowEdge> | null>(null),
    canvas = useRef<HTMLDivElement>(null),
    file = useRef<HTMLInputElement>(null);
  const readyRef = useRef(false),
    lastRoute = useRef("");
  const queuedFit = useRef(false);
  const selectedNode =
    selection?.kind === "node"
      ? scene.nodes.find((n) => n.id === selection.id)
      : undefined;
  const selectedEdge =
    selection?.kind === "edge"
      ? scene.edges.find((e) => e.id === selection.id)
      : undefined;
  const selected = selectedNode || selectedEdge;
  const hoverBindings = hovered ? scene.bindings.filter(b=>b.target.kind===hovered.kind&&b.target.id===hovered.id) : [];
  function showTechniqueHover(event:{clientX:number;clientY:number;buttons:number},kind:'node'|'edge',id:string,name:string){
    if(event.buttons||tool!=='select'||picker||draftList||!sceneRef.current.bindings.some(b=>b.target.kind===kind&&b.target.id===id))return;
    setHovered({kind,id,name,x:event.clientX,y:event.clientY});
  }
  useEffect(()=>{setHovered(null);},[scene.id,tool,picker,draftList]);
  useEffect(()=>{const dismiss=(event:KeyboardEvent)=>{if(event.key==='Escape')setHovered(null);};window.addEventListener('keydown',dismiss);return()=>window.removeEventListener('keydown',dismiss);},[]);

  const remember = useCallback(() => {
    history.current.push(structuredClone(sceneRef.current));
    if (history.current.length > 80) history.current.shift();
    future.current = [];
    bumpHistory((v) => v + 1);
  }, []);
  function edit(fn: (draft: Scene) => void, record = true) {
    if (record) remember();
    const next = structuredClone(sceneRef.current);
    fn(next);
    updateAutomaticAnchors(next);
    next.updatedAt = new Date().toISOString();
    sceneRef.current = next;
    setScene(next);
    setSaveState("待保存");
  }
  async function persist(snapshot = sceneRef.current) {
    try {
      await saveDraft(parseScene(snapshot));
      setError((previous) =>
        previous.startsWith("草稿保存失败") ? "" : previous,
      );
      if (sceneRef.current === snapshot) setSaveState("已保存到本机浏览器");
      return true;
    } catch (e) {
      setSaveState("保存失败");
      setError(`草稿保存失败，请导出 JSON 备份。${String(e)}`);
      return false;
    }
  }
  function initialViewport(document: Scene) {
    if(!document.nodes.length)return document.viewport;
    const boxes=document.nodes.map(n=>({...absolutePosition(n,document.nodes),...n.size}));
    const minX=Math.min(...boxes.map(b=>b.x)),minY=Math.min(...boxes.map(b=>b.y));
    const width=Math.max(...boxes.map(b=>b.x+b.width))-minX,height=Math.max(...boxes.map(b=>b.y+b.height))-minY;
    const area=canvas.current?.getBoundingClientRect();const w=area?.width||1000,h=area?.height||700;
    const zoom=Math.max(.1,Math.min(1,w/(width*1.12),h/(height*1.12)));
    return {x:(w-width*zoom)/2-minX*zoom,y:(h-height*zoom)/2-minY*zoom,zoom};
  }
  function replaceScene(next: Scene, fit = false) {
    updateAutomaticAnchors(next, true);
    history.current = [];
    future.current = [];
    bumpHistory((v) => v + 1);
    setSelection(null);
    setPicker(false);
    sceneRef.current = next;
    setScene(next);
    setSaveState("待保存");
    flow.current?.setViewport(next.viewport);
    queuedFit.current = fit;
  }
  useEffect(() => {
    let cancelled = false;
    async function load() {
      const key = location.pathname;
      if (lastRoute.current === key) return;
      lastRoute.current = key;
      // A preset redirects to the draft already in memory. Re-reading IndexedDB
      // here can overwrite edits made while that initial snapshot is saving.
      if (readyRef.current && key === `/simulation/draft/${sceneRef.current.id}`) {
        setReady(true);
        return;
      }
      const previous = sceneRef.current;
      if (readyRef.current && !(await persist(previous))) {
        lastRoute.current = "";
        return;
      }
      setReady(false);
      try {
        const presetId = key.startsWith("/simulation/preset/")
          ? decodeURIComponent(key.split("/")[3] || "")
          : null;
        if (presetId) {
          const entry = catalog.find((c) => c.id === presetId);
          if (!entry) throw new Error("未找到该预置场景");
          const loader = sceneFiles[`../../../scenes/${entry.file}`];
          if (!loader) throw new Error("预置场景文件缺失");
          const original = parseScene(await loader());
          const time = new Date().toISOString();
          const next = {
            ...original,
            viewport: initialViewport(original),
            id: newId("scene"),
            presetId: entry.id,
            name: original.name,
            createdAt: time,
            updatedAt: time,
          };
          if (!cancelled) {
            replaceScene(next, true);
            setMessage("预置场景已作为可编辑副本打开，原文件保持不变。");
            await saveDraft(next);
            navigate(`/simulation/draft/${next.id}`, { replace: true });
          }
        } else if (key.startsWith("/simulation/draft/")) {
          const id = decodeURIComponent(key.split("/")[3] || "");
          const saved = (await drafts()).find((s) => s.id === id);
          if (!saved)
            throw new Error(
              "当前浏览器中未找到这个草稿，请通过 JSON 导入或重新打开预置场景。",
            );
          if (!cancelled) replaceScene(saved);
        } else if (!readyRef.current) {
          const saved = await activeDraft();
          if (!cancelled) {
            replaceScene(saved || blankScene(data));
            if (saved) setMessage("已恢复上次的本地草稿。");
          }
        }
      } catch (e) {
        if (!cancelled) {
          setError(String(e));
          if (!readyRef.current) replaceScene(blankScene(data));
        }
      } finally {
        if (!cancelled) {
          readyRef.current = true;
          setReady(true);
        }
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, [location.pathname]);
  useEffect(() => {
    if (!ready) return;
    const timer = setTimeout(() => persist(scene), 450);
    return () => clearTimeout(timer);
  }, [scene, ready]);
  useEffect(
    () => () => {
      if (readyRef.current) void persist(sceneRef.current);
    },
    [],
  );
  useEffect(() => {
    const hide = () => {
      if (readyRef.current && document.visibilityState === "hidden")
        void persist(sceneRef.current);
    };
    document.addEventListener("visibilitychange", hide);
    return () => document.removeEventListener("visibilitychange", hide);
  }, []);
  function undo() {
    if (!history.current.length) return;
    future.current.push(structuredClone(sceneRef.current));
    const next = history.current.pop()!;
    updateAutomaticAnchors(next);
    next.updatedAt = new Date().toISOString();
    sceneRef.current = next;
    setScene(next);
    setSelection(null);
    bumpHistory((v) => v + 1);
    flow.current?.setViewport(next.viewport);
  }
  function redo() {
    if (!future.current.length) return;
    history.current.push(structuredClone(sceneRef.current));
    const next = future.current.pop()!;
    updateAutomaticAnchors(next);
    next.updatedAt = new Date().toISOString();
    sceneRef.current = next;
    setScene(next);
    setSelection(null);
    bumpHistory((v) => v + 1);
    flow.current?.setViewport(next.viewport);
  }
  function deleteSelected() {
    if (!selection) return;
    edit((draft) => Object.assign(draft, removeObjects(draft, selection)));
    setSelection(null);
  }
  useEffect(() => {
    const key = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      if (
        target.closest('input,textarea,select,dialog,[contenteditable="true"]')
      )
        return;
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") {
        e.preventDefault();
        e.shiftKey ? redo() : undo();
      } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
        e.preventDefault();
        persist();
      } else if (e.key === "Delete" || e.key === "Backspace") {
        e.preventDefault();
        deleteSelected();
      }
    };
    window.addEventListener("keydown", key);
    return () => window.removeEventListener("keydown", key);
  }, [selection, historyVersion]);
  const bindingCount = (kind: "node" | "edge", id: string) =>
    scene.bindings.filter((b) => b.target.kind === kind && b.target.id === id)
      .length;
  const nodes: FlowNode[] = useMemo(
    () =>
      orderedNodes(scene.nodes).map((n) => ({
        id: n.id,
        type: "entity",
        position: n.position,
        parentId: n.parentId,
        measured: { width: n.size.width, height: n.size.height },
        style: {
          width: n.size.width,
          height: n.size.height,
          zIndex: n.container ? 0 : 2,
        },
        zIndex: n.container ? 0 : 2,
        selected: selection?.kind === "node" && selection.id === n.id,
        data: {
          name: n.name,
          subtitle:n.subtitle, entityClass:n.entityClass, borderColor:n.borderColor,
          kind: n.kind,
          color: n.color,
          container: n.container,
          count: bindingCount("node", n.id),
          onResizeStart: remember,
        },
      })),
    [scene.nodes, scene.bindings, selection, remember],
  );
  const edges: FlowEdge[] = useMemo(
    () =>
      scene.edges.map((e) => ({
        id: e.id,
        type: "relation",
        source: e.source,
        target: e.target,
        sourceHandle: e.sourcePort,
        targetHandle: e.targetPort,
        selected: selection?.kind === "edge" && selection.id === e.id,
        reconnectable: selection?.kind === "edge" && selection.id === e.id,
        markerEnd:
          e.direction === "none"
            ? undefined
            : {
                type: MarkerType.ArrowClosed,
                color: e.color,
                width: 17,
                height: 17,
              },
        markerStart:
          e.direction === "both"
            ? {
                type: MarkerType.ArrowClosed,
                color: e.color,
                width: 17,
                height: 17,
              }
            : undefined,
        data: { edge: e, count: bindingCount("edge", e.id) },
      })),
    [scene.edges, scene.bindings, selection],
  );
  function changeNodes(changes: NodeChange<FlowNode>[]) {
    const relevant = changes.filter(
      (c) => c.type === "position" || (c.type === "dimensions" && c.resizing),
    );
    if (!relevant.length) return;
    edit((d) => {
      for (const c of relevant) {
        if (!("id" in c)) continue;
        const n = d.nodes.find((n) => n.id === c.id);
        if (!n) continue;
        if (c.type === "position" && c.position) n.position = c.position;
        if (c.type === "dimensions" && c.dimensions)
          n.size = { width: c.dimensions.width, height: c.dimensions.height };
      }
    }, false);
  }
  function addNode(kind: string, point?: { x: number; y: number }) {
    const item = palette.find((p) => p.kind === kind);
    if (!item) return;
    const bounds = canvas.current?.getBoundingClientRect();
    const pos = point ||
      flow.current?.screenToFlowPosition({
        x: (bounds?.left || 0) + (bounds?.width || 600) / 2 - 75,
        y: (bounds?.top || 0) + (bounds?.height || 400) / 2 - 50,
      }) || { x: 100, y: 100 };
    const node: SceneNode = {
      id: newId("node"),
      kind: item.kind,
      category: item.category,
      name: item.name,
      position: pos,
      size: {
        width: "container" in item ? 380 : 150,
        height: "container" in item ? 260 : 100,
      },
      color: "#ffffff",
      notes: "",
      container: "container" in item,
      ...("entityClass" in item ? {entityClass:item.entityClass}: {}),
    };
    edit((d) => {
      d.nodes.push(node);
    });
    setSelection({ kind: "node", id: node.id });
    setTool("select");
  }
  function connect(c: Connection) {
    if (!c.source || !c.target) return;
    const e: SceneEdge = {
      id: newId("edge"),
      source: c.source,
      target: c.target,
      sourcePort: (c.sourceHandle || "right") as SceneEdge["sourcePort"],
      targetPort: (c.targetHandle || "left") as SceneEdge["targetPort"],
      name: relations[relation],
      relation,
      direction: "forward",
      lineStyle:
        relation === "internet"
          ? "dashed"
          : relation === "social"
            ? "dotted"
            : "solid",
      routing: "bezier",
      color: "#657c70",
      notes: "",
      waypoints: [],
      anchorMode: "manual",
    };
    edit((d) => {
      d.edges.push(e);
    });
    setSelection({ kind: "edge", id: e.id });
  }
  function reconnect(edge: FlowEdge, connection: Connection) {
    if (!connection.source || !connection.target) return;
    edit(draft => {
      const current = draft.edges.find(item => item.id === edge.id);
      if (!current) return;
      current.source = connection.source;
      current.target = connection.target;
      current.sourcePort = (connection.sourceHandle || 'right') as SceneEdge['sourcePort'];
      current.targetPort = (connection.targetHandle || 'left') as SceneEdge['targetPort'];
      current.anchorMode = 'manual';
      // Old absolute bend points would preserve the old detour after reconnection.
      current.waypoints = [];
      delete current.labelPosition;
    });
    setSelection({kind:'edge',id:edge.id});
  }
  function setProperty(key: string, value: unknown) {
    if (!selection) return;
    edit((d) => {
      const item =
        selection.kind === "node"
          ? d.nodes.find((n) => n.id === selection.id)
          : d.edges.find((e) => e.id === selection.id);
      if (item) Object.assign(item, { [key]: value });
    });
  }
  function setParent(parentId: string) {
    if (!selectedNode) return;
    edit((d) => {
      const n = d.nodes.find((n) => n.id === selectedNode.id)!;
      const pos = absolutePosition(n, d.nodes);
      if (!parentId) {
        delete n.parentId;
        n.position = pos;
      } else {
        const parent = d.nodes.find((n) => n.id === parentId)!;
        const origin = absolutePosition(parent, d.nodes);
        n.parentId = parentId;
        n.position = {
          x: Math.max(
            16,
            Math.min(parent.size.width - n.size.width - 16, pos.x - origin.x),
          ),
          y: Math.max(
            52,
            Math.min(parent.size.height - n.size.height - 16, pos.y - origin.y),
          ),
        };
      }
    });
  }
  function possibleParents() {
    if (!selectedNode) return [];
    return scene.nodes.filter((n) => {
      if (!n.container || n.id === selectedNode.id) return false;
      let p = n.parentId;
      while (p) {
        if (p === selectedNode.id) return false;
        p = scene.nodes.find((n) => n.id === p)?.parentId;
      }
      return true;
    });
  }
  async function newScene() {
    if (!(await persist())) return;
    replaceScene(blankScene(data));
    navigate("/simulation");
    setMessage("已新建空白画布，原场景已保存在本地草稿。");
  }
  async function importFile(f: File) {
    try {
      if (f.size > 8 * 1024 * 1024) throw new Error("场景文件不能超过 8 MB");
      const next = parseScene(JSON.parse(await f.text()));
      if (!(await persist())) return;
      next.id = newId("scene");
      next.name = next.name + " · 导入";
      next.updatedAt = new Date().toISOString();
      replaceScene(next);
      navigate("/simulation");
      setMessage("导入成功，已作为独立草稿保存。");
      setError("");
    } catch (e) {
      setError(`导入失败：${String(e)}`);
    }
  }
  function exportFile() {
    try {
      const valid = parseScene(sceneRef.current);
      const blob = new Blob([JSON.stringify(valid, null, 2)], {
        type: "application/json",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download =
        (valid.name.replace(/[\\/:*?"<>|]/g, "-") || "未命名场景") +
        ".niji-scene.json";
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      setMessage("已导出完整场景 JSON，可重新导入继续编辑。");
    } catch (e) {
      setError(String(e));
    }
  }
  function applyBindings(ids: string[]) {
    if (!selection) return;
    const target = selection;
    edit((d) => {
      d.bindings = d.bindings.filter(
        (b) =>
          b.target.kind !== target.kind ||
          b.target.id !== target.id ||
          ids.includes(b.matrixRef),
      );
      for (const id of ids)
        if (
          !d.bindings.some(
            (b) =>
              b.target.kind === target.kind &&
              b.target.id === target.id &&
              b.matrixRef === id,
          )
        )
          d.bindings.push({
            id: newId("binding"),
            target: { ...target },
            matrixRef: id,
            applicationNote: "",
            basis: "hypothesis",
            evidenceRefs: [],
          });
    });
    setPicker(false);
  }
  function updateBinding(id: string, changes: Partial<Binding>) {
    edit((d) => {
      const b = d.bindings.find((b) => b.id === id);
      if (b) Object.assign(b, changes);
    });
  }
  const notices = warnings(scene, data);
  const bound = selection
    ? scene.bindings.filter(
        (b) => b.target.kind === selection.kind && b.target.id === selection.id,
      )
    : [];
  function menu(category: "threat" | "case", label: string) {
    return (
      <details
        className="sim-catalog"
        onMouseEnter={(e) => {
          e.currentTarget.open = true;
        }}
        onMouseLeave={(e) => {
          if (!e.currentTarget.contains(document.activeElement))
            e.currentTarget.open = false;
        }}
        onBlur={(e) => {
          if (
            !e.currentTarget.contains(e.relatedTarget as globalThis.Node | null)
          )
            e.currentTarget.open = false;
        }}
      >
        <summary>
          {label}
          <ChevronDown size={13} />
        </summary>
        <div className="sim-catalog-popover">
          {catalog
            .filter((c) => c.category === category)
            .map((c) => (
              <button
                key={c.id}
                onClick={async (e) => {
                  e.currentTarget.closest("details")?.removeAttribute("open");
                  if (location.pathname === `/simulation/preset/${c.id}`) {
                    if (!(await persist())) return;
                    const loader = sceneFiles[`../../../scenes/${c.file}`];
                    const original = parseScene(await loader());
                    replaceScene(
                      {
                        ...original,
                        id: newId("scene"),
                        presetId: c.id,
                        name: original.name,
                        updatedAt: new Date().toISOString(),
                      },
                      true,
                    );
                  } else navigate(`/simulation/preset/${c.id}`);
                }}
              >
                <strong>{c.name}</strong>
                
              </button>
            ))}
        </div>
      </details>
    );
  }
  return (
    <div className={`sim-app ${scene.views?.length ? "sim-report-scene" : ""}`}>
      <div className="sim-toolbar">
        <div className="sim-heading">
          <h1>高隐蔽网络公害仿真系统</h1>
          <input
            aria-label="场景名称"
            value={sceneDisplayName(scene)}
            onChange={(e) =>
              edit((d) => {
                d.name = e.target.value;
              })
            }
            maxLength={300}
          />
          {scene.presetId && <span className="sim-copy-tag">可编辑副本</span>}
        </div>
        <div className="sim-actions">
          {menu("threat", "典型公害")}
          {menu("case", "典型案例")}
          <span className="sim-action-divider" />
          <button
            title="撤销 Ctrl+Z"
            aria-label="撤销"
            disabled={!history.current.length}
            onClick={undo}
          >
            <Undo2 size={17} />
          </button>
          <button
            title="重做 Ctrl+Shift+Z"
            aria-label="重做"
            disabled={!future.current.length}
            onClick={redo}
          >
            <Redo2 size={17} />
          </button>
          <button onClick={newScene}>
            <FilePlus2 size={16} />
            新建
          </button>
          <button
            onClick={async () => {
              if (await persist())
                drafts()
                  .then(setDraftList)
                  .catch((e) => setError(String(e)));
            }}
          >
            <FolderOpen size={16} />
            草稿
          </button>
          <button onClick={() => persist()}>
            <Save size={16} />
            保存
          </button>
          <button onClick={() => file.current?.click()}>
            <Upload size={16} />
            导入
          </button>
          <button onClick={exportFile}>
            <Download size={16} />
            导出
          </button>
          <input
            hidden
            ref={file}
            type="file"
            accept=".json,application/json"
            aria-label="导入场景文件"
            onChange={(e) => {
              const f = e.target.files?.[0];
              if (f) importFile(f);
              e.target.value = "";
            }}
          />
        </div>
      </div>
      {error && (
        <div className="sim-error" role="alert">
          {error}
          <button aria-label="关闭错误提示" onClick={() => setError("")}>
            <X size={14} />
          </button>
        </div>
      )}
      <div className="sim-workspace">
        <aside className="sim-palette">
          <div className="sim-tabs">
            <button
              className={tab === "elements" ? "active" : ""}
              onClick={() => setTab("elements")}
            >
              元素库
            </button>
            <button
              className={tab === "layers" ? "active" : ""}
              onClick={() => setTab("layers")}
            >
              图层
            </button>
          </div>
          {tab === "elements" ? (
            <>
              <label className="sim-palette-search">
                <Search size={15} />
                <input
                  aria-label="搜索画布元素"
                  placeholder="搜索元素…"
                  value={paletteQuery}
                  onChange={(e) => setPaletteQuery(e.target.value)}
                />
              </label>
              {(["human", "cloud", "endpoint", "auxiliary"] as const).map((category) => (
                <section className="sim-palette-section" key={category}>
                  <h2>{categoryNames[category]}</h2>
                  <div className="sim-palette-grid">
                    {palette
                      .filter(
                        (p) =>
                          p.category === category &&
                          p.name
                            .toLowerCase()
                            .includes(paletteQuery.toLowerCase()),
                      )
                      .map((item) => (
                        <button
                          key={item.kind}
                          draggable
                          aria-label={`添加${item.name}`}
                          onDragStart={(e) => {
                            e.dataTransfer.setData(
                              "application/niji-element",
                              item.kind,
                            );
                            e.dataTransfer.effectAllowed = "copy";
                          }}
                          onClick={() => addNode(item.kind)}
                          title={`拖到画布，或点击添加${item.name}`}
                        >
                          <item.icon size={23} />
                          <span>{item.name}</span>
                        </button>
                      ))}
                  </div>
                </section>
              ))}
              <section className="sim-palette-section">
                <h2>网</h2>
                <div className="sim-relations">
                  {Object.entries(relations).map(([key, label]) => (
                    <button
                      key={key}
                      className={
                        tool === "connect" && relation === key ? "active" : ""
                      }
                      onClick={() => {
                        setRelation(key);
                        setTool("connect");
                      }}
                    >
                      <span className={`sim-line-preview ${key}`} />{" "}
                      <span>{label}</span>
                    </button>
                  ))}
                </div>
              </section>
            </>
          ) : (
            <div className="sim-layer-list">
              {scene.nodes.map((n) => (
                <button
                  className={selection?.id === n.id ? "active" : ""}
                  key={n.id}
                  onClick={() => {
                    setSelection({ kind: "node", id: n.id });
                    flow.current?.fitView({
                      nodes: [{ id: n.id }],
                      padding: 0.8,
                      maxZoom: 1.2,
                    });
                  }}
                >
                  {n.parentId ? "↳ " : ""}
                  {n.name}
                </button>
              ))}
              {scene.edges.map((e) => (
                <button
                  key={e.id}
                  className={selection?.id === e.id ? "active" : ""}
                  onClick={() => setSelection({ kind: "edge", id: e.id })}
                >
                  <Link2 size={13} />
                  {e.name}
                </button>
              ))}
              {!scene.nodes.length && <p>画布中还没有元素</p>}
            </div>
          )}
        </aside>
        <div
          className="sim-canvas"
          ref={canvas}
          onDragOver={(e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = "copy";
          }}
          onDrop={(e) => {
            e.preventDefault();
            addNode(
              e.dataTransfer.getData("application/niji-element"),
              flow.current?.screenToFlowPosition({
                x: e.clientX,
                y: e.clientY,
              }),
            );
          }}
        >
          {ready ? (
            <ReactFlow<FlowNode, FlowEdge>
              key={scene.id}
              nodes={nodes}
              edges={edges}
              nodeTypes={nodeTypes}
              edgeTypes={edgeTypes}
              onInit={(instance) => {
                flow.current = instance;
                instance.setViewport(sceneRef.current.viewport);
                if (queuedFit.current) {
                  queuedFit.current = false;
                  setTimeout(
                    () => instance.fitView({ padding: 0.2, maxZoom: 1 }),
                    100,
                  );
                }
              }}
              onNodesChange={changeNodes}
              onNodeDragStart={()=>{setHovered(null);remember();}}
              onNodeMouseEnter={(event,node)=>showTechniqueHover(event,'node',node.id,node.data.name)}
              onNodeMouseLeave={()=>setHovered(null)}
              onEdgeMouseEnter={(event,edge)=>showTechniqueHover(event,'edge',edge.id,edge.data!.edge.name)}
              onEdgeMouseLeave={()=>setHovered(null)}
              onMoveStart={()=>setHovered(null)}
              onConnectStart={()=>setHovered(null)}
              onReconnectStart={()=>setHovered(null)}
              onNodeClick={(_, node) => {setHovered(null);setSelection({kind:"node",id:node.id});}}
              onEdgeClick={(_, edge) => {setHovered(null);setSelection({kind:"edge",id:edge.id});}}
              onPaneClick={() => setSelection(null)}
              onConnect={connect}
              onReconnect={reconnect}
              edgesReconnectable={tool !== "hand"}
              reconnectRadius={12}
              onMoveEnd={(_, viewport) => {
                if (
                  JSON.stringify(viewport) !==
                  JSON.stringify(sceneRef.current.viewport)
                )
                  edit((d) => {
                    d.viewport = viewport;
                  }, false);
              }}
              connectionMode={ConnectionMode.Loose}
              nodesDraggable={tool !== "hand"}
              nodesConnectable={tool !== "hand"}
              elementsSelectable={tool !== "hand"}
              panOnDrag={tool === "hand" ? [0, 1, 2] : [1, 2]}
              selectionOnDrag={tool === "select"}
              deleteKeyCode={null}
              minZoom={0.1}
              maxZoom={3}
              defaultViewport={scene.viewport}
              fitView={false}
            >
              <Background id="scene-grid-minor" variant={BackgroundVariant.Lines} gap={scene.viewport.zoom < .3 ? 120 : 24} lineWidth={0.5} color="#e1e9e3" />
              <Background id="scene-grid-major" variant={BackgroundVariant.Lines} gap={scene.viewport.zoom < .3 ? 600 : 120} lineWidth={0.8} color="#cbd9cf" />
              <Controls showInteractive={false} />
              <MiniMap
                pannable
                zoomable
                nodeColor={(n) =>
                  n.data.color === "#ffffff"
                    ? "#dce9e0"
                    : String(n.data.color || "#dce9e0")
                }
                nodeStrokeColor="#a7beaf"
                nodeBorderRadius={4}
                maskColor="rgba(244,247,245,.75)"
              />
            </ReactFlow>
          ) : (
            <div className="sim-loading">正在加载场景…</div>
          )}
          <div className="sim-canvas-tools">
            <button
              aria-label="选择工具"
              aria-pressed={tool === "select"}
              className={tool === "select" ? "active" : ""}
              onClick={() => setTool("select")}
            >
              <MousePointer2 size={18} />
            </button>
            <button
              aria-label="平移工具"
              aria-pressed={tool === "hand"}
              className={tool === "hand" ? "active" : ""}
              onClick={() => setTool("hand")}
            >
              <Hand size={18} />
            </button>
            <button
              aria-label="连线工具"
              aria-pressed={tool === "connect"}
              className={tool === "connect" ? "active" : ""}
              onClick={() => setTool("connect")}
            >
              <Link2 size={18} />
            </button>
            <button
              aria-label="适应画布"
              onClick={() =>
                flow.current?.fitView({ padding: 0.2, maxZoom: 1 })
              }
            >
              <LocateFixed size={18} />
            </button>
          </div>
          {!!scene.views?.length && <div className="sim-scene-views"><label>场景视图<select aria-label="场景视图" defaultValue="" key={scene.id} onChange={e=>{const view=scene.views?.find(v=>v.id===e.target.value);flow.current?.fitView({nodes:view?.nodeIds.map(id=>({id})),padding:0.12,maxZoom:1});}}><option value="">全景</option>{scene.views.map(view=><option key={view.id} value={view.id}>{view.name}</option>)}</select></label><button onClick={()=>{setSelection(null);setMessage(sceneIntroduction(scene));}}>案例说明</button></div>}
          <SceneLegend scene={scene}/>
          {tool === "connect" && (
            <div className="sim-tool-hint">
              {relations[relation]} · 从实体连接点拖动到另一个实体
            </div>
          )}
          {ready && !scene.nodes.length && (
            <div className="sim-blank">
              <Layers size={34} />
              <h2>从一张白板开始</h2>
              <p>拖入左侧元素，连接关系，关联匿迹技战术。</p>
              <span>也可以从上方选择典型公害或典型案例</span>
            </div>
          )}
        </div>
        <aside className={`sim-inspector ${selected ? "has-selection" : ""}`}>
          <div className="sim-inspector-title">
            <strong>
              {selectedNode
                ? "实体属性"
                : selectedEdge
                  ? "连线属性"
                  : "场景信息"}
            </strong>
            {selected && (
              <button aria-label="取消选择" onClick={() => setSelection(null)}>
                <X size={16} />
              </button>
            )}
          </div>
          {selected ? (
            <>
              <div className="sim-inspector-section">
                <span className="sim-type-label">
                  {selectedNode
                    ? `${categoryNames[selectedNode.category]} / ${palette.find((p) => p.kind === selectedNode.kind)?.name}`
                    : relations[selectedEdge!.relation]}
                </span>
                <label>
                  名称
                  <input
                    aria-label="对象名称"
                    value={selected.name}
                    onChange={(e) => setProperty("name", e.target.value)}
                    maxLength={300}
                  />
                </label>
                <label>
                  颜色
                  <div className="sim-colors">
                    {(selectedEdge
                      ? ["#657c70", "#12745d", "#56718a", "#927047", "#8e5555"]
                      : swatches
                    ).map((color) => (
                      <button
                        key={color}
                        aria-label={`颜色 ${color}`}
                        aria-pressed={selected.color === color}
                        style={{ background: color }}
                        onClick={() => setProperty("color", color)}
                      />
                    ))}
                    <input
                      aria-label="自定义颜色"
                      type="color"
                      value={selected.color}
                      onChange={(e) => setProperty("color", e.target.value)}
                    />
                  </div>
                </label>
                {selectedNode && (
                  <label>
                    所属容器
                    <select
                      aria-label="所属容器"
                      value={selectedNode.parentId || ""}
                      onChange={(e) => setParent(e.target.value)}
                    >
                      <option value="">画布根层级</option>
                      {possibleParents().map((n) => (
                        <option key={n.id} value={n.id}>
                          {n.name}
                        </option>
                      ))}
                    </select>
                  </label>
                )}
                {selectedEdge && (
                  <>
                    <label>
                      关系类型
                      <select
                        aria-label="关系类型"
                        value={selectedEdge.relation}
                        onChange={(e) =>
                          setProperty("relation", e.target.value)
                        }
                      >
                        {Object.entries(relations).map(([key, label]) => (
                          <option key={key} value={key}>
                            {label}
                          </option>
                        ))}
                      </select>
                    </label>
                    <div className="sim-endpoints">
                      <span>起点</span>
                      <strong>
                        {
                          scene.nodes.find((n) => n.id === selectedEdge.source)
                            ?.name
                        }
                      </strong>
                      <span>终点</span>
                      <strong>
                        {
                          scene.nodes.find((n) => n.id === selectedEdge.target)
                            ?.name
                        }
                      </strong>
                    </div>
                    <div className="sim-field-pair">
                      <label>起点锚点<select aria-label="起点锚点" value={selectedEdge.sourcePort} onChange={e=>edit(d=>{const edge=d.edges.find(item=>item.id===selectedEdge.id)!;edge.sourcePort=e.target.value as SceneEdge['sourcePort'];edge.anchorMode='manual';edge.waypoints=[];delete edge.labelPosition;})}>{Object.entries({top:'上方',right:'右侧',bottom:'下方',left:'左侧'}).map(([value,label])=><option key={value} value={value}>{label}</option>)}</select></label>
                      <label>终点锚点<select aria-label="终点锚点" value={selectedEdge.targetPort} onChange={e=>edit(d=>{const edge=d.edges.find(item=>item.id===selectedEdge.id)!;edge.targetPort=e.target.value as SceneEdge['targetPort'];edge.anchorMode='manual';edge.waypoints=[];delete edge.labelPosition;})}>{Object.entries({top:'上方',right:'右侧',bottom:'下方',left:'左侧'}).map(([value,label])=><option key={value} value={value}>{label}</option>)}</select></label>
                    </div>
                    <button className="sim-optimize-anchors" onClick={()=>edit(d=>{const edge=d.edges.find(item=>item.id===selectedEdge.id)!;edge.anchorMode='auto';edge.waypoints=[];delete edge.labelPosition;})}>自动优化锚点</button>
                    <p className="sim-muted">选中连线后，拖动两端的圆点可更换实体或锚点。{selectedEdge.anchorMode==='auto'?'当前随布局自动调整。':'当前保留手动锚点。'}</p>
                    <div className="sim-field-pair">
                      <label>
                        线型
                        <select
                          aria-label="线型"
                          value={selectedEdge.lineStyle}
                          onChange={(e) =>
                            setProperty("lineStyle", e.target.value)
                          }
                        >
                          <option value="solid">实线</option>
                          <option value="dashed">虚线</option>
                          <option value="dotted">点线</option>
                        </select>
                      </label>
                      <label>
                        方向
                        <select
                          aria-label="方向"
                          value={selectedEdge.direction}
                          onChange={(e) =>
                            setProperty("direction", e.target.value)
                          }
                        >
                          <option value="forward">单向</option>
                          <option value="both">双向</option>
                          <option value="none">无方向</option>
                        </select>
                      </label>
                    </div>
                    <label>
                      路径
                      <select
                        aria-label="路径"
                        value={selectedEdge.routing}
                        onChange={(e) => setProperty("routing", e.target.value)}
                      >
                        <option value="bezier">曲线</option>
                        <option value="step">折线</option>
                        <option value="straight">直线</option>
                      </select>
                    </label>
                    <details className="sim-waypoints">
                      <summary>
                        路径控制点（{selectedEdge.waypoints.length}）
                      </summary>
                      {selectedEdge.waypoints.map((point, i) => (
                        <div className="sim-waypoint" key={i}>
                          {(["x", "y"] as const).map((axis) => (
                            <label key={axis}>
                              {axis}
                              <input
                                type="number"
                                aria-label={`控制点 ${i + 1} ${axis}`}
                                value={point[axis]}
                                onChange={(e) => {
                                  const value = Number(e.target.value);
                                  if (
                                    Number.isFinite(value) &&
                                    Math.abs(value) <= 1000000
                                  )
                                    setProperty(
                                      "waypoints",
                                      selectedEdge.waypoints.map((p, j) =>
                                        i === j ? { ...p, [axis]: value } : p,
                                      ),
                                    );
                                }}
                              />
                            </label>
                          ))}
                          <button
                            aria-label={`删除控制点 ${i + 1}`}
                            onClick={() =>
                              setProperty(
                                "waypoints",
                                selectedEdge.waypoints.filter(
                                  (_, j) => j !== i,
                                ),
                              )
                            }
                          >
                            <X size={13} />
                          </button>
                        </div>
                      ))}
                      <button
                        onClick={() => {
                          if (selectedEdge.waypoints.length >= 30) return;
                          const n = scene.nodes.find(
                            (n) => n.id === selectedEdge.source,
                          )!;
                          const p = absolutePosition(n, scene.nodes);
                          setProperty("waypoints", [
                            ...selectedEdge.waypoints,
                            { x: p.x + 200, y: p.y + 100 },
                          ]);
                        }}
                      >
                        添加控制点
                      </button>
                    </details>
                  </>
                )}
                <label>
                  备注
                  <textarea
                    aria-label="对象备注"
                    value={selected.notes}
                    onChange={(e) => setProperty("notes", e.target.value)}
                  />
                </label>
              </div>
              <SceneEvidence scene={scene} provenance={selected.provenance} attributes={selectedNode?.attributes} data={data} lang={lang}/>
              <div className="sim-inspector-section">
                <h3>
                  关联匿迹技战术 <span>{bound.length}</span>
                </h3>
                {bound.map((b) => (
                  <div className="sim-bound-item" key={b.id}>
                    <div className="sim-bound-title">
                      <Link
                        target="_blank"
                        rel="noreferrer"
                        to={`/objects/${b.matrixRef}`}
                      >
                        {data.objects[b.matrixRef]
                          ? title(data.objects[b.matrixRef], lang)
                          : "未解析技术"}
                        <code>{b.matrixRef}</code>
                      </Link>
                      <button
                        aria-label={`移除关联 ${b.matrixRef}`}
                        onClick={() =>
                          edit((d) => {
                            d.bindings = d.bindings.filter(
                              (item) => item.id !== b.id,
                            );
                          })
                        }
                      >
                        <X size={13} />
                      </button>
                    </div>
                    <label>
                      依据
                      <select
                        aria-label={`${b.matrixRef} 关联依据`}
                        value={b.basis}
                        onChange={(e) =>
                          updateBinding(b.id, {
                            basis: e.target.value as Binding["basis"],
                          })
                        }
                      >
                        <option value="hypothesis">场景假设</option>
                        <option value="inference">分析推断</option>
                        <option value="fact">有证据事实</option>
                      </select>
                    </label>
                    <label>
                      应用说明
                      <textarea
                        aria-label={`${b.matrixRef} 应用说明`}
                        value={b.applicationNote}
                        onChange={(e) =>
                          updateBinding(b.id, {
                            applicationNote: e.target.value,
                          })
                        }
                      />
                    </label>
                    <label>
                      证据引用
                      <input
                        aria-label={`${b.matrixRef} 证据引用`}
                        placeholder="REF-000001, CASE-000001"
                        value={b.evidenceRefs.join(", ")}
                        onChange={(e) =>
                          updateBinding(b.id, {
                            evidenceRefs: e.target.value
                              .split(/[,，\s]+/)
                              .filter(Boolean),
                          })
                        }
                      />
                    </label>
                    <div className="sim-binding-sources">
                      {b.evidenceRefs.map((ref, i) => {
                        const source = scene.sources.find(item => item.id === ref);
                        const record = data.objects[ref];
                        return source || record ? <SceneSourceLink key={`${ref}-${i}`} data={data} lang={lang}
                          source={source || { id: ref, title: title(record, lang), matrixRef: ref }} /> : null;
                      })}
                    </div>
                  </div>
                ))}
                {!bound.length && (
                  <p className="sim-muted">尚未关联技术或子技术</p>
                )}
                <button
                  className="sim-add-binding"
                  onClick={() => setPicker(true)}
                >
                  <Plus size={16} />
                  添加技术 / 子技术
                </button>
              </div>
              <div className="sim-inspector-section">
                <h3>关联关系</h3>
                {(selectedNode
                  ? scene.edges.filter(
                      (e) =>
                        e.source === selectedNode.id ||
                        e.target === selectedNode.id,
                    )
                  : [selectedEdge!]
                ).map((e) => (
                  <button
                    className="sim-related-edge"
                    key={e.id}
                    onClick={() => setSelection({ kind: "edge", id: e.id })}
                  >
                    {scene.nodes.find((n) => n.id === e.source)?.name} →{" "}
                    {scene.nodes.find((n) => n.id === e.target)?.name}
                    <span>{e.name}</span>
                  </button>
                ))}
                <button className="sim-delete" onClick={deleteSelected}>
                  <Trash2 size={15} />
                  {selectedNode?.container
                    ? "删除容器及内部元素"
                    : "删除选中对象"}
                </button>
              </div>
            </>
          ) : (
            <div className="sim-inspector-section sim-scene-overview">
              <h2>{sceneDisplayName(scene)}</h2>
              <p className="sim-scene-introduction">{sceneIntroduction(scene)||'暂无场景简介。可添加实体和连线，开始构建场景。'}</p>
              <div className="sim-scene-stats">
                <span><strong>{scene.nodes.length}</strong> 实体</span>
                <span><strong>{scene.edges.length}</strong> 连线</span>
                <span><strong>{scene.bindings.length}</strong> 技术关联</span>
              </div>
            </div>
          )}
          {selected && !!notices.length && (
            <div className="sim-warnings" role="status">
              <strong>关联核对</strong>
              {notices.map((n) => (
                <p key={n}>{n}</p>
              ))}
            </div>
          )}
        </aside>
      </div>
      <div className="sim-status">
        <span role="status">
          {message || "点击或拖拽元素开始建模"}
          {message && (
            <button aria-label="关闭状态提示" onClick={() => setMessage("")}>
              <X size={12} />
            </button>
          )}
        </span>
        <span>{saveState}</span>
      </div>
      {hovered && hoverBindings.length>0 && <TechniqueHover target={hovered} bindings={hoverBindings} data={data} lang={lang}/>}
      {picker && selection && selected && (
        <TechniquePicker
          data={data}
          lang={lang}
          targetName={selected.name}
          existing={bound.map((b) => b.matrixRef)}
          onApply={applyBindings}
          onClose={() => setPicker(false)}
        />
      )}
      {draftList && (
        <DraftDialog
          items={draftList}
          onClose={() => setDraftList(null)}
          onLoad={async (next) => {
            if (!(await persist())) return;
            replaceScene(parseScene(next));
            setDraftList(null);
            navigate("/simulation");
            setMessage("已打开本地草稿。");
          }}
        />
      )}
    </div>
  );
}
function DraftDialog({
  items,
  onClose,
  onLoad,
}: {
  items: Scene[];
  onClose: () => void;
  onLoad: (scene: Scene) => void;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    ref.current?.showModal();
    return () => ref.current?.close();
  }, []);
  return (
    <dialog
      ref={ref}
      className="sim-drafts"
      aria-labelledby="sim-draft-title"
      onCancel={onClose}
    >
      <div className="sim-picker-heading">
        <h2 id="sim-draft-title">本地草稿</h2>
        <button aria-label="关闭草稿列表" onClick={onClose}>
          <X size={18} />
        </button>
      </div>
      <p>草稿保存在当前浏览器，导出 JSON 可备份或转移到其他设备。</p>
      <div className="sim-draft-list">
        {items.map((s) => (
          <button key={s.id} onClick={() => onLoad(s)}>
            <strong>{s.name}</strong>
            <span>
              {s.nodes.length} 实体 · {s.edges.length} 连线 ·{" "}
              {new Date(s.updatedAt).toLocaleString("zh-CN")}
            </span>
          </button>
        ))}
      </div>
    </dialog>
  );
}
