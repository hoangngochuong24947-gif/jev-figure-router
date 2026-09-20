#!/usr/bin/env python3
"""
quickstart_routing.py — Programmatic quickstart for jev-figure-router
=============================================================================
Demonstrates how to evaluate user visualization queries programmatically
and inspect the high-confidence routing decision.

Usage:
    python3 examples/quickstart_routing.py
"""

import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.fast_route import query_jev, QUESTIONS

SAMPLE_QUERIES = [
    "绘制发表级 Nature 钙钛矿能带结构与声子态密度双栏折线图",
    "帮我画一个 Kubernetes Ingress 到 Service 的网络拓扑和调用时序图",
    "制作一张用于技术分享汇报的 16:9 商业 PPT 架构介绍页",
    "为我的博客文章生成一张赛博朋克风格的 AI 算法架构插画"
]

def main():
    print("=================================================================")
    print("  jev-figure-router — Programmatic Quickstart Demo")
    print("=================================================================\n")

    for i, query in enumerate(SAMPLE_QUERIES, 1):
        print(f"[{i}] Testing query: '{query}'")
        try:
            decision = query_jev(query, QUESTIONS)
            branch = decision.get("visual_branch", {}).get("choice", "unknown")
            conf = decision.get("visual_branch", {}).get("confidence", 0.0)
            fmt = decision.get("rendering_format", {}).get("choice", "unknown")

            print(f"    --> Routed Branch : {branch}")
            print(f"    --> Format Target : {fmt}")
            print(f"    --> Confidence    : {conf:.2f}")
            print(f"    --> Status        : {'FAST_PATH_HIT (Direct Execution)' if conf >= 0.85 else 'FALLBACK_TO_FULL_MATRIX'}\n")
        except Exception as e:
            print(f"    [!] Error during fast routing: {e}\n")

if __name__ == "__main__":
    main()
