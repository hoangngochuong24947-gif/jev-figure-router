# figure-router 工具与素材注册表

> **版本**: v0.1 (2026-08-30)
> **定位**: figure-router 路由 skill 的核心注册表——所有做图工具、库、素材、规范的单一事实源。
> **使用方式**: 收到做图需求时，先按「路由仲裁优先级」选路，再在对应分支查找工具，按「集成类型」调用。

---

## 0. 路由仲裁优先级（当多个工具都能做同一件事时）

1. **输出目的地优先**
   - 论文/期刊投稿 → 矢量静态、确定性渲染（matplotlib/SciencePlots/drawio-academic）
   - PPT/演示 → 可编辑、可嵌入（Slidev/Marp/python-pptx/PptxGenJS）
   - 网页/前端 → 可交互（ECharts/D3/archify HTML）
   - 概念讲解/TOC/装饰 → AI 生成式（seedream/creative-design/prompt-engine）

2. **复用已有优先** — 已装 skill / 已克隆库能做，就不引入新东西

3. **美学优先** — 功能差不多时，选更好看、更精致的那个（见各条目「美学」列）

4. **期刊级硬规则** — Nature/PNAS/NPJ 数据图：强制矢量输出 + SciencePlots 风格 + 色盲安全配色；AI 禁入数据图，仅用于示意图并标注 "schematic"

---

## 1. 集成类型说明

| 类型 | 标记 | 说明 | 调用方式 |
|---|---|---|---|
| **Skill** | `[SKILL]` | 已安装的 agent skill，可直接触发 | 按 skill 描述触发 |
| **文档** | `[DOC]` | 使用指南/风格规范/期刊要求，写成 markdown | 读取对应 docs/ 文件 |
| **代码库** | `[CODE]` | pip/npm 包或本地克隆 repo | 注册表里写最小可用示例 |
| **MCP/服务** | `[MCP]` | MCP 服务器或需部署的服务 | 按部署配置调用 |
| **外部工具** | `[EXT]` | 桌面应用/闭源软件，登记对接路径 | 调用本地安装或导出文件 |

---

## 2. 分支一：数据图表（统计/分析/科研曲线）

### 核心轮子

| 名称 | 类型 | Stars | License | 美学 | 能力 | 调用路径 | 状态 |
|---|---|---|---|---|---|---|---|
| **Apache ECharts** | `[CODE]` | 66.8k | Apache 2.0 | ★★★★★ | 20+ 图表类型，交互最强，Canvas/WebGL | 本地克隆 `~/Documents/projects/echarts`；或 npm/CDN；doubao-visualization 已封装 | ✅ 已有 |
| **Chart.js** | `[CODE]` | 67.5k | MIT | ★★★★ | 8 种基础图表，轻量 Canvas | npm/CDN；简单快速需求首选 | ⬜ 待引入 |
| **D3.js** | `[CODE]` | 113.2k | ISC | ★★★★ | 自定义 SVG 可视化底层，无限可能 | 本地克隆 `~/Documents/projects/d3`；需要完全自定义时用 | ✅ 已有 |
| **SciencePlots** | `[CODE]`+`[DOC]` | ~4k | MIT | ★★★★★ | Nature/IEEE/Science 期刊 matplotlib 风格，色盲安全配色 | `pip install SciencePlots` + `plt.style.use(['science','nature'])`；已装入 figure-router-venv | ✅ 已有 |
| **figures4papers (scientific-figure-making)** | `[SKILL]`+`[CODE]` | 5.2k | CC-BY-NC 4.0 | ★★★★★ | 耶鲁刘晨顶会顶刊插图集(Nature MI/ICML/NeurIPS/ECCV)；消融透明度、超宽布局、独立图例、雷达图 | 直接触发 `scientific-figure-making` skill；源码 `~/Documents/projects/figures4papers` | ✅ 已有 |
| **Recharts** | `[CODE]` | 27k | MIT | ★★★★ | React SVG 图表，前端项目用 | npm；仅前端项目需要时 | ⬜ 按需 |
| **Altair** | `[CODE]` | 10k | BSD-3 | ★★★★ | 声明式图表语法（Vega-Lite Python 端） | pip；统计分析优雅表达 | ⬜ 按需 |
| **plotnine** | `[CODE]` | 4.8k | MIT | ★★★★ | R ggplot2 的 Python 实现，语法优雅 | pip；习惯 ggplot 语法时 | ⬜ 按需 |
| **pyecharts** | `[CODE]` | ~15k | MIT | ★★★★★ | Python 版 ECharts，国内数据分析常用 | pip；Python 出交互图 | ⬜ 待引入 |
| **paperplot** | `[CODE]` | — | MIT | ★★★★ | 期刊栏宽精确尺寸，Type-42 字体，APS/Nature 预检 | pip；投稿前预检用 | ⬜ 按需 |
| **cnsplots** | `[CODE]` | — | MIT | ★★★★ | Cell/Nature/Science 风格，多面板图 | pip；CNS 级多面板 | ⬜ 按需 |

