# 程式架構：每個部分負責什麼？

目前已完成本機圖片標註及 JSON 讀寫，程式依用途拆成五個檔案，並保留中文註解。下方也保留未來線上服務的規劃，相關服務資料夾尚未建立。

## 目前的檔案分工

所有檔案位於 `src/vision_lab/`。先讀 `main.py` 掌握順序，需要修改某項功能時再查看負責的檔案。

| 檔案 | 負責內容 | 主要函式 |
| --- | --- | --- |
| `main.py` | 串接主流程、顯示視窗與摘要、處理錯誤 | `main()`、`cli()` |
| `cli.py` | 定義 CMD 參數及檢查合法範圍 | `parse_args()` |
| `detection.py` | 模擬結果與篩選 | `detect_objects()`、`filter_results()` |
| `drawing.py` | 標註顏色、畫框、文字與準備裁切 | `draw_label()`、`render_results()`、`prepare_crops()` |
| `exporter.py` | JSON／CSV／JPG 存檔與覆寫保護 | `save_results()`、`load_results()`、`save_csv()`、`save_image()`、`ensure_outputs_available()`、`save_crops()` |

依賴方向為 `main.py` 呼叫各功能模組；`cli.py` 使用 `drawing.py` 的顏色選項，`exporter.py` 使用 `drawing.py` 的裁切功能。各功能模組不會反過來匯入 `main.py`。

## 目前的執行流程

```text
解析 --threshold 參數（預設 0.5，範圍 0 到 1）
    ↓
讀取專案根目錄的 meme.jpg
    ↓
detect_objects：產生模擬資料並過濾分數
    ↓
render_results：在原圖副本畫框
    ↓
save_results → results.json → load_results
    ↓
render_results：使用讀回的結果重新畫框
    ↓
儲存 meme_boxed.jpg、meme_restored.jpg，顯示兩個視窗
```

`draw_label()` 負責單筆畫框與文字；`render_results()` 重複呼叫它處理整份結果。`main()` 負責串接整體流程，並在按鍵結束後清理視窗。

結果統一使用 `label`、`confidence`、`box` 三個欄位，`box` 依序是左、上、右、下的像素座標。預設讀取專案根目錄的圖片，每次輸出到新的 `outputs/時間_識別碼/`（電腦本地時間加上隨機識別碼）。指定的相對路徑以工作資料夾為準。預設保護既有輸出，只有 `--overwrite` 才允許覆寫同名檔案。

根目錄的 `run-vision.cmd` 先切換到專案資料夾，再使用 `.venv` 的 Python 執行主程式，預設啟用裁切、對照圖和不顯示視窗，門檻為 `0.4`。使用者可以附加參數，日常從 CMD 重跑並查看各次輸出即可。

`filter_results()` 先篩選名稱與面積，再取分數最高的前 K 筆。`prepare_crops()` 先驗證裁切範圍，`ensure_outputs_available()` 統一檢查包含裁切圖在內的所有預定輸出；檢查通過才開始寫入。所有 JPG 共用 `save_image()`，JSON 和 CSV 則各自使用專用函式。存檔不是交易式操作，磁碟寫入途中失敗仍可能留下部分結果。

`cli()` 是直接執行及安裝後 `vision-lab` 指令的共同入口，統一處理錯誤與結束代碼。所有參數說明見 [README](../README.md)。

`detect_objects()` 目前只產生固定名稱和分數的練習資料，位置依圖片尺寸計算，尚未執行 AI 辨識。

## 未來線上服務：一張圖片會經過哪些步驟？

```text
使用者上傳圖片
    ↓
後端接收圖片，檢查是否符合規定
    ↓
把圖片送到外部 AI 服務
    ↓
取得 AI 辨識結果
    ↓
整理成我們要顯示的內容
    ↓
把結果回傳給使用者
```

FastAPI 負責接收使用者的請求；HTTPX 負責和外部 AI 服務交換資料。這些功能目前都還沒寫。

## 未來的檔案分工

下列路徑都位於 `src/vision_lab/` 裡。

| 檔案或資料夾 | 白話說明 | 目前狀態 |
| --- | --- | --- |
| `main.py` | 串接本機流程，未來入口分工依服務需求調整 | 已拆分參數、辨識、繪圖與匯出模組 |
| `api/` | 接收上傳圖片、開始辨識等操作 | 尚未建立 |
| `services/` | 決定辨識要依照哪些步驟進行 | 尚未建立 |
| `clients/` | 專門和外部 AI 服務溝通 | 尚未建立 |
| `schemas/` | 規定送進來和回傳出去的資料要有哪些欄位 | 尚未建立 |
| `config.py` | 讀取 API Key 等服務設定 | 尚未建立 |

這樣分工後，未來更換 AI 服務商時，主要調整和對方溝通的部分，其他功能比較容易沿用。

帳號、辨識歷史和訂閱付款會在後面的開發階段加入。各階段目標見 [開發計畫](../FEATURES_ROADMAP.md)。
