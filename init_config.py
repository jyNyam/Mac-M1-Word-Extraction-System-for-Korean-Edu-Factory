import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_PATH = Path("/Volumes/Macbook_dat/Python/CoreWorkWord")
CONFIG_PATH = BASE_PATH / "config"
CONFIG_PATH.mkdir(parents=True, exist_ok=True)

# 초기 마스터 데이터 정의
initial_data = {
    "뿌리산업": {
        "주조": ["쇳물", "용탕", "주물", "도가니", "사형주조", "응고"],
        "금형": ["파팅라인", "코어", "캐비티", "가이드핀", "밀핀"],
        "열처리": ["담금질", "뜨임", "풀림", "불림", "가열로", "퀜칭", "냉각"]
    },
    "사회통합": {
        "KIIP_0~2단계": ["이름", "인사", "가족", "음식"],
        "KIIP_3~4단계": ["취업", "면접", "이력서", "경제"]
    }
}

rows = []
curr_id = 1
now = datetime.now().isoformat()

for m_cat, sub_dict in initial_data.items():
    for s_cat, words in sub_dict.items():
        for word in words:
            rows.append({
                "id": curr_id,
                "term": word,
                "main_category": m_cat,
                "sub_category": s_cat,
                "status": "active",       # 초기 데이터는 활성 상태
                "source_type": "manual",  # 초기 수동 등록
                "source_ref": "init_config.py",
                "freq": 0,
                "similarity": 1.0,
                "analyzed_at": now,
                "created_at": now,
                "updated_at": now
            })
            curr_id += 1

# DB 규격 엑셀 생성
df = pd.DataFrame(rows)
df.to_excel(CONFIG_PATH / "industry_keywords.xlsx", index=False)
print(f"✅ DB-Ready 마스터 테이블 생성 완료 (총 {len(df)} 레코드)")