### 路由规则
- **论文数据图** → SciencePlots + matplotlib（矢量 PDF），顶会基准对比与消融实验首选 **scientific-figure-making**
- **交互/网页数据图** → ECharts（已有），复杂自定义 → D3
- **Python 快速出图** → pyecharts（交互）或 plotnine（静态学术风）
- **前端 React 项目** → Recharts

---

## 3. 分支二：结构图 / 示意图 / 架构图 / 白板

### 核心轮子

| 名称 | 类型 | Stars | License | 美学 | 能力 | 调用路径 | 状态 |
|---|---|---|---|---|---|---|---|
| **archify** | `[SKILL]` | — | MIT | ★★★★ | 架构/流程/时序/数据流/状态机→独立 HTML，9 项机器校验 | 直接触发 archify skill；技术工程图首选 | ✅ 已有 |
| **drawio** | `[SKILL]`+`[EXT]` | 39k+ | Apache 2.0 | ★★★★ | YAML-first 离线绘图，全类型图，300dpi PNG/PDF/SVG | 直接触发 drawio skill；需 draw.io Desktop 导出 | ✅ 已有 |
| **drawio-academic-skills** | `[SKILL]` | — | MIT | ★★★★★ | drawio 的学术出版叠加层，预检期刊/配色/公式/打印目标 | 作为 drawio 的 sibling overlay 安装；论文示意图首选 | ⬜ 待安装 |
| **Excalidraw** | `[CODE]`+`[EXT]` | 116k+ | MIT | ★★★★★ | 手绘风图/白板，可编辑工程，风格独特 | npm/自托管/Web；草稿/讲解/手绘风示意图 | ⬜ 待引入 |
| **handraw-style** | `[REF]` | — | MIT | ★★★★★ | 手绘风全系规范：Mermaid(handDrawn)/drawio(sketch)/rough.js/Excalidraw/D2 | 详阅 `references/handraw-style.md`；手绘/草图/白板风首选 | ✅ 已有 |
| **Mermaid** | `[CODE]` | 75k+ | MIT | ★★★ | 代码→15+ 图类型，GitHub 原生支持（支持 look: handDrawn） | CLI/JS/Markdown 内嵌；文档内嵌快速图 | ⬜ 按需 |
| **D2** | `[CODE]` | ~15k | MPL-2.0 | ★★★★ | 现代架构图 DSL，比 Mermaid 好看，支持 sketch: true | CLI；复杂架构图，美学优于 Mermaid | ⬜ 待引入 |
| **Python diagrams** | `[CODE]` | ~38k | MIT | ★★★ | Python→云架构图，200+ 云图标 | pip；云架构/技术栈图 | ⬜ 按需 |
| **rough.js** | `[CODE]` | — | MIT | ★★★★ | 手绘风 SVG 生成 | 本地克隆 `~/Documents/projects/rough`；Excalidraw 风格的代码实现 | ✅ 已有 |
| **antvis-x6** | `[CODE]` | — | MIT | ★★★★ | 图编辑引擎，节点式交互图 | 本地克隆 `~/Documents/projects/antvis-x6`；需要可编辑节点图时 | ✅ 已有 |
| **xyflow (React Flow)** | `[CODE]` | — | MIT | ★★★★ | React 节点图，前端交互 | 本地克隆 `~/Documents/projects/xyflow`；前端节点式 UI | ✅ 已有 |

### 路由规则
- **技术工程图（架构/流程/时序/数据流）** → archify（交互 HTML）或 drawio（可编辑文件）
- **论文/出版级示意图** → drawio + drawio-academic-skills 叠加层
- **手绘风/草稿/讲解图/白板涂鸦** → **handraw-style**（文档内嵌用 Mermaid handDrawn，架构用 draw.io sketch / D2，SVG 编程用 rough.js）
- **文档内嵌快速图** → Mermaid
- **复杂架构图（美学优先）** → D2
- **云架构/技术栈图** → Python diagrams
- **前端可编辑节点图** → antvis-x6 或 xyflow

