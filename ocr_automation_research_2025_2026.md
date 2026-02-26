# 2025-2026 最新 OCR 自動化開源專案研究報告

## 專案概覽（依 Stars 排序）

---

## 🥇 第一梯隊：高 Stars 明星專案

### 1. **RAGFlow** ⭐ 73,707
- **連結**: https://github.com/infiniflow/ragflow
- **主要特色**: 
  - 頂級開源 RAG (Retrieval-Augmented Generation) 引擎
  - 結合 RAG + Agent 能力
  - 完整文檔處理 pipeline：解析、分塊、嵌入、檢索
  - 支援多種文檔格式（PDF、Word、Excel、圖片等）
  - Docker 一鍵部署
- **適用場景 (BNI 報表)**:
  - ✅ 非常適合：結構化報表數據提取、批次處理多份文件
  - ✅ 支援表格識別和數字精確提取
- **部署難度**: ⭐⭐⭐ 中等（需 Docker，有完整文檔）
- **語言**: Python

---

### 2. **PaddleOCR** ⭐ 71,177
- **連結**: https://github.com/PaddlePaddle/PaddleOCR
- **主要特色**:
  - 百度開發的多語言 OCR 工具包
  - 支援 80+ 語言
  - 文本檢測 + 識別 + 版面分析 + 表格識別
  - 超輕量級模型（適合邊緣設備）
  - 支援自訂訓練
- **適用場景 (BNI 報表)**:
  - ✅ 適合：中文報表處理、數字識別
  - ✅ 表格結構識別功能強大
- **部署難度**: ⭐⭐ 容易（pip 安裝，多平台支援）
- **語言**: Python

---

### 3. **Tesseract** ⭐ 72,552
- **連結**: https://github.com/tesseract-ocr/tesseract
- **主要特色**:
  - Google 開發的經典 OCR 引擎
  - 歷史悠久，穩定可靠
  - 支援 100+ 語言
  - 支援 LSTM 深度學習模型
  - 可訓練自訂字體
- **適用場景 (BNI 報表)**:
  - ⚠️ 基礎 OCR 使用，需配合其他工具處理版面
  - 適合數字識別但需要額外處理表格結構
- **部署難度**: ⭐⭐ 容易（多平台二進制包）
- **語言**: C++

---

### 4. **Marker** ⭐ ~20,000+ (估計)
- **連結**: https://github.com/VikParuchuri/marker
- **主要特色**:
  - **專門針對 PDF → Markdown 轉換**
  - 支援 PDF、圖片、PPTX、DOCX、XLSX、HTML、EPUB
  - 表格、公式、內聯數學、連結、參考文獻格式化
  - 自動移除頁首頁尾
  - **支援 LLM 增強模式**（使用 Gemini/Ollama）
  - 批次處理速度：H100 可達 25 頁/秒
- **適用場景 (BNI 報表)**:
  - ✅ **極度推薦**：專為報表數字追蹤設計
  - ✅ 表格識別準確率高
  - ✅ 可輸出結構化 JSON
- **部署難度**: ⭐⭐⭐ 中等（Python 3.10+、PyTorch）
- **語言**: Python
- **授權**: GPL（商業使用需付費授權）

---

### 5. **MinerU** ⭐ 54,992
- **連結**: https://github.com/opendatalab/MinerU
- **主要特色**:
  - **專為 LLM 訓練數據準備設計**
  - 複雜 PDF → Markdown/JSON 轉換
  - 自動移除頁首頁尾、頁碼
  - 人類閱讀順序輸出（支援多欄位、複雜版面）
  - **科學文獻符號轉換專家**
  - 支援多種國產 GPU（華為昇騰、海光、寒武紀等）
  - Hybrid 模式：結合傳統 pipeline + VLM
- **適用場景 (BNI 報表)**:
  - ✅ **推薦**：複雜版面報表處理
  - ✅ 多欄位報表識別
- **部署難度**: ⭐⭐⭐ 中等（Docker 可用）
- **語言**: Python

---

### 6. **Paperless-ngx** ⭐ 36,934
- **連結**: https://github.com/paperless-ngx/paperless-ngx
- **主要特色**:
  - 完整的文檔管理系統（DMS）
  - 掃描、索引、歸檔一體化
  - OCR 自動化 + 全文檢索
  - 標籤、分類、工作流程
  - 現代化 Web UI
- **適用場景 (BNI 報表)**:
  - ✅ 適合：需要長期存檔和檢索的報表管理
  - ⚠️ 偏重文檔管理而非單純 OCR 提取
