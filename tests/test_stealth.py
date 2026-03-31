from scraper_lib import stealth


def test_human_delay_sleeps_within_requested_bounds(monkeypatch):
    captured = {}

    def fake_sleep(seconds):
        captured["seconds"] = seconds

    monkeypatch.setattr(stealth.time, "sleep", fake_sleep)

    stealth.human_delay(1.0, 2.0)

    assert 1.0 <= captured["seconds"] <= 2.0


def test_human_type_sends_each_character(monkeypatch):
    monkeypatch.setattr(stealth.time, "sleep", lambda seconds: None)

    sent = []

    class FakeElement:
        def send_keys(self, char):
            sent.append(char)

    stealth.human_type(FakeElement(), "abc")

    assert sent == ["a", "b", "c"]


# NOTE: monkeypatch replaces time.sleep for fast, deterministic tests.
