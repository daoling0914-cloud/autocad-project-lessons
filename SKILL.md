---
name: autocad-project-lessons
description: "创建、修改和交付 CAD 图纸及三维模型：Windows AutoCAD 原生 DWG、build123d/text-to-cad 参数建模与装配、二维 DXF 轮廓和模型派生工程 PDF。用于按图复绘、局改、机械零件、平面轮廓、三视图、尺寸公差及出图；融合项目经验与最终验收。仅查历史文件、泛泛解释 CAD 时不使用。"
license: MIT
metadata:
  version: "0.3.0"
---

# CAD 绘图、建模与交付

将经过项目回读和修订验证的经验用于当前任务。用户的本次要求优先；图幅、线宽、版本、图层名和对象数量均以本次输入为准，不能继承旧案例的参数。

## 先进入生产路线

对绘图或建模请求执行所需的建图、修改、导出和检查。先按 [生产流程](references/production-workflows.md) 判断本次应采用的路线，再读取下表对应的完整操作参考；只检查的请求直接进入相关验收章节。

| 需要产出的内容 | 生产入口与能力 |
| --- | --- |
| 原生 DWG，含可编辑文字、尺寸、建筑/工艺等二维图及局改 | [AutoCAD 生产路线](references/production-workflows.md#autocad-native)，使用现有 AutoCAD API/Core Console 和适用的 DXF 中间文件 |
| 参数化三维零件、装配、模型修改或 STEP/STL 等导出 | [CAD 建模完整参考](references/upstream/cad/guide.md)，及其中链接的建模、定位、导出与机构资料 |
| 二维切割轮廓、面板、垫片、几何展平及 DXF | [DXF 生成完整参考](references/upstream/dxf/guide.md)与[构造模板](references/upstream/dxf/references/generator-templates.md) |
| 由模型投影的视图、孔标注、尺寸和工程 PDF | [工程图完整参考](references/upstream/engineering-drawing/guide.md)与[Sheet API](references/upstream/engineering-drawing/references/sheet-api.md) |

三套生产指南已随包提供，调用本 skill 不需要另外找到或安装同名 skill。实际执行仍需对应软件运行时；参考 [第三方说明](THIRD_PARTY_NOTICES.md) 保留来源和许可证。

`assets/starter-project/` 提供可运行的双孔板示例：参数模型、同源轮廓、STEP/DXF 导出及投影 PDF。复制到本次工作目录后再运行、修改，不在已安装 skill 目录生成工程输出。示例尺寸只用于演示；复杂形状按本次要求编写，不把双孔板当通用模型。

## 从当前任务开始

先确认当前输入、指定修改范围、几何依据及交付格式；能从对话或文件确定的信息不重复询问。区分实尺寸绘图、参数示意、按图复绘与允许自主设计的部分；要求变化时按当前有效约定继续。任务、图形、视图、文件、页数分别计数。把影响正确性的缺项与可先执行的部分分开处理。

| 当前问题 | 按需读取 |
| --- | --- |
| 选择 Core Console、COM 或 .NET；进程卡住、布局报错 | [原生执行](references/native-execution.md) |
| 复绘、局部修订、块分解、图内尺寸、公差和拓扑 | [图形与修订质量](references/drawing-quality.md) |
| 中文字体、2004/2010 保存、打印比例、粗细线、PDF | [兼容与打印](references/compatibility-and-plotting.md) |
| 参数详图、实验分项、三视图、装配出图或整件编辑性 | [任务模式专项检查](references/task-specific-checks.md) |
| 想知道某条规则来自什么实际问题 | [去标识化经验案例](references/experience-cases.md) |
| 师兄的补充经验、合并去重及证据范围 | [融合来源与对照](references/source-notes.md) |

## 贯穿执行的关键判断

- 先检查原图的空间、单位、图层、块、外参和字体，再确定编辑方式。现有 DWG 的局部修改应保留主体几何及用户未要求变更的内容。
- 将修改前后数据、错误日志和临时 DXF 放入独立运行目录。检查本次新输出，避免上轮成功文件或残留完成标记掩盖失败。
- 交付可编辑 DWG 时，几何、文字和符号应有相应 CAD 对象；需要可编辑尺寸时保留原生尺寸对象。不能以粘贴整张图片代替复绘。
- 尺寸和形位公差要落到对应视图、要素和引线上。说明表只能补充；若用户明确要求无尺寸，则几何按约束绘制，交付图不加尺寸。
- 使用真实几何约束检验长度、角度、圆弧方向、相切、孔距和连接关系。对象数量或 `AUDIT` 成功不能单独证明图画对了。
- 保存后重新打开最终 DWG，执行原生审计，并从该文件回读关键属性或导出核验 DXF。再从最终文件打印 PDF，检查页面和局部细节。
- 若只能执行结构检查，明确记录“原生回读未执行”；若只能查看预览，不能声称已完成原生验证。推定尺寸及未核实的标准符合性也要准确说明。
- 验收报告应对应当前文件摘要及检查范围。原生曲线、尺寸、整件块/组、实体与图片的编辑能力不同；需要逐件编辑时，实际移开测试完整本体、原位残留及邻件影响。

## 验收随修改范围变化

| 请求 | 最有用的验证 |
| --- | --- |
| 只改姓名、日期、标题栏 | 指定文字更新；主体几何和块变换不变；DWG/PDF 同步 |
| 分解指定家具块 | 目标嵌套块已分解；位置、可见几何不变；其他块不动 |
| 修剖面、倒角、孔、圆角 | 修订处放大图；方向、半径、相切、投影对应关系 |
| 修尺寸、公差 | 原生测量值、尺寸覆盖文字、基准及引线落点；纸面可读性 |
| PDF 导出 | 原 DWG 未意外改变；页数、图幅、比例、裁切、线宽及字体 |
| 旧版 DWG 交付 | 实际文件头、重新打开后的文字和对象、原生审计 |
| 按实验或任务分项 | 任务到文件的映射、每份页数、整体覆盖与图序；空框是否符合模板任务 |

无需为小修订重建整套图，也无需重复已通过且未受影响的昂贵检查。

## 可复用交付检查

`scripts/check_delivery.py` 只读检查 DWG 文件头、PDF 页数/纸张尺寸、ZIP 内容与最终文件是否一致，并输出哈希。它不启动 AutoCAD，不检查几何、公差、字体外观或原生审计。

```powershell
python scripts/check_delivery.py --dwg final.dwg --dwg-version 2010 --pdf final.pdf --paper-mm 420 297 --pages 1 --zip delivery.zip --report delivery-checks.json
```

DWG/ZIP 检查仅依赖 Python 标准库；PDF 检查需要 `pypdf`。脚本未通过时先查看具体失败项，不把结构检查通过表述成整张图合格。

多任务 PDF 页数不一致时，按 [任务清单示例](assets/task-delivery.example.json) 填写实际路径和要求，再运行 `python scripts/check_delivery.py --plan task-delivery.json --report delivery-checks.json`。报告分别给出任务数、PDF 文件数和总页数；示例文件不代表实际任务已通过。

## 后续经验如何进入本 skill

发生新的实际失败或用户纠正后，先完成修复和验收，再按“触发条件 → 现象 → 已确认原因或待证假设 → 修复 → 独立验证 → 适用范围”更新相关参考。修正或合并已有规则，避免不断堆叠重复禁令。把确定性重复工作提取为脚本前，先确认它确实能跨案例复用。

公开版本仅收录去标识化的规则和自建示例；真实图纸、聊天、截图、字体文件、个人信息及本机证据记录不随包发布。保留引用或复用内容所需的许可证与来源。
