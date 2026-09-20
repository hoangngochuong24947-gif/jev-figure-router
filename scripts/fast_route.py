#!/usr/bin/env python3
"""
fast_route.py — jev-figure-router 极速语义分发器 (Fast-Path Semantic Router)
=============================================================================
结合 TypeSafe Jev System-1 决策引擎，对用户的制图需求在 300ms 内完成分支判决与具体工具匹配。
具备免外部依赖自愈能力（支持直接 HTTP 调用 OpenRouter Decisions API 或复用 jev CLI）。

用法：
  python3 scripts/fast_route.py -q "帮我画一个 Raft 共识时序交互图"
  python3 scripts/fast_route.py -q "Nature 论文标准的声子谱与态密度数据折线图" --json
  python3 scripts/fast_route.py -q "科技感云计算架构拓扑图" --template
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

DECISIONS_ENDPOINT = "https://openrouter.ai/api/alpha/decisions"
DEFAULT_MODEL = "~typesafe/jev-latest"


def resolve_openrouter_key() -> Optional[str]:
    """尝试从环境变量、.env 文件中获取 OpenRouter Key"""
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if key and key.startswith("sk-or-"):
        return key

    # 尝试当前目录及上级目录的 .env
    current = os.path.abspath(os.getcwd())
    while current != os.path.dirname(current):
        env_path = os.path.join(current, ".env")
        if os.path.isfile(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("OPENROUTER_API_KEY="):
                            val = line.split("=", 1)[1].strip("'\" \t")
                            if val.startswith("sk-or-"):
                                return val
            except Exception:
                pass
        current = os.path.dirname(current)
    return None


def query_jev_direct(state: str, questions: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    """无需外部 CLI，直接通过 Python 内置 urllib 请求 OpenRouter Jev Alpha 端点"""
    payload = {
        "model": DEFAULT_MODEL,
        "state": state,
        "questions": questions
    }
    req = urllib.request.Request(
        DECISIONS_ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost",
            "X-Title": "jev-figure-router"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("answers", {})


def query_jev(state: str, questions: Dict[str, Any]) -> Dict[str, Any]:
    """混合策略：优先使用 local jev CLI，不存在则自愈回退到原生 HTTP API"""
    # 策略 1：检查本地是否存在 jev 命令
    jev_path = shutil.which("jev")
    if jev_path:
        try:
            cmd = [
                jev_path, "decide",
                "--state", state,
                "--questions", json.dumps(questions, ensure_ascii=False),
                "--answers-only"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(res.stdout.strip())
        except Exception:
            pass  # 回退到原生 HTTP

    # 策略 2：通过 OPENROUTER_API_KEY 原生 HTTP 请求
    api_key = resolve_openrouter_key()
    if api_key:
        try:
            return query_jev_direct(state, questions, api_key)
        except Exception as e:
            print(f"Error querying OpenRouter Decisions API: {e}", file=sys.stderr)
            sys.exit(1)

    print(
        "Error: OPENROUTER_API_KEY is not set and 'jev' CLI is not found in PATH.\n"
        "Please run: export OPENROUTER_API_KEY='sk-or-v1-...'\n"
        "Or install jev: pip install typesafe-jev",
        file=sys.stderr
    )
    sys.exit(1)


STARTER_TEMPLATES = {
    "scientific_plots": """# Scientific Plot Starter (Matplotlib + SciencePlots)
import matplotlib.pyplot as plt
import numpy as np

# Apply Nature/Science style if available
try:
    plt.style.use(['science', 'nature'])
except Exception:
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

