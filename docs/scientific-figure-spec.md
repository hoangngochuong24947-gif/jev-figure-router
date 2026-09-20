# 科研出版图规范（Scientific Figure Specification）

> **适用**: Nature / Science / Cell / PNAS / NPJ 系列 / IEEE / ACS / RSC 等期刊投稿
> **核心原则**: 数据图必须确定性矢量渲染；AI 仅用于示意图并标注；所有数字可追溯到原始数据。

---

## 1. 输出格式与分辨率

| 图类型 | 推荐格式 | 最低分辨率 | 说明 |
|---|---|---|---|
| 曲线图 / 散点图 / 柱状图 | **PDF / EPS / SVG**（矢量） | — | 矢量优先，无限缩放不失真 |
| 谱图（XRD/XPS/FTIR/Raman） | **PDF / SVG**（矢量） | — | 数据点+曲线，矢量可编辑 |
| 能带/态密度 | **PDF / SVG**（矢量） | — | pymatgen 生成后矢量导出 |
| 显微图像（SEM/TEM/AFM） | **TIFF / PNG** | ≥600 DPI | 位图原图，标注用矢量叠加 |
| 晶体/分子结构图 | **PDF / SVG**（矢量）或 ≥300 DPI PNG | — | VESTA/pyvista/hofmann 导出 |
| 多面板组合图 | **PDF**（矢量） | — | 所有面板组合后矢量导出 |
| TOC / Graphical Abstract | **PDF / SVG** 或 ≥300 DPI PNG | — | 允许 AI 辅助，须标注 |

**硬规则**:
- 投稿系统要求 TIFF 时，从矢量 PDF 转换，≥300 DPI（组合图 ≥600 DPI）
- 禁止从截图、PPT 导出、或 AI 生成的数据图投稿
- 位图图像不得放大超过原始分辨率的 150%

---

## 2. 尺寸规范（Nature 系列为基准）

| 维度 | 单栏（1-column） | 双栏（2-column） |
|---|---|---|
| 宽度 | 86 mm（3.39 in） | 178 mm（7.01 in） |
| 最大高度 | — | 225 mm（含图注） |

**其他期刊参考**:
- IEEE: 单栏 88 mm，双栏 181 mm
- ACS: 单栏 8.5 cm，双栏 17.8 cm
- Cell: 单栏 8.3 cm，双栏 17.4 cm

**实现方式**（SciencePlots + matplotlib）:
```python
import matplotlib.pyplot as plt
import scienceplots

# 方式一：完整 Nature 风格（需安装 LaTeX，文字质量最高）
plt.style.use(['science', 'nature'])

# 方式二：无 LaTeX 回退（matplotlib 内置 mathtext，无需额外安装）
# 推荐当前环境使用，质量接近完整风格
plt.style.use(['science', 'no-latex'])

# 双栏图手动指定
fig, ax = plt.subplots(figsize=(7.01, 4))  # 英寸，双栏宽
```

> **LaTeX 说明**: `nature` 风格默认用 LaTeX 渲染数学公式和文字，需安装 MacTeX（`brew install --cask mactex`，~4GB）或 BasicTeX（~100MB）。未安装时使用 `no-latex` 回退，质量接近且无需额外依赖。投稿前如追求最高文字质量，建议安装 LaTeX。

**硬规则**:
- 图提交后不得拉伸变形；比例在生成时固定
- 图内文字印刷后不得小于 5 pt（主标签 ≥7 pt）
- 线宽印刷后不得小于 0.5 pt（坐标轴 ≥0.75 pt）

---

## 3. 字体规范

| 项目 | 规范 |
|---|---|
| 字体族 | **无衬线**（Arial / Helvetica，Nature 推荐） |
| 正文字号 | 7–8 pt（印刷后） |
| 轴标签 | 7–8 pt |
| 刻度标签 | 6–7 pt |
| 面板标注（a/b/c） | **8–9 pt，粗体** |
| 图注 | 期刊正文同字号（通常 8 pt） |
| 字体嵌入 | **Type-42（TrueType）**，禁用 Type-3 |

**实现方式**:
```python
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica'],
    'font.size': 8,
    'axes.labelsize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'pdf.fonttype': 42,  # Type-42 嵌入
    'ps.fonttype': 42,
})
```

**硬规则**:
- 同一张图内字体族统一，不得混用衬线/无衬线
- 数学符号使用 LaTeX 渲染（`$E_f$`），字体与正文一致
- 投稿前用 paperplot 或 Adobe Acrobat 预检字体类型

---

## 4. 配色规范

### 4.1 色盲安全调色板（首选）

| 调色板 | 用途 | 颜色 |
|---|---|---|
| **Okabe-Ito** | 分类数据（≤8 类） | `#E69F00` `#56B4E9` `#009E73` `#F0E442` `#0072B2` `#D55E00` `#CC79A7` `#000000` |
| **viridis** | 连续数据/热力图 | matplotlib 内置，色盲安全 |
| **ColorBrewer Set2** | 分类数据（≤8 类） | 柔和、打印友好 |
| **plasma / inferno** | 连续数据 | 感知均匀，色盲安全 |

### 4.2 禁止使用

- ❌ 彩虹调色板（jet / rainbow）—— 感知不均匀、色盲不安全
- ❌ 红绿对比（红绿色盲无法区分）
- ❌ 纯灰阶中使用相近灰度（打印后无法区分）

### 4.3 实现方式

```python
# Okabe-Ito 调色板
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=okabe_ito)

# 连续数据用 viridis
plt.imshow(data, cmap='viridis')
```

### 4.4 灰度可读性（IEEE 强制）

- 所有图在黑白打印后必须可区分
- 用线型（实线/虚线/点线）+ 标记（○/□/△）辅助区分，不依赖颜色 alone

