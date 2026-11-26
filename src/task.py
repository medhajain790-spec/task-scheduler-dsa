from dataclasses import dataclass

@dataclass
class Task:
    id: int
    start: int
    finish: int
    priority: int
    resources: int
