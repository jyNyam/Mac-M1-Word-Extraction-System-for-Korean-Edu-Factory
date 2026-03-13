
---

# 🏭 CoreWorkWord: Root Industry On-Device AI Lexicon System (v3.5)

**현장의 거친 언어를 안전의 언어로 정제합니다.** CoreWorkWord는 뿌리산업(용접, 주조, 금형 등) 현장에서 통용되는 은어와 속어를 수집하여 KS 표준어로 매핑하고, 외국인 근로자(E-9)를 위한 직관적인 안전 지시어와 해설을 생성하는 **100% 온디바이스 AI 자산화 시스템**입니다.

클라우드 API의 경제적 부담과 데이터 유출 리스크를 완전히 제거하기 위해, v3.5 아키텍처는 **Apple Silicon(M1/M2/M3)** 자원을 극한으로 활용하는 폐쇄형 구조를 채택했습니다.

---

## 📌 Project Overview

산업 현장의 소통 장벽은 단순한 오해를 넘어 중대재해로 이어집니다. 우리는 외부 통신 없이도 현장에서 즉시 가동되는 지식 베이스(Glossary)를 지향합니다.

* **Target**: 1차 타겟은 대한민국 뿌리산업 현장 관리자 및 외국인 근로자(E-9)입니다.
* **Core Value**:
* **Zero Cost**: 운영비 0원을 목표로 로컬 LLM(**Gemma 2**)을 최적화했습니다.
* **Data Sovereignty**: "데이터가 공장을 떠나지 않게 하라." 100% Offline 환경을 구축했습니다.
* **High Reliability**: AI의 환각을 방지하기 위해 KS 표준(**Ground Truth**) 검증 알고리즘과 인간 검수(**HiTL**)를 결합했습니다.



---

## 💻 System Environment

* **Hardware**: MacBook Pro M1/M2/M3 (Apple Silicon 전용 최적화)
* **Inference Engine**: Ollama (Model: `gemma2:2b`)
* **Acceleration**: Apple Metal Performance Shaders (**MPS**) 가속 활용
* **Database**: SQLite3 (**Golden Data Shield** 로직 적용)

---

## 🛠 Tech Stack & Engineering Choices

단순히 최신 라이브러리를 나열하는 대신, 안정성을 위해 우리가 선택한 도구들입니다.

| 카테고리 | 도구 | 선정 이유 및 통찰 |
| --- | --- | --- |
| **Inference** | **Ollama / Gemma 2** | M1 8GB 메모리 환경에서도 안정적으로 돌아가는 최적의 파라미터 타협점. |
| **NLP** | **MeCab / KcBERT** | KoNLPy 중 가장 속도가 빠른 MeCab을 채택, 문맥 이해를 위해 KcBERT를 결합. |
| **Vision** | **EasyOCR / 4.9.0.80** | **[Strategic Choice]** 최신 OpenCV(4.13+)의 의존성 충돌을 피하기 위해 검증된 4.9.0.80 버전으로 '의도적 다운그레이드' 단행. |
| **Package** | **Poetry** | **[Why Poetry?]** `requirements.txt`의 버전 꼬임 문제를 해결하고, 어떤 환경에서도 동일하게 빌드되는 '결정론적 빌드'를 위해 도입. |

---

## 📂 System Architecture

데이터의 무결성을 보장하기 위해 각 모듈이 유기적으로 연결된 5공정 파이프라인입니다.

1. **`config.py` (The Brain)**: KS 규격 코드와 법적 근거를 담은 프로젝트의 '설계 원본'.
2. **`db_management.py` (The Vault)**: 인간이 검수한 '골든 데이터'를 AI가 다시 덮어쓰지 못하도록 막는 보호 쉴드 가동.
3. **`main.py` (Miner)**: OCR 및 형태소 분석을 통해 원재료(현장 문서)에서 유효한 명사를 채굴.
4. **`smart_merge.py` (Synthesizer)**: 페르소나를 입힌 로컬 AI가 상황별 안전 명령과 해설을 합성.
5. **`export_report.py` (Bridge)**: 인간 검수자가 엑셀을 통해 최종 '승인'을 내리는 피드백 루프 완성.

---

## 📦 Installation & Setup

### 1. Prerequisite (Infrastructure)

M1 Mac의 성능을 100% 끌어내기 위한 기반 공사입니다.

```bash
# JDK 설치 및 시스템 경로 연결 (KoNLPy 구동을 위한 JVM 환경 구축)
brew install openjdk
sudo ln -sfn $(brew --prefix)/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk

# MeCab 엔진 및 한국어 사전 설치 (속도 중시 세팅)
brew install mecab mecab-ko-dic

# Ollama 로컬 모델 다운로드
ollama pull gemma2:2b

```

### 2. Dependency Management (The Poetry Way)

우리는 라이브러리 간 간섭을 원천 차단하기 위해 **Conda**로 환경을 만들고 **Poetry**로 버전을 고정합니다.

```bash
# Conda 환경 생성 후 Poetry 초기화
conda create -n corework_stable python=3.12 -y
conda activate corework_stable

# 엄격한 버전 관리가 적용된 패키지 설치
# OpenCV 4.9 버전 고정으로 런타임 에러 사전 차단
poetry add numpy==1.26.4 pandas==2.2.1 opencv-python-headless==4.9.0.80 \
           konlpy==0.6.0 mecab-python3==1.0.8 easyocr==1.7.1 "torch>=2.2.0"
poetry lock --no-update && poetry install

```

---

## 🚀 Workflow (실행 가이드)

공정의 선후 관계를 지키는 것이 데이터 무결성의 핵심입니다.

1. **전원 가동**: `conda activate corework_stable`
2. **안전 점검**: `poetry run python check_integrity.py` (모든 부품이 ✅인지 확인)
3. **부지 조성**: `python config.py` (필수 디렉토리 자동 생성)
4. **창고 짓기**: `python db_management.py` (DB 스키마 초기화)
5. **데이터 채굴**: `python main.py` (uploads/ 폴더의 문서를 분석하여 원천 데이터 추출)
6. **AI 가공**: `python smart_merge.py` (로컬 LLM이 실무형 지식으로 변환)
7. **최종 검수**: `python export_report.py` (엑셀을 통해 골든 데이터 확정)

---

## 📝 Key Features (Deep Dive)

* **Anti-Hallucination**: AI가 아는 척하지 않도록 `config.py`에 정의된 KS 표준 데이터와 실시간으로 대조합니다.
* **Safety Command Implementation**: "안전모를 착용하세요" 대신 현장 반장님의 투박하지만 명확한 어조(**"안전모 써!"**)를 반영해 실무 적합성을 높였습니다.
* **Data Integrity**: `is_verified` 플래그를 통해 데이터의 생애주기를 관리하며, 검증된 자산은 AI의 간섭으로부터 독립됩니다.

---

**Maintainer**: Heo Jin-yeong (HR STANDARD)

**Specialty**: Korean Language Education & AI-driven Industrial Content Development

---

