#!/usr/bin/env python3
"""
FastAPI バックエンドサーバー
音声ファイルのアップロードと文字起こし処理を提供
"""

import os
import sys
import time
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# transcribe.py をインポート
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.transcribe import transcribe_audio

app = FastAPI(title="Whisper Transcription API")

# CORS設定 - React フロントエンドからのアクセスを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptionResponse(BaseModel):
    """文字起こし結果のレスポンスモデル"""
    text: str
    fileName: str
    processingTime: float
    segments: Optional[list] = None

# サポートされている音声ファイル形式
SUPPORTED_FORMATS = {
    ".mp3", ".wav", ".m4a", ".ogg", ".flac", 
    ".aac", ".wma", ".mp4", ".avi", ".mov"
}

@app.get("/")
async def root():
    """ヘルスチェックエンドポイント"""
    return {"status": "ok", "message": "Whisper Transcription API is running"}

@app.post("/api/transcribe", response_model=TranscriptionResponse)
async def transcribe(
    file: UploadFile = File(...),
    model: str = Form("base"),
    language: Optional[str] = Form(None)
):
    """
    音声ファイルを文字起こしするエンドポイント
    
    Parameters:
        file: アップロードされた音声ファイル
        model: Whisperモデル名 (tiny, base, small, medium, large)
        language: 言語コード (例: ja, en) - オプション
    
    Returns:
        TranscriptionResponse: 文字起こし結果
    """
    # ファイル形式のチェック
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"サポートされていないファイル形式です: {file_ext}. "
                   f"サポート形式: {', '.join(SUPPORTED_FORMATS)}"
        )
    
    # 一時ファイルに保存
    temp_file = None
    temp_file_path: Optional[str] = None
    try:
        # 一時ファイルを作成 (自動削除しない)
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            # アップロードされたファイルを一時ファイルに書き込み
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        print(f"一時ファイルに保存: {temp_file_path}")
        print(f"ファイル名: {file.filename}")
        print(f"モデル: {model}")
        print(f"言語: {language or '自動検出'}")
        
        # 処理時間の計測開始
        start_time = time.time()
        
        # 言語が "auto" の場合は None に設定して自動検出を有効にする
        lang_param = None if language == "auto" else language

        # 文字起こし実行
        result = transcribe_audio(
            file_path=temp_file_path,
            model_name=model,
            language=lang_param
        )
        
        # 処理時間の計測終了
        processing_time = time.time() - start_time
        
        print(f"文字起こし完了: {processing_time:.2f}秒")
        
        # セグメント情報を整形
        segments = []
        if "segments" in result:
            for segment in result["segments"]:
                segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"]
                })
        
        # レスポンスを返す
        return TranscriptionResponse(
            text=result["text"],
            fileName=file.filename,
            processingTime=round(processing_time, 2),
            segments=segments if segments else None
        )
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"ファイルが見つかりません: {str(e)}")
    
    except ValueError as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"不正なパラメータ: {str(e)}")
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"エラーが発生しました: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文字起こし処理中にエラーが発生しました: {str(e)}")
    
    finally:
        # 一時ファイルを削除
        if temp_file and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                print(f"一時ファイルを削除: {temp_file_path}")
            except Exception as e:
                print(f"一時ファイルの削除に失敗: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