fig, ax = plt.subplots(figsize=(3.5, 2.8), dpi=300)
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label=r'$\\sin(x)$', color='#0072B2', lw=1.5)
ax.set_xlabel(r'Energy $(\\mathrm{eV})$')
ax.set_ylabel(r'Density of States $(\\mathrm{a.u.})$')
ax.legend(frameon=True, fontsize=8)
plt.tight_layout()
plt.savefig('output_nature_plot.pdf', format='pdf')
print("Saved to output_nature_plot.pdf")
""",
    "archify": """<!-- Archify Interactive HTML/SVG Diagram Starter -->
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>System Architecture</title>
<style>
  body { background: #0f172a; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
  .box { stroke: #38bdf8; fill: #1e293b; stroke-width: 2; rx: 8; }
  .text { fill: #f8fafc; font-size: 14px; font-weight: 600; text-anchor: middle; }
</style>
</head>
<body>
<svg width="600" height="300" viewBox="0 0 600 300">
  <rect class="box" x="50" y="100" width="160" height="80"/>
  <text class="text" x="130" y="145">Client Request</text>
  <path d="M 210 140 L 380 140" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)"/>
  <rect class="box" x="390" y="100" width="160" height="80"/>
  <text class="text" x="470" y="145">Jev Router</text>
</svg>
</body>
</html>
""",
    "mermaid_d2": """```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Jev as Jev Fast-Path
    participant Tool as Specialized Visual Tool

    User->>Jev: Submit natural language figure request
    Note over Jev: 300ms System-1 Evaluation
    Jev-->>User: Route verdict (Confidence >= 0.85)
    Jev->>Tool: Activate exact rendering engine
    Tool-->>User: Output vector publication figure
```
"""
}


QUESTIONS = {
    "visual_branch": {
        "type": "choice",
        "instructions": "Route the visual request to the exact specialized branch",
        "criteria": {
            "archify": "Interactive HTML architecture, sequence, lifecycle, data flow, or state machine diagrams",
            "drawio_academic": "Publication-grade paper architecture, vector schemas, or thesis figures",
            "scientific_plots": "Matplotlib/SciencePlots numerical scientific data curves (Nature/PNAS style)",
            "patent_drawings": "Patent disclosure figures, mechanical orthographic views, component lead lines",
            "handraw_style": "Hand-drawn sketch architecture or whiteboard illustration (Mermaid/D2)",
            "generative_visual": "Conceptual illustrations, decorative covers, or 3D visual assets"
        }
    },
    "target_tool": {
        "type": "choice",
        "instructions": "Identify the exact primary tool or skill to activate",
        "criteria": {
            "archify": "archify skill (interactive standalone HTML/SVG with trace motion)",
            "drawio_academic": "drawio + drawio-academic-skills (publication vector figures)",
            "scientific_figure_making": "scientific-figure-making / matplotlib + SciencePlots",
            "patent_disclosure_skill": "patent-disclosure-skill",
            "mermaid_d2": "Mermaid (look: handDrawn) or D2",
            "generative_engine": "seedream-50 / doubao-creative-design / gpt-image-prompt-engine"
        }
    },
    "rendering_format": {
        "type": "choice",
        "instructions": "Determine the optimal output rendering format",
        "criteria": {
            "standalone_html": "Interactive standalone HTML with SVG",
            "vector_pdf_eps": "Vector PDF/EPS for LaTeX publication",
            "raster_image": "PNG / WebP image asset"
        }
    }
}


def main():
    parser = argparse.ArgumentParser(description="Jev-powered Fast-Path Semantic Router for figure-router")
    parser.add_argument("--query", "-q", required=True, help="User request text describing the figure to create")
    parser.add_argument("--json", action="store_true", help="Print raw JSON only")
    parser.add_argument("--template", action="store_true", help="Print starter template code for the matched branch")

    args = parser.parse_args()

    answers = query_jev(args.query, QUESTIONS)

    branch = answers.get("visual_branch", {}).get("choice", "archify")
    tool = answers.get("target_tool", {}).get("choice", "archify")
    fmt = answers.get("rendering_format", {}).get("choice", "standalone_html")
    confidence = answers.get("target_tool", {}).get("confidence", 0.0)

    fast_path_eligible = confidence >= 0.85

    result = {
        "query": args.query,
        "visual_branch": branch,
        "target_tool": tool,
        "rendering_format": fmt,
        "confidence": round(confidence, 3),
        "fast_path_eligible": fast_path_eligible,
        "fast_path_action": (
            f"FAST_PATH_HIT: Directly invoke skill '{tool}' without loading full 210-line figure-router table."
            if fast_path_eligible else
            "CONFIDENCE_LOW: Fallback to full figure-router/SKILL.md table for deeper deliberation."
        )
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"FAST_ROUTE_JSON: {json.dumps(result, ensure_ascii=False)}")
        print(f"Target Branch: {branch}")
        print(f"Target Tool  : {tool} (Confidence: {confidence:.2f})")
        print(f"Format       : {fmt}")
        print(f"Action       : {result['fast_path_action']}")

        if args.template or branch in STARTER_TEMPLATES:
            print("\n--- RECOMMENDED STARTER TEMPLATE ---")
            tmpl_key = "scientific_plots" if branch == "scientific_plots" else ("archify" if branch == "archify" else "mermaid_d2")
            print(STARTER_TEMPLATES.get(tmpl_key, ""))


if __name__ == "__main__":
    main()
