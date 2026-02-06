# FinQA 테스트 시나리오 (Test Plan)

## 1. 개요
본 문서는 'AI 주식 뉴스 서비스'의 API 기능 검증 및 데이터 무결성 검증을 위한 테스트 케이스(TC)를 정의한다.

## 2. 테스트 환경
* **Target Server:** http://127.0.0.1:8000
* **Tools:** pytest, requests, pydantic

## 3. 테스트 케이스 (Test Cases)

| ID | 카테고리 | 테스트 항목 | 기대 결과 (Expected Result) | 중요도 |
| :--- | :--- | :--- | :--- | :--- |
| **API-001** | 서비스 QA | API 응답 상태 확인 | `/news` 호출 시 Status Code가 **200 OK**여야 한다. | High |
| **API-002** | 서비스 QA | 응답 시간(Latency) 측정 | API 응답 시간이 **500ms 이내**여야 한다. | Medium |
| **DATA-001** | 데이터 QA | 필수 필드 누락 검증 | `id`, `ticker`, `title` 필드는 **Null이 아니어야(Not None)** 한다. | High |
| **DATA-002** | 데이터 QA | 주가(Price) 로직 검증 | `price`는 반드시 **0보다 큰 양수**여야 한다. | High |
| **DATA-003** | 데이터 QA | 날짜(Date) 정합성 검증 | `published_at`은 **현재 시간보다 과거**여야 한다. (미래 날짜 불가) | Medium |
| **CNT-001** | 콘텐츠 QA | 비속어(Profanity) 필터링 | `content` 내에 욕설(*, f**k 등)이 포함되어서는 안 된다. | High |
| **AI-001** | AI QA | AI 신뢰도 검증 | `confidence_score`가 **0.7 미만**인 경우 경고(Warning) 처리한다. | Low |