- **部署難度**: ⭐⭐⭐⭐ 較難（Docker Compose 多服務）
- **語言**: Python

---

### 7. **OCRmyPDF** ⭐ 32,764
- **連結**: https://github.com/ocrmypdf/OCRmyPDF
- **主要特色**:
  - 為掃描 PDF 添加 OCR 文字層
  - 保留原始 PDF 品質
  - 基於 Tesseract
  - 支援 PDF/A 歸檔標準
- **適用場景 (BNI 報表)**:
  - ⚠️ 主要用於「使 PDF 可搜尋」，非結構化數據提取
- **部署難度**: ⭐⭐ 容易
- **語言**: Python

---

## 🥈 第二梯隊：新興高潛力專案

### 8. **olmOCR** ⭐ 16,942 (2025 新發布)
- **連結**: https://github.com/allenai/olmocr
- **主要特色**:
  - **Allen AI (AI2) 開發**
  - 基於 7B 參數 VLM 的端到端 OCR
  - PDF、PNG、JPEG → Markdown
  - **支援方程式、表格、手寫、複雜格式**
  - 自動移除頁首頁尾
  - **成本效益：每百萬頁 <$200**
  - 自帶評測基準 olmOCR-Bench
- **適用場景 (BNI 報表)**:
  - ✅ **高度推薦**：表格識別準確率高
  - ✅ 處理複雜數字格式
- **部署難度**: ⭐⭐⭐⭐ 較難（需 GPU、Docker 支援）
- **語言**: Python
- **注意**: 需要 GPU（基於 VLM）

---

### 9. **Unstructured** ⭐ 14,056
- **連結**: https://github.com/Unstructured-IO/unstructured
- **主要特色**:
  - 企業級文檔處理 ETL 工具
  - 支援 10+ 種文檔格式
  - 專為 LLM 應用設計的數據清洗
  - 提供商用雲端服務
  - 靈活的分塊策略
- **適用場景 (BNI 報表)**:
  - ✅ 適合：需要複雜預處理的報表數據
  - ✅ 企業級應用
- **部署難度**: ⭐⭐⭐ 中等（Docker 可用）
- **語言**: Python

---

### 10. **Zerox** ⭐ 12,143
- **連結**: https://github.com/getomni-ai/zerox
- **主要特色**:
  - **極簡 Vision Model OCR**
  - PDF/圖片 → 轉換為圖片序列 → GPT Vision → Markdown
  - 支援 OpenAI、Azure、AWS Bedrock、Google Gemini
  - TypeScript + Python 雙版本
  - 並發處理支援
- **適用場景 (BNI 報表)**:
  - ✅ 適合：已經使用 OpenAI/Gemini API 的場景
  - ⚠️ 依賴外部 API，成本需考量
- **部署難度**: ⭐⭐ 容易（pip/npm 安裝）
- **語言**: TypeScript/Python

---

### 11. **Docling** ⭐ ~10,000+ (IBM 開發)
- **連結**: https://github.com/DS4SD/docling
- **主要特色**:
  - **IBM 開源的文檔處理工具**
  - 多種格式支援：PDF、DOCX、PPTX、XLSX、HTML、圖片、LaTeX
  - 進階 PDF 理解：版面、閱讀順序、表格、公式、圖片分類
  - 匯出 Markdown、HTML、JSON
  - **本地執行，資料不外洩**
  - 支援 Visual Language Models (GraniteDocling)
  - MCP Server 支援 Agentic AI
- **適用場景 (BNI 報表)**:
  - ✅ **推薦**：資料隱私要求高
  - ✅ 表格和數字提取準確
- **部署難度**: ⭐⭐ 容易（pip install docling）
- **語言**: Python

---

### 12. **Surya** ⭐ ~8,000+
- **連結**: https://github.com/VikParuchuri/surya
- **主要特色**:
  - Marker 的底層 OCR 引擎
  - 90+ 語言 OCR
  - 行級文字檢測
  - 版面分析（表格、圖片、頁首頁尾）
  - 閱讀順序檢測
  - 表格識別（行列檢測）
  - LaTeX OCR
- **適用場景 (BNI 報表)**:
  - ✅ 可作為 Marker 的輕量替代
  - ✅ 適合多語言報表
- **部署難度**: ⭐⭐⭐ 中等
- **語言**: Python

---

