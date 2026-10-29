# BATCH-TA0003-012 人工审查局部整改记录

2026-09-12 审计确认 NJT-0092 父级、两个镜像变量和 image identity—content—instance 防御链成立，但子技术场景、攻防模型和限制过短。整改逐项扩充 tag→digest 解析、缓存/pull policy、多架构 manifest、registry actor、签名/SBOM、deployment/template、node pull、instance first action 与跨镜像寿命保留；复用 REF-000211、214、215 的审计、runtime event 与签名 admission，不制造无合格来源的 Case。两个子项升级到 1.0.0 并保持 `review`。
