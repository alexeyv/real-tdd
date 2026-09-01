"""Sum token usage from Claude Code session logs.

Usage: python3 tools/session_tokens.py ~/.claude/projects/<project-dir>

Walks every .jsonl under the directory, including subagents/, and prints
per-log and total counts of uncached input, cache writes, cache reads,
and output tokens. Streamed assistant messages repeat their usage block
across chunks, so the largest value per message id is taken.
"""
import collections, glob, json, os, sys


def tally(path):
    per = {}
    role = None
    with open(path) as fh:
        head = fh.read(20000)
    for r in ("ping", "pong"):
        if f"command-args>{r}" in head:
            role = r
    for line in open(path):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        m = d.get("message") or {}
        u = m.get("usage")
        if d.get("type") != "assistant" or not u:
            continue
        cur = per.setdefault(m.get("id"), collections.Counter())
        for k, f in (
            ("input", "input_tokens"),
            ("cache_create", "cache_creation_input_tokens"),
            ("cache_read", "cache_read_input_tokens"),
            ("output", "output_tokens"),
        ):
            cur[k] = max(cur[k], u.get(f) or 0)
    t = collections.Counter()
    for c in per.values():
        t.update(c)
    t["calls"] = len(per)
    return t, role


def main(root):
    total = collections.Counter()
    print(f"{'log':60} {'role':5} {'calls':>5} {'input':>7} {'cache_w':>9} {'cache_r':>11} {'output':>8}")
    for path in sorted(glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True)):
        t, role = tally(path)
        total.update(t)
        name = os.path.relpath(path, root)
        if "subagents" in name:
            name = "subagent " + os.path.basename(name)[6:30]
        else:
            name = name[:8]
        print(f"{name:60} {role or '':5} {t['calls']:5} {t['input']:7} {t['cache_create']:9} {t['cache_read']:11} {t['output']:8}")
    print(f"{'total':60} {'':5} {total['calls']:5} {total['input']:7} {total['cache_create']:9} {total['cache_read']:11} {total['output']:8}")


if __name__ == "__main__":
    main(sys.argv[1])