---

## 4. 分支三：演示与交付视觉（PPT / 幻灯片 / 信息图）

### 核心轮子

| 名称 | 类型 | Stars | License | 美学 | 能力 | 调用路径 | 状态 |
|---|---|---|---|---|---|---|---|
| **Slidev** | `[CODE]` | ~30k | MIT | ★★★★★ | Markdown→交互式 HTML 幻灯片，Vue 组件，代码高亮，主题丰富 | npm init slidev；比赛答辩/技术演讲首选 | ⬜ 待引入 |
| **Marp** | `[CODE]` | — | MIT | ★★★★ | Markdown→PPTX/PDF/HTML，极简，多主题（含学术风） | npm/marp-cli；学术汇报/简洁演示首选 | ⬜ 待引入 |
| **python-pptx** | `[CODE]` | — | MIT | ★★★ | Python 程序化生成 PPTX，与数据分析流水线衔接 | pip；批量/数据驱动 PPT | ⬜ 待安装 |
| **PptxGenJS** | `[CODE]` | — | — | ★★★ | JS 生成 PPTX | 本地克隆 `~/Documents/projects/PptxGenJS`；Node 端生成 PPT | ✅ 已有 |
| **reveal.js** | `[CODE]` | ~67k | MIT | ★★★★ | HTML 幻灯片，动画最强 | npm；需要复杂动画/网页演示 | ⬜ 按需 |
| **lark-slides-pro** | `[SKILL]` | — | — | ★★★★ | 飞书幻灯片创建/编辑 | 直接触发；整套 PPT 组装交付 | ✅ 已有 |
| **slidev-templates** | `[CODE]` | — | MIT | ★★★★★ | 高质量 Slidev 模板集合（neko-style 技术演讲风） | GitHub 克隆；Slidev 模板参考 | ⬜ 按需 |
| **marp-pptx** | `[CODE]` | — | — | ★★★★ | Marp 学术主题 + PPTX 导出，含 TMU 学术绿/Beamer 风 | GitHub；学术汇报模板 | ⬜ 按需 |

### 比赛风 vs 学术汇报风

| 维度 | 比赛风（Slidev） | 学术汇报风（Marp/Beamer） |
|---|---|---|
| 配色 | 高对比、品牌色、撞色 | 低饱和、蓝/灰、克制 |
| 动画 | 转场/动效/交互 | 无动画，静态 PDF |
| 封面 | 视觉冲击、大图、slogan | 简洁标题+作者+单位 |
| 数据页 | 大字号、突出关键数字 | 小而精、图表严谨、引用标注 |
| 输出 | HTML/PDF | PPTX/PDF |
| 首选工具 | Slidev + slidev-templates | Marp + marp-pptx 或 LaTeX Beamer |

### 路由规则
- **整套 PPT 交付** → lark-slides-pro（飞书原生）或 Slidev/Marp（独立文件）
- **比赛答辩/视觉冲击** → Slidev（交互/动画/主题）
- **学术汇报/组会/答辩** → Marp（简洁 PPTX）或 Beamer（LaTeX 标准）
- **数据驱动/批量 PPT** → python-pptx 或 PptxGenJS
- **PPT 中的图表** → 走分支一（数据图表）生成后嵌入

---

## 5. 分支四：生成式视觉 / 图标 / 插画 / 3D 素材 / 装饰图

### 核心轮子

