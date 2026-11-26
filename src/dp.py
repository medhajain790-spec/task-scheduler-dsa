from bisect import bisect_right

def weighted_job_scheduling(tasks):
    """Max total priority with no overlapping tasks. O(n log n)."""
    tasks = sorted(tasks, key=lambda t: t.finish)
    finishes = [t.finish for t in tasks]
    n = len(tasks)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        t = tasks[i - 1]
        p = bisect_right(finishes, t.start, 0, i - 1)  # last compatible task
        dp[i] = max(dp[i - 1], t.priority + dp[p])
    # backtrack
    selected, i = [], n
    while i > 0:
        t = tasks[i - 1]
        p = bisect_right(finishes, t.start, 0, i - 1)
        if t.priority + dp[p] >= dp[i - 1]:
            selected.append(t)
            i = p
        else:
            i -= 1
    return dp[n], selected[::-1]


def weighted_job_scheduling_with_resources(tasks, max_resources):
    """Max total priority, no overlap, total resources <= max_resources. O(n * R)."""
    tasks = sorted(tasks, key=lambda t: t.finish)
    finishes = [t.finish for t in tasks]
    n, R = len(tasks), max_resources
    prev = [bisect_right(finishes, tasks[i].start, 0, i) for i in range(n)]
    dp = [[0] * (R + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        t, p = tasks[i - 1], prev[i - 1]
        for r in range(R + 1):
            dp[i][r] = dp[i - 1][r]
            if t.resources <= r:
                dp[i][r] = max(dp[i][r], t.priority + dp[p][r - t.resources])
    selected, i, r = [], n, R
    while i > 0:
        if dp[i][r] == dp[i - 1][r]:
            i -= 1
        else:
            t = tasks[i - 1]
            selected.append(t)
            r -= t.resources
            i = prev[i - 1]
    return dp[n][R], selected[::-1]
