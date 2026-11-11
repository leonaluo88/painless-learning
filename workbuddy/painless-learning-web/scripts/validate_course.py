#!/usr/bin/env python3
"""Validate a painless-learning-web course.json.

Usage:
    python3 validate_course.py path/to/course.json [--order]

Checks (errors make the exit code 1; warnings do not):
  errors   duplicate point IDs, prerequisites pointing to missing IDs,
           cycles among active points, merged points without a valid merged_into,
           lessons / questions referencing unknown points
  warnings prerequisites that are deprecated/merged, a point taught in an earlier
           week than one of its hard prerequisites (unless backfill is true),
           active points without a mastery criterion or without any question,
           lessons without a storyline
--order prints one valid learning order (week first, then dependencies).
"""
import json
import sys
from collections import defaultdict


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    data = load(args[0])
    points = data.get("points", [])
    errors, warnings = [], []

    by_id = {}
    for p in points:
        pid = p.get("id")
        if not pid:
            errors.append(f"知识点缺少 id：{p.get('title', p)}")
            continue
        if pid in by_id:
            errors.append(f"重复的 id：{pid}")
        by_id[pid] = p

    def status(pid):
        return by_id[pid].get("status", "active")

    active = {pid for pid in by_id if status(pid) == "active"}

    for pid, p in by_id.items():
        if status(pid) == "merged":
            tgt = p.get("merged_into")
            if not tgt or tgt not in by_id:
                errors.append(f"{pid} 标为 merged，但 merged_into 无效：{tgt}")

    graph = defaultdict(list)  # prerequisite -> dependents
    for pid in active:
        p = by_id[pid]
        for pre in p.get("pre", []):
            qid = pre.get("id") if isinstance(pre, dict) else pre
            kind = pre.get("kind", "hard") if isinstance(pre, dict) else "hard"
            if qid not in by_id:
                errors.append(f"{pid} 的前置 {qid} 不存在")
                continue
            if status(qid) != "active":
                warnings.append(f"{pid} 的前置 {qid} 状态是 {status(qid)}，应改指向新知识点")
                continue
            graph[qid].append(pid)
            if kind == "hard":
                w_p, w_q = p.get("week"), by_id[qid].get("week")
                if w_p is not None and w_q is not None and w_q > w_p and not p.get("backfill"):
                    warnings.append(
                        f"{pid}（第 {w_p} 周）的 hard 前置 {qid} 在第 {w_q} 周才讲：如属后补前置，设 backfill 并加回看卡片")
        if not p.get("mastery"):
            warnings.append(f"{pid} 没有掌握标准 mastery")

    # cycle detection (iterative DFS)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {pid: WHITE for pid in active}
    for start in sorted(active):
        if color[start] != WHITE:
            continue
        stack = [(start, iter(graph[start]))]
        path = [start]
        color[start] = GRAY
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                color[node] = BLACK
                stack.pop()
                path.pop()
                continue
            if nxt not in color:
                continue
            if color[nxt] == GRAY:
                cyc = path[path.index(nxt):] + [nxt]
                errors.append("循环依赖：" + " → ".join(cyc))
            elif color[nxt] == WHITE:
                color[nxt] = GRAY
                stack.append((nxt, iter(graph[nxt])))
                path.append(nxt)

    covered = set()
    for q in data.get("questions", []):
        for pid in q.get("points", []):
            if pid not in by_id:
                errors.append(f"题目 {q.get('id')} 引用了不存在的知识点 {pid}")
            covered.add(pid)
    if data.get("questions"):
        for pid in sorted(active - covered):
            warnings.append(f"{pid} 还没有任何题目")

    for les in data.get("lessons", []):
        for pid in les.get("points", []):
            if pid not in by_id:
                errors.append(f"课 {les.get('id')} 引用了不存在的知识点 {pid}")
        if not les.get("storyline"):
            warnings.append(f"课 {les.get('id')} 没有逻辑主线 storyline")

    print(f"知识点 {len(by_id)} 个（active {len(active)}），题目 {len(data.get('questions', []))} 道，课 {len(data.get('lessons', []))} 节")
    for e in errors:
        print("错误  " + e)
    for w in warnings:
        print("提醒  " + w)
    if not errors and not warnings:
        print("全部通过")

    if "--order" in sys.argv and not any(e.startswith("循环") for e in errors):
        indeg = {pid: 0 for pid in active}
        for q in graph:
            for d in graph[q]:
                indeg[d] += 1
        key = lambda pid: (by_id[pid].get("week") or 0, by_id[pid].get("no") or 0, pid)
        ready = sorted([pid for pid, d in indeg.items() if d == 0], key=key)
        order = []
        while ready:
            n = ready.pop(0)
            order.append(n)
            for d in graph[n]:
                indeg[d] -= 1
                if indeg[d] == 0:
                    ready.append(d)
            ready.sort(key=key)
        print("\n学习顺序：")
        for i, pid in enumerate(order, 1):
            print(f"{i:>4}  {pid}  {by_id[pid].get('title', '')}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
