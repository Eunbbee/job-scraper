from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time


class WwrJobScraper:
    BASE_URL = "https://weworkremotely.com"

    def __init__(self, headless=True):
        self.keywords = []
        self.results = []
        self.headless = headless

    def add_keyword(self, keyword):
        if isinstance(keyword, list):
            self.keywords.extend(keyword)
        elif isinstance(keyword, str):
            self.keywords.append(keyword)
        else:
            raise ValueError("keyword must be str or list")

        print(f"Keywords: {self.keywords}")

    def _auto_scroll(self, page, repeat=5):
        for _ in range(repeat):
            page.mouse.wheel(0, 3000)
            time.sleep(1)

    def start(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()

            for keyword in self.keywords:
                print(f"Scraping keyword: {keyword}")

                page.goto(
                    f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}",
                    timeout=60000
                )

                page.wait_for_selector("a[href^='/remote-jobs/']")
                self._auto_scroll(page)

                soup = BeautifulSoup(page.content(), "html.parser")

                jobs = soup.select("article ul li")

                for job in jobs:
                    link_tag = job.find("a", href=True)
                    if not link_tag or not link_tag['href'].startwith("/remote-jobs/"):
                        continue

                    title = job.find("span", class_="title")
                    company = job.find("span", class_="company")
                    location = job.find("span", class_="region")
                    link = job.find("a")["href"]

                    self.results.append({
                        "keyword": keyword,
                        "title": title.text.strip() if title else None,
                        "company": company.text.strip() if company else None,
                        "location": location.text.strip() if location else "Worldwide",
                        "link": self.BASE_URL + link
                    })

            browser.close()

        return self.results


def extract_wwr_jobs(keyword, headless=True):
    scraper = WwrJobScraper(headless=headless)
    scraper.add_keyword(keyword)
    return scraper.start()
