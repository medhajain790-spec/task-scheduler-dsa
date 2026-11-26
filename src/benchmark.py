import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .generator import generate_tasks
from .greedy import greedy_activity_selection, greedy_priority
from .dp import weighted_job_scheduling

def timed(fn, *args):
    s = time.perf_counter()
    r = fn(*args)
    return r, (time.perf_counter() - s) * 1000

if __name__ == "__main__":
    sizes = [100, 500, 1000, 2000, 5000]
    g_t, p_t, d_t = [], [], []
    print(f"{'n':>6} | {'time ms (act/pri/dp)':>24} | {'priority (act/pri/dp)':>24} | {'#tasks (act/pri/dp)':>20} | {'res used (pri/dp)':>18}")
    for n in sizes:
        tasks = generate_tasks(n)
        limit = n * 3
        g, tg = timed(greedy_activity_selection, tasks)
        p, tp = timed(greedy_priority, tasks, limit)
        (best, d), td = timed(weighted_job_scheduling, tasks)
        g_t.append(tg); p_t.append(tp); d_t.append(td)
        pr = lambda L: sum(t.priority for t in L)
        rs = lambda L: sum(t.resources for t in L)
        print(f"{n:>6} | {tg:>7.2f}/{tp:>7.2f}/{td:>6.2f} | "
              f"{pr(g):>7}/{pr(p):>7}/{best:>7} | "
              f"{len(g):>5}/{len(p):>5}/{len(d):>5} | "
              f"{rs(p)/limit:>7.1%}/{rs(d)/limit:>7.1%}")
    plt.plot(sizes, g_t, label="Greedy (activity)")
    plt.plot(sizes, p_t, label="Greedy (priority)")
    plt.plot(sizes, d_t, label="DP")
    plt.xlabel("Number of tasks"); plt.ylabel("Time (ms)")
    plt.title("Runtime comparison"); plt.legend()
    plt.savefig("results/runtime_comparison.png", dpi=150)
