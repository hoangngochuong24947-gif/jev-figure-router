# Python 环境与包清单

> **定位**: figure-router 的 Python 执行环境说明。所有科研出图、材料化学、PPT 生成的 Python 代码都在这个 venv 中执行。

---

## 1. 环境信息

| 项目 | 值 |
|---|---|
| Python 版本 | 3.14.5（Homebrew） |
| venv 路径 | `~/.local/figure-router-venv` |
| Python 可执行文件 | `~/.local/figure-router-venv/bin/python` |
| pip 可执行文件 | `~/.local/figure-router-venv/bin/pip` |
| 创建时间 | 2026-08-30 |

---

## 2. 已安装包清单

### 核心绘图

| 包 | 版本 | 用途 |
|---|---|---|
| matplotlib | 3.11.1 | 基础绘图引擎 |
| SciencePlots | 最新 | 期刊风格（Nature/IEEE/Science） |
| plotly | 7.0.0 | 交互式图表（pymatgen 依赖） |

### 材料化学

| 包 | 版本 | 用途 |
|---|---|---|
| pymatgen | 2026.5.4 | 材料信息学标准库（结构/相图/能带） |
| pymatgen-core | 2026.8.30 | pymatgen 核心 |
| pyvista | 0.48.4 | 3D 科学可视化（VTK for humans） |
| VTK | 9.6.2 | 3D 可视化底层（pyvista 依赖） |
| hofmann | 最新 | 轻量晶体结构可视化 |
| spglib | 2.7.0 | 空间群分析 |
| monty | 2026.7.16 | pymatgen 工具库 |

### PPT / 文档

| 包 | 版本 | 用途 |
|---|---|---|
| python-pptx | 1.0.2 | 程序化生成 PPTX |

### 数据处理（依赖项）

| 包 | 版本 |
|---|---|
| numpy | 最新 |
| pandas | 3.0.5 |
| scipy | 最新 |
| sympy | 1.14.0 |
| networkx | 3.6.1 |

---

## 3. 使用方式

### 3.1 激活 venv（终端）

```bash
source ~/.local/figure-router-venv/bin/activate
python my_figure.py
deactivate
```

### 3.2 不激活直接调用（推荐，脚本中）

```bash
~/.local/figure-router-venv/bin/python my_figure.py
```

### 3.3 在 figure-router skill 中

所有 Python 代码执行统一使用 `~/.local/figure-router-venv/bin/python`，不使用系统 Python 或 Doubao 沙箱 Python。

---

## 4. 快速验证

```bash
~/.local/figure-router-venv/bin/python -c "
import matplotlib; print('matplotlib', matplotlib.__version__)
import scienceplots; print('scienceplots OK')
import pymatgen; print('pymatgen OK')
import pyvista; print('pyvista', pyvista.__version__)
import hofmann; print('hofmann OK')
import pptx; print('python-pptx OK')
print('ALL PACKAGES VERIFIED')
"
```

---

## 5. LaTeX（可选，推荐）

SciencePlots 的 `nature` 风格默认使用 LaTeX 渲染文字。当前环境未安装 LaTeX，使用 `no-latex` 回退风格。

如需完整 Nature 级文字质量，安装：

```bash
# 完整版（~4GB，含所有宏包）
brew install --cask mactex

# 或精简版（~100MB，需手动补宏包）
brew install --cask basictex
```

安装后即可使用 `plt.style.use(['science', 'nature'])`。

---

## 6. 安装新包

```bash
~/.local/figure-router-venv/bin/pip install <package-name>
```

**注意**:
- 不要使用 `--break-system-packages`（我们用的是 venv，不需要）
- 不要安装到系统 Python 或 Doubao 沙箱 Python
- 安装后更新本文档的包清单

---

## 6. 待安装 / 可选包

| 包 | 用途 | 优先级 |
|---|---|---|
| seaborn | 统计图表美化 | 中 |
| proplot | matplotlib 增强（科研风格） | 低 |
| cnsplots | Cell/Nature/Science 多面板 | 低 |
| paperplot | 期刊尺寸/字体预检 | 低 |
| RDKit | 化学信息学/分子渲染 | 中（化学相关时） |
| ase | 原子模拟（LGPL，注意） | 低（pymatgen 可覆盖） |
| altair | 声明式图表 | 低 |
| plotnine | ggplot2 for Python | 低 |

---

## 7. 环境重建（如果需要）

```bash
# 删除旧环境
rm -rf ~/.local/figure-router-venv

# 重建
/opt/homebrew/bin/python3 -m venv ~/.local/figure-router-venv
~/.local/figure-router-venv/bin/pip install --upgrade pip
~/.local/figure-router-venv/bin/pip install matplotlib SciencePlots python-pptx hofmann pyvista pymatgen
```

---

*本文档是 figure-router 的 Python 环境单一事实源。执行任何 Python 出图代码前确认使用此 venv。*
