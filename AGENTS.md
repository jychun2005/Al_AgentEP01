# 專案：用 Agent 來學習 Agent

## 技術棧
- Python + yt-dlp
- Python + Obsidian
- Python + Web

## 專案概述
從 sensebar YouTube 頻道提取字幕，建立結構化的三層 Obsidian 第二大腦知識庫，
並用於自動化教案/課程規劃。

## 目錄結構
- `extract_videos.py` — 過濾頻道影片並提取 URL
- `download_all_subs.py` — 下載字幕並清理 VTT
- `sensebar_ai_urls.txt` — 影片 URL 列表
- `sensebar_ai_videos.md` — 影片資訊
- `subtitles/` — 清理後的字幕 Markdown 檔案
- `Clipping/` — Obsidian 外部來源層
- `創作庫/` — Obsidian 創作庫層
- `知識庫/` — Obsidian 知識庫層

## Obsidian Vault
尚未建立，可於後續手動建立。

## 排程任務
每週執行知識重構：
1. 掃描 Clipping/ 和 創作庫/ 的新檔案
2. 摘要提煉關鍵字與主題
3. 寫入對應的 知識庫/ 資料夾
4. 執行健康檢查（矛盾、連結錯誤）
5. 更新全域 Index 與 Log