| 名称 | 类型 | Stars | License | 美学 | 能力 | 调用路径 | 状态 |
|---|---|---|---|---|---|---|---|
| **doubao-creative-design** | `[SKILL]` | — | — | ★★★★ | 商业/社交媒体创意图，海报/Banner/主视觉 | 直接触发；商业创意图首选 | ✅ 已有 |
| **seedream-50** | `[SKILL]` | — | — | ★★★★★ | Seedream 5.0 Pro 文生图，高质量 | 直接触发；高质量 AI 生图 | ✅ 已有 |
| **gpt-image-prompt-engine** | `[SKILL]` | — | — | ★★★★ | 530+ 案例模板，Prompt-as-Code，高精度中英文文字排版 | 直接触发；需要优化/生成生图提示词时 | ✅ 已有 |
| **byted-mediakit-image** | `[SKILL]` | — | — | ★★★★ | 图片增强/擦除/画质/文字识别/背景移除 | 直接触发；图片后期处理 | ✅ 已有 |
| **doubao-visualization（生成式配图分支）** | `[SKILL]` | — | — | ★★★★ | 生成式知识配图，概念/机制/流程插画 | 直接触发；知识讲解配图 | ✅ 已有 |
| **Lucide** | `[CODE]` | — | ISC | ★★★★ | 1500+ 极简线性图标，多框架包，tree-shakeable | 本地克隆 `~/Documents/projects/lucide`；图标首选 | ✅ 已有 |
| **Heroicons** | `[CODE]` | ~8k | MIT | ★★★★ | ~300 几何图标（线性/实心），Tailwind 出品 | npm/CDN；产品 UI 图标 | ⬜ 按需 |
| **unDraw** | `[EXT]` | — | 免费 | ★★★★ | 可定制配色插画，统一扁平风格，无需署名 | Web 下载；产品/PPT 装饰插画 | ⬜ 登记 |
| **3dicons** | `[CODE]` | — | CC0 | ★★★★★ | 1500+ 3D 图标，含 Blender 源文件，可编辑 | GitHub；产品装饰/3D 元素 | ⬜ 待引入 |
| **Poly Haven** | `[EXT]` | — | CC0 | ★★★★★ | HDRI(16K)/PBR 纹理(8K+)/3D 模型，有 REST API | Web/API；3D 渲染/科研可视化素材 | ⬜ 登记 |
| **storyset** | `[EXT]` | — | 免费(需署名) | ★★★★ | 可编辑插画，风格多样 | Web；插画素材（注意署名） | ⬜ 登记 |
| **ambientCG** | `[EXT]` | — | CC0 | ★★★★ | PBR 材质/纹理，与 Poly Haven 互补 | Web；3D 材质 | ⬜ 登记 |

### 路由规则
- **AI 生图（海报/主视觉/概念图）** → seedream-50 或 doubao-creative-design
- **生图提示词优化** → gpt-image-prompt-engine
- **知识讲解配图（概念/机制/流程）** → doubao-visualization 生成式配图分支
- **图片后期（增强/擦除/去背景）** → byted-mediakit-image
- **图标** → Lucide（首选，已有），产品 UI 需几何风 → Heroicons
- **插画/装饰** → unDraw（扁平可改色）、3dicons（3D 元素）
- **3D 渲染素材** → Poly Haven + ambientCG
- **AI 边界**：数据图禁 AI；AI 仅用于示意图/TOC/装饰，须标注 "schematic / AI-generated illustration"

---

## 6. 分支五：材料化学与科研出版图工具链

### 核心轮子

| 名称 | 类型 | Stars | License | 美学 | 能力 | 调用路径 | 状态 |
|---|---|---|---|---|---|---|---|
| **pymatgen** | `[CODE]` | — | MIT | ★★★★ | 晶体结构表示/分析，相图/Pourbaix 图，能带/态密度绘制，VTK 查看器，VASP/CIF IO | pip；材料信息学标准，可能已在 mattools 环境中 | ⬜ 确认/安装 |
| **pyvista** | `[CODE]` | 3,783 | MIT | ★★★★ | 3D 科学可视化，"VTK for humans"，体渲染/PBR/glTF，NumPy 原生 | `pip install 'pyvista[all]'`；材料 3D 渲染首选 | ⬜ 待安装 |
| **hofmann** | `[CODE]` | — | MIT | ★★★★ | 晶体结构可视化，ASE/pymatgen 互操作，配位多面体渲染，晶胞线框，交互式查看器 | `pip install hofmann`；轻量晶体结构图 | ⬜ 待安装 |
| **VESTA** | `[EXT]` | — | 免费 | ★★★★ | 晶体/分子结构 3D 可视化，体数据，等值面 | 本地已安装；登记对接路径和导出规范 | ✅ 已在用 |
| **ASE** | `[CODE]` | — | LGPL-2.1⚠️ | ★★★ | 原子模拟，Atoms 对象，与 pymatgen 互转 | pip；LGPL 传染性，pymatgen 可覆盖大部分需求 | ⚠️ deferred |
| **RDKit** | `[CODE]` | — | BSD-3 | ★★★★ | 化学信息学，2D 分子渲染，SMILES→图 | pip；分子/化学结构图 | ⬜ 按需 |
| **Ovito** | `[EXT]` | — | 开源核心(GPL)/商业 Pro | ★★★★ | 原子轨迹可视化，材料模拟标准 | 本地安装；轨迹/动力学可视化 | ⬜ 登记 |
| **sci-figure** | `[CODE]`+`[SKILL]` | — | — | ★★★★ | Python 库+skill，render_atoms/figkit，draw.io 导出 | GitHub；科研图一体化 | ⬜ 按需 |

