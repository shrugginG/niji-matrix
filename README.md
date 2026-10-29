# 匿迹技战术矩阵 · Niji Matrix

基于规范 YAML 的匿迹技战术知识库，以及用于矩阵浏览、知识关联和公害场景建模的 Web 系统。

- 在线展示：https://shrugging.github.io/niji-matrix/
- `niji-matrix/`：矩阵内容、Schema、作者规范和校验脚本。
- `niji-matrix-web/`：React + TypeScript Web、预置场景、场景文件规范及测试。

## 本地启动

需要 Node.js 22.12+（推荐 24）和 Python 3。

```bash
python3 -m pip install -r niji-matrix/requirements-dev.txt
cd niji-matrix-web
npm ci
npm run dev
```

默认地址 http://127.0.0.1:18091/。局域网访问可使用：

```bash
npm run dev -- --host 0.0.0.0 --port 18092
```

本地启动时校验 YAML 并生成数据，随后监听规范内容更新。

## GitHub Pages

推送到 `main` 后，GitHub Actions 安装 Node/Python 依赖、校验矩阵、生成静态 JSON、检查类型和场景合同，最后部署网站。构建失败不会替换已发布站点。

```bash
cd niji-matrix-web
VITE_BASE_PATH=/niji-matrix/ npm run build:pages
```

产物在 `dist-pages/`。Pages 使用 Hash 路由，例如 `/#/matrix`、`/#/objects/NJT-0001`，支持详情和章节链接刷新。只发布当前数据快照，不包含本地积累的历史快照。

网站与源码公开。场景草稿仍保存在访问者自己的浏览器 IndexedDB；迁移到新的域名或设备时，应通过 JSON 导出/导入。浏览器草稿地址不等于可供其他人访问的共享案例，公开预置案例可以通过其菜单入口打开。

预置事件基于所注明的公开报道整理，矩阵映射中的推断与不确定性保留在场景数据中。案例图片和引用资料的权利属于原作者；原始浏览器 HTML 捕获不纳入仓库，仅保留正文及图片材料和来源说明。本仓库未为第三方材料授予额外许可。

更多操作说明见 [Web README](niji-matrix-web/README.md)；内容规范见 [矩阵 README](niji-matrix/README.md)。
