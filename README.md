# FinQA: AI Financial News QA System

> **"잘못된 금융 정보는 고객의 자산에 치명적입니다."**
> AI 기반 주식 뉴스 서비스의 데이터 정합성(Integrity)과 API 안정성을 검증하는 **자동화된 QA 파이프라인 구축 프로젝트**입니다.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python) ![FastAPI](https://img.shields.io/badge/FastAPI-Mock%20Server-009688?logo=fastapi) ![Pytest](https://img.shields.io/badge/Pytest-Automation-yellow?logo=pytest) ![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Automation-2088FF?logo=githubactions)

## 프로젝트 개요
실제 운영 환경과 유사한 **결함(Bug)이 포함된 모의 서버(Mock Server)**를 구축하고, 이에 대한 **테스트 자동화(Test Automation)**를 수행합니다.
단순 기능 테스트를 넘어, 금융 데이터의 논리적 오류와 AI 모델의 결과 품질까지 검증하는 것을 목표로 합니다.

## 개발 로그 (7-Day Challenge)
* **Day 1: 테스트 환경 구축 & 설계**
    * `FastAPI`를 활용한 결함 주입 모의 서버(`mock_server.py`) 개발
    * 테스트 시나리오(TC) 및 검증 전략 수립 (`TEST_PLAN.md`)
* **Day 2: API 기능 테스트 (Functional QA)**
    * `tests/test_api_basic.py` 작성
    * `pytest`를 활용한 Status Code(200) 및 Latency(500ms) 자동 검증 구현
* **Day 3: 데이터 무결성 검증 (Data Integrity)**
    * `tests/test_data_integrity.py` 작성
    * `Pydantic` Schema를 활용하여 Null 값, 음수 가격, 미래 날짜 등 논리적 오류 자동 탐지
* **Day 4: VOC 기반 시나리오 테스트 (Content QA)**
    * `tests/test_content_quality.py` 작성
    * 고객 불만(VOC) 시나리오 반영: 뉴스 본문 내 비속어(Profanity) 자동 탐지 및 필터링 테스트 구현
* **Day 5: AI 서비스 품질 검증 (AI QA)**
    * `tests/test_ai_quality.py` 작성
    * AI 신뢰도(Confidence Score) 임계값 테스트 및 Hallucination(길이 기반) 탐지 로직 구현
* **Day 6: 리포팅 자동화 (Allure Report)**
    * `allure-pytest` 연동 및 테스트 코드에 메타데이터(`@allure.feature`, `@allure.step`) 적용
    * 테스트 실행 결과를 시각화된 웹 대시보드로 생성하여 가독성 확보
* **Day 7:** CI/CD 파이프라인 구축 (GitHub Actions)
  * `push` 이벤트 발생 시 자동으로 서버 구동 및 전체 테스트 수행 환경 구축

## 기술 스택 (Tech Stack)
| Category | Technology | Usage |
| :--- | :--- | :--- |
| **Language** | Python 3.11 | 전체 로직 구현 |
| **Target Server** | **FastAPI** | 테스트 대상(SUT) 및 버그 시뮬레이션 |
| **Testing** | **Pytest** | 테스트 케이스 작성 및 실행 |
| **Validation** | Pydantic | 데이터 스키마 검증 |
| **Reporting** | Allure | 테스트 결과 시각화 |

## 실행 방법 (How to Run)
```bash
# 1. 가상환경 활성화
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate

# 2. 필수 라이브러리 설치
pip install -r requirements.txt  # (추후 생성 예정)

# 3. 모의 서버(Mock Server) 실행
python -m uvicorn mock_server:app --reload
# -> [http://127.0.0.1:8000/news](http://127.0.0.1:8000/news) 접속 시 가짜 뉴스 데이터 반환

```

## 프로젝트 성과
* **금융 도메인 특화 QA:** 주가 데이터의 음수 방지, 미래 날짜 방지 등 도메인 로직 검증 구현.
* **AI 품질 보증:** 단순 기능 점검을 넘어, AI 모델의 신뢰도(Confidence)와 환각(Hallucination) 현상을 탐지하는 고급 테스트 케이스 설계.
* **완전 자동화:** GitHub Actions를 도입하여, 코드 변경 시마다 즉각적인 품질 피드백 루프(Feedback Loop) 형성.

---

*Created by [Kim Kyunghun]*
