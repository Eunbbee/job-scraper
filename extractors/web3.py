from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv


class WebJobScraper:
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
                f"https://web3.career/{keyword}-jobs")

            for x in range(5):
                time.sleep(5)
                page.keyboard.down("End")

            content = page.content()
            soup = BeautifulSoup(content, "html.parser")

            jobs = soup.find("tbody", class_="tbody").find_all("tr")

            print("jobs found:", len(jobs))

            jobs_db = []

            for job in jobs:
                # 첫 번째 td 안의 a 태그가 title + link
                a_tag = job.find("td")
                if not a_tag:
                    continue

                link_tag = a_tag.find("a")
                if not link_tag:
                    continue

                title = link_tag.get_text(strip=True)
                link = "https://web3.career" + link_tag["href"]

                # 두 번째 td가 company
                company_td = job.find_all("td")[1] if len(
                    job.find_all("td")) > 1 else None
                company_name = company_td.get_text(
                    strip=True) if company_td else "N/A"

                # 세 번째 td가 location
                location_td = job.find_all("td")[3] if len(
                    job.find_all("td")) > 3 else None
                location = location_td.get_text(
                    strip=True) if location_td else "N/A"

                job = {
                    "type": "Web3",
                    "title": title.strip(),
                    "company_name": company_name.strip(),
                    "location": location.strip(),
                    "link": link
                }

                jobs_db.append(job)

            self.result = jobs_db
        # self.reset()
        return self.result


def extract_web_jobs(keyword):
    scraper = WebJobScraper()
    scraper.add_keyword(keyword)
    jobs = scraper.start()   # start() 안에서는 self.reset() 호출하지 않음
    scraper.reset()          # 한 번만 안전하게 Playwright 종료
    return jobs


# ref = WebJobScraper()
# ref.add_keyword("python")
# jobs = ref.start()  # start() 안에서 self.result에 저장 후 반환
# print("web3 jobs_db sample:", jobs[:5])
# ref.reset()
