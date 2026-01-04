from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv


class WwrJobScraper:
    def __init__(self, headless=True):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=False)
        self.keywords = []
        self.result = []

    def add_keyword(self, keyword):
        if isinstance(keyword, list) == True:
            self.keywords = keyword
        elif isinstance(keyword, str) == True:
            self.keywords.append(keyword)
        print(f"Keywords : {self.keywords}")

    def reset(self):
        self.keywords.clear()
        self.p.stop()

    def start(self):
        for keyword in self.keywords:
            print(f"Scraper {keyword}...")
            page = self.browser.new_page()
            page.goto(
                f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}")

            for x in range(5):
                time.sleep(5)
                page.keyboard.down("End")

            content = page.content()
            soup = BeautifulSoup(content, "html.parser")

            jobs = soup.select("section", class_="jobs")

            # print("jobs found:", len(jobs))

            jobs_db = []

            for job in jobs:
                listings = job.find_all(
                    "li", class_="new-listing-container feature") \
                    + job.find_all("div", class_="ew-listing")

                for li in listings:
                    a_tag = li.find("a", class_="listing-link--unlocked")
                    if not a_tag:
                        continue

                    href = a_tag["href"]
                    if "/remote-jobs/" not in href:
                        continue

                    link = f"https://weworkremotely.com{href}"

                    title = a_tag.find(
                        "h3", class_="new-listing__header__title").text
                    company_name = a_tag.find(
                        "p", class_="new-listing__company-name").text
                    location = a_tag.find(
                        "p", class_="new-listing__company-headquarters").text

                    job = {
                        "type": "WWR",
                        "title": title.strip(),
                        "company_name": company_name.strip(),
                        "location": location.strip(),
                        "link": link
                    }
                    jobs_db.append(job)

            self.result = jobs_db
        self.reset()
        return self.result


def extract_wwr_jobs(keyword):
    scraper = WwrJobScraper()
    scraper.add_keyword(keyword)
    return scraper.start()


# ref = WwrJobScraper()
# ref.add_keyword("python")
# ref.start()
