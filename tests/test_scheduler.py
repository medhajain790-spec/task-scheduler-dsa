from itertools import combinations
from src.greedy import greedy_activity_selection, greedy_priority
from src.dp import weighted_job_scheduling
from src.generator import generate_tasks

def no_overlap(sel):
    sel = sorted(sel, key=lambda t: t.start)
    return all(a.finish <= b.start for a, b in zip(sel, sel[1:]))

def brute_force(tasks):
    best = 0
    for r in range(len(tasks) + 1):
        for c in combinations(tasks, r):
            if no_overlap(c):
                best = max(best, sum(t.priority for t in c))
    return best

def test_dp_matches_brute_force():
    for seed in range(20):
        tasks = generate_tasks(10, seed)
        assert weighted_job_scheduling(tasks)[0] == brute_force(tasks)

def test_dp_selection_valid():
    tasks = generate_tasks(200)
    best, sel = weighted_job_scheduling(tasks)
    assert no_overlap(sel)
    assert sum(t.priority for t in sel) == best

def test_greedy_activity_no_overlap():
    assert no_overlap(greedy_activity_selection(generate_tasks(500)))

def test_greedy_priority_respects_limits():
    sel = greedy_priority(generate_tasks(300), 50)
    assert no_overlap(sel)
    assert sum(t.resources for t in sel) <= 50

def test_dp_beats_greedy():
    tasks = generate_tasks(300)
    g = greedy_activity_selection(tasks)
    assert weighted_job_scheduling(tasks)[0] >= sum(t.priority for t in g)


from src.dp import weighted_job_scheduling_with_resources

def brute_force_res(tasks, limit):
    best = 0
    for r in range(len(tasks) + 1):
        for c in combinations(tasks, r):
            if no_overlap(c) and sum(t.resources for t in c) <= limit:
                best = max(best, sum(t.priority for t in c))
    return best

def test_dp_resources_matches_brute_force():
    for seed in range(15):
        tasks = generate_tasks(10, seed)
        for limit in (5, 15, 30):
            assert weighted_job_scheduling_with_resources(tasks, limit)[0] == brute_force_res(tasks, limit)

def test_dp_resources_selection_valid():
    tasks = generate_tasks(200)
    best, sel = weighted_job_scheduling_with_resources(tasks, 100)
    assert no_overlap(sel)
    assert sum(t.resources for t in sel) <= 100
    assert sum(t.priority for t in sel) == best

def test_dp_resources_beats_greedy_priority():
    tasks = generate_tasks(300)
    g = greedy_priority(tasks, 75)
    assert weighted_job_scheduling_with_resources(tasks, 75)[0] >= sum(t.priority for t in g)
