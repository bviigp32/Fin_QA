import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

# 금칙어 리스트 (Blacklist)
# 실제 현업에서는 DB나 별도 파일로 관리하지만, 여기선 리스트로 정의합니다.
BANNED_WORDS = ["sh*t", "f**k", "damn", "trash"]

def test_no_profanity_in_content():
    """
    [CNT-001] 콘텐츠 비속어(Profanity) 필터링 테스트
    - 뉴스 본문(content)에 금칙어가 포함되어 있으면 안 된다.
    - 대소문자를 구분하지 않고 검사한다.
    """
    print("\n[QA] 콘텐츠 유해성 검사 시작 (Profanity Check)...")
    
    # 데이터 많이 요청 (20개) -> 버그 걸릴 확률 높이기
    response = requests.get(f"{BASE_URL}/news?limit=20")
    assert response.status_code == 200
    
    news_list = response.json()["items"]
    caught_bad_words = []

    for index, news in enumerate(news_list):
        content = news.get("content", "")
        
        # 본문이 비어있으면 패스 (이건 Day 3의 Null 체크에서 잡을 문제)
        if not content:
            continue

        # 🔍 금칙어 스캔 로직
        for bad_word in BANNED_WORDS:
            # 대소문자 무시하고 비교 (lower())
            if bad_word in content.lower():
                print(f"\n[Catch!] 비속어 발견 (Index: {index})")
                print(f"   - Ticker: {news['ticker']}")
                print(f"   - 금칙어: '{bad_word}'")
                print(f"   - 원문: \"{content}\"")
                
                caught_bad_words.append({
                    "id": news['id'],
                    "word": bad_word,
                    "content": content
                })
                break # 한 뉴스에 욕이 여러 개여도 한 번만 걸리면 됨

    # 결과 판정
    if len(caught_bad_words) > 0:
        pytest.fail(f"총 {len(caught_bad_words)}건의 유해 콘텐츠가 발견되었습니다! 배포 불가!")
    else:
        print("클린한 뉴스입니다. (Clean Content)")