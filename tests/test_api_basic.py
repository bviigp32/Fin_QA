import pytest
import requests
import time
import allure  

BASE_URL = "http://127.0.0.1:8000"

@allure.feature("API Basic Functional Test")  # 대분류
@allure.story("Server Health Check")          # 소분류
@allure.title("서버 상태 확인 (Health Check)")   # 보고서에 나올 테스트 이름
@allure.description("루트(/) 경로 호출 시 200 OK 응답을 확인합니다.") # 설명
@allure.severity(allure.severity_level.BLOCKER) # 중요도 (이거 안되면 배포 막음)
def test_health_check():
    with allure.step("1. 루트 경로 요청"):  # 스텝별 로그
        try:
            response = requests.get(f"{BASE_URL}/")
        except requests.exceptions.ConnectionError:
            pytest.fail("서버가 꺼져 있습니다!")

    with allure.step("2. Status Code 검증"):
        assert response.status_code == 200
        print("서버 생존 확인 완료!")

@allure.feature("API Basic Functional Test")
@allure.story("News List API")
@allure.title("뉴스 목록 조회 및 상태 검증")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_news_status():
    with allure.step("API 호출 (/news)"):
        response = requests.get(f"{BASE_URL}/news")
    
    with allure.step("응답 코드 확인"):
        if response.status_code != 200:
            allure.attach(response.text, name="Error Response", attachment_type=allure.attachment_type.TEXT)
        assert response.status_code == 200

@allure.feature("API Basic Functional Test")
@allure.story("Performance")
@allure.title("API 응답 속도(Latency) 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_api_latency():
    limit_time = 0.5
    
    with allure.step(f"API 호출 및 시간 측정 (기준: {limit_time}초)"):
        start_time = time.time()
        requests.get(f"{BASE_URL}/news?limit=5")
        end_time = time.time()
        duration = end_time - start_time
    
    with allure.step(f"결과 판정: {duration:.4f}초"):
        allure.attach(str(duration), name="Measured Latency", attachment_type=allure.attachment_type.TEXT)
        assert duration < limit_time