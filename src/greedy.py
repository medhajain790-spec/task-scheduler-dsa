def greedy_activity_selection(tasks):
    """Earliest finish time first. Maximizes number of tasks."""
    selected, last_finish = [], float("-inf")
    for t in sorted(tasks, key=lambda t: t.finish):
        if t.start >= last_finish:
            selected.append(t)
            last_finish = t.finish
    return selected

def greedy_priority(tasks, max_resources):
    """Highest priority per resource first, within resource limit and no overlap."""
    selected, used = [], 0
    for t in sorted(tasks, key=lambda t: t.priority / t.resources, reverse=True):
        if used + t.resources > max_resources:
            continue
        if all(t.start >= s.finish or t.finish <= s.start for s in selected):
            selected.append(t)
            used += t.resources
    return selected
