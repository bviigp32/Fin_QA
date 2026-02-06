import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_ai_confidence_threshold():
    """
    [AI-001] AI 신뢰도(Confidence Score) 검증
    - AI가 내놓은 답변의 신뢰도가 기준치(Threshold)보다 낮으면 위험하다.
    - 여기서는 엄격하게 '0.90 (90%)' 이상인 경우만 통과시킨다.
    """
    print("\n[QA] AI 모델 신뢰도 측정 중...")
    
    # 20개 요청해서 신뢰도 분포 확인
    response = requests.get(f"{BASE_URL}/news?limit=20")
    assert response.status_code == 200
    news_list = response.json()["items"]
    
    low_confidence_items = []
    
    # 기준값 (Threshold) 설정 - 90% 미만은 불합격 처리
    MIN_SCORE = 0.90 

    for index, news in enumerate(news_list):
        score = news.get("confidence_score", 0.0)
        
        # 신뢰도가 기준보다 낮으면 적발
        if score < MIN_SCORE:
            print(f"[Warning] AI 확신 부족 (Index: {index})")
            print(f"   - Ticker: {news['ticker']}")
            print(f"   - 점수: {score} (기준: {MIN_SCORE})")
            
            low_confidence_items.append({
                "id": news['id'],
                "score": score
            })

    # 하나라도 기준 미달이면 테스트 실패
    if len(low_confidence_items) > 0:
        pytest.fail(f"총 {len(low_confidence_items)}건의 AI 결과가 신뢰도 기준({MIN_SCORE})에 미달했습니다!")
    else:
        print(f"모든 AI 결과가 높은 신뢰도({MIN_SCORE} 이상)를 보입니다.")

def test_ai_hallucination_check():
    """
    [AI-002] 환각(Hallucination) 의심 탐지 - 길이 체크
    - 상식적으로 '요약(Summary)'은 '원문(Content)'보다 짧아야 한다.
    - 만약 요약이 원문보다 길다면, AI가 없는 말을 지어낸 것으로 의심하고 Fail 처리한다.
    """
    print("\n[QA] AI 환각(Hallucination) 의심 검사...")
    
    response = requests.get(f"{BASE_URL}/news?limit=20")
    news_list = response.json()["items"]
    
    hallucination_cases = []

    for index, news in enumerate(news_list):
        content = news.get("content", "")
        summary = news.get("ai_summary", "")
        
        # 원문이 없거나 요약이 없으면 스킵 (다른 테스트에서 잡음)
        if not content or not summary:
            continue

        # 📏 길이 비교: 요약 > 원문
        if len(summary) > len(content):
            print(f"[Hallucination?] 요약이 원문보다 깁니다! (Index: {index})")
            print(f"   - 원문 길이: {len(content)}")
            print(f"   - 요약 길이: {len(summary)}")
            hallucination_cases.append(news['id'])

    if len(hallucination_cases) > 0:
        pytest.fail(f"총 {len(hallucination_cases)}건의 환각 의심 사례(요약 길이 초과)가 발견되었습니다.")
    else:
        print("AI 요약 길이가 정상 범위 내에 있습니다.")