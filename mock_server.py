from fastapi import FastAPI, HTTPException
from faker import Faker
import random
from datetime import datetime

app = FastAPI()
fake = Faker()

# 일부러 심어놓은 버그 리스트 
def generate_bad_news():
    error_type = random.choice(['null_title', 'negative_price', 'bad_word', 'future_date', 'normal'])
    
    news = {
        "id": fake.uuid4(),
        "ticker": random.choice(["AAPL", "TSLA", "GOOGL", "AMZN", "NVDA"]), # 정상 티커
        "price": round(random.uniform(100, 1000), 2),
        "title": fake.sentence(),
        "content": fake.text(),
        "ai_summary": "Positive outlook based on recent earnings.",
        "published_at": datetime.now().isoformat(),
        "confidence_score": round(random.uniform(0.8, 0.99), 2)
    }

    # 랜덤하게 버그 주입 (QA 테스트용)
    if error_type == 'null_title':
        news['title'] = None  # 제목 누락 (Content Error)
    
    elif error_type == 'negative_price':
        news['price'] = -500.00  # 주가가 마이너스? (Logic Error)
    
    elif error_type == 'bad_word':
        news['content'] = "This stock is sh*t and f**k."  # 비속어 포함 (Content Quality Error)
    
    elif error_type == 'future_date':
        news['published_at'] = "2099-12-31T00:00:00"  # 미래 날짜 (Data Integrity Error)
    
    return news

@app.get("/")
def read_root():
    return {"status": "FinQA Mock Server is Running!"}

@app.get("/news")
def get_news(limit: int = 10):
    """
    가짜 주식 뉴스를 반환하는 API.
    주의: 간헐적으로 '쓰레기 데이터'가 섞여서 나옴.
    """
    # 10% 확률로 서버 에러(500) 발생 시뮬레이션
    if random.random() < 0.1:
        raise HTTPException(status_code=500, detail="Internal Server Error (Simulated)")

    data = [generate_bad_news() for _ in range(limit)]
    return {"total": limit, "items": data}