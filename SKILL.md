---
name: figure-router
description: 统一做图路由 skill。当用户需要任何形式的图——科研论文图（Nature/PNAS/NPJ 级数据图/晶体结构/谱图/TOC）、比赛或汇报 PPT 用图、前端参考图、产品装饰图、数据分析图表、架构/流程/示意图、AI 生成式配图、图标/插画/3D 素材——时触发。核心原则：能复用已有 skill/库就不造轮子，功能相当时选更好看的，数据图必须确定性矢量渲染、AI 禁入数据图。路由到数据图表、结构图、演示视觉、生成式视觉、材料化学科研图、AI 做图 MCP 六个分支，执行后端包括 doubao-visualization、archify、drawio、drawio-academic-skills、doubao-creative-design、seedream-50、gpt-image-prompt-engine、lark-slides-pro、SciencePlots、pyvista、pymatgen、hofmann、python-pptx、Slidev、Marp、mcp-server-chart 及本地克隆库（echarts/d3/antvis-x6/xyflow/rough/lucide/PptxGenJS）。
---

# figure-router — 统一做图路由

> **核心理念**: 不造轮子。所有做图需求先路由到已有 skill / 已收录库 / 已安装工具，功能相当时选更好看的。

---

## 1. 路由仲裁优先级与 Jev 极速快分流 (Fast-Path)

> ⚡ **Jev 亚秒级快路径 (推荐优先执行)**:  
> 遇到具体制图需求时，可先运行快路径分发脚本：  
> `python3 scripts/fast_route.py -q "<用户需求>"`  
> 若置信度 $\ge 0.85$（`FAST_PATH_HIT`），直接调起目标技能，**无需通读下方 200 行路由大表**，立省 2,000 Tokens 上下文！若置信度不足则回落至下方人工规则。

当多个工具都能做同一件事时，按以下优先级选路：

1. **输出目的地优先**
   - 论文/期刊投稿 → 矢量静态、确定性渲染
   - PPT/演示 → 可编辑、可嵌入
   - 网页/前端 → 可交互
   - 概念讲解/TOC/装饰 → AI 生成式

2. **复用已有优先** — 已装 skill / 已克隆库 / 已安装工具能做，就不引入新东西

3. **美学优先** — 功能差不多时，选更好看、更精致的那个（见 REGISTRY.md 各条目「美学」列）

4. **期刊级硬规则** — Nature/PNAS/NPJ 数据图：强制矢量 + SciencePlots 风格 + 色盲安全配色；AI 禁入数据图，仅用于示意图并标注 "schematic"

---

## 2. 六分支路由表

收到做图需求时，先判断属于哪个分支，再按分支内的路由规则选工具。

### 分支一：数据图表（统计/分析/科研曲线）

| 需求 | 首选工具 | 备选 |
|---|---|---|
| 顶会/顶刊基准对比、消融与雷达图 | **scientific-figure-making（figures4papers）** | matplotlib + SciencePlots |
| 论文数据图（Nature/PNAS/NPJ） | **matplotlib + SciencePlots**（venv） | paperplot 预检、cnsplots |
| 交互/网页数据图 | **doubao-visualization（ECharts）** | ECharts 本地库、pyecharts |
| Python 快速出图 | **pyecharts**（交互）或 plotnine（静态学术风） | — |
| 前端 React 项目 | **Recharts** | — |
| 完全自定义可视化 | **D3.js**（本地克隆） | — |
| AI 自动选图/快速探索 | **mcp-server-chart**（如已配置） | doubao-visualization |

**必读**: `docs/scientific-figure-spec.md`（论文级数据图规范）、`docs/python-env.md`（Python 环境）、`scientific-figure-making` 技能文档

### 分支二：结构图 / 示意图 / 架构图 / 白板

| 需求 | 首选工具 | 备选 |
|---|---|---|
| 技术工程图（架构/流程/时序/数据流/状态机） | **archify**（交互 HTML，9 项机器校验） | drawio |
| 论文/出版级示意图 | **drawio + drawio-academic-skills** | archify |
| 专利附图（发明框图/实用新型部件序号引出线/外观正投影/CAD视角） | **patent-disclosure-skill**（含部件引出、线稿组合、规范流程图） | drawio-academic-skills |
| 手绘风/草稿/讲解图/架构草图 | **handraw-style（手绘风全系方案）** | Mermaid (handDrawn) / draw.io (sketch) / rough.js / Excalidraw / D2 |
| 文档内嵌快速图 | **Mermaid**（支持 `look: handDrawn`） | — |
| 复杂架构图（美学优先） | **D2**（支持 `sketch: true`） | archify |
| 云架构/技术栈图 | **Python diagrams** | drawio |
| 前端可编辑节点图 | **antvis-x6** 或 **xyflow**（本地克隆） | — |

