# BATCH-TA0003-017 T1542 研究约束

- 固定 `enterprise-attack 19.1`；本批只处理 T1542，前序 T1653 全部门禁通过。
- 直接对象是操作系统接管前控制启动流的固件、启动记录/分区、ROM monitor 或网络启动配置，以及它们到 OS/设备运行结果的谱系。主机软件二进制、运行中系统镜像和普通自启动排除。
- 五项 ATT&CK 子项触发多轴检查，不按 system/component firmware、bootkit、ROMMON、TFTP 直接导入。正式变量必须改变度量覆盖或启动来源观察。
- 本批完成后仍只有固定基线前十七项完成；剩余五项与 Niji 原生缺口不在本轮，Persistence 不关闭。

