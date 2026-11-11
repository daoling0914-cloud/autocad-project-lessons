# 第三方来源与许可

v0.3.0 融合本机已安装的下列 text-to-cad 技能文档，来源仓库为 [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad)。快照日期为 2026-11-11，不声称对应某个未经核实的上游提交。

| 随附生产参考 | 原始许可 |
| --- | --- |
| [CAD 建模](references/upstream/cad/guide.md)及其 references | [MIT / Copyright 2026 Thompson Labs LLC](references/upstream/cad/LICENSE) |
| [DXF 生成](references/upstream/dxf/guide.md)及构造模板 | [MIT / Copyright 2026 Thompson Labs LLC](references/upstream/dxf/LICENSE) |
| [工程 PDF](references/upstream/engineering-drawing/guide.md)及 Sheet API | [MIT / Copyright 2026 Thompson Labs LLC](references/upstream/engineering-drawing/LICENSE) |

为避免嵌套技能被重复发现，三个入口由 `SKILL.md` 改名为 `guide.md`；相应内部链接从 `../SKILL.md` 改为 `../guide.md`。其余文档保留原有内容，许可证原样保留。各源文件与打包文件的摘要见 [upstream-manifest.json](references/upstream-manifest.json)。

上游指南的规则仅用于其对应技术路线。它们不会将 PDF 变为 DWG、赋予不存在的宿主工具，或使当前任务自动获得配置修改权限。本包不附带 text-to-cad/build123d/AutoCAD 的软件二进制；实际依赖保持各自许可。

本项目入口、衔接说明、经验整理及新增示例沿用根目录 [MIT License](LICENSE)。师兄提供的经验整理授权及其原包不在本次复制范围内的原文/代码边界，见 [融合来源说明](references/source-notes.md)。
