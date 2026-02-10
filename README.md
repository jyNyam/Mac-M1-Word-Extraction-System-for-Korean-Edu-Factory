

# 🏭 Korean Edu Factory: Root Industry & KIIP AI Lexicon Analyzer (v3.5)

**[프로젝트 개요]** 본 프로젝트는 **MacBook Pro M1 (Apple Silicon)**의 로컬 자원과 **Google Gemini 1.5 Flash**의 추론 능력을 결합한 **하이브리드 지능형 어휘 분석 시스템**입니다.

산업 현장 문서(PDF/이미지)에서 핵심 어휘를 추출하고, **① KS 표준 기반의 지식 필터링**, **② 현장 반장에 최적화된 페르소나**, **③ 인간 검수(Human-in-the-Loop)** 과정을 거쳐 외국인 근로자(E-9)를 위한 **고신뢰성 Glossary DB**로 자산화합니다.

---

## 💻 시스템 환경 (Environment)

* **Hardware**: MacBook Pro M1 (GPU 가속 MPS 활용)
* **Architecture**: Local Pre-processing (OCR/NLP) + Cloud Inference (Gemini API)
* **Storage**: External SSD (`/Volumes/Macbook_dat/Python/CoreWorkWord`)
* **Knowledge Base**: KS 표준 규격 및 산업안전보건법 기반 **Ground Truth** 탑재
* **Database**: SQLite3 (골든 데이터 보존 및 선순환 구조)

## 🛠 주요 기술 스택 (Tech Stack)

* **AI Engine**: `Google Gemini 1.5 Flash` - JSON Mode 강제 및 Temperature 제어로 환각 최소화
* **Prompt Eng**: **Method** - 페르소나 부여 및 구조화된 출력 설계
* **NLP**: `KoNLPy (Okt)` - 불용어 제거 및 산업 명사 정밀 추출
* **OCR**: `EasyOCR` - M1 Metal(MPS) 가속 기반의 텍스트 인식
* **Verification**: **3-Stage Filtering** (Ground Truth 매칭 → AI 추론 → 교차 검증)
* **Utils**: `pandas`, `openpyxl`, `python-dotenv`, `pdfplumber`

---

## 📂 프로젝트 구조 (Structure)

이 프로젝트는 **데이터의 흐름(Flow)**과 **무결성(Integrity)**을 중심으로 설계되었습니다.

* **`config.py` (Knowledge Core)**:
* 프로젝트 경로 설정 및 **Ground Truth(뿌리산업 지식 사전)** 정의.
* KS 규격 코드와 현장 키워드가 매핑된 기준점 역할.


* **`db_management.py` (The Vault)**:
* SQLite DB 스키마 관리 (`industrial_glossary`).
* **골든 데이터 보호 로직**: 사람이 검증한 데이터(`is_verified=1`)는 AI가 덮어쓰지 않도록 보호.


* **`main.py` (Miner)**:
* `uploads/` 폴더의 PDF/이미지에서 텍스트 추출.
* OCR 및 형태소 분석을 통해 1차 정제된 CSV 생성.


* **`smart_merge.py` (AI Brain)**:
* **하이브리드 분석 엔진**: KS 데이터 주입(RAG) + 제임스 타일즈 페르소나.
* JSON 파싱 방어 코드 및 신뢰도(상/중/하) 자동 산정.


* **`export_report.py` (Human Bridge)**:
* 검수가 필요한 데이터만 엑셀로 추출 및 승인된 데이터를 DB로 회귀(Feedback Loop).



---

## 📦 설치 및 실행 (Installation & Usage)

### 1. 시스템 의존성 설치

M1 환경에서의 KoNLPy 가동을 위해 Java(JDK)가 필요합니다.

```bash
brew install openjdk

```

### 2. 라이브러리 설치

최신 Gemini SDK와 데이터 처리 패키지를 설치합니다.

```bash
pip install -U google-generativeai pandas easyocr pdfplumber konlpy python-dotenv openpyxl

```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 Google API Key를 입력합니다.

```text
GOOGLE_API_KEY=your_api_key_here

```

### 4. 실행 루틴 (Workflow)

데이터 무결성을 위해 반드시 **아래 순서**대로 실행하십시오.

1. **초기화 (Config)**: 폴더 생성 및 지식 베이스 로드 확인
```bash
python config.py

```


2. **DB 구축 (Schema)**: 테이블 생성 (기존 데이터 보호)
```bash
python db_management.py

```


3. **데이터 추출 (Mining)**: `uploads/` 폴더 내 파일 분석
```bash
python main.py

```


4. **AI 분석 (Analysis)**: KS 기반 검증 및 자산화
```bash
python smart_merge.py

```


5. **검수 및 선순환 (Feedback)**: 엑셀 리포트 생성 및 DB 재반영
```bash
python export_report.py

```



---

## 🧠 핵심 차별화 포인트 (Key Insights)

| 지표 | 설명 |
| --- | --- |
| **🛡️ 환각 방지 (Anti-Hallucination)** | `config.py`에 정의된 **Ground Truth(KS 표준)**와 교차 검증하여 AI의 거짓 생성을 3단계로 차단함. |
| **💎 골든 데이터 (Golden Data)** | 인간이 검수한 데이터는 **'검증됨(Verified)'** 상태로 격상되어, 이후 AI가 재분석하더라도 변형되지 않도록 보호함. |
| **👷 안전 최우선 (Safety First)** | 최적의 페르소나를 통해 **현장 반장님의 "안전 지시(Command)"** 말투를 구현, 실무 적합성 강화. |
| **🔄 선순환 구조 (Human-in-the-Loop)** | [AI 분석] → [엑셀 검수] → [DB 재학습]으로 이어지는 사이클을 통해 데이터 품질이 지속적으로 향상됨. |
| **🌏 공공성 (Public Value)** | 외국인 근로자(E-9) 눈높이에 맞춘 '초등학생 수준의 해설'과 '일본어 잔재 병기'로 교육적 가치 실현. |

---

## 📝 유지보수 가이드 (Maintenance)

* **지식 확장**: 새로운 직무(예: 표면처리) 추가 시, `config.py`의 `ROOT_INDUSTRIES` 딕셔너리만 수정하면 됩니다.
* **프롬프트 튜닝**: `smart_merge.py` 내의 `prompt` 변수에서 대상 독자나 어조를 수정할 수 있습니다.
* **API 관리**: `smart_merge.py`에는 `time.sleep()`을 통한 부하 조절 기능이 포함되어 있습니다. 데이터 양에 따라 배치 사이즈(Default: 50)를 조절하세요.

> *이 프로젝트는 현장의 목소리와 AI의 기술을 연결하는 가교 역할을 수행합니다.*
