# Relationships

本目录保存需要独立证据、描述或生命周期的跨对象关系，例如：

- 案例主体 `uses` 某项技术；
- 检测策略 `detects` 某项技术；
- 缓解措施 `mitigates` 某项技术；
- 一个对象 `replaces` 已废弃对象。

战术归属和技术—匿迹子技术父子关系已经分别由 `tactic_refs` 和 `parent_ref` 显式保存，编译器可以自动生成对应 STIX relationship；只有关系本身需要额外说明或证据时，才在这里单独建档。

