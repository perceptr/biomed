from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class StatisticsResult:
    total_users: int
    total_operators: int
    total_analyses: int
    analyses_status_counts: dict[str, int]
    top_5_cities: List[Tuple[str, int]]
