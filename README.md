# Intelligent Task Scheduling and Resource Allocation

Greedy vs Dynamic Programming approaches for scheduling tasks with start/finish times, priorities and resource limits.

## Setup
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt

## Run
    python -m src.benchmark   # runtime comparison table + results/runtime_comparison.png
    python -m pytest -q       # run tests

## Algorithms
- Greedy (activity selection): earliest finish first, O(n log n), maximizes number of tasks
- Greedy (priority): best priority/resource ratio first within the resource limit, O(n^2) due to overlap check
- DP (weighted job scheduling): maximizes total priority, O(n log n), optimal but ignores resource limit
- DP with resources: optimal under both overlap and resource constraints, O(n*R)

## Results
- results/runtime_comparison.png: runtime vs number of tasks
- results/fair_comparison.txt: Greedy (priority) vs DP under the same resource limit

## Key findings
- DP gives 0.6-5% higher priority under tight resource limits and 21-26% under loose limits
- Greedy (priority) is much faster (6.8 ms vs 389 ms at n=1000, R=1000) but not optimal
- DP uses ~100% of available resources, greedy only 57-69% when the limit is loose
# task-scheduler-dsa