### 13. **Nougat** ⭐ 9,847 (Meta/Facebook)
- **連結**: https://github.com/facebookresearch/nougat
- **主要特色**:
  - **學術文檔 PDF 解析專家**
  - 專門處理 LaTeX 數學和表格
  - 基於 Transformer 架構
  - 理解學術文檔結構
- **適用場景 (BNI 報表)**:
  - ⚠️ 專為學術論文設計，一般報表可能過於專門
- **部署難度**: ⭐⭐⭐ 中等
- **語言**: Python

---

## 🥉 第三梯隊：專用工具

### 14. **text-extract-api** ⭐ 2,981
- **連結**: https://github.com/CatchTheTornado/text-extract-api
- **主要特色**:
  - FastAPI + Celery 異步處理
  - 本地部署，無雲端依賴
  - 整合多種 OCR：EasyOCR、Marker、Llama Vision
  - PDF → Markdown/JSON
  - PII 去除功能
  - Redis 快取
- **適用場景 (BNI 報表)**:
  - ✅ 適合：需要 API 介面的批次處理
  - ✅ 自托管需求
- **部署難度**: ⭐⭐⭐⭐ 較難（需 Docker Compose）
- **語言**: Python

---

### 15. **LLM-aided OCR** ⭐ 2,867
- **連結**: https://github.com/Dicklesworthstone/llm_aided_ocr
- **主要特色**:
  - Tesseract OCR + LLM 錯誤修正
  - 智慧文本分塊
  - 本地或 API LLM 支援
- **適用場景 (BNI 報表)**:
  - ✅ 適合：對準確率要求極高，願意犧牲速度
- **部署難度**: ⭐⭐⭐ 中等
- **語言**: Python

---

### 16. **OCRFlux** ⭐ 2,484
- **連結**: https://github.com/chatdoc-com/OCRFlux
- **主要特色**:
  - 輕量級多模態 PDF → Markdown 工具包
  - 針對表格和版面優化
- **適用場景 (BNI 報表)**:
  - ✅ 輕量級選擇
- **部署難度**: ⭐⭐⭐ 中等
- **語言**: Python

---

## 📊 專案比較總表

| 專案 | Stars | 最佳用途 | BNI 報表適合度 | 部署難度 | GPU 需求 |
|------|-------|----------|----------------|----------|----------|
| **RAGFlow** | 73K | 完整 RAG pipeline | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 建議有 |
| **Marker** | 20K | PDF → Markdown | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 可選 |
| **MinerU** | 55K | 複雜 PDF 解析 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 可選 |
| **olmOCR** | 17K | AI 驅動 OCR | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 必需 |
| **Docling** | 10K | IBM 企業級 | ⭐⭐⭐⭐ | ⭐⭐ | 無 |
| **Zerox** | 12K | Vision API 方案 | ⭐⭐⭐ | ⭐⭐ | 無 |
| **Unstructured** | 14K | 企業 ETL | ⭐⭐⭐⭐ | ⭐⭐⭐ | 無 |
| **PaddleOCR** | 71K | 中文多語言 | ⭐⭐⭐⭐ | ⭐⭐ | 可選 |

---

## 🎯 BNI 報表數字追蹤推薦方案

### 推薦順序（綜合考量）

#### 🥇 首選：**Marker** 或 **Docling**
- Marker: 專門為 PDF → Markdown/JSON 設計，表格識別強
- Docling: IBM 出品，穩定可靠，本地執行保護隱私

#### 🥈 次選：**MinerU**
- 複雜版面處理能力強
- 多欄位報表識別準確

#### 🥉 AI 強化：**olmOCR**
- 最新 VLM 技術，準確率最高
- 需 GPU，成本較高但效果最佳

---

## 🔧 部署建議

### 快速原型（< 1 小時）
```bash
# 推薦：Docling
pip install docling
docling https://example.com/report.pdf

# 或 Marker
pip install marker-pdf
marker_single /path/to/report.pdf
```

### 生產環境
- **Docker 部署**: RAGFlow、MinerU、Unstructured
- **自托管 API**: text-extract-api
- **GPU 伺服器**: olmOCR、Marker (batch mode)

---

## 📚 相關討論來源

### Reddit 社群推薦
- r/MachineLearning: Marker、olmOCR 近期熱門
- r/selfhosted: Paperless-ngx、RAGFlow

### Hacker News 趨勢
- olmOCR (2025-02 發布) 討論熱烈
- MinerU 中文社群支持度高

---

*報告生成時間: 2026-02-26*
*資料來源: GitHub API、專案 README*
