from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CacheDecision(str, Enum):
    MISS = "miss"
    FRESH = "fresh"
    STALE = "stale"
    STALE_IF_ERROR = "stale_if_error"


@dataclass(frozen=True)
class CachePolicy:
    """Freshness windows independent from any cache transport."""

    fresh_for: float
    stale_for: float = 0.0

    def __post_init__(self) -> None:
        if self.fresh_for < 0 or self.stale_for < 0:
            raise ValueError("fresh_for and stale_for must be non-negative")

    def decide(self, age: float | None, *, error: bool = False) -> CacheDecision:
        return decide(age, fresh_for=self.fresh_for, stale_for=self.stale_for, error=error)

    def remaining(self, age: float | None) -> float:
        if age is None:
            return 0.0
        return max(0.0, self.fresh_for - age)


def decide(age: float | None, *, fresh_for: float, stale_for: float = 0.0, error: bool = False) -> CacheDecision:
    if fresh_for < 0 or stale_for < 0:
        raise ValueError("fresh_for and stale_for must be non-negative")
    if age is None:
        return CacheDecision.MISS
    if age < 0:
        raise ValueError("age must be non-negative")
    if age <= fresh_for:
        return CacheDecision.FRESH
    if error and age <= fresh_for + stale_for:
        return CacheDecision.STALE_IF_ERROR
    if age <= fresh_for + stale_for:
        return CacheDecision.STALE
    return CacheDecision.MISS


def is_usable(decision: CacheDecision) -> bool:
    """Return whether a cached value may be served to a caller."""

    return decision in {CacheDecision.FRESH, CacheDecision.STALE, CacheDecision.STALE_IF_ERROR}