### 科研出版图规范（Nature/PNAS/NPJ）

详见 `docs/scientific-figure-spec.md`（待写），核心要点：

- **格式**：矢量优先（PDF/EPS/SVG），位图 ≥300 DPI（组合图 ≥600 DPI）
- **尺寸**：单栏 8.6cm，双栏 17.8cm（Nature）；精确控制不拉伸
- **字体**：无衬线（Arial/Helvetica），嵌入 Type-42 字体，禁用 Type-3
- **字号**：图中文字 ≥5pt（印刷后），主标签 ≥7pt
- **线宽**：≥0.5pt（印刷后），坐标轴 ≥0.75pt
- **配色**：色盲安全（Okabe-Ito / viridis / ColorBrewer），避免红绿对比
- **面板标注**：a/b/c 粗体，左上角，统一位置
- **AI 边界**：数据图禁 AI 生成；AI 仅用于示意图/TOC，须标注 "schematic"

### 路由规则
- **晶体/分子结构图** → hofmann（轻量 pip）或 pyvista（3D 渲染）或 VESTA（本地已装，高质量导出）
- **能带/态密度/相图** → pymatgen 内置绘图 + SciencePlots 风格
- **谱图（XRD/XPS/FTIR/Raman）** → matplotlib + SciencePlots（数据确定性渲染）
- **显微图标注（SEM/TEM/AFM）** → 原图保持 + doubao-visualization 原图标注分支 或 Inkscape
- **机理/反应路径示意图** → drawio + drawio-academic-skills 或 AI 生成式（标注 schematic）
- **TOC/Graphical Abstract** → AI 生成式 + 后期精修，须标注
- **3D 渲染大图** → pyvista + Poly Haven 素材 或 Blender（deferred）

---

## 7. AI 做图 MCP / 专用 Skill

| 名称 | 类型 | Stars | License | 美学 | 能力 | 调用路径 | 状态 |
|---|---|---|---|---|---|---|---|
| **antvis/mcp-server-chart** | `[MCP]` | 4.2k | MIT | ★★★★ | 最流行可视化 MCP，AntV/G2 驱动，自然语言→25+ 图表，支持 Claude/Cursor，可 Docker | npx / Docker / 配置 MCP；AI 自动做数据图核心 | ⬜ 待部署 |
| **flint-mcp** | `[MCP]` | — | — | ★★★★ | 统一中间语言编译到 Vega-Lite/ECharts/Chart.js，agent 可创建/校验/渲染 | MCP 配置；多后端统一图表 | ⬜ 按需 |
| **viz-mcp** | `[MCP]` | — | MIT | ★★★ | 自动选图类型，多图仪表盘，输出自包含 HTML/PNG | MCP 配置；快速数据探索 | ⬜ 按需 |
| **scientific-figure-making** | `[SKILL]`+`[CODE]` | 5.2k | CC-BY-NC 4.0 | ★★★★★ | 基于 figures4papers 的顶会顶刊插图专用 skill，含完整 API 契约与实战脚本 | 直接触发 `scientific-figure-making` | ✅ 已有 |
| **sci-figure-workflow** | `[SKILL]` | — | — | ★★★★ | AIGC 科研绘图 4 步工作流（GPT-image-2 × Gemini Vision × Nano Banana 2 × draw.io） | GitHub；科研图 AI 工作流参考 | ⬜ 登记 |
| **thesis-figure-skill** | `[SKILL]` | — | — | ★★★★ | 论文配图 skill：LaTeX/TikZ + draw.io XML 双输出 | GitHub；论文配图参考 | ⬜ 登记 |
| **Icarus Figures** | `[SKILL]` | — | — | ★★★★ | 出版级科研图 skill：matplotlib/seaborn 数据图 + TikZ 方法图 | GitHub；出版级图参考 | ⬜ 登记 |

### 路由规则
- **AI 自动做数据图** → antvis/mcp-server-chart（首选，4.2k stars，最成熟）
- **顶会论文插图规范/消融/对比** → **scientific-figure-making**（首选实操规范）
- **多后端统一图表** → flint-mcp
- **快速数据探索仪表盘** → viz-mcp
- **科研图 AI 工作流参考** → sci-figure-workflow / Icarus Figures / thesis-figure-skill（登记为方法论参考，不直接集成）

