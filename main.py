import os
import re
import gc
import json
import fitz  # PyMuPDF
import easyocr
import pandas as pd
import torch
import whisper
from datetime import datetime
from konlpy.tag import Okt
from sentence_transformers import SentenceTransformer, util
from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL
from pathlib import Path
import logging
from supabase import create_client, Client

# [환경 설정]
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
BASE_PATH = Path("/Volumes/Macbook_dat/Python/CoreWorkWord")
MODEL_PATH = BASE_PATH / "ai_models"
UPLOAD_PATH = BASE_PATH / "uploads"
RESULT_PATH = BASE_PATH / "results"

# [Supabase 설정] 본인의 정보로 교체 필수
SUPABASE_URL = "https://kggpojguiwnzmikibhzn.supabase.co"
SUPABASE_KEY = "sb_publishable_rFVuNo9uGALWqk5cUIEoAw_lXR2S2jH"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class CoreWorkCloudAnalyzer:
    def __init__(self):
        logging.info("🚀 Korean Edu Factory v2.6 (DB-Ready) 엔진 초기화...")
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        
        # 1. AI 모델 로드
        self.embed_model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS').to(self.device)
        self.reader = easyocr.Reader(['ko', 'en'], gpu=(self.device == "mps"), model_storage_directory=str(MODEL_PATH))
        self.stt_model = whisper.load_model("base", device=self.device, download_root=str(MODEL_PATH))
        self.okt = Okt()
        
        # 2. 클라우드 마스터 DB 동기화 (임베딩 사전 계산)
        self._sync_db_embeddings()

    def _sync_db_embeddings(self):
        """Supabase에서 확정된 단어들을 가져와 벡터화하여 GPU 메모리에 상주"""
        response = supabase.table("industry_keywords").select("*").execute()
        self.db_df = pd.DataFrame(response.data)
        
        # 확정된(active) 데이터만 추출 (검토필요/대기 제외)
        confirmed_df = self.db_df[self.db_df['status'] == 'active'].reset_index(drop=True)
        
        if not confirmed_df.empty:
            with torch.no_grad():
                self.db_embeddings = self.embed_model.encode(
                    confirmed_df['term'].tolist(), convert_to_tensor=True
                ).to(self.device)
            self.confirmed_df = confirmed_df
        else:
            self.db_embeddings = None

    def classify_semantic(self, nouns):
        """Tensor Batch를 이용한 의미 기반 분류 (Threshold 0.65)"""
        if self.db_embeddings is None or not nouns:
            return ["일반/기타"] * len(nouns)
        
        results = []
        with torch.no_grad():
            input_embs = self.embed_model.encode(nouns, convert_to_tensor=True).to(self.device)
            cos_scores = util.cos_sim(input_embs, self.db_embeddings)
            top_scores, top_idxs = torch.max(cos_scores, dim=1)
            
            for i, score in enumerate(top_scores):
                if score > 0.65:
                    results.append(self.confirmed_df.iloc[top_idxs[i].item()]['sub_category'])
                else:
                    results.append("일반/기타")
        return results

    def upload_results(self, freq_df, source_info):
        """분석 결과 및 신규 단어를 Supabase에 업로드"""
        now = datetime.now().isoformat()
        
        # 1. 히스토리 기록 (analysis_history 테이블)
        history_rows = []
        for _, row in freq_df.iterrows():
            history_rows.append({
                "source_name": source_info['file'],
                "word": row['단어'],
                "frequency": int(row['빈도']),
                "category": row['분류'],
                "analyzed_at": now
            })
        if history_rows:
            supabase.table("analysis_history").insert(history_rows).execute()

        # 2. 신규 단어 마스터 DB(industry_keywords) 대기열 등록
        unknowns = freq_df[freq_df['분류'] == "일반/기타"]
        existing_terms = set(self.db_df['term'].tolist())
        new_entries = []
        
        for _, row in unknowns.iterrows():
            if row['단어'] not in existing_terms:
                new_entries.append({
                    "term": row['단어'],
                    "main_category": "미분류_대기",
                    "sub_category": "분류필요_대기",
                    "status": "candidate",
                    "source_type": source_info['type'],
                    "source_ref": source_info['file'],
                    "freq": int(row['빈도']),
                    "created_at": now,
                    "updated_at": now
                })
        
        if new_entries:
            supabase.table("industry_keywords").insert(new_entries).execute()
        logging.info(f"✅ 클라우드 업로드 완료: {source_info['file']}")

    def analyze_file(self, file_path):
        """파일별 분석 메인 파이프라인"""
        ext = file_path.suffix.lower()
        if ext == '.pdf':
            doc = fitz.open(file_path); text = " ".join([p.get_text() for p in doc]); doc.close()
            s_type = "pdf"
        elif ext in ['.jpg', '.png', '.jpeg']:
            text = " ".join(self.reader.readtext(str(file_path), detail=0))
            s_type = "image"
        else: return

        nouns = [n for n in self.okt.nouns(re.sub(r'[^가-힣\s]', '', text)) if len(n) > 1]
        if not nouns: return
        
        unique_nouns = list(set(nouns))
        classifications = self.classify_semantic(unique_nouns)
        mapping = dict(zip(unique_nouns, classifications))
        
        freq_df = pd.DataFrame(nouns, columns=['단어']).value_counts().reset_index()
        freq_df.columns = ['단어', '빈도']
        freq_df['분류'] = freq_df['단어'].map(mapping)
        
        self.upload_results(freq_df, {"type": s_type, "file": file_path.name})

def main():
    analyzer = CoreWorkCloudAnalyzer()
    for f in UPLOAD_PATH.glob('*'):
        if f.suffix.lower() in ['.pdf', '.jpg', '.png']:
            logging.info(f"📄 분석 중: {f.name}")
            analyzer.analyze_file(f)
    if torch.backends.mps.is_available(): torch.mps.empty_cache()

if __name__ == "__main__":
    main()
