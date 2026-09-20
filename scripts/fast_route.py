#!/usr/bin/env python3
"""
fast_route.py — figure-router 亚秒级快路径语义分发器 (Fast-Path Semantic Router)
=============================================================================
结合 TypeSafe Jev，对用户的制图需求在 300ms 内完成分支判决与具体工具匹配，
当置信度 >= 0.85 时直接定位目标技能，彻底免除在上下文载入 210 行全量路由表的开销。

用法：
  python3 fast_route.py --query "帮我画一个 Raft 共识时序交互图"
  python3 fast_route.py -q "Nature 风格晶体能带结构与声子谱" --json
"""

import argparse
import json
import subprocess
import sys
from typing import Any, Dict


def query_jev(state: str, questions: Dict[str, Any]) -> Dict[str, Any]:
    """通过 jev CLI 执行结构化快决策"""
    try:
        cmd = [
            "jev", "decide",
            "--state", state,
            "--questions", json.dumps(questions, ensure_ascii=False),
            "--answers-only"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(res.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error executing jev CLI: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error querying Jev: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Jev-powered Fast-Path Semantic Router for figure-router")
    parser.add_argument("--query", "-q", required=True, help="User request text describing the figure to create")
    parser.add_argument("--json", action="store_true", help="Print raw JSON only")

    args = parser.parse_args()

    questions = {
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

    answers = query_jev(args.query, questions)

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


if __name__ == "__main__":
    main()
