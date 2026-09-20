# 演示工具使用指南（Slidev / Marp / python-pptx）

> **定位**: figure-router 演示与交付视觉分支的工具使用指南。覆盖比赛答辩 PPT、学术汇报 PPT、数据驱动 PPT 三种场景。

---

## 1. 工具选型矩阵

| 场景 | 首选工具 | 备选 | 输出格式 |
|---|---|---|---|
| 比赛答辩 / 视觉冲击 / 技术演讲 | **Slidev** | reveal.js | HTML / PDF / PNG |
| 学术汇报 / 组会 / 答辩（简洁） | **Marp** | LaTeX Beamer | PPTX / PDF / HTML |
| 数据驱动 / 批量生成 PPT | **python-pptx** | PptxGenJS | PPTX |
| 整套飞书幻灯片交付 | **lark-slides-pro** | — | 飞书幻灯片 |
| 复杂动画 / 网页演示 | reveal.js | Slidev | HTML |

---

## 2. Slidev（比赛答辩 / 技术演讲首选）

### 2.1 特点

- Markdown 写幻灯片，Vue 组件增强
- 代码高亮、公式、图表、交互组件
- 主题丰富，可定制
- 支持演讲者模式、录制、导出 PDF/PNG
- 美学评级：★★★★★（现代极客风）

### 2.2 快速开始

```bash
# 创建新项目（交互式）
npx -y @slidev/cli init my-slides

# 或手动创建
mkdir my-slides && cd my-slides
echo "---
theme: default
---

# 我的演讲标题

副标题内容
" > slides.md

# 启动开发服务器
npx -y @slidev/cli slides.md

# 导出 PDF
npx -y @slidev/cli export slides.md --format pdf

# 导出 PNG（每页一张）
npx -y @slidev/cli export slides.md --format png
```

### 2.3 比赛风 PPT 要点

- **封面**: 大标题 + 视觉冲击背景 + 团队/学校 Logo
- **目录**: 简洁，4-6 个章节
- **数据页**: 大字号关键数字 + ECharts 图表 + 对比表格
- **技术页**: 架构图（archify/drawio）+ 代码片段 + 流程图
- **结尾**: 总结 + 致谢 + Q&A
- **配色**: 品牌色/学校色 + 高对比强调色
- **动画**: 适度使用转场，不要每页都动

### 2.4 推荐主题

| 主题 | 风格 | 适用 |
|---|---|---|
| default | 简洁现代 | 通用 |
| seriph | 衬线优雅 | 学术/正式 |
| apple | 苹果风 | 产品/技术 |
| bricks | 多彩活泼 | 比赛/创意 |
| neko-style | 技术演讲（KubeCon 风） | 技术答辩 |

---

## 3. Marp（学术汇报首选）

### 3.1 特点

- 极简 Markdown → PPTX/PDF/HTML
- 多主题（minimal / beamer / 学术绿等）
- 直接输出 PPTX（可在 PowerPoint/Keynote 中编辑）
- 轻量、快速、无依赖
- 美学评级：★★★★（简洁学术风）

### 3.2 快速开始

```bash
# 基本用法
npx -y @marp-team/marp-cli slides.md -o output.pptx

# 导出 PDF
npx -y @marp-team/marp-cli slides.md -o output.pdf

# 预览（启动服务器）
npx -y @marp-team/marp-cli -s slides.md

# 指定主题
npx -y @marp-team/marp-cli slides.md --theme academic.css -o output.pptx
```

### 3.3 学术汇报 PPT 要点

- **封面**: 标题 + 作者 + 单位 + 日期（简洁，无多余装饰）
- **目录**: 可选，3-5 个章节
- **背景**: 研究动机 + 问题定义 + 文献缺口
- **方法**: 流程图 + 关键公式 + 实验设置
- **结果**: 数据图（matplotlib/SciencePlots 生成）+ 对比表
- **讨论**: 主要发现 + 局限性 + 未来工作
- **结尾**: 致谢 + 参考文献
- **配色**: 低饱和（蓝/灰/绿），克制
- **动画**: 无（学术汇报不使用动画）
- **字号**: 正文 ≥20pt，标题 ≥32pt（投影可读）

### 3.4 Marp 幻灯片模板

```markdown
---
marp: true
theme: default
size: 16:9
paginate: true
---

# 论文标题

**作者名**
单位 / 实验室
2026-08-30

---

## 研究背景

- 问题 1
- 问题 2
- 本文贡献

---

## 方法

![方法流程图](method.png)

关键公式：
$$E = mc^2$$

---

## 结果

![数据图](result.png)

| 方法 | 指标 A | 指标 B |
|---|---|---|
| 本文 | 0.95 | 0.87 |
| 基线 | 0.82 | 0.71 |

---

## 结论与展望

- 主要发现
- 局限性
- 未来工作

**谢谢！Q&A**
```

---

## 4. python-pptx（数据驱动 / 批量 PPT）

### 4.1 特点

- Python 程序化生成 PPTX
- 与数据分析流水线无缝衔接
- 可批量生成、模板化
- 美学评级：★★★（功能型，需手动设计模板）

### 4.2 快速开始

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.33)  # 16:9
prs.slide_height = Inches(7.5)

# 标题页
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "数据驱动报告"
slide.placeholders[1].text = "自动生成"

# 内容页 + 图片
slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.title.text = "数据分析结果"
slide.shapes.add_picture('chart.png', Inches(1), Inches(1.5), width=Inches(11))

prs.save('report.pptx')
```

---

## 5. 比赛风 vs 学术风 关键差异

| 维度 | 比赛风（Slidev） | 学术风（Marp） |
|---|---|---|
| 配色 | 高对比、品牌色、撞色 | 低饱和、蓝/灰、克制 |
| 动画 | 转场/动效/交互 | 无动画 |
| 封面 | 视觉冲击、大图、slogan | 简洁标题+作者+单位 |
| 数据页 | 大字号关键数字、突出 | 严谨图表、标注、误差棒 |
| 字号 | 灵活，视觉优先 | 正文≥20pt，投影可读 |
| 输出 | HTML/PDF（演示用） | PPTX/PDF（可编辑） |
| 工具 | Slidev | Marp / Beamer |

---

## 6. PPT 中的图表

PPT 中的数据图**不要在 PPT 里画**，按以下流程：

1. 用 matplotlib + SciencePlots 生成矢量图（PDF/SVG）
2. 或用 ECharts 生成交互图（HTML 演示时）
3. 导入 PPT 时保持矢量格式（PPTX 支持 EMF/SVG）
4. 图的风格与 PPT 整体配色协调

---

*本文档是 figure-router 演示分支的工具使用指南。路由到 PPT/演示时读取本文档。*
