import random
from .task import Task

def generate_tasks(n, seed=42):
    random.seed(seed)
    tasks = []
    for i in range(n):
        start = random.randint(0, n * 2)
        tasks.append(Task(i, start, start + random.randint(1, 20),
                          random.randint(1, 100), random.randint(1, 10)))
    return tasks
