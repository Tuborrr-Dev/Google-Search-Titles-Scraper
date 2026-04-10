from types import SimpleNamespace

from scraper_lib.captcha import is_captcha_page


def _fake_driver(page_source: str, current_url: str = "https://google.com/search?q=test"):
    return SimpleNamespace(page_source=page_source, current_url=current_url)


def test_detects_unusual_traffic():
    driver = _fake_driver("Our systems have detected unusual traffic from your network.")
    assert is_captcha_page(driver) is True


def test_detects_recaptcha_mention():
    driver = _fake_driver("Please complete the reCAPTCHA to continue.")
    assert is_captcha_page(driver) is True


def test_detects_sorry_url():
    driver = _fake_driver("<html>blocked</html>", current_url="https://www.google.com/sorry/index")
    assert is_captcha_page(driver) is True


def test_normal_results_page_is_not_captcha():
    driver = _fake_driver("<html><div id='rso'>results here</div></html>")
    assert is_captcha_page(driver) is False


# NOTE: uses SimpleNamespace to mock driver without Selenium dependency.
