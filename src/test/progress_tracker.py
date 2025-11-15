from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class TestRecord:
    passed: bool
    points: float


class TestProgressTracker:
    _results: Dict[str, TestRecord] = {}
    _metrics: Dict[str, float] = {}
    _objects: Dict[str, object] = {}

    SINGLE_DIVIDER = "-" * 50
    DOUBLE_DIVIDER = "=" * 50

    @classmethod
    def record(cls, label: str, passed: bool, points: float) -> None:
        cls._results[label] = TestRecord(passed=passed, points=points)

    @classmethod
    def store_metric(cls, key: str, value: float) -> None:
        cls._metrics[key] = value

    @classmethod
    def get_metric(cls, key: str, default: float = float("nan")) -> float:
        return cls._metrics.get(key, default)

    @classmethod
    def store_object(cls, key: str, value: object) -> None:
        cls._objects[key] = value

    @classmethod
    def get_object(cls, key: str) -> Optional[object]:
        return cls._objects.get(key)

    @classmethod
    def passed_count(cls) -> int:
        return sum(1 for record in cls._results.values() if record.passed)

    @classmethod
    def points_earned(cls) -> float:
        return sum(record.points for record in cls._results.values() if record.passed)
