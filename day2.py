# 딕셔너리
# 딕셔너리란 "이름표(key)"와 "내용(value)"가 짝을 이뤄 저장되는 자료형이야!
# 쉽게 말하면, "누구=무엇" 식으로 저장하는 상자!
# 딕셔너리 구조" {"키": 값, "키": 값, .... }

# person = {
#     "이름": "이비",
#     "나이": 10,
#     "좋아하는 것": "파이썬"
# }

# student = {
#     "이름": "영희",
#     "성적": 95
# }

# print(student["이름"])
# print(person["이름"], person["나이"])

# student["성적"] = 100 # 값 변경
# student["이름"] = "루디"
# student["반"] = 3

# print(student.keys())
# print(student.values())
# print(student.get("키없음", "없음"))

# my_info = {
#     "이름": "이비",
#     "나이": "20",
#     "좋아하는 것": "명상"
# }

# print("이름:", my_info["이름"])
# print("나이:", my_info["나이"])
# print("좋아하는 것:", my_info["좋아하는 것"])


# animals = {}
# animals["강아지"] = "멍멍"
# animals["고양이"] = "야옹"

# print(animals)


# BLUEPRINT | DONT EDIT

from requests import get
import requests

movie_ids = [
    238, 680, 550, 185, 641, 515042, 152532, 120467, 872585, 906126, 840430
]

# /BLUEPRINT

# 👇🏻 YOUR CODE 👇🏻:
# 각 아이디 통과하여 API 에서 영화의 세부 정보를 가져오는 for loop 를 만드는 것
# 사용하는 API 는 https://nomad-movies.nomadcoders.workers.dev/movies/XXXX 이며, 여기서 XXXX 는 영화 ID 임
# 예를 들어, 아이디가 508883 인 동영상의 세부정보를 얻으려면, 다음 URL 을 요청합니다. https://nomad-movies.nomadcoders.workers.dev/movies/508883 (응답을 보려면 해당 URL 로 이동).

# data는 영화의 세부정보가 포함된 dictionary임 (빈 딕셔너리 만들어주기)
data = {}

for movie_id in movie_ids:
    response = requests.get(
        f"https://nomad-movies.nomadcoders.workers.dev/movies/{movie_id}")
    data = response.json()

    print(
        f" - Title: {data['title']}\n - Overview: {data['overview']}\n - Vote Average: {data['vote_average']}\n")
    # /YOUR CODE
