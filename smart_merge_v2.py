import pandas as pd
import torch
import logging
from datetime import datetime
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer, util

# [설정]
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
SUPABASE_URL = "https://kggpojguiwnzmikibhzn.supabase.co"
SUPABASE_KEY = "sb_publishable_rFVuNo9uGALWqk5cUIEoAw_lXR2S2jH"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def cloud_smart_merge_v26():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS').to(device)
    now = datetime.now().isoformat()

    # 1. 클라우드에서 '대기(candidate)' 단어만 가져오기
    response = supabase.table("industry_keywords").select("*").eq("status", "candidate").execute()
    pending_items = response.data
    if not pending_items:
        logging.info("✨ 분석할 신규 단어가 없습니다.")
        return

    # 2. 카테고리별 시맨틱 대표 벡터 생성
    full_db = supabase.table("industry_keywords").select("*").execute()
    df_db = pd.DataFrame(full_db.data)
    confirmed_df = df_db[df_db['status'] == 'active']
    
    cat_reps = {}
    for cat in confirmed_df['sub_category'].unique():
        words = confirmed_df[confirmed_df['sub_category'] == cat]['term'].tolist()
        w_embs = model.encode(words, convert_to_tensor=True)
        c_emb = model.encode(cat, convert_to_tensor=True)
        cat_reps[cat] = 0.7 * w_embs.mean(dim=0) + 0.3 * c_emb # 이름 가중치 부여

    cat_list = list(cat_reps.keys())
    cat_tensor = torch.stack(list(cat_reps.values()))

    # 3. 신규 단어 AI 분류 및 클라우드 업데이트
    logging.info(f"🔎 {len(pending_items)}건의 신규 단어 AI 시맨틱 매칭 시작...")
    
    for item in pending_items:
        word_emb = model.encode(item['term'], convert_to_tensor=True)
        scores = util.cos_sim(word_emb, cat_tensor)[0]
        top_val, top_idx = torch.max(scores, dim=0)
        
        suggested_sub = cat_list[top_idx.item()]
        # 해당 중분류가 속한 대분류 찾기
        suggested_main = confirmed_df[confirmed_df['sub_category'] == suggested_sub]['main_category'].iloc[0]
        
        # [DB 업데이트] status를 auto_labeled로 변경하고 추천값 기록
        supabase.table("industry_keywords").update({
            "main_category": suggested_main,
            "sub_category": f"검토필요({suggested_sub})",
            "status": "auto_labeled",
            "similarity": round(float(top_val), 4),
            "updated_at": now
        }).eq("id", item['id']).execute()

    logging.info(f"✅ 클라우드 DB 최적화 완료. 이제 관리자 페이지에서 검토하세요.")

if __name__ == "__main__":
    cloud_smart_merge_v26()
