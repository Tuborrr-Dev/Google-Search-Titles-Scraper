"""Core scraping logic against Google's search results page."""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .captcha import is_captcha_page
from .stealth import human_delay, human_type


def scrape(
    driver, query: str, max_pages: int, wait_seconds: float
) -> tuple[list[str], list[str | None]]:
    """Scrape up to `max_pages` of Google results for `query`.

    Returns (titles, urls) as parallel lists. Stops early (without raising)
    on a CAPTCHA page, a missing results container, or a missing 'next page'
    button -- callers should treat an empty result as "nothing usable was
    scraped", not necessarily an error.
    """
    page_titles: list[str] = []
    page_urls: list[str | None] = []

    driver.get("https://www.google.com")

    try:
        search_box = WebDriverWait(driver, wait_seconds).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
    except TimeoutException:
        print("Could not find the Google search box. The page layout may have "
              "changed, or Google may be showing a consent/CAPTCHA page.")
        return page_titles, page_urls

    human_type(search_box, query)
    human_delay(0.5, 1.5)
    search_box.send_keys(Keys.RETURN)

    pages_scraped = 0
    while pages_scraped < max_pages:
        human_delay()  # let the results page settle like a real visitor would

        if is_captcha_page(driver):
            print(f"Google served a CAPTCHA/'unusual traffic' page after "
                  f"{pages_scraped} page(s). Stopping.")
            break

        try:
            results = WebDriverWait(driver, wait_seconds).until(
                EC.presence_of_element_located((By.ID, "rso"))
            )
        except TimeoutException:
            print(f"No results container found on page {pages_scraped + 1}. Stopping.")
            break

        # NOTE: "MjjYud" / "LC20lb" are Google's current (undocumented, and
        # frequently changing) CSS class names for a result card / its title.
        # If this scraper stops finding results, this is the first place to check.
        result_blocks = results.find_elements(By.CLASS_NAME, "MjjYud")
        for block in result_blocks:
            try:
                title_el = block.find_element(By.CSS_SELECTOR, "h3.LC20lb")
            except Exception:
                continue  # not every block is an organic result card

            title_text = title_el.text.strip()
            if not title_text:
                continue

            try:
                url = block.find_element(By.TAG_NAME, "a").get_attribute("href")
            except Exception:
                url = None
                print(f"No link found for result: {title_text!r}")

            page_titles.append(title_text)
            page_urls.append(url)

        pages_scraped += 1

        if pages_scraped >= max_pages:
            break

        try:
            next_button = WebDriverWait(driver, wait_seconds).until(
                EC.element_to_be_clickable((By.ID, "pnnext"))
            )
        except TimeoutException:
            print(f"No 'next page' button found after {pages_scraped} page(s). "
                  "Reached the last page.")
            break

        next_button.click()

    return page_titles, page_urls
