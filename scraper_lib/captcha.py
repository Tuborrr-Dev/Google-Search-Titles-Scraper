"""CAPTCHA / 'unusual traffic' page detection.

Kept as a standalone function (taking anything with `.page_source` and
`.current_url`) so it's testable without a real browser.
"""


def is_captcha_page(driver) -> bool:
    page = driver.page_source.lower()
    return (
        "unusual traffic" in page
        or "recaptcha" in page
        or "/sorry/" in driver.current_url
    )


# FIXME: add notification hook (email/Slack) when CAPTCHA is detected.
