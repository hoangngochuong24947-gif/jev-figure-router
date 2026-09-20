# VESTA 对接与导出规范

> **定位**: VESTA 是用户已在用的晶体/分子结构 3D 可视化桌面应用（免费软件，非开源）。figure-router 将其登记为外部工具，提供对接路径和导出规范。
> **适用**: 晶体结构图、分子结构图、缺陷/界面结构、电荷密度、能带三维可视化等。

---

## 1. VESTA 基础信息

| 项目 | 内容 |
|---|---|
| 官网 | https://jp-minerals.org/vesta/en/ |
| 平台 | macOS / Windows / Linux |
| 许可 | 免费软件（非开源，禁止二次分发） |
| 输入格式 | CIF, POSCAR, CONTCAR, xyz, pdb, mol, xsf, cube 等 |
| 输出格式 | PNG, TIFF, JPEG, BMP, EPS, PDF, SVG, POV-Ray, RTF |

---

## 2. 在 figure-router 中的路由规则

| 需求 | 首选 | VESTA 适用场景 |
|---|---|---|
| 快速晶体结构图（代码生成） | hofmann / pyvista | 需要精确控制多面体/配色时 |
| 高质量 3D 渲染大图 | **VESTA** | 论文 Figure 级别的晶体结构图 |
| 电荷密度/自旋密度等值面 | **VESTA** | cube 文件可视化 |
| 界面/缺陷结构 | **VESTA** | 复杂结构的手动调整视角 |
| 分子结构 | RDKit / PyMOL | 小分子 2D/3D |
| 交互式 3D（网页） | pyvista / plotly | 需要旋转交互时 |

**路由逻辑**: 当需求是"论文级晶体结构 3D 图"且用户已有 VESTA 时，优先使用 VESTA 导出；当需要代码自动化/批量生成时，用 hofmann 或 pyvista。

---

## 3. VESTA 导出规范（论文级）

### 3.1 图像设置

| 参数 | 推荐值 | 说明 |
|---|---|---|
| 格式 | **TIFF**（投稿）或 **PNG**（预览） | TIFF 无损，期刊首选 |
| 分辨率 | **≥600 DPI** | 论文图最低 300 DPI，推荐 600 |
| 宽度 | 单栏 86mm / 双栏 178mm | 与 scientific-figure-spec.md 一致 |
| 背景 | **白色**（`Display → Background → White`） | 期刊要求白底 |
| 抗锯齿 | 开启 | 平滑边缘 |

### 3.2 显示设置

| 元素 | 推荐 |
|---|---|
| 原子球 | 多面体模式或球棍模式，半径适中 |
| 多面体 | 半透明（透明度 50-70%），便于看到内部原子 |
| 键 | 细线，颜色与原子协调 |
| 晶胞 | 黑色细线，宽度适中 |
| 标签 | 元素符号，无衬线字体，7-8 pt |
| 配色 | 元素标准色（CPK）或自定义色盲安全配色 |
| 视角 | 正投影（Orthographic），避免透视变形 |

### 3.3 导出操作

1. 调整视角到最佳角度（`View → Reset View` 后手动旋转）
2. 设置显示参数（原子/多面体/晶胞/标签）
3. `File → Export Rendering Image`
4. 选择 TIFF 格式，设置分辨率 ≥600 DPI
5. 勾选 "White background"
6. 导出后用 Inkscape 或 matplotlib 组合多面板

---

## 4. VESTA 与 Python 工具链协作

### 4.1 从 pymatgen 生成 VESTA 输入文件

```python
from pymatgen.core import Structure
from pymatgen.io.vasp import Poscar

# 加载或创建结构
struct = Structure.from_file('structure.cif')

# 导出为 VESTA 可读的 POSCAR 格式
poscar = Poscar(struct)
poscar.write_file('structure.vasp')  # VESTA 直接打开
```

### 4.2 批量生成结构后用 VESTA 渲染

```python
# 批量生成多个结构的 POSCAR
import os
os.makedirs('vesta_inputs', exist_ok=True)

for name, struct in structures.items():
    Poscar(struct).write_file(f'vesta_inputs/{name}.vasp')
    print(f'生成 {name}.vasp，用 VESTA 打开并导出 600dpi TIFF')
```

### 4.3 用 hofmann 快速预览（代码生成，无需 VESTA）

```python
from hofmann import CrystalPlot
from pymatgen.core import Structure

struct = Structure.from_file('structure.cif')
plot = CrystalPlot(struct)
plot.show()  # 交互式预览
plot.save('structure.png', dpi=300)  # 导出
```

---

## 5. VESTA 替代方案对比

| 工具 | 优势 | 劣势 | 适用场景 |
|---|---|---|---|
| **VESTA** | 免费、高质量渲染、支持电荷密度、界面友好 | 非开源、手动操作、批量困难 | 论文级结构图、电荷密度 |
| **hofmann** | pip 安装、代码自动化、pymatgen 互操作 | 渲染质量不如 VESTA | 快速预览、批量生成 |
| **pyvista** | 3D 科学可视化、体渲染、交互式 | 学习曲线、晶体结构需手动构建 | 复杂 3D 数据、体渲染 |
| **pymatgen.vis** | 内置结构查看器、VTK | 功能有限 | 快速查看 |
| **Ovito** | 原子轨迹、动力学、批量渲染 | 开源核心功能有限（Pro 收费） | 分子动力学轨迹 |
| **PyMOL** | 分子渲染质量极高、脚本化 | 主要面向生物分子 | 分子/蛋白结构 |

---

## 6. 常见问题

**Q: VESTA 导出的图可以用 AI 后处理吗？**
A: 可以裁剪、调整亮度对比度、组合多面板，但不得用 AI 重新生成结构或修改原子位置。导出的结构图属于"实验/计算数据"，不是示意图。

**Q: VESTA 图需要标注 "schematic" 吗？**
A: 不需要。VESTA 从真实结构文件渲染，属于确定性可视化，不是 AI 生成。但如果是理想化的示意结构（非真实计算结构），应在图注中注明 "schematic representation"。

**Q: 可以在 VESTA 里加面板标注 a/b/c 吗？**
A: 不建议。VESTA 导出单张图后，用 matplotlib 或 Inkscape 组合多面板并加标注，确保标注位置和字号统一。

---

*本文档是 figure-router 材料化学分支的 VESTA 对接规范。路由到晶体结构图时读取本文档。*
