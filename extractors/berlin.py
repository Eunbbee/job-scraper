from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv


class BerlinJobScraper:
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
                f"https://berlinstartupjobs.com/skill-areas/{keyword}")

            for x in range(5):
                time.sleep(5)
                page.keyboard.down("End")

            content = page.content()
            soup = BeautifulSoup(content, "html.parser")

            jobs = soup.find("ul", class_="jobs-list-items").find_all("li")

            jobs_db = []

            for job in jobs:
                link = job.find("h4", class_="bjs-jlid__h").find("a")["href"]
                title = job.find(
                    "h4", class_="bjs-jlid__h").find("a").get_text(strip=True)
                company_name = job.find("a", class_="bjs-jlid__b").text
                # job_description = job.find(
                #     "div", class_="bjs-jlid__description").get_text(strip=True)

                job = {
                    "type": "Berlin",
                    "title": title.strip(),
                    "company_name": company_name.strip(),
                    "location": "N/A",
                    "link": link
                }

                jobs_db.append(job)

            self.result = jobs_db
        self.reset()
        return self.result


def extract_berlin_jobs(keyword):
    scraper = BerlinJobScraper()
    scraper.add_keyword(keyword)
    return scraper.start()


# ref = BerlinJobScraper()
# ref.add_keyword("python")
# jobs = ref.start()  # start() 안에서 self.result에 저장 후 반환
# print("berlin jobs_db sample:", jobs[:5])
# ref.reset()
