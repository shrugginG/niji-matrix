# BATCH-TA0003-017 人工审查局部整改记录

2026-09-12 审计确认 NJT-0097 的两项变量与 NIST protect—detect—recover 防御链成立，但子技术威胁模型和硬件/网络观察边界过短。整改分别扩充实际 measurement coverage、firmware inventory/readback、flash/update actor、root-of-trust 与重启结果，以及 boot variable/source pointer、PXE/TFTP server、image hash、boot ID 与 running image；明确合法更新、换件、灾备和 netboot 反例。两个子项升级到 1.0.0 并保持 `review`。
