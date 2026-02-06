import pytest
import requests
from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional
from datetime import datetime

# 테스트 대상 URL
BASE_URL = "http://127.0.0.1:8000"

# ==========================================
# 1. 검증 규칙(Schema) 정의
# Pydantic을 사용해 '정상 데이터'의 기준을 세웁니다.
# ==========================================
class NewsSchema(BaseModel):
    id: str
    ticker: str
    price: float
    title: Optional[str]  # 일단 Optional로 두지만, 아래에서 필수 체크
    content: str
    published_at: str
    
    # 규칙 1: 제목(Title)은 절대 비어있으면 안 된다. (Null Check)
    @field_validator('title')
    def check_title_not_null(cls, v):
        if v is None:
            raise ValueError("제목(title)이 누락되었습니다! (Null Value)")
        return v

    # 규칙 2: 주가(Price)는 0보다 커야 한다. (Logic Check)
    @field_validator('price')
    def check_price_positive(cls, v):
        if v <= 0:
            raise ValueError(f"주가(price)가 0 이하일 수 없습니다: {v}")
        return v

    # 규칙 3: 발행일(published_at)은 미래일 수 없다. (Time Integrity)
    @field_validator('published_at')
    def check_date_past(cls, v):
        # 문자열을 날짜 객체로 변환
        news_date = datetime.fromisoformat(v)
        if news_date > datetime.now():
            raise ValueError(f"미래 날짜의 뉴스가 발견되었습니다: {v}")
        return v

# ==========================================
# 2. 테스트 케이스 구현
# ==========================================
def test_news_data_quality():
    """
    [DATA-001 ~ 003] 데이터 무결성 검증
    API에서 받아온 뉴스 리스트를 하나씩 Pydantic 모델에 넣어서
    규칙을 위반하는지 검사합니다.
    """
    print("\n[QA] 데이터 정밀 검수 시작 (Data Integrity Test)...")
    
    # API 호출 (뉴스 10개 요청)
    response = requests.get(f"{BASE_URL}/news?limit=10")
    assert response.status_code == 200
    
    news_list = response.json()["items"]
    error_count = 0
    
    # 전수 조사 (Loop)
    for index, news_item in enumerate(news_list):
        try:
            # 여기가 핵심! 데이터를 Schema에 강제로 끼워 맞춰봄
            NewsSchema(**news_item)
            
        except ValidationError as e:
            # 검증 실패 시 에러 내용을 출력하고 카운트 증가
            print(f"\n[Bug Found] 데이터 오류 발견! (Index: {index})")
            print(f"   - Ticker: {news_item.get('ticker')}")
            # 에러 메시지 깔끔하게 정리해서 출력
            for err in e.errors():
                print(f"   - 위반 항목: {err['loc'][0]}")
                print(f"   - 원인: {err['msg']}")
            error_count += 1

    # 만약 불량 데이터가 하나라도 있었다면 테스트 실패(Fail) 처리
    if error_count > 0:
        pytest.fail(f"총 {error_count}개의 데이터 결함(Bug)이 발견되었습니다!")
    else:
        print("모든 데이터가 무결합니다 (Perfect!)")