**手绘风专指**: 涉及手绘草图/白板涂鸦风图表系统、硬性参数配置（jiggle/roughness/hachure）与代码片段，详阅 [`references/handraw-style.md`](references/handraw-style.md)。
**必读**: `REGISTRY.md` 分支二各条目

### 分支三：演示与交付视觉（PPT / 幻灯片 / 信息图）

| 需求 | 首选工具 | 备选 |
|---|---|---|
| 比赛答辩 / 视觉冲击 / 技术演讲 | **Slidev**（npx） | reveal.js |
| 学术汇报 / 组会 / 答辩（简洁） | **Marp**（npx） | LaTeX Beamer |
| 数据驱动 / 批量生成 PPT | **python-pptx**（venv） | PptxGenJS（本地克隆） |
| 整套飞书幻灯片交付 | **lark-slides-pro** | — |
| PPT 中的数据图 | matplotlib + SciencePlots 生成矢量图后嵌入 | ECharts（HTML 演示时） |

**必读**: `docs/presentation-tools.md`（演示工具完整指南）

### 分支四：生成式视觉 / 图标 / 插画 / 3D 素材 / 装饰图

| 需求 | 首选工具 | 备选 |
|---|---|---|
| AI 生图（海报/主视觉/概念图） | **seedream-50** 或 **doubao-creative-design** | — |
| 生图提示词优化 | **gpt-image-prompt-engine** | — |
| 知识讲解配图（概念/机制/流程） | **doubao-visualization（生成式配图）** | seedream-50 |
| 图片后期（增强/擦除/去背景） | **byted-mediakit-image** | — |
| 图标 | **Lucide**（本地克隆，首选） | Heroicons |
| 插画/装饰 | **unDraw**（扁平可改色）、**3dicons**（3D 元素） | storyset（需署名） |
| 3D 渲染素材 | **Poly Haven** + ambientCG | — |

**硬规则**:
- AI 生成的图用于论文时必须标注 "schematic / AI-generated illustration"；数据图禁 AI。
- **文字渲染实事求是（严禁中文乱码偏见）**：现代 ChatGPT Image (GPT-4o/DALL-E 3) 等模型已全面支持高精度中文字符排版与笔画渲染。生成提示词时严禁抱有“中文无法生成/必然严重幻觉”的陈旧偏见。用户或场景需要中文时，坚决输出包含精准中文字样与排版规范的提示词（或全中文提示词），严禁擅自说教、劝退或私自篡改为英文。
**必读**: 涉及生图提示词结构化工程、多方案异构采样、防四宫格拼图及高精度中文字符渲染规范时，参阅 [`references/gpt-image-prompt-engine.md`](references/gpt-image-prompt-engine.md) 或调用 `gpt-image-prompt-engine`。

### 分支五：材料化学与科研出版图

| 需求 | 首选工具 | 备选 |
|---|---|---|
| 晶体/分子结构图（论文级） | **VESTA**（用户已装，高质量导出） | hofmann（代码自动化） |
| 晶体结构图（代码/批量） | **hofmann**（venv，pip 即用） | pyvista |
| 3D 渲染/体数据 | **pyvista**（venv） | VESTA |
| 能带/态密度/相图/Pourbaix | **pymatgen**（venv）+ matplotlib | — |
| 谱图（XRD/XPS/FTIR/Raman） | **matplotlib + SciencePlots** | — |
| 显微图标注（SEM/TEM/AFM） | **doubao-visualization（原图标注）** | Inkscape（外部） |
| 机理/反应路径示意图 | **drawio + drawio-academic-skills** | AI 生成（标注 schematic） |
| TOC/Graphical Abstract | **seedream-50** + 后期精修 | doubao-creative-design |
| 分子/化学结构 | **RDKit**（按需安装） | PyMOL（外部） |

**必读**: `docs/scientific-figure-spec.md`、`docs/vesta-integration.md`、`docs/python-env.md`

### 分支六：AI 做图 MCP / 专用 Skill

| 需求 | 首选工具 | 备选 |
|---|---|---|
| AI 自动做数据图（自然语言→图） | **mcp-server-chart**（如已配置 MCP） | doubao-visualization（ECharts） |
| 多后端统一图表 | **flint-mcp** | mcp-server-chart |
| 快速数据探索仪表盘 | **viz-mcp** | mcp-server-chart |
| 科研图 AI 工作流参考 | sci-figure-workflow / Icarus Figures | 方法论参考，不直接集成 |

**必读**: `docs/mcp-server-chart-setup.md`

---

## 3. 执行流程

收到做图需求时，按以下步骤执行：

1. **判断收益**: 用户明确要求做图 → 触发；任务含数据关系/结构/概念/动态变化且图示增益 → 触发。文字已足够 → 只回答文字。

2. **选分支**: 按第 2 节路由表判断属于哪个分支（可多分支组合）。

3. **选工具**: 在分支内按「路由仲裁优先级」（第 1 节）选具体工具。先查 REGISTRY.md 确认工具状态（已装/待装/登记）。

