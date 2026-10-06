from stats import cache


class FakeRedis:
    """Minimal stand-in so the tests need no server."""

    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value


def test_store_then_lookup_returns_the_recorded_value():
    conn = FakeRedis()
    cache.store("mean", [1.0, 2.0, 3.0], 2.0, client=conn)
    assert cache.lookup("mean", [1.0, 2.0, 3.0], client=conn) == 2.0


def test_lookup_returns_none_for_an_unseen_call():
    assert cache.lookup("median", [4.0, 5.0], client=FakeRedis()) is None


def test_different_inputs_do_not_collide():
    conn = FakeRedis()
    cache.store("mean", [1.0], 1.0, client=conn)
    assert cache.lookup("mean", [2.0], client=conn) is None


def test_cache_is_disabled_without_a_configured_server(monkeypatch):
    monkeypatch.delenv("STATS_CACHE_URL", raising=False)
    assert cache.lookup("mean", [1.0]) is None
