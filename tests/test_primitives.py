import pytest
from stats.primitives import mean, median, mode, variance, stdev, percentile


class TestMean:
    def test_basic(self):
        assert mean([1, 2, 3, 4, 5]) == pytest.approx(3.0)

    def test_single(self):
        assert mean([7.0]) == pytest.approx(7.0)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            mean([])


class TestMedian:
    def test_odd_length(self):
        assert median([3, 1, 2]) == pytest.approx(2.0)

    def test_even_length(self):
        assert median([1, 2, 3, 4]) == pytest.approx(2.5)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            median([])


class TestMode:
    def test_single_mode(self):
        assert mode([1, 2, 2, 3]) == pytest.approx(2.0)

    def test_tie_returns_smallest(self):
        assert mode([1, 2]) == pytest.approx(1.0)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            mode([])


class TestVariance:
    def test_known(self):
        assert variance([2, 4, 4, 4, 5, 5, 7, 9]) == pytest.approx(4.571428, rel=1e-4)

    def test_one_value_raises(self):
        with pytest.raises(ValueError):
            variance([5])


class TestStdev:
    def test_basic(self):
        assert stdev([2, 4, 4, 4, 5, 5, 7, 9]) == pytest.approx(2.138, rel=1e-3)


class TestPercentile:
    def test_min_max(self):
        data = [1, 2, 3, 4, 5]
        assert percentile(data, 0) == pytest.approx(1.0)
        assert percentile(data, 100) == pytest.approx(5.0)

    def test_median_matches(self):
        data = [1, 2, 3, 4, 5]
        assert percentile(data, 50) == pytest.approx(median(data))

    def test_invalid_p_raises(self):
        with pytest.raises(ValueError):
            percentile([1, 2, 3], 101)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            percentile([], 50)
