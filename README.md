# Vision Lab：圖片標註與 AI 辨識練習

目前是本機執行的圖片標註練習，未來目標是串接外部 AI API，建立圖片辨識服務。

**目前沒有呼叫 AI，也沒有網站或圖片上傳功能。** `Object A`、`Object B` 的名稱、信心分數和位置都是模擬資料，不會依照圖片內容辨識物體。

## 1. 第一次使用

需要 Python 3.13 或以上版本。預設開啟桌面視窗，使用 `--no-show` 可只輸出檔案。在 CMD（命令提示字元）依序執行：

```cmd
cd /d C:\A_TestSpring\visionLab-docs
py -3.13 --version
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

如果已有可用的 `.venv`，可略過建立環境的指令。直接使用環境內的 Python，不需要另外啟用環境。

`pip install -e .` 會安裝專案及所需套件，包含 OpenCV。需要視窗功能時，請使用 `opencv-python`。更新套件設定或指令入口後，請重新執行安裝指令。

## 2. 準備圖片與執行

將一張有效的 JPG 圖片命名為 `meme.jpg`，放在專案根目錄，也就是與本文件相同的資料夾。

### 雙擊或用 CMD 執行

雙擊根目錄的 `run-vision.cmd` 即可執行。預設門檻為 `0.4`，輸出 JSON、CSV、兩張標註圖、物件裁切和左右對照圖；不開啟 OpenCV 視窗，執行完成後保留 CMD 視窗供查看訊息。

也可以在 CMD 執行，或附加參數：

```cmd
cd /d C:\A_TestSpring\visionLab-docs
run-vision.cmd
run-vision.cmd --threshold 0.5 --box-color red
run-vision.cmd --image "C:\My Photos\cat.jpg" --label "Object B"
```

CMD 會顯示本次輸出資料夾。打開其中的 `preview.jpg` 查看左右對照、`results.csv` 查看資料；每次執行自動建立新資料夾，可以修改程式或參數後直接重跑。啟動檔會先切換到專案根目錄，因此附加的相對路徑以專案根目錄為準。直接執行 Python 時則以 CMD 當前資料夾為準。

### 直接執行 Python

想顯示圖片視窗時，直接執行 Python（預設門檻為 `0.5`）：

```cmd
.\.venv\Scripts\python.exe .\src\vision_lab\main.py
```

程式會：

1. 從專案根目錄讀取 `meme.jpg`。
2. 產生模擬結果，依信心分數門檻過濾。
3. 畫框、加上英文名稱與分數，儲存 JSON 結果。
4. 讀回 JSON，在原圖副本上重新畫框。
5. 儲存兩張標註圖片，並顯示 `Boxed` 和 `Restored` 視窗。

兩個視窗應顯示相同的標註。點選任一圖片視窗後按任意鍵，程式就會關閉視窗並結束。

預設輸入是專案根目錄的圖片，輸出自動存入 `outputs/時間_識別碼/`；明確指定的相對路徑以終端機目前的資料夾為準。上述執行指令以專案根目錄為起點。

## 3. 調整信心分數門檻

```cmd
.\.venv\Scripts\python.exe .\src\vision_lab\main.py --threshold 0.5
.\.venv\Scripts\python.exe .\src\vision_lab\main.py --threshold 0.4
```

| 門檻 | 顯示的模擬結果 |
| --- | --- |
| `0.5`（預設） | Object A 92% |
| `0.4` | Object A 92%、Object B 45% |

分數等於門檻時會保留。參數必須介於 `0` 到 `1`；超出範圍時會顯示錯誤。可用以下指令查看說明：

```cmd
.\.venv\Scripts\python.exe .\src\vision_lab\main.py --help
```

安裝專案後，也可以用指令入口執行：

```cmd
.\.venv\Scripts\vision-lab.exe --threshold 0.4
```

如果找不到 `vision-lab.exe`，請重新執行 `pip install -e .` 的安裝指令。

## 4. 輸出檔案

預設每次建立新的 `outputs/時間_識別碼/` 資料夾，可用 `--output-dir` 指定固定資料夾。**預設拒絕覆寫同名輸出，確認要取代時才加上 `--overwrite`。** 所有預定輸出（包含裁切圖）會先檢查，再開始寫入；這不是交易式存檔，寫入途中若磁碟失敗，仍可能留下部分檔案。覆寫不會清除資料夾中其他既有檔案，例如前次產生而本次沒有使用的裁切圖。

| 檔案 | 內容 |
| --- | --- |
| `results.json` | 通過門檻的模擬結果 |
| `results.csv` | 相同結果的 CSV 表格，可用 Excel 開啟 |
| `meme_boxed.jpg` | 直接根據結果畫框的圖片 |
| `meme_restored.jpg` | 讀回 JSON 後重新畫框的圖片 |
| `crop_001.jpg` 等 | 加上 `--save-crops` 時，依結果順序裁切彩色原圖 |
| `preview.jpg` | 加上 `--save-preview` 時，左原圖、右標註圖的對照 |

JSON 最外層是清單，每一筆包含以下欄位：

| 欄位 | 意義 |
| --- | --- |
| `label` | 名稱，例如 `Object A` |
| `confidence` | 信心分數，例如 `0.92` |
| `box` | `[left, top, right, bottom]`，單位為像素 |

目前每次執行都會先產生並寫入 JSON，再重新讀取；還不能單獨載入既有結果執行還原。

### 完整參數

| 參數 | 預設／用途 |
| --- | --- |
| `--image PATH` | 專案根目錄的 `meme.jpg`；指定輸入圖片 |
| `--output-dir PATH` | 自動建立 `outputs/時間_識別碼/`；也可指定固定資料夾 |
| `--threshold NUMBER` | `0.5`，範圍 0 到 1，等於門檻也保留 |
| `--label NAME` | 不限制；完全相同的名稱才保留，可重複指定 |
| `--min-area INTEGER` | `0`；方框最小面積，單位為平方像素 |
| `--top-k INTEGER` | 不限制；篩選後保留分數最高的前 K 筆，K 必須大於 0 |
| `--grayscale` | 使用灰階背景，標註仍有顏色 |
| `--box-color COLOR` | `green`；可選 `green`、`red`、`blue` |
| `--line-thickness INTEGER` | `3`；方框粗細，必須大於 0 |
| `--font-scale NUMBER` | `0.8`；文字大小，必須大於 0 且不超過 5 |
| `--hide-confidence` | 圖片只顯示名稱；JSON、CSV 仍保留分數 |
| `--jpg-quality INTEGER` | `95`，範圍 0 到 100；套用所有 JPG 輸出 |
| `--save-crops` | 額外儲存每筆結果的原圖裁切 |
| `--save-preview` | 額外儲存左右對照圖 |
| `--overwrite` | 允許覆寫同名輸出，但不允許輸出覆蓋輸入圖片 |
| `--no-show` | 不顯示視窗、不等待按鍵 |

篩選順序為：分數 → 名稱與面積 → 分數排序並取前 K 筆。沒有結果時仍正常輸出：JSON 為空清單，CSV 只含欄位，標註圖沒有框。

整合範例：

```cmd
.\.venv\Scripts\python.exe .\src\vision_lab\main.py --image .\meme.jpg --threshold 0.4 --label "Object B" --top-k 1 --save-crops --save-preview --output-dir .\outputs\demo --no-show
```

正常完成的結束代碼為 `0`，圖片讀取或處理失敗為 `1`，參數錯誤為 `2`。CMD 可用 `echo %ERRORLEVEL%` 查看（請在執行後的下一行輸入）。摘要顯示圖片尺寸、筆數和處理耗時，耗時不包含等待視窗按鍵的時間。

## 5. 程式如何分工

程式已依用途拆分到 `src/vision_lab/`。建議先讀 `main.py`，需要了解細節時，再依下表查看對應檔案：

| 檔案 | 閱讀重點 |
| --- | --- |
| `main.py` | 整體步驟、視窗、執行摘要與錯誤處理 |
| `cli.py` | CMD 參數、預設值與輸入檢查 |
| `detection.py` | 模擬辨識、名稱／面積／前 K 筆篩選 |
| `drawing.py` | 色彩設定、畫框、文字與裁切範圍 |
| `exporter.py` | JSON、CSV、JPG 存檔與覆寫保護 |

`run-vision.cmd` 和原本直接執行 `main.py` 的指令都可繼續使用。各函式用途如下：

| 函式 | 負責的工作 |
| --- | --- |
| `draw_label()` | 在圖片上畫一個框和文字 |
| `detect_objects()` | 產生模擬結果並過濾分數，尚未接入 AI |
| `render_results()` | 複製圖片，逐筆畫出結果並回傳圖片 |
| `save_results()` | 將結果寫入 JSON |
| `load_results()` | 讀取 JSON 並回傳結果 |
| `parse_args()` | 解析並驗證命令列參數 |
| `filter_results()` | 依名稱、面積及前 K 筆篩選 |
| `prepare_crops()` / `save_crops()` | 驗證裁切範圍／獨立儲存裁切圖 |
| `ensure_outputs_available()` | 檢查同名輸出和資料夾衝突 |
| `save_image()` / `save_csv()` | 統一 JPG 輸出／CSV 匯出 |
| `main()` | 解析參數，安排讀圖、處理、存檔與視窗顯示 |
| `cli()` | 直接執行與安裝指令共用的錯誤處理入口 |

`pyproject.toml` 記錄專案名稱、Python 版本、套件需求，以及 `vision-lab` 指令入口。FastAPI 和 HTTPX 已列為套件需求，目前圖片標註流程尚未使用它們。

## 6. 常見問題

- **`No module named 'cv2'`**：用 `.\.venv\Scripts\python.exe -m pip install opencv-python` 安裝到專案環境。
- **讀不到圖片**：依終端機提示的完整路徑檢查圖片；確認不是 `meme.jpg.jpg`，且檔案確實為有效圖片。
- **圖片儲存失敗**：程式會拋出錯誤並顯示輸出路徑，請檢查資料夾是否可寫入。
- **無法開啟視窗**：視窗需要桌面環境及支援 GUI 的 OpenCV；只想存檔時加上 `--no-show`。
- **辨識名稱和圖片內容無關**：這是預期行為，目前使用固定的模擬結果。

## 7. 接下來看哪份文件

日常手動確認：執行 `run-vision.cmd`，查看本次資料夾中的圖片與 CSV，再調整參數重跑。專案不另外加入測試檔或測試框架。

- [開發計畫](./FEATURES_ROADMAP.md)：目前進度與後續功能。
- [程式架構](./docs/program-architecture.md)：目前函式分工與未來服務架構。
- [學習筆記](./docs/learning-notes.md)：圖片處理與模型的延伸學習方向。