---

## 5. 多面板组合图规范

### 5.1 面板标注

- 位置：**左上角**，面板内或紧贴左上角外侧
- 格式：**小写粗体** `a` `b` `c`（不是 A/B/C，不是 (a)/(b)/(c)）
- 字号：8–9 pt，粗体
- 位置统一：所有面板标注在同一相对位置

### 5.2 布局

- 面板间距：紧凑但不拥挤，标签不重叠
- 轴标签：共享轴时只在最外层面板标注
- 图例：放在空白处或图注中，不遮挡数据
- 对齐：所有面板严格对齐（网格布局）

### 5.3 实现方式（matplotlib + patchwork 风格）

```python
fig, axes = plt.subplots(2, 2, figsize=(7.01, 5.5),
                          gridspec_kw={'hspace': 0.3, 'wspace': 0.25})

# 面板标注
for i, ax in enumerate(axes.flat):
    ax.text(-0.15, 1.05, chr(97+i), transform=ax.transAxes,
            fontsize=9, fontweight='bold', va='top')

plt.savefig('figure1.pdf', dpi=600, bbox_inches='tight')
```

---

## 6. 数据图硬规则（AI 边界）

| 图类型 | 允许 AI | 要求 |
|---|---|---|
| 曲线图 / 散点图 / 柱状图 / 饼图 | ❌ **禁止** | 必须从原始数据确定性渲染（matplotlib/SciencePlots/ECharts） |
| 谱图 / 热图 / 等高线 | ❌ **禁止** | 必须从原始数据渲染 |
| 能带 / 态密度 / 相图 | ❌ **禁止** | pymatgen 等工具从计算数据生成 |
| 显微图像标注 | ⚠️ 有限 | 原图保持不变，标注用矢量叠加（doubao-visualization 原图标注） |
| 机理示意图 / 反应路径 | ✅ 允许 | AI 可生成，**必须标注 "schematic" / "AI-generated illustration"** |
| TOC / Graphical Abstract | ✅ 允许 | AI 可辅助，须标注，后期精修 |
| 架构图 / 流程图 | ✅ 允许 | archify/drawio/Mermaid/D2 生成 |

**标注规范**:
- AI 生成的示意图在图注中注明：`(schematic, generated with AI assistance)`
- 不得将 AI 生成的图描述为 "experimental" / "measured" / "calculated"
- 数据图的每个数字必须可追溯到原始数据文件或计算结果

---

## 7. 图注规范

- 图注包含：图号、面板说明、实验条件、统计信息、缩写定义
- 数据图注明：n（样本量）、误差棒含义（SD/SEM/CI）、统计检验方法和 p 值
- 示意图注明：`(schematic)` 或 `(not to scale)`
- 图注自包含：不读正文也能理解图

**示例**:
> **图 1** | 材料 X 的晶体结构与电学性能。**a**, 材料 X 的晶体结构（VESTA 渲染，schematic）。**b**, 不同温度下的电阻率曲线（n=3，误差棒表示 SD）。**c**, 能带结构（pymatgen 从 DFT 计算生成）。**d**, 态密度积分。缩写：DOS, 态密度；E_F, 费米能级。

---

## 8. 工具链速查

| 任务 | 首选工具 | 备选 |
|---|---|---|
| 顶会基准对比与消融实验 | **scientific-figure-making**（figures4papers） | matplotlib + SciencePlots |
| 数据曲线图 | matplotlib + SciencePlots | ECharts（交互）、plotnine |
| 多面板组合 | matplotlib + GridSpec / scientific-figure-making | patchwork（R）、cowplot（R） |
| 谱图（XRD等） | matplotlib + SciencePlots | origin（外部） |
| 能带/态密度 | pymatgen + matplotlib | VASP 自带、sumo |
| 相图/Pourbaix | pymatgen | — |
| 晶体结构图 | hofmann（轻量）/ pyvista（3D） | VESTA（外部，高质量导出） |
| 分子结构图 | RDKit | PyMOL（外部） |
| 机理示意图 | drawio + drawio-academic-skills | archify、AI 生成（标注 schematic） |
| 架构/流程图 | archify（交互HTML） | drawio、Mermaid、D2 |
| 显微图标注 | doubao-visualization 原图标注 | Inkscape（外部） |
| TOC/Graphical Abstract | seedream-50 + 后期精修 | doubao-creative-design |
| 矢量后期 | Inkscape（外部） | Adobe Illustrator |
| 投稿预检 | paperplot | Adobe Acrobat（字体检查） |

---

## 9. 投稿前检查清单

- [ ] 所有数据图为矢量格式（PDF/EPS/SVG）
- [ ] 位图 ≥300 DPI（组合图 ≥600 DPI）
- [ ] 尺寸符合期刊要求（单栏 86mm / 双栏 178mm）
- [ ] 字体为无衬线（Arial/Helvetica），Type-42 嵌入
- [ ] 图内文字 ≥5 pt（主标签 ≥7 pt）
- [ ] 线宽 ≥0.5 pt（坐标轴 ≥0.75 pt）
- [ ] 配色色盲安全（Okabe-Ito / viridis），无 jet/rainbow
- [ ] 黑白打印可区分（线型+标记辅助）
- [ ] 面板标注 a/b/c 粗体，左上角，位置统一
- [ ] 数据图无 AI 生成；AI 示意图已标注 "schematic"
- [ ] 图注自包含，含 n/误差棒/统计检验/缩写
- [ ] 每个数字可追溯到原始数据
- [ ] 无截图、无 PPT 导出、无拉伸变形

---

*本文档是 figure-router 科研出图分支的执行规范。路由到科研出图时必须读取本文档。*
