"""CMD 參數：定義選項、預設值，並檢查輸入範圍。"""

import argparse
from pathlib import Path

from .drawing import COLORS

PROJECT_DIR = Path(__file__).resolve().parents[2]

def parse_args(argv=None):
    """解析 CMD 參數；argv=None 表示直接讀取本次命令列。"""
    # type 轉換輸入型別，default 是未填時的值，help 會顯示在 --help。
    # store_true：有填選項為 True，未填為 False。
    # append：可重複填寫，例如 --label "Object A" --label "Object B"。
    parser = argparse.ArgumentParser(description="圖片標註練習")
    parser.add_argument(
        "--save-preview",
        action="store_true",
        help="儲存原圖與標註圖的左右對照圖片",
    )
    parser.add_argument(
        "--jpg-quality",
        type=int,
        default=95,
        help="JPG 輸出品質，範圍為 0 到 100，預設為 95",
    )
    parser.add_argument(
        "--hide-confidence",
        action="store_true",
        help="圖片標籤只顯示名稱，不顯示信心分數",
    )
    parser.add_argument(
        "--font-scale",
        type=float,
        default=0.8,
        help="標籤文字大小比例，預設為 0.8",
    )
    parser.add_argument(
        "--line-thickness",
        type=int,
        default=3,
        help="方框粗細，單位為像素，預設為 3",
    )
    parser.add_argument(
        "--box-color",
        choices=list(COLORS),
        default="green",
        help="標註顏色，預設為 green",
    )
    parser.add_argument(
        "--min-area",
        type=int,
        default=0,
        help="方框最小面積，單位為平方像素，預設不限制",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="只保留分數最高的前 K 筆，預設不限制",
    )
    parser.add_argument(
        "--save-crops",
        action="store_true",
        help="將每個保留結果裁切成獨立圖片",
    )
    parser.add_argument(
        "--grayscale",
        action="store_true",
        help="使用灰階背景輸出標註圖片",
    )
    parser.add_argument(
        "--label",
        action="append",
        help="只保留指定名稱，可重複使用；預設保留所有名稱",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="允許覆寫同名的輸出檔案",
    )
    parser.add_argument(
        "--image",
        type=Path,
        default=PROJECT_DIR / "meme.jpg",
        help="輸入圖片路徑；相對路徑以終端機目前的資料夾為準",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="信心分數門檻，範圍為 0 到 1，預設為 0.5",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="輸出資料夾，預設自動建立 outputs/時間_識別碼",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="只儲存結果，不開啟圖片視窗",
    )
    args = parser.parse_args(argv)
    # 型別正確後還要檢查範圍；parser.error 會顯示原因並以代碼 2 結束。
    if not 0 <= args.jpg_quality <= 100:
        parser.error("--jpg-quality 必須介於 0 到 100")
    if not 0 < args.font_scale <= 5:
        parser.error("--font-scale 必須大於 0 且不超過 5")
    if args.line_thickness < 1:
        parser.error("--line-thickness 必須大於 0")
    if args.min_area < 0:
        parser.error("--min-area 不可小於 0")
    if args.top_k is not None and args.top_k < 1:
        parser.error("--top-k 必須是大於 0 的整數")
    if not 0 <= args.threshold <= 1:
        parser.error("--threshold 必須介於 0 到 1")
    return args
