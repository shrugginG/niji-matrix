import {
  Binoculars, PackagePlus, DoorOpen, SquareTerminal, Anchor,
  ShieldPlus, EyeOff, ShieldOff, KeyRound, ScanSearch,
  Waypoints, FolderDown, RadioTower, FileOutput, Zap,
} from 'lucide-react';

// Canonical tactic IDs keep the same visual meaning across every entry point.
const tacticIcons = {
  TA0043: Binoculars,     // 目标侦查：望远镜
  TA0042: PackagePlus,    // 攻击准备：资源包
  TA0001: DoorOpen,       // 初始入侵：入口
  TA0002: SquareTerminal,// 攻击执行：命令终端
  TA0003: Anchor,         // 入侵维持：锚定
  TA0004: ShieldPlus,     // 权限提升：权限盾牌
  TA0005: EyeOff,         // 行动隐匿：隐藏观察
  TA0112: ShieldOff,      // 防御削弱：失效防护
  TA0006: KeyRound,       // 凭据获取：钥匙
  TA0007: ScanSearch,     // 环境测绘：扫描发现
  TA0008: Waypoints,      // 横向渗透：节点路径
  TA0009: FolderDown,     // 信息收集：归集文件
  TA0011: RadioTower,     // 命令控制：通信塔
  TA0010: FileOutput,     // 数据渗出：文件传出
  TA0040: Zap,            // 影响释放：闪电冲击
};

export function TacticIcon({id, size = 18}: {id: string; size?: number}) {
  const Icon = tacticIcons[id as keyof typeof tacticIcons];
  return Icon ? <Icon className="tactic-icon" data-tactic={id} size={size}
    strokeWidth={1.65} aria-hidden="true" focusable="false" /> : null;
}
