"""Pure descriptive statistics primitives.

All functions operate on lists of numbers using only Python builtins.
No I/O, no exec, no subprocess, no external imports, no file operations.
"""

from __future__ import annotations


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of *values*.

    Raises ValueError if *values* is empty.
    """
    if not values:
        raise ValueError("mean() requires at least one value")
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    """Return the median of *values*.

    For an even-length list the average of the two middle values is returned.
    Raises ValueError if *values* is empty.
    """
    if not values:
        raise ValueError("median() requires at least one value")
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
    return float(sorted_vals[mid])


def mode(values: list[float]) -> float:
    """Return the most frequently occurring value in *values*.

    If multiple values tie for most frequent, returns the smallest.
    Raises ValueError if *values* is empty.
    """
    if not values:
        raise ValueError("mode() requires at least one value")
    counts: dict[float, int] = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    max_count = max(counts.values())
    # Among all values with the maximum count, return the smallest for determinism.
    return min(v for v, c in counts.items() if c == max_count)


def variance(values: list[float]) -> float:
    """Return the sample variance (Bessel-corrected, n-1 denominator) of *values*.

    Raises ValueError if *values* has fewer than 2 elements.
    """
    if len(values) < 2:
        raise ValueError("variance() requires at least 2 values")
    m = mean(values)
    return sum((v - m) ** 2 for v in values) / (len(values) - 1)


def stdev(values: list[float]) -> float:
    """Return the sample standard deviation of *values*.

    Raises ValueError if *values* has fewer than 2 elements.
    """
    return variance(values) ** 0.5


def percentile(values: list[float], p: float) -> float:
    """Return the p-th percentile of *values* using linear interpolation.

    *p* must be in [0, 100].
    Raises ValueError if *values* is empty or *p* is out of range.
    """
    if not values:
        raise ValueError("percentile() requires at least one value")
    if not (0 <= p <= 100):
        raise ValueError(f"p must be in [0, 100], got {p}")
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    index = (p / 100) * (n - 1)
    lo = int(index)
    hi = lo + 1
    if hi >= n:
        return float(sorted_vals[-1])
    frac = index - lo
    return sorted_vals[lo] + frac * (sorted_vals[hi] - sorted_vals[lo])
