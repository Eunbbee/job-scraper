# BLUEPRINT | DONT EDIT

import requests
from bs4 import BeautifulSoup

response = requests.get(
    "https://berlinstartupjobs.com/engineering/",
    headers={
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })

skills = ["python", "typescript", "javascript", "rust"]

# /BLUEPRINT

# 👇🏻 YOUR CODE 👇🏻:

headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 스크랩해서 정보 넣을 공간 빈 리스트로 만들어주기
all_jobs = []


# 스크랩하기
def scrape_page(url, skill=None):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    jobs = soup.find("ul", class_="jobs-list-items").find_all("li")

    for job in jobs:
        position = job.find(
            "h4", class_="bjs-jlid__h").find("a").get_text(strip=True)
        company_name = job.find("a", class_="bjs-jlid__b").text
        job_description = job.find(
            "div", class_="bjs-jlid__description").get_text(strip=True)
        link = job.find("h4", class_="bjs-jlid__h").find("a")["href"]

        all_jobs.append({
            "company": company_name,
            "position": position,
            "description": job_description,
            "link": link,
            "skill": skill
        })


# Pagination
def get_pages(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    buttons = len(
        soup.find("ul", class_="bsj-nav").find_all("a", class_="page-numbers"))
    return buttons


total_pages = get_pages("https://berlinstartupjobs.com/engineering/page/1/")

for x in range(total_pages):
    url = f"https://berlinstartupjobs.com/engineering/page/{x+1}/"
    scrape_page(url, skill="engineering")

# 스킬 스크래퍼
for skill in skills:
    url = f"https://berlinstartupjobs.com/skill-areas/{skill}/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    job_list = soup.find("ul", class_="jobs-list-items")

    if not job_list:
        print(f"No jobs found for skill: {skill} at {url}")
        continue

    scrape_page(url, skill=skill)


# 프린트해주기
for job in all_jobs:
    skill_info = job.get("skill", "N/A")
    print(f"""
    Skill: {skill_info}
    Company: {job['company']}
    Position: {job['position']}
    Description: {job['description']}
    Link: {job['link']}
    """)
    print("=" * 100)
# # /YOUR CODE
