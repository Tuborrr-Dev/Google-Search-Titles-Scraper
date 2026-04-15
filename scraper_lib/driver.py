"""Chrome WebDriver construction, with a few basic anti-detection tweaks.

None of this defeats Google's bot detection outright -- it just avoids the
most obvious automated-browser fingerprints (default automation banner,
`navigator.webdriver`, a fixed default user-agent) so the scraper doesn't
get flagged on the very first request.
"""

import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

try:
    from webdriver_manager.chrome import ChromeDriverManager
    HAVE_WEBDRIVER_MANAGER = True
except ImportError:
    HAVE_WEBDRIVER_MANAGER = False


# A small, current pool of real desktop Chrome user-agents. Rotating among
# a handful of real strings is enough to avoid always presenting the exact
# same fingerprint; it is not meant to be an exhaustive or self-updating list.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
]


def random_user_agent() -> str:
    return random.choice(USER_AGENTS)


def build_driver(driver_path: str | None = None, headless: bool = False,
                  user_agent: str | None = None) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument(f"--user-agent={user_agent or random_user_agent()}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    if driver_path:
        service = Service(driver_path)
    elif HAVE_WEBDRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
    else:
        service = Service()  # fall back to chromedriver on PATH

    chrome_driver = webdriver.Chrome(service=service, options=options)

    try:
        # Patch navigator.webdriver before any page script runs, so it
        # doesn't read back as `true` to Google's detection scripts.
        chrome_driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
        )
    except Exception:
        pass  # non-Chromium driver or CDP unavailable; not fatal

    return chrome_driver


# TODO: consider adding proxy rotation for higher-volume scraping.


# REVIEWED: 2026-03-20 — user-agent rotation covers major platforms.