---

## 8. 现有资产盘点

### 已安装 Skill

| Skill | 位置 | 在 figure-router 中的角色 |
|---|---|---|
| scientific-figure-making | `~/.agents/skills/scientific-figure-making` | 顶会顶刊级 Python 插图规范与实战脚本库（来自 figures4papers） |
| doubao-visualization | 内置 | 数据图(ECharts)/原图标注/HTML-SVG 交互/生成式配图 的执行后端 |
| archify | `~/.agents/skills/archify` | 技术工程图（架构/流程/时序/数据流/状态机）首选 |
| drawio | `~/.agents/skills/drawio` | 全能可编辑图，论文示意图需叠加 academic-skills |
| drawio-academic-skills | `~/.agents/skills/drawio-academic-skills` | drawio 学术出版叠加层 |
| gpt-image-prompt-engine | user_skills | AI 生图提示词优化 |
| doubao-creative-design | 内置 | 商业创意图/海报/Banner |
| seedream-50 | 内置 | 高质量文生图 |
| byted-mediakit-image | 内置 | 图片后期（增强/擦除/去背景/OCR） |
| lark-slides-pro | 内置 | 整套 PPT 组装交付 |
| lark-whiteboard | 内置 | 白板/协作图 |

### 已克隆本地库（`~/Documents/projects/`）

| 库 | 在 figure-router 中的角色 | 建议 |
|---|---|---|
| figures4papers | 顶会顶刊科研图脚本集 (ImmunoStruct/VIGIL/Dispersion等) | 保留，沙盒参考库 |
| echarts | 数据图核心，交互最强 | 保留，补齐 .git 和上游 URL |
| d3 | 自定义可视化底层 | 保留 |
| antvis-x6 | 图编辑引擎，节点式交互图 | 保留 |
| xyflow (React Flow) | 前端节点图 | 保留 |
| rough | 手绘风 SVG | 保留，与 Excalidraw 风格配套 |
| lucide | 图标首选 | 保留，升级到最新 |
| PptxGenJS | JS 生成 PPTX | 保留 |

---

## 9. Deferred（体量大 / 非必要 / 传染性 license）

| 项目 | 原因 | 重新考虑条件 |
|---|---|---|
| Three.js | 通用 3D 引擎，非图表专用，体量大 | 需要复杂 3D 网页交互且 pyvista/archify 不够时 |
| Manim | 需 LaTeX + 系统依赖，动画视频非日常需求 | 需要制作 3Blue1Brown 风格教学视频时 |
| ASE | LGPL-2.1 传染性，pymatgen 可覆盖大部分 | pymatgen 不够用且接受 LGPL 时 |
| Ovito Pro | 商业版，开源核心功能有限（GPL） | 需要原子轨迹高级分析且愿意用商业版时 |
| Blender | 体量大，学习曲线陡 | pyvista 不够用且需要电影级 3D 渲染时 |
| VMD / PyMOL | 免费非开源，登记为外部工具即可 | 需要大分子/生物分子可视化时 |
| PlantUML | GPL v3 传染性，UML 场景少 | 大量 UML 图且接受 GPL 时 |

---

## 10. 待办（按优先级）

- [ ] **安装 SciencePlots**（pip，科研出图事实标准）
- [ ] **安装 drawio-academic-skills**（作为 drawio sibling overlay）
- [ ] **部署 antvis/mcp-server-chart**（npx 或 Docker，AI 做图核心）
- [ ] **安装 pyvista + hofmann**（材料 3D 可视化）
- [ ] **确认 pymatgen 是否已安装**（mattools 环境中可能已有）
- [ ] **引入 Slidev + Marp**（演示双轨：比赛风 + 学术风）
- [ ] **补齐已克隆库的 .git 和上游 URL**（echarts/d3/x6/xyflow/rough/lucide/PptxGenJS）
- [ ] **编写 docs/scientific-figure-spec.md**（科研出版图完整规范）
- [ ] **编写 docs/vesta-integration.md**（VESTA 对接与导出规范）
- [ ] **编写 SKILL.md**（figure-router 路由 skill 本体，等注册表稳定后）

---

*注册表维护：新增工具时在此登记，标注类型/Stars/License/美学/能力/调用路径/状态。路由规则变更时同步更新第 0 节。*
