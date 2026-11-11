# CAD 绘图与交付 — AutoCAD Project Lessons

融合 CAD 生产流程与项目经验的 skill：原生 AutoCAD 绘图/改图、参数三维建模、二维 DXF 轮廓、模型派生工程 PDF，以及最终交付验收。

这是工作流知识的积累，不是模型参数微调。首版依据 AutoCAD 2021 项目整理；其他版本、字体与打印设备需要按实际环境核对。

v0.2.0 融合了师兄提供的 27 条经验：参数详图与实尺寸、实验任务拆分、三视图、装配爆炸、整件语义编辑，以及数据库资源、视口和字体补充。与首版重合的规则已归并。来源、感谢及证据范围见 [融合来源与对照](references/source-notes.md)。

v0.3.0 将之前安装的 `cad`、`dxf`、`engineering-drawing` 三套 MIT 技能的完整操作参考纳入同一个包，并加入模型、同源轮廓、STEP/DXF 导出和工程 PDF 的可运行示例。调用同一个技能名即可按任务进入生产路线，再使用已有经验检查结果。见 [生产流程](references/production-workflows.md) 和 [第三方许可说明](THIRD_PARTY_NOTICES.md)。

## 使用

把此文件夹放到当前 Codex 配置的 `skills` 目录；常见个人目录为 `~/.codex/skills/autocad-project-lessons`，项目级也可放到 `.agents/skills/autocad-project-lessons`。若配置了 `CODEX_HOME`，个人目录为其下的 `skills`。重新加载技能列表或新开聊天后，确认技能可见。

调用示例：

```text
使用 $autocad-project-lessons，只修改这张 DWG 的标题栏日期，保留主体几何，更新配套 PDF。
```

```text
使用 $autocad-project-lessons，检查这份 2004 版 DWG 的中文、原生尺寸及打印结果。
```

```text
使用 $autocad-project-lessons，按这张尺寸图建立参数化零件，交付 STEP 和带尺寸的工程 PDF。
```

入口为 [SKILL.md](SKILL.md)；详细案例在 [experience-cases.md](references/experience-cases.md)。自动匹配已启用。

## 环境与检查工具

实际 DWG 编辑、原生回读和打印需要可用的 AutoCAD，以及任务选用的 COM/.NET/LISP 管线。参数模型、几何 DXF 与模型派生 PDF 使用可用的 text-to-cad/build123d 运行时。完整技能文档已随包提供；软件二进制、AutoCAD SDK、商业字体和业务原图不随包分发。

将 `assets/starter-project/` 复制到本次工作目录后，可依次运行 `cad run plate.py`、`cad run exports.py`、`cad run plate_sheet.py`，在副本的 `output/` 生成双孔板示例 STEP、DXF 和工程 PDF。参数在 `plate.py` 中修改。不要在安装目录运行示例；示例也不表示 PDF 路线支持 DWG 导出。具体路线及限制见生产流程。

Python 检查工具对输入只读，只在指定 `--report` 时写报告；PDF 检查需要 `pypdf`，脚本不会自动安装依赖。

```powershell
python scripts/check_delivery.py --dwg final.dwg --dwg-version 2010 --pdf final.pdf --paper-mm 420 297 --pages 1 --zip delivery.zip --report delivery-checks.json
```

可重复提供 `--dwg` 或 `--pdf`；同次检查的版本、每份 PDF 的页数和每页纸张要求相同。不指定纸张或页数时仅记录实际值。ZIP 可使用子目录，但各预期文件的 basename 必须唯一。

多任务的页数或纸张不同时，使用 [任务清单示例](assets/task-delivery.example.json) 填写自己的任务映射：

```powershell
python scripts/check_delivery.py --plan task-delivery.json --report delivery-checks.json
```

清单模式分别检查每个任务 PDF，记录任务数、PDF 数和总页数；可附带整体 DWG 和 ZIP。它不自动解析任务书来判断是否漏项，也不根据正文文字多少拒绝有意的空白模板。清单路径与普通 `--dwg` / `--pdf` 模式互斥。

工具检查文件头签名、页数、纸张和 ZIP 一致性，**不验证 DWG 能否被 AutoCAD 打开，也不判断几何、字体外观、真实比例或制图规范**。

## 来源与许可

本包的 text-to-cad 生产参考按其 MIT 许可复制，保留 Thompson Labs LLC 的版权及许可文本；入口改名及链接适配详见 [第三方说明](THIRD_PARTY_NOTICES.md)。感谢师兄提供并允许公开整理后的经验；师兄原包代码或业务数据不在本次复制范围。与 [text-to-cad](https://github.com/earthtojake/text-to-cad) 等工具无隶属关系；不表示 Autodesk 或 OpenAI 认可本包。

本包随附 [MIT License](LICENSE)。如后续引入其他 skill、代码、模板或图片，须另行核实其授权并保留所需声明；当前许可证不能替第三方内容授权。真实业务图纸和聊天记录应留在项目中，社区案例使用自建或有发布授权的素材。

技能结构参考 [OpenAI 官方说明](https://developers.openai.com/plugins/build/skills)；仓库公开与开源授权的区别见 [GitHub 许可说明](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)。