4. **加载规范**: 命中论文/科研图 → 读 `docs/scientific-figure-spec.md`；命中晶体结构 → 读 `docs/vesta-integration.md`；命中 PPT → 读 `docs/presentation-tools.md`；命中 Python → 确认用 `~/.local/figure-router-venv/bin/python`；命中 MCP → 读 `docs/mcp-server-chart-setup.md`。

5. **生成**: 按选定工具的规范生成。Python 代码统一用 venv 的 Python。AI 生图遵守数据图禁令。

6. **验证**:
   - 论文图：矢量格式、尺寸/字体/配色符合规范、数据可追溯
   - PPT 图：矢量嵌入、风格一致、投影可读
   - 交互图：在浏览器中验证渲染和交互
   - AI 图：标注 schematic（如用于论文）

7. **交付**: 说明产物路径、格式、使用方式。论文图标注数据来源和规范遵循情况。

---

## 4. 现有资产速查

### 已安装 Skill（直接触发）

| Skill | 用途 |
|---|---|
| scientific-figure-making | 顶会顶刊(Nature MI/ICML/NeurIPS/ECCV) Python 插图规范与实战脚本库 |
| doubao-visualization | ECharts 数据图 / 原图标注 / HTML-SVG 交互 / 生成式配图 |
| archify | 架构/流程/时序/数据流/状态机 → 交互 HTML |
| drawio | YAML-first 离线绘图，全类型图 |
| drawio-academic-skills | drawio 的学术出版叠加层（论文/学位论文/IEEE/camera-ready） |
| doubao-creative-design | 商业创意图/海报/Banner/主视觉 |
| seedream-50 | 高质量文生图 |
| gpt-image-prompt-engine | 生图提示词优化（530+ 模板） |
| byted-mediakit-image | 图片增强/擦除/去背景/OCR |
| lark-slides-pro | 飞书幻灯片创建/编辑 |
| lark-whiteboard | 白板/协作图 |

### 已安装 Python 包（venv: `~/.local/figure-router-venv`）

| 包 | 版本 | 用途 |
|---|---|---|
| matplotlib | 3.11.1 | 基础绘图 |
| SciencePlots | 最新 | Nature/IEEE/Science 期刊风格 |
| pymatgen | 2026.5.4 | 材料信息学（结构/相图/能带） |
| pyvista | 0.48.4 | 3D 科学可视化（VTK） |
| hofmann | 最新 | 轻量晶体结构可视化 |
| python-pptx | 1.0.2 | 程序化生成 PPTX |

### 已克隆本地库（`~/Documents/projects/`）

echarts、d3、antvis-x6、xyflow（React Flow）、rough（手绘风）、lucide（图标）、PptxGenJS

### 外部工具（用户已装 / 登记）

VESTA（晶体结构可视化，用户已在用）、Inkscape（矢量后期，如已装）

---

## 5. 参考文件

- **`REGISTRY.md`** — 完整工具注册表（50+ 工具，含 Stars/License/美学/能力/调用路径/状态）
- **`docs/scientific-figure-spec.md`** — 科研出版图完整规范（Nature/PNAS/NPJ 级）
- **`docs/vesta-integration.md`** — VESTA 对接与导出规范
- **`docs/python-env.md`** — Python 环境与包清单
- **`docs/presentation-tools.md`** — 演示工具使用指南（Slidev/Marp/python-pptx）
- **`docs/mcp-server-chart-setup.md`** — MCP Server Chart 配置指南

---

## 6. 硬规则（不可违反）

1. **数据图禁 AI**: 含坐标/数值/统计关系的图必须确定性渲染（matplotlib/ECharts/D3），禁止 AI 生成
2. **AI 图标注**: AI 生成的示意图/TOC/装饰图用于论文时，必须标注 "schematic" 或 "AI-generated illustration"
3. **论文图矢量**: Nature/PNAS/NPJ 投稿图必须矢量格式（PDF/EPS/SVG），位图 ≥300 DPI
4. **色盲安全**: 论文图配色必须色盲安全（Okabe-Ito/viridis），禁用 jet/rainbow
5. **不造轮子**: 已有 skill/库/工具能做就不引入新东西；功能相当时选更好看的
6. **Python 环境统一**: 所有 Python 出图代码用 `~/.local/figure-router-venv/bin/python`，不用系统 Python 或沙箱 Python
7. **不编造**: 工具/库/数据必须真实可查，不确定的宁可不收录也不能虚构
8. **文字渲染实事求是**: 现代生图模型已全面支持中文文字精准排版。严禁 AI 自以为是地宣称“无法生成中文”或以“中文幻觉严重”为由强行替换为英文。用户要中文就出中文，准确执行。

---

*figure-router v0.1 | 2026-08-30 | 统一做图路由，不造轮子，选好看的*
