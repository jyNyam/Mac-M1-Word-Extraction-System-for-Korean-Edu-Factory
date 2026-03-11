
# CoreWorkWord: Root Industry On-Device AI Lexicon System

**CoreWorkWord**는 뿌리산업(용접, 주조, 금형 등) 현장의 은어 및 속어를 수집하여 KS 표준용어로 매핑하고, 외국인 근로자(E-9)를 위한 쉬운 해설과 안전 지시용어를 생성하는 **100% 로컬 자립형 데이터 자산화 시스템**입니다. v3.5 아키텍처는 외부 클라우드 API 의존성을 제거하고 **Apple Silicon(M1/M2/M3)** 기반의 온디바이스 추론으로 전환하여 데이터 주권과 경제성을 동시에 확보했습니다.

## 📌 Project Overview

산업 현장의 소통 장벽 해소 및 안전사고 예방을 위해 외부 데이터 유출이 없는 폐쇄형 AI 환경에서 산업 지식 베이스(Glossary)를 구축합니다.

* **Target**: 1차. 대한민국 뿌리산업 현장 관리자 및 외국인 근로자(E-9).
* **Core Value**:
* **Zero Cost**: 외부 API 호출 없이 로컬 LLM(Gemma 2) 활용.
* **Data Sovereignty**: 기업 내부 데이터 유출 0% 보장 (100% Offline).
* **High Reliability**: KS 표준(Ground Truth) 기반 검증 및 Human-in-the-Loop(HiTL) 결합.



## 💻 System Environment

* **Hardware**: MacBook Pro M1/M2/M3 (Apple Silicon 최적화).
* **Inference Engine**: Ollama (Model: `gemma2:2b`).
* **Acceleration**: Apple Metal Performance Shaders (MPS) 가속 활용.
* **Database**: SQLite3 (골든 데이터 보존 및 이력 관리).

## 🛠 Tech Stack

* **NLP/Extraction**: Mecab (고속 형태소 분석), KR-WordRank (핵심어 추출), KcBERT (유사도 기반 직무 분류).
* **Multi-modal**: EasyOCR (이미지 인식), pdfplumber (문서 파싱), OpenAI Whisper (현장 음성 전사).
* **AI Logic**: James Tiles Prompt Engineering Method (구조화된 페르소나 설계).
* **Language**: Python 3.12+.

## 📂 System Architecture

데이터의 흐름과 무결성을 보장하기 위해 5개 모듈로 분산 설계되었습니다.

1. **`config.py` (Knowledge Core)**: 산업별 핵심 키워드, KS 규격 코드, 법적 근거 등 지식 베이스(Ground Truth) 정의.
2. **`db_management.py` (The Vault)**: '골든 데이터 보호 쉴드' 로직 탑재 (인간 검수 완료 데이터의 AI 덮어쓰기 방지).
3. **`main.py` (ETL Processor)**: OCR/PDF/SNS 데이터에서 명사 추출 및 KcBERT 기반 직무 자동 분류.
4. **`smart_merge.py` (Local AI Engine)**: Ollama 기반 로컬 LLM을 통한 JSON 형태의 해설 및 안전 지시 명령 생성.
5. **`export_report.py` (Human-in-the-Loop)**: 검수용 엑셀 리포트 추출 및 '승인' 데이터의 DB 선순환 반영(Feedback Loop).

## 📦 Installation & Setup

### 1. Prerequisite (Apple Silicon)

M1 Mac의 GPU 가속과 KoNLPy 가동을 위해 JDK 및 환경 설정이 필요합니다.

```bash
# JDK 설치 및 심볼릭 링크 설정
brew install openjdk
sudo ln -sfn $(brew --prefix)/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk

# Mecab 엔진 및 사전 설치
brew install mecab mecab-ko-dic

# Ollama 설치 후 모델 다운로드
ollama pull gemma2:2b

```

### 2. Dependencies

```bash
pip install -U pandas openpyxl konlpy mecab-python3 easyocr pymupdf torch sentence-transformers ollama

```

## 🚀 Workflow (실행 가이드)

데이터 무결성을 위해 아래 순서대로 실행을 권장합니다.

1. **지식 베이스 초기화**: `python config.py` 실행으로 폴더 구조 및 Ground Truth 로드 확인.
2. **원천 데이터 투입**: `uploads/` 폴더에 분석할 원본 파일 업로드.
3. **데이터 추출 및 자동 분류**:
```bash
python main.py

```


4. **로컬 AI 분석 및 자산화**:
```bash
python smart_merge.py

```


5. **인간 검수 및 골든 데이터 승격**:
* `export_report.py` 실행 후 생성된 엑셀에서 '승인' 기입 후 저장.
* 피드백 로직을 통해 최종 데이터베이스(`is_verified=1`) 확정.



## 📝 Key Features

* **Anti-Hallucination**: KS 표준 규격 데이터와 AI 추론 결과를 교차 검증하여 환각 현상 억제.
* **Safety Command Implementation**: 현장 반장의 구어체(명령조)를 반영하여 실무 활용성 극대화.
* **Data Integrity**: `is_verified` 플래그를 통한 데이터 생애주기 관리.

---

**Maintainer**: Heo Jin-yeong (HR STANDARD).
**Specialty**: Korean Language Education & AI-driven Industrial Content Development.

---
