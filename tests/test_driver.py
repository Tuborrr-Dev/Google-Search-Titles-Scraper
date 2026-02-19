from scraper_lib.driver import USER_AGENTS, random_user_agent


def test_random_user_agent_returns_from_pool():
    for _ in range(20):
        assert random_user_agent() in USER_AGENTS


def test_user_agent_pool_is_non_trivial():
    # Rotation is pointless if there's only one string to rotate through.
    assert len(USER_AGENTS) >= 3
    assert len(set(USER_AGENTS)) == len(USER_AGENTS)
