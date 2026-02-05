# 🏭 Korean Edu Factory: Root Industry & KIIP AI Lexicon Analyzer (v3.0)

본 프로젝트는 MacBook Pro M1 환경의 로컬 컴퓨팅 자원과 Gemini 2.5 Pro의 추론 능력을 결합한 지능형 어휘 분석 시스템입니다.
산업 현장 문서(PDF/이미지) 및 SNS 콘텐츠(YouTube)에서 핵심 어휘를 추출하고, 이를 전문적인 기술 해설이 담긴 Glossary DB로 자산화하는 것을 목표로 합니다.

## 💻 시스템 환경 (Environment)

- **Hardware**: MacBook Pro M1 (GPU 가속 MPS 활용)
- **Storage**: External SSD (/Volumes/Macbook_dat/Python/CoreWorkWord)
- **Language**: Python 3.12+
- **Database**: SQLite3 (지속적 학습 및 데이터 누적)

## 🛠 주요 기술 스택 (Tech Stack)

- **NLP**: KoNLPy (Okt) - 형태소 분석을 통한 노이즈 제거 및 명사 정밀 추출
- **OCR**: EasyOCR - M1 GPU 가속 기반의 고성능 이미지 텍스트 인식
- **AI**: Google Gemini 2.5 Pro - 심층 구조화 프롬프트 기법 적용
- **Infra**: youtube-transcript-api, pdfplumber, python-dotenv, openpyxl

## 📂 프로젝트 구조 (Structure)

- **main.py**: 데이터 추출 엔진. OCR 및 유튜브 자막에서 명사를 추출하고 KoNLPy로 정제합니다.
- **db_manager.py**: 데이터 관리자. SQLite DB 연동, CRUD 처리 및 과거 분석 사례(Few-shot)를 관리합니다.
- **smart_merge_v3.py**: 지능형 분류기. Gemini 2.5 Pro를 통해 실무적 해설을 생성하고 DB에 동기화합니다.
- **glossary.db**: 분석된 모든 어휘와 해설이 누적되는 지식 베이스 파일입니다.
- **uploads/**: 분석 대상 원본 파일(PDF, JPG, PNG, TXT) 저장소입니다.
- **results/**: 중간 결과물(raw_cleaned.csv) 및 리포트가 저장됩니다.

## 📦 설치 및 실행 (Installation & Usage)

1. **시스템 의존성 설치**  
   KoNLPy 가동(JVM)을 위해 Java(JDK) 설치가 필수입니다.  

brew install openjdk
text

2. **라이브러리 설치**  
구형 SDK와의 충돌을 방지하기 위해 정리가 필요합니다.  

구형 SDK 제거
pip uninstall google-generativeai
필수 라이브러리 통합 설치
pip install -U google-genai pandas easyocr pdfplumber konlpy pynput python-dotenv youtube-transcript-api openpyxl
text

3. **실행 루틴**  
- uploads/ 폴더에 분석할 파일을 넣거나 sns_links.txt에 유튜브 주소를 입력합니다.
- `python main.py`를 실행하여 정제된 명사를 추출합니다.
- `python smart_merge_v3.py`를 실행하여 AI 심층 분석 및 DB 저장을 완료합니다.

## 🧠 지속적 유지보수 가이드 (Maintenance with AI)

이 프로젝트는 AI와의 협업을 통해 진화합니다. 기능 수정 시 아래 가이드를 활용하십시오.

- **프롬프트 고도화**: 분류 정확도를 높이려면 smart_merge_v3.py 내의 전문가 페르소나 및 분류 원칙 세션을 수정하십시오.
- **지속적 학습**: AI가 오답을 반복할 경우 db_manager.py의 upsert_word 로직에 예외 필터를 추가하거나 프롬프트에 '오답 사례'를 명시하십시오.
- **성능 최적화**: 대량 처리가 필요할 경우 main.py의 easyocr 배치 사이즈를 조정하여 M1 GPU 부하를 관리하십시오.

## 📝 포트폴리오 핵심 지표 (Key Insights)

| 지표 | 설명 |
|------|------|
| **정확성 (Accuracy)** | 뿌리산업 10대 핵심 기술(주조, 금형 등)을 명확히 정의하여 AI 분류의 환각(Hallucination) 현상을 차단함. |
| **공공성 (Public Value)** | 외국인 근로자를 타겟으로 KIIP 단계별 어휘를 구분하여 기술 교육과 사회 통합을 동시에 지원함. |
| **공정성 (Fairness)** | 특정 국적·문화에 대한 편견이나 혐오 표현이 배제되도록 프롬프트 내 윤리 지침을 강화함. |
| **신뢰성 (Reliability)** | DB 내 과거 우수 분석 데이터(Few-shot)를 프롬프트에 자동 주입하여 일관된 해설 품질을 유지함.|
| **데이터 자산화** | 단순 문서 분석을 넘어, 시간이 흐를수록 정교해지는 독자적인 산업 지식 베이스(Glossary DB)를 구축함.
