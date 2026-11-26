"""Fair comparison: Greedy (priority) vs DP (with resources) under the SAME resource limit.
Run:  python -m src.fair_benchmark
Writes: results/fair_comparison.txt, priority_comparison.png, resource_utilization.png, fair_runtime.png
"""
import os
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .generator import generate_tasks
from .greedy import greedy_priority
from .dp import weighted_job_scheduling_with_resources

def timed(fn, *args):
    s = time.perf_counter()
    r = fn(*args)
    return r, (time.perf_counter() - s) * 1000

def main(sizes=(100, 500, 1000)):
    os.makedirs("results", exist_ok=True)
    rows = []
    for n in sizes:
        tasks = generate_tasks(n)
        for limit in (n // 4, n // 2, n):
            g, tg = timed(greedy_priority, tasks, limit)
            (best, d), td = timed(weighted_job_scheduling_with_resources, tasks, limit)
            gp = sum(t.priority for t in g)
            rows.append(dict(n=n, limit=limit, gp=gp, dp=best, gain=(best - gp) / gp * 100,
                             tg=tg, td=td,
                             gu=sum(t.resources for t in g) / limit * 100,
                             du=sum(t.resources for t in d) / limit * 100))
    head = f"{'n':>5} {'limit':>6} | {'greedy pri':>10} {'dp pri':>8} {'gain':>7} | {'greedy ms':>9} {'dp ms':>8} | {'g used':>7} {'dp used':>8}"
    lines = [head] + [f"{r['n']:>5} {r['limit']:>6} | {r['gp']:>10} {r['dp']:>8} {r['gain']:>6.1f}% | "
                      f"{r['tg']:>9.2f} {r['td']:>8.2f} | {r['gu']:>6.1f}% {r['du']:>7.1f}%" for r in rows]
    text = "\n".join(lines)
    print(text)
    with open("results/fair_comparison.txt", "w") as f:
        f.write(text + "\n")

    labels = [f"n={r['n']}\nR={r['limit']}" for r in rows]
    x = range(len(rows))
    w = 0.4

    def bars(key_g, key_d, title, ylabel, fname, log=False):
        plt.figure(figsize=(11, 5))
        plt.bar([i - w / 2 for i in x], [r[key_g] for r in rows], w, label="Greedy (priority)", color="#e8833a")
        plt.bar([i + w / 2 for i in x], [r[key_d] for r in rows], w, label="DP (with resources)", color="#2f6fdb")
        plt.xticks(list(x), labels, fontsize=8)
        plt.ylabel(ylabel); plt.title(title); plt.legend()
        if log:
            plt.yscale("log")
        plt.tight_layout(); plt.savefig(f"results/{fname}", dpi=150); plt.close()

    bars("gp", "dp", "Total priority (higher is better)", "Total priority", "priority_comparison.png")
    bars("gu", "du", "Resource utilization", "% of limit used", "resource_utilization.png")
    bars("tg", "td", "Runtime under same resource limit (log scale)", "Time (ms)", "fair_runtime.png", log=True)
    print("\nSaved tables and graphs in results/")

if __name__ == "__main__":
    main()
