# MCP Server Chart 配置指南

> **定位**: antvis/mcp-server-chart（4.2k stars, MIT）是目前最流行的 AI 做图 MCP 服务器。基于 AntV/G2，支持自然语言→25+ 种图表。本文档说明配置和使用方式。

---

## 1. 基本信息

| 项目 | 值 |
|---|---|
| 包名 | `@antv/mcp-server-chart` |
| 版本 | 0.9.10 |
| License | MIT |
| Stars | 4.2k |
| 底层 | AntV G2（蚂蚁集团图形语法） |
| 图表类型 | 25+（折线/柱状/饼图/散点/雷达/漏斗/热力图/地图/思维导图/网络图/鱼骨图等） |
| 传输协议 | stdio / SSE / streamable |

---

## 2. 功能特点

- 自然语言描述 → 自动选择图表类型 → 生成图表
- 支持数据传入（JSON/CSV）
- 输出自包含 HTML（可交互）或 PNG
- 支持 Claude Desktop / Cursor / VS Code / Cherry Studio 等 MCP 客户端
- 可 Docker 部署
- 美学评级：★★★★（AntV 设计语言，现代专业）

---

## 3. 配置方式

### 3.1 方式一：npx 直接运行（最简单）

```bash
npx -y @antv/mcp-server-chart --transport stdio
```

在 MCP 客户端配置中添加：

```json
{
  "mcpServers": {
    "chart": {
      "command": "npx",
      "args": ["-y", "@antv/mcp-server-chart", "--transport", "stdio"]
    }
  }
}
```

### 3.2 方式二：全局安装

```bash
npm install -g @antv/mcp-server-chart

# 验证
mcp-server-chart --help
```

MCP 配置：

```json
{
  "mcpServers": {
    "chart": {
      "command": "mcp-server-chart",
      "args": ["--transport", "stdio"]
    }
  }
}
```

### 3.3 方式三：SSE / Streamable 服务（远程部署）

```bash
# SSE 模式
npx -y @antv/mcp-server-chart --transport sse --host 0.0.0.0 --port 1122

# Streamable 模式（推荐，MCP 新标准）
npx -y @antv/mcp-server-chart --transport streamable --host 0.0.0.0 --port 1122 --endpoint /mcp
```

访问：`http://localhost:1122/mcp`

### 3.4 方式四：Docker

```bash
docker run -d -p 1122:1122 --name mcp-chart \
  -e TRANSPORT=streamable \
  -e PORT=1122 \
  antv/mcp-server-chart:latest
```

---

## 4. 在 Doubao 环境中的使用

> **注意**: 当前 Doubao  agent 环境的 MCP 配置方式取决于客户端设置。如果客户端支持 MCP 服务器配置，按上述方式添加。如果不支持，可通过以下替代方式使用：

### 替代方式：命令行生成

```bash
# 生成图表（通过 MCP 工具调用）
# 在支持 MCP 的客户端中直接说："帮我画一个折线图，数据是..."
```

### 在 figure-router 中的定位

mcp-server-chart 是 figure-router 的 **AI 做图执行后端**之一。当路由到"AI 自动做数据图"时：

1. 如果 MCP 服务器已配置 → 直接调用 MCP 工具
2. 如果未配置 → 用 ECharts（doubao-visualization）或 matplotlib 手动生成
3. 复杂定制 → 用 D3 或 ECharts 手动编写

---

## 5. 支持的图表类型

| 类别 | 图表类型 |
|---|---|
| 基础 | 折线图、柱状图、饼图、散点图、面积图、环形图 |
| 分布 | 直方图、箱线图、热力图、小提琴图 |
| 关系 | 网络图、桑基图、弦图、树图 |
| 层次 | 旭日图、矩形树图、冰挂图 |
| 地理 | 地图、散点地图、流向地图 |
| 专业 | 雷达图、漏斗图、仪表盘、词云、思维导图、鱼骨图、瀑布图 |
| 组合 | 双轴图、多面板图 |

---

## 6. 使用示例（自然语言）

> "帮我画一个折线图，展示 2020-2025 年的销售额增长，数据是：2020:100, 2021:150, 2022:200, 2023:280, 2024:350, 2025:420"

> "用柱状图对比 A/B/C 三个产品的用户留存率，7日和30日两个维度"

> "画一个雷达图展示五个维度的能力评估：性能、易用性、扩展性、安全性、成本"

---

## 7. 与其他做图工具的对比

| 工具 | AI 自动 | 交互 | 矢量 | 定制深度 | 美学 |
|---|---|---|---|---|---|
| **mcp-server-chart** | ✅ 最强 | ✅ HTML | ✅ SVG | 中 | ★★★★ |
| ECharts（手动） | ❌ | ✅ | ✅ | 高 | ★★★★★ |
| matplotlib + SciencePlots | ❌ | ❌ | ✅ PDF | 高 | ★★★★（学术） |
| D3 | ❌ | ✅ | ✅ | 极高 | 取决于实现 |
| AI 生图（seedream） | ✅ | ❌ | ❌ 位图 | 低 | ★★★★★（创意） |

**路由规则**:
- 快速数据探索 / AI 自动选图 → mcp-server-chart
- 论文数据图 → matplotlib + SciencePlots（确定性矢量）
- 网页交互图 → ECharts
- 完全自定义 → D3
- 创意/示意图 → seedream / doubao-creative-design

---

## 8. 故障排查

| 问题 | 解决方案 |
|---|---|
| npx 下载慢 | 使用国内镜像：`NPM_CONFIG_REGISTRY=https://registry.npmmirror.com npx -y @antv/mcp-server-chart` |
| 端口被占用 | `--port 1123` 换端口 |
| MCP 客户端连不上 | 检查 transport 类型，stdio 模式不需要 host/port |
| 图表不显示 | 检查数据格式是否正确，尝试简化数据 |
| 中文乱码 | 确保终端/客户端 UTF-8 编码 |

---

*本文档是 figure-router AI 做图分支的 MCP 配置指南。路由到 AI 自动做图时读取本文档。*
