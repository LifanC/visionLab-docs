# Vision Lab：AI 圖片辨識服務

這個專案要做一個可以上傳圖片、取得 AI 辨識結果的線上服務。

使用者上傳照片後，Python 程式會把圖片交給外部 AI 服務，再把辨識結果回傳給使用者。實際能辨識哪些內容，要等選定 AI 服務後確認。

API 可以理解成「兩個程式交換資料的管道」。SaaS 是讓使用者透過網路使用服務，之後可以加入帳號、使用次數限制和訂閱付款。

## 1. 目前可以做什麼？

目前已準備好專案設定、說明文件，以及一個簡單的程式入口。

**現在執行只會顯示 `main`，還不能上傳圖片、進行辨識或開啟網站。** AI 服務商也還沒選定。

## 2. 第一次使用：準備環境

電腦需要先安裝 Python 3.13 或以上版本。以下指令以 Python 3.13 為例。

在 VS Code 開啟這個專案，再開啟 PowerShell 終端機，依序執行：

```powershell
cd C:\A_TestSpring\visionLab-docs
py -3.13 --version
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

| 指令 | 白話說明 |
| --- | --- |
| `cd ...` | 切換到專案資料夾 |
| `py -3.13 --version` | 確認電腦能使用 Python 3.13 |
| `py -3.13 -m venv .venv` | 建立專案專用的 Python 環境，放在 `.venv` 資料夾 |
| `python.exe -m pip install -e .` | 安裝目前專案，以及它需要的套件 |

如果已有可用的 `.venv`，不用再建立一次，切換到專案資料夾後執行最後一行即可。這些指令直接使用 `.venv` 裡的 Python，不需要另外啟用環境。

`-e` 表示開發時可以直接修改 Python 檔案，不必每改一行就重新安裝。最後的 `.` 代表目前資料夾。

## 3. 平常怎麼執行？

完成第一次安裝後，在 PowerShell 執行：

```powershell
cd C:\A_TestSpring\visionLab-docs
.\.venv\Scripts\vision-lab.exe
```

目前會顯示以下文字，然後結束：

```text
main
```

看到這個結果，代表目前的程式入口可以執行。它還沒有啟動網站或呼叫 AI。

也可以直接指定 Python 檔案執行，結果相同：

```powershell
.\.venv\Scripts\python.exe .\src\vision_lab\main.py
```

如果找不到 `vision-lab.exe`，先確認已切換到專案資料夾，再重新安裝：

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

## 4. pyproject.toml 在設定什麼？

這是 Python 專案的設定檔，記錄名稱、Python 版本、需要的套件及執行指令。

| 套件 | 預計用途 |
| --- | --- |
| `fastapi[standard]` | 建立後端服務，接收圖片和使用者的操作 |
| `httpx` | 把資料送到外部 AI API，取得結果 |

選定 AI 服務後，再決定是否加入服務商提供的 Python 套件。

設定檔裡的這段：

```toml
[project.scripts]
vision-lab = "vision_lab.main:main"
```

意思是：「執行 `vision-lab` 指令時，去執行 `src/vision_lab/main.py` 裡的 `main()` 函式。」

左邊 `vision-lab` 是指令名稱；右邊 `vision_lab` 是 Python 套件資料夾名稱，因此一個使用連字號，另一個使用底線。

**修改套件清單或指令入口後，要重新執行安裝指令。** 舊的 `vision_lab` 指令已改名為 `vision-lab`。

## 5. 每個檔案放什麼？

沿用 `quant-flow-docs` 的方式，把 Python 程式放在 `src/` 裡。

```text
visionLab-docs/
├── .gitignore                  不要提交到 Git 的檔案清單
├── pyproject.toml              專案與套件設定
├── README.md                   安裝和執行說明（本文件）
├── FEATURES_ROADMAP.md         接下來要做的功能
├── docs/
│   ├── program-architecture.md  未來程式如何分工
│   └── learning-notes.md        額外的學習方向
└── src/
    └── vision_lab/
        ├── __init__.py         Python 套件的基本檔案
        └── main.py             目前的程式入口
```

`.venv/` 是專案專用環境；`*.egg-info/` 是安裝時產生的資料，都不需要提交到 Git。

未來 AI 的 API Key（呼叫服務用的金鑰）會透過環境變數提供。`.env` 可保存本機設定，已列入 Git 忽略清單；目前程式尚未加入讀取 `.env` 的功能。

## 6. 接下來看哪份文件？

- 想知道先做哪些功能：看 [開發計畫](./FEATURES_ROADMAP.md)。
- 想知道程式如何分工：看 [程式架構](./docs/program-architecture.md)。
- 想額外學習圖片處理或自行執行模型：看 [學習筆記](./docs/learning-notes.md)